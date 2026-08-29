from __future__ import annotations

from collections.abc import Callable
from typing import Any

from sparkbrain.evaluation.v06_confirmatory import ConfirmatoryCondition
from sparkbrain.evaluation.v06_confirmatory_heldout_dryrun_contract import (
    AdapterSafetyDeclaration,
    HeldoutAdapterDryRun,
    build_adapter_dry_run,
)
from sparkbrain.evaluation.v06_confirmatory_heldout_spec import (
    HeldoutWorldParameters,
)
from sparkbrain.evaluation.v06_confirmatory_resources import (
    PrivilegedInformation,
)


def _architecture_projection(
    world: HeldoutWorldParameters,
    *,
    route: str,
    comparator_state: str,
) -> dict[str, Any]:
    return {
        "active_unit_ids": list(world.active_unit_ids),
        "alternate_path": list(world.alternate_path),
        "boundary_lag_ms": world.boundary_lag_ms,
        "branch_exposure_counts": list(world.branch_exposure_counts),
        "capability_execution": "disabled",
        "comparator_state": comparator_state,
        "competition_paths": [list(row) for row in world.competition_paths],
        "contingency_cycle_targets": list(world.contingency_cycle_targets),
        "contingency_phase_lengths": list(world.contingency_phase_lengths),
        "control_path": list(world.control_path),
        "control_port": world.control_port,
        "cue_magnitude": world.cue_magnitude,
        "distractor_unit_ids": list(world.distractor_unit_ids),
        "episode_spacings_ms": list(world.episode_spacings_ms),
        "evaluation_lags_ms": list(world.evaluation_lags_ms),
        "main_path": list(world.main_path),
        "main_port": world.main_port,
        "new_target": world.new_target,
        "normal_field_threshold": "bypassed",
        "old_target": world.old_target,
        "provided_world_threshold": world.threshold,
        "relation_reentry_gain": world.relation_reentry_gain,
        "route": route,
        "third_target": world.third_target,
        "training_lag_profiles_ms": [
            list(row) for row in world.training_lag_profiles_ms
        ],
        "unit_count": world.unit_count,
    }


def describe_g3_recurrent(
    world: HeldoutWorldParameters,
) -> HeldoutAdapterDryRun:
    return build_adapter_dry_run(
        world,
        condition=ConfirmatoryCondition.G3_RECURRENT,
        adapter_path=(
            "sparkbrain.baselines.v06.heldout_dryrun."
            "describe_g3_recurrent"
        ),
        architecture_projection=_architecture_projection(
            world,
            route="generic-autoregressive-transition-comparator",
            comparator_state="untyped-recurrent-transition-state",
        ),
        safety=AdapterSafetyDeclaration(
            reads_primary_runtime_state=False,
            capability_executed=False,
            generated_events_count_as_observations=False,
            generated_events_commit_positive_learning=False,
            normal_field_threshold_present=False,
            threshold_bypassed=True,
            explicit_assembly_entries=0,
            typed_head_count=0,
            scalar_reward_observations=0,
            privileged_information=(),
        ),
    )


def describe_g4_assembly(
    world: HeldoutWorldParameters,
) -> HeldoutAdapterDryRun:
    return build_adapter_dry_run(
        world,
        condition=ConfirmatoryCondition.G4_ASSEMBLY,
        adapter_path=(
            "sparkbrain.baselines.v06.heldout_dryrun."
            "describe_g4_assembly"
        ),
        architecture_projection=_architecture_projection(
            world,
            route="explicit-assembly-conditioned-comparator",
            comparator_state="explicit-assembly-prototype-state",
        ),
        safety=AdapterSafetyDeclaration(
            reads_primary_runtime_state=False,
            capability_executed=False,
            generated_events_count_as_observations=False,
            generated_events_commit_positive_learning=False,
            normal_field_threshold_present=False,
            threshold_bypassed=True,
            explicit_assembly_entries=max(1, len(world.competition_paths)),
            typed_head_count=0,
            scalar_reward_observations=0,
            privileged_information=(
                PrivilegedInformation.EXPLICIT_ASSEMBLY_STATE,
            ),
        ),
    )


def describe_g5_typed(
    world: HeldoutWorldParameters,
) -> HeldoutAdapterDryRun:
    return build_adapter_dry_run(
        world,
        condition=ConfirmatoryCondition.G5_TYPED,
        adapter_path=(
            "sparkbrain.baselines.v06.heldout_dryrun."
            "describe_g5_typed"
        ),
        architecture_projection=_architecture_projection(
            world,
            route="typed-functional-head-comparator",
            comparator_state="typed-prediction-boundary-persistence-heads",
        ),
        safety=AdapterSafetyDeclaration(
            reads_primary_runtime_state=False,
            capability_executed=False,
            generated_events_count_as_observations=False,
            generated_events_commit_positive_learning=False,
            normal_field_threshold_present=False,
            threshold_bypassed=True,
            explicit_assembly_entries=0,
            typed_head_count=3,
            scalar_reward_observations=1,
            privileged_information=(
                PrivilegedInformation.TYPED_PREDICTION_HEAD,
                PrivilegedInformation.TYPED_BOUNDARY_HEAD,
                PrivilegedInformation.TYPED_MEMORY_HEAD,
                PrivilegedInformation.SCALAR_REWARD,
            ),
        ),
    )


COMPARATOR_DRY_RUN_ADAPTERS: dict[
    ConfirmatoryCondition,
    Callable[[HeldoutWorldParameters], HeldoutAdapterDryRun],
] = {
    ConfirmatoryCondition.G3_RECURRENT: describe_g3_recurrent,
    ConfirmatoryCondition.G4_ASSEMBLY: describe_g4_assembly,
    ConfirmatoryCondition.G5_TYPED: describe_g5_typed,
}
