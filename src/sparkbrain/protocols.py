from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from .model import EventKind, TraceFrame


@runtime_checkable
class BrainBackend(Protocol):
    """Behavioral interface shared by reference, learned, and spiking backends."""

    @property
    def prediction(self) -> str | None: ...

    def schedule(
        self,
        *,
        time: float,
        kind: EventKind,
        source: str,
        target: str | None,
        strength: float = 0.0,
        priority: int = 10,
        evidence_id: str | None = None,
        evidence_label: str | None = None,
        metadata: dict | None = None,
    ) -> None: ...

    def run(self, *, max_events: int = 100_000) -> None: ...

    def snapshot(self, *, external_event: str, truth: str | None = None) -> TraceFrame: ...

    def state_dict(self, *, include_trace: bool = True) -> dict[str, Any]: ...
