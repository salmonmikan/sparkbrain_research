from __future__ import annotations

from collections.abc import Callable

from sparkbrain.baselines.v06.heldout_adapters import run_g3, run_g4, run_g5

from .v06_confirmatory import ConfirmatoryCondition
from .v06_confirmatory_heldout_common import HeldoutConditionExecution
from .v06_confirmatory_heldout_controls import (
    run_no_endogenous,
    run_random_matched,
    run_readout_only,
    run_shuffled_relation,
)
from .v06_confirmatory_heldout_primary import run_condition as run_primary
from .v06_confirmatory_heldout_spec import HeldoutWorldParameters

AdapterCallable = Callable[[HeldoutWorldParameters], HeldoutConditionExecution]

REAL_ADAPTERS: dict[ConfirmatoryCondition, AdapterCallable] = {
    ConfirmatoryCondition.PRIMARY: run_primary,
    ConfirmatoryCondition.NO_ENDOGENOUS: run_no_endogenous,
    ConfirmatoryCondition.RANDOM_MATCHED: run_random_matched,
    ConfirmatoryCondition.READOUT_ONLY: run_readout_only,
    ConfirmatoryCondition.SHUFFLED_RELATION: run_shuffled_relation,
    ConfirmatoryCondition.G3_RECURRENT: run_g3,
    ConfirmatoryCondition.G4_ASSEMBLY: run_g4,
    ConfirmatoryCondition.G5_TYPED: run_g5,
}

ADAPTER_PATHS: dict[ConfirmatoryCondition, str] = {
    ConfirmatoryCondition.PRIMARY: (
        "sparkbrain.evaluation.v06_confirmatory_heldout_primary.run_condition"
    ),
    ConfirmatoryCondition.NO_ENDOGENOUS: (
        "sparkbrain.evaluation.v06_confirmatory_heldout_controls.run_no_endogenous"
    ),
    ConfirmatoryCondition.RANDOM_MATCHED: (
        "sparkbrain.evaluation.v06_confirmatory_heldout_controls.run_random_matched"
    ),
    ConfirmatoryCondition.READOUT_ONLY: (
        "sparkbrain.evaluation.v06_confirmatory_heldout_controls.run_readout_only"
    ),
    ConfirmatoryCondition.SHUFFLED_RELATION: (
        "sparkbrain.evaluation.v06_confirmatory_heldout_controls.run_shuffled_relation"
    ),
    ConfirmatoryCondition.G3_RECURRENT: (
        "sparkbrain.baselines.v06.heldout_adapters.run_g3"
    ),
    ConfirmatoryCondition.G4_ASSEMBLY: (
        "sparkbrain.baselines.v06.heldout_adapters.run_g4"
    ),
    ConfirmatoryCondition.G5_TYPED: (
        "sparkbrain.baselines.v06.heldout_adapters.run_g5"
    ),
}


def validate_adapter_registry() -> None:
    if set(REAL_ADAPTERS) != set(ConfirmatoryCondition):
        raise RuntimeError("real adapter registry is incomplete")
    if set(ADAPTER_PATHS) != set(ConfirmatoryCondition):
        raise RuntimeError("adapter path registry is incomplete")
    if len(set(ADAPTER_PATHS.values())) != len(ADAPTER_PATHS):
        raise RuntimeError("adapter paths must be unique")
    for condition in (
        ConfirmatoryCondition.G3_RECURRENT,
        ConfirmatoryCondition.G4_ASSEMBLY,
        ConfirmatoryCondition.G5_TYPED,
    ):
        if not ADAPTER_PATHS[condition].startswith("sparkbrain.baselines.v06."):
            raise RuntimeError("comparator adapter must remain under baselines")


def run_registered_condition(
    parameters: HeldoutWorldParameters,
    condition: ConfirmatoryCondition,
) -> HeldoutConditionExecution:
    validate_adapter_registry()
    return REAL_ADAPTERS[condition](parameters)
