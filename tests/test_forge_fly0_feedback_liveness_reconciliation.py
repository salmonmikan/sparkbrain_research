from __future__ import annotations

import pytest

from forge_prototypes.fly0_ascending_observed_state import (
    AscendingObservedStateBridge,
)
from forge_prototypes.fly0_feedback_liveness_reconciliation import (
    FeedbackLivenessReconciler,
    build_feedback_liveness_report,
)
from forge_prototypes.fly0_hierarchical_loop import WorldState
from forge_prototypes.fly0_reconciliation_admission_gate import (
    make_validation_proof,
)
from forge_prototypes.fly0_typed_ascending_signal import make_typed_signal

_VARIANTS = ("structured", "rewired", "random_sparse", "reactive")


def _observation(variant: str, *, frame_sequence: int = 0):
    bridge = AscendingObservedStateBridge(
        WorldState(position=2, target=-1),
        variant=variant,
        authority_token="intent-a",
    )
    result = bridge.step(
        bridge.guard.make_frame(
            frame_sequence=frame_sequence,
            mode="permit_side",
            target_side="left",
        )
    )
    observed_signal = make_typed_signal(
        semantic_kind="REAFFERENT_WORLD_OUTCOME",
        availability="OBSERVED",
        observed=result.observed,
    )
    return result.observed, observed_signal


@pytest.mark.parametrize("variant", _VARIANTS)
def test_timeout_never_invents_zero_and_late_valid_outcome_reconciles(
    variant: str,
) -> None:
    observed, observed_signal = _observation(variant)
    delayed = make_typed_signal(
        semantic_kind="REAFFERENT_WORLD_OUTCOME",
        availability="DELAYED",
        observed=observed,
        delay_steps=2,
    )
    reconciler = FeedbackLivenessReconciler()

    pending = reconciler.submit(
        f"{variant}-feedback",
        delayed,
        current_step=0,
        max_wait_steps=2,
    )
    timed_out = reconciler.advance_clock(2)

    assert pending.status == "PENDING"
    assert reconciler.world_position is None
    assert len(timed_out) == 1
    assert timed_out[0].status == "TIMEOUT_NO_WORLD_ASSUMPTION"
    assert timed_out[0].world_position is None

    proof = make_validation_proof(
        observed_signal,
        transaction_id=f"{variant}-tx",
        outcome_sequence=1,
        source_control_current=False,
    )
    late = reconciler.submit(
        f"{variant}-feedback",
        observed_signal,
        current_step=3,
        proof=proof,
    )
    duplicate = reconciler.submit(
        f"{variant}-feedback",
        observed_signal,
        current_step=4,
        proof=proof,
    )

    assert late.status == "RECONCILED"
    assert late.arrived_after_timeout is True
    assert late.state_advanced is True
    assert late.world_position == 1
    assert late.reason == (
        "COMMITTED_OUTCOME_RECONCILED_WITHOUT_CONTROL_RESTORATION"
    )
    assert duplicate.status == "DUPLICATE_NOOP"
    assert duplicate.state_advanced is False
    assert reconciler.world_position == 1


@pytest.mark.parametrize(
    "availability",
    ("GATED", "MASKED", "DELAYED", "MISSING"),
)
def test_unavailable_feedback_lifecycle_never_becomes_world_fact(
    availability: str,
) -> None:
    observed, observed_signal = _observation("structured")
    signal = make_typed_signal(
        semantic_kind="REAFFERENT_WORLD_OUTCOME",
        availability=availability,
        observed=None if availability == "MISSING" else observed,
        source_token=(
            observed_signal.source_token if availability == "MISSING" else None
        ),
        delay_steps=2 if availability == "DELAYED" else 0,
    )
    reconciler = FeedbackLivenessReconciler()

    first = reconciler.submit(
        "feedback-1",
        signal,
        current_step=0,
        max_wait_steps=3,
    )
    timeout = reconciler.advance_clock(3)

    assert first.status == "PENDING"
    assert reconciler.world_position is None
    assert len(timeout) == 1
    assert timeout[0].status == "TIMEOUT_NO_WORLD_ASSUMPTION"
    assert timeout[0].world_position is None
    assert reconciler.pending_count == 1


def test_repeated_unavailable_signal_does_not_extend_deadline() -> None:
    observed, _ = _observation("rewired")
    delayed = make_typed_signal(
        semantic_kind="REAFFERENT_WORLD_OUTCOME",
        availability="DELAYED",
        observed=observed,
        delay_steps=2,
    )
    masked = make_typed_signal(
        semantic_kind="REAFFERENT_WORLD_OUTCOME",
        availability="MASKED",
        observed=observed,
    )
    reconciler = FeedbackLivenessReconciler()

    assert (
        reconciler.submit(
            "feedback-1",
            delayed,
            current_step=0,
            max_wait_steps=2,
        ).status
        == "PENDING"
    )
    updated = reconciler.submit(
        "feedback-1",
        masked,
        current_step=1,
        max_wait_steps=50,
    )
    timeout = reconciler.advance_clock(2)

    assert updated.status == "PENDING_UPDATED"
    assert len(timeout) == 1
    assert timeout[0].status == "TIMEOUT_NO_WORLD_ASSUMPTION"


def test_pending_source_lineage_mismatch_fails_closed() -> None:
    first_observed, _ = _observation("structured", frame_sequence=0)
    second_observed, second_signal = _observation(
        "structured", frame_sequence=1
    )
    delayed = make_typed_signal(
        semantic_kind="REAFFERENT_WORLD_OUTCOME",
        availability="DELAYED",
        observed=first_observed,
        delay_steps=2,
    )
    reconciler = FeedbackLivenessReconciler()
    reconciler.submit(
        "feedback-1",
        delayed,
        current_step=0,
        max_wait_steps=4,
    )

    rejected = reconciler.submit(
        "feedback-1",
        second_signal,
        current_step=1,
        proof=make_validation_proof(
            second_signal,
            transaction_id="tx-wrong-lineage",
            outcome_sequence=1,
        ),
    )

    assert second_observed.token() != first_observed.token()
    assert rejected.status == "LINEAGE_REJECTED"
    assert rejected.reason == "OBSERVED_FEEDBACK_DOES_NOT_MATCH_PENDING_SOURCE"
    assert reconciler.world_position is None
    assert reconciler.pending_count == 1


def test_observed_feedback_still_requires_upstream_receipt_proof() -> None:
    _, signal = _observation("random_sparse")
    reconciler = FeedbackLivenessReconciler()

    decision = reconciler.submit(
        "feedback-1",
        signal,
        current_step=0,
    )

    assert decision.status == "RECEIPT_REQUIRED"
    assert decision.world_position is None


def test_non_reafferent_signal_is_not_given_feedback_liveness_state() -> None:
    predictive = make_typed_signal(
        semantic_kind="PREDICTIVE_MOTOR_COPY",
        availability="OBSERVED",
        source_token="prediction",
    )
    reconciler = FeedbackLivenessReconciler()

    decision = reconciler.submit(
        "prediction-1",
        predictive,
        current_step=0,
    )

    assert decision.status == "IGNORED_NON_REAFFERENT"
    assert reconciler.pending_count == 0
    assert reconciler.world_position is None


def test_checkpoint_restore_preserves_timeout_and_exactly_once_state() -> None:
    observed, signal = _observation("reactive")
    delayed = make_typed_signal(
        semantic_kind="REAFFERENT_WORLD_OUTCOME",
        availability="DELAYED",
        observed=observed,
        delay_steps=2,
    )
    proof = make_validation_proof(
        signal,
        transaction_id="tx-checkpoint",
        outcome_sequence=1,
    )
    reconciler = FeedbackLivenessReconciler()
    reconciler.submit(
        "feedback-1",
        delayed,
        current_step=0,
        max_wait_steps=2,
    )

    restored = FeedbackLivenessReconciler()
    restored.restore(reconciler.checkpoint())
    timeout = restored.advance_clock(2)
    late = restored.submit(
        "feedback-1",
        signal,
        current_step=3,
        proof=proof,
    )

    assert len(timeout) == 1
    assert timeout[0].status == "TIMEOUT_NO_WORLD_ASSUMPTION"
    assert late.status == "RECONCILED"
    assert late.arrived_after_timeout is True
    assert restored.world_position == 1

    restored_again = FeedbackLivenessReconciler()
    restored_again.restore(restored.checkpoint())
    duplicate = restored_again.submit(
        "feedback-1",
        signal,
        current_step=4,
        proof=proof,
    )
    assert duplicate.status == "DUPLICATE_NOOP"
    assert duplicate.state_advanced is False
    assert restored_again.world_position == 1


def test_report_keeps_liveness_and_scientific_claims_separate() -> None:
    report = build_feedback_liveness_report()

    assert report["status"] == "NON_EVIDENTIARY_NONCANONICAL_FORGE"
    assert report["design"] == "FEEDBACK_LIVENESS_RECONCILIATION"
    assert report["timeout_implies_zero_world_change"] is False
    assert report["late_valid_committed_outcome_may_reconcile"] is True
    assert report["deadline_extension_on_repeat_unavailable_signal"] is False
    assert report["full_r22_receipt_contract_implemented"] is False
