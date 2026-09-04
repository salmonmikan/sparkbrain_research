from __future__ import annotations

import hashlib

import pytest

from sparkbrain.comparison.cx01.candidate import (
    CX01_COMPARATOR_INVENTORY,
    CandidatePurpose,
    CandidateSpec,
    build_outcome_blind_declarations,
)
from sparkbrain.comparison.cx01.freeze import (
    build_freeze_manifest,
    issue_execution_seal,
    require_execution_seal,
)
from sparkbrain.comparison.cx01.worlds import CX01Family


def _candidate() -> CandidateSpec:
    return CandidateSpec(
        generation_id="cx01-fixture-structure-001",
        seeds=tuple(range(5000, 5010)),
        purpose=CandidatePurpose.STRUCTURE_FIXTURE,
    )


def test_candidate_declarations_are_complete_and_unscored() -> None:
    candidate = _candidate()
    declarations = build_outcome_blind_declarations(candidate)
    assert len(declarations) == (
        len(candidate.seeds) * len(CX01Family) * len(CX01_COMPARATOR_INVENTORY)
    )
    assert all(row.status == "unscored" for row in declarations)
    assert not any(row.capability_result_present for row in declarations)
    assert not any(row.measurements_present for row in declarations)


def test_candidate_rejects_historical_confirmatory_seeds() -> None:
    with pytest.raises(ValueError):
        CandidateSpec(
            generation_id="cx01-candidate-illegal",
            seeds=tuple(range(2000, 2010)),
        ).validate()


def test_formal_candidate_rejects_entire_cx01_development_test_band() -> None:
    for start in (3000, 3998, 4100, 4200, 4300, 4400, 4500, 5000, 5900):
        with pytest.raises(ValueError, match="development/test seed band"):
            CandidateSpec(
                generation_id=f"cx01-candidate-illegal-{start}",
                seeds=tuple(range(start, start + 10)),
            ).validate()


def test_freeze_and_seal_bind_exact_source_and_candidate() -> None:
    candidate = _candidate()
    source_sha = "a" * 40
    manifest = build_freeze_manifest(
        source_git_sha=source_sha,
        builder="freeze-builder-fixture",
        candidate=candidate,
        execution_command="python -m sparkbrain.comparison.cx01.formal",
        artifact_root="artifacts/cx01/formal",
    )
    approval_digest = hashlib.sha256(b"independent-review-fixture").hexdigest()
    seal = issue_execution_seal(
        manifest,
        reviewer="independent-reviewer-fixture",
        approval_digest=approval_digest,
        approved=True,
    )
    require_execution_seal(manifest, seal, current_source_git_sha=source_sha)
    with pytest.raises(RuntimeError):
        require_execution_seal(manifest, seal, current_source_git_sha="b" * 40)


def test_seal_refuses_missing_approval() -> None:
    manifest = build_freeze_manifest(
        source_git_sha="c" * 40,
        builder="freeze-builder-fixture",
        candidate=_candidate(),
        execution_command="formal-fixture",
        artifact_root="artifacts/cx01/formal",
    )
    with pytest.raises(ValueError):
        issue_execution_seal(
            manifest,
            reviewer="independent-reviewer-fixture",
            approval_digest=hashlib.sha256(b"fixture").hexdigest(),
            approved=False,
        )


def test_freeze_builder_cannot_self_approve() -> None:
    manifest = build_freeze_manifest(
        source_git_sha="d" * 40,
        builder="same-person",
        candidate=_candidate(),
        execution_command="formal-fixture",
        artifact_root="artifacts/cx01/formal",
    )
    with pytest.raises(ValueError, match="self-approve"):
        issue_execution_seal(
            manifest,
            reviewer="same-person",
            approval_digest=hashlib.sha256(b"fixture").hexdigest(),
            approved=True,
        )
