from __future__ import annotations

from pathlib import Path

import pytest

from sparkbrain.v06 import (
    ALLOWED_STRUCTURAL_EXAMPLES,
    FORBIDDEN_FUNCTIONAL_FIELDS,
    AssemblyFreeRuntimeState,
    EventOrigin,
    RuntimePulse,
    audit_runtime_source_tree,
    validate_runtime_mapping,
    verify_taxonomy_variant_runtime_equality,
)
from sparkbrain.v06 import foundation


def test_functional_taxonomy_fields_extend_the_foundation_guard() -> None:
    assert FORBIDDEN_FUNCTIONAL_FIELDS <= foundation.FORBIDDEN_RUNTIME_FIELDS
    assert {
        "prediction_relation",
        "action_relation",
        "memory_relation",
        "reward_relation",
        "reward",
        "relation_type",
        "functional_role",
        "meaning",
    } <= foundation.FORBIDDEN_RUNTIME_FIELDS


@pytest.mark.parametrize(
    "field_name",
    [
        "prediction_relation",
        "action_relation",
        "memory_relation",
        "reward_relation",
        "reward",
        "reward_value",
        "utility_target",
        "functional_role",
        "relation_type",
        "meaning",
        "semantic_state",
        "action_bias",
    ],
)
def test_runtime_metadata_rejects_predeclared_functional_categories(
    field_name: str,
) -> None:
    with pytest.raises(ValueError, match=field_name):
        RuntimePulse(
            event_id="external-1",
            time_ms=0.0,
            target="unit:0",
            magnitude=1.0,
            polarity=1,
            origin=EventOrigin.EXTERNAL,
            metadata={field_name: "leak"},
        )


def test_nested_runtime_state_rejects_relation_type() -> None:
    with pytest.raises(ValueError, match="relation_type"):
        AssemblyFreeRuntimeState(
            field_state={
                "local_path": {
                    "relation_type": "prediction",
                }
            }
        )


def test_structural_temporal_and_boundary_fields_remain_allowed() -> None:
    state = {
        "boundary_port_id": "port:7",
        "external_consistency": "unconfirmed",
        "predicted_arrival_ms": 5.0,
        "prediction_error": 0.25,
    }
    validate_runtime_mapping(state)
    assert set(state) == ALLOWED_STRUCTURAL_EXAMPLES


def test_taxonomy_labels_are_ignored_when_runtime_states_match() -> None:
    runtime_state = {
        "field_state": {"potential": [0.1, 0.2]},
        "outbound_boundary_events": [
            {"port_id": "port:7", "time_ms": 4.0, "magnitude": 0.8}
        ],
    }
    result = verify_taxonomy_variant_runtime_equality(
        {
            "predictive-view": runtime_state,
            "renamed-view": runtime_state,
            "port-7-described-differently": runtime_state,
        }
    )
    assert len(result) == 64


def test_taxonomy_change_fails_when_it_changes_runtime() -> None:
    with pytest.raises(AssertionError, match="taxonomy changed"):
        verify_taxonomy_variant_runtime_equality(
            {
                "view-a": {"field_state": {"potential": [0.1]}},
                "view-b": {"field_state": {"potential": [0.2]}},
            }
        )


def test_primary_runtime_source_tree_has_no_typed_function_objects() -> None:
    root = Path(__file__).parents[2] / "src" / "sparkbrain" / "v06"
    assert audit_runtime_source_tree(root) == ()
