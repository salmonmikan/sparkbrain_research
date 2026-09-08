from __future__ import annotations

from sparkbrain.comparison.cx01.candidate import (
    REJECTED_PREFORMAL_SEEDS,
    CandidatePurpose,
    CandidateSpec,
    candidate_identifiability_audit,
    candidate_structure_audit,
)
from sparkbrain.comparison.cx01.formal_seed_selection import select_outcome_blind_formal_seeds


def test_formal_seed_selection_is_deterministic_and_structurally_eligible() -> None:
    source_sha = "1234567890abcdef1234567890abcdef12345678"
    left = select_outcome_blind_formal_seeds(
        source_git_sha=source_sha,
        generation_id="cx01-candidate-002",
    )
    right = select_outcome_blind_formal_seeds(
        source_git_sha=source_sha,
        generation_id="cx01-candidate-002",
    )

    assert left == right
    assert left.selection_hash() == right.selection_hash()
    assert len(left.seeds) == 10
    assert not set(left.seeds).intersection(REJECTED_PREFORMAL_SEEDS)

    candidate = CandidateSpec(
        generation_id=left.generation_id,
        seeds=left.seeds,
        purpose=CandidatePurpose.FORMAL,
    )
    structure = candidate_structure_audit(candidate)
    identifiability = candidate_identifiability_audit(candidate)
    assert all(
        row["development_overlap_count"] == 0
        for row in structure["family_rows"].values()
    )
    assert all(
        identifiability["family_pass_counts"][family]
        == identifiability["family_world_counts"][family]
        for family in identifiability["family_world_counts"]
    )


def test_formal_seed_selection_changes_with_exact_source_sha() -> None:
    left = select_outcome_blind_formal_seeds(
        source_git_sha="1" * 40,
        generation_id="cx01-candidate-002",
    )
    right = select_outcome_blind_formal_seeds(
        source_git_sha="2" * 40,
        generation_id="cx01-candidate-002",
    )
    assert left.seeds != right.seeds


def test_formal_seed_selection_rejects_candidate001_namespace() -> None:
    try:
        select_outcome_blind_formal_seeds(
            source_git_sha="3" * 40,
            generation_id="cx01-candidate-001",
            maximum_attempts=2,
        )
    except RuntimeError as exc:
        assert "no structurally eligible" in str(exc)
    else:
        raise AssertionError("rejected candidate-001 namespace must not be selectable")
