from __future__ import annotations

from sparkbrain.evaluation.v06_confirmatory import ConfirmatoryCondition
from sparkbrain.evaluation.v06_confirmatory_heldout_common import (
    HeldoutConditionExecution,
)
from sparkbrain.evaluation.v06_confirmatory_heldout_comparators import (
    run_condition as _run_comparator,
)
from sparkbrain.evaluation.v06_confirmatory_heldout_spec import (
    HeldoutWorldParameters,
)


def run_g3_recurrent_candidate(
    world: HeldoutWorldParameters,
) -> HeldoutConditionExecution:
    """Execute the isolated G3 comparator for one frozen candidate world."""

    return _run_comparator(world, ConfirmatoryCondition.G3_RECURRENT)


def run_g4_assembly_candidate(
    world: HeldoutWorldParameters,
) -> HeldoutConditionExecution:
    """Execute the explicit-Assembly comparator for one frozen candidate world."""

    return _run_comparator(world, ConfirmatoryCondition.G4_ASSEMBLY)


def run_g5_typed_candidate(
    world: HeldoutWorldParameters,
) -> HeldoutConditionExecution:
    """Execute the typed-head comparator for one frozen candidate world."""

    return _run_comparator(world, ConfirmatoryCondition.G5_TYPED)
