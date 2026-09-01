from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v06.foundation import digest

from .v06_confirmatory import ConfirmatoryCondition
from .v06_confirmatory_heldout_comparators import (
    _FACADE_FACTORIES,
    _context,
    _train_paths,
)
from .v06_confirmatory_heldout_primary import (
    _chain_paths,
    _train_expectation,
)
from .v061_diagnostic_worlds import DiagnosticWorld, lag_factor_worlds
from .v061_lag_diagnostics import diagnose_lag_world

_COMPARATORS = (
    ConfirmatoryCondition.G3_RECURRENT,
    ConfirmatoryCondition.G4_ASSEMBLY,
    ConfirmatoryCondition.G5_TYPED,
)


@dataclass(frozen=True, slots=True)
class ComparatorTemporalContrast:
    condition: str
    world_a_state_hash: str
    world_b_state_hash: str
    learned_state_equal: bool
    world_a_output: tuple[int, ...]
    world_b_output: tuple[int, ...]
    output_equal: bool
    lag_profile_values_represented_in_learned_state: bool
    privileged_structure: tuple[str, ...]

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class PrimaryTemporalContrast:
    world_a_state_hash: str
    world_b_state_hash: str
    learned_state_equal: bool
    world_a_trajectory_class: str
    world_b_trajectory_class: str
    trajectory_equal: bool
    world_a_main_current_ratio: float
    world_b_main_current_ratio: float
    world_a_alternate_current_ratio: float
    world_b_alternate_current_ratio: float

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


def _world_pair() -> tuple[DiagnosticWorld, DiagnosticWorld]:
    worlds = {world.family_id: world for world in lag_factor_worlds()}
    return (
        worlds["diagnostic-lag-profile-rotation-0"],
        worlds["diagnostic-lag-profile-rotation-1"],
    )


def _privileges(condition: ConfirmatoryCondition) -> tuple[str, ...]:
    if condition is ConfirmatoryCondition.G3_RECURRENT:
        return ("explicit-transition-state", "time-abstracted-sequence")
    if condition is ConfirmatoryCondition.G4_ASSEMBLY:
        return (
            "explicit-assembly-state",
            "explicit-trajectory-identity",
            "time-abstracted-sequence",
        )
    if condition is ConfirmatoryCondition.G5_TYPED:
        return (
            "typed-prediction-head",
            "typed-boundary-head",
            "typed-memory-head",
            "scalar-reward",
            "time-abstracted-sequence",
        )
    raise ValueError(f"unsupported comparator: {condition.value}")


def _comparator_contrast(
    condition: ConfirmatoryCondition,
    world_a: DiagnosticWorld,
    world_b: DiagnosticWorld,
) -> ComparatorTemporalContrast:
    factory = _FACADE_FACTORIES[condition]
    paths_a = _chain_paths(world_a)  # type: ignore[arg-type]
    paths_b = _chain_paths(world_b)  # type: ignore[arg-type]
    if paths_a != paths_b:
        raise ValueError("temporal contrast requires identical anonymous paths")
    if world_a.branch_exposure_counts != world_b.branch_exposure_counts:
        raise ValueError("temporal contrast requires identical exposure counts")

    model_a = factory.create()
    model_b = factory.create()
    _train_paths(model_a, world_a, paths_a)  # type: ignore[arg-type]
    _train_paths(model_b, world_b, paths_b)  # type: ignore[arg-type]
    state_a = model_a.learned_state_dict()
    state_b = model_b.learned_state_dict()
    context = _context("sequence", world_a.main_path)
    output_a = model_a.rollout(context, world_a.main_path[0])
    output_b = model_b.rollout(context, world_b.main_path[0])
    equal = state_a == state_b
    return ComparatorTemporalContrast(
        condition=condition.value,
        world_a_state_hash=digest(state_a),
        world_b_state_hash=digest(state_b),
        learned_state_equal=equal,
        world_a_output=output_a,
        world_b_output=output_b,
        output_equal=output_a == output_b,
        lag_profile_values_represented_in_learned_state=not equal,
        privileged_structure=_privileges(condition),
    )


def _candidate_ratio(diagnosis, branch: str) -> float:
    return next(
        row.current_threshold_ratio
        for row in diagnosis.root_candidates
        if row.branch == branch
    )


def _primary_contrast(
    world_a: DiagnosticWorld,
    world_b: DiagnosticWorld,
) -> PrimaryTemporalContrast:
    expectation_a = _train_expectation(  # type: ignore[arg-type]
        world_a,
        _chain_paths(world_a),  # type: ignore[arg-type]
    )
    expectation_b = _train_expectation(  # type: ignore[arg-type]
        world_b,
        _chain_paths(world_b),  # type: ignore[arg-type]
    )
    state_a = expectation_a.learned_state_dict()
    state_b = expectation_b.learned_state_dict()
    diagnosis_a = diagnose_lag_world(world_a)
    diagnosis_b = diagnose_lag_world(world_b)
    return PrimaryTemporalContrast(
        world_a_state_hash=digest(state_a),
        world_b_state_hash=digest(state_b),
        learned_state_equal=state_a == state_b,
        world_a_trajectory_class=diagnosis_a.sham.trajectory_class,
        world_b_trajectory_class=diagnosis_b.sham.trajectory_class,
        trajectory_equal=(
            diagnosis_a.sham.generated_units == diagnosis_b.sham.generated_units
        ),
        world_a_main_current_ratio=_candidate_ratio(diagnosis_a, "main"),
        world_b_main_current_ratio=_candidate_ratio(diagnosis_b, "main"),
        world_a_alternate_current_ratio=_candidate_ratio(diagnosis_a, "alternate"),
        world_b_alternate_current_ratio=_candidate_ratio(diagnosis_b, "alternate"),
    )


def run_comparator_contrast() -> dict[str, Any]:
    world_a, world_b = _world_pair()
    comparators = tuple(
        _comparator_contrast(condition, world_a, world_b)
        for condition in _COMPARATORS
    )
    primary = _primary_contrast(world_a, world_b)
    comparator_time_quotient = all(
        row.learned_state_equal and row.output_equal for row in comparators
    )
    primary_time_sensitive = (
        not primary.learned_state_equal and not primary.trajectory_equal
    )
    return {
        "scope": "development-only temporal abstraction contrast",
        "candidate_003_executions": 0,
        "world_a": world_a.state_dict(),
        "world_b": world_b.state_dict(),
        "same_paths": _chain_paths(world_a) == _chain_paths(world_b),  # type: ignore[arg-type]
        "same_exposure_counts": (
            world_a.branch_exposure_counts == world_b.branch_exposure_counts
        ),
        "same_lag_profile_multiset": (
            sorted(world_a.training_lag_profiles_ms)
            == sorted(world_b.training_lag_profiles_ms)
        ),
        "lag_profile_order_equal": (
            world_a.training_lag_profiles_ms == world_b.training_lag_profiles_ms
        ),
        "primary": primary.state_dict(),
        "comparators": [row.state_dict() for row in comparators],
        "all_comparators_quotient_lag_order": comparator_time_quotient,
        "primary_retains_lag_order_in_state_and_expression": primary_time_sensitive,
        "interpretation": (
            "G3/G4/G5 produce identical learned sequence state and output when only "
            "the chronological lag-profile order changes. Primary G1 retains temporal "
            "moments and changes trajectory expression. Comparator success therefore "
            "shows that the tested task can be solved after quotienting out time; it "
            "does not demonstrate superior processing of the same temporal Dynamics."
        ),
    }
