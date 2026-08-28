from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

import scripts.validate_release as validation_cli
from sparkbrain.release import (
    REQUIRED_PREPARATION_FILES,
    build_release_archive,
    build_release_manifest,
    declared_project_license,
    integrity_problems,
    owner_blockers,
    package_version,
    preparation_problems,
    project_license_selected,
    release_validation,
    sha256_file,
    validate_evidence_map,
    validate_generated_release_evidence,
    validate_project_license_metadata,
    validate_release_tree,
    verify_release_manifest,
)

ROOT = Path(__file__).resolve().parents[1]

SCIENTIFIC_HASHES = {
    "artifacts/external_validation/c06-final-official/belief_r_metrics.json": (
        "2bdd0d88a48c5ed7c02dd7e3f55ceb56520ba42c0731e9c23aa416b09d0c7f43"
    ),
    "artifacts/phase3/structural-plasticity-v1/main/acceptance-matrix.json": (
        "ad6cac143f6d95ce128e982a31542c833b6acfae3e516d4987ba384271e10da6"
    ),
    "artifacts/phase3/structural-plasticity-v1/main/summary.json": (
        "8e4e689be66be55b2bdc7418e55c57120b1692cfd0f15e726fe51eeef0b84ae6"
    ),
    "artifacts/release/primary_subset.json": (
        "8c069b8d679575dc3856ee3267d356395f6be7c2da72838d2eec3af65969c391"
    ),
    "docs/CLAIMS_REGISTER.md": (
        "5562a4e04ec99ede1f4c8ea15cf1d5e4db306c6b7e71a838eaf90c14f188cc62"
    ),
}


def _validation_categories(*, integrity: list[str] | None = None) -> dict[str, list[str]]:
    return {
        "integrity_problems": integrity or [],
        "preparation_problems": [],
        "owner_blockers": [
            "project license has not been selected by the repository owner"
        ],
        "evidence_blockers": [],
    }


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


def test_release_validation_classifies_integrity_and_owner_separately(
    tmp_path: Path,
) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs/result.md").write_text("evidence\n", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "fixture"\nversion = "1.0"\n', encoding="utf-8"
    )
    manifest = build_release_manifest(
        tmp_path,
        generated_at="2026-08-25T00:00:00+00:00",
        source_revision="a" * 40,
        paths=["docs/result.md", "pyproject.toml"],
    )
    from sparkbrain.release import build_release_metadata, write_release_metadata

    (tmp_path / "PACKAGE_MANIFEST.json").write_text(
        json.dumps(manifest), encoding="utf-8"
    )
    metadata = build_release_metadata(tmp_path, tmp_path / "PACKAGE_MANIFEST.json")
    write_release_metadata(tmp_path / "RELEASE_METADATA.json", metadata)
    (tmp_path / "docs/result.md").write_text("tampered content\n", encoding="utf-8")

    validation = release_validation(tmp_path, require_public=False)

    assert "size mismatch: docs/result.md" in validation["integrity_problems"]
    assert "sha256 mismatch: docs/result.md" in validation["integrity_problems"]
    assert validation["owner_blockers"] == [
        "project license has not been selected by the repository owner"
    ]
    assert owner_blockers(tmp_path) == validation["owner_blockers"]
    assert set(integrity_problems(tmp_path)).issubset(validation["integrity_problems"])


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


@pytest.mark.parametrize("unsafe", ["C:/outside.txt", r"C:\\outside.txt", "//server/share.txt"])
def test_release_manifest_rejects_windows_absolute_paths(
    tmp_path: Path, unsafe: str
) -> None:
    with pytest.raises(ValueError, match="unsafe release path"):
        build_release_manifest(
            tmp_path,
            generated_at="fixed",
            source_revision="fixed",
            paths=[unsafe],
        )


def test_unselected_project_license_blocks_release(tmp_path: Path) -> None:
    (tmp_path / "LICENSE_NOT_SELECTED.md").write_text("pending", encoding="utf-8")
    assert not project_license_selected(tmp_path)
    (tmp_path / "LICENSE_NOT_SELECTED.md").unlink()
    (tmp_path / "LICENSE").write_text("selected by owner", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "example"\nversion = "1.0"\nlicense = "MIT"\n',
        encoding="utf-8",
    )
    assert declared_project_license(tmp_path) == "MIT"
    assert project_license_selected(tmp_path)


def test_selected_license_requires_matching_sbom_metadata(tmp_path: Path) -> None:
    (tmp_path / "LICENSE").write_text("selected by owner", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "example"\nversion = "1.0"\nlicense = "MIT"\n',
        encoding="utf-8",
    )
    (tmp_path / "artifacts/release").mkdir(parents=True)
    sbom = {
        "packages": [
            {
                "name": "sparkbrain-research",
                "licenseDeclared": "NOASSERTION",
                "licenseConcluded": "NOASSERTION",
                "comment": "Project license is intentionally owner-blocked.",
            }
        ]
    }
    (tmp_path / "artifacts/release/sbom.spdx.json").write_text(
        json.dumps(sbom), encoding="utf-8"
    )
    assert validate_project_license_metadata(tmp_path) == [
        "release SBOM licenseDeclared does not match pyproject project.license",
        "release SBOM licenseConcluded does not match pyproject project.license",
        "release SBOM still marks the project license as owner-blocked",
    ]


def test_complete_manifest_detects_omitted_tracked_file() -> None:
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    manifest["files"] = manifest["files"][1:]
    problems = verify_release_manifest(root, manifest, require_complete_tracked_tree=True)
    assert any(
        problem.startswith(
            ("release manifest omits tracked files:", "release manifest omits archive files:")
        )
        for problem in problems
    )


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
        "project license has not been selected by the repository owner",
    ]
    validation = release_validation(root)
    assert validation == {
        "integrity_problems": [],
        "preparation_problems": [],
        "owner_blockers": [
            "project license has not been selected by the repository owner"
        ],
        "evidence_blockers": [],
    }


def test_v03_final_manifest_replaces_the_historical_root_manifest() -> None:
    metadata = json.loads((ROOT / "RELEASE_METADATA.json").read_text(encoding="utf-8"))
    assert metadata["package_version"] == package_version(ROOT)
    assert sha256_file(ROOT / "PACKAGE_MANIFEST.json") == metadata["manifest_sha256"]
    validation = release_validation(ROOT)
    assert validation["preparation_problems"] == []
    assert validation["integrity_problems"] == []
    assert validation["owner_blockers"] == [
        "project license has not been selected by the repository owner"
    ]


def test_evidence_map_has_existing_artifacts_and_pending_gates() -> None:
    root = Path(__file__).resolve().parents[1]
    evidence = json.loads(
        (root / "artifacts/release/evidence_map.json").read_text(encoding="utf-8")
    )
    assert validate_evidence_map(root, evidence) == []
    pending = {entry["id"] for entry in evidence["entries"] if entry["status"] == "pending"}
    assert pending == set()


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


def test_preparation_only_fails_closed_for_integrity_problem(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        validation_cli,
        "release_validation",
        lambda root: _validation_categories(integrity=["sha256 mismatch: README.md"]),
    )
    monkeypatch.setattr(sys, "argv", ["validate_release.py", "--preparation-only"])

    with pytest.raises(SystemExit) as exc_info:
        validation_cli.main()

    assert exc_info.value.code == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "invalid"
    assert payload["preparation_status"] == "fail"
    assert payload["integrity_problems"] == ["sha256 mismatch: README.md"]
    assert payload["problems"] == [
        "sha256 mismatch: README.md",
        "project license has not been selected by the repository owner",
    ]


def test_preparation_only_allows_owner_license_blocker(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        validation_cli, "release_validation", lambda root: _validation_categories()
    )
    monkeypatch.setattr(sys, "argv", ["validate_release.py", "--preparation-only"])

    validation_cli.main()

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "blocked"
    assert payload["preparation_status"] == "pass"
    assert payload["problems"] == payload["owner_blockers"]


def test_c06_c08_primary_subset_and_claim_grades_remain_frozen() -> None:
    assert {relative: sha256_file(ROOT / relative) for relative in SCIENTIFIC_HASHES} == (
        SCIENTIFIC_HASHES
    )
    subset = json.loads(
        (ROOT / "artifacts/release/primary_subset.json").read_text(encoding="utf-8")
    )
    assert subset["full_evaluation"] is False
    claims = (ROOT / "docs/CLAIMS_REGISTER.md").read_text(encoding="utf-8")
    assert "| CL-007 |" in claims and "| E0 |" in claims
    assert "| CL-008 |" in claims and claims.count("| E0 |") >= 2
