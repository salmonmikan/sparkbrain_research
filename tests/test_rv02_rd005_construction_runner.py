from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

import sparkbrain.research.rv02_rd005_construction_runner as runner
from sparkbrain.research.rv02_rd005_development_package import RD005CollisionRegistry

SOURCE_SHA = "a" * 40
DIGEST = "b" * 64


class _FakeArtifact:
    def __init__(self, *, matrix_status: str = "D1_CONSTRUCTION_READY") -> None:
        self.matrix_status = matrix_status
        self.artifact_sha256 = "e" * 64

    def state_dict(self) -> dict[str, object]:
        return {
            "matrix_status": self.matrix_status,
            "formal_execution_allowed": False,
            "held_out_capability_allowed": False,
        }


def _registry() -> RD005CollisionRegistry:
    return RD005CollisionRegistry(
        registry_id="rv02-retained-identities-v1",
        source_paths=("docs/research/RV02_RETAINED_IDENTITY_REGISTRY.json",),
        consumed_or_reserved_seed_ids=(92503, 92504),
        consumed_or_reserved_world_ids=(
            "rv02:rd003:92503:family-a",
            "rv02:rd004:92504:family-b",
        ),
        authoritative_complete=True,
    )


def _payload() -> dict[str, object]:
    registry = _registry()
    return {
        "source_git_sha": SOURCE_SHA,
        "source_manifest_sha256": DIGEST,
        "collision_registry_sha256": registry.registry_sha256,
        "package_plan_sha256": "d" * 64,
        "collision_registry": registry.state_dict(),
    }


def _write_input(path: Path, payload: dict[str, object] | None = None) -> None:
    path.write_text(json.dumps(payload or _payload(), sort_keys=True), encoding="utf-8")


def test_rd005_runner_writes_verified_fresh_construction_only_artifacts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    input_path = tmp_path / "input.json"
    output_dir = tmp_path / "output"
    _write_input(input_path)
    fake = _FakeArtifact()
    monkeypatch.setattr(runner, "build_rd005_construction_artifact", lambda **_: fake)
    monkeypatch.setattr(
        runner,
        "verify_rd005_artifact_for_future_capability",
        lambda artifact: ("cell-a", "cell-b") if artifact is fake else (),
    )

    result = runner.run_construction(input_path=input_path, output_dir=output_dir)

    assert result == output_dir
    assert (output_dir / "construction_input.json").read_bytes() == input_path.read_bytes()
    complete = json.loads((output_dir / "COMPLETE.json").read_text(encoding="utf-8"))
    assert complete["status"] == "D1_CONSTRUCTION_COMPLETE_CAPABILITY_UNOPENED"
    assert complete["capability_output_opened"] is False
    assert complete["learner_or_probe_executed"] is False
    assert complete["formal_execution_allowed"] is False
    verification = json.loads(
        (output_dir / "verification.json").read_text(encoding="utf-8")
    )
    assert verification["verified_ready_cell_ids"] == ["cell-a", "cell-b"]
    assert not (output_dir / "FAILED.json").exists()


def test_rd005_runner_never_clobbers_existing_output(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    input_path = tmp_path / "input.json"
    output_dir = tmp_path / "output"
    _write_input(input_path)
    fake = _FakeArtifact()
    monkeypatch.setattr(runner, "build_rd005_construction_artifact", lambda **_: fake)
    monkeypatch.setattr(
        runner,
        "verify_rd005_artifact_for_future_capability",
        lambda _: ("cell-a",),
    )
    runner.run_construction(input_path=input_path, output_dir=output_dir)
    complete_before = (output_dir / "COMPLETE.json").read_bytes()

    with pytest.raises(FileExistsError):
        runner.run_construction(input_path=input_path, output_dir=output_dir)

    assert (output_dir / "COMPLETE.json").read_bytes() == complete_before


def test_rd005_runner_retains_terminal_stop_when_verified_matrix_is_not_ready(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    input_path = tmp_path / "input.json"
    output_dir = tmp_path / "output"
    _write_input(input_path)
    fake = _FakeArtifact(matrix_status="D1_ZERO_READY_STOP")
    monkeypatch.setattr(runner, "build_rd005_construction_artifact", lambda **_: fake)
    monkeypatch.setattr(
        runner,
        "verify_rd005_artifact_for_future_capability",
        lambda _: (),
    )

    with pytest.raises(RuntimeError, match="verified D1 matrix is not ready"):
        runner.run_construction(input_path=input_path, output_dir=output_dir)

    assert (output_dir / "rd005_construction_artifact.json").is_file()
    assert (output_dir / "FAILED.json").is_file()
    assert not (output_dir / "COMPLETE.json").exists()


def test_rd005_runner_rejects_registry_digest_mismatch(tmp_path: Path) -> None:
    input_path = tmp_path / "input.json"
    output_dir = tmp_path / "output"
    payload = _payload()
    payload["collision_registry_sha256"] = hashlib.sha256(b"other").hexdigest()
    _write_input(input_path, payload)

    with pytest.raises(ValueError, match="digest does not match"):
        runner.run_construction(input_path=input_path, output_dir=output_dir)

    assert (output_dir / "FAILED.json").is_file()
    assert not (output_dir / "COMPLETE.json").exists()
