from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import pytest

from sparkbrain import equiv_audit_architecture as audit


def _available() -> bool:
    return (
        sys.platform.startswith("linux")
        and bool(audit.shutil.which("unshare"))
        and Path("/usr/bin/time").exists()
    )


@pytest.mark.skipif(not _available(), reason="Linux unshare/GNU time architecture probe unavailable")
def test_clean_pair_recomputes_raw_match(tmp_path: Path) -> None:
    root = tmp_path / "clean"
    args = argparse.Namespace(
        run_root=str(root),
        run_id="test-clean",
        ref_id="fixture-v1",
        right_variant="match",
    )
    assert audit.run_controller(args) == 0
    ledger = json.loads((root / "launch_ledger.json").read_text())
    assert ledger["producer_exit_complete_before_verifier"] is True
    assert all(item["counter_capture_agreement"] for item in ledger["producers"])


@pytest.mark.skipif(not _available(), reason="Linux unshare/GNU time architecture probe unavailable")
def test_mismatch_pair_is_system_mismatch_not_semantic_claim(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = tmp_path / "mismatch"
    args = argparse.Namespace(
        run_root=str(root),
        run_id="test-mismatch",
        ref_id="fixture-v1",
        right_variant="mismatch",
    )
    assert audit.run_controller(args) == 0
    payload = json.loads(capsys.readouterr().out.splitlines()[-1])
    assert payload["verdict"] == "AUDITABLE_RAW_MISMATCH"
    assert payload["reason"] == "VERIFIER_RECOMPUTED_RAW_BYTES"


def _seed_pair(tmp_path: Path) -> tuple[dict, dict]:
    lock = audit._runtime_lock()
    audit._write_json(tmp_path / "runtime_lock.json", lock)
    entries = []
    for idx, producer_id in enumerate(("producer-A", "producer-B")):
        raw_dir = tmp_path / "raw" / producer_id
        raw_dir.mkdir(parents=True)
        audit._write_ndjson(raw_dir / "trajectory.ndjson", audit._TRAJECTORY)
        audit._write_ndjson(raw_dir / "checkpoints.ndjson", audit._CHECKPOINTS)
        manifest = {
            "schema_version": 1,
            "raw_schema": audit.RAW_SCHEMA,
            "contract_id": audit.CONTRACT_ID,
            "fixture_id": audit.FIXTURE_ID,
            "run_id": "run",
            "ref_id": "ref",
            "producer_id": producer_id,
            "challenge_nonce": str(idx + 1) * 32,
            "variant": "match",
            "namespace": {
                "inside_pid": 1,
                "pid_ns": f"pid:{idx}",
                "mnt_ns": f"mnt:{idx}",
                "net_ns": f"net:{idx}",
                "user_ns": f"user:{idx}",
            },
            "runtime_lock_sha256": audit._sha256_file(tmp_path / "runtime_lock.json"),
            "runtime_dependency_lock_status": "PASS",
        }
        audit._write_json(raw_dir / "producer_manifest.json", manifest)
        audit._write_json(
            raw_dir / "resources.json",
            {
                "schema_version": 1,
                "wall_ms": 1.0,
                "ru_maxrss_kib": 1,
                "rss_source": "resource.getrusage(RUSAGE_SELF).ru_maxrss",
                "cpu_count_observed": os.cpu_count(),
                "caps": audit.RESOURCE_CAPS,
                "within_caps": True,
            },
        )
        audit._write_json(
            raw_dir / "declared_digests.json",
            {
                "trajectory.ndjson": audit._sha256_file(raw_dir / "trajectory.ndjson"),
                "checkpoints.ndjson": audit._sha256_file(raw_dir / "checkpoints.ndjson"),
            },
        )
        entries.append(
            {
                "launch_id": f"run:{producer_id}",
                "run_id": "run",
                "ref_id": "ref",
                "producer_id": producer_id,
                "challenge_nonce": manifest["challenge_nonce"],
                "host_pid": 200 + idx,
                "raw_relpath": f"raw/{producer_id}",
                "controller_wrapper_max_rss_kib": 1,
            }
        )
    ledger = {
        "schema_version": 1,
        "contract_id": audit.CONTRACT_ID,
        "run_id": "run",
        "ref_id": "ref",
        "runtime_lock_sha256": audit._sha256_file(tmp_path / "runtime_lock.json"),
        "controller_runtime": audit._runtime_fingerprint(),
        "controller_recipe_sha256": audit._recipe_sha256("controller"),
        "producers": entries,
        "producer_exit_complete_before_verifier": True,
    }
    return lock, ledger


def test_verifier_uses_raw_bytes_not_stale_declared_digest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    lock, ledger = _seed_pair(tmp_path)
    with (tmp_path / "raw" / "producer-B" / "trajectory.ndjson").open("ab") as handle:
        handle.write(b'{"mutation":true}\n')
    monkeypatch.setattr(audit.os, "getpid", lambda: 1)
    result = audit.verify_raw_pair(tmp_path, ledger, lock)
    assert result.verdict == "AUDITABLE_RAW_MISMATCH"
    assert result.reason == "VERIFIER_RECOMPUTED_RAW_BYTES"


def test_verifier_fail_closes_binding_swap(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    lock, ledger = _seed_pair(tmp_path)
    ledger["producers"][1]["ref_id"] = "swapped-ref"
    monkeypatch.setattr(audit.os, "getpid", lambda: 1)
    result = audit.verify_raw_pair(tmp_path, ledger, lock)
    assert result.verdict == "INVALID_PROVENANCE_CHAIN"
    assert result.reason == "LEDGER_BINDING_MISMATCH:producer-B:ref_id"
