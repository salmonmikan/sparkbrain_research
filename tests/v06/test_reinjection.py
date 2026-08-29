from __future__ import annotations

from dataclasses import replace

import pytest

from sparkbrain.v04.field import ExcitableFieldConfig, TemporalExcitableField
from sparkbrain.v04.topology import UnitState, explicit_topology
from sparkbrain.v06.foundation import EndogenousPulseProposal, EventOrigin, ProvenanceLedger
from sparkbrain.v06.reinjection import FieldReinjectionGate, ReinjectionConfig


def field(*, threshold: float = 1.0, refractory_ms: float = 3.0) -> TemporalExcitableField:
    topology = explicit_topology(
        [UnitState(unit_id=0, x=0.0, y=0.0, base_threshold=threshold)],
        [],
        receptor_ids=[0],
    )
    return TemporalExcitableField(
        topology,
        ExcitableFieldConfig(
            receptor_fanout=1,
            refractory_ms=refractory_ms,
            adaptation_increment=0.0,
        ),
    )


def proposal(
    ledger: ProvenanceLedger,
    proposal_id: str,
    *,
    time_ms: float = 5.0,
    target: str = "unit:0",
    magnitude: float = 0.8,
    confidence: float = 0.5,
    polarity: int = 1,
    origin_state_hash: str = "s" * 64,
    generation_depth: int = 1,
    energy_cost: float = 0.0,
) -> EndogenousPulseProposal:
    row = EndogenousPulseProposal(
        proposal_id=proposal_id,
        created_at_ms=max(0.0, time_ms - 2.0),
        target=target,
        predicted_arrival_ms=time_ms,
        magnitude=magnitude,
        polarity=polarity,
        confidence=confidence,
        origin_state_hash=origin_state_hash,
        local_path_ids=("local:unit:1->unit:0",),
        generation_depth=generation_depth,
        valid_until_ms=time_ms + 10.0,
        energy_cost=energy_cost,
    )
    ledger.register_proposal(row)
    return row


def test_reinjection_schedules_current_but_does_not_force_spike() -> None:
    ledger = ProvenanceLedger()
    brain_field = field(threshold=1.0)
    gate = FieldReinjectionGate(ledger)
    row = proposal(ledger, "p-1", magnitude=0.8, confidence=0.5)

    decision = gate.schedule(row, brain_field)
    assert decision.accepted is True
    assert decision.effective_current == pytest.approx(0.4)
    assert decision.field_state_hash_after != decision.field_state_hash_before

    spikes = brain_field.run_until(row.predicted_arrival_ms)
    assert spikes == ()
    assert brain_field.units[0].potential == pytest.approx(0.4)
    assert ledger.events["endo:p-1"].origin is EventOrigin.ENDOGENOUS_UNCONFIRMED
    assert ledger.external_observation_count == 0
    assert ledger.committed_positive_updates == 0


def test_reinjection_can_spike_only_through_the_field_threshold() -> None:
    ledger = ProvenanceLedger()
    brain_field = field(threshold=1.0)
    gate = FieldReinjectionGate(ledger)
    row = proposal(ledger, "p-1", magnitude=2.0, confidence=1.0)

    assert gate.schedule(row, brain_field).accepted is True
    spikes = brain_field.run_until(row.predicted_arrival_ms)
    assert len(spikes) == 1
    assert spikes[0].unit_id == 0
    assert "endo:p-1" in spikes[0].source_pulse_ids
    assert ledger.committed_positive_updates == 0


def test_refractory_rule_applies_to_reinjected_pulses() -> None:
    ledger = ProvenanceLedger()
    brain_field = field(threshold=0.5, refractory_ms=3.0)
    gate = FieldReinjectionGate(ledger)
    first = proposal(ledger, "p-1", time_ms=5.0, magnitude=1.0, confidence=1.0)
    second = proposal(ledger, "p-2", time_ms=6.0, magnitude=1.0, confidence=1.0)

    assert gate.schedule(first, brain_field).accepted is True
    assert gate.schedule(second, brain_field).accepted is True
    spikes = brain_field.run_until(6.0)
    assert len(spikes) == 1
    assert spikes[0].time_ms == 5.0


def test_low_confidence_is_rejected_without_field_mutation() -> None:
    ledger = ProvenanceLedger()
    brain_field = field()
    gate = FieldReinjectionGate(
        ledger,
        ReinjectionConfig(minimum_confidence=0.7),
    )
    row = proposal(ledger, "p-1", confidence=0.69)
    before = brain_field.state_hash()

    decision = gate.schedule(row, brain_field)
    assert decision.accepted is False
    assert decision.reason == "low_confidence"
    assert brain_field.state_hash() == before


def test_unregistered_or_modified_proposal_is_rejected() -> None:
    ledger = ProvenanceLedger()
    brain_field = field()
    gate = FieldReinjectionGate(ledger)
    row = EndogenousPulseProposal(
        proposal_id="p-1",
        created_at_ms=3.0,
        target="unit:0",
        predicted_arrival_ms=5.0,
        magnitude=0.8,
        polarity=1,
        confidence=0.8,
        origin_state_hash="s" * 64,
        valid_until_ms=10.0,
    )
    assert gate.schedule(row, brain_field).reason == "unregistered_proposal"

    ledger.register_proposal(row)
    modified = replace(row, magnitude=0.9)
    assert gate.schedule(modified, brain_field).reason == "proposal_content_mismatch"


def test_generation_depth_and_duplicate_schedule_are_bounded() -> None:
    ledger = ProvenanceLedger()
    brain_field = field()
    gate = FieldReinjectionGate(
        ledger,
        ReinjectionConfig(maximum_generation_depth=1),
    )
    deep = proposal(ledger, "deep", generation_depth=2, confidence=1.0)
    assert gate.schedule(deep, brain_field).reason == "generation_depth"

    normal = proposal(ledger, "normal", confidence=1.0)
    assert gate.schedule(normal, brain_field).accepted is True
    state_after_first = brain_field.state_hash()
    duplicate = gate.schedule(normal, brain_field)
    assert duplicate.reason == "already_scheduled"
    assert brain_field.state_hash() == state_after_first


def test_energy_budget_rejects_before_scheduling() -> None:
    ledger = ProvenanceLedger()
    brain_field = field()
    gate = FieldReinjectionGate(
        ledger,
        ReinjectionConfig(maximum_energy_per_window=0.5),
    )
    row = proposal(ledger, "p-1", magnitude=0.6, confidence=1.0)
    before = brain_field.state_hash()

    decision = gate.schedule(row, brain_field)
    assert decision.accepted is False
    assert decision.reason == "energy_budget"
    assert brain_field.state_hash() == before


def test_per_window_proposal_budget_is_fail_closed() -> None:
    ledger = ProvenanceLedger()
    brain_field = field()
    gate = FieldReinjectionGate(
        ledger,
        ReinjectionConfig(maximum_proposals_per_window=1),
    )
    first = proposal(
        ledger,
        "p-1",
        time_ms=5.0,
        confidence=1.0,
        origin_state_hash="a" * 64,
    )
    second = proposal(
        ledger,
        "p-2",
        time_ms=6.0,
        confidence=1.0,
        origin_state_hash="b" * 64,
    )
    assert gate.schedule(first, brain_field).accepted is True
    after_first = brain_field.state_hash()
    decision = gate.schedule(second, brain_field)
    assert decision.reason == "proposal_budget"
    assert brain_field.state_hash() == after_first


def test_branch_budget_is_per_origin_state() -> None:
    ledger = ProvenanceLedger()
    brain_field = field()
    gate = FieldReinjectionGate(
        ledger,
        ReinjectionConfig(maximum_branches_per_origin_state=1),
    )
    first = proposal(ledger, "p-1", time_ms=5.0, confidence=1.0)
    second = proposal(ledger, "p-2", time_ms=60.0, confidence=1.0)
    assert gate.schedule(first, brain_field).accepted is True
    after_first = brain_field.state_hash()
    decision = gate.schedule(second, brain_field)
    assert decision.reason == "branch_budget"
    assert brain_field.state_hash() == after_first


def test_unknown_target_fails_before_queue_mutation() -> None:
    ledger = ProvenanceLedger()
    brain_field = field()
    gate = FieldReinjectionGate(ledger)
    row = proposal(ledger, "p-1", target="unit:99", confidence=1.0)
    before = brain_field.state_hash()
    with pytest.raises(KeyError, match="unknown reinjection target"):
        gate.schedule(row, brain_field)
    assert brain_field.state_hash() == before


def test_gate_state_is_assembly_free_and_deterministic() -> None:
    ledger = ProvenanceLedger()
    brain_field = field()
    gate = FieldReinjectionGate(ledger)
    row = proposal(ledger, "p-1", confidence=1.0)
    gate.schedule(row, brain_field)
    state = gate.state_dict()
    assert "assembly_id" not in str(state).lower()
    assert "motif_id" not in str(state).lower()
    assert gate.state_hash() == gate.state_hash()
