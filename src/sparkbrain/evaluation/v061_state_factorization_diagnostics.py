from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from typing import Any

from sparkbrain.v06.foundation import digest
from sparkbrain.v06.local_expectation import LocalTemporalExpectation

from .v06_confirmatory_heldout_primary import (
    _chain_paths,
    _field,
    _relation_cycles,
    _run_reentry,
    _train_expectation,
)
from .v061_diagnostic_worlds import DiagnosticWorld, lag_factor_worlds
from .v061_failure_locus_diagnostics import (
    _run_main_cue,
    _runtime_from_components,
    _trajectory_class,
)


@dataclass(frozen=True, slots=True)
class StateFactorizationCell:
    transition_label: str
    consistency_label: str
    transition_state_hash: str
    consistency_state_hash: str
    trajectory_units: tuple[int, ...]
    trajectory_class: str
    relation_reentry_units: tuple[int, ...]

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class StateFactorizationAssessment:
    transition_states_distinct: bool
    consistency_states_distinct: bool
    transition_changes_trajectory: bool
    consistency_changes_relation_expression: bool
    trajectory_invariant_under_consistency_swap: bool
    relation_expression_invariant_under_transition_swap: bool
    full_cartesian_factorization: bool
    missing_consistency_to_trajectory_edge_supported: bool
    interpretation: str

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


def _worlds() -> tuple[DiagnosticWorld, DiagnosticWorld, DiagnosticWorld]:
    worlds = {world.family_id: world for world in lag_factor_worlds()}
    return (
        worlds["diagnostic-lag-profile-rotation-0"],
        worlds["diagnostic-lag-profile-rotation-1"],
        worlds["diagnostic-lag-narrow-shared"],
    )


def _single_relation_world(
    base: DiagnosticWorld,
    *,
    target: int,
    label: str,
    seed: int,
) -> DiagnosticWorld:
    world = replace(
        base,
        family_id=f"diagnostic-factorization-relation-{label}",
        seed=seed,
        structural_token=(
            f"development-only:diagnostic:factorization-relation-{label}:{seed}"
        ),
        contingency_cycle_targets=(target,),
        contingency_phase_lengths=(6,),
        factor_name="anonymous-relation-target",
        factor_value=label,
    )
    world.validate()
    return world


def _transition_state(world: DiagnosticWorld) -> dict[str, Any]:
    expectation = _train_expectation(  # type: ignore[arg-type]
        world,
        _chain_paths(world),  # type: ignore[arg-type]
    )
    return expectation.learned_state_dict()


def _consistency_state(world: DiagnosticWorld) -> dict[str, Any]:
    relation = _relation_cycles(world)  # type: ignore[arg-type]
    if len(relation.snapshots) != 1:
        raise RuntimeError("factorization relation world must emit one snapshot")
    return relation.snapshots[0]


def _trajectory_output(
    execution_world: DiagnosticWorld,
    transition_state: dict[str, Any],
    *,
    event_id: str,
) -> tuple[int, ...]:
    expectation = LocalTemporalExpectation.from_learned_state_dict(
        transition_state
    )
    runtime = _runtime_from_components(
        execution_world,
        _field(execution_world),  # type: ignore[arg-type]
        expectation,
    )
    return _run_main_cue(
        execution_world,
        runtime,
        start_ms=100.0,
        event_id=event_id,
    )


def _cell(
    execution_world: DiagnosticWorld,
    *,
    transition_label: str,
    transition_state: dict[str, Any],
    consistency_label: str,
    consistency_state: dict[str, Any],
) -> StateFactorizationCell:
    trajectory = _trajectory_output(
        execution_world,
        transition_state,
        event_id=(
            f"diagnostic:factorization:trajectory:{transition_label}:"
            f"{consistency_label}"
        ),
    )
    reentry = _run_reentry(  # type: ignore[arg-type]
        execution_world,
        consistency_state,
        event_id=(
            f"diagnostic:factorization:reentry:{transition_label}:"
            f"{consistency_label}"
        ),
    )
    return StateFactorizationCell(
        transition_label=transition_label,
        consistency_label=consistency_label,
        transition_state_hash=digest(transition_state),
        consistency_state_hash=digest(consistency_state),
        trajectory_units=trajectory,
        trajectory_class=_trajectory_class(execution_world, trajectory),
        relation_reentry_units=reentry,
    )


def run_state_factorization_diagnosis() -> dict[str, Any]:
    alternate_world, main_world, execution_world = _worlds()
    transition_states = {
        "alternate-favoring": _transition_state(alternate_world),
        "main-favoring": _transition_state(main_world),
    }
    old_world = _single_relation_world(
        execution_world,
        target=execution_world.old_target,
        label="old-target",
        seed=932_000,
    )
    new_world = _single_relation_world(
        execution_world,
        target=execution_world.new_target,
        label="new-target",
        seed=932_001,
    )
    consistency_states = {
        "old-target": _consistency_state(old_world),
        "new-target": _consistency_state(new_world),
    }
    cells = tuple(
        _cell(
            execution_world,
            transition_label=transition_label,
            transition_state=transition_state,
            consistency_label=consistency_label,
            consistency_state=consistency_state,
        )
        for transition_label, transition_state in transition_states.items()
        for consistency_label, consistency_state in consistency_states.items()
    )
    by_key = {
        (cell.transition_label, cell.consistency_label): cell for cell in cells
    }
    alternate_old = by_key[("alternate-favoring", "old-target")]
    alternate_new = by_key[("alternate-favoring", "new-target")]
    main_old = by_key[("main-favoring", "old-target")]
    main_new = by_key[("main-favoring", "new-target")]

    transition_distinct = (
        alternate_old.transition_state_hash != main_old.transition_state_hash
    )
    consistency_distinct = (
        alternate_old.consistency_state_hash != alternate_new.consistency_state_hash
    )
    transition_changes = (
        alternate_old.trajectory_units != main_old.trajectory_units
    )
    consistency_changes = (
        alternate_old.relation_reentry_units
        != alternate_new.relation_reentry_units
    )
    trajectory_invariant = (
        alternate_old.trajectory_units == alternate_new.trajectory_units
        and main_old.trajectory_units == main_new.trajectory_units
    )
    relation_invariant = (
        alternate_old.relation_reentry_units == main_old.relation_reentry_units
        and alternate_new.relation_reentry_units == main_new.relation_reentry_units
    )
    factorized = all(
        (
            transition_distinct,
            consistency_distinct,
            transition_changes,
            consistency_changes,
            trajectory_invariant,
            relation_invariant,
        )
    )
    assessment = StateFactorizationAssessment(
        transition_states_distinct=transition_distinct,
        consistency_states_distinct=consistency_distinct,
        transition_changes_trajectory=transition_changes,
        consistency_changes_relation_expression=consistency_changes,
        trajectory_invariant_under_consistency_swap=trajectory_invariant,
        relation_expression_invariant_under_transition_swap=relation_invariant,
        full_cartesian_factorization=factorized,
        missing_consistency_to_trajectory_edge_supported=factorized,
        interpretation=(
            "Under the development-only 2x2 transplant, G1 transition state alone "
            "selects the anonymous trajectory and consistency state alone selects "
            "relation re-entry. Swapping consistency does not alter trajectory "
            "competition, and swapping G1 does not alter relation expression. The "
            "current implementation therefore behaves as two explicit anonymous "
            "state systems coupled only through later Field expression, with no "
            "observed world-consistency-to-G1 competition edge."
        ),
    )
    return {
        "scope": "development-only G1 x consistency causal factorization",
        "candidate_003_executions": 0,
        "execution_world": execution_world.state_dict(),
        "transition_source_worlds": {
            "alternate-favoring": alternate_world.state_dict(),
            "main-favoring": main_world.state_dict(),
        },
        "relation_source_worlds": {
            "old-target": old_world.state_dict(),
            "new-target": new_world.state_dict(),
        },
        "cells": [cell.state_dict() for cell in cells],
        "assessment": assessment.state_dict(),
    }
