from __future__ import annotations

import json

import pytest

from sparkbrain.research.rv02_rd005_construction_artifact import (
    RD005ConstructionArtifact,
    RD005ConstructionCell,
    SeedCollisionRecord,
    _rotation,
    _selected_batch,
)
from sparkbrain.research.rv02_rd005_gate_construction import ConnectionSnapshot
from sparkbrain.v04.contracts import SpikeEvent


def _spike(time_ms: float, unit_id: int, pulse_id: str) -> SpikeEvent:
    return SpikeEvent(
        time_ms=time_ms,
        unit_id=unit_id,
        potential_before_reset=1.0,
        dynamic_threshold=0.5,
        x=float(unit_id),
        y=0.0,
        source_pulse_ids=(pulse_id,),
        novelty=0.0,
        prediction_error=0.0,
        excitatory_drive=1.0,
        inhibitory_drive=0.0,
    )


def _cell(index: int, status: str = "D1_READY") -> RD005ConstructionCell:
    return RD005ConstructionCell(
        cell_id=f"cell-{index:02d}",
        family=f"family-{index // 3}",
        scale=(1, 3, 10)[index % 3],
        world_id=f"world-{index // 3}",
        world_sha256="a" * 64,
        evidence_sha256="b" * 64,
        topology_sha256="c" * 64,
        ordinary_schedule_sha256="d" * 64,
        connection_rows_sha256="e" * 64,
        inspected_clocks=(),
        selected_clock_ms=1.0 if status == "D1_READY" else None,
        eligibility_events=(),
        return_events=(),
        es_assignment=(),
        e1_certificates=(),
        es_certificates=(),
        status=status,  # type: ignore[arg-type]
    )


def _collision() -> SeedCollisionRecord:
    return SeedCollisionRecord(
        seed=92505,
        searched_seed_ids=(92001, 141500, 141600),
        searched_world_ids=("rv02-development:92001:disjoint-routes",),
    )


def test_rd005_selects_latest_eligible_spike_and_smallest_visible_target() -> None:
    connections = (
        ConnectionSnapshot(40, 7, True, 0.05),
        ConnectionSnapshot(40, 3, True, 0.05),
        ConnectionSnapshot(41, 5, True, 0.05),
    )
    selected = _selected_batch(
        spikes=(
            _spike(3.5, 40, "lag-max"),
            _spike(9.5, 40, "lag-min"),
            _spike(8.0, 41, "second-source"),
        ),
        return_time_ms=10.0,
        connections=connections,
    )

    assert tuple((spike.unit_id, spike.time_ms, target) for spike, target in selected) == (
        (40, 9.5, 3),
        (41, 8.0, 5),
    )


def test_rd005_requires_two_sources_and_rotation_is_non_identity() -> None:
    connections = (ConnectionSnapshot(40, 3, True, 0.05),)
    selected = _selected_batch(
        spikes=(_spike(9.0, 40, "only-source"),),
        return_time_ms=10.0,
        connections=connections,
    )
    assert selected == ()
    assert _rotation((40, 41, 42)) == {40: 41, 41: 42, 42: 40}


def test_rd005_collision_record_fails_closed() -> None:
    _collision().validate()
    with pytest.raises(ValueError, match="collides with a prior registered seed"):
        SeedCollisionRecord(
            seed=92505,
            searched_seed_ids=(92001, 92505),
            searched_world_ids=("rv02-development:92001:shared-cue",),
        ).validate()


def test_rd005_artifact_derives_ready_cells_without_task_outputs() -> None:
    cells = tuple(
        _cell(index, "D1_UNREACHABLE" if index in (2, 7) else "D1_READY")
        for index in range(18)
    )
    artifact = RD005ConstructionArtifact(
        source_git_sha="f" * 40,
        collision_search=_collision(),
        cells=cells,
    )

    assert artifact.matrix_status == "D1_CONSTRUCTION_READY"
    assert len(artifact.future_capability_cell_ids) == 16
    encoded = json.dumps(artifact.state_dict(), sort_keys=True)
    for forbidden in ('"score"', '"reward"', '"route_correct"'):
        assert forbidden not in encoded
    assert len(artifact.artifact_sha256) == 64


def test_rd005_integrity_failure_blocks_future_capability_cells() -> None:
    cells = tuple(
        _cell(index, "CONSTRUCTION_INTEGRITY_FAILURE" if index == 5 else "D1_READY")
        for index in range(18)
    )
    artifact = RD005ConstructionArtifact(
        source_git_sha="f" * 40,
        collision_search=_collision(),
        cells=cells,
    )

    assert artifact.matrix_status == "CONSTRUCTION_INTEGRITY_FAILURE"
    assert artifact.future_capability_cell_ids == ()
