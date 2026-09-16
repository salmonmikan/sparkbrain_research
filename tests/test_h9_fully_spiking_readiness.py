from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINESS = (
    ROOT / "artifacts" / "spiking" / "h9_fully_spiking_readiness" / "readiness.json"
)


def test_h9_fully_spiking_readiness_is_fail_closed_and_source_only() -> None:
    value = json.loads(READINESS.read_text(encoding="utf-8"))
    assert value["status"] == "PRE_START_UNDERSPECIFIED"
    assert value["execution_allowed"] is False
    assert value["hypothesis"]["fresh_successor_identity"] is None
    assert value["completion"]["scientific_execution_performed"] is False
    assert value["completion"]["identity_consumed"] is False
    assert value["independence"]["independent_of_main_critical_path"] is True
    assert value["independence"]["main_dependencies"] == []
    assert value["existing_boundary_inventory"]["fully_spiking_backend_present"] is False
    assert len(value["missing_scientific_choices"]) == 8


def test_h9_fully_spiking_readiness_verifier_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/verify_h9_fully_spiking_readiness.py"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PRE_START_UNDERSPECIFIED" in result.stdout
