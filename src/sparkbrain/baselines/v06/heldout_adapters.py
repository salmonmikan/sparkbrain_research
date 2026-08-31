from __future__ import annotations

from sparkbrain.evaluation.v06_confirmatory import ConfirmatoryCondition
from sparkbrain.evaluation.v06_confirmatory_heldout_common import (
    HeldoutConditionExecution,
)
from sparkbrain.evaluation.v06_confirmatory_heldout_comparators import (
    run_condition,
)
from sparkbrain.evaluation.v06_confirmatory_heldout_spec import (
    HeldoutWorldParameters,
)


def run_g3(parameters: HeldoutWorldParameters) -> HeldoutConditionExecution:
    return run_condition(parameters, ConfirmatoryCondition.G3_RECURRENT)


def run_g4(parameters: HeldoutWorldParameters) -> HeldoutConditionExecution:
    return run_condition(parameters, ConfirmatoryCondition.G4_ASSEMBLY)


def run_g5(parameters: HeldoutWorldParameters) -> HeldoutConditionExecution:
    return run_condition(parameters, ConfirmatoryCondition.G5_TYPED)
