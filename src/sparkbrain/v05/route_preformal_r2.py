from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v04.contracts import canonical_json

from .route_preformal import bind_preformal_r1

PREFORMAL_R2_SCHEMA = "cand34-route-preformal-r2-v1"
CANDIDATE_ID = "CAND-34-ASSEMBLY-TEMPORAL-ROUTE-IDENTIFIABILITY"
ANALYST_AUTHORITY = "EVA-20260923T110053+0900-R92-A7B61F3C"
PRIOR_DEVELOPMENT_RESULT = "D34-Q001"
QUEUE_POLICY = (
    "one_fresh_queue_entry; every execution step starts from an independent deep clone "
    "of the same untouched prebound checkpoint/anchor; no outcome-adaptive skip, "
    "reorder, retry, or anchor replacement"
)
PRIMARY_REDUCTION = (
    "assembly_level_reference_responses_and_assembly_level_intervention_deltas"
)
SECONDARY_EXPORT = "unit_index_reductions_secondary_export_only"


def _sha256(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


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
class QueueConditionBinding:
    step_id: str
    arm: str
    anchor_checkpoint_sha256: str
    execution_plan_sha256: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class PreformalR2ContractClosure:
    schema: str
    candidate_id: str
    analyst_authority: str
    prior_development_result: str
    prior_result_preserved_unchanged: bool
    architecture_contract_sha256: str
    r1_prebinding_sha256: str
    checkpoint_sha256: str
    execution_plan_sha256: str
    queue_policy: str
    primary_reduction: str
    secondary_export: str
    unit_export_map: tuple[UnitExportBinding, ...]
    queue_conditions: tuple[QueueConditionBinding, ...]
    response_bearing_execution_allowed: bool
    formal_action_allowed: bool
    sha256: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "candidate_id": self.candidate_id,
            "analyst_authority": self.analyst_authority,
            "prior_development_result": self.prior_development_result,
            "prior_result_preserved_unchanged": self.prior_result_preserved_unchanged,
            "architecture_contract_sha256": self.architecture_contract_sha256,
            "r1_prebinding_sha256": self.r1_prebinding_sha256,
            "checkpoint_sha256": self.checkpoint_sha256,
            "execution_plan_sha256": self.execution_plan_sha256,
            "queue_policy": self.queue_policy,
            "primary_reduction": self.primary_reduction,
            "secondary_export": self.secondary_export,
            "unit_export_map": [row.as_dict() for row in self.unit_export_map],
            "queue_conditions": [row.as_dict() for row in self.queue_conditions],
            "response_bearing_execution_allowed": self.response_bearing_execution_allowed,
            "formal_action_allowed": self.formal_action_allowed,
            "sha256": self.sha256,
        }


@dataclass(frozen=True, slots=True)
class PreformalR2QueueEntry:
    schema: str
    queue_entry_id: str
    candidate_id: str
    analyst_authority: str
    contract_closure_sha256: str
    checkpoint_sha256: str
    execution_plan_sha256: str
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
    if len({row.assembly_id for row in rows}) != len(rows):
        raise ValueError("ambiguous unit-export assembly map")
    return tuple(rows)


def bind_preformal_r2_contract_closure() -> tuple[
    PreformalR2ContractClosure,
    PreformalR2QueueEntry,
]:
    """Close R92's prospective R2 contract without executing candidate responses."""
    brain, contract, surface, plan, r1_binding = bind_preformal_r1()
    if brain.results or brain.trace:
        raise RuntimeError("R2 contract closure must not execute a candidate response")
    if contract.measurement_window_ms != 64.0 or contract.quiescence_cap_ms != 256.0:
        raise RuntimeError("Architecture-R2 measurement contract drift")
    if contract.response_bearing_execution_allowed or contract.formal_action_allowed:
        raise RuntimeError("Architecture-R2 one-way guard drift")

    unit_export_map = _unit_export_map(brain, surface, plan)
    queue_conditions = tuple(
        QueueConditionBinding(
            step_id=step.step_id,
            arm=step.arm,
            anchor_checkpoint_sha256=surface.checkpoint_sha256,
            execution_plan_sha256=plan.sha256,
        )
        for step in plan.steps
    )
    if not queue_conditions:
        raise ValueError("R2 queue must bind at least one prospective condition")
    if {row.anchor_checkpoint_sha256 for row in queue_conditions} != {
        surface.checkpoint_sha256
    }:
        raise ValueError("queue conditions do not share one untouched anchor")

    payload: dict[str, object] = {
        "schema": PREFORMAL_R2_SCHEMA,
        "candidate_id": CANDIDATE_ID,
        "analyst_authority": ANALYST_AUTHORITY,
        "prior_development_result": PRIOR_DEVELOPMENT_RESULT,
        "prior_result_preserved_unchanged": True,
        "architecture_contract_sha256": contract.sha256,
        "r1_prebinding_sha256": r1_binding.sha256,
        "checkpoint_sha256": surface.checkpoint_sha256,
        "execution_plan_sha256": plan.sha256,
        "queue_policy": QUEUE_POLICY,
        "primary_reduction": PRIMARY_REDUCTION,
        "secondary_export": SECONDARY_EXPORT,
        "unit_export_map": [row.as_dict() for row in unit_export_map],
        "queue_conditions": [row.as_dict() for row in queue_conditions],
        "response_bearing_execution_allowed": False,
        "formal_action_allowed": False,
    }
    closure_sha256 = _sha256(payload)
    closure = PreformalR2ContractClosure(
        schema=PREFORMAL_R2_SCHEMA,
        candidate_id=CANDIDATE_ID,
        analyst_authority=ANALYST_AUTHORITY,
        prior_development_result=PRIOR_DEVELOPMENT_RESULT,
        prior_result_preserved_unchanged=True,
        architecture_contract_sha256=contract.sha256,
        r1_prebinding_sha256=r1_binding.sha256,
        checkpoint_sha256=surface.checkpoint_sha256,
        execution_plan_sha256=plan.sha256,
        queue_policy=QUEUE_POLICY,
        primary_reduction=PRIMARY_REDUCTION,
        secondary_export=SECONDARY_EXPORT,
        unit_export_map=unit_export_map,
        queue_conditions=queue_conditions,
        response_bearing_execution_allowed=False,
        formal_action_allowed=False,
        sha256=closure_sha256,
    )

    queue_payload: dict[str, object] = {
        "schema": PREFORMAL_R2_SCHEMA,
        "queue_entry_id": "D34-Q002",
        "candidate_id": CANDIDATE_ID,
        "analyst_authority": ANALYST_AUTHORITY,
        "contract_closure_sha256": closure.sha256,
        "checkpoint_sha256": closure.checkpoint_sha256,
        "execution_plan_sha256": closure.execution_plan_sha256,
        "queue_policy": closure.queue_policy,
        "status": "QUEUED_NOT_EXECUTED",
        "response_bearing_execution_performed": False,
        "formal_action_performed": False,
    }
    queue = PreformalR2QueueEntry(
        schema=PREFORMAL_R2_SCHEMA,
        queue_entry_id="D34-Q002",
        candidate_id=CANDIDATE_ID,
        analyst_authority=ANALYST_AUTHORITY,
        contract_closure_sha256=closure.sha256,
        checkpoint_sha256=closure.checkpoint_sha256,
        execution_plan_sha256=closure.execution_plan_sha256,
        queue_policy=closure.queue_policy,
        status="QUEUED_NOT_EXECUTED",
        response_bearing_execution_performed=False,
        formal_action_performed=False,
        sha256=_sha256(queue_payload),
    )
    return closure, queue
