from __future__ import annotations

import hashlib
import json
from dataclasses import replace

import pytest

from sparkbrain.research.rv02_rd005_artifact_verifier import (
    verify_rd005_artifact_for_future_capability,
    verify_rd005_construction_cell,
)
from sparkbrain.research.rv02_rd005_construction_artifact import (
    RD005_FRESH_SEED,
    InspectedClock,
    RD005ConstructionArtifact,
    RD005ConstructionCell,
    SeedCollisionRecord,
)
from sparkbrain.research.rv02_rd005_gate_construction import (
    ConnectionSnapshot,
    EligibilityEvent,
    ExternalReturnEvent,
    RD005GateConstruction,
)
from sparkbrain.research.rv02_scale import ScaleStudyConfig, development_worlds, digest
from sparkbrain.v04.contracts import SpikeEvent


def _canonical_sha256(value: object) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _spike(unit_id: int) -> dict[str, object]:
    return SpikeEvent(
        time_ms=10.0,
        unit_id=unit_id,
        potential_before_reset=1.0,
        dynamic_threshold=0.5,
        x=float(unit_id),
        y=0.0,
        source_pulse_ids=(f"source-{unit_id}",),
        novelty=0.0,
        prediction_error=0.0,
        excitatory_drive=1.0,
        inhibitory_drive=0.0,
    ).as_dict()


def _ready_cell(
    *,
    family: str = "test",
    scale: int = 4,
    world_id: str = "world:test",
    world_sha256: str = "a" * 64,
    evidence_sha256: str = "b" * 64,
) -> RD005ConstructionCell:
    schedule = (
        {
            "event_id": "rd005-plan-000000",
            "ordinal": 0,
            "time_ms": 10.0,
            "unit_id": 0,
        },
    )
    connection_rows = (
        {
            "source_id": 40,
            "target_id": 2,
            "weight": 0.10,
            "delay_ms": 1.0,
            "plastic": True,
        },
        {
            "source_id": 41,
            "target_id": 4,
            "weight": 0.20,
            "delay_ms": 1.0,
            "plastic": True,
        },
        {
            "source_id": 41,
            "target_id": 2,
            "weight": 0.30,
            "delay_ms": 1.0,
            "plastic": True,
        },
        {
            "source_id": 40,
            "target_id": 4,
            "weight": 0.40,
            "delay_ms": 1.0,
            "plastic": True,
        },
    )
    spikes = (_spike(40), _spike(41))
    eligibility = tuple(
        EligibilityEvent(
            event_id=(
                f"rd005-eligibility:{family}:{scale}:{ordinal}:"
                f"{_canonical_sha256(spike)[:16]}"
            ),
            observed_source_id=int(spike["unit_id"]),
            time_ms=float(spike["time_ms"]),
        )
        for ordinal, spike in enumerate(spikes)
    )
    # The registered constructor chooses the minimum visible target for each
    # source. Both sources expose target 2 in this symmetric gate fixture.
    returns = tuple(
        ExternalReturnEvent(
            event_id=(
                f"rd005-return:{family}:{scale}:{ordinal}:"
                f"{_canonical_sha256(spike)[:16]}"
            ),
            eligibility_event_id=eligibility[ordinal].event_id,
            target_id=2,
            time_ms=11.0,
            outcome_blind=True,
        )
        for ordinal, spike in enumerate(spikes)
    )
    mapping = {40: 41, 41: 40}
    connections = tuple(
        ConnectionSnapshot(
            source_id=int(row["source_id"]),
            target_id=int(row["target_id"]),
            plastic=bool(row["plastic"]),
            initial_weight=float(row["weight"]),
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
        cell_id=f"{world_id}|scale={scale}",
        family=family,
        scale=scale,
        world_id=world_id,
        world_sha256=world_sha256,
        evidence_sha256=evidence_sha256,
        topology_sha256="c" * 64,
        ordinary_schedule=schedule,
        ordinary_schedule_sha256=digest(schedule),
        connection_rows=connection_rows,
        connection_rows_sha256=digest(connection_rows),
        inspected_clocks=(InspectedClock(time_ms=10.0, spikes=spikes),),
        selected_clock_ms=10.0,
        eligibility_events=eligibility,
        return_events=returns,
        es_assignment=tuple(sorted(mapping.items())),
        e1_certificates=gate.certificates("E1"),
        es_certificates=gate.certificates("ES"),
        status="D1_READY",
    )


def _fixed_artifact() -> RD005ConstructionArtifact:
    config = ScaleStudyConfig(seed=RD005_FRESH_SEED)
    cells = tuple(
        _ready_cell(
            family=str(world["family"]),
            scale=int(scale),
            world_id=str(world["world_id"]),
            world_sha256=digest(world),
            evidence_sha256=str(world["evidence_hash"]),
        )
        for world in development_worlds(config)
        for scale in config.scales
    )
    return RD005ConstructionArtifact(
        source_git_sha="a" * 40,
        collision_search=SeedCollisionRecord(
            seed=RD005_FRESH_SEED,
            searched_seed_ids=(92504,),
            searched_world_ids=("prior:92504:world",),
        ),
        cells=cells,
    )


def test_verifier_accepts_reconstructable_ready_cell() -> None:
    verify_rd005_construction_cell(_ready_cell())


def test_verifier_rejects_ready_cell_without_gate_certificates() -> None:
    malformed = replace(_ready_cell(), e1_certificates=(), es_certificates=())
    with pytest.raises(ValueError, match="retained E1/ES certificates"):
        verify_rd005_construction_cell(malformed)


def test_verifier_rejects_ready_cell_with_fabricated_eligibility() -> None:
    cell = _ready_cell()
    fabricated = replace(
        cell,
        eligibility_events=(
            replace(cell.eligibility_events[0], observed_source_id=99),
            cell.eligibility_events[1],
        ),
    )
    with pytest.raises(ValueError, match="do not reconstruct from retained spikes"):
        verify_rd005_construction_cell(fabricated)


def test_verifier_rejects_ready_cell_relabelled_unreachable() -> None:
    ready = _ready_cell()
    relabelled = replace(
        ready,
        status="D1_UNREACHABLE",
        selected_clock_ms=None,
        eligibility_events=(),
        return_events=(),
        es_assignment=(),
        e1_certificates=(),
        es_certificates=(),
    )
    with pytest.raises(ValueError, match="status does not match"):
        verify_rd005_construction_cell(relabelled)


def test_verifier_accepts_exact_preregistered_matrix_identity() -> None:
    ready = verify_rd005_artifact_for_future_capability(_fixed_artifact())
    assert len(ready) == 18


def test_verifier_rejects_substituted_preregistered_matrix_cell() -> None:
    artifact = _fixed_artifact()
    cells = list(artifact.cells)
    cells[0] = replace(cells[0], cell_id="substituted|scale=1")
    malformed = replace(artifact, cells=tuple(cells))
    with pytest.raises(ValueError, match="exact preregistered 18-cell matrix"):
        verify_rd005_artifact_for_future_capability(malformed)
