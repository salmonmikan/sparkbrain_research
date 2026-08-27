from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("c18_runner", ROOT / "scripts/run_c18_brain_lab.py")
runner = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = runner
SPEC.loader.exec_module(runner)


def test_disabled_preregistration_cannot_execute(tmp_path: Path) -> None:
    protocol = json.loads((ROOT / runner.PROTOCOL_RELATIVE).read_text(encoding="utf-8"))
    assert protocol["runner_execution_allowed"] is False
    with pytest.raises(RuntimeError, match="remains disabled"):
        runner.load_protocol(ROOT / runner.PROTOCOL_RELATIVE, require_enabled=True)
    assert not list(tmp_path.iterdir())
