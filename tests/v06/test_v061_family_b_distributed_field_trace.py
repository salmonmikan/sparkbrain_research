from __future__ import annotations

import math
import re
from collections.abc import Callable

import pytest

from sparkbrain.evaluation.v061_family_b_distributed_field_trace import (
    DistributedFieldTraceState,
)


def _with_left_activity() -> DistributedFieldTraceState:
    return DistributedFieldTraceState.zeros().deposit_local_activity(
        (1.0, 0.0, 0.0, 0.0)
    )


def test_external_return_is_required_for_credit_update() -> None:
    state = _with_left_activity()

    replayed = state.internal_replay()
    returned = state.apply_external_world_return(
        (1.0, 0.0, 0.0, 0.0),
        sign=1,
    )

    assert replayed.credit == (0.0, 0.0, 0.0, 0.0)
    assert returned.credit == (1.0, 0.0, 0.0, 0.0)


def test_anonymous_lineage_swap_follows_physical_field_footprint() -> None:
    left = _with_left_activity()
    right = DistributedFieldTraceState.zeros().deposit_local_activity(
        (0.0, 1.0, 0.0, 0.0)
    )

    left_returned = left.apply_external_world_return(
        (1.0, 0.0, 0.0, 0.0),
        sign=1,
    )
    right_returned = right.apply_external_world_return(
        (0.0, 1.0, 0.0, 0.0),
        sign=1,
    )

    assert left_returned.competition_score((1.0, 0.0, 0.0, 0.0)) == 1.0
    assert left_returned.competition_score((0.0, 1.0, 0.0, 0.0)) == 0.0
    assert right_returned.competition_score((1.0, 0.0, 0.0, 0.0)) == 0.0
    assert right_returned.competition_score((0.0, 1.0, 0.0, 0.0)) == 1.0


def test_contradiction_reverses_local_credit_sign() -> None:
    state = _with_left_activity()
    confirmed = state.apply_external_world_return(
        (1.0, 0.0, 0.0, 0.0),
        sign=1,
    )
    contradicted = confirmed.apply_external_world_return(
        (1.0, 0.0, 0.0, 0.0),
        sign=-1,
    )

    assert confirmed.competition_score((1.0, 0.0, 0.0, 0.0)) == 1.0
    assert contradicted.competition_score((1.0, 0.0, 0.0, 0.0)) == 0.0


def test_f_only_carrier_transplant_preserves_functional_score() -> None:
    donor = DistributedFieldTraceState.zeros().deposit_local_activity(
        (0.0, 1.0, 0.0, 0.0)
    )
    donor = donor.apply_external_world_return(
        (0.0, 1.0, 0.0, 0.0),
        sign=1,
    )

    transplanted = DistributedFieldTraceState.from_field_carrier(
        donor.export_field_carrier()
    )

    probe = (0.0, 1.0, 0.0, 0.0)
    assert transplanted.competition_score(probe) == donor.competition_score(probe) == 1.0


def test_bounded_plurality_can_hold_two_footprints_then_differentiate_by_overlap() -> None:
    state = DistributedFieldTraceState.zeros().deposit_local_activity(
        (1.0, 1.0, 0.0, 0.0)
    )

    left_evidence = state.apply_external_world_return(
        (1.0, 0.0, 0.0, 0.0),
        sign=1,
    )
    right_evidence = state.apply_external_world_return(
        (0.0, 1.0, 0.0, 0.0),
        sign=1,
    )

    assert left_evidence.eligibility[:2] == (1.0, 1.0)
    assert right_evidence.eligibility[:2] == (1.0, 1.0)
    assert left_evidence.credit[:2] == (1.0, 0.0)
    assert right_evidence.credit[:2] == (0.0, 1.0)


def test_eligibility_decays_before_new_local_activity_is_added() -> None:
    state = DistributedFieldTraceState.zeros(decay=0.5)
    state = state.deposit_local_activity((1.0, 0.0, 0.0, 0.0))
    state = state.deposit_local_activity((0.0, 0.0, 0.0, 0.0))

    assert state.eligibility == (0.5, 0.0, 0.0, 0.0)


def test_competition_score_rejects_arithmetic_overflow() -> None:
    state = DistributedFieldTraceState(
        eligibility=(0.0, 0.0, 0.0, 0.0),
        credit=(1e308, 0.0, 0.0, 0.0),
    )

    with pytest.raises(ValueError, match="competition score must be finite"):
        state.competition_score((1e308, 0.0, 0.0, 0.0))


@pytest.mark.parametrize(
    ("operation", "expected_message"),
    [
        (
            lambda: DistributedFieldTraceState.zeros(width=0),
            "width must be positive",
        ),
        (
            lambda: DistributedFieldTraceState.zeros(decay=1.0),
            "decay must be finite and in [0, 1)",
        ),
        (
            lambda: DistributedFieldTraceState.zeros().deposit_local_activity((1.0,)),
            "vector width mismatch",
        ),
        (
            lambda: DistributedFieldTraceState.zeros().deposit_local_activity(
                (math.inf, 0.0, 0.0, 0.0)
            ),
            "vector values must be finite",
        ),
        (
            lambda: DistributedFieldTraceState.zeros().apply_external_world_return(
                (1.0, 0.0, 0.0, 0.0),
                sign=0,
            ),
            "external world-return sign must be -1 or +1",
        ),
        (
            lambda: DistributedFieldTraceState(
                eligibility=(1e308, 0.0, 0.0, 0.0),
                credit=(0.0, 0.0, 0.0, 0.0),
            ).apply_external_world_return(
                (1e308, 0.0, 0.0, 0.0),
                sign=1,
            ),
            "vector values must be finite",
        ),
    ],
)
def test_invalid_carrier_inputs_fail_closed(
    operation: Callable[[], object],
    expected_message: str,
) -> None:
    with pytest.raises(ValueError, match=re.escape(expected_message)):
        operation()
