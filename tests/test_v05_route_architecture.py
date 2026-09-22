from __future__ import annotations

import copy

from sparkbrain.v04.contracts import SynapticArrival
from sparkbrain.v04.field import TemporalExcitableField
from sparkbrain.v04.topology import Connection, UnitState, explicit_topology
from sparkbrain.v05.brain import IntegratedV05Brain
from sparkbrain.v05.route_architecture import (
    QUIESCENCE_CAP_MS,
    RouteArchitectureUnreachable,
    apply_edge_intervention,
    clone_at_quiescent_anchor,
    freeze_response_signature,
    match_non_target_controls,
    opportunity_arc,
    select_candidate_edges,
)


def _field() -> TemporalExcitableField:
    units = tuple(UnitState(unit_id=i, x=float(i), y=0.0) for i in range(7))
    edges = (
        Connection(3, 2, -0.40, 3.0),
        Connection(2, 3, 0.20, 2.0),
        Connection(1, 2, 0.90, 1.0),
        Connection(4, 2, 0.80, 1.5),
        Connection(1, 4, 0.88, 1.1),
        Connection(4, 5, 0.22, 2.2),
        Connection(5, 6, -0.39, 3.1),
        Connection(6, 5, 0.78, 1.6),
        Connection(5, 1, 0.19, 2.1),
    )
    topology = explicit_topology(units, edges, receptor_ids=(0,))
    return TemporalExcitableField(topology)


def test_candidate_edge_family_is_bounded_and_deterministic() -> None:
    field = _field()
    rows = select_candidate_edges(field, (2, 3))
    assert [row.key for row in rows] == [(3, 2), (2, 3), (1, 2), (4, 2)]
    assert [row.internal for row in rows] == [True, True, False, False]


def test_matched_controls_are_non_target_unique_and_checkpoint_only() -> None:
    field = _field()
    targets = select_candidate_edges(field, (2, 3))
    pairs = match_non_target_controls(field, (2, 3), targets)
    controls = [pair.control for pair in pairs]
    assert len({row.key for row in controls}) == len(targets)
    assert all(2 not in row.key and 3 not in row.key for row in controls)
    assert pairs == match_non_target_controls(field, (2, 3), targets)


def test_matched_controls_fail_closed_when_pool_is_exhausted() -> None:
    field = _field()
    targets = select_candidate_edges(field, (2, 3))
    for key in [(4, 5), (5, 6), (6, 5), (5, 1)]:
        del field.connections[key]
    try:
        match_non_target_controls(field, (2, 3), targets)
    except RouteArchitectureUnreachable:
        pass
    else:
        raise AssertionError("control-pool exhaustion must fail closed")


def test_interventions_modify_only_selected_clone_edge() -> None:
    field = _field()
    target = select_candidate_edges(field, (2, 3))[0]

    null_field = copy.deepcopy(field)
    null_row = apply_edge_intervention(null_field, target, "transmission_null")
    assert null_row.weight == 0.0
    assert field.connection(*target.key).weight == target.weight

    delay_field = copy.deepcopy(field)
    delay_row = apply_edge_intervention(delay_field, target, "delay_plus_1ms")
    assert delay_row.delay_ms == target.delay_ms + 1.0
    assert field.connection(*target.key).delay_ms == target.delay_ms

    sham_field = copy.deepcopy(field)
    sham_row = apply_edge_intervention(sham_field, target, "sham")
    assert sham_row.weight == target.weight
    assert sham_row.delay_ms == target.delay_ms


def test_time_unrolled_opportunity_arc_uses_exact_delay() -> None:
    target = select_candidate_edges(_field(), (2, 3))[0]
    arc = opportunity_arc(target, 7.25)
    assert arc.source_id == target.source_id
    assert arc.target_id == target.target_id
    assert arc.source_time_ms == 7.25
    assert arc.target_time_ms == 7.25 + target.delay_ms


def test_quiescent_anchor_uses_clone_and_fixed_boundary() -> None:
    brain = IntegratedV05Brain()
    target_id = next(
        unit_id
        for unit_id in brain.base.field.units
        if unit_id not in brain.base.field.receptor_ids
    )
    brain.base.field.schedule_arrival(
        SynapticArrival(
            time_ms=brain.current_time_ms + 16.0,
            target_id=target_id,
            current=0.01,
            source_id=None,
            pulse_id="architecture-test",
        )
    )
    source_hash = brain.base.field.state_hash()
    clone, report = clone_at_quiescent_anchor(brain)
    assert report.quiescent is True
    assert report.steps == 1
    assert report.pending_counts[-1] == 0
    assert clone.current_time_ms == brain.current_time_ms + 32.0
    assert brain.base.field.state_hash() == source_hash


def test_quiescent_anchor_does_not_extend_256ms_cap() -> None:
    brain = IntegratedV05Brain()
    target_id = next(iter(brain.base.field.units))
    brain.base.field.schedule_arrival(
        SynapticArrival(
            time_ms=brain.current_time_ms + QUIESCENCE_CAP_MS + 1.0,
            target_id=target_id,
            current=0.01,
            source_id=None,
            pulse_id="beyond-cap",
        )
    )
    _, report = clone_at_quiescent_anchor(brain)
    assert report.quiescent is False
    assert report.steps == 8
    assert report.end_time_ms - report.start_time_ms == QUIESCENCE_CAP_MS
    assert report.pending_counts[-1] == 1


def test_response_signature_is_order_independent_and_value_sensitive() -> None:
    left = freeze_response_signature({"similarity": 0.75, "coverage": 0.5})
    reordered = freeze_response_signature({"coverage": 0.5, "similarity": 0.75})
    changed = freeze_response_signature({"coverage": 0.5, "similarity": 0.76})
    assert left == reordered
    assert left.sha256 != changed.sha256
