from __future__ import annotations

import pytest

from sparkbrain.v04.field import ExcitableFieldConfig, TemporalExcitableField
from sparkbrain.v04.topology import Connection, UnitState, explicit_topology
from sparkbrain.v06.foundation import EventOrigin, ProvenanceLedger, RuntimePulse
from sparkbrain.v06.local_expectation import LocalExpectationConfig, LocalTemporalExpectation
from sparkbrain.v06.local_transition import SparseLocalTransitionAdaptation
from sparkbrain.v06.reality import RealityCorrectionEngine
from sparkbrain.v06.reinjection import FieldReinjectionGate, ReinjectionConfig


def pulse(
    event_id: str,
    time_ms: float,
    target: str,
    *,
    magnitude: float = 0.8,
    polarity: int = 1,
    origin: EventOrigin = EventOrigin.EXTERNAL,
) -> RuntimePulse:
    return RuntimePulse(event_id, time_ms, target, magnitude, polarity, origin)


def field() -> TemporalExcitableField:
    topology = explicit_topology(
        [
            UnitState(unit_id=0, x=0.0, y=0.0, base_threshold=0.5),
            UnitState(unit_id=1, x=1.0, y=0.0, base_threshold=0.5),
            UnitState(unit_id=2, x=2.0, y=0.0, base_threshold=0.5),
        ],
        [Connection(source_id=0, target_id=1, weight=1.0, delay_ms=5.0)],
        receptor_ids=[0, 1, 2],
    )
    return TemporalExcitableField(
        topology,
        ExcitableFieldConfig(
            receptor_fanout=1,
            refractory_ms=2.0,
            adaptation_increment=0.0,
        ),
    )


def trained_stack() -> tuple[
    ProvenanceLedger,
    SparseLocalTransitionAdaptation,
    FieldReinjectionGate,
    RealityCorrectionEngine,
]:
    expectation = LocalTemporalExpectation(
        LocalExpectationConfig(
            minimum_observations=2,
            minimum_confidence=0.1,
            proposal_ttl_ms=20.0,
        )
    )
    expectation.observe_external_transition(
        pulse("train-a1", 0.0, "unit:9"),
        pulse("train-b1", 5.0, "unit:0"),
    )
    expectation.observe_external_transition(
        pulse("train-a2", 20.0, "unit:9"),
        pulse("train-b2", 25.0, "unit:0"),
    )
    ledger = ProvenanceLedger()
    transition = SparseLocalTransitionAdaptation(expectation, ledger)
    reinjection = FieldReinjectionGate(
        ledger,
        ReinjectionConfig(minimum_confidence=0.1, maximum_effective_current=2.0),
    )
    reality = RealityCorrectionEngine(transition, ledger)
    return ledger, transition, reinjection, reality


def prepare(
    transition: SparseLocalTransitionAdaptation,
    *,
    event_id: str = "source",
    time_ms: float = 100.0,
    state_hash: str = "s" * 64,
):
    return transition.prepare(
        pulse(event_id, time_ms, "unit:9"),
        origin_state_hash=state_hash,
    )[0]


def test_matching_external_replaces_queued_prediction_without_double_current() -> None:
    ledger, transition, reinjection, reality = trained_stack()
    brain_field = field()
    row = prepare(transition)
    assert reinjection.schedule(row.proposal, brain_field).accepted is True

    result = reality.process_external(
        pulse("external-c", 104.0, "unit:0", magnitude=0.8),
        brain_field,
    )
    assert result.matched_proposal_id == row.proposal.proposal_id
    assert result.cancelled_arrivals == 1
    assert ledger.committed_positive_updates == 1
    assert ledger.external_observation_count == 1

    spikes = brain_field.run_until(row.proposal.predicted_arrival_ms)
    assert len(spikes) == 1
    assert spikes[0].time_ms == 104.0
    assert "external-c" in spikes[0].source_pulse_ids
    assert f"endo:{row.proposal.proposal_id}" not in spikes[0].source_pulse_ids


def test_contradiction_cancels_descendant_queue_and_external_wins() -> None:
    ledger, transition, reinjection, reality = trained_stack()
    brain_field = field()
    row = prepare(transition)
    assert reinjection.schedule(row.proposal, brain_field).accepted is True

    internal_spikes = brain_field.run_until(row.proposal.predicted_arrival_ms)
    assert [spike.unit_id for spike in internal_spikes] == [0]
    reality.observe_spikes(internal_spikes)

    result = reality.process_external(
        pulse("external-e", 106.0, "unit:2", magnitude=1.0),
        brain_field,
    )
    assert result.matched_proposal_id is None
    assert result.contradicted_proposal_ids == (row.proposal.proposal_id,)
    assert result.cancelled_arrivals == 1
    assert ledger.events[f"endo:{row.proposal.proposal_id}"].origin is (
        EventOrigin.ENDOGENOUS_CONTRADICTED
    )
    assert ledger.committed_positive_updates == 0

    later = brain_field.run_until(111.0)
    assert 2 in [spike.unit_id for spike in later]
    assert 1 not in [spike.unit_id for spike in later]


def test_expired_prediction_is_cancelled_before_unrelated_external_input() -> None:
    ledger, transition, reinjection, reality = trained_stack()
    brain_field = field()
    row = prepare(transition)
    assert reinjection.schedule(row.proposal, brain_field).accepted is True
    external_time = row.proposal.valid_until_ms + 1.0

    result = reality.process_external(
        pulse("late-reality", external_time, "unit:2", magnitude=1.0),
        brain_field,
    )
    assert result.expired_proposal_ids == (row.proposal.proposal_id,)
    assert result.cancelled_arrivals == 1
    assert ledger.events[f"endo:{row.proposal.proposal_id}"].origin is (
        EventOrigin.ENDOGENOUS_EXPIRED
    )
    assert ledger.committed_positive_updates == 0


def test_endogenous_input_cannot_be_presented_as_reality() -> None:
    ledger, transition, reinjection, reality = trained_stack()
    brain_field = field()
    row = prepare(transition)
    reinjection.schedule(row.proposal, brain_field)
    field_before = brain_field.state_hash()
    ledger_before = ledger.state_hash()
    transition_before = transition.state_hash()

    with pytest.raises(ValueError, match="only external"):
        reality.process_external(
            pulse(
                "endo:fake",
                104.0,
                "unit:0",
                origin=EventOrigin.ENDOGENOUS_CONFIRMED,
            ),
            brain_field,
        )
    assert brain_field.state_hash() == field_before
    assert ledger.state_hash() == ledger_before
    assert transition.state_hash() == transition_before


def test_external_event_cannot_be_processed_twice() -> None:
    ledger, transition, _, reality = trained_stack()
    brain_field = field()
    external = pulse("external", 10.0, "unit:2")
    reality.process_external(external, brain_field)
    with pytest.raises(ValueError, match="already processed"):
        reality.process_external(external, brain_field)
    assert ledger.external_observation_count == 1
    assert transition.state_dict()["paths"] == {}


def test_one_external_event_commits_at_most_one_matching_branch() -> None:
    ledger, transition, reinjection, reality = trained_stack()
    brain_field = field()
    first = prepare(transition, event_id="source-a", state_hash="a" * 64)
    second = prepare(transition, event_id="source-b", state_hash="b" * 64)
    reinjection.schedule(first.proposal, brain_field)
    reinjection.schedule(second.proposal, brain_field)

    result = reality.process_external(
        pulse("external", 105.0, "unit:0", magnitude=0.8),
        brain_field,
    )
    assert result.matched_proposal_id in {
        first.proposal.proposal_id,
        second.proposal.proposal_id,
    }
    assert ledger.committed_positive_updates == 1
    assert ledger.external_observation_count == 1
    assert result.cancelled_arrivals == 2


def test_external_target_is_validated_before_any_mutation() -> None:
    ledger, transition, reinjection, reality = trained_stack()
    brain_field = field()
    row = prepare(transition)
    reinjection.schedule(row.proposal, brain_field)
    field_before = brain_field.state_hash()
    ledger_before = ledger.state_hash()
    transition_before = transition.state_hash()

    with pytest.raises(KeyError, match="unknown external target"):
        reality.process_external(
            pulse("bad-target", 104.0, "unit:99"),
            brain_field,
        )
    assert brain_field.state_hash() == field_before
    assert ledger.state_hash() == ledger_before
    assert transition.state_hash() == transition_before


def test_reality_state_remains_assembly_free() -> None:
    ledger, _, _, reality = trained_stack()
    state = reality.state_dict()
    assert "assembly_id" not in str(state).lower()
    assert "motif_id" not in str(state).lower()
    assert reality.state_hash() == reality.state_hash()
    assert ledger.external_observation_count == 0
