from __future__ import annotations

import math
import re
from collections.abc import Callable

import pytest

from sparkbrain.evaluation.v061_family_b_distributed_field_trace import (
    DistributedFieldTraceState,
    ExternalEvidenceLedger,
)


def _with_left_activity() -> DistributedFieldTraceState:
    return DistributedFieldTraceState.zeros().deposit_local_activity(
        (1.0, 0.0, 0.0, 0.0)
    )


def test_external_return_is_required_for_credit_update() -> None:
    state = _with_left_activity()
    ledger = ExternalEvidenceLedger()

    replayed = state.internal_replay()
    returned = state.apply_external_world_return(
        (1.0, 0.0, 0.0, 0.0),
        sign=1,
        evidence_id="ev:left:confirm",
        evidence_ledger=ledger,
    )

    assert replayed.credit == (0.0, 0.0, 0.0, 0.0)
    assert returned.credit == (0.5, 0.0, 0.0, 0.0)


def test_duplicate_external_evidence_id_is_rejected_without_second_credit() -> None:
    state = _with_left_activity()
    ledger = ExternalEvidenceLedger()
    returned = state.apply_external_world_return(
        (1.0, 0.0, 0.0, 0.0),
        sign=1,
        evidence_id="ev:duplicate",
        evidence_ledger=ledger,
    )

    with pytest.raises(ValueError, match="external evidence ID already consumed"):
        returned.apply_external_world_return(
            (1.0, 0.0, 0.0, 0.0),
            sign=1,
            evidence_id="ev:duplicate",
            evidence_ledger=ledger,
        )

    assert returned.credit == (0.5, 0.0, 0.0, 0.0)
    assert ledger.consumed_ids == frozenset({"ev:duplicate"})


def test_consumed_evidence_ids_round_trip_across_ledger_recreation() -> None:
    state = _with_left_activity()
    ledger = ExternalEvidenceLedger()
    returned = state.apply_external_world_return(
        (1.0, 0.0, 0.0, 0.0),
        sign=1,
        evidence_id="ev:checkpoint",
        evidence_ledger=ledger,
    )

    checkpoint = ledger.export_consumed_ids()
    restored = ExternalEvidenceLedger.from_consumed_ids(checkpoint)

    assert checkpoint == ("ev:checkpoint",)
    assert restored.export_consumed_ids() == checkpoint
    with pytest.raises(ValueError, match="external evidence ID already consumed"):
        returned.apply_external_world_return(
            (1.0, 0.0, 0.0, 0.0),
            sign=1,
            evidence_id="ev:checkpoint",
            evidence_ledger=restored,
        )
    assert returned.credit == (0.5, 0.0, 0.0, 0.0)


def test_anonymous_lineage_swap_follows_physical_field_footprint() -> None:
    left = _with_left_activity()
    right = DistributedFieldTraceState.zeros().deposit_local_activity(
        (0.0, 1.0, 0.0, 0.0)
    )
    ledger = ExternalEvidenceLedger()

    left_returned = left.apply_external_world_return(
        (1.0, 0.0, 0.0, 0.0),
        sign=1,
        evidence_id="ev:left",
        evidence_ledger=ledger,
    )
    right_returned = right.apply_external_world_return(
        (0.0, 1.0, 0.0, 0.0),
        sign=1,
        evidence_id="ev:right",
        evidence_ledger=ledger,
    )

    assert left_returned.competition_score((1.0, 0.0, 0.0, 0.0)) == 0.5
    assert left_returned.competition_score((0.0, 1.0, 0.0, 0.0)) == 0.0
    assert right_returned.competition_score((1.0, 0.0, 0.0, 0.0)) == 0.0
    assert right_returned.competition_score((0.0, 1.0, 0.0, 0.0)) == 0.5


def test_contradiction_reverses_local_credit_sign() -> None:
    state = _with_left_activity()
    ledger = ExternalEvidenceLedger()
    confirmed = state.apply_external_world_return(
        (1.0, 0.0, 0.0, 0.0),
        sign=1,
        evidence_id="ev:confirm",
        evidence_ledger=ledger,
    )
    contradicted = confirmed.apply_external_world_return(
        (1.0, 0.0, 0.0, 0.0),
        sign=-1,
        evidence_id="ev:contradict",
        evidence_ledger=ledger,
    )

    assert confirmed.competition_score((1.0, 0.0, 0.0, 0.0)) == 0.5
    assert contradicted.competition_score((1.0, 0.0, 0.0, 0.0)) == -0.25


def test_f_only_carrier_transplant_preserves_functional_score() -> None:
    donor = DistributedFieldTraceState.zeros().deposit_local_activity(
        (0.0, 1.0, 0.0, 0.0)
    )
    donor = donor.apply_external_world_return(
        (0.0, 1.0, 0.0, 0.0),
        sign=1,
        evidence_id="ev:transfer",
        evidence_ledger=ExternalEvidenceLedger(),
    )

    transplanted = DistributedFieldTraceState.from_field_carrier(
        donor.export_field_carrier()
    )

    probe = (0.0, 1.0, 0.0, 0.0)
    assert transplanted.competition_score(probe) == donor.competition_score(probe) == 0.5


def test_state_construction_rejects_boolean_width() -> None:
    with pytest.raises(TypeError, match="width must be a non-boolean integer"):
        DistributedFieldTraceState.zeros(width=True)


@pytest.mark.parametrize(
    ("carrier", "expected_message"),
    [
        (
            [[True, False], [0.0, 0.0], 0.5],
            "vector values must be real numbers",
        ),
        (
            [[0.0, 0.0], [False, 0.0], 0.5],
            "vector values must be real numbers",
        ),
        (
            [[0.0, 0.0], [0.0, 0.0], False],
            "decay must be a real number",
        ),
    ],
)
def test_f_only_carrier_restore_rejects_boolean_numeric_values(
    carrier: list[object],
    expected_message: str,
) -> None:
    with pytest.raises(TypeError, match=re.escape(expected_message)):
        DistributedFieldTraceState.from_field_carrier(carrier)


def test_bounded_plurality_can_hold_two_footprints_then_differentiate_by_overlap() -> None:
    state = DistributedFieldTraceState.zeros().deposit_local_activity(
        (1.0, 1.0, 0.0, 0.0)
    )
    ledger = ExternalEvidenceLedger()

    left_evidence = state.apply_external_world_return(
        (1.0, 0.0, 0.0, 0.0),
        sign=1,
        evidence_id="ev:plural:left",
        evidence_ledger=ledger,
    )
    right_evidence = state.apply_external_world_return(
        (0.0, 1.0, 0.0, 0.0),
        sign=1,
        evidence_id="ev:plural:right",
        evidence_ledger=ledger,
    )

    assert left_evidence.eligibility[:2] == (1.0, 1.0)
    assert right_evidence.eligibility[:2] == (1.0, 1.0)
    assert left_evidence.credit[:2] == (0.5, 0.0)
    assert right_evidence.credit[:2] == (0.0, 0.5)


def test_eligibility_and_credit_decay_on_local_steps() -> None:
    ledger = ExternalEvidenceLedger()
    state = DistributedFieldTraceState.zeros(decay=0.5)
    state = state.deposit_local_activity((1.0, 0.0, 0.0, 0.0))
    state = state.apply_external_world_return(
        (1.0, 0.0, 0.0, 0.0),
        sign=1,
        evidence_id="ev:decay",
        evidence_ledger=ledger,
    )
    state = state.deposit_local_activity((0.0, 0.0, 0.0, 0.0))

    assert state.eligibility == (0.5, 0.0, 0.0, 0.0)
    assert state.credit == (0.25, 0.0, 0.0, 0.0)


def test_distinct_external_returns_remain_resource_bounded() -> None:
    ledger = ExternalEvidenceLedger()
    state = _with_left_activity()

    for index in range(64):
        state = state.apply_external_world_return(
            (1.0, 0.0, 0.0, 0.0),
            sign=1,
            evidence_id=f"ev:bounded:{index}",
            evidence_ledger=ledger,
        )

    assert 0.0 < state.credit[0] <= 2.0
    assert len(ledger.consumed_ids) == 64


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
            lambda: DistributedFieldTraceState.zeros().deposit_local_activity(
                (1.1, 0.0, 0.0, 0.0)
            ),
            "local activity values must be in [0, 1]",
        ),
        (
            lambda: DistributedFieldTraceState.zeros().apply_external_world_return(
                (1.0, 0.0, 0.0, 0.0),
                sign=0,
                evidence_id="ev:bad-sign",
                evidence_ledger=ExternalEvidenceLedger(),
            ),
            "external world-return sign must be -1 or +1",
        ),
        (
            lambda: DistributedFieldTraceState(
                eligibility=(3.0, 0.0, 0.0, 0.0),
                credit=(0.0, 0.0, 0.0, 0.0),
                decay=0.5,
            ).validate(),
            "eligibility values exceed the fixed resource bound",
        ),
        (
            lambda: DistributedFieldTraceState(
                eligibility=(0.0, 0.0, 0.0, 0.0),
                credit=(3.0, 0.0, 0.0, 0.0),
                decay=0.5,
            ).validate(),
            "credit values exceed the fixed resource bound",
        ),
        (
            lambda: ExternalEvidenceLedger.from_consumed_ids(("ev:a", "ev:a")),
            "consumed evidence IDs must be unique",
        ),
    ],
)
def test_invalid_carrier_inputs_fail_closed(
    operation: Callable[[], object],
    expected_message: str,
) -> None:
    with pytest.raises(ValueError, match=re.escape(expected_message)):
        operation()
