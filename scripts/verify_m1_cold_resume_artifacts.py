#!/usr/bin/env python3
"""Verify retained M1 diagnostic data without importing or running its runtime."""
from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import tarfile
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "artifacts/m1_cold_resume_diagnostic_20261001"
ANCHORS = ROOT / "protocols/m1_cold_resume_artifact_anchors_v1.json"
ANCHORS_SHA256 = "921f0c86668f706ee058615bc3f04e3c46a80482c29715598fcc10ea937f7fa3"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def load_anchors() -> dict[str, Any]:
    """Use reviewed repository anchors, never a transport-supplied trust root."""
    raw = ANCHORS.read_bytes()
    if sha(raw) != ANCHORS_SHA256:
        raise ValueError("frozen artifact anchors digest mismatch")
    return json.loads(raw)


def verify_inventory(files: dict[str, bytes], anchor: dict[str, Any]) -> None:
    actual = {name: sha(raw) for name, raw in files.items()}
    if actual != anchor["raw_files_sha256"]:
        raise ValueError("frozen raw inventory or file digests mismatch")
    expected = json.loads(files["inventory.json"])
    if {name: digest for name, digest in actual.items() if name != "inventory.json"} != expected:
        raise ValueError("internal raw inventory or file digests mismatch")


def read_bundle(parts: Path, identity: str) -> tuple[dict[str, bytes], str]:
    anchor = load_anchors()["attempts"][identity]
    manifest = json.loads((parts / "manifest.json").read_bytes())
    rows = manifest["parts"]
    expected_names = {"manifest.json"} | {row["path"] for row in rows}
    if {p.name for p in parts.iterdir()} != expected_names:
        raise ValueError("transport inventory mismatch")
    chunks = []
    for index, row in enumerate(rows):
        if row["path"] != f"part-{index:03d}.b64":
            raise ValueError("transport part order/path mismatch")
        raw = (parts / row["path"]).read_bytes()
        if sha(raw) != row["sha256"]:
            raise ValueError("transport part digest mismatch")
        chunks.append(base64.b64decode(raw.strip(), validate=True))
    payload = b"".join(chunks)
    if len(payload) != manifest["archive_bytes"] or sha(payload) != manifest["archive_sha256"]:
        raise ValueError("reconstructed archive digest/size mismatch")
    if len(payload) != anchor["archive_bytes"] or sha(payload) != anchor["archive_sha256"]:
        raise ValueError("frozen archive digest/size mismatch")
    files = {}
    total = 0
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:*") as archive:
        for member in archive:
            path = PurePosixPath(member.name)
            if not member.isfile() or path.is_absolute() or ".." in path.parts:
                raise ValueError("unsafe archive member")
            if member.name in files:
                raise ValueError("duplicate archive member")
            total += member.size
            if total > 64 * 1024 * 1024:
                raise ValueError("archive exceeds frozen output cap")
            stream = archive.extractfile(member)
            assert stream is not None
            files[member.name] = stream.read()
    verify_inventory(files, anchor)
    return files, sha(payload)


def verify_provenance(files: dict[str, bytes], identity: str) -> None:
    anchors = load_anchors()
    anchor = anchors["attempts"][identity]
    protocol = json.loads(files["protocol.json"])
    version = anchor["protocol_version"]
    if files["protocol.json"] != (ROOT / "protocols" /
                                   f"m1_cold_resume_diagnostic_v{version}.json").read_bytes():
        raise ValueError("frozen protocol bytes mismatch")
    provenance = anchor["provenance"]
    if sha(files["protocol.json"]) != provenance["protocol_sha256"]:
        raise ValueError("frozen protocol digest mismatch")
    if protocol["runtime_source_commit"] != anchors["runtime_source_commit"]:
        raise ValueError("frozen runtime source commit mismatch")
    expected = {**provenance, "protocol": protocol,
                "runtime_source_files_sha256": anchors["runtime_source_files_sha256"],
                "schema_assets_sha256": anchors["schema_assets_sha256"]}
    if canonical(json.loads(files["STARTED.json"])) != canonical(expected):
        raise ValueError("top-level execution provenance mismatch")
    cases = [("baseline", "baseline", 0, 1), ("observed", "observed", 0, 1)]
    cases += [(f"restore-{seed}-{cut}", "restore", cut, seed)
              for seed in (1, 37) for cut in (2, 7, 15)]
    cases.append(("secondary", "secondary", 7, 1))
    pids, parents = set(), set()
    for name, mode, cut, seed in cases:
        started = json.loads(files[f"{name}/STARTED.json"])
        for key in ("pid", "parent_pid"):
            if type(started[key]) is not int or started[key] <= 0:
                raise ValueError("invalid worker process provenance")
        pids.add(started["pid"])
        parents.add(started["parent_pid"])
        common = {key: provenance[key] for key in (
            "protocol_sha256", "runner_sha256", "python", "executable", "platform")}
        expected_worker = {**common, "mode": mode, "cut": cut, "hashseed": str(seed),
                           "reference_timeline": "observed" if cut else None,
                           "pid": started["pid"], "parent_pid": started["parent_pid"]}
        if canonical(started) != canonical(expected_worker):
            raise ValueError(f"worker execution provenance mismatch: {name}")
        if sha(files[f"{name}/config.json"]) != anchor["worker_config_sha256"]:
            raise ValueError(f"frozen worker configuration mismatch: {name}")
    if len(pids) != len(cases) or len(parents) != 1 or pids & parents:
        raise ValueError("worker process identity mismatch")


def snapshot(files: dict[str, bytes], prefix: str) -> dict[str, bytes]:
    return {name.removeprefix(prefix): raw for name, raw in files.items()
            if name.startswith(prefix)}


def rows(files: dict[str, bytes], name: str) -> list[dict[str, Any]]:
    return [json.loads(line) for line in files[name].splitlines()]


def verify(root: Path) -> dict[str, Any]:
    if not __debug__:
        raise RuntimeError("artifact verification requires Python without -O")
    original, original_archive = read_bundle(root / "original.parts", "original")
    corrected, corrected_archive = read_bundle(root / "corrected.parts", "corrected")
    verify_provenance(original, "original")
    verify_provenance(corrected, "corrected")
    old_summary = json.loads(original["summary.json"])
    summary = json.loads(corrected["summary.json"])
    assert old_summary["recorded_committed_cycles"] == 54
    assert old_summary["primary_status"] == "not_pass"
    assert summary["recorded_committed_cycles"] == 144
    assert summary["primary_status"] == "pass" and summary["primary_failures"] == []
    protocol = json.loads(corrected["protocol.json"])
    assert protocol["horizon"] == 24 and protocol["cutpoints"] == [2, 7, 15]
    assert protocol["restore_hashseeds"] == [1, 37] and protocol["model_seed"] == 31
    assert protocol["amendment"]["maximum_cumulative_primary_commits"] == 198
    primary_rows = sum(len(rows(corrected, name)) for name in corrected
                       if name.endswith("/cycles.jsonl"))
    assert primary_rows == 144
    observed = rows(corrected, "observed/cycles.jsonl")
    assert [row["step"] for row in observed] == list(range(1, 25))
    assert canonical(observed) == canonical(rows(corrected, "baseline/cycles.jsonl"))
    assert corrected["observed/cycles.jsonl"] == original["observed/cycles.jsonl"]
    assert corrected["baseline/cycles.jsonl"] == original["baseline/cycles.jsonl"]
    final = "checkpoints/step-024/"
    assert snapshot(corrected, "baseline/" + final) == snapshot(corrected, "observed/" + final)
    assert len(snapshot(corrected, "observed/" + final)) == 6
    resumed = 0
    pids = []
    original_checked = 0
    for seed in (1, 37):
        for cut in (2, 7, 15):
            case = f"restore-{seed}-{cut}"
            start = json.loads(corrected[f"{case}/STARTED.json"])
            assert start["hashseed"] == str(seed) and start["cut"] == cut
            pids.append(start["pid"])
            expected = observed[cut:]
            actual = rows(corrected, f"{case}/cycles.jsonl")
            assert canonical(actual) == canonical(expected)
            resumed += len(actual)
            for step in (cut, 24):
                checkpoint = f"checkpoints/step-{step:03d}/"
                assert len(snapshot(corrected, "observed/" + checkpoint)) == 6
                assert snapshot(corrected, case + "/" + checkpoint) == snapshot(
                    corrected, "observed/" + checkpoint)
            record_names = {name for name in corrected if name.startswith(case + "/file-records/")}
            assert record_names == {f"{case}/file-records/step-{step:03d}.json"
                                    for step in range(cut + 1, 25)}
            for step in range(cut + 1, 25):
                checkpoint = f"observed/checkpoints/step-{step:03d}/"
                saved = snapshot(corrected, checkpoint)
                assert len(saved) == 6
                recorded = json.loads(corrected[f"{case}/file-records/step-{step:03d}.json"])
                assert recorded == {name: sha(raw) for name, raw in saved.items()}
            old = json.loads(original[f"{case}/transition-mismatch.json"])
            assert canonical(old["left"]) == canonical(old["right"])
            assert len(snapshot(original, case + "/transition-mismatch-checkpoint/")) == 6
            assert snapshot(original, case + "/transition-mismatch-checkpoint/") == snapshot(
                original, f"observed/checkpoints/step-{cut + 1:03d}/")
            original_checked += 1
    assert resumed == 96 and len(set(pids)) == 6
    secondary = json.loads(corrected["secondary/secondary.json"])
    assert secondary["deepcopy"]["supported"] is False
    assert secondary["deepcopy"]["error_type"] == "TypeError"
    assert secondary["pending_roundtrip"]["equal"] is True
    assert secondary["automatic_cycle"]["rejected"] is True
    assert secondary["automatic_cycle"]["committed_cycles"] == 0
    assert secondary["automatic_cycle_no_write"]["equal"] is True
    pending = snapshot(corrected, "secondary/pending/")
    assert pending == snapshot(corrected, "secondary/pending-roundtrip/")
    assert pending == snapshot(corrected, "secondary/pending-after-cycle/")
    return {"status": "verified_without_runtime_execution", "primary_commits": primary_rows,
            "resumed_transitions": resumed, "original_preserved_commits": 54,
            "total_primary_commits": 198, "original_harness_mismatches_rechecked": original_checked,
            "cold_processes": len(set(pids)), "primary_snapshot_comparisons": 103,
            "original_archive_sha256": original_archive,
            "corrected_archive_sha256": corrected_archive, "scientific_credit": 0}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path, default=DEFAULT)
    args = parser.parse_args()
    print(json.dumps(verify(args.artifacts), sort_keys=True))
