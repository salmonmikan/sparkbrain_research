from __future__ import annotations

import pytest

from sparkbrain.evaluation.v06_confirmatory import ConfirmatoryCondition
from sparkbrain.evaluation.v06_qualification_matrix import (
    run_complete_qualification_matrix,
)

_FAKE_QUALIFICATION_SHA = "c" * 40


@pytest.fixture(scope="module")
def matrix():
    return run_complete_qualification_matrix(
        code_ref=_FAKE_QUALIFICATION_SHA
    )


def test_complete_matrix_has_required_648_records(matrix) -> None:
    assert matrix.code_ref == _FAKE_QUALIFICATION_SHA
    assert matrix.family_count == 3
    assert matrix.seed_count == 3
    assert matrix.condition_count == 8
    assert matrix.record_count == 648
    assert matrix.strict_metric_coverage.complete is True
    assert matrix.condition_record_counts() == {
        condition.value: 81 for condition in ConfirmatoryCondition
    }


def test_primary_and_all_three_comparators_pass_development_qualification(
    matrix,
) -> None:
    outcome = matrix.outcome
    assert outcome.primary_raw_supported is True
    assert outcome.primary_supported is True
    assert outcome.supported_comparators == (
        "g3-recurrent",
        "g4-assembly-conditioned",
        "g5-typed-functional-heads",
    )
    assert outcome.comparator_only_success is False
    assert "architectural uniqueness is not established" in outcome.interpretation


def test_complete_matrix_passes_every_strict_control_and_safety_gate(matrix) -> None:
    outcome = matrix.outcome
    assert outcome.null_false_positive_fraction == 0.0
    assert outcome.minimum_selective_effect == 1.0
    assert outcome.taxonomy_hash_match_fraction == 1.0
    assert outcome.self_confirmation_violations == 0
    assert outcome.control_contract_fraction == 1.0
    assert outcome.control_and_safety_gates_passed is True


def test_complete_qualification_matrix_is_deterministic(matrix) -> None:
    replay = run_complete_qualification_matrix(
        code_ref=_FAKE_QUALIFICATION_SHA
    )
    assert replay.state_dict() == matrix.state_dict()
    assert replay.records == matrix.records
