from __future__ import annotations

from collections.abc import Callable

from .v06_confirmatory import ConfirmatoryCondition
from .v06_confirmatory_heldout_common import HeldoutConditionExecution
from .v06_confirmatory_heldout_comparators import run_condition as run_comparator
from .v06_confirmatory_heldout_controls import run_condition as run_control
from .v06_confirmatory_heldout_primary import run_condition as run_primary
from .v06_confirmatory_heldout_spec import HeldoutWorldParameters

Adapter = Callable[[HeldoutWorldParameters], HeldoutConditionExecution]


def run_primary_v2(world: HeldoutWorldParameters) -> HeldoutConditionExecution:
    return run_primary(world)


def run_no_endogenous_v2(
    world: HeldoutWorldParameters,
) -> HeldoutConditionExecution:
    return run_control(world, ConfirmatoryCondition.NO_ENDOGENOUS)


def run_random_matched_v2(
    world: HeldoutWorldParameters,
) -> HeldoutConditionExecution:
    return run_control(world, ConfirmatoryCondition.RANDOM_MATCHED)


def run_readout_only_v2(
    world: HeldoutWorldParameters,
) -> HeldoutConditionExecution:
    return run_control(world, ConfirmatoryCondition.READOUT_ONLY)


def run_shuffled_relation_v2(
    world: HeldoutWorldParameters,
) -> HeldoutConditionExecution:
    return run_control(world, ConfirmatoryCondition.SHUFFLED_RELATION)


def run_g3_recurrent_v2(
    world: HeldoutWorldParameters,
) -> HeldoutConditionExecution:
    return run_comparator(world, ConfirmatoryCondition.G3_RECURRENT)


def run_g4_assembly_v2(
    world: HeldoutWorldParameters,
) -> HeldoutConditionExecution:
    return run_comparator(world, ConfirmatoryCondition.G4_ASSEMBLY)


def run_g5_typed_v2(
    world: HeldoutWorldParameters,
) -> HeldoutConditionExecution:
    return run_comparator(world, ConfirmatoryCondition.G5_TYPED)


ADAPTERS_V2: dict[ConfirmatoryCondition, Adapter] = {
    ConfirmatoryCondition.PRIMARY: run_primary_v2,
    ConfirmatoryCondition.NO_ENDOGENOUS: run_no_endogenous_v2,
    ConfirmatoryCondition.RANDOM_MATCHED: run_random_matched_v2,
    ConfirmatoryCondition.READOUT_ONLY: run_readout_only_v2,
    ConfirmatoryCondition.SHUFFLED_RELATION: run_shuffled_relation_v2,
    ConfirmatoryCondition.G3_RECURRENT: run_g3_recurrent_v2,
    ConfirmatoryCondition.G4_ASSEMBLY: run_g4_assembly_v2,
    ConfirmatoryCondition.G5_TYPED: run_g5_typed_v2,
}

ADAPTER_PATHS_V2: dict[ConfirmatoryCondition, str] = {
    condition: f"{adapter.__module__}.{adapter.__name__}"
    for condition, adapter in ADAPTERS_V2.items()
}


def validate_adapter_registry_v2() -> None:
    if set(ADAPTERS_V2) != set(ConfirmatoryCondition):
        raise RuntimeError("v2 adapter registry does not cover every condition")
    if set(ADAPTER_PATHS_V2) != set(ConfirmatoryCondition):
        raise RuntimeError("v2 adapter path registry does not cover every condition")
    if len({id(adapter) for adapter in ADAPTERS_V2.values()}) != len(ADAPTERS_V2):
        raise RuntimeError("v2 adapter registry contains duplicate callable identities")
    if len(set(ADAPTER_PATHS_V2.values())) != len(ADAPTER_PATHS_V2):
        raise RuntimeError("v2 adapter path registry contains duplicate entrypoints")
    for condition, adapter in ADAPTERS_V2.items():
        expected = f"{adapter.__module__}.{adapter.__name__}"
        if ADAPTER_PATHS_V2[condition] != expected:
            raise RuntimeError("v2 adapter path differs from executed callable")


def run_registered_adapter_v2(
    world: HeldoutWorldParameters,
    condition: ConfirmatoryCondition,
) -> HeldoutConditionExecution:
    validate_adapter_registry_v2()
    execution = ADAPTERS_V2[condition](world)
    execution.validate()
    if execution.condition is not condition:
        raise RuntimeError("adapter execution returned the wrong condition identity")
    if execution.family_id != world.family_id or execution.seed != world.seed:
        raise RuntimeError("adapter execution returned the wrong world identity")
    if execution.world_specification_hash != world.specification_hash():
        raise RuntimeError("adapter execution returned the wrong world hash")
    return execution
