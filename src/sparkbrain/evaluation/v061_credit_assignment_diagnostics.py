from __future__ import annotations

import inspect
from dataclasses import asdict, dataclass, fields
from typing import Any

from sparkbrain.v06.boundary import BoundaryEvent
from sparkbrain.v06.consistency import (
    AnonymousConsistencyResolution,
    AnonymousLinkState,
)
from sparkbrain.v06.foundation import (
    LearningEligibility,
    RuntimePulse,
)

from .v06_confirmatory_heldout_primary import (
    _components,
    _run_cue,
    _world,
)
from .v061_diagnostic_worlds import DiagnosticWorld, lag_factor_worlds


@dataclass(frozen=True, slots=True)
class CreditPathAssessment:
    proposal_to_spark_lineage_present: bool
    spark_to_boundary_proposal_ids_present: bool
    boundary_to_world_parent_id_present: bool
    world_to_consistency_resolution_ids_present: bool
    complete_runtime_lineage_reconstructible: bool
    world_pulse_carries_local_path_ids_directly: bool
    learned_consistency_retains_proposal_ids: bool
    learned_consistency_retains_local_path_ids: bool
    g2_eligibility_exists_for_terminal_path: bool
    g2_eligibility_committed_by_world_consequence: bool
    g2_path_adaptation_updated_by_world_consequence: bool
    direct_g2_resolution_treats_world_consequence_as_match: bool
    automatic_world_to_g2_resolution_present: bool
    anonymous_credit_information_available_transiently: bool
    anonymous_credit_loop_closed_in_learning: bool
    interpretation: str

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


def _world_spec() -> DiagnosticWorld:
    return next(
        world
        for world in lag_factor_worlds()
        if world.family_id == "diagnostic-lag-narrow-shared"
    )


def _proposal_ancestry(runtime, proposal_ids: tuple[str, ...]) -> tuple[str, ...]:
    visited: set[str] = set()
    pending = list(proposal_ids)
    while pending:
        proposal_id = pending.pop()
        if proposal_id in visited:
            continue
        visited.add(proposal_id)
        proposal = runtime.ledger.proposals[proposal_id]
        pending.extend(proposal.parent_proposal_ids)
    return tuple(sorted(visited))


def _run_closed_loop_episode(world: DiagnosticWorld) -> dict[str, Any]:
    runtime, emitter, consistency = _components(world)  # type: ignore[arg-type]
    physical_world = _world(world, world.old_target)  # type: ignore[arg-type]
    result = _run_cue(
        runtime,
        world,  # type: ignore[arg-type]
        cue_unit_id=world.main_path[0],
        start_ms=100.0,
        event_id="diagnostic:credit:main-cue",
        settle_to_horizon=False,
    )
    terminal = next(
        spark for spark in result.runtime.generated_sparks if spark.unit_id == world.main_path[-1]
    )
    boundary = emitter.emit(
        (terminal,),
        source_state_hash=runtime.state_hash(),
    )[0]
    consistency.register_boundary(boundary)
    external = physical_world.receive(boundary)[0]
    runtime.present_external(external)
    resolution = consistency.observe_external(external)

    immediate_proposals = terminal.proposal_ids
    ancestry = _proposal_ancestry(runtime, immediate_proposals)
    path_ids = tuple(
        sorted(
            {
                path_id
                for proposal_id in ancestry
                for path_id in runtime.ledger.proposals[proposal_id].local_path_ids
            }
        )
    )
    terminal_eligibilities = tuple(
        row
        for row in runtime.ledger.eligibilities.values()
        if set(row.path_ids).intersection(path_ids)
    )
    learned_consistency = consistency.learned_state_dict()
    return {
        "runtime": runtime,
        "consistency": consistency,
        "terminal": terminal,
        "boundary": boundary,
        "external": external,
        "resolution": resolution,
        "immediate_proposal_ids": immediate_proposals,
        "proposal_ancestry": ancestry,
        "local_path_ids": path_ids,
        "terminal_eligibilities": terminal_eligibilities,
        "learned_consistency": learned_consistency,
    }


def _direct_g2_probe(world: DiagnosticWorld) -> dict[str, Any]:
    runtime, emitter, _ = _components(world)  # type: ignore[arg-type]
    physical_world = _world(world, world.old_target)  # type: ignore[arg-type]
    result = _run_cue(
        runtime,
        world,  # type: ignore[arg-type]
        cue_unit_id=world.main_path[0],
        start_ms=100.0,
        event_id="diagnostic:credit:g2-probe-cue",
        settle_to_horizon=False,
    )
    terminal = next(
        spark for spark in result.runtime.generated_sparks if spark.unit_id == world.main_path[-1]
    )
    boundary = emitter.emit(
        (terminal,),
        source_state_hash=runtime.state_hash(),
    )[0]
    external = physical_world.receive(boundary)[0]
    proposal_id = terminal.proposal_ids[0]
    proposal = runtime.ledger.proposals[proposal_id]
    pending_before = runtime.transition.pending(proposal_id)
    resolution = runtime.transition.resolve_external(proposal_id, external)
    return {
        "proposal_id": proposal_id,
        "proposal_target": proposal.target,
        "external_target": external.target,
        "path_id": pending_before.path_id,
        "matched": resolution.matched,
        "confidence_before": resolution.confidence_before,
        "confidence_after": resolution.confidence_after,
    }


def _contains_key(value: Any, key: str) -> bool:
    if isinstance(value, dict):
        return key in value or any(_contains_key(item, key) for item in value.values())
    if isinstance(value, (list, tuple)):
        return any(_contains_key(item, key) for item in value)
    return False


def run_credit_assignment_diagnosis() -> dict[str, Any]:
    world = _world_spec()
    episode = _run_closed_loop_episode(world)
    terminal = episode["terminal"]
    boundary: BoundaryEvent = episode["boundary"]
    external: RuntimePulse = episode["external"]
    resolution: AnonymousConsistencyResolution = episode["resolution"]
    eligibilities: tuple[LearningEligibility, ...] = episode[
        "terminal_eligibilities"
    ]
    runtime = episode["runtime"]
    learned_consistency = episode["learned_consistency"]
    g2_probe = _direct_g2_probe(world)

    proposal_to_spark = bool(
        terminal.proposal_ids
        and set(terminal.proposal_ids).issubset(runtime.ledger.proposals)
    )
    spark_to_boundary = (
        boundary.source_spark_id == terminal.spark_id
        and boundary.source_proposal_ids == terminal.proposal_ids
    )
    boundary_to_world = external.parent_event_ids == (boundary.event_id,)
    world_to_resolution = (
        resolution.boundary_event_id == boundary.event_id
        and resolution.external_event_id == external.event_id
    )
    complete_lineage = all(
        (
            proposal_to_spark,
            spark_to_boundary,
            boundary_to_world,
            world_to_resolution,
        )
    )
    eligibility_exists = bool(eligibilities)
    eligibility_committed = any(row.committed for row in eligibilities)
    g2_paths = runtime.transition.state_dict()["paths"]
    path_updated = any(
        path_id in g2_paths for path_id in episode["local_path_ids"]
    )
    automatic_resolution = "resolve_external(" in inspect.getsource(
        runtime.present_external
    )
    learned_has_proposal = _contains_key(learned_consistency, "proposal_id") or (
        _contains_key(learned_consistency, "source_proposal_ids")
    )
    learned_has_path = _contains_key(learned_consistency, "local_path_ids") or (
        _contains_key(learned_consistency, "path_ids")
    )
    transient_available = complete_lineage and bool(episode["local_path_ids"])
    credit_closed = all(
        (
            transient_available,
            eligibility_committed,
            path_updated,
            automatic_resolution,
        )
    )
    assessment = CreditPathAssessment(
        proposal_to_spark_lineage_present=proposal_to_spark,
        spark_to_boundary_proposal_ids_present=spark_to_boundary,
        boundary_to_world_parent_id_present=boundary_to_world,
        world_to_consistency_resolution_ids_present=world_to_resolution,
        complete_runtime_lineage_reconstructible=complete_lineage,
        world_pulse_carries_local_path_ids_directly=bool(external.source_path_ids),
        learned_consistency_retains_proposal_ids=learned_has_proposal,
        learned_consistency_retains_local_path_ids=learned_has_path,
        g2_eligibility_exists_for_terminal_path=eligibility_exists,
        g2_eligibility_committed_by_world_consequence=eligibility_committed,
        g2_path_adaptation_updated_by_world_consequence=path_updated,
        direct_g2_resolution_treats_world_consequence_as_match=bool(
            g2_probe["matched"]
        ),
        automatic_world_to_g2_resolution_present=automatic_resolution,
        anonymous_credit_information_available_transiently=transient_available,
        anonymous_credit_loop_closed_in_learning=credit_closed,
        interpretation=(
            "The causal route from local proposal through actual Spark, boundary "
            "event, world consequence, and consistency resolution is reconstructible "
            "while the runtime and audit objects coexist. The world pulse preserves "
            "its parent boundary ID, and the boundary preserves the terminal proposal "
            "ID. However, persistent consistency state collapses this history into "
            "port-target-polarity statistics and does not retain proposal or local-path "
            "identity. G2 has an uncommitted local eligibility, but the downstream "
            "world consequence is not routed into G2; direct G2 resolution treats it "
            "as a contradiction because its target differs from the local predicted "
            "unit. Anonymous credit information therefore exists transiently but the "
            "world-to-trajectory learning loop is not closed."
        ),
    )
    return {
        "scope": "development-only anonymous credit-assignment continuity audit",
        "candidate_003_executions": 0,
        "world": world.state_dict(),
        "runtime_lineage": {
            "terminal_spark_id": terminal.spark_id,
            "terminal_unit_id": terminal.unit_id,
            "terminal_proposal_ids": terminal.proposal_ids,
            "proposal_ancestry": episode["proposal_ancestry"],
            "local_path_ids": episode["local_path_ids"],
            "boundary_event": boundary.state_dict(),
            "world_external": external.as_dict(),
            "consistency_resolution": resolution.state_dict(),
        },
        "persistence_boundary": {
            "learned_consistency": learned_consistency,
            "terminal_eligibilities": [asdict(row) for row in eligibilities],
            "g2_path_state": g2_paths,
        },
        "direct_g2_probe": g2_probe,
        "schema_fields": {
            "BoundaryEvent": [row.name for row in fields(BoundaryEvent)],
            "RuntimePulse": [row.name for row in fields(RuntimePulse)],
            "AnonymousConsistencyResolution": [
                row.name for row in fields(AnonymousConsistencyResolution)
            ],
            "AnonymousLinkState": [
                row.name for row in fields(AnonymousLinkState)
            ],
            "LearningEligibility": [
                row.name for row in fields(LearningEligibility)
            ],
        },
        "assessment": assessment.state_dict(),
    }
