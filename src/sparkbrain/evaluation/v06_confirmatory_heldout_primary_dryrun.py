from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .v06_confirmatory import ConfirmatoryCondition
from .v06_confirmatory_heldout_dryrun_contract import (
    AdapterSafetyDeclaration,
    HeldoutAdapterDryRun,
    build_adapter_dry_run,
)
from .v06_confirmatory_heldout_spec import HeldoutWorldParameters

_PRIMARY_AND_CONTROLS = (
    ConfirmatoryCondition.PRIMARY,
    ConfirmatoryCondition.NO_ENDOGENOUS,
    ConfirmatoryCondition.RANDOM_MATCHED,
    ConfirmatoryCondition.READOUT_ONLY,
    ConfirmatoryCondition.SHUFFLED_RELATION,
)


def _safety() -> AdapterSafetyDeclaration:
    return AdapterSafetyDeclaration(
        reads_primary_runtime_state=False,
        capability_executed=False,
        generated_events_count_as_observations=False,
        generated_events_commit_positive_learning=False,
        normal_field_threshold_present=True,
        threshold_bypassed=False,
        explicit_assembly_entries=0,
        typed_head_count=0,
        scalar_reward_observations=0,
        privileged_information=(),
    )


def _architecture_projection(
    world: HeldoutWorldParameters,
    *,
    route: str,
    endogenous_mode: str,
    relation_mode: str,
) -> dict[str, Any]:
    return {
        "active_unit_ids": list(world.active_unit_ids),
        "alternate_path": list(world.alternate_path),
        "boundary_lag_ms": world.boundary_lag_ms,
        "branch_exposure_counts": list(world.branch_exposure_counts),
        "capability_execution": "disabled",
        "competition_paths": [list(row) for row in world.competition_paths],
        "contingency_cycle_targets": list(world.contingency_cycle_targets),
        "contingency_phase_lengths": list(world.contingency_phase_lengths),
        "control_path": list(world.control_path),
        "control_port": world.control_port,
        "cue_magnitude": world.cue_magnitude,
        "distractor_unit_ids": list(world.distractor_unit_ids),
        "endogenous_mode": endogenous_mode,
        "episode_spacings_ms": list(world.episode_spacings_ms),
        "evaluation_lags_ms": list(world.evaluation_lags_ms),
        "field_threshold": world.threshold,
        "main_path": list(world.main_path),
        "main_port": world.main_port,
        "new_target": world.new_target,
        "normal_field_threshold": "present",
        "old_target": world.old_target,
        "relation_mode": relation_mode,
        "relation_reentry_gain": world.relation_reentry_gain,
        "route": route,
        "third_target": world.third_target,
        "training_lag_profiles_ms": [
            list(row) for row in world.training_lag_profiles_ms
        ],
        "unit_count": world.unit_count,
    }


def _describe(
    world: HeldoutWorldParameters,
    *,
    condition: ConfirmatoryCondition,
    function_name: str,
    route: str,
    endogenous_mode: str,
    relation_mode: str,
) -> HeldoutAdapterDryRun:
    if condition not in _PRIMARY_AND_CONTROLS:
        raise ValueError("unsupported Primary/control held-out dry-run condition")
    return build_adapter_dry_run(
        world,
        condition=condition,
        adapter_path=(
            "sparkbrain.evaluation."
            "v06_confirmatory_heldout_primary_dryrun."
            f"{function_name}"
        ),
        architecture_projection=_architecture_projection(
            world,
            route=route,
            endogenous_mode=endogenous_mode,
            relation_mode=relation_mode,
        ),
        safety=_safety(),
    )


def describe_primary(world: HeldoutWorldParameters) -> HeldoutAdapterDryRun:
    return _describe(
        world,
        condition=ConfirmatoryCondition.PRIMARY,
        function_name="describe_primary",
        route="g0-g1-g2-field",
        endogenous_mode="normal-rule-reinjection",
        relation_mode="learned-anonymous-reentry",
    )


def describe_no_endogenous(
    world: HeldoutWorldParameters,
) -> HeldoutAdapterDryRun:
    return _describe(
        world,
        condition=ConfirmatoryCondition.NO_ENDOGENOUS,
        function_name="describe_no_endogenous",
        route="primary-field-control",
        endogenous_mode="disabled-at-all-depths",
        relation_mode="present-but-not-reentered",
    )


def describe_random_matched(
    world: HeldoutWorldParameters,
) -> HeldoutAdapterDryRun:
    return _describe(
        world,
        condition=ConfirmatoryCondition.RANDOM_MATCHED,
        function_name="describe_random_matched",
        route="matched-random-field-control",
        endogenous_mode="matched-count-time-current-energy",
        relation_mode="no-learned-sequential-lineage",
    )


def describe_readout_only(
    world: HeldoutWorldParameters,
) -> HeldoutAdapterDryRun:
    return _describe(
        world,
        condition=ConfirmatoryCondition.READOUT_ONLY,
        function_name="describe_readout_only",
        route="primary-structural-readout-control",
        endogenous_mode="proposal-only-no-reinjection",
        relation_mode="readout-only",
    )


def describe_shuffled_relation(
    world: HeldoutWorldParameters,
) -> HeldoutAdapterDryRun:
    return _describe(
        world,
        condition=ConfirmatoryCondition.SHUFFLED_RELATION,
        function_name="describe_shuffled_relation",
        route="primary-field-shuffled-relation-control",
        endogenous_mode="normal-rule-reinjection",
        relation_mode="permuted-reentry-target",
    )


PRIMARY_CONTROL_DRY_RUN_ADAPTERS: dict[
    ConfirmatoryCondition,
    Callable[[HeldoutWorldParameters], HeldoutAdapterDryRun],
] = {
    ConfirmatoryCondition.PRIMARY: describe_primary,
    ConfirmatoryCondition.NO_ENDOGENOUS: describe_no_endogenous,
    ConfirmatoryCondition.RANDOM_MATCHED: describe_random_matched,
    ConfirmatoryCondition.READOUT_ONLY: describe_readout_only,
    ConfirmatoryCondition.SHUFFLED_RELATION: describe_shuffled_relation,
}
