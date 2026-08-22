from __future__ import annotations

import json
from pathlib import Path

import pytest

from sparkbrain.release import (
    REQUIRED_PREPARATION_FILES,
    build_release_archive,
    build_release_manifest,
    preparation_problems,
    project_license_selected,
    validate_evidence_map,
    validate_generated_release_evidence,
    validate_release_tree,
    verify_release_manifest,
)


def test_release_manifest_is_stable_and_detects_tampering(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "result.md").write_text("evidence\n", encoding="utf-8")
    manifest = build_release_manifest(
        tmp_path,
        generated_at="2026-08-23T00:00:00+00:00",
        source_revision="a" * 40,
        paths=["docs/result.md", "PACKAGE_MANIFEST.json"],
    )

    assert manifest["file_count"] == 1
    assert manifest["files"][0]["path"] == "docs/result.md"
    assert manifest["files"][0]["artifact_class"] == "documentation"
    assert manifest["platform"]
    assert verify_release_manifest(tmp_path, manifest) == []

    (tmp_path / "docs" / "result.md").write_text("changed\n", encoding="utf-8")
    problems = verify_release_manifest(tmp_path, manifest)
    assert "size mismatch: docs/result.md" in problems
    assert "sha256 mismatch: docs/result.md" in problems


def test_release_manifest_rejects_parent_traversal(tmp_path: Path) -> None:
    outside = tmp_path.parent / "outside.txt"
    outside.write_text("not in release", encoding="utf-8")
    try:
        build_release_manifest(
            tmp_path,
            generated_at="fixed",
            source_revision="fixed",
            paths=["../outside.txt"],
        )
    except ValueError as exc:
        assert "unsafe release path" in str(exc)
    else:
        raise AssertionError("parent traversal was accepted")


def test_unselected_project_license_blocks_release(tmp_path: Path) -> None:
    (tmp_path / "LICENSE_NOT_SELECTED.md").write_text("pending", encoding="utf-8")
    assert not project_license_selected(tmp_path)
    (tmp_path / "LICENSE_NOT_SELECTED.md").unlink()
    (tmp_path / "LICENSE").write_text("selected by owner", encoding="utf-8")
    assert project_license_selected(tmp_path)


def test_release_validator_reports_missing_artifacts_and_unselected_license(
    tmp_path: Path,
) -> None:
    (tmp_path / "LICENSE_NOT_SELECTED.md").write_text("pending", encoding="utf-8")
    problems = validate_release_tree(tmp_path)
    assert f"missing required release artifact: {REQUIRED_PREPARATION_FILES[0]}" in problems
    assert "project license has not been selected by the repository owner" in problems


def test_integrated_release_preparation_passes_but_public_release_is_blocked() -> None:
    root = Path(__file__).resolve().parents[1]
    assert preparation_problems(root) == []
    assert not project_license_selected(root)
    assert validate_release_tree(root) == [
        "pending release evidence gate: EV-C05-CHECKPOINT",
        "pending release evidence gate: EV-C06-FOUNDATION",
        "pending release evidence gate: EV-C08-PLASTICITY",
        "project license has not been selected by the repository owner",
    ]


def test_evidence_map_has_existing_artifacts_and_pending_gates() -> None:
    root = Path(__file__).resolve().parents[1]
    evidence = json.loads(
        (root / "artifacts/release/evidence_map.json").read_text(encoding="utf-8")
    )
    assert validate_evidence_map(root, evidence) == []
    pending = {entry["id"] for entry in evidence["entries"] if entry["status"] == "pending"}
    assert pending == {"EV-C05-CHECKPOINT", "EV-C06-FOUNDATION", "EV-C08-PLASTICITY"}


def test_archive_refuses_unlicensed_repository(tmp_path: Path) -> None:
    (tmp_path / "LICENSE_NOT_SELECTED.md").write_text("owner decision pending", encoding="utf-8")
    with pytest.raises(PermissionError, match="project license is not selected"):
        build_release_archive(tmp_path, tmp_path / "release.zip", source_date_epoch=1_700_000_000)


def test_generated_release_evidence_contract_passes() -> None:
    root = Path(__file__).resolve().parents[1]
    assert validate_generated_release_evidence(root) == []


def test_generated_release_evidence_detects_primary_output_tampering(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    (tmp_path / "artifacts/release").mkdir(parents=True)
    for name in ("primary_subset.json", "provenance.json", "claim_audit.json", "sbom.spdx.json"):
        (tmp_path / "artifacts/release" / name).write_bytes(
            (root / "artifacts/release" / name).read_bytes()
        )
    subset = json.loads(
        (tmp_path / "artifacts/release/primary_subset.json").read_text(encoding="utf-8")
    )
    subset["inputs"] = {"artifacts/release/tampered.txt": "0" * 64}
    subset["outputs"] = {"artifacts/release/tampered.txt": "0" * 64}
    (tmp_path / "artifacts/release/primary_subset.json").write_text(
        json.dumps(subset), encoding="utf-8"
    )
    (tmp_path / "artifacts/release/tampered.txt").write_text("changed", encoding="utf-8")
    problems = validate_generated_release_evidence(tmp_path)
    assert "primary subset input hash mismatch: artifacts/release/tampered.txt" in problems
    assert "primary subset output hash mismatch: artifacts/release/tampered.txt" in problems
