from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from sparkbrain.release_v03_artifacts import (
    C19_BLOCKED_ARTIFACTS,
    V03_RELEASE_RELATIVE,
    V031_RELEASE_RELATIVE,
    build_v03_evidence_map,
    build_v03_root_manifest,
    generate_v03_release_artifacts,
    generated_artifact_paths_for_version,
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
            "C19/G09 is not accepted and science is not_evaluated: the truth-free "
            "Belief-R-to-I2 adapter and a new official-evaluation protocol are absent."
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


def test_v030_checked_evidence_remains_byte_reproducible(tmp_path: Path) -> None:
    checked_release = ROOT / V03_RELEASE_RELATIVE
    checked_evidence = json.loads(
        (checked_release / "evidence_map.json").read_text(encoding="utf-8")
    )
    generated = tmp_path / "generated-v030"
    hashes = generate_v03_release_artifacts(
        ROOT,
        output_root=generated,
        source_revision=checked_evidence["source_revision"],
    )
    assert all(
        (generated / relative).read_bytes() == (ROOT / relative).read_bytes()
        for relative in hashes
    )


def test_v031_release_artifacts_use_separate_versioned_evidence(tmp_path: Path) -> None:
    output = tmp_path / "v031"
    hashes = generate_v03_release_artifacts(
        ROOT,
        output_root=output,
        source_revision=REVISION,
        release_version="0.3.1",
    )
    release = output / V031_RELEASE_RELATIVE
    assert set(hashes) == generated_artifact_paths_for_version("0.3.1")
    assert not (output / V03_RELEASE_RELATIVE).exists()

    evidence = json.loads((release / "evidence_map.json").read_text(encoding="utf-8"))
    assert validate_v03_evidence_map(ROOT, evidence, release_version="0.3.1") == []
    by_id = {entry["id"]: entry for entry in evidence["entries"]}
    assert by_id["EV-V03-C19"]["status"] == "blocked"
    assert by_id["EV-V031-C17-V1-CONTROL-GAP"] == {
        "id": "EV-V031-C17-V1-CONTROL-GAP",
        "status": "implementation_failure",
        "claim_ids": ["CL-008"],
        "artifacts": [
            "artifacts/v03/c17_functional_organs/preregistration.json",
            "artifacts/v03/c17_functional_organs/candidate_discovery.jsonl",
            "artifacts/v03/c17_functional_organs/matched_ablations.json",
            "artifacts/v03/c17_functional_organs/acceptance_matrix.json",
            "artifacts/v03/c17_functional_organs/report.md",
        ],
        "boundary": (
            "C17 v1 candidate-present cells exhausted the disjoint control pool: five cells have "
            "25 incomplete controls, so science is not_evaluated_implementation_failure. The 100 "
            "not-applicable controls in candidate-absent cells remain valid negative observations."
        ),
    }
    assert by_id["EV-V031-CORRECTIVE"] == {
        "id": "EV-V031-CORRECTIVE",
        "status": "accepted",
        "claim_ids": [],
        "artifacts": [
            "src/sparkbrain/release_v03.py",
            "examples/v03_seed_demo.py",
            "tests/test_v03_private_review_bundle.py",
            "tests/test_v03_seed_demo.py",
        ],
        "boundary": (
            "Corrective packaging and seed-demo engineering evidence only; no scientific rerun, "
            "claim-grade increase, or integrated-runtime acceptance."
        ),
    }
    integrated = by_id["EV-V031-INTEGRATED-RUNTIME"]
    assert integrated["status"] == "accepted"
    assert integrated["claim_ids"] == []
    assert integrated["artifacts"][-2:] == [
        "tests/test_v031_brain_lab_api.py",
        "tests/test_v031_brain_lab_artifact.py",
    ]
    assert "engineering integration only" in integrated["boundary"]
    source_manifest = json.loads((release / "source_manifest.json").read_text(encoding="utf-8"))
    metadata = json.loads((release / "release_metadata.json").read_text(encoding="utf-8"))
    sbom = json.loads((release / "sbom.spdx.json").read_text(encoding="utf-8"))
    assert source_manifest["package_version"] == "0.3.1"
    assert metadata["package_version"] == "0.3.1"
    assert metadata["source_manifest"].startswith("artifacts/release/v0.3.1/")
    project = next(row for row in sbom["packages"] if row["name"] == "sparkbrain-research")
    assert project["versionInfo"] == "0.3.1"


def test_v031_evidence_map_rejects_unregistered_entry() -> None:
    evidence = build_v03_evidence_map(
        ROOT, source_revision=REVISION, release_version="0.3.1"
    )
    evidence["entries"].append(
        {
            "id": "EV-V031-UNREGISTERED",
            "status": "accepted",
            "claim_ids": [],
            "artifacts": ["src/sparkbrain/v03/__init__.py"],
            "boundary": "unregistered",
        }
    )
    problems = validate_v03_evidence_map(ROOT, evidence, release_version="0.3.1")
    assert any("invalid id" in problem for problem in problems)
    assert any("fixed versioned inventory" in problem for problem in problems)


def test_v031_corrective_boundary_rejects_claim_escalation() -> None:
    evidence = build_v03_evidence_map(
        ROOT, source_revision=REVISION, release_version="0.3.1"
    )
    corrective = next(
        entry for entry in evidence["entries"] if entry["id"] == "EV-V031-CORRECTIVE"
    )
    corrective["claim_ids"] = ["CL-008"]
    problems = validate_v03_evidence_map(ROOT, evidence, release_version="0.3.1")
    assert any("does not match its registered boundary" in problem for problem in problems)


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


def test_root_manifest_group_publish_restores_both_files_on_second_replace_failure(
    tmp_path: Path, monkeypatch
) -> None:
    from scripts import generate_v03_root_manifest as generator

    manifest = tmp_path / "PACKAGE_MANIFEST.json"
    metadata = tmp_path / "RELEASE_METADATA.json"
    manifest.write_bytes(b"old-manifest")
    metadata.write_bytes(b"old-metadata")
    staged_manifest = tmp_path / "new-manifest"
    staged_metadata = tmp_path / "new-metadata"
    staged_manifest.write_bytes(b"new-manifest")
    staged_metadata.write_bytes(b"new-metadata")
    original_replace = os.replace

    def fail_second(source: str | Path, target: str | Path) -> None:
        if Path(target) == metadata and Path(source) == staged_metadata:
            raise OSError("injected second publish failure")
        original_replace(source, target)

    monkeypatch.setattr(generator.os, "replace", fail_second)
    with pytest.raises(RuntimeError, match="was restored"):
        generator._publish_manifest_group(
            staged_manifest, manifest, staged_metadata, metadata
        )
    assert manifest.read_bytes() == b"old-manifest"
    assert metadata.read_bytes() == b"old-metadata"


def test_root_manifest_requires_the_exact_ten_generated_artifacts() -> None:
    from scripts.generate_v03_root_manifest import V03_GENERATED_ARTIFACTS, _generated_artifacts

    assert V03_GENERATED_ARTIFACTS == {
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
    assert _generated_artifacts() == generated_artifact_paths_for_version("0.3.1")


@pytest.mark.skipif(
    not (ROOT / "artifacts/release/v0.3.1/evidence_map.json").is_file(),
    reason="final artifact integration has not yet been committed",
)
def test_root_manifest_cli_publishes_a_valid_pair(tmp_path: Path) -> None:
    from sparkbrain.release import sha256_file

    source_state = subprocess.run(
        ["git", "diff", "--quiet"], cwd=ROOT, check=False, capture_output=True
    )
    if source_state.returncode:
        pytest.skip("root manifest pair is staged for its integration commit")

    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()
    manifest = tmp_path / "PACKAGE_MANIFEST.json"
    metadata = tmp_path / "RELEASE_METADATA.json"
    result = subprocess.run(
        [
            sys.executable,
            "scripts/generate_v03_root_manifest.py",
            "--source-revision",
            head,
            "--generated-at",
            "2026-08-28T00:00:00+00:00",
            "--output",
            str(manifest),
            "--metadata-output",
            str(metadata),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(metadata.read_text(encoding="utf-8"))
    assert payload["manifest_sha256"] == sha256_file(manifest)
    assert payload["package_version"] == "0.3.2.dev0"
