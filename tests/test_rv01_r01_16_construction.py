from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from sparkbrain.research.rv01_r01_16_construction import run_construction

SOURCE_SHA = "a" * 40
DIGEST = "b" * 64


def _connection(
    source_id: int,
    target_id: int,
    *,
    weight: float,
    delay_ms: float,
) -> dict[str, object]:
    return {
        "source_id": source_id,
        "target_id": target_id,
        "weight": weight,
        "delay_ms": delay_ms,
        "plastic": True,
    }


def _payload(*, changed: bool = True) -> dict[str, object]:
    pre = [
        _connection(1, 2, weight=0.25, delay_ms=2.0),
        _connection(2, 3, weight=0.50, delay_ms=3.0),
    ]
    post = [
        _connection(1, 2, weight=0.75 if changed else 0.25, delay_ms=2.0),
        _connection(2, 3, weight=0.50, delay_ms=4.0 if changed else 3.0),
    ]
    return {
        "source_git_sha": SOURCE_SHA,
        "source_manifest_sha256": DIGEST,
        "collision_registry_sha256": "c" * 64,
        "package_plan_sha256": "d" * 64,
        "pre_training": pre,
        "post_training": post,
        "queued_propagation": [],
    }


def _write_input(path: Path, *, changed: bool = True) -> None:
    path.write_text(
        json.dumps(_payload(changed=changed), sort_keys=True),
        encoding="utf-8",
    )


def test_r01_16_construction_writes_fresh_auditable_artifacts(tmp_path: Path) -> None:
    input_path = tmp_path / "input.json"
    output_dir = tmp_path / "output"
    _write_input(input_path)

    result = run_construction(input_path=input_path, output_dir=output_dir)

    assert result == output_dir
    assert (output_dir / "construction_input.json").read_bytes() == input_path.read_bytes()
    complete = json.loads((output_dir / "COMPLETE.json").read_text(encoding="utf-8"))
    assert complete["status"] == "CONSTRUCTION_COMPLETE_CAPABILITY_UNOPENED"
    assert complete["capability_output_opened"] is False
    assert complete["learner_or_probe_executed"] is False
    assert complete["formal_execution_allowed"] is False
    assert not (output_dir / "FAILED.json").exists()

    runtime = json.loads((output_dir / "runtime.json").read_text(encoding="utf-8"))
    assert runtime["python_executable"] == sys.executable
    assert runtime["runner_module"] == "sparkbrain.research.rv01_r01_16_construction"

    for arm in ("F0", "FW", "FD", "FWD"):
        assert (output_dir / "arms" / f"{arm}.json").is_file()


def test_r01_16_construction_never_clobbers_an_existing_output(tmp_path: Path) -> None:
    input_path = tmp_path / "input.json"
    output_dir = tmp_path / "output"
    _write_input(input_path)
    run_construction(input_path=input_path, output_dir=output_dir)
    complete_before = (output_dir / "COMPLETE.json").read_bytes()

    with pytest.raises(FileExistsError):
        run_construction(input_path=input_path, output_dir=output_dir)

    assert (output_dir / "COMPLETE.json").read_bytes() == complete_before


def test_r01_16_zero_contrast_is_retained_as_terminal_construction_failure(
    tmp_path: Path,
) -> None:
    input_path = tmp_path / "input.json"
    output_dir = tmp_path / "output"
    _write_input(input_path, changed=False)

    with pytest.raises(RuntimeError, match="no learned weight or delay contrast"):
        run_construction(input_path=input_path, output_dir=output_dir)

    failed = json.loads((output_dir / "FAILED.json").read_text(encoding="utf-8"))
    assert failed["status"] == "CONSTRUCTION_FAILED_TERMINAL_FOR_THIS_OUTPUT_IDENTITY"
    assert failed["retry_same_output_identity_allowed"] is False
    assert not (output_dir / "COMPLETE.json").exists()


def test_r01_16_construction_rejects_unbound_extra_input_fields(tmp_path: Path) -> None:
    input_path = tmp_path / "input.json"
    output_dir = tmp_path / "output"
    payload = _payload()
    payload["capability_allowed"] = True
    input_path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="keys must exactly match"):
        run_construction(input_path=input_path, output_dir=output_dir)

    assert (output_dir / "FAILED.json").is_file()
    assert not (output_dir / "COMPLETE.json").exists()
