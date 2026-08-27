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


def test_disabled_and_tampered_source_fail_closed(tmp_path: Path) -> None:
    protocol = {
        "execution_base_commit": "4447c27eb7ac5f9a54f16a1e29552d3ae8c300d2",
        "protocol_id": "c18-trace-checkpoint-brain-lab-v6",
        "runner_execution_allowed": True,
        "source_commit": None,
        "source_control": {"expected_runtime_runner_and_test_paths": []},
    }
    protocol["runner_execution_allowed"] = False
    path = tmp_path / "disabled.json"
    path.write_text(json.dumps(protocol), encoding="utf-8")
    with pytest.raises(RuntimeError):
        runner.load_protocol(path, require_enabled=True)
    protocol["source_commit"] = "0" * 40
    with pytest.raises(RuntimeError):
        runner.preflight(protocol)


def test_v6_runner_defaults_to_the_preregistered_official_seed() -> None:
    parser = runner.argparse.ArgumentParser()
    parser.add_argument("--seed", default=1802, type=int)
    assert parser.parse_args([]).seed == 1802
    assert runner.PROTOCOL_RELATIVE.endswith("c18_brain_lab_v6/preregistration.json")


def test_write_artifacts_rejects_non_clean_room_before_protocol_read(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="clean room"):
        runner.write_artifacts(tmp_path / "official", seed=1802)


def test_integration_requires_both_preregistration_blobs(monkeypatch: pytest.MonkeyPatch) -> None:
    responses = iter(("protocol", "protocol", "sidecar", "sidecar"))
    monkeypatch.setattr(runner, "_git", lambda *_args: next(responses))
    runner._require_integration_preregistration_blobs()
    responses = iter(("protocol", "protocol", "sidecar", "wrong"))
    monkeypatch.setattr(runner, "_git", lambda *_args: next(responses))
    with pytest.raises(RuntimeError, match="preregistration blobs"):
        runner._require_integration_preregistration_blobs()
