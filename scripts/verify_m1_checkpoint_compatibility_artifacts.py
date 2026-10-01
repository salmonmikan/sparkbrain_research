#!/usr/bin/env python3
"""Verify the one retained compatibility matrix using data only, never a runtime."""
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
DEFAULT = ROOT / "artifacts/m1_checkpoint_compatibility_20261001"
ANCHORS = ROOT / "protocols/m1_checkpoint_compatibility_artifact_anchors_v1.json"
ANCHORS_SHA256 = "a370ff202cef218e11889a3959cac73892c13ff7ea5576242621712c0bac2ef8"
EXPECTED_ERRORS = {
    "C03": "unsupported M1 checkpoint identity",
    "C05": "unsupported pilot checkpoint schema or build id",
    "C06": "unsupported direct checkpoint schema",
    "C07": "unsupported BUILD-SB-002 checkpoint identity",
    "C08": "unsupported M1 compositor state identity",
    "C09": "pilot config has unexpected fields",
    "C10": "router config does not match checkpoint config",
}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode()


def anchors() -> dict[str, Any]:
    raw = ANCHORS.read_bytes()
    if sha(raw) != ANCHORS_SHA256:
        raise ValueError("frozen external anchor digest mismatch")
    return json.loads(raw)


def read_bundle(root: Path) -> dict[str, bytes]:
    fixed = anchors()
    parts = root / "run.parts"
    manifest = json.loads((parts / "manifest.json").read_bytes())
    names = {"manifest.json"} | {row["path"] for row in manifest["parts"]}
    if {p.name for p in parts.iterdir()} != names:
        raise ValueError("transport inventory mismatch")
    chunks = []
    for index, row in enumerate(manifest["parts"]):
        if row["path"] != f"part-{index:03d}.b64":
            raise ValueError("transport part order mismatch")
        raw = (parts / row["path"]).read_bytes()
        if sha(raw) != row["sha256"]:
            raise ValueError("transport part digest mismatch")
        chunks.append(base64.b64decode(raw.strip(), validate=True))
    payload = b"".join(chunks)
    for expected in (manifest, fixed):
        if sha(payload) != expected["archive_sha256"] or len(payload) != expected["archive_bytes"]:
            raise ValueError("frozen archive digest/size mismatch")
    # Repackaged directories also contain standalone copies. Legacy committed
    # transport may omit them, but every present representation must be verified.
    for name, expected in (("run.tar.xz", payload), ("anchors.json", ANCHORS.read_bytes())):
        path = root / name
        if path.exists() or path.is_symlink():
            if path.is_symlink() or not path.is_file():
                raise ValueError(f"standalone package copy is not a regular file: {name}")
            if path.read_bytes() != expected:
                raise ValueError(f"standalone package copy mismatch: {name}")
    files = {}
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:*") as archive:
        for entry in archive:
            path = PurePosixPath(entry.name)
            if (not entry.isfile() or path.is_absolute() or ".." in path.parts
                    or entry.name in files):
                raise ValueError("unsafe or duplicate archive member")
            source = archive.extractfile(entry)
            if source is None:
                raise ValueError("missing member bytes")
            files[entry.name] = source.read()
    actual = {name: sha(raw) for name, raw in files.items()}
    if actual != fixed["raw_files_sha256"]:
        raise ValueError("frozen complete raw inventory mismatch")
    internal = json.loads(files["inventory.json"])
    if {n: h for n, h in actual.items() if n != "inventory.json"} != internal:
        raise ValueError("internal inventory mismatch")
    return files


def subset(files: dict[str, bytes], prefix: str) -> dict[str, bytes]:
    return {name.removeprefix(prefix): raw for name, raw in files.items()
            if name.startswith(prefix)}


def digests(files: dict[str, bytes]) -> dict[str, str]:
    return {name: sha(raw) for name, raw in files.items()}


def expected_mutant(original: dict[str, bytes], case: dict[str, Any]) -> dict[str, bytes]:
    result = dict(original)
    if case["mutation_path"] == "none":
        return result
    relative, suffix = case["mutation_path"].split(".json/", 1)
    relative += ".json"
    value = json.loads(result[relative])
    owner = value
    keys = suffix.split("/")
    for key in keys[:-1]:
        owner = owner[key]
    if case["mutation_value"] == "DELETE":
        del owner[keys[-1]]
    else:
        owner[keys[-1]] = case["mutation_value"]
    if case["case_id"] == "C06":
        value["payload_hash"] = sha(canonical({k: v for k, v in value.items()
                                               if k != "payload_hash"}))
    if case["case_id"] in {"C07", "C10"}:
        value["payload_sha256"] = sha(canonical(value["payload"]))
    result[relative] = canonical(value) + b"\n"
    if relative != "manifest.json":
        manifest = json.loads(result["manifest.json"])
        manifest["files"][relative] = sha(result[relative])
        result["manifest.json"] = canonical(manifest) + b"\n"
    return result


def journal(files: dict[str, bytes], prefix: str) -> list[dict[str, Any]]:
    events = [json.loads(line) for line in files[prefix + "milestones.jsonl"].splitlines()]
    assert events == json.loads(files[prefix + "milestones.json"])
    stack = []
    for event in events:
        if event["event"] == "call_intent":
            stack.append((event["phase"], event["name"]))
        else:
            assert event["event"] in {"return", "error"}
            assert stack.pop() == (event["phase"], event["name"])
    assert not stack
    return events


def completed(events: list[dict[str, Any]], name: str,
              phase: str | None = None) -> list[dict[str, Any]]:
    return [e for e in events if e["name"] == name and e["event"] in {"return", "error"}
            and (phase is None or e["phase"] == phase)]


def check_stages(events: list[dict[str, Any]], case: str) -> None:
    primary = [e for e in events if e["phase"] == "primary-load"]
    found = {(e["name"], e["event"]) for e in primary}
    required, absent = [], []
    if case in {"C01", "C02", "C04"}:
        required = [(name, "return") for name in (
            "direct_reconstruct", "predictive_restore", "scope_restore", "compositor_restore",
            "world_restore", "session_construct", "integrated_load")]
    elif case == "C03":
        assert [(e["name"], e["event"]) for e in primary] == [
            ("integrated_load", "call_intent"), ("integrated_load", "error")]
    elif case in {"C05", "C09"}:
        required = [("direct_reconstruct", "return"), ("predictive_restore", "error")]
        absent = ["predictive_construct", "scope_load"]
    elif case == "C06":
        required = [("direct_reconstruct", "error")]
        absent = ["predictive_restore", "scope_load"]
    elif case == "C07":
        required = [("predictive_restore", "return"), ("scope_restore", "error")]
        absent = ["scope_construct", "compositor_construct"]
    elif case == "C08":
        required = [("scope_restore", "return"), ("compositor_construct", "return"),
                    ("compositor_restore", "error")]
        absent = ["world_restore", "session_construct"]
    elif case == "C10":
        required = [("scope_construct", "return"), ("router_restore", "return"),
                    ("scope_restore", "error")]
        absent = ["compositor_construct", "world_restore", "session_construct"]
    assert all(pair in found for pair in required)
    assert not any(name in absent for name, _ in found)


def verify(root: Path = DEFAULT) -> dict[str, Any]:
    if not __debug__:
        raise RuntimeError("artifact verification requires Python without -O")
    files = read_bundle(root)
    fixed = anchors()
    started = json.loads(files["STARTED.json"])
    assert {k: v for k, v in started.items() if k != "command"} == fixed["execution_provenance"]
    protocol = json.loads(files["protocol.json"])
    inputs = json.loads(files["inputs.json"])
    assert sha(files["protocol.json"]) == started["protocol_sha256"] == inputs["protocol_sha256"]
    assert sha(files["inputs.json"]) == started["inputs_sha256"]
    assert files["protocol.json"] == (
        ROOT / "protocols/m1_checkpoint_compatibility_v1.json").read_bytes()
    assert files["inputs.json"] == (
        ROOT / "protocols/m1_checkpoint_compatibility_inputs_v1.json").read_bytes()
    assert protocol["source_commit"] == inputs["runtime_baseline_commit"]
    assert len(protocol["cases"]) == 10 and protocol["budget"]["dynamics_transitions"] == 0
    assert len(json.loads(files["planned-matrix.json"])) == 10
    assert not any(name.endswith(("ERROR.json", "measurement-errors.json")) for name in files)
    base = subset(files, "base-fixture/")
    assert len(base) == 6 and digests(base) == inputs["retained_fixture"]["files"]
    assert json.loads(files["input-provenance.json"]) == inputs["retained_fixture"]
    nondefault = subset(files, "setup/nondefault/")
    setup = json.loads(files["setup/result.json"])
    assert setup["status"] == "completed" and setup["dynamics_transitions"] == 0
    assert len(nondefault) == 6 and digests(nondefault) == setup["fixture"]
    assert setup["config"] == inputs["nondefault_public_configs"]
    assert json.loads(nondefault["world-state.json"])["index"] == 0
    assert json.loads(nondefault["pilot-state.json"])["sequence"] == 0
    assert json.loads(nondefault["scope/sb002-state.json"])["payload"]["sequence"] == 0
    assert json.loads(nondefault["predictive/pilot-state.json"])["revision_step"] == 0
    summary = json.loads(files["summary.json"])
    assert summary["status"] == "complete" and summary["controller_failure"] is None
    assert summary["setup_complete"] is True and summary["counts_are_lower_bounds"] is False
    assert summary["output_threshold_exceeded"] is False and summary["deadline_exceeded"] is False
    assert summary["elapsed_seconds"] < protocol["budget"]["max_total_seconds"]
    assert sum(map(len, files.values())) < protocol["budget"]["max_retained_bytes"]
    assert summary["retained_fixture_unchanged"] is True
    assert summary["source_transport_unchanged"] is True
    assert summary["scientific_credit"] == 0 and summary["dynamics_transitions"] == 0
    setup_events = journal(files, "setup/")
    assert all(e["phase"] == "setup" for e in setup_events)
    direct = completed(setup_events, "direct_reconstruct")
    assert len(direct) == 1 and direct[0]["event"] == "return"
    primary_count, accepted, rejected = 0, [], []
    worker_ids = set()
    workers = {row["name"]: row for row in summary["workers"]}
    assert set(workers) == {"setup"} | {c["case_id"] for c in protocol["cases"]}
    for name, worker in workers.items():
        assert worker == json.loads(files[f"worker-status/{name}.json"])
        assert worker["returncode"] == 0 and worker["status"] == "returned"
        assert worker["stdout_stderr_may_be_truncated"] is False
        assert worker["elapsed_seconds"] < protocol["budget"]["max_worker_seconds"]
        prefix = "setup/" if name == "setup" else f"cases/{name}/"
        meta = json.loads(files[prefix + "STARTED.json"])
        expected = {"source_commit": started["source_commit"],
                    "protocol_sha256": started["protocol_sha256"],
                    "runner_sha256": started["runner_sha256"], "python": started["python"],
                    "mode": "setup" if name == "setup" else "case",
                    "case_id": None if name == "setup" else name,
                    "pid": meta["pid"], "limits_active_before_runtime_import": True}
        assert meta == expected and type(meta["pid"]) is int and meta["pid"] > 0
        worker_ids.add(meta["pid"])
        command = worker["command"]
        assert command[0] == started["executable"]
        assert command[command.index("--source-commit") + 1] == started["source_commit"]
        assert command[command.index("--mode") + 1] == expected["mode"]
    assert len(worker_ids) == 11
    assert [row["case_id"] for row in summary["cases"]] == [c["case_id"] for c in protocol["cases"]]
    for case, aggregate in zip(protocol["cases"], summary["cases"], strict=True):
        cid = case["case_id"]
        prefix = f"cases/{cid}/"
        original = nondefault if cid == "C02" else base
        current = subset(files, f"case-inputs/{cid}/")
        assert current == expected_mutant(original, case)
        mutation = json.loads(files[f"mutations/{cid}.json"])
        assert mutation["before"] == digests(original) and mutation["after"] == digests(current)
        result = json.loads(files[prefix + "result.json"])
        primary = json.loads(files[prefix + "primary-result.json"])
        assert result["status"] == aggregate["status"] == "completed"
        assert result["case_id"] == cid and result["dynamics_transitions"] == 0
        assert all(result[k] == digests(current) for k in (
            "input_before", "input_after_load", "input_after_saveback"))
        assert result["input_unchanged"] is True and aggregate["input_unchanged"] is True
        assert primary == {k: result["primary_load"][k] for k in primary}
        assert aggregate["primary_load"] == {k: v for k, v in result["primary_load"].items()
                                             if k != "inspect"}
        events = journal(files, prefix)
        calls = completed(events, "integrated_load", "primary-load")
        assert len(calls) == result["primary_integrated_loads"] == 1
        assert aggregate["primary_calls_completed_observed"] == 1
        assert aggregate["observations_may_be_incomplete"] is False
        primary_count += len(calls)
        check_stages(events, cid)
        direct += completed(events, "direct_reconstruct")
        if cid in EXPECTED_ERRORS:
            rejected.append(cid)
            assert primary == {"returned": False, "error_type": "ValueError",
                               "error": EXPECTED_ERRORS[cid]}
            assert calls[0]["event"] == "error" and calls[0]["error"] == EXPECTED_ERRORS[cid]
            assert result["save_back"] == {"status": "not_applicable"}
            assert not subset(files, prefix + "saveback/")
            assert not any(e["phase"] == "save-back" for e in events)
        else:
            accepted.append(cid)
            assert primary == {"returned": True} and calls[0]["event"] == "return"
            saved = subset(files, prefix + "saveback/")
            assert len(saved) == 6 and digests(saved) == result["save_back"]["files"]
            config = {"predictive": json.loads(current["predictive/pilot-state.json"])["config"],
                      "scope": json.loads(current["scope/sb002-state.json"])["payload"]["config"]}
            assert config == result["primary_load"]["config"]
            assert result["primary_load"]["saved_config_preserved"] is True
            if cid == "C04":
                before = json.loads(current["manifest.json"])
                after = json.loads(saved["manifest.json"])
                assert before["schema_version"] is True
                assert type(after["schema_version"]) is int and after["schema_version"] == 1
                assert {**before, "schema_version": 1} == after
                assert saved == base
                assert result["save_back"]["changed_files"] == ["manifest.json"]
                assert result["save_back"]["equal"] is False
            else:
                assert saved == current and result["save_back"]["equal"] is True
            if cid == "C02":
                assert config == inputs["nondefault_public_configs"]
                assert result["primary_load"]["nondefault_config_matches_plan"] is True
    assert primary_count == summary["primary_integrated_loads_completed_observed"] == 10
    assert len(direct) == summary["direct_reconstructions_completed_observed"] == 13
    assert sum(row["event"] == "error" for row in direct) == 1
    assert accepted == ["C01", "C02", "C04"] and len(rejected) == 7
    return {"status": "verified_without_runtime_execution", "case_count": 10,
            "primary_load_calls": primary_count, "direct_validation_calls": len(direct),
            "direct_validation_returns": 12, "direct_validation_rejections": 1,
            "exact_valid_controls": 2, "expected_semantic_rejections": len(rejected),
            "outer_boolean_schema_accepted": True,
            "alias_saveback_changed_files": ["manifest.json"],
            "all_retained_inputs_match_before_after": True, "dynamics_transitions": 0,
            "archive_sha256": fixed["archive_sha256"], "scientific_credit": 0}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path, default=DEFAULT)
    args = parser.parse_args()
    print(json.dumps(verify(args.artifacts), sort_keys=True))
