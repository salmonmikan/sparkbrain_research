from __future__ import annotations

import sparkbrain.research.rv02_rd005_construction_artifact as artifact_module
from sparkbrain.research.rv02_rd005_construction_artifact import (
    InspectedClock,
    SeedCollisionRecord,
)
from sparkbrain.research.rv02_scale import digest


def _collision() -> SeedCollisionRecord:
    return SeedCollisionRecord(
        seed=92505,
        searched_seed_ids=(92001, 141500, 141600),
        searched_world_ids=("rv02-development:92001:disjoint-routes",),
    )


def test_rd005_failure_retains_partial_construction_evidence_without_retry(monkeypatch) -> None:
    calls = 0
    schedule = (
        {"ordinal": 0, "event_id": "rd005-plan-000000", "time_ms": 1.0, "unit_id": 3},
    )
    connection_rows = (
        {
            "source_id": 40,
            "target_id": 3,
            "weight": 0.05,
            "delay_ms": 1.0,
            "plastic": True,
        },
    )
    inspected = InspectedClock(
        time_ms=1.0,
        spikes=({"time_ms": 1.0, "unit_id": 40},),
    )

    def fail_after_partial_observation(config, world, scale, *, trace):
        nonlocal calls
        calls += 1
        trace.topology_sha256 = "c" * 64
        trace.ordinary_schedule = schedule
        trace.connection_rows = connection_rows
        trace.inspected_clocks.append(inspected)
        raise RuntimeError("synthetic post-observation failure")

    monkeypatch.setattr(
        artifact_module,
        "_construct_cell",
        fail_after_partial_observation,
    )
    artifact = artifact_module.build_rd005_construction_artifact(
        source_git_sha="f" * 40,
        collision_search=_collision(),
    )

    assert calls == 18
    assert artifact.matrix_status == "CONSTRUCTION_INTEGRITY_FAILURE"
    for cell in artifact.cells:
        assert cell.status == "CONSTRUCTION_INTEGRITY_FAILURE"
        assert cell.topology_sha256 == "c" * 64
        assert cell.ordinary_schedule == schedule
        assert cell.ordinary_schedule_sha256 == digest(schedule)
        assert cell.connection_rows == connection_rows
        assert cell.connection_rows_sha256 == digest(connection_rows)
        assert cell.inspected_clocks == (inspected,)
        assert cell.error == "RuntimeError: synthetic post-observation failure"
