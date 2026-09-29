"""Forge-only exact correlation between issued FLY-0 frames and observed outcomes.

The existing observed-state adapter reports what actually happened after a
guarded local sensorimotor step.  This helper adds an explicit receipt identity
so a delayed or reordered outcome can be matched to the exact high-level frame
that produced it instead of being applied merely because it came from the same
authority epoch.

This is noncanonical, non-evidentiary engineering work.  It does not add a
control channel, allocate SYSTEM_BUILD authority, or establish a biological
mechanism.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, replace
from hashlib import sha256

from forge_prototypes.fly0_ascending_observed_state import (
    AscendingObservedStateBridge,
    ObservedStateSummary,
    ObservedStepResult,
)
from forge_prototypes.fly0_hierarchical_loop import WorldState
from forge_prototypes.fly0_matched_replacement import Variant
from forge_prototypes.fly0_modulation_supersession_guard import (
    GuardedModulationFrame,
)


@dataclass(frozen=True)
class CorrelatedOutcomeReceipt:
    authority_epoch: int
    authority_token: str
    frame_sequence: int
    frame_schema_version: str
    frame_mode: str
    frame_target_side: str | None
    frame_issued_at_local_sequence: int
    frame_ttl_steps: int
    frame_source_checkpoint_token: str
    observed_token: str
    accepted: bool
    reason: str
    local_step_committed: bool
    bridge_sequence_before: int
    bridge_sequence_after: int
    local_sequence_before: int
    local_sequence_after: int
    world_position_before: int
    world_position_after: int

    def token(self) -> str:
        payload = json.dumps(
            asdict(self), sort_keys=True, separators=(",", ":")
        ).encode()
        return sha256(payload).hexdigest()


def build_receipt(result: ObservedStepResult) -> CorrelatedOutcomeReceipt:
    guarded = result.guarded_result.guarded_frame
    frame = guarded.frame
    observed = result.observed
    return CorrelatedOutcomeReceipt(
        authority_epoch=guarded.authority_epoch,
        authority_token=guarded.authority_token,
        frame_sequence=frame.frame_sequence,
        frame_schema_version=frame.schema_version,
        frame_mode=frame.mode,
        frame_target_side=frame.target_side,
        frame_issued_at_local_sequence=frame.issued_at_local_sequence,
        frame_ttl_steps=frame.ttl_steps,
        frame_source_checkpoint_token=frame.source_checkpoint_token,
        observed_token=observed.token(),
        accepted=observed.accepted,
        reason=observed.reason,
        local_step_committed=observed.local_step_committed,
        bridge_sequence_before=observed.bridge_sequence_before,
        bridge_sequence_after=observed.bridge_sequence_after,
        local_sequence_before=observed.local_sequence_before,
        local_sequence_after=observed.local_sequence_after,
        world_position_before=observed.world_position_before,
        world_position_after=observed.world_position_after,
    )


def _frame_identity(frame: GuardedModulationFrame) -> tuple[object, ...]:
    inner = frame.frame
    return (
        frame.authority_epoch,
        frame.authority_token,
        inner.frame_sequence,
        inner.schema_version,
        inner.mode,
        inner.target_side,
        inner.issued_at_local_sequence,
        inner.ttl_steps,
        inner.source_checkpoint_token,
    )


def _receipt_frame_identity(
    receipt: CorrelatedOutcomeReceipt,
) -> tuple[object, ...]:
    return (
        receipt.authority_epoch,
        receipt.authority_token,
        receipt.frame_sequence,
        receipt.frame_schema_version,
        receipt.frame_mode,
        receipt.frame_target_side,
        receipt.frame_issued_at_local_sequence,
        receipt.frame_ttl_steps,
        receipt.frame_source_checkpoint_token,
    )


def _observed_projection(
    observed: ObservedStateSummary,
) -> tuple[object, ...]:
    return (
        observed.token(),
        observed.accepted,
        observed.reason,
        observed.local_step_committed,
        observed.bridge_sequence_before,
        observed.bridge_sequence_after,
        observed.local_sequence_before,
        observed.local_sequence_after,
        observed.world_position_before,
        observed.world_position_after,
    )


def _receipt_observed_projection(
    receipt: CorrelatedOutcomeReceipt,
) -> tuple[object, ...]:
    return (
        receipt.observed_token,
        receipt.accepted,
        receipt.reason,
        receipt.local_step_committed,
        receipt.bridge_sequence_before,
        receipt.bridge_sequence_after,
        receipt.local_sequence_before,
        receipt.local_sequence_after,
        receipt.world_position_before,
        receipt.world_position_after,
    )


def verify_receipt(
    receipt: CorrelatedOutcomeReceipt,
    *,
    expected_frame: GuardedModulationFrame,
    current_authority_epoch: int,
    current_authority_token: str,
    expected_observed: ObservedStateSummary | None = None,
) -> tuple[bool, str]:
    """Fail closed unless an outcome belongs to the exact expected frame."""

    if (
        receipt.authority_epoch != current_authority_epoch
        or receipt.authority_token != current_authority_token
    ):
        return False, "SUPERSEDED_OUTCOME_AUTHORITY"
    if _receipt_frame_identity(receipt) != _frame_identity(expected_frame):
        return False, "FRAME_IDENTITY_MISMATCH"
    if (
        expected_observed is not None
        and _receipt_observed_projection(receipt)
        != _observed_projection(expected_observed)
    ):
        return False, "OBSERVED_PAYLOAD_MISMATCH"
    return True, "RECEIPT_CORRELATED"


_VARIANTS: tuple[Variant, ...] = (
    "structured",
    "rewired",
    "random_sparse",
    "reactive",
)


def build_outcome_receipt_correlation_report() -> dict[str, object]:
    rows: dict[str, object] = {}
    for variant in _VARIANTS:
        bridge = AscendingObservedStateBridge(
            WorldState(position=2, target=-1),
            variant=variant,
            authority_token="intent-a",
        )
        checkpoint = bridge.checkpoint()
        frame = bridge.guard.make_frame(
            frame_sequence=0,
            mode="permit_side",
            target_side="left",
        )
        result = bridge.step(frame)
        receipt = build_receipt(result)

        exact_ok, exact_reason = verify_receipt(
            receipt,
            expected_frame=frame,
            current_authority_epoch=bridge.guard.authority_epoch,
            current_authority_token=bridge.guard.authority_token,
            expected_observed=result.observed,
        )

        wrong_frame = GuardedModulationFrame(
            authority_epoch=frame.authority_epoch,
            authority_token=frame.authority_token,
            frame=replace(frame.frame, frame_sequence=1),
        )
        wrong_ok, wrong_reason = verify_receipt(
            receipt,
            expected_frame=wrong_frame,
            current_authority_epoch=bridge.guard.authority_epoch,
            current_authority_token=bridge.guard.authority_token,
            expected_observed=result.observed,
        )

        bridge.guard.supersede("intent-b")
        stale_ok, stale_reason = verify_receipt(
            receipt,
            expected_frame=frame,
            current_authority_epoch=bridge.guard.authority_epoch,
            current_authority_token=bridge.guard.authority_token,
            expected_observed=result.observed,
        )

        bridge.restore(checkpoint)
        replay_frame = bridge.guard.make_frame(
            frame_sequence=0,
            mode="permit_side",
            target_side="left",
        )
        replay_result = bridge.step(replay_frame)
        replay_receipt = build_receipt(replay_result)

        rows[variant] = {
            "exact_receipt_correlates": (
                exact_ok and exact_reason == "RECEIPT_CORRELATED"
            ),
            "same_authority_wrong_frame_rejected": (
                not wrong_ok and wrong_reason == "FRAME_IDENTITY_MISMATCH"
            ),
            "superseded_receipt_rejected": (
                not stale_ok
                and stale_reason == "SUPERSEDED_OUTCOME_AUTHORITY"
            ),
            "checkpoint_replay_receipt_exact": (
                replay_receipt.token() == receipt.token()
            ),
        }

    return {
        "status": "NON_EVIDENTIARY_NONCANONICAL_FORGE",
        "design": "EXACT_OUTCOME_RECEIPT_CORRELATION",
        "control_surface_expanded": False,
        "modulation_vocabulary_expanded": False,
        "rows": rows,
        "all_variants_exactly_correlate_receipts": all(
            row["exact_receipt_correlates"]
            and row["same_authority_wrong_frame_rejected"]
            and row["superseded_receipt_rejected"]
            and row["checkpoint_replay_receipt_exact"]
            for row in rows.values()
        ),
        "ordinary_reduction": (
            "message correlation / provenance receipt for hierarchical control"
        ),
        "claim_boundary": (
            "This adds only exact command/outcome provenance correlation around "
            "the existing Forge observer. It does not establish biological "
            "fidelity or equivalence, topology necessity or superiority, "
            "compute or energy efficiency, composition contribution, "
            "whole-system superiority, external validity, scientific novelty, "
            "scientific credit, or SYSTEM_BUILD completion."
        ),
    }


if __name__ == "__main__":
    print(
        json.dumps(
            build_outcome_receipt_correlation_report(),
            indent=2,
            sort_keys=True,
        )
    )
