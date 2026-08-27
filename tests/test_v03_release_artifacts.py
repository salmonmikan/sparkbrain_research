from __future__ import annotations

import json
from pathlib import Path

from sparkbrain.release_v03_artifacts import (
    C19_BLOCKED_ARTIFACTS,
    V03_RELEASE_RELATIVE,
    build_v03_evidence_map,
    build_v03_root_manifest,
    generate_v03_release_artifacts,
    validate_v03_evidence_map,
)

ROOT = Path(__file__).resolve().parents[1]
REVISION = "1" * 40


def test_v03_evidence_map_retains_negative_boundaries_and_blocks_unpinned_c19() -> None:
    evidence = build_v03_evidence_map(ROOT, source_revision=REVISION)
    assert validate_v03_evidence_map(ROOT, evidence) == []
    by_id = {entry["id"]: entry for entry in evidence["entries"]}
    assert by_id["EV-V02-C06-NEGATIVE"]["status"] == "negative"
    assert by_id["EV-V02-C08-NEGATIVE"]["status"] == "negative"
    assert by_id["EV-V03-C17"]["status"] == "negative"
    assert by_id["EV-V03-C19"] == {
        "id": "EV-V03-C19",
        "status": "blocked",
        "claim_ids": ["CL-007"],
        "artifacts": list(C19_BLOCKED_ARTIFACTS),
        "boundary": (
            "C19 is release-blocked pending an independently pinned external validation result."
        ),
    }


def test_v03_release_artifact_generation_is_staged_and_deterministic(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first_hashes = generate_v03_release_artifacts(
        ROOT, output_root=first, source_revision=REVISION
    )
    second_hashes = generate_v03_release_artifacts(
        ROOT, output_root=second, source_revision=REVISION
    )
    assert first_hashes == second_hashes
    release = first / V03_RELEASE_RELATIVE
    evidence = json.loads((release / "evidence_map.json").read_text(encoding="utf-8"))
    assert validate_v03_evidence_map(ROOT, evidence) == []
    source_manifest = json.loads((release / "source_manifest.json").read_text(encoding="utf-8"))
    assert source_manifest["package_version"] == "0.3.0"
    assert source_manifest["source_revision"] == REVISION
    assert set(first_hashes) == {
        "artifacts/release/v0.3/evidence_map.json",
        "artifacts/release/v0.3/release_report.md",
        "artifacts/release/v0.3/release_figure.svg",
        "artifacts/release/v0.3/claim_boundary_figure.svg",
        "artifacts/release/v0.3/sbom.spdx.json",
        "artifacts/release/v0.3/source_license_inventory.json",
        "artifacts/release/v0.3/primary_subset.json",
        "artifacts/release/v0.3/source_manifest.json",
        "artifacts/release/v0.3/reproduction_manifest.json",
        "artifacts/release/v0.3/release_metadata.json",
    }
    primary_subset = json.loads((release / "primary_subset.json").read_text(encoding="utf-8"))
    metadata = json.loads((release / "release_metadata.json").read_text(encoding="utf-8"))
    assert primary_subset["full_evaluation"] is False
    assert metadata["public_release_blocked"] is True


def test_v03_root_manifest_is_computed_in_a_staging_root_without_self_hashing(
    tmp_path: Path,
) -> None:
    (tmp_path / "pyproject.toml").write_text(
        "[project]\nname = 'sparkbrain-research'\nversion = '0.3.0'\n", encoding="utf-8"
    )
    (tmp_path / "README.md").write_text("source\n", encoding="utf-8")
    manifest, metadata = build_v03_root_manifest(
        tmp_path,
        source_revision=REVISION,
        generated_at="2026-08-28T00:00:00+00:00",
        paths=("README.md", "pyproject.toml"),
    )
    assert manifest["source_revision"] == REVISION
    assert metadata["package_version"] == "0.3.0"
    assert not (tmp_path / "PACKAGE_MANIFEST.json").exists()
