from __future__ import annotations

from dataclasses import replace

import pytest

from sparkbrain.research.rv02_rd005_artifact_verifier import (
    verify_rd005_construction_cell,
)
from sparkbrain.research.rv02_rd005_construction_artifact import (
    InspectedClock,
    RD005ConstructionCell,
)
from sparkbrain.research.rv02_rd005_gate_construction import (
    ConnectionSnapshot,
    EligibilityEvent,
    ExternalReturnEvent,
    RD005GateConstruction,
)
from sparkbrain.research.rv02_scale import digest


def _ready_cell() -> RD005ConstructionCell:
    schedule = (
        {"event_id": "rd005-plan-000000", "ordinal": 0, "time_ms": 10.0, "unit_id": 0},
    )
    connection_rows = (
        {"source_id": 1, "target_id": 2, "weight": 0.10, "delay_ms": 1.0, "plastic": True},
        {"source_id": 3, "target_id": 4, "weight": 0.20, "delay_ms": 1.0, "plastic": True},
        {"source_id": 3, "target_id": 2, "weight": 0.30, "delay_ms": 1.0, "plastic": True},
        {"source_id": 1, "target_id": 4, "weight": 0.40, "delay_ms": 1.0, "plastic": True},
    )
    eligibility = (
        EligibilityEvent("elig-1", 1, 9.0),
        EligibilityEvent("elig-3", 3, 9.0),
    )
    returns = (
        ExternalReturnEvent("return-1", "elig-1", 2, 10.0, True),
        ExternalReturnEvent("return-3", "elig-3", 4, 10.0, True),
    )
    mapping = {1: 3, 3: 1}
    connections = tuple(
        ConnectionSnapshot(
            source_id=row["source_id"],
            target_id=row["target_id"],
            plastic=row["plastic"],
            initial_weight=row["weight"],
        )
        for row in connection_rows
    )
    gate = RD005GateConstruction(
        eligibility_events=eligibility,
        return_events=returns,
        connections=connections,
        shuffled_assignment=mapping,
    )
    gate.assert_development_matrix_reachable()
    return RD005ConstructionCell(
        cell_id="world:test|scale=4",
        family="test",
        scale=4,
        world_id="world:test",
        world_sha256="a" * 64,
        evidence_sha256="b" * 64,
        topology_sha256="c" * 64,
        ordinary_schedule=schedule,
        ordinary_schedule_sha256=digest(schedule),
        connection_rows=connection_rows,
        connection_rows_sha256=digest(connection_rows),
        inspected_clocks=(InspectedClock(time_ms=10.0, spikes=()),),
        selected_clock_ms=10.0,
        eligibility_events=eligibility,
        return_events=returns,
        es_assignment=tuple(sorted(mapping.items())),
        e1_certificates=gate.certificates("E1"),
        es_certificates=gate.certificates("ES"),
        status="D1_READY",
    )


def test_verifier_accepts_reconstructable_ready_cell() -> None:
    verify_rd005_construction_cell(_ready_cell())


def test_verifier_rejects_ready_cell_without_gate_certificates() -> None:
    malformed = replace(_ready_cell(), e1_certificates=(), es_certificates=())
    with pytest.raises(ValueError, match="retained E1/ES certificates"):
        verify_rd005_construction_cell(malformed)


def test_verifier_rejects_ready_cell_with_tampered_certificate() -> None:
    cell = _ready_cell()
    tampered = replace(
        cell,
        e1_certificates=(replace(cell.e1_certificates[0], assigned_source_id=999),)
        + cell.e1_certificates[1:],
    )
    with pytest.raises(ValueError, match="do not reconstruct"):
        verify_rd005_construction_cell(tampered)


def test_verifier_rejects_selected_clock_not_retained_in_trace() -> None:
    malformed = replace(_ready_cell(), selected_clock_ms=11.0)
    with pytest.raises(ValueError, match="not retained"):
        verify_rd005_construction_cell(malformed)


def test_verifier_rejects_unreachable_cell_with_ready_only_evidence() -> None:
    ready = _ready_cell()
    malformed = replace(ready, status="D1_UNREACHABLE", selected_clock_ms=None)
    with pytest.raises(ValueError, match="ready-only gate evidence"):
        verify_rd005_construction_cell(malformed)
