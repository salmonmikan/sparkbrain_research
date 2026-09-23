from __future__ import annotations

import hashlib
import math
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from typing import Any, Literal

from sparkbrain.v04.contracts import canonical_json

from .brain import IntegratedV05Brain
from .route_architecture import (
    DELAY_PERTURBATION_MS,
    MAX_CANDIDATE_EDGES,
    QUIESCENCE_CAP_MS,
    EdgeControlPair,
    RouteArchitectureUnreachable,
    RouteEdge,
    match_non_target_controls,
    select_candidate_edges,
)

CONTRACT_SCHEMA = "cand34-route-architecture-r2-v1"
MEASUREMENT_WINDOW_MS = 64.0
MAX_EXECUTION_STEPS = 1 + MAX_CANDIDATE_EDGES * 5 + 4
MAX_RESPONSE_CLONES = MAX_EXECUTION_STEPS * 2

EdgeArm = Literal[
    "target_sham",
    "target_transmission_null",
    "target_delay_plus_1ms",
    "matched_non_target_transmission_null",
    "matched_non_target_delay_plus_1ms",
]
GlobalArm = Literal[
    "baseline",
    "assembly_target_suppression",
    "unit_target_suppression",
    "matched_random_assembly_suppression",
    "matched_random_unit_suppression",
]
Arm = EdgeArm | GlobalArm

EDGE_ARM_ORDER: tuple[EdgeArm, ...] = (
    "target_sham",
    "target_transmission_null",
    "target_delay_plus_1ms",
    "matched_non_target_transmission_null",
    "matched_non_target_delay_plus_1ms",
)
GLOBAL_ARM_ORDER: tuple[GlobalArm, ...] = (
    "baseline",
    "assembly_target_suppression",
    "unit_target_suppression",
    "matched_random_assembly_suppression",
    "matched_random_unit_suppression",
)
RESPONSE_FIELDS = (
    "target_assembly_active",
    "target_assembly_mature",
    "target_assembly_similarity",
    "target_prototype_relative_spike_bins",
    "prediction_covered",
    "prediction_correct",
    "collateral_assembly_active",
    "collateral_assembly_similarity",
    "runaway",
    "dead",
)
REDUCTION_PANEL = (
    "target_assembly_suppression",
    "target_unit_suppression",
    "matched_random_assembly_suppression",
    "matched_random_unit_suppression",
    "matched_non_target_edge_transmission_null",
    "matched_non_target_edge_delay_plus_1ms",
    "target_edge_sham",
    "collateral_response",
)
FAIL_CLOSED_REASONS = (
    "no_mature_unsuppressed_assembly",
    "no_candidate_edges",
    "matched_non_target_control_unreachable",
    "quiescence_not_reached_within_256ms",
    "evaluation_surface_not_prebound",
    "response_signature_incomplete_or_invalid",
    "execution_step_or_plan_mismatch",
)
PROTOTYPE_SELECTION_POLICY = (
    "mature_unsuppressed_then_episode_count_desc_occurrences_desc_"
    "mean_similarity_desc_assembly_id_asc"
)
CHECKPOINT_BINDING_POLICY = (
    "bind_exact_integrated_v05_state_hash_before_quiescent_clone_or_intervention"
)
ANCHOR_POLICY = (
    "deep_clone_exact_checkpoint_then_advance_without_input_in_32ms_steps_"
    "until_queue_empty_or_fail_at_256ms_without_cap_extension"
)
EXECUTION_POLICY = (
    "baseline_once_then_each_candidate_edge_in_frozen_rank_order_with_all_edge_arms_"
    "then_global_reductions; each step and each target/collateral cue uses an independent_"
    "deep_clone_of_the_same_quiescent_anchor; no outcome_adaptive_skip_or_reordering"
)
LEARNING_POLICY = "learn_assembly=false;learn_field=false;explore_action=false"
EQUIVALENCE_POLICY = (
    "distinct_route_alternatives_with_identical_complete_frozen_response_vectors_"
    "collapse_to_the_same_interventional_equivalence_class"
)


class RouteArchitectureContractError(ValueError):
    """The prospective R2 contract cannot be constructed or validated."""


@dataclass(frozen=True, slots=True)
class PrototypeBinding:
    checkpoint_sha256: str
    assembly_id: str
    prototype_pattern_id: str
    prototype_sha256: str
    unit_ids: tuple[int, ...]
    ordered_units: tuple[int, ...]
    relative_bins: tuple[int, ...]
    episode_count: int
    occurrences: int
    mean_similarity: float
    support_episode_ids: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        row = asdict(self)
        for key in (
            "unit_ids",
            "ordered_units",
            "relative_bins",
            "support_episode_ids",
        ):
            row[key] = list(row[key])
        return row


@dataclass(frozen=True, slots=True)
class ArchitectureR2Contract:
    schema: str
    candidate_id: str
    claim_ceiling: str
    evidentiary_status: str
    prototype_selection_policy: str
    checkpoint_binding_policy: str
    candidate_edge_limit: int
    edge_ranking: tuple[str, ...]
    delay_perturbation_ms: float
    quiescence_cap_ms: float
    anchor_policy: str
    measurement_window_ms: float
    response_fields: tuple[str, ...]
    edge_arm_order: tuple[EdgeArm, ...]
    global_arm_order: tuple[GlobalArm, ...]
    reduction_panel: tuple[str, ...]
    execution_policy: str
    learning_policy: str
    equivalence_policy: str
    max_execution_steps: int
    max_response_clones: int
    fail_closed_reasons: tuple[str, ...]
    response_bearing_execution_allowed: bool
    preformal_execution_allowed: bool
    formal_action_allowed: bool
    sha256: str

    def as_dict(self) -> dict[str, Any]:
        row = asdict(self)
        for key in (
            "edge_ranking",
            "response_fields",
            "edge_arm_order",
            "global_arm_order",
            "reduction_panel",
            "fail_closed_reasons",
        ):
            row[key] = list(row[key])
        return row


@dataclass(frozen=True, slots=True)
class ReductionBinding:
    control_seed_sha256: str
    target_assembly_id: str
    target_unit_ids: tuple[int, ...]
    matched_random_assembly_id: str
    matched_random_unit_ids: tuple[int, ...]

    def as_dict(self) -> dict[str, Any]:
        row = asdict(self)
        row["target_unit_ids"] = list(self.target_unit_ids)
        row["matched_random_unit_ids"] = list(self.matched_random_unit_ids)
        return row


@dataclass(frozen=True, slots=True)
class EdgeExecutionBinding:
    edge_index: int
    target: RouteEdge
    matched_control: RouteEdge

    def as_dict(self) -> dict[str, Any]:
        return {
            "edge_index": self.edge_index,
            "matched_control": self.matched_control.as_dict(),
            "target": self.target.as_dict(),
        }


@dataclass(frozen=True, slots=True)
class ExecutionStep:
    step_id: str
    arm: Arm
    edge_index: int | None
    target_edge: RouteEdge | None
    control_edge: RouteEdge | None
    assembly_ids: tuple[str, ...] = ()
    unit_ids: tuple[int, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "arm": self.arm,
            "assembly_ids": list(self.assembly_ids),
            "control_edge": (
                self.control_edge.as_dict() if self.control_edge is not None else None
            ),
            "edge_index": self.edge_index,
            "step_id": self.step_id,
            "target_edge": (
                self.target_edge.as_dict() if self.target_edge is not None else None
            ),
            "unit_ids": list(self.unit_ids),
        }


@dataclass(frozen=True, slots=True)
class ExecutionPlan:
    schema: str
    contract_sha256: str
    evaluation_surface_sha256: str
    prototype: PrototypeBinding
    reduction_binding: ReductionBinding
    edge_bindings: tuple[EdgeExecutionBinding, ...]
    steps: tuple[ExecutionStep, ...]
    measurement_window_ms: float
    quiescence_cap_ms: float
    max_response_clones: int
    sha256: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "contract_sha256": self.contract_sha256,
            "edge_bindings": [row.as_dict() for row in self.edge_bindings],
            "evaluation_surface_sha256": self.evaluation_surface_sha256,
            "max_response_clones": self.max_response_clones,
            "measurement_window_ms": self.measurement_window_ms,
            "prototype": self.prototype.as_dict(),
            "reduction_binding": self.reduction_binding.as_dict(),
            "quiescence_cap_ms": self.quiescence_cap_ms,
            "schema": self.schema,
            "sha256": self.sha256,
            "steps": [row.as_dict() for row in self.steps],
        }


@dataclass(frozen=True, slots=True)
class FrozenArchitectureResponse:
    plan_sha256: str
    step_id: str
    arm: Arm
    target_response: Mapping[str, object]
    collateral_response: Mapping[str, object]
    sha256: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "arm": self.arm,
            "collateral_response": dict(self.collateral_response),
            "plan_sha256": self.plan_sha256,
            "sha256": self.sha256,
            "step_id": self.step_id,
            "target_response": dict(self.target_response),
        }


@dataclass(frozen=True, slots=True)
class InterventionalEquivalenceVector:
    plan_sha256: str
    response_sha256s: tuple[str, ...]
    sha256: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "plan_sha256": self.plan_sha256,
            "response_sha256s": list(self.response_sha256s),
            "sha256": self.sha256,
        }


def _sha256(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _valid_sha256(value: str) -> bool:
    return len(value) == 64 and all(char in "0123456789abcdef" for char in value)


def frozen_contract() -> ArchitectureR2Contract:
    edge_ranking = (
        "internal_before_ingress",
        "descending_abs_weight",
        "ascending_delay_ms",
        "ascending_source_id",
        "ascending_target_id",
    )
    payload: dict[str, object] = {
        "schema": CONTRACT_SCHEMA,
        "candidate_id": "CAND-34-ASSEMBLY-TEMPORAL-ROUTE-IDENTIFIABILITY",
        "claim_ceiling": "MECHANISM",
        "evidentiary_status": "MECHANISM_ARCHITECTURE_NON_EVIDENTIARY",
        "prototype_selection_policy": PROTOTYPE_SELECTION_POLICY,
        "checkpoint_binding_policy": CHECKPOINT_BINDING_POLICY,
        "candidate_edge_limit": MAX_CANDIDATE_EDGES,
        "edge_ranking": list(edge_ranking),
        "delay_perturbation_ms": DELAY_PERTURBATION_MS,
        "quiescence_cap_ms": QUIESCENCE_CAP_MS,
        "anchor_policy": ANCHOR_POLICY,
        "measurement_window_ms": MEASUREMENT_WINDOW_MS,
        "response_fields": list(RESPONSE_FIELDS),
        "edge_arm_order": list(EDGE_ARM_ORDER),
        "global_arm_order": list(GLOBAL_ARM_ORDER),
        "reduction_panel": list(REDUCTION_PANEL),
        "execution_policy": EXECUTION_POLICY,
        "learning_policy": LEARNING_POLICY,
        "equivalence_policy": EQUIVALENCE_POLICY,
        "max_execution_steps": MAX_EXECUTION_STEPS,
        "max_response_clones": MAX_RESPONSE_CLONES,
        "fail_closed_reasons": list(FAIL_CLOSED_REASONS),
        "response_bearing_execution_allowed": False,
        "preformal_execution_allowed": False,
        "formal_action_allowed": False,
    }
    return ArchitectureR2Contract(
        schema=CONTRACT_SCHEMA,
        candidate_id="CAND-34-ASSEMBLY-TEMPORAL-ROUTE-IDENTIFIABILITY",
        claim_ceiling="MECHANISM",
        evidentiary_status="MECHANISM_ARCHITECTURE_NON_EVIDENTIARY",
        prototype_selection_policy=PROTOTYPE_SELECTION_POLICY,
        checkpoint_binding_policy=CHECKPOINT_BINDING_POLICY,
        candidate_edge_limit=MAX_CANDIDATE_EDGES,
        edge_ranking=edge_ranking,
        delay_perturbation_ms=DELAY_PERTURBATION_MS,
        quiescence_cap_ms=QUIESCENCE_CAP_MS,
        anchor_policy=ANCHOR_POLICY,
        measurement_window_ms=MEASUREMENT_WINDOW_MS,
        response_fields=RESPONSE_FIELDS,
        edge_arm_order=EDGE_ARM_ORDER,
        global_arm_order=GLOBAL_ARM_ORDER,
        reduction_panel=REDUCTION_PANEL,
        execution_policy=EXECUTION_POLICY,
        learning_policy=LEARNING_POLICY,
        equivalence_policy=EQUIVALENCE_POLICY,
        max_execution_steps=MAX_EXECUTION_STEPS,
        max_response_clones=MAX_RESPONSE_CLONES,
        fail_closed_reasons=FAIL_CLOSED_REASONS,
        response_bearing_execution_allowed=False,
        preformal_execution_allowed=False,
        formal_action_allowed=False,
        sha256=_sha256(payload),
    )


def select_checkpoint_prototype(brain: IntegratedV05Brain) -> PrototypeBinding:
    """Bind a target Assembly using checkpoint state only, never response outcomes."""
    candidates = [
        row
        for row in brain.assemblies.candidates.values()
        if row.episode_count >= brain.assemblies.config.mature_episodes
        and row.assembly_id not in brain.assemblies.suppressed
    ]
    if not candidates:
        raise RouteArchitectureUnreachable("no mature unsuppressed Assembly at checkpoint")
    candidates.sort(
        key=lambda row: (
            -row.episode_count,
            -row.occurrences,
            -row.mean_similarity,
            row.assembly_id,
        )
    )
    target = candidates[0]
    prototype_payload = target.prototype.as_dict()
    return PrototypeBinding(
        checkpoint_sha256=brain.state_hash(),
        assembly_id=target.assembly_id,
        prototype_pattern_id=target.prototype.pattern_id,
        prototype_sha256=_sha256(prototype_payload),
        unit_ids=target.prototype.unit_ids,
        ordered_units=target.prototype.ordered_units,
        relative_bins=target.prototype.relative_bins,
        episode_count=target.episode_count,
        occurrences=target.occurrences,
        mean_similarity=target.mean_similarity,
        support_episode_ids=tuple(sorted(target.episode_ids)),
    )


def _edge_bindings(
    brain: IntegratedV05Brain,
    prototype: PrototypeBinding,
) -> tuple[EdgeExecutionBinding, ...]:
    targets = select_candidate_edges(
        brain.base.field,
        prototype.unit_ids,
        limit=MAX_CANDIDATE_EDGES,
    )
    if not targets:
        raise RouteArchitectureUnreachable("prospective candidate edge family is empty")
    pairs: tuple[EdgeControlPair, ...] = match_non_target_controls(
        brain.base.field,
        prototype.unit_ids,
        targets,
    )
    return tuple(
        EdgeExecutionBinding(
            edge_index=index,
            target=pair.target,
            matched_control=pair.control,
        )
        for index, pair in enumerate(pairs)
    )


def _rank_digest(seed_sha256: str, kind: str, value: object) -> str:
    return _sha256({"kind": kind, "seed_sha256": seed_sha256, "value": value})


def _reduction_binding(
    brain: IntegratedV05Brain,
    prototype: PrototypeBinding,
    *,
    evaluation_surface_sha256: str,
    contract_sha256: str,
) -> ReductionBinding:
    seed = _sha256(
        {
            "checkpoint_sha256": prototype.checkpoint_sha256,
            "contract_sha256": contract_sha256,
            "evaluation_surface_sha256": evaluation_surface_sha256,
            "purpose": "cand34-r2-matched-random-reductions",
        }
    )
    alternatives = [
        row
        for row in brain.assemblies.candidates.values()
        if row.assembly_id != prototype.assembly_id
        and row.episode_count >= brain.assemblies.config.mature_episodes
        and row.assembly_id not in brain.assemblies.suppressed
    ]
    alternatives.sort(
        key=lambda row: (
            abs(len(row.prototype.unit_ids) - len(prototype.unit_ids)),
            abs(row.episode_count - prototype.episode_count),
            _rank_digest(seed, "assembly", row.assembly_id),
            row.assembly_id,
        )
    )
    if not alternatives:
        raise RouteArchitectureUnreachable(
            "prospective matched-random Assembly reduction is unreachable"
        )
    matched_assembly = alternatives[0]

    field = brain.base.field
    target_thresholds = [
        float(field.units[unit_id].base_threshold)
        for unit_id in prototype.unit_ids
        if unit_id in field.units
    ]
    if len(target_thresholds) != len(prototype.unit_ids):
        raise RouteArchitectureUnreachable("target prototype contains non-field unit")
    target_mean_threshold = sum(target_thresholds) / len(target_thresholds)
    receptors = set(field.receptor_ids)
    target_units = set(prototype.unit_ids)
    unit_pool = [
        unit
        for unit in field.units.values()
        if unit.unit_id not in receptors and unit.unit_id not in target_units
    ]
    unit_pool.sort(
        key=lambda unit: (
            abs(float(unit.base_threshold) - target_mean_threshold),
            _rank_digest(seed, "unit", int(unit.unit_id)),
            int(unit.unit_id),
        )
    )
    if len(unit_pool) < len(prototype.unit_ids):
        raise RouteArchitectureUnreachable(
            "prospective matched-random unit reduction is unreachable"
        )
    matched_units = tuple(
        sorted(int(unit.unit_id) for unit in unit_pool[: len(prototype.unit_ids)])
    )
    return ReductionBinding(
        control_seed_sha256=seed,
        target_assembly_id=prototype.assembly_id,
        target_unit_ids=prototype.unit_ids,
        matched_random_assembly_id=matched_assembly.assembly_id,
        matched_random_unit_ids=matched_units,
    )


def _execution_steps(
    bindings: Sequence[EdgeExecutionBinding],
    reductions: ReductionBinding,
) -> tuple[ExecutionStep, ...]:
    steps: list[ExecutionStep] = [
        ExecutionStep(
            step_id="global-baseline",
            arm="baseline",
            edge_index=None,
            target_edge=None,
            control_edge=None,
        )
    ]
    for binding in bindings:
        for arm in EDGE_ARM_ORDER:
            target = (
                binding.matched_control
                if arm.startswith("matched_non_target_")
                else binding.target
            )
            control = binding.matched_control if target is binding.target else binding.target
            steps.append(
                ExecutionStep(
                    step_id=f"edge-{binding.edge_index:02d}-{arm}",
                    arm=arm,
                    edge_index=binding.edge_index,
                    target_edge=target,
                    control_edge=control,
                )
            )
    for arm in GLOBAL_ARM_ORDER[1:]:
        assembly_ids: tuple[str, ...] = ()
        unit_ids: tuple[int, ...] = ()
        if arm == "assembly_target_suppression":
            assembly_ids = (reductions.target_assembly_id,)
        elif arm == "unit_target_suppression":
            unit_ids = reductions.target_unit_ids
        elif arm == "matched_random_assembly_suppression":
            assembly_ids = (reductions.matched_random_assembly_id,)
        elif arm == "matched_random_unit_suppression":
            unit_ids = reductions.matched_random_unit_ids
        steps.append(
            ExecutionStep(
                step_id=f"global-{arm}",
                arm=arm,
                edge_index=None,
                target_edge=None,
                control_edge=None,
                assembly_ids=assembly_ids,
                unit_ids=unit_ids,
            )
        )
    if len(steps) > MAX_EXECUTION_STEPS:
        raise AssertionError("execution plan exceeds frozen resource bound")
    return tuple(steps)


def build_execution_plan(
    brain: IntegratedV05Brain,
    *,
    evaluation_surface_sha256: str,
) -> ExecutionPlan:
    """Construct a target-blind plan without executing a candidate response."""
    if not _valid_sha256(evaluation_surface_sha256):
        raise RouteArchitectureContractError(
            "evaluation surface must be prebound by lowercase sha256"
        )
    contract = frozen_contract()
    prototype = select_checkpoint_prototype(brain)
    reductions = _reduction_binding(
        brain,
        prototype,
        evaluation_surface_sha256=evaluation_surface_sha256,
        contract_sha256=contract.sha256,
    )
    bindings = _edge_bindings(brain, prototype)
    steps = _execution_steps(bindings, reductions)
    payload: dict[str, object] = {
        "schema": CONTRACT_SCHEMA,
        "contract_sha256": contract.sha256,
        "evaluation_surface_sha256": evaluation_surface_sha256,
        "prototype": prototype.as_dict(),
        "reduction_binding": reductions.as_dict(),
        "edge_bindings": [row.as_dict() for row in bindings],
        "steps": [row.as_dict() for row in steps],
        "measurement_window_ms": MEASUREMENT_WINDOW_MS,
        "quiescence_cap_ms": QUIESCENCE_CAP_MS,
        "max_response_clones": len(steps) * 2,
    }
    return ExecutionPlan(
        schema=CONTRACT_SCHEMA,
        contract_sha256=contract.sha256,
        evaluation_surface_sha256=evaluation_surface_sha256,
        prototype=prototype,
        reduction_binding=reductions,
        edge_bindings=bindings,
        steps=steps,
        measurement_window_ms=MEASUREMENT_WINDOW_MS,
        quiescence_cap_ms=QUIESCENCE_CAP_MS,
        max_response_clones=len(steps) * 2,
        sha256=_sha256(payload),
    )


def _validate_response(response: Mapping[str, object]) -> dict[str, object]:
    if set(response) != set(RESPONSE_FIELDS):
        raise RouteArchitectureContractError("response signature field set is not frozen")
    bool_fields = (
        "target_assembly_active",
        "target_assembly_mature",
        "prediction_covered",
        "collateral_assembly_active",
        "runaway",
        "dead",
    )
    for field in bool_fields:
        if type(response[field]) is not bool:
            raise RouteArchitectureContractError(f"{field} must be bool")
    prediction_correct = response["prediction_correct"]
    if prediction_correct is not None and type(prediction_correct) is not bool:
        raise RouteArchitectureContractError("prediction_correct must be bool or null")
    for field in ("target_assembly_similarity", "collateral_assembly_similarity"):
        value = response[field]
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise RouteArchitectureContractError(f"{field} must be numeric")
        numeric = float(value)
        if not math.isfinite(numeric) or not 0.0 <= numeric <= 1.0:
            raise RouteArchitectureContractError(f"{field} must be finite in [0, 1]")
    bins = response["target_prototype_relative_spike_bins"]
    if not isinstance(bins, (list, tuple)) or any(type(value) is not int for value in bins):
        raise RouteArchitectureContractError(
            "target_prototype_relative_spike_bins must be an integer sequence"
        )
    normalized = dict(response)
    normalized["target_assembly_similarity"] = float(
        normalized["target_assembly_similarity"]
    )
    normalized["collateral_assembly_similarity"] = float(
        normalized["collateral_assembly_similarity"]
    )
    normalized["target_prototype_relative_spike_bins"] = list(bins)
    return normalized


def freeze_architecture_response(
    plan: ExecutionPlan,
    *,
    step_id: str,
    target_response: Mapping[str, object],
    collateral_response: Mapping[str, object],
) -> FrozenArchitectureResponse:
    matching = [row for row in plan.steps if row.step_id == step_id]
    if len(matching) != 1:
        raise RouteArchitectureContractError("response step is not bound by the plan")
    step = matching[0]
    target = _validate_response(target_response)
    collateral = _validate_response(collateral_response)
    payload = {
        "plan_sha256": plan.sha256,
        "step_id": step.step_id,
        "arm": step.arm,
        "target_response": target,
        "collateral_response": collateral,
    }
    return FrozenArchitectureResponse(
        plan_sha256=plan.sha256,
        step_id=step.step_id,
        arm=step.arm,
        target_response=target,
        collateral_response=collateral,
        sha256=_sha256(payload),
    )


def freeze_interventional_equivalence_vector(
    plan: ExecutionPlan,
    responses: Sequence[FrozenArchitectureResponse],
) -> InterventionalEquivalenceVector:
    by_step: dict[str, FrozenArchitectureResponse] = {}
    for response in responses:
        if response.plan_sha256 != plan.sha256:
            raise RouteArchitectureContractError("response belongs to a different plan")
        if response.step_id in by_step:
            raise RouteArchitectureContractError("duplicate response step")
        by_step[response.step_id] = response
    expected = tuple(step.step_id for step in plan.steps)
    if set(by_step) != set(expected):
        raise RouteArchitectureContractError(
            "complete frozen response vector is required for equivalence"
        )
    hashes = tuple(by_step[step_id].sha256 for step_id in expected)
    payload = {"plan_sha256": plan.sha256, "response_sha256s": list(hashes)}
    return InterventionalEquivalenceVector(
        plan_sha256=plan.sha256,
        response_sha256s=hashes,
        sha256=_sha256(payload),
    )
