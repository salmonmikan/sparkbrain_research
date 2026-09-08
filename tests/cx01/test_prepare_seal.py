from __future__ import annotations

import json
from pathlib import Path

import pytest

from sparkbrain.comparison.cx01.candidate import CandidatePurpose
from sparkbrain.comparison.cx01.prepare import (
    prepare_outcome_blind_bundle,
    verify_outcome_blind_bundle,
)
from sparkbrain.comparison.cx01.seal_candidate import issue_seal_file


def _prepare_fixture(output: Path, *, source_sha: str = "a" * 40) -> tuple[Path, Path, Path]:
    return prepare_outcome_blind_bundle(
        generation_id="cx01-fixture-prepare-001",
        seeds=tuple(range(5000, 5010)),
        purpose=CandidatePurpose.STRUCTURE_FIXTURE,
        source_git_sha=source_sha,
        builder="fixture-builder",
        execution_command="formal-fixture",
        artifact_root="artifacts/cx01/formal",
        output_dir=output,
    )


def test_prepare_bundle_contains_complete_structure_only_package(
    tmp_path: Path,
) -> None:
    output = tmp_path / "prepared"
    candidate_path, declarations_path, manifest_path = _prepare_fixture(output)
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    declarations = [
        json.loads(line)
        for line in declarations_path.read_text(encoding="utf-8").splitlines()
    ]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    worlds = json.loads(
        (output / "world_grid.json").read_text(encoding="utf-8")
    )
    audits = json.loads(
        (output / "structural_novelty_audit.json").read_text(
            encoding="utf-8"
        )
    )
    status = json.loads(
        (output / "package_status.json").read_text(encoding="utf-8")
    )
    checksums = json.loads(
        (output / "package_checksums.json").read_text(encoding="utf-8")
    )

    assert candidate["purpose"] == CandidatePurpose.STRUCTURE_FIXTURE.value
    assert worlds["world_count"] == 60
    assert len(worlds["worlds"]) == 60
    assert len(declarations) == 420
    assert all(row["status"] == "unscored" for row in declarations)
    assert not any(row["capability_result_present"] for row in declarations)
    assert not any(row["measurements_present"] for row in declarations)
    assert all(row["passed"] for row in audits.values())
    assert manifest["builder"] == "fixture-builder"
    assert status["execution_seal_status"] == "NOT_ISSUED"
    assert status["formal_status"] == "NOT_STARTED"
    assert status["formal_capability_executed"] is False
    assert status["formal_score_present"] is False
    assert (output / "OUTCOME_BLIND").is_file()
    assert not (output / "execution_seal.json").exists()
    assert not (output / "STARTED").exists()
    assert not (output / "results.jsonl").exists()
    assert set(checksums["files"]) == {
        "OUTCOME_BLIND",
        "candidate.json",
        "declarations.jsonl",
        "freeze_manifest.json",
        "package_status.json",
        "structural_novelty_audit.json",
        "world_grid.json",
    }
    assert verify_outcome_blind_bundle(output) == {
        "candidate_generation_id": "cx01-fixture-prepare-001",
        "declaration_count": 420,
        "execution_seal_status": "NOT_ISSUED",
        "formal_status": "NOT_STARTED",
        "source_git_sha": "a" * 40,
        "verified": True,
        "world_count": 60,
    }

    with pytest.raises(FileExistsError):
        _prepare_fixture(output)


def test_package_verification_detects_payload_tampering(tmp_path: Path) -> None:
    output = tmp_path / "prepared"
    _prepare_fixture(output)
    candidate_path = output / "candidate.json"
    candidate_path.write_text(
        candidate_path.read_text(encoding="utf-8") + " ",
        encoding="utf-8",
    )
    with pytest.raises(RuntimeError, match="checksum mismatch"):
        verify_outcome_blind_bundle(output)


def test_independent_seal_file_is_immutable_and_refuses_self_review(
    tmp_path: Path,
) -> None:
    output = tmp_path / "prepared"
    _, _, manifest_path = prepare_outcome_blind_bundle(
        generation_id="cx01-fixture-seal-001",
        seeds=tuple(range(5000, 5010)),
        purpose=CandidatePurpose.STRUCTURE_FIXTURE,
        source_git_sha="b" * 40,
        builder="builder-a",
        execution_command="formal-fixture",
        artifact_root="artifacts/cx01/formal",
        output_dir=output,
    )
    evidence = tmp_path / "approval.txt"
    evidence.write_text("approved fixture\n", encoding="utf-8")
    seal_path = tmp_path / "seal.json"
    issue_seal_file(
        manifest_path=manifest_path,
        reviewer="reviewer-b",
        approval_evidence_path=evidence,
        output_path=seal_path,
    )
    assert seal_path.exists()
    assert seal_path.stat().st_mode & 0o222 == 0
    with pytest.raises(FileExistsError):
        issue_seal_file(
            manifest_path=manifest_path,
            reviewer="reviewer-b",
            approval_evidence_path=evidence,
            output_path=seal_path,
        )
    with pytest.raises(ValueError, match="self-approve"):
        issue_seal_file(
            manifest_path=manifest_path,
            reviewer="builder-a",
            approval_evidence_path=evidence,
            output_path=tmp_path / "self-seal.json",
        )
