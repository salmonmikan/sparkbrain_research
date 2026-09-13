from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

import sparkbrain.research.rv02_rd005_construction_runner as runner
from sparkbrain.research.rv02_rd005_development_package import (
    RD005_REQUIRED_SOURCE_PATHS,
    RD005CollisionRegistry,
    RD005SourceManifest,
    RD005SourceManifestEntry,
)

SOURCE_SHA = "a" * 40
FILE_SHA = "b" * 64


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


class _VerifiedSource:
    def __init__(self, manifest: RD005SourceManifest) -> None:
        self.manifest = manifest

    def state_dict(self) -> dict[str, object]:
        return {
            "source_git_sha": self.manifest.source_git_sha,
            "source_manifest_sha256": self.manifest.manifest_sha256,
            "verified_paths": sorted(row.path for row in self.manifest.entries),
            "tracked_checkout_clean": True,
            "source_bytes_verified": True,
            "execution_authority_granted": False,
        }


@pytest.fixture(autouse=True)
def _stub_exact_source_gate(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        runner,
        "verify_rd005_source_checkout",
        lambda repo_root, manifest: _VerifiedSource(manifest),
    )


def _manifest() -> RD005SourceManifest:
    return RD005SourceManifest(
        source_git_sha=SOURCE_SHA,
        entries=tuple(
            RD005SourceManifestEntry(path=path, sha256=FILE_SHA)
            for path in sorted(RD005_REQUIRED_SOURCE_PATHS)
        ),
    )


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
    manifest = _manifest()
    return {
        "source_git_sha": manifest.source_git_sha,
        "source_manifest_sha256": manifest.manifest_sha256,
        "source_manifest": manifest.state_dict(),
        "collision_registry_sha256": registry.registry_sha256,
        "package_plan_sha256": "d" * 64,
        "collision_registry": registry.state_dict(),
    }


def _write_input(path: Path, payload: dict[str, object] | None = None) -> None:
    path.write_text(json.dumps(payload or _payload(), sort_keys=True), encoding="utf-8")


def _expected_output(repo_root: Path, input_path: Path) -> Path:
    input_sha256 = hashlib.sha256(input_path.read_bytes()).hexdigest()
    return (
        repo_root
        / "artifacts"
        / "rv02"
        / "rd005"
        / "development"
        / f"construction-{input_sha256}"
    )


def test_rd005_runner_writes_verified_fresh_construction_only_artifacts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    input_path = tmp_path / "input.json"
    repo_root = tmp_path / "repo"
    _write_input(input_path)
    output_dir = _expected_output(repo_root, input_path)
    fake = _FakeArtifact()
    monkeypatch.setattr(runner, "build_rd005_construction_artifact", lambda **_: fake)
    monkeypatch.setattr(
        runner,
        "verify_rd005_artifact_for_future_capability",
        lambda artifact: ("cell-a", "cell-b") if artifact is fake else (),
    )

    result = runner.run_construction(input_path=input_path, repo_root=repo_root)

    assert result == output_dir
    assert (output_dir / "construction_input.json").read_bytes() == input_path.read_bytes()
    identity = json.loads((output_dir / "input_identity.json").read_text(encoding="utf-8"))
    assert identity["retry_same_input_identity_allowed"] is False
    assert identity["output_relpath"].startswith("artifacts/rv02/rd005/development/")
    source_binding = json.loads(
        (output_dir / "source_binding.json").read_text(encoding="utf-8")
    )
    assert source_binding["source_git_sha"] == SOURCE_SHA
    assert source_binding["source_manifest_sha256"] == _manifest().manifest_sha256
    assert source_binding["source_bytes_verified"] is True
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


def test_rd005_runner_never_retries_same_input_identity_under_another_output(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    input_path = tmp_path / "input.json"
    repo_root = tmp_path / "repo"
    _write_input(input_path)
    output_dir = _expected_output(repo_root, input_path)
    fake = _FakeArtifact()
    monkeypatch.setattr(runner, "build_rd005_construction_artifact", lambda **_: fake)
    monkeypatch.setattr(
        runner,
        "verify_rd005_artifact_for_future_capability",
        lambda _: ("cell-a",),
    )
    first = runner.run_construction(input_path=input_path, repo_root=repo_root)
    complete_before = (output_dir / "COMPLETE.json").read_bytes()

    with pytest.raises(FileExistsError):
        runner.run_construction(input_path=input_path, repo_root=repo_root)

    assert first == output_dir
    assert (output_dir / "COMPLETE.json").read_bytes() == complete_before
    assert len(list((repo_root / "artifacts/rv02/rd005/development").iterdir())) == 1


def test_rd005_runner_retains_terminal_stop_when_verified_matrix_is_not_ready(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    input_path = tmp_path / "input.json"
    repo_root = tmp_path / "repo"
    _write_input(input_path)
    output_dir = _expected_output(repo_root, input_path)
    fake = _FakeArtifact(matrix_status="D1_ZERO_READY_STOP")
    monkeypatch.setattr(runner, "build_rd005_construction_artifact", lambda **_: fake)
    monkeypatch.setattr(
        runner,
        "verify_rd005_artifact_for_future_capability",
        lambda _: (),
    )

    with pytest.raises(RuntimeError, match="verified D1 matrix is not ready"):
        runner.run_construction(input_path=input_path, repo_root=repo_root)

    assert (output_dir / "rd005_construction_artifact.json").is_file()
    assert (output_dir / "FAILED.json").is_file()
    assert not (output_dir / "COMPLETE.json").exists()


def test_rd005_runner_rejects_registry_digest_mismatch_before_output(tmp_path: Path) -> None:
    input_path = tmp_path / "input.json"
    repo_root = tmp_path / "repo"
    payload = _payload()
    payload["collision_registry_sha256"] = hashlib.sha256(b"other").hexdigest()
    _write_input(input_path, payload)

    with pytest.raises(ValueError, match="digest does not match"):
        runner.run_construction(input_path=input_path, repo_root=repo_root)

    assert not (repo_root / "artifacts").exists()


def test_rd005_runner_rejects_source_manifest_digest_mismatch_before_output(
    tmp_path: Path,
) -> None:
    input_path = tmp_path / "input.json"
    repo_root = tmp_path / "repo"
    payload = _payload()
    payload["source_manifest_sha256"] = hashlib.sha256(b"other manifest").hexdigest()
    _write_input(input_path, payload)

    with pytest.raises(ValueError, match="source manifest digest"):
        runner.run_construction(input_path=input_path, repo_root=repo_root)

    assert not (repo_root / "artifacts").exists()


def test_rd005_source_gate_failure_does_not_consume_output_identity(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    input_path = tmp_path / "input.json"
    repo_root = tmp_path / "repo"
    _write_input(input_path)

    def reject_source(repo_root: Path, manifest: RD005SourceManifest) -> None:
        raise ValueError("source checkout rejected before construction")

    monkeypatch.setattr(runner, "verify_rd005_source_checkout", reject_source)
    with pytest.raises(ValueError, match="source checkout rejected"):
        runner.run_construction(input_path=input_path, repo_root=repo_root)

    assert not (repo_root / "artifacts").exists()
