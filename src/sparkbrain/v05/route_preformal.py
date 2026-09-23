from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v04.contracts import canonical_json
from sparkbrain.v04.field import TemporalExcitableField
from sparkbrain.v04.topology import Connection, UnitState, explicit_topology

from .assemblies import TemporalAssemblyMemory
from .brain import IntegratedV05Brain
from .contracts import ActivityPattern
from .route_architecture_contract import (
    ArchitectureR2Contract,
    ExecutionPlan,
    PrototypeBinding,
    build_execution_plan,
    frozen_contract,
    select_checkpoint_prototype,
)

PREFORMAL_SCHEMA = "cand34-route-preformal-r1-v1"
CANDIDATE_ID = "CAND-34-ASSEMBLY-TEMPORAL-ROUTE-IDENTIFIABILITY"
ARCHITECTURE_R2_HEAD = "a6455a3929b86ad25fd106ea93a03604192fc3be"
ANALYST_AUTHORITY = "EVA-20260923T101328+0900-R91-C199605F"
DEVELOPMENT_SURFACE_ID = "cand34-preformal-r1-development-surface-01"
CUE_POLICY = "prototype_direct_threshold_arrival_replay_v1"


def _sha256(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class CueArrivalBinding:
    unit_id: int
    relative_time_ms: float
    current: float
    pulse_id: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class CueBinding:
    role: str
    assembly_id: str
    prototype_pattern_id: str
    arrivals: tuple[CueArrivalBinding, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "assembly_id": self.assembly_id,
            "prototype_pattern_id": self.prototype_pattern_id,
            "arrivals": [row.as_dict() for row in self.arrivals],
        }


@dataclass(frozen=True, slots=True)
class DevelopmentSurfaceBinding:
    schema: str
    candidate_id: str
    development_surface_id: str
    architecture_r2_head: str
    analyst_authority: str
    checkpoint_sha256: str
    target_prototype: PrototypeBinding
    collateral_prototype: PrototypeBinding
    cue_policy: str
    target_cue: CueBinding
    collateral_cue: CueBinding
    response_bearing_execution_allowed: bool
    formal_action_allowed: bool
    sha256: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "candidate_id": self.candidate_id,
            "development_surface_id": self.development_surface_id,
            "architecture_r2_head": self.architecture_r2_head,
            "analyst_authority": self.analyst_authority,
            "checkpoint_sha256": self.checkpoint_sha256,
            "target_prototype": self.target_prototype.as_dict(),
            "collateral_prototype": self.collateral_prototype.as_dict(),
            "cue_policy": self.cue_policy,
            "target_cue": self.target_cue.as_dict(),
            "collateral_cue": self.collateral_cue.as_dict(),
            "response_bearing_execution_allowed": self.response_bearing_execution_allowed,
            "formal_action_allowed": self.formal_action_allowed,
            "sha256": self.sha256,
        }


@dataclass(frozen=True, slots=True)
class PreformalR1Binding:
    schema: str
    candidate_id: str
    analyst_authority: str
    architecture_r2_head: str
    architecture_contract_sha256: str
    development_surface_sha256: str
    checkpoint_sha256: str
    execution_plan_sha256: str
    target_assembly_id: str
    collateral_assembly_id: str
    response_bearing_execution_performed: bool
    evidentiary_status: str
    sha256: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _development_field() -> TemporalExcitableField:
    units = tuple(UnitState(unit_id=i, x=float(i), y=0.0) for i in range(7))
    edges = (
        Connection(3, 2, -0.40, 3.0),
        Connection(2, 3, 0.20, 2.0),
        Connection(1, 2, 0.90, 1.0),
        Connection(4, 2, 0.80, 1.5),
        Connection(1, 4, 0.88, 1.1),
        Connection(4, 5, 0.22, 2.2),
        Connection(5, 6, -0.39, 3.1),
        Connection(6, 5, 0.78, 1.6),
        Connection(5, 1, 0.19, 2.1),
    )
    topology = explicit_topology(units, edges, receptor_ids=(0,))
    return TemporalExcitableField(topology)


def _pattern(
    pattern_id: str,
    units: tuple[int, ...],
    bins: tuple[int, ...],
) -> ActivityPattern:
    return ActivityPattern(
        pattern_id=pattern_id,
        start_ms=0.0,
        end_ms=float(max(bins, default=0)),
        ordered_units=units,
        relative_bins=bins,
        unit_ids=tuple(sorted(set(units))),
        spike_count=len(units),
    )


def build_development_checkpoint() -> IntegratedV05Brain:
    """Construct the single R91-authorized development checkpoint without responses.

    This is a deterministic development-only surface.  It reuses the same small
    reachability topology used during Architecture R2 construction, but no
    Architecture observation or Forge history is treated as evidentiary support.
    """
    brain = IntegratedV05Brain()
    brain.base.field = _development_field()
    brain.assemblies = TemporalAssemblyMemory()
    target = _pattern("target-pattern", (2, 3), (0, 4))
    collateral = _pattern("collateral-pattern", (5, 6), (0, 4))
    for index in range(3):
        brain.assemblies.observe(
            target,
            time_ms=float(index),
            episode_id=f"target-{index}",
        )
        brain.assemblies.observe(
            collateral,
            time_ms=float(index),
            episode_id=f"collateral-{index}",
        )
    return brain


def _prototype_binding_for_assembly(
    brain: IntegratedV05Brain,
    assembly_id: str,
) -> PrototypeBinding:
    candidate = brain.assemblies.candidates[assembly_id]
    prototype = candidate.prototype
    return PrototypeBinding(
        checkpoint_sha256=brain.state_hash(),
        assembly_id=candidate.assembly_id,
        prototype_pattern_id=prototype.pattern_id,
        prototype_sha256=_sha256(prototype.as_dict()),
        unit_ids=prototype.unit_ids,
        ordered_units=prototype.ordered_units,
        relative_bins=prototype.relative_bins,
        episode_count=candidate.episode_count,
        occurrences=candidate.occurrences,
        mean_similarity=candidate.mean_similarity,
        support_episode_ids=tuple(sorted(candidate.episode_ids)),
    )


def _select_collateral_prototype(
    brain: IntegratedV05Brain,
    target: PrototypeBinding,
) -> PrototypeBinding:
    candidates = [
        row
        for row in brain.assemblies.candidates.values()
        if row.assembly_id != target.assembly_id
        and row.episode_count >= brain.assemblies.config.mature_episodes
        and row.assembly_id not in brain.assemblies.suppressed
    ]
    if not candidates:
        raise ValueError("development surface requires one mature collateral Assembly")
    candidates.sort(
        key=lambda row: (
            -row.episode_count,
            -row.occurrences,
            -row.mean_similarity,
            row.assembly_id,
        )
    )
    return _prototype_binding_for_assembly(brain, candidates[0].assembly_id)


def _cue_binding(
    brain: IntegratedV05Brain,
    prototype: PrototypeBinding,
    *,
    role: str,
) -> CueBinding:
    bin_ms = float(brain.config.pattern_temporal_bin_ms)
    arrivals: list[CueArrivalBinding] = []
    for index, (unit_id, relative_bin) in enumerate(
        zip(prototype.ordered_units, prototype.relative_bins, strict=True)
    ):
        unit = brain.base.field.units[unit_id]
        arrivals.append(
            CueArrivalBinding(
                unit_id=int(unit_id),
                relative_time_ms=float(relative_bin) * bin_ms,
                current=float(unit.base_threshold),
                pulse_id=(
                    f"{DEVELOPMENT_SURFACE_ID}:{role}:{prototype.prototype_pattern_id}:"
                    f"{index:02d}"
                ),
            )
        )
    return CueBinding(
        role=role,
        assembly_id=prototype.assembly_id,
        prototype_pattern_id=prototype.prototype_pattern_id,
        arrivals=tuple(arrivals),
    )


def bind_development_surface(
    brain: IntegratedV05Brain,
) -> DevelopmentSurfaceBinding:
    contract = frozen_contract()
    if contract.response_bearing_execution_allowed:
        raise AssertionError("Architecture R2 must remain non-executable in place")
    if contract.preformal_execution_allowed:
        raise AssertionError("Architecture R2 must not be edited to enable PRE_FORMAL")
    if contract.formal_action_allowed:
        raise AssertionError("Architecture R2 must retain FORMAL stop")

    target = select_checkpoint_prototype(brain)
    collateral = _select_collateral_prototype(brain, target)
    target_cue = _cue_binding(brain, target, role="target")
    collateral_cue = _cue_binding(brain, collateral, role="collateral")
    checkpoint_sha256 = brain.state_hash()
    payload: dict[str, object] = {
        "schema": PREFORMAL_SCHEMA,
        "candidate_id": CANDIDATE_ID,
        "development_surface_id": DEVELOPMENT_SURFACE_ID,
        "architecture_r2_head": ARCHITECTURE_R2_HEAD,
        "analyst_authority": ANALYST_AUTHORITY,
        "checkpoint_sha256": checkpoint_sha256,
        "target_prototype": target.as_dict(),
        "collateral_prototype": collateral.as_dict(),
        "cue_policy": CUE_POLICY,
        "target_cue": target_cue.as_dict(),
        "collateral_cue": collateral_cue.as_dict(),
        "response_bearing_execution_allowed": True,
        "formal_action_allowed": False,
    }
    return DevelopmentSurfaceBinding(
        schema=PREFORMAL_SCHEMA,
        candidate_id=CANDIDATE_ID,
        development_surface_id=DEVELOPMENT_SURFACE_ID,
        architecture_r2_head=ARCHITECTURE_R2_HEAD,
        analyst_authority=ANALYST_AUTHORITY,
        checkpoint_sha256=checkpoint_sha256,
        target_prototype=target,
        collateral_prototype=collateral,
        cue_policy=CUE_POLICY,
        target_cue=target_cue,
        collateral_cue=collateral_cue,
        response_bearing_execution_allowed=True,
        formal_action_allowed=False,
        sha256=_sha256(payload),
    )


def bind_preformal_r1() -> tuple[
    IntegratedV05Brain,
    ArchitectureR2Contract,
    DevelopmentSurfaceBinding,
    ExecutionPlan,
    PreformalR1Binding,
]:
    """Bind PRE_FORMAL R1 exactly; do not execute any candidate response."""
    brain = build_development_checkpoint()
    contract = frozen_contract()
    surface = bind_development_surface(brain)
    plan = build_execution_plan(
        brain,
        evaluation_surface_sha256=surface.sha256,
    )
    payload: dict[str, object] = {
        "schema": PREFORMAL_SCHEMA,
        "candidate_id": CANDIDATE_ID,
        "analyst_authority": ANALYST_AUTHORITY,
        "architecture_r2_head": ARCHITECTURE_R2_HEAD,
        "architecture_contract_sha256": contract.sha256,
        "development_surface_sha256": surface.sha256,
        "checkpoint_sha256": surface.checkpoint_sha256,
        "execution_plan_sha256": plan.sha256,
        "target_assembly_id": surface.target_prototype.assembly_id,
        "collateral_assembly_id": surface.collateral_prototype.assembly_id,
        "response_bearing_execution_performed": False,
        "evidentiary_status": "PREFORMAL_DEVELOPMENT_PREBIND_NO_RESULT",
    }
    binding = PreformalR1Binding(
        schema=PREFORMAL_SCHEMA,
        candidate_id=CANDIDATE_ID,
        analyst_authority=ANALYST_AUTHORITY,
        architecture_r2_head=ARCHITECTURE_R2_HEAD,
        architecture_contract_sha256=contract.sha256,
        development_surface_sha256=surface.sha256,
        checkpoint_sha256=surface.checkpoint_sha256,
        execution_plan_sha256=plan.sha256,
        target_assembly_id=surface.target_prototype.assembly_id,
        collateral_assembly_id=surface.collateral_prototype.assembly_id,
        response_bearing_execution_performed=False,
        evidentiary_status="PREFORMAL_DEVELOPMENT_PREBIND_NO_RESULT",
        sha256=_sha256(payload),
    )
    return brain, contract, surface, plan, binding
