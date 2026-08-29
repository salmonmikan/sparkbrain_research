from __future__ import annotations

from sparkbrain.v04.field import ExcitableFieldConfig, TemporalExcitableField
from sparkbrain.v04.topology import UnitState, explicit_topology
from sparkbrain.v06.forward import (
    AssemblyFreeForwardRuntime,
    ForwardRuntimeConfig,
    evaluate_forward_completion,
    train_external_sequences,
)
from sparkbrain.v06.foundation import EventOrigin, ProvenanceLedger, RuntimePulse
from sparkbrain.v06.local_expectation import LocalExpectationConfig, LocalTemporalExpectation
from sparkbrain.v06.local_transition import SparseLocalTransitionAdaptation
from sparkbrain.v06.reality import RealityCorrectionEngine
from sparkbrain.v06.reinjection import FieldReinjectionGate, ReinjectionConfig


def pulse(event_id: str, time_ms: float, unit_id: int) -> RuntimePulse:
    return RuntimePulse(
        event_id=event_id,
        time_ms=time_ms,
        target=f"unit:{unit_id}",
        magnitude=1.0,
        polarity=1,
        origin=EventOrigin.EXTERNAL,
    )


def build_runtime(*, reinjection_enabled: bool = True) -> AssemblyFreeForwardRuntime:
    expectation = LocalTemporalExpectation(
        LocalExpectationConfig(
            minimum_observations=2,
            minimum_confidence=0.1,
            proposal_ttl_ms=25.0,
        )
    )
    sequences = []
    for episode in range(3):
        offset = episode * 30.0
        sequences.append(
            (
                pulse(f"train-{episode}-a", offset, 0),
                pulse(f"train-{episode}-b", offset + 5.0, 1),
                pulse(f"train-{episode}-c", offset + 10.0, 2),
                pulse(f"train-{episode}-d", offset + 15.0, 3),
            )
        )
    train_external_sequences(expectation, sequences)

    topology = explicit_topology(
        [
            UnitState(unit_id=unit_id, x=float(unit_id), y=0.0, base_threshold=0.5)
            for unit_id in range(4)
        ],
        [],
        receptor_ids=range(4),
    )
    brain_field = TemporalExcitableField(
        topology,
        ExcitableFieldConfig(
            receptor_fanout=1,
            refractory_ms=2.0,
            adaptation_increment=0.0,
        ),
    )
    ledger = ProvenanceLedger()
    transition = SparseLocalTransitionAdaptation(expectation, ledger)
    reinjection = FieldReinjectionGate(
        ledger,
        ReinjectionConfig(
            minimum_confidence=0.1,
            maximum_effective_current=2.0,
            maximum_branches_per_origin_state=4,
        ),
    )
    reality = RealityCorrectionEngine(transition, ledger)
    return AssemblyFreeForwardRuntime(
        brain_field,
        expectation,
        transition,
        reinjection,
        reality,
        ForwardRuntimeConfig(reinjection_enabled=reinjection_enabled),
    )


def test_missing_middle_spark_is_generated_before_later_external_cue() -> None:
    runtime = build_runtime()
    runtime.process_external(pulse("test-a", 100.0, 0))
    runtime.process_external(pulse("test-b", 105.0, 1))
    runtime.process_external(pulse("test-d", 115.0, 3))

    result = evaluate_forward_completion(
        runtime,
        expected_target="unit:2",
        later_external_event_id="test-d",
        later_external_time_ms=115.0,
    )
    assert result.forward_generated is True
    assert result.temporal_compliance is True
    assert result.endogenous_spark_time_ms == 110.0
    assert result.later_prediction_matched is True
    assert result.retrospective_only is False


def test_forward_completion_keeps_missing_event_endogenous() -> None:
    runtime = build_runtime()
    runtime.process_external(pulse("test-a", 100.0, 0))
    runtime.process_external(pulse("test-b", 105.0, 1))
    runtime.process_external(pulse("test-d", 115.0, 3))

    missing_rows = [row for row in runtime.generated_sparks if row.target == "unit:2"]
    assert len(missing_rows) == 1
    missing_root = missing_rows[0].proposal_root_ids[0]
    assert runtime.ledger.events[f"endo:{missing_root}"].origin is (
        EventOrigin.ENDOGENOUS_UNCONFIRMED
    )
    assert runtime.ledger.external_observation_count == 3
    assert runtime.ledger.committed_positive_updates == 2


def test_readout_only_prediction_does_not_satisfy_forward_completion() -> None:
    runtime = build_runtime(reinjection_enabled=False)
    runtime.process_external(pulse("test-a", 100.0, 0))
    runtime.process_external(pulse("test-b", 105.0, 1))
    runtime.process_external(pulse("test-d", 115.0, 3))

    result = evaluate_forward_completion(
        runtime,
        expected_target="unit:2",
        later_external_event_id="test-d",
        later_external_time_ms=115.0,
    )
    assert result.forward_generated is False
    assert result.temporal_compliance is False
    assert result.later_prediction_matched is False
    assert result.retrospective_only is True


def test_early_external_future_prevents_after_the_fact_completion_claim() -> None:
    runtime = build_runtime()
    runtime.process_external(pulse("test-a", 100.0, 0))
    runtime.process_external(pulse("test-b", 105.0, 1))
    runtime.process_external(pulse("test-d-early", 109.0, 3))

    result = evaluate_forward_completion(
        runtime,
        expected_target="unit:2",
        later_external_event_id="test-d-early",
        later_external_time_ms=109.0,
    )
    assert result.forward_generated is False
    assert result.temporal_compliance is False
    assert result.retrospective_only is True
    assert not [row for row in runtime.generated_sparks if row.target == "unit:2"]


def test_prefix_continuation_generates_two_internal_sparks_in_silence() -> None:
    runtime = build_runtime()
    runtime.process_external(pulse("test-a", 100.0, 0))
    runtime.process_external(pulse("test-b", 105.0, 1))
    generated = runtime.advance_internal_until(116.0)

    assert [(row.time_ms, row.target) for row in generated] == [
        (110.0, "unit:2"),
        (115.0, "unit:3"),
    ]
    assert runtime.ledger.external_observation_count == 2
    assert runtime.ledger.committed_positive_updates == 1


def test_forward_runtime_state_contains_no_explicit_assembly_or_motif() -> None:
    runtime = build_runtime()
    runtime.process_external(pulse("test-a", 100.0, 0))
    runtime.process_external(pulse("test-b", 105.0, 1))
    runtime.advance_internal_until(111.0)
    state = runtime.state_dict()
    lowered = str(state).lower()
    assert "assembly_id" not in lowered
    assert "motif_id" not in lowered
    assert "outcome_label" not in lowered
