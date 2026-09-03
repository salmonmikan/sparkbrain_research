from __future__ import annotations

from enum import StrEnum
from typing import Any, Protocol, runtime_checkable

from .events import ComparatorEvent, PredictionDistribution


class ComparatorKind(StrEnum):
    G3_FIRST_ORDER = "g3-first-order-anchor"
    G4_ASSEMBLY = "g4-assembly-anchor"
    G5_TYPED = "g5-typed-anchor"
    G6_VARIABLE_ORDER = "g6-variable-order"
    G7_HTM_TEMPORAL_MEMORY = "g7-htm-temporal-memory"
    G8_PREDICTION = "g8-spiking-temporal-memory-prediction"
    G8_REPLAY = "g8-spiking-temporal-memory-replay"


@runtime_checkable
class ComparatorProtocol(Protocol):
    """Minimal architecture-neutral CX01 comparator interface.

    Models receive anonymous external tokens and timestamps only. They must not
    receive evaluator context IDs, correct targets, semantic labels, or reward.

    `learn=False` is an explicit evaluation boundary: the external event may
    update transient inference state but must not change learned parameters.
    """

    kind: ComparatorKind

    def observe_external(self, event: ComparatorEvent, *, learn: bool = True) -> None: ...

    def finalize_episode(self) -> None: ...

    def advance(self, timestamp_ms: float) -> None: ...

    def generate(self, *, max_steps: int = 1) -> tuple[ComparatorEvent, ...]: ...

    def distribution(self) -> PredictionDistribution: ...

    def suppress(self, token: str) -> None: ...

    def clear_suppression(self) -> None: ...

    def snapshot(self) -> dict[str, Any]: ...

    def restore(self, state: dict[str, Any]) -> None: ...

    def learned_state_dict(self) -> dict[str, Any]: ...

    @property
    def parameter_count(self) -> int: ...

    @property
    def state_entry_count(self) -> int: ...

    @property
    def observed_external_events(self) -> int: ...

    @property
    def generated_internal_events(self) -> int: ...
