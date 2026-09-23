from __future__ import annotations

import json

import pytest

from sparkbrain.v05.candidate35_architecture import (
    ARMS,
    ADAPTATION_TAU_MS,
    ANCHOR_MAX_ADDITIONAL_BOUNDARIES,
    ANCHOR_MAX_ADDITIONAL_MS,
    Candidate35ResponseNotAuthorized,
    CUE_SOURCE_ID,
    MEASUREMENT_WINDOW_MS,
    MEMBRANE_TAU_MS,
    PRIME_EPISODE_ID,
    PRIME_SOURCE_ID,
    build_candidate35_brain,
    candidate35_frozen_contract,
    candidate35_nonresult_preflight,
    candidate35_prime_pulses,
    execute_candidate35_response,
)


def test_frozen_contract_matches_discovery_r1_without_response_authority() -> None:
    contract = candidate35_frozen_contract()

    assert contract["claim_ceiling"] == "SYSTEM"
    assert contract["prime"]["episode_id"] == PRIME_EPISODE_ID
    assert contract["prime"]["source_id"] == PRIME_SOURCE_ID
    assert contract["prime"]["learn_assembly"] is False
    assert contract["prime"]["learn_field"] is False
    assert contract["prime"]["explore_action"] is False
    assert contract["anchor"]["max_additional_boundaries"] == ANCHOR_MAX_ADDITIONAL_BOUNDARIES
    assert contract["anchor"]["max_additional_ms"] == ANCHOR_MAX_ADDITIONAL_MS
    assert contract["arms"] == list(ARMS)
    assert contract["cue"]["source_id"] == CUE_SOURCE_ID
    assert contract["measurement_window_ms"] == MEASUREMENT_WINDOW_MS
    assert contract["decay_constants_ms"] == {
        "potential": MEMBRANE_TAU_MS,
        "adaptation": ADAPTATION_TAU_MS,
    }
    assert contract["same_object_system_to_mechanism_uplift_allowed"] is False
    assert contract["candidate_response_execution_allowed"] is False
    assert contract["preformal_execution_allowed"] is False
    assert contract["formal_action_allowed"] is False


def test_prime_bytes_are_exact_and_constructed_without_execution() -> None:
    pulses = candidate35_prime_pulses()

    assert [(row.channel, row.time_ms) for row in pulses] == [
        ("A", 0.0),
        ("F", 5.0),
        ("C", 7.0),
    ]
    assert all(row.magnitude == 1.18 for row in pulses)
    assert all(row.polarity == 1 for row in pulses)
    assert all(row.novelty == 0.25 for row in pulses)
    assert all(row.prediction_error == 0.0 for row in pulses)
    assert all(row.source_id == PRIME_SOURCE_ID for row in pulses)


def test_nonresult_preflight_is_deterministic_and_does_not_execute_candidate() -> None:
    left = candidate35_nonresult_preflight()
    right = candidate35_nonresult_preflight()

    assert left == right
    assert left.candidate_response_executed is False
    assert len(left.cue_route_targets) > 0
    assert left.contract_sha256 == right.contract_sha256
    assert left.binding_sha256 == right.binding_sha256

    contract = json.loads(left.contract_json)
    assert contract["candidate_response_execution_allowed"] is False
    assert contract["preformal_execution_allowed"] is False
    assert contract["formal_action_allowed"] is False


def test_response_executor_fails_closed_before_mutation_without_authority() -> None:
    brain = build_candidate35_brain()
    source_hash = brain.state_hash()

    with pytest.raises(Candidate35ResponseNotAuthorized):
        execute_candidate35_response(
            brain,
            anchor_time_ms=brain.current_time_ms,
            arm="SHAM_STATE",
            response_execution_allowed=False,
        )

    assert brain.state_hash() == source_hash
    assert brain.current_time_ms == 0.0
    assert brain.base.field.state_dict()["queue"] == []
