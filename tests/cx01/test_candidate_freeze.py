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


def test_candidate_rejects_historically_exposed_and_development_seeds() -> None:
    with pytest.raises(ValueError):
        CandidateSpec(
            generation_id="cx01-candidate-illegal",
            seeds=tuple(range(2000, 2010)),
        ).validate()
    with pytest.raises(ValueError):
        CandidateSpec(
            generation_id="cx01-candidate-illegal-dev",
            seeds=tuple(range(3000, 3010)),
        ).validate()


def test_formal_candidate_rejects_reserved_fixture_seed_band() -> None:
    with pytest.raises(ValueError):
        CandidateSpec(
            generation_id="cx01-candidate-illegal-fixture-reuse",
            seeds=tuple(range(5000, 5010)),
        ).validate()


def test_freeze_and_seal_bind_exact_source_and_candidate() -> None:
    candidate = _candidate()
    source_sha = "a" * 40
    manifest = build_freeze_manifest(
        source_git_sha=source_sha,
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
        candidate=_candidate(),
        execution_command="formal-fixture",
        artifact_root="artifacts/cx01/formal",
    )
    with pytest.raises(ValueError):
        issue_execution_seal(
            manifest,
            reviewer="fixture",
            approval_digest=hashlib.sha256(b"fixture").hexdigest(),
            approved=False,
        )
