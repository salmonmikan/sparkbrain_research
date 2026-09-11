from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "artifacts/research/rv01/r01_14/development_result.json"
MANIFEST = ROOT / "artifacts/research/rv01/r01_14/development_result_manifest.json"


def test_r01_14_fixed_development_raw_is_retained_and_hash_bound() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    raw = RAW.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == manifest["development_result_json_sha256"]
    assert manifest["development_result_json_sha256"] == (
        "4a214059cacc66d473776de7b46455c959ce0ac5c7089c6acfafbc9e0ef91e25"
    )
    assert manifest["execution_source_git_sha"] == (
        "d0c828dda9faf1ff0d455adf02be4e9ef65030fb"
    )
    assert manifest["execution_python_implementation"] == "CPython"
    assert manifest["execution_python_version"] == "3.11.15"
    assert manifest["portable_reexecution_claim"] is False
    assert manifest["held_out_capability_executed"] is False
    assert manifest["normalized_discovery_auc_status"] == (
        "historical-v1-invalid-unregistered-denominator"
    )
    assert manifest["retained_raw_result_path"] == (
        "artifacts/research/rv01/r01_14/development_result.json"
    )
