"""Forge-only typed semantics for FLY-0 ascending signals."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Literal

from forge_prototypes.fly0_ascending_observed_state import (
    AscendingObservedStateBridge,
    ObservedStateSummary,
)
from forge_prototypes.fly0_hierarchical_loop import WorldState
from forge_prototypes.fly0_matched_replacement import Variant

SemanticKind = Literal[
    "PREDICTIVE_MOTOR_COPY",
    "REALIZED_LOCAL_STATE",
    "REAFFERENT_WORLD_OUTCOME",
]
Availability = Literal["OBSERVED", "GATED", "MASKED", "DELAYED", "MISSING"]

_KINDS: tuple[SemanticKind, ...] = (
    "PREDICTIVE_MOTOR_COPY",
    "REALIZED_LOCAL_STATE",
    "REAFFERENT_WORLD_OUTCOME",
)
_AVAILABILITY: tuple[Availability, ...] = (
    "OBSERVED",
    "GATED",
    "MASKED",
    "DELAYED",
    "MISSING",
)


@dataclass(frozen=True)
class TypedAscendingSignal:
    semantic_kind: SemanticKind
    availability: Availability
    source_token: str
    delay_steps: int
    accepted: bool | None
    local_step_committed: bool | None
    local_sequence_after: int | None
    world_position_after: int | None
    position_delta: int | None
    remaining_signed_error: int | None

    @property
    def provisional_only(self) -> bool:
        return self.semantic_kind == "PREDICTIVE_MOTOR_COPY"

    @property
    def world_reconciliation_candidate(self) -> bool:
        return (
            self.semantic_kind == "REAFFERENT_WORLD_OUTCOME"
            and self.availability == "OBSERVED"
            and self.accepted is True
            and self.local_step_committed is True
            and self.world_position_after is not None
        )

    @property
    def requires_full_r22_receipt_validation(self) -> bool:
        return self.world_reconciliation_candidate

    def token(self) -> str:
        raw = json.dumps(
            asdict(self), sort_keys=True, separators=(",", ":")
        ).encode()
        return sha256(raw).hexdigest()


def make_typed_signal(
    *,
    semantic_kind: SemanticKind,
    availability: Availability,
    observed: ObservedStateSummary | None = None,
    source_token: str | None = None,
    delay_steps: int = 0,
) -> TypedAscendingSignal:
    if semantic_kind not in _KINDS:
        raise ValueError(f"unsupported semantic_kind: {semantic_kind}")
    if availability not in _AVAILABILITY:
        raise ValueError(f"unsupported availability: {availability}")
    if delay_steps < 0:
        raise ValueError("delay_steps must be non-negative")
    if semantic_kind == "PREDICTIVE_MOTOR_COPY" and observed is not None:
        raise ValueError("predictive signal cannot carry realized observation")
    if (
        semantic_kind != "PREDICTIVE_MOTOR_COPY"
        and availability == "OBSERVED"
        and observed is None
    ):
        raise ValueError("observed realized signal requires observation")
    if source_token is None:
        if observed is None:
            raise ValueError("source_token is required")
        source_token = sha256(observed.token().encode()).hexdigest()

    visible = observed if availability == "OBSERVED" else None
    realized_world = bool(
        semantic_kind == "REAFFERENT_WORLD_OUTCOME"
        and visible is not None
        and visible.accepted
        and visible.local_step_committed
    )
    return TypedAscendingSignal(
        semantic_kind=semantic_kind,
        availability=availability,
        source_token=source_token,
        delay_steps=delay_steps,
        accepted=visible.accepted if visible is not None else None,
        local_step_committed=(
            visible.local_step_committed if visible is not None else None
        ),
        local_sequence_after=(
            visible.local_sequence_after
            if visible is not None
            and semantic_kind != "PREDICTIVE_MOTOR_COPY"
            else None
        ),
        world_position_after=(
            visible.world_position_after if realized_world else None
        ),
        position_delta=visible.position_delta if realized_world else None,
        remaining_signed_error=(
            visible.remaining_signed_error if realized_world else None
        ),
    )


_VARIANTS: tuple[Variant, ...] = (
    "structured",
    "rewired",
    "random_sparse",
    "reactive",
)


def build_typed_ascending_report() -> dict[str, object]:
    rows: dict[str, dict[str, bool]] = {}
    for variant in _VARIANTS:
        bridge = AscendingObservedStateBridge(
            WorldState(position=2, target=-1),
            variant=variant,
            authority_token="intent-a",
        )
        fresh = bridge.step(
            bridge.guard.make_frame(
                frame_sequence=0, mode="permit_side", target_side="left"
            )
        )
        reafferent = make_typed_signal(
            semantic_kind="REAFFERENT_WORLD_OUTCOME",
            availability="OBSERVED",
            observed=fresh.observed,
        )
        local = make_typed_signal(
            semantic_kind="REALIZED_LOCAL_STATE",
            availability="OBSERVED",
            observed=fresh.observed,
        )
        predictive = make_typed_signal(
            semantic_kind="PREDICTIVE_MOTOR_COPY",
            availability="OBSERVED",
            source_token=f"{variant}-motor-copy",
        )
        masked = make_typed_signal(
            semantic_kind="REAFFERENT_WORLD_OUTCOME",
            availability="MASKED",
            observed=fresh.observed,
        )
        rows[variant] = {
            "reafferent_candidate_only": (
                reafferent.world_reconciliation_candidate
                and reafferent.requires_full_r22_receipt_validation
            ),
            "predictive_not_realized": (
                predictive.provisional_only
                and predictive.world_position_after is None
                and not predictive.world_reconciliation_candidate
            ),
            "local_not_world": (
                local.local_sequence_after is not None
                and local.world_position_after is None
                and not local.world_reconciliation_candidate
            ),
            "masked_not_zero_outcome": (
                masked.world_position_after is None
                and masked.position_delta is None
                and not masked.world_reconciliation_candidate
            ),
        }
    return {
        "status": "NON_EVIDENTIARY_NONCANONICAL_FORGE",
        "design": "TYPED_ASCENDING_SEMANTIC_RECONCILIATION",
        "control_surface_expanded": False,
        "full_r22_receipt_contract_implemented": False,
        "semantic_kinds": list(_KINDS),
        "availability_states": list(_AVAILABILITY),
        "rows": rows,
        "all_variants_green": all(all(row.values()) for row in rows.values()),
        "ordinary_reduction": "typed telemetry / observer event semantics",
    }


if __name__ == "__main__":
    print(json.dumps(build_typed_ascending_report(), indent=2, sort_keys=True))
