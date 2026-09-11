"""Execution-disabled restore adapter for the prospective A01 MD-002 P2 fixture.

This module reconstructs actual A01 local, Field, consistency and live return-address
state from the byte-bound P2 arm input.  It deliberately does not apply external
evidence, execute the world relation, or open the MD-002 capability gate.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from sparkbrain.v04.field import TemporalExcitableField
from sparkbrain.v06.boundary import BoundaryDirection, BoundaryEvent
from sparkbrain.v06.consistency import UntypedBoundaryConsistency
from sparkbrain.v06.foundation import (
    EndogenousPulseProposal,
    EventOrigin,
    ProvenanceLedger,
    RuntimePulse,
    validate_runtime_mapping,
)

from .credit_bridge import A01LocalTemporalExpectation
from .md002_fixtures import P2WorldArmInput
from .md002_state_binding import LiveReturnAddressState, canonical_bytes


@dataclass(slots=True)
class RestoredA01P2Arm:
    """One reconstructed pre-evidence arm; no capability has been executed."""

    arm: str
    expectation: A01LocalTemporalExpectation
    field: TemporalExcitableField
    ledger: ProvenanceLedger
    consistency: UntypedBoundaryConsistency
    boundary: BoundaryEvent | None
    world_relation: dict[str, Any]
    admissible_external_evidence: tuple[RuntimePulse, ...]


def _mapping_from_bytes(value: bytes, name: str) -> dict[str, Any]:
    try:
        row = json.loads(value)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"{name} is not canonical JSON") from exc
    if not isinstance(row, dict):
        raise ValueError(f"{name} must decode to a mapping")
    validate_runtime_mapping(row, path=f"v061_a01.md002.restore.{name}")
    return row


def _proposal_from_state(value: dict[str, Any]) -> EndogenousPulseProposal:
    return EndogenousPulseProposal(
        proposal_id=str(value["proposal_id"]),
        created_at_ms=float(value["created_at_ms"]),
        target=str(value["target"]),
        predicted_arrival_ms=float(value["predicted_arrival_ms"]),
        magnitude=float(value["magnitude"]),
        polarity=int(value["polarity"]),
        confidence=float(value["confidence"]),
        origin_state_hash=str(value["origin_state_hash"]),
        parent_proposal_ids=tuple(map(str, value.get("parent_proposal_ids", ()))),
        local_path_ids=tuple(map(str, value.get("local_path_ids", ()))),
        generation_depth=int(value["generation_depth"]),
        valid_until_ms=float(value["valid_until_ms"]),
        energy_cost=float(value["energy_cost"]),
    )


def _boundary_from_state(value: dict[str, Any]) -> BoundaryEvent:
    return BoundaryEvent(
        event_id=str(value["event_id"]),
        time_ms=float(value["time_ms"]),
        port_id=str(value["port_id"]),
        magnitude=float(value["magnitude"]),
        polarity=int(value["polarity"]),
        direction=BoundaryDirection(value["direction"]),
        source_spark_id=str(value["source_spark_id"]),
        source_unit_id=int(value["source_unit_id"]),
        source_proposal_ids=tuple(map(str, value.get("source_proposal_ids", ()))),
        generation_depth=int(value["generation_depth"]),
        source_state_hash=str(value["source_state_hash"]),
    )


def _pulse_from_state(value: dict[str, Any]) -> RuntimePulse:
    return RuntimePulse(
        event_id=str(value["event_id"]),
        time_ms=float(value["time_ms"]),
        target=str(value["target"]),
        magnitude=float(value["magnitude"]),
        polarity=int(value["polarity"]),
        origin=EventOrigin(value["origin"]),
        generation_depth=int(value.get("generation_depth", 0)),
        parent_event_ids=tuple(map(str, value.get("parent_event_ids", ()))),
        source_path_ids=tuple(map(str, value.get("source_path_ids", ()))),
        metadata=dict(value.get("metadata", {})),
    )


def _register_closed_proposals(
    ledger: ProvenanceLedger,
    rows: list[dict[str, Any]],
) -> tuple[EndogenousPulseProposal, ...]:
    pending = {
        str(row["proposal_id"]): _proposal_from_state(dict(row))
        for row in rows
    }
    if len(pending) != len(rows):
        raise ValueError("restored return-address proposal IDs must be unique")
    ordered: list[EndogenousPulseProposal] = []
    while pending:
        ready = sorted(
            proposal_id
            for proposal_id, proposal in pending.items()
            if set(proposal.parent_proposal_ids).issubset(ledger.proposals)
        )
        if not ready:
            raise ValueError("return-address proposal ancestry is cyclic or incomplete")
        for proposal_id in ready:
            proposal = pending.pop(proposal_id)
            ledger.register_proposal(proposal)
            ordered.append(proposal)
    return tuple(ordered)


def restore_a01_p2_arm(arm_input: P2WorldArmInput) -> RestoredA01P2Arm:
    """Restore one arm and prove byte-identical L/F/C/R round-trip identity."""

    arm_input.validate()
    local_state = _mapping_from_bytes(arm_input.partitions.local, "local")
    field_state = _mapping_from_bytes(arm_input.partitions.field, "field")
    consistency_state = _mapping_from_bytes(
        arm_input.partitions.consistency,
        "consistency",
    )

    expectation = A01LocalTemporalExpectation.from_learned_state_dict(local_state)
    field = TemporalExcitableField.from_state_dict(field_state)
    ledger = ProvenanceLedger()
    consistency = UntypedBoundaryConsistency.from_learned_state_dict(
        consistency_state,
        ledger=ledger,
    )

    boundary: BoundaryEvent | None = None
    restored_proposals: tuple[EndogenousPulseProposal, ...] = ()
    return_bytes = arm_input.partitions.return_address
    if return_bytes is not None:
        return_state = _mapping_from_bytes(return_bytes, "return_address")
        proposal_rows = return_state.get("proposals")
        boundary_row = return_state.get("boundary")
        if not isinstance(proposal_rows, list) or not isinstance(boundary_row, dict):
            raise ValueError("return-address state requires proposals and boundary")
        restored_proposals = _register_closed_proposals(
            ledger,
            [dict(row) for row in proposal_rows],
        )
        boundary = _boundary_from_state(dict(boundary_row))
        unknown = set(boundary.source_proposal_ids) - set(ledger.proposals)
        if unknown:
            raise ValueError(f"restored boundary references unknown proposals: {sorted(unknown)}")
        consistency.register_boundary(boundary)

    world_relation = _mapping_from_bytes(arm_input.world_relation, "world_relation")
    try:
        evidence_rows = json.loads(arm_input.admissible_external_evidence)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("admissible external evidence is not canonical JSON") from exc
    if not isinstance(evidence_rows, list) or not evidence_rows:
        raise ValueError("admissible external evidence must decode to a non-empty list")
    evidence = tuple(_pulse_from_state(dict(row)) for row in evidence_rows)
    if any(row.origin is not EventOrigin.EXTERNAL for row in evidence):
        raise ValueError("restored P2 evidence contains a non-external event")
    if any(
        right.time_ms <= left.time_ms
        for left, right in zip(evidence, evidence[1:], strict=False)
    ):
        raise ValueError("restored P2 evidence is not strictly time ordered")

    if canonical_bytes(expectation.learned_state_dict()) != arm_input.partitions.local:
        raise ValueError("restored local state does not round-trip to frozen bytes")
    if canonical_bytes(field.state_dict()) != arm_input.partitions.field:
        raise ValueError("restored Field state does not round-trip to frozen bytes")
    if canonical_bytes(consistency.learned_state_dict()) != arm_input.partitions.consistency:
        raise ValueError("restored consistency state does not round-trip to frozen bytes")
    if return_bytes is not None:
        assert boundary is not None
        rebuilt_return = LiveReturnAddressState(restored_proposals, boundary).state_dict()
        if canonical_bytes(rebuilt_return) != return_bytes:
            raise ValueError("restored return-address state does not round-trip to frozen bytes")
    if canonical_bytes(world_relation) != arm_input.world_relation:
        raise ValueError("restored world relation does not round-trip to frozen bytes")
    if canonical_bytes([row.as_dict() for row in evidence]) != arm_input.admissible_external_evidence:
        raise ValueError("restored external evidence does not round-trip to frozen bytes")

    return RestoredA01P2Arm(
        arm=arm_input.arm,
        expectation=expectation,
        field=field,
        ledger=ledger,
        consistency=consistency,
        boundary=boundary,
        world_relation=world_relation,
        admissible_external_evidence=evidence,
    )


__all__ = ["RestoredA01P2Arm", "restore_a01_p2_arm"]
