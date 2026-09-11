from __future__ import annotations

import json

import pytest

import sparkbrain.research.rv02_rd005_construction_artifact as artifact_module
from sparkbrain.research.rv02_rd005_construction_artifact import (
    RD005ConstructionArtifact,
    RD005ConstructionCell,
    SeedCollisionRecord,
    _rd005_training_schedule,
    _rotation,
    _selected_batch,
)
from sparkbrain.research.rv02_rd005_gate_construction import ConnectionSnapshot
from sparkbrain.research.rv02_scale import digest
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
    schedule: tuple[dict[str, object], ...] = ()
    connection_rows: tuple[dict[str, object], ...] = ()
    is_failure = status == "CONSTRUCTION_INTEGRITY_FAILURE"
    return RD005ConstructionCell(
        cell_id=f"cell-{index:02d}",
        family=f"family-{index // 3}",
        scale=(1, 3, 10)[index % 3],
        world_id=f"world-{index // 3}",
        world_sha256="a" * 64,
        evidence_sha256="b" * 64,
        topology_sha256=None if is_failure else "c" * 64,
        ordinary_schedule=schedule,
        ordinary_schedule_sha256=None if is_failure else digest(schedule),
        connection_rows=connection_rows,
        connection_rows_sha256=None if is_failure else digest(connection_rows),
        inspected_clocks=(),
        selected_clock_ms=1.0 if status == "D1_READY" else None,
        eligibility_events=(),
        return_events=(),
        es_assignment=(),
        e1_certificates=(),
        es_certificates=(),
        status=status,  # type: ignore[arg-type]
        error="synthetic construction failure" if is_failure else None,
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


def test_rd005_rebinds_and_retains_exact_injected_schedule_ids(monkeypatch) -> None:
    monkeypatch.setattr(
        artifact_module,
        "_training_schedule",
        lambda world: (
            {"ordinal": 0, "event_id": "rd003-ext-000000", "time_ms": 1.0, "unit_id": 3},
            {"ordinal": 1, "event_id": "rd003-ext-000001", "time_ms": 2.0, "unit_id": 4},
        ),
    )

    schedule = _rd005_training_schedule({})
    assert tuple(row["event_id"] for row in schedule) == (
        "rd005-plan-000000",
        "rd005-plan-000001",
    )
    assert digest(schedule) == digest(tuple(dict(row) for row in schedule))


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


def test_rd005_serializes_connection_rows_not_only_their_hash() -> None:
    connection_rows = (
        {
            "source_id": 40,
            "target_id": 3,
            "weight": 0.05,
            "delay_ms": 1.0,
            "plastic": True,
        },
    )
    cell = _cell(0)
    cell = RD005ConstructionCell(
        **{
            **cell.__dict__,
            "connection_rows": connection_rows,
            "connection_rows_sha256": digest(connection_rows),
        }
    )
    state = cell.state_dict()
    assert state["connection_rows"] == list(connection_rows)
    assert state["connection_rows_sha256"] == digest(connection_rows)


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


def test_rd005_builder_records_setup_failures_without_retrying_them(monkeypatch) -> None:
    calls = 0

    def fail_construct(*args, **kwargs):
        nonlocal calls
        calls += 1
        raise RuntimeError("synthetic setup failure")

    monkeypatch.setattr(artifact_module, "_construct_cell", fail_construct)
    artifact = artifact_module.build_rd005_construction_artifact(
        source_git_sha="f" * 40,
        collision_search=_collision(),
    )

    assert calls == 18
    assert len(artifact.cells) == 18
    assert artifact.matrix_status == "CONSTRUCTION_INTEGRITY_FAILURE"
    assert all(row.status == "CONSTRUCTION_INTEGRITY_FAILURE" for row in artifact.cells)
    assert all(row.error == "RuntimeError: synthetic setup failure" for row in artifact.cells)
