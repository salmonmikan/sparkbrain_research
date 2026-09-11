"""Real-state serialization boundary for prospective A01 MD-002 P2.

This module contains no capability runner.  It serializes the actual A01 local
learner, Field state mapping, anonymous consistency learned state, optional live
return-address lineage, external world relation, and admissible external evidence
into the byte-bound P2 reset fixture added after MD-001.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from sparkbrain.v06.boundary import BoundaryEvent
from sparkbrain.v06.consistency import UntypedBoundaryConsistency
from sparkbrain.v06.foundation import (
    EndogenousPulseProposal,
    EventOrigin,
    RuntimePulse,
    validate_runtime_mapping,
)

from .credit_bridge import A01LocalTemporalExpectation
from .md002_fixtures import FrozenPartitionBytes, P2WorldOnlyFixture


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def canonical_state(value: object) -> dict[str, Any]:
    """Return the JSON-normalized object represented by canonical bytes."""

    normalized = json.loads(canonical_bytes(value))
    if not isinstance(normalized, dict):
        raise ValueError("canonical A01 partition state must be a mapping")
    return normalized


@dataclass(frozen=True, slots=True)
class LiveReturnAddressState:
    """Exact live proposal ancestry and BoundaryEvent retained at pairing time."""

    proposals: tuple[EndogenousPulseProposal, ...]
    boundary: BoundaryEvent

    def state_dict(self) -> dict[str, Any]:
        proposal_rows = []
        ids: set[str] = set()
        for proposal in self.proposals:
            if proposal.proposal_id in ids:
                raise ValueError("return-address proposal IDs must be unique")
            ids.add(proposal.proposal_id)
            proposal_rows.append(
                {
                    "proposal_id": proposal.proposal_id,
                    "created_at_ms": proposal.created_at_ms,
                    "target": proposal.target,
                    "predicted_arrival_ms": proposal.predicted_arrival_ms,
                    "magnitude": proposal.magnitude,
                    "polarity": proposal.polarity,
                    "confidence": proposal.confidence,
                    "origin_state_hash": proposal.origin_state_hash,
                    "parent_proposal_ids": list(proposal.parent_proposal_ids),
                    "local_path_ids": list(proposal.local_path_ids),
                    "generation_depth": proposal.generation_depth,
                    "valid_until_ms": proposal.valid_until_ms,
                    "energy_cost": proposal.energy_cost,
                }
            )
        required = set(self.boundary.source_proposal_ids)
        required.update(
            parent
            for proposal in self.proposals
            for parent in proposal.parent_proposal_ids
        )
        missing = required - ids
        if missing:
            raise ValueError(
                f"return-address lineage is not closed over proposal ancestry: {sorted(missing)}"
            )
        row = {
            "proposals": sorted(proposal_rows, key=lambda item: item["proposal_id"]),
            "boundary": self.boundary.state_dict(),
        }
        validate_runtime_mapping(row, path="v061_a01.md002.return_address")
        return canonical_state(row)


@dataclass(frozen=True, slots=True)
class BoundA01P2State:
    partitions: FrozenPartitionBytes
    local_state: dict[str, Any]
    field_state: dict[str, Any]
    consistency_state: dict[str, Any]
    return_address_state: dict[str, Any] | None


def freeze_a01_p2_partitions(
    *,
    expectation: A01LocalTemporalExpectation,
    field_state: Mapping[str, Any],
    consistency: UntypedBoundaryConsistency,
    return_address: LiveReturnAddressState | None = None,
) -> BoundA01P2State:
    """Serialize one actual L/F/C/R checkpoint without executing capability."""

    local_raw = expectation.learned_state_dict()
    field_raw = dict(field_state)
    consistency_raw = consistency.learned_state_dict()
    validate_runtime_mapping(local_raw, path="v061_a01.md002.local")
    validate_runtime_mapping(field_raw, path="v061_a01.md002.field")
    validate_runtime_mapping(consistency_raw, path="v061_a01.md002.consistency")

    local = canonical_state(local_raw)
    field = canonical_state(field_raw)
    consistency_row = canonical_state(consistency_raw)
    return_row = return_address.state_dict() if return_address is not None else None
    partitions = FrozenPartitionBytes(
        local=canonical_bytes(local),
        field=canonical_bytes(field),
        consistency=canonical_bytes(consistency_row),
        return_address=(None if return_row is None else canonical_bytes(return_row)),
    )
    partitions.validate()
    return BoundA01P2State(
        partitions=partitions,
        local_state=local,
        field_state=field,
        consistency_state=consistency_row,
        return_address_state=return_row,
    )


def build_bound_a01_p2_fixture(
    *,
    expectation: A01LocalTemporalExpectation,
    field_state: Mapping[str, Any],
    consistency: UntypedBoundaryConsistency,
    control_world_relation: Mapping[str, Any],
    intervention_world_relation: Mapping[str, Any],
    admissible_external_evidence: tuple[RuntimePulse, ...],
    return_address: LiveReturnAddressState | None = None,
) -> P2WorldOnlyFixture:
    """Bind actual A01 state to a world-only intervention fixture."""

    if not admissible_external_evidence:
        raise ValueError("P2 requires at least one admissible external observation")
    if any(row.origin is not EventOrigin.EXTERNAL for row in admissible_external_evidence):
        raise ValueError("P2 admissible evidence must contain external observations only")
    if any(
        right.time_ms <= left.time_ms
        for left, right in zip(
            admissible_external_evidence,
            admissible_external_evidence[1:],
            strict=False,
        )
    ):
        raise ValueError("P2 admissible external evidence must be strictly time ordered")

    control = dict(control_world_relation)
    intervention = dict(intervention_world_relation)
    validate_runtime_mapping(control, path="v061_a01.md002.world.control")
    validate_runtime_mapping(intervention, path="v061_a01.md002.world.intervention")
    evidence_rows = [row.as_dict() for row in admissible_external_evidence]
    for row in evidence_rows:
        validate_runtime_mapping(row, path="v061_a01.md002.evidence")

    bound = freeze_a01_p2_partitions(
        expectation=expectation,
        field_state=field_state,
        consistency=consistency,
        return_address=return_address,
    )
    fixture = P2WorldOnlyFixture(
        checkpoint=bound.partitions,
        control_world_relation=canonical_bytes(control),
        intervention_world_relation=canonical_bytes(intervention),
        admissible_external_evidence=canonical_bytes(evidence_rows),
    )
    fixture.prospective_contract().validate()
    return fixture


__all__ = [
    "BoundA01P2State",
    "LiveReturnAddressState",
    "build_bound_a01_p2_fixture",
    "canonical_bytes",
    "canonical_state",
    "freeze_a01_p2_partitions",
]
