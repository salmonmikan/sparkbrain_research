from __future__ import annotations

from dataclasses import asdict

import pytest

from sparkbrain.v04.contracts import SynapticArrival
from sparkbrain.v05.brain import IntegratedV05Brain
from sparkbrain.v05.subthreshold_architecture import (
    SubthresholdArchitectureUnreachable,
    clone_at_queue_free_anchor,
    clone_with_subthreshold_reset,
    enforce_queue_cap,
    freeze_subthreshold_signature,
    snapshot_subthreshold_units,
)


def _internal_unit_ids(brain: IntegratedV05Brain, count: int = 2) -> tuple[int, ...]:
    receptor_ids = set(brain.base.field.receptor_ids)
    return tuple(
        unit_id
        for unit_id in sorted(brain.base.field.units)
        if unit_id not in receptor_ids
    )[:count]


def test_queue_free_anchor_is_exact_clone_without_source_mutation() -> None:
    brain = IntegratedV05Brain()
    source_hash = brain.state_hash()

    clone, anchor = clone_at_queue_free_anchor(brain)

    assert anchor.pending_arrivals == 0
    assert anchor.source_state_hash == source_hash
    assert anchor.clone_state_hash == source_hash
    assert clone.state_hash() == source_hash
    assert brain.state_hash() == source_hash


def test_queue_cap_fails_closed_without_advancing_pending_work() -> None:
    brain = IntegratedV05Brain()
    target_id = _internal_unit_ids(brain, count=1)[0]
    brain.base.field.schedule_arrival(
        SynapticArrival(
            time_ms=brain.current_time_ms + 1.0,
            target_id=target_id,
            current=0.01,
            source_id=None,
            pulse_id="cand35-synthetic-queue-cap",
        )
    )
    source_hash = brain.state_hash()

    with pytest.raises(SubthresholdArchitectureUnreachable):
        enforce_queue_cap(brain, max_pending_arrivals=0)

    assert brain.state_hash() == source_hash


def test_subthreshold_reset_changes_only_potential_and_adaptation_on_clone() -> None:
    brain = IntegratedV05Brain()
    unit_id = _internal_unit_ids(brain, count=1)[0]
    source_unit = brain.base.field.units[unit_id]
    source_unit.potential = 0.37
    source_unit.adaptation = 0.19
    source_hash = brain.state_hash()
    before = asdict(source_unit)

    clone = clone_with_subthreshold_reset(brain, [unit_id])
    after = asdict(clone.base.field.units[unit_id])

    assert brain.state_hash() == source_hash
    assert source_unit.potential == 0.37
    assert source_unit.adaptation == 0.19
    changed = {key for key in before if before[key] != after[key]}
    assert changed == {"potential", "adaptation"}
    assert after["potential"] == 0.0
    assert after["adaptation"] == 0.0


def test_snapshot_and_signature_are_order_deterministic_and_state_sensitive() -> None:
    brain = IntegratedV05Brain()
    first, second = _internal_unit_ids(brain)
    brain.base.field.units[first].potential = 0.25
    brain.base.field.units[first].adaptation = 0.10
    brain.base.field.units[second].potential = -0.05

    rows = snapshot_subthreshold_units(brain, [second, first])
    left = freeze_subthreshold_signature(brain, [second, first])
    reordered = freeze_subthreshold_signature(brain, [first, second])

    assert [row.unit_id for row in rows] == sorted((first, second))
    assert left == reordered

    brain.base.field.units[first].potential = 0.26
    changed = freeze_subthreshold_signature(brain, [first, second])
    assert changed.sha256 != left.sha256


def test_signature_explicitly_forbids_result_bearing_layers() -> None:
    brain = IntegratedV05Brain()
    unit_id = _internal_unit_ids(brain, count=1)[0]

    signature = freeze_subthreshold_signature(brain, [unit_id])

    assert '"candidate_response_execution_allowed":false' in signature.payload_json
    assert '"preformal_execution_allowed":false' in signature.payload_json
    assert '"formal_action_allowed":false' in signature.payload_json
