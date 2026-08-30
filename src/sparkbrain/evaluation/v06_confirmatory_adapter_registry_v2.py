from __future__ import annotations

from collections.abc import Callable

from .v06_confirmatory import ConfirmatoryCondition
from .v06_confirmatory_heldout_common import HeldoutConditionExecution
from .v06_confirmatory_heldout_comparators import run_condition as run_comparator
from .v06_confirmatory_heldout_controls import run_condition as run_control
from .v06_confirmatory_heldout_primary import run_condition as run_primary
from .v06_confirmatory_heldout_spec import HeldoutWorldParameters

Adapter = Callable[[HeldoutWorldParameters], HeldoutConditionExecution]


def _primary(world: HeldoutWorldParameters) -> HeldoutConditionExecution:
    return run_primary(world)


def _control(condition: ConfirmatoryCondition) -> Adapter:
    return lambda world: run_control(world, condition)


def _comparator(condition: ConfirmatoryCondition) -> Adapter:
    return lambda world: run_comparator(world, condition)


ADAPTERS_V2: dict[ConfirmatoryCondition, Adapter] = {
    ConfirmatoryCondition.PRIMARY: _primary,
    ConfirmatoryCondition.NO_ENDOGENOUS: _control(
        ConfirmatoryCondition.NO_ENDOGENOUS
    ),
    ConfirmatoryCondition.RANDOM_MATCHED: _control(
        ConfirmatoryCondition.RANDOM_MATCHED
    ),
    ConfirmatoryCondition.READOUT_ONLY: _control(
        ConfirmatoryCondition.READOUT_ONLY
    ),
    ConfirmatoryCondition.SHUFFLED_RELATION: _control(
        ConfirmatoryCondition.SHUFFLED_RELATION
    ),
    ConfirmatoryCondition.G3_RECURRENT: _comparator(
        ConfirmatoryCondition.G3_RECURRENT
    ),
    ConfirmatoryCondition.G4_ASSEMBLY: _comparator(
        ConfirmatoryCondition.G4_ASSEMBLY
    ),
    ConfirmatoryCondition.G5_TYPED: _comparator(ConfirmatoryCondition.G5_TYPED),
}


def validate_adapter_registry_v2() -> None:
    if set(ADAPTERS_V2) != set(ConfirmatoryCondition):
        raise RuntimeError("v2 adapter registry does not cover every condition")
    if len({id(adapter) for adapter in ADAPTERS_V2.values()}) != len(ADAPTERS_V2):
        raise RuntimeError("v2 adapter registry contains duplicate callable identities")


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
