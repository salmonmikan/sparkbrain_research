from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v04.contracts import canonical_json

from .route_architecture import RouteEdge
from .route_preformal import bind_preformal_r1

PREFORMAL_R2_SCHEMA = "cand34-route-preformal-r2-opportunity-v2"
CANDIDATE_ID = "CAND-34-ASSEMBLY-TEMPORAL-ROUTE-IDENTIFIABILITY"
ANALYST_AUTHORITY = "EVA-20260923T105725+0900-R92-6B8E31D4"
DEVELOPMENT_REVISION = (
    "PRE_FORMAL-R2-OPPORTUNITY-AWARE-VERSIONED-REVISION-AUTHORIZED"
)
PRIOR_DEVELOPMENT_RESULT = "D34-Q001"
CUE_POLICY = (
    "per_tested_edge_source_only_threshold_pulse_at_anchor_time; never directly cue "
    "the tested edge destination; matched-control arm cues its own edge source"
)
OPPORTUNITY_POLICY = (
    "source spike is guaranteed prospectively by a source-only pulse equal to the "
    "checkpoint dynamic threshold; destination must be non-refractory and not directly "
    "cued; matched control must have the same weight sign and plasticity class"
)
OBSERVATION_POLICY = (
    "for the tested edge destination record membrane potential and spike state at the "
    "nominal arrival and nominal-plus-1ms arrival boundary, then retain the frozen "
    "64ms Assembly response as secondary scope"
)
CLAIM_SCOPE = (
    "development-only physical route influence on the tested edge destination under "
    "a source-only cue; Assembly-level response is secondary and no null can establish "
    "absence of route causality outside this surface"
)
QUEUE_POLICY = (
    "one fresh queue entry; every condition starts from an independent deep clone of "
    "the same untouched prebound checkpoint; fixed edge and arm order; no outcome-"
    "adaptive skip, reorder, retry, cue replacement, or intervention shopping"
)
PRIMARY_REDUCTION = "edge_destination_membrane_and_spike_response"
SECONDARY_EXPORT = "assembly_level_frozen_response_secondary_only"
RESPONSE_FIELDS = (
    "cued_source_spike_guaranteed_by_contract",
    "edge_destination_membrane_potential_at_nominal_arrival",
    "edge_destination_membrane_potential_at_nominal_plus_1ms",
    "edge_destination_spike_state",
    "assembly_level_frozen_response_secondary",
)
EDGE_ARM_ORDER = (
    "target_sham",
    "target_transmission_null",
    "target_delay_plus_1ms",
    "matched_non_target_transmission_null",
    "matched_non_target_delay_plus_1ms",
)


def _sha256(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _sign_class(value: float) -> int:
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


@dataclass(frozen=True, slots=True)
class UnitExportBinding:
    assembly_id: str
    unit_ids: tuple[int, ...]
    prototype_sha256: str

    def as_dict(self) -> dict[str, Any]:
        row = asdict(self)
        row["unit_ids"] = list(self.unit_ids)
        return row


@dataclass(frozen=True, slots=True)
class EdgeOpportunityBinding:
    edge_index: int
    target_edge: RouteEdge
    matched_control_edge: RouteEdge
    target_cue_source_id: int
    target_cue_current: float
    control_cue_source_id: int
    control_cue_current: float
    target_destination_directly_cued: bool
    control_destination_directly_cued: bool
    target_destination_initial_potential: float
    control_destination_initial_potential: float
    target_destination_dynamic_threshold: float
    control_destination_dynamic_threshold: float
    target_destination_refractory_until_ms: float
    control_destination_refractory_until_ms: float
    target_nominal_arrival_ms: float
    target_delayed_arrival_ms: float
    control_nominal_arrival_ms: float
    control_delayed_arrival_ms: float
    sign_class_matched: bool
    plasticity_matched: bool
    causal_opportunity_predeclared: bool

    def as_dict(self) -> dict[str, Any]:
        return {
            "edge_index": self.edge_index,
            "target_edge": self.target_edge.as_dict(),
            "matched_control_edge": self.matched_control_edge.as_dict(),
            "target_cue_source_id": self.target_cue_source_id,
            "target_cue_current": self.target_cue_current,
            "control_cue_source_id": self.control_cue_source_id,
            "control_cue_current": self.control_cue_current,
            "target_destination_directly_cued": self.target_destination_directly_cued,
            "control_destination_directly_cued": self.control_destination_directly_cued,
            "target_destination_initial_potential": self.target_destination_initial_potential,
            "control_destination_initial_potential": self.control_destination_initial_potential,
            "target_destination_dynamic_threshold": self.target_destination_dynamic_threshold,
            "control_destination_dynamic_threshold": self.control_destination_dynamic_threshold,
            "target_destination_refractory_until_ms": (
                self.target_destination_refractory_until_ms
            ),
            "control_destination_refractory_until_ms": (
                self.control_destination_refractory_until_ms
            ),
            "target_nominal_arrival_ms": self.target_nominal_arrival_ms,
            "target_delayed_arrival_ms": self.target_delayed_arrival_ms,
            "control_nominal_arrival_ms": self.control_nominal_arrival_ms,
            "control_delayed_arrival_ms": self.control_delayed_arrival_ms,
            "sign_class_matched": self.sign_class_matched,
            "plasticity_matched": self.plasticity_matched,
            "causal_opportunity_predeclared": self.causal_opportunity_predeclared,
        }


@dataclass(frozen=True, slots=True)
class QueueConditionBinding:
    step_id: str
    arm: str
    edge_index: int
    intervention_edge: RouteEdge
    cue_source_id: int
    cue_current: float
    observed_destination_unit_id: int
    checkpoint_sha256: str
    opportunity_plan_sha256: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "step_id": self.step_id,
            "arm": self.arm,
            "edge_index": self.edge_index,
            "intervention_edge": self.intervention_edge.as_dict(),
            "cue_source_id": self.cue_source_id,
            "cue_current": self.cue_current,
            "observed_destination_unit_id": self.observed_destination_unit_id,
            "checkpoint_sha256": self.checkpoint_sha256,
            "opportunity_plan_sha256": self.opportunity_plan_sha256,
        }


@dataclass(frozen=True, slots=True)
class PreformalR2ContractClosure:
    schema: str
    candidate_id: str
    analyst_authority: str
    development_revision: str
    prior_development_result: str
    prior_result_preserved_unchanged: bool
    architecture_contract_sha256: str
    r1_prebinding_sha256: str
    r1_execution_plan_sha256: str
    checkpoint_sha256: str
    cue_policy: str
    opportunity_policy: str
    observation_policy: str
    claim_scope: str
    queue_policy: str
    primary_reduction: str
    secondary_export: str
    response_fields: tuple[str, ...]
    opportunity_ledger: tuple[EdgeOpportunityBinding, ...]
    unit_export_map: tuple[UnitExportBinding, ...]
    queue_conditions: tuple[QueueConditionBinding, ...]
    opportunity_plan_sha256: str
    response_bearing_execution_allowed: bool
    fresh_analyst_ready_review_required: bool
    formal_action_allowed: bool
    sha256: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "candidate_id": self.candidate_id,
            "analyst_authority": self.analyst_authority,
            "development_revision": self.development_revision,
            "prior_development_result": self.prior_development_result,
            "prior_result_preserved_unchanged": self.prior_result_preserved_unchanged,
            "architecture_contract_sha256": self.architecture_contract_sha256,
            "r1_prebinding_sha256": self.r1_prebinding_sha256,
            "r1_execution_plan_sha256": self.r1_execution_plan_sha256,
            "checkpoint_sha256": self.checkpoint_sha256,
            "cue_policy": self.cue_policy,
            "opportunity_policy": self.opportunity_policy,
            "observation_policy": self.observation_policy,
            "claim_scope": self.claim_scope,
            "queue_policy": self.queue_policy,
            "primary_reduction": self.primary_reduction,
            "secondary_export": self.secondary_export,
            "response_fields": list(self.response_fields),
            "opportunity_ledger": [row.as_dict() for row in self.opportunity_ledger],
            "unit_export_map": [row.as_dict() for row in self.unit_export_map],
            "queue_conditions": [row.as_dict() for row in self.queue_conditions],
            "opportunity_plan_sha256": self.opportunity_plan_sha256,
            "response_bearing_execution_allowed": self.response_bearing_execution_allowed,
            "fresh_analyst_ready_review_required": (
                self.fresh_analyst_ready_review_required
            ),
            "formal_action_allowed": self.formal_action_allowed,
            "sha256": self.sha256,
        }


@dataclass(frozen=True, slots=True)
class PreformalR2QueueEntry:
    schema: str
    queue_entry_id: str
    candidate_id: str
    analyst_authority: str
    development_revision: str
    contract_closure_sha256: str
    checkpoint_sha256: str
    opportunity_plan_sha256: str
    queue_policy: str
    status: str
    response_bearing_execution_performed: bool
    formal_action_performed: bool
    sha256: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _unit_export_map(brain: object, surface: object, plan: object) -> tuple[UnitExportBinding, ...]:
    assembly_ids = {
        surface.target_prototype.assembly_id,
        surface.collateral_prototype.assembly_id,
        plan.reduction_binding.target_assembly_id,
        plan.reduction_binding.matched_random_assembly_id,
    }
    rows: list[UnitExportBinding] = []
    for assembly_id in sorted(assembly_ids):
        candidate = brain.assemblies.candidates.get(assembly_id)
        if candidate is None:
            raise ValueError(f"missing unit-export assembly: {assembly_id}")
        unit_ids = tuple(int(value) for value in candidate.prototype.unit_ids)
        if not unit_ids or len(set(unit_ids)) != len(unit_ids):
            raise ValueError(f"degenerate unit-export map: {assembly_id}")
        rows.append(
            UnitExportBinding(
                assembly_id=assembly_id,
                unit_ids=unit_ids,
                prototype_sha256=_sha256(candidate.prototype.as_dict()),
            )
        )
    return tuple(rows)


def _edge_opportunity_ledger(brain: object, plan: object) -> tuple[EdgeOpportunityBinding, ...]:
    field = brain.base.field
    cue_time = float(field.current_time_ms)
    rows: list[EdgeOpportunityBinding] = []
    for binding in plan.edge_bindings:
        target = binding.target
        control = binding.matched_control
        target_source = field.units[target.source_id]
        control_source = field.units[control.source_id]
        target_destination = field.units[target.target_id]
        control_destination = field.units[control.target_id]
        target_cue_current = float(field.dynamic_threshold(target_source))
        control_cue_current = float(field.dynamic_threshold(control_source))
        if cue_time < target_source.refractory_until_ms:
            raise ValueError("target edge source is refractory at the R2 cue anchor")
        if cue_time < control_source.refractory_until_ms:
            raise ValueError("control edge source is refractory at the R2 cue anchor")
        if cue_time < target_destination.refractory_until_ms:
            raise ValueError("target edge destination is refractory at the R2 cue anchor")
        if cue_time < control_destination.refractory_until_ms:
            raise ValueError("control edge destination is refractory at the R2 cue anchor")
        sign_matched = _sign_class(target.weight) == _sign_class(control.weight)
        plasticity_matched = target.plastic == control.plastic
        if not sign_matched or not plasticity_matched:
            raise ValueError("matched control lacks fixed metadata class match")
        rows.append(
            EdgeOpportunityBinding(
                edge_index=int(binding.edge_index),
                target_edge=target,
                matched_control_edge=control,
                target_cue_source_id=target.source_id,
                target_cue_current=target_cue_current,
                control_cue_source_id=control.source_id,
                control_cue_current=control_cue_current,
                target_destination_directly_cued=False,
                control_destination_directly_cued=False,
                target_destination_initial_potential=float(target_destination.potential),
                control_destination_initial_potential=float(control_destination.potential),
                target_destination_dynamic_threshold=float(
                    field.dynamic_threshold(target_destination)
                ),
                control_destination_dynamic_threshold=float(
                    field.dynamic_threshold(control_destination)
                ),
                target_destination_refractory_until_ms=float(
                    target_destination.refractory_until_ms
                ),
                control_destination_refractory_until_ms=float(
                    control_destination.refractory_until_ms
                ),
                target_nominal_arrival_ms=cue_time + target.delay_ms,
                target_delayed_arrival_ms=cue_time + target.delay_ms + 1.0,
                control_nominal_arrival_ms=cue_time + control.delay_ms,
                control_delayed_arrival_ms=cue_time + control.delay_ms + 1.0,
                sign_class_matched=sign_matched,
                plasticity_matched=plasticity_matched,
                causal_opportunity_predeclared=True,
            )
        )
    if not rows:
        raise ValueError("R2 opportunity ledger must bind at least one target edge")
    return tuple(rows)


def _queue_conditions(
    *,
    checkpoint_sha256: str,
    ledger: tuple[EdgeOpportunityBinding, ...],
    opportunity_plan_sha256: str,
) -> tuple[QueueConditionBinding, ...]:
    rows: list[QueueConditionBinding] = []
    for item in ledger:
        for arm in EDGE_ARM_ORDER:
            use_control = arm.startswith("matched_non_target_")
            edge = item.matched_control_edge if use_control else item.target_edge
            cue_source_id = (
                item.control_cue_source_id if use_control else item.target_cue_source_id
            )
            cue_current = (
                item.control_cue_current if use_control else item.target_cue_current
            )
            rows.append(
                QueueConditionBinding(
                    step_id=f"r2-edge-{item.edge_index:02d}-{arm}",
                    arm=arm,
                    edge_index=item.edge_index,
                    intervention_edge=edge,
                    cue_source_id=cue_source_id,
                    cue_current=cue_current,
                    observed_destination_unit_id=edge.target_id,
                    checkpoint_sha256=checkpoint_sha256,
                    opportunity_plan_sha256=opportunity_plan_sha256,
                )
            )
    return tuple(rows)


def bind_preformal_r2_contract_closure() -> tuple[
    PreformalR2ContractClosure,
    PreformalR2QueueEntry,
]:
    """Close R92's opportunity-aware R2 contract without candidate responses."""
    brain, contract, surface, r1_plan, r1_binding = bind_preformal_r1()
    if brain.results or brain.trace:
        raise RuntimeError("R2 contract closure must not execute a candidate response")
    if contract.measurement_window_ms != 64.0 or contract.quiescence_cap_ms != 256.0:
        raise RuntimeError("Architecture-R2 measurement contract drift")
    if contract.response_bearing_execution_allowed or contract.formal_action_allowed:
        raise RuntimeError("Architecture-R2 one-way guard drift")

    ledger = _edge_opportunity_ledger(brain, r1_plan)
    unit_export_map = _unit_export_map(brain, surface, r1_plan)
    opportunity_payload: dict[str, object] = {
        "schema": PREFORMAL_R2_SCHEMA,
        "candidate_id": CANDIDATE_ID,
        "analyst_authority": ANALYST_AUTHORITY,
        "development_revision": DEVELOPMENT_REVISION,
        "checkpoint_sha256": surface.checkpoint_sha256,
        "cue_policy": CUE_POLICY,
        "opportunity_policy": OPPORTUNITY_POLICY,
        "observation_policy": OBSERVATION_POLICY,
        "claim_scope": CLAIM_SCOPE,
        "response_fields": list(RESPONSE_FIELDS),
        "edge_arm_order": list(EDGE_ARM_ORDER),
        "opportunity_ledger": [row.as_dict() for row in ledger],
    }
    opportunity_plan_sha256 = _sha256(opportunity_payload)
    conditions = _queue_conditions(
        checkpoint_sha256=surface.checkpoint_sha256,
        ledger=ledger,
        opportunity_plan_sha256=opportunity_plan_sha256,
    )

    payload: dict[str, object] = {
        **opportunity_payload,
        "prior_development_result": PRIOR_DEVELOPMENT_RESULT,
        "prior_result_preserved_unchanged": True,
        "architecture_contract_sha256": contract.sha256,
        "r1_prebinding_sha256": r1_binding.sha256,
        "r1_execution_plan_sha256": r1_plan.sha256,
        "queue_policy": QUEUE_POLICY,
        "primary_reduction": PRIMARY_REDUCTION,
        "secondary_export": SECONDARY_EXPORT,
        "unit_export_map": [row.as_dict() for row in unit_export_map],
        "queue_conditions": [row.as_dict() for row in conditions],
        "opportunity_plan_sha256": opportunity_plan_sha256,
        "response_bearing_execution_allowed": False,
        "fresh_analyst_ready_review_required": True,
        "formal_action_allowed": False,
    }
    closure_sha256 = _sha256(payload)
    closure = PreformalR2ContractClosure(
        schema=PREFORMAL_R2_SCHEMA,
        candidate_id=CANDIDATE_ID,
        analyst_authority=ANALYST_AUTHORITY,
        development_revision=DEVELOPMENT_REVISION,
        prior_development_result=PRIOR_DEVELOPMENT_RESULT,
        prior_result_preserved_unchanged=True,
        architecture_contract_sha256=contract.sha256,
        r1_prebinding_sha256=r1_binding.sha256,
        r1_execution_plan_sha256=r1_plan.sha256,
        checkpoint_sha256=surface.checkpoint_sha256,
        cue_policy=CUE_POLICY,
        opportunity_policy=OPPORTUNITY_POLICY,
        observation_policy=OBSERVATION_POLICY,
        claim_scope=CLAIM_SCOPE,
        queue_policy=QUEUE_POLICY,
        primary_reduction=PRIMARY_REDUCTION,
        secondary_export=SECONDARY_EXPORT,
        response_fields=RESPONSE_FIELDS,
        opportunity_ledger=ledger,
        unit_export_map=unit_export_map,
        queue_conditions=conditions,
        opportunity_plan_sha256=opportunity_plan_sha256,
        response_bearing_execution_allowed=False,
        fresh_analyst_ready_review_required=True,
        formal_action_allowed=False,
        sha256=closure_sha256,
    )

    queue_payload: dict[str, object] = {
        "schema": PREFORMAL_R2_SCHEMA,
        "queue_entry_id": "D34-Q002",
        "candidate_id": CANDIDATE_ID,
        "analyst_authority": ANALYST_AUTHORITY,
        "development_revision": DEVELOPMENT_REVISION,
        "contract_closure_sha256": closure.sha256,
        "checkpoint_sha256": closure.checkpoint_sha256,
        "opportunity_plan_sha256": closure.opportunity_plan_sha256,
        "queue_policy": closure.queue_policy,
        "status": "AWAITING_FRESH_ANALYST_READY_REVIEW",
        "response_bearing_execution_performed": False,
        "formal_action_performed": False,
    }
    queue = PreformalR2QueueEntry(
        schema=PREFORMAL_R2_SCHEMA,
        queue_entry_id="D34-Q002",
        candidate_id=CANDIDATE_ID,
        analyst_authority=ANALYST_AUTHORITY,
        development_revision=DEVELOPMENT_REVISION,
        contract_closure_sha256=closure.sha256,
        checkpoint_sha256=closure.checkpoint_sha256,
        opportunity_plan_sha256=closure.opportunity_plan_sha256,
        queue_policy=closure.queue_policy,
        status="AWAITING_FRESH_ANALYST_READY_REVIEW",
        response_bearing_execution_performed=False,
        formal_action_performed=False,
        sha256=_sha256(queue_payload),
    )
    return closure, queue
