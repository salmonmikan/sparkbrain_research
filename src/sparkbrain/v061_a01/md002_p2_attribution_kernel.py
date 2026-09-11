"""Execution-disabled P2 attribution kernel for the prospective A01 MD-002 runner.

The kernel implements one cloned attribution subepisode from already-bound P2
condition input. It deliberately does not iterate the registered MD-002 matrix,
combine subepisodes into a scored diagnostic, invoke the MD002 execution gate, or
open any held-out/formal capability. Tests may exercise this kernel on synthetic
fixtures to validate the actual world-response -> ledger -> consistency -> A01
credit path before a separately authorized diagnostic runner exists.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from typing import Any

from sparkbrain.v06.foundation import EventOrigin, RuntimePulse, digest, validate_runtime_mapping

from .credit_bridge import A01CausalCreditResolution, A01TransientCreditBridge
from .md002_development_plan import P2DevelopmentConditionInput
from .md002_p2_schedule import P2AttributionSubepisode
from .md002_restore_adapter import restore_a01_p2_arm
from .md002_world_fixture import P2AnonymousWorldRelation


@dataclass(frozen=True, slots=True)
class P2AttributionKernelResult:
    condition_id: str
    world_arm: str
    proposal_id: str
    returned_external_evidence: bool
    boundary_event_id: str
    response_event_id: str
    response_target: str
    local_state_hash_before: str
    local_state_hash_after: str
    field_state_hash_before: str
    field_state_hash_after: str
    consistency_state_hash_before: str
    consistency_state_hash_after: str
    resolution: A01CausalCreditResolution | None

    def state_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["resolution"] = self.resolution.state_dict() if self.resolution is not None else None
        validate_runtime_mapping(value, path="v061_a01.md002.p2_attribution_kernel")
        return value


def _world_response(
    relation: P2AnonymousWorldRelation,
    *,
    boundary_event_id: str,
    response_event_id: str,
    response_time_ms: float,
    target: str,
    magnitude: float,
    polarity: int,
) -> RuntimePulse:
    """Construct the anonymous external response selected only by the world relation."""

    relation.validate()
    return RuntimePulse(
        event_id=response_event_id,
        time_ms=response_time_ms,
        target=target,
        magnitude=magnitude,
        polarity=polarity,
        origin=EventOrigin.EXTERNAL,
        parent_event_ids=(boundary_event_id,),
    )


def execute_p2_attribution_subepisode(
    condition: P2DevelopmentConditionInput,
    subepisode: P2AttributionSubepisode,
) -> P2AttributionKernelResult:
    """Execute one cloned P2 attribution subepisode without opening MD-002 itself."""

    condition.validate()
    subepisode.validate()
    scheduled = {row.proposal_id: row for row in condition.schedule.subepisodes}
    if scheduled.get(subepisode.proposal_id) != subepisode:
        raise ValueError("subepisode is not part of the condition's fixed P2 schedule")

    restored = restore_a01_p2_arm(condition.arm_input)
    if restored.boundary is None:
        raise ValueError("P2 attribution requires a live return-address boundary")
    proposal = restored.ledger.proposals.get(subepisode.proposal_id)
    if proposal is None:
        raise ValueError("P2 scheduled proposal is absent from the restored ledger")

    relation = P2AnonymousWorldRelation.from_state_dict(restored.world_relation)
    try:
        response_target = relation.mapping[subepisode.proposal_id]
    except KeyError as exc:
        raise ValueError(
            "P2 scheduled proposal is absent from the anonymous world relation"
        ) from exc

    boundary = replace(
        restored.boundary,
        event_id=subepisode.boundary_event_id,
        time_ms=float(subepisode.boundary_time_ms),
        source_proposal_ids=(subepisode.proposal_id,),
        generation_depth=proposal.generation_depth,
    )
    restored.consistency.register_boundary(boundary)

    local_before = restored.expectation.learned_state_dict()
    field_before = restored.field.state_dict()
    consistency_before = restored.consistency.learned_state_dict()

    response = _world_response(
        relation,
        boundary_event_id=boundary.event_id,
        response_event_id=subepisode.response_event_id,
        response_time_ms=float(subepisode.response_time_ms),
        target=response_target,
        magnitude=float(boundary.magnitude),
        polarity=int(boundary.polarity),
    )

    resolution: A01CausalCreditResolution | None = None
    if condition.returned_external_evidence:
        restored.ledger.register_external(response)
        bridge = A01TransientCreditBridge(
            restored.expectation,
            restored.consistency,
            restored.ledger,
        )
        resolution = bridge.observe_external(boundary, response)

    local_after = restored.expectation.learned_state_dict()
    field_after = restored.field.state_dict()
    consistency_after = restored.consistency.learned_state_dict()
    if digest(field_after) != digest(field_before):
        raise RuntimeError("P2 attribution subepisode unexpectedly modified Field state")
    if not condition.returned_external_evidence:
        if digest(local_after) != digest(local_before):
            raise RuntimeError("P2 withheld condition modified local causal support")
        if digest(consistency_after) != digest(consistency_before):
            raise RuntimeError("P2 withheld condition modified learned consistency state")

    return P2AttributionKernelResult(
        condition_id=condition.condition_id,
        world_arm=condition.world_arm,
        proposal_id=subepisode.proposal_id,
        returned_external_evidence=condition.returned_external_evidence,
        boundary_event_id=boundary.event_id,
        response_event_id=response.event_id,
        response_target=response.target,
        local_state_hash_before=digest(local_before),
        local_state_hash_after=digest(local_after),
        field_state_hash_before=digest(field_before),
        field_state_hash_after=digest(field_after),
        consistency_state_hash_before=digest(consistency_before),
        consistency_state_hash_after=digest(consistency_after),
        resolution=resolution,
    )


__all__ = ["P2AttributionKernelResult", "execute_p2_attribution_subepisode"]
