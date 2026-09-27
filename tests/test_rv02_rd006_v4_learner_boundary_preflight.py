from __future__ import annotations

import inspect
from pathlib import Path

import pytest

from sparkbrain.research import rv02_rd006_external_learning_reachability as v1
from sparkbrain.research import rv02_rd006_external_learning_reachability_v4 as v4
from sparkbrain.v04.contracts import SpikeEvent

ARTIFACT = Path(
    "artifacts/rv02_rd006/"
    "external_learning_reachability_a_v4_port_to_hidden_trace_boundary_preflight/"
    "synthetic_preflight.json"
)


def _spike(unit_id: int, time_ms: float) -> SpikeEvent:
    return SpikeEvent(
        time_ms=time_ms,
        unit_id=unit_id,
        potential_before_reset=1.0,
        dynamic_threshold=0.5,
        x=float(unit_id),
        y=0.0,
        source_pulse_ids=("test-pulse",),
        novelty=0.0,
        prediction_error=0.0,
        excitatory_drive=1.0,
        inhibitory_drive=0.0,
    )


def _pulse(unit_id: int, time_ms: float = 0.0) -> v1.RuntimePulse:
    return v1.RuntimePulse(
        event_id=f"pulse-{unit_id}-{time_ms}",
        time_ms=time_ms,
        target=f"unit:{unit_id}",
        magnitude=1.0,
    )


def test_positive_microfixture_uses_actual_hidden_spike_and_existing_edge() -> None:
    report = v4.build_synthetic_preflight()
    positive = report["positive_microfixture"]
    assert report["preflight_status"] == "PASS"
    assert len(positive["actual_hidden_spikes"]) == 1
    assert positive["actual_hidden_spikes"][0]["unit_id"] == 36
    assert len(positive["updates"]) == 1
    assert positive["updated_edge_class"] == "PORT_TO_HIDDEN"
    assert positive["updates"][0]["source_id"] == 0
    assert positive["updates"][0]["target_id"] == 36
    assert positive["updates"][0]["lag_ms"] == 5.5
    assert positive["updates"][0]["weight_after"] > positive["updates"][0][
        "weight_before"
    ]


def test_existing_port_to_port_behavior_is_byte_for_byte_equivalent() -> None:
    parity = v4.build_synthetic_preflight()["port_to_port_behavior"]
    assert parity["status"] == "PASS"
    assert parity["parent_updates_equal"] is True
    assert parity["final_field_state_equal"] is True
    assert len(parity["updates"]) == 1


def test_absent_negative_nonplastic_and_out_of_window_edges_do_not_update() -> None:
    cases = v4.build_synthetic_preflight()["negative_microfixtures"]
    for name in ("absent_edge", "negative_edge", "nonplastic_edge", "out_of_window"):
        assert cases[name] == {
            "status": "PASS",
            "update_count": 0,
            "connection_set_unchanged": True,
            "connection_values_unchanged": True,
        }
    assert cases["hidden_external_trace_rejected"]["status"] == "PASS"
    assert cases["port_spike_not_hidden_target"]["update_count"] == 0
    for name in ("hidden_to_port", "hidden_to_hidden"):
        assert cases[name] == {
            "status": "PASS",
            "update_count": 0,
            "connection_values_unchanged": True,
        }


@pytest.mark.parametrize("lag_ms", [0.5, 6.5])
def test_fixed_window_boundaries_are_inclusive(lag_ms: float) -> None:
    field = v4._microfixture_field()
    learner = v4.PortToHiddenExternalPlasticity(field)
    learner.observe_external(_pulse(0))
    updates = learner.observe_hidden_spikes((_spike(36, lag_ms),))
    assert len(updates) == 1
    assert updates[0].lag_ms == lag_ms


def test_hidden_and_port_events_never_create_hidden_traces() -> None:
    field = v4._microfixture_field()
    learner = v4.PortToHiddenExternalPlasticity(field)
    learner.observe_external(_pulse(0))
    learner.observe_hidden_spikes((_spike(1, 5.0), _spike(36, 5.5)))
    state = learner.learner_state_dict()
    assert [trace["unit_id"] for trace in state["port_traces"]] == [0]
    assert state["observed_hidden_spike_count"] == 1
    assert state["ignored_port_spike_count"] == 1


def test_checkpoint_roundtrip_is_deterministic_and_rejects_hidden_trace() -> None:
    field = v4._microfixture_field()
    learner = v4.PortToHiddenExternalPlasticity(field)
    learner.observe_external(_pulse(0))
    payload = v4.serialize_checkpoint(learner.checkpoint())
    restored_field, restored = v4.replay_checkpoint(payload)
    assert v1.canonical_json(restored_field.state_dict()) == v1.canonical_json(
        field.state_dict()
    )
    assert restored.learner_state_dict() == learner.learner_state_dict()

    tampered = restored.learner_state_dict()
    tampered["port_traces"][0]["unit_id"] = 36
    with pytest.raises(ValueError, match="must belong to a PORT"):
        v4.PortToHiddenExternalPlasticity.from_learner_state_dict(
            restored_field, tampered
        )


def test_public_observation_api_accepts_no_outcome_or_gate_context() -> None:
    hidden_parameters = inspect.signature(
        v4.PortToHiddenExternalPlasticity.observe_hidden_spikes
    ).parameters
    external_parameters = inspect.signature(
        v4.PortToHiddenExternalPlasticity.observe_external
    ).parameters
    assert tuple(hidden_parameters) == ("self", "spikes")
    assert tuple(external_parameters) == ("self", "pulse")


def test_exact_single_invariant_diff_and_fixed_future_surface() -> None:
    report = v4.build_synthetic_preflight()
    surface = report["fixed_future_evaluation_surface"]
    config = v1.RD006Config()
    assert report["changed_invariant_count"] == 1
    assert report["changed_invariant"] == v4.CHANGED_INVARIANT
    assert surface == {
        "topology": "V3_FIXED",
        "seed": 92701,
        "families": 6,
        "unit_count": 48,
        "edge_count": 384,
        "degree": 8,
        "event_spacing_ms": 5.5,
        "minimum_return_lag_ms": 0.5,
        "maximum_return_lag_ms": 6.5,
        "threshold": 0.5,
        "initial_weight": 0.05,
        "initial_delay_ms": 5.0,
        "boundary_gain": 4.0,
        "input_magnitude": 1.0,
        "max_events_per_run": 4096,
        "max_spikes_per_run": 512,
    }
    assert surface["seed"] == config.seed
    assert report["hidden_return_learning_enabled"] is False
    assert report["six_family_result_bearing_matrix_executed"] is False
    assert report["capability_scoring"] is False
    assert report["held_out_access"] is False


@pytest.mark.parametrize(
    "entrypoint",
    [
        v4.run_execution_cell,
        v4.run_family_pair,
        v4.run_matrix,
        v4.score_capability,
        v4.load_held_out,
    ],
)
def test_result_bearing_and_protected_entrypoints_fail_closed(entrypoint) -> None:  # type: ignore[no-untyped-def]
    with pytest.raises(v4.PreflightExecutionForbidden):
        entrypoint()


def test_committed_report_matches_deterministic_builder() -> None:
    payload = ARTIFACT.read_bytes()
    assert payload == v4.serialize_synthetic_preflight(v4.build_synthetic_preflight())
    replayed = v4.replay_synthetic_preflight(payload)
    assert replayed["preflight_status"] == "PASS"
    assert replayed["new_scientific_result"] is False
