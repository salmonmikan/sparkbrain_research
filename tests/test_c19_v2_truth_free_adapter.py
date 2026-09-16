from __future__ import annotations

import hashlib
import inspect
import json
from dataclasses import fields, replace
from pathlib import Path

import pytest

from sparkbrain.v03_external_validation.truth_free_adapter import (
    ADAPTER_CONTRACT_ID,
    CONDITION_ID,
    QUERY_MARKER,
    BeliefRTruthFreeSymbolicAdapter,
    TruthFreeBeliefRInput,
    canonical_visible_envelope,
    compositional_visible_input,
    static_representation_audit,
    surface_events,
    whole_hash_visible_input,
)

ROOT = Path(__file__).parents[1]
V1_PREREG_SHA256 = "97a2448e2918f3b0a4583520ad2f35d5d47d99813585be7bb3fae32e0b340cfe"


def synthetic_input(*, source_index: int = 0, step_index: int = 0) -> TruthFreeBeliefRInput:
    return TruthFreeBeliefRInput(
        record_id=f"synthetic:{source_index}:{step_index}",
        source_index=source_index,
        step_index=step_index,
        question=(
            "Premise one. New premise. What necessarily had to follow assuming that "
            "the above premises were true?"
        ),
        choices=("alpha", "beta", "uncertain"),
    )


def test_adapter_api_is_exactly_the_preregistered_visible_boundary() -> None:
    assert tuple(field.name for field in fields(TruthFreeBeliefRInput)) == (
        "record_id",
        "source_index",
        "step_index",
        "question",
        "choices",
    )
    parameters = inspect.signature(TruthFreeBeliefRInput).parameters
    assert "ground_truth" not in parameters
    assert "target" not in parameters
    assert "modus" not in parameters
    assert "dataset_id" not in parameters


def test_adapter_is_deterministic_target_blind_and_non_oracle() -> None:
    value = synthetic_input()
    adapter = BeliefRTruthFreeSymbolicAdapter()
    first = adapter.encode(value)
    second = adapter.encode(value)
    assert first == second
    assert first.condition_id == CONDITION_ID
    assert first.oracle is False
    assert adapter.contract_id == ADAPTER_CONTRACT_ID
    assert all("ground_truth" not in key and "truth" not in key for key, _ in first.features)


def test_surface_parser_preserves_registered_roles_and_indices_only() -> None:
    events = surface_events(synthetic_input(source_index=4, step_index=1))
    assert events[:3] == (
        ("source_index", 0, "4"),
        ("step_index", 0, "1"),
        ("query_marker", 0, QUERY_MARKER.casefold()),
    )
    assert [row[:2] for row in events[3:5]] == [("premise", 0), ("premise", 1)]
    assert [row[:2] for row in events[-3:]] == [
        ("choice", 0),
        ("choice", 1),
        ("choice", 2),
    ]


def test_adapter_fails_closed_on_unregistered_question_shape_and_indices() -> None:
    value = synthetic_input()
    with pytest.raises(ValueError, match="query marker exactly once"):
        BeliefRTruthFreeSymbolicAdapter().encode(replace(value, question="premise only"))
    with pytest.raises(ValueError, match="source_index"):
        BeliefRTruthFreeSymbolicAdapter().encode(replace(value, source_index=-1))
    with pytest.raises(ValueError, match="choices"):
        TruthFreeBeliefRInput(
            record_id="bad",
            source_index=0,
            step_index=0,
            question=value.question,
            choices=("", "beta", "gamma"),
        ).validate()


def test_i0_i1_and_adapter_receive_exact_same_visible_byte_budget() -> None:
    value = synthetic_input()
    envelope = canonical_visible_envelope(value)
    encoded = BeliefRTruthFreeSymbolicAdapter().encode(value)
    i0 = whole_hash_visible_input(value)
    i1 = compositional_visible_input(value)
    assert encoded.input_bytes == i0.input_bytes == i1.input_bytes == len(envelope.encode("utf-8"))


def test_registered_synthetic_probe_is_not_exact_i0_or_i1_feature_equivalence() -> None:
    audit = static_representation_audit(synthetic_input())
    assert audit == {
        "adapter_contract_id": ADAPTER_CONTRACT_ID,
        "condition_id": CONDITION_ID,
        "oracle": False,
        "same_visible_input_bytes": True,
        "exact_feature_equivalent_to_i0": False,
        "exact_feature_equivalent_to_i1": False,
        "source_index": 0,
        "step_index": 0,
    }


def test_source_index_is_preserved_not_inferred_from_surface_text() -> None:
    first = synthetic_input(source_index=0)
    second = replace(first, record_id="synthetic:1:0", source_index=1)
    first_events = surface_events(first)
    second_events = surface_events(second)
    assert first_events[0] == ("source_index", 0, "0")
    assert second_events[0] == ("source_index", 0, "1")
    assert first.question == second.question
    assert first.choices == second.choices
    assert BeliefRTruthFreeSymbolicAdapter().encode(first).feature_hash != BeliefRTruthFreeSymbolicAdapter().encode(second).feature_hash


def test_v2_preregistration_forbids_official_access_and_oracle_conditions() -> None:
    protocol = json.loads(
        (ROOT / "artifacts/v03/c19_external_validation/v2/preregistration.json").read_text(
            encoding="utf-8"
        )
    )
    assert protocol["protocol_id"] == "c19-external-v2"
    assert protocol["adapter_contract_id"] == ADAPTER_CONTRACT_ID
    assert protocol["official_evaluation_allowed"] is False
    assert protocol["belief_r_metadata_pin"]["cache_content_access_allowed"] is False
    assert protocol["belief_r_metadata_pin"]["cache_verification_allowed"] is False
    assert protocol["belief_r_metadata_pin"]["examples_read_allowed"] is False
    assert protocol["condition_matrix"]["oracle_conditions"] == []
    assert CONDITION_ID in protocol["condition_matrix"]["inputs"]


def test_historical_v1_preregistration_bytes_remain_exact() -> None:
    raw = (ROOT / "artifacts/v03/c19_external_validation/preregistration.json").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == V1_PREREG_SHA256
