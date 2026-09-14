from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

import sparkbrain.research.rv02_rd005_construction_input as construction_input
from sparkbrain.research.rv02_rd005_development_package import (
    RD005_REQUIRED_SOURCE_PATHS,
    RD005CollisionRegistry,
    RD005SourceManifest,
    RD005SourceManifestEntry,
)


def _manifest() -> RD005SourceManifest:
    return RD005SourceManifest(
        source_git_sha="1" * 40,
        entries=tuple(
            RD005SourceManifestEntry(path=path, sha256="2" * 64)
            for path in sorted(RD005_REQUIRED_SOURCE_PATHS)
        ),
    )


def _registry() -> RD005CollisionRegistry:
    return RD005CollisionRegistry(
        registry_id="rv02-rd005-retained-identities-v1",
        source_paths=("docs/research/RV02_RD005_RETAINED_IDENTITY_REGISTRY.json",),
        consumed_or_reserved_seed_ids=(92001,),
        consumed_or_reserved_world_ids=(
            "rv02-development:92001:disjoint-routes",
        ),
        authoritative_complete=True,
    )


def _write_manifest(path: Path, manifest: RD005SourceManifest) -> None:
    path.write_text(
        json.dumps(manifest.state_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def test_prepare_construction_input_is_deterministic_and_execution_disabled(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manifest = _manifest()
    registry = _registry()
    source_manifest_path = tmp_path / "source-manifest.json"
    _write_manifest(source_manifest_path, manifest)
    events: list[str] = []

    def verify_source(repo_root: Path, loaded: RD005SourceManifest) -> object:
        assert repo_root == tmp_path
        assert loaded.state_dict() == manifest.state_dict()
        events.append("source")
        return object()

    def build_registry(repo_root: Path) -> RD005CollisionRegistry:
        assert repo_root == tmp_path
        events.append("registry")
        return registry

    monkeypatch.setattr(construction_input, "verify_rd005_source_checkout", verify_source)
    monkeypatch.setattr(
        construction_input,
        "build_authoritative_rd005_collision_registry",
        build_registry,
    )

    raw_a, digest_a = construction_input.prepare_construction_input_bytes(
        repo_root=tmp_path,
        source_manifest_path=source_manifest_path,
    )
    raw_b, digest_b = construction_input.prepare_construction_input_bytes(
        repo_root=tmp_path,
        source_manifest_path=source_manifest_path,
    )

    assert raw_a == raw_b
    assert digest_a == digest_b == hashlib.sha256(raw_a).hexdigest()
    assert events == ["source", "registry", "source", "registry"]
    payload = json.loads(raw_a)
    assert payload["source_git_sha"] == manifest.source_git_sha
    assert payload["source_manifest_sha256"] == manifest.manifest_sha256
    assert payload["collision_registry_sha256"] == registry.registry_sha256
    assert payload["collision_registry"] == registry.state_dict()
    assert isinstance(payload["package_plan_sha256"], str)
    assert len(payload["package_plan_sha256"]) == 64
    assert not (tmp_path / "artifacts" / "rv02" / "rd005" / "development").exists()


def test_write_construction_input_is_fresh_and_no_clobber(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manifest = _manifest()
    registry = _registry()
    source_manifest_path = tmp_path / "source-manifest.json"
    _write_manifest(source_manifest_path, manifest)
    monkeypatch.setattr(
        construction_input,
        "verify_rd005_source_checkout",
        lambda _root, _manifest: object(),
    )
    monkeypatch.setattr(
        construction_input,
        "build_authoritative_rd005_collision_registry",
        lambda _root: registry,
    )

    output = tmp_path / "control" / "construction-input.json"
    digest = construction_input.write_construction_input(
        repo_root=tmp_path,
        source_manifest_path=source_manifest_path,
        output_path=output,
    )

    assert hashlib.sha256(output.read_bytes()).hexdigest() == digest
    with pytest.raises(FileExistsError, match="construction input already exists"):
        construction_input.write_construction_input(
            repo_root=tmp_path,
            source_manifest_path=source_manifest_path,
            output_path=output,
        )
    assert not (tmp_path / "artifacts" / "rv02" / "rd005" / "development").exists()


def test_source_failure_writes_no_construction_input_or_d1_artifact(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manifest = _manifest()
    source_manifest_path = tmp_path / "source-manifest.json"
    _write_manifest(source_manifest_path, manifest)

    def reject_source(_repo_root: Path, _manifest: RD005SourceManifest) -> object:
        raise ValueError("source mismatch")

    monkeypatch.setattr(construction_input, "verify_rd005_source_checkout", reject_source)

    output = tmp_path / "control" / "construction-input.json"
    with pytest.raises(ValueError, match="source mismatch"):
        construction_input.write_construction_input(
            repo_root=tmp_path,
            source_manifest_path=source_manifest_path,
            output_path=output,
        )

    assert not output.exists()
    assert not output.parent.exists()
    assert not (tmp_path / "artifacts" / "rv02" / "rd005" / "development").exists()
