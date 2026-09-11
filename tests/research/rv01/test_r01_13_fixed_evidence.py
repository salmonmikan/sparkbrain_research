from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "artifacts/research/rv01/r01_13/development_result.json"
MANIFEST = ROOT / "artifacts/research/rv01/r01_13/development_result_manifest.json"


def test_r01_13_fixed_development_raw_is_retained_and_hash_bound() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    raw = RAW.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == manifest["development_result_json_sha256"]
    assert manifest["development_result_json_sha256"] == (
        "1ab43a8950be572b163e7bba4950b23d5258933e5463dc3d944f41eaea2adf60"
    )
    assert manifest["execution_source_git_sha"] == (
        "241669c92a0fd93b1f98ffe5e5dcaf8fd97c4de2"
    )
    assert manifest["execution_python_implementation"] == "CPython"
    assert manifest["execution_python_version"] == "3.11.15"
    assert manifest["portable_reexecution_claim"] is False
    assert manifest["held_out_capability_executed"] is False
    assert manifest["retained_raw_result_path"] == (
        "artifacts/research/rv01/r01_13/development_result.json"
    )
