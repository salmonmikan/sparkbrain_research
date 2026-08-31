from __future__ import annotations

import json
from pathlib import Path

import pytest

from sparkbrain.comparison.cx01.candidate import CandidatePurpose
from sparkbrain.comparison.cx01.prepare import prepare_outcome_blind_bundle
from sparkbrain.comparison.cx01.seal_candidate import issue_seal_file


def test_prepare_bundle_contains_structure_only(tmp_path: Path) -> None:
    output = tmp_path / "prepared"
    candidate_path, declarations_path, manifest_path = prepare_outcome_blind_bundle(
        generation_id="cx01-fixture-prepare-001",
        seeds=tuple(range(5000, 5010)),
        purpose=CandidatePurpose.STRUCTURE_FIXTURE,
        source_git_sha="a" * 40,
        builder="fixture-builder",
        execution_command="formal-fixture",
        artifact_root="artifacts/cx01/formal",
        output_dir=output,
    )
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    declarations = [
        json.loads(line)
        for line in declarations_path.read_text(encoding="utf-8").splitlines()
    ]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert candidate["purpose"] == CandidatePurpose.STRUCTURE_FIXTURE.value
    assert declarations
    assert all(row["status"] == "unscored" for row in declarations)
    assert not any(row["capability_result_present"] for row in declarations)
    assert not any(row["measurements_present"] for row in declarations)
    assert manifest["builder"] == "fixture-builder"
    with pytest.raises(FileExistsError):
        prepare_outcome_blind_bundle(
            generation_id="cx01-fixture-prepare-001",
            seeds=tuple(range(5000, 5010)),
            purpose=CandidatePurpose.STRUCTURE_FIXTURE,
            source_git_sha="a" * 40,
            builder="fixture-builder",
            execution_command="formal-fixture",
            artifact_root="artifacts/cx01/formal",
            output_dir=output,
        )


def test_independent_seal_file_is_immutable_and_refuses_self_review(tmp_path: Path) -> None:
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
