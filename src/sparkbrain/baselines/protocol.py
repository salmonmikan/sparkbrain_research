from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class StreamingBaseline(Protocol):
    name: str

    def reset(self) -> None: ...

    def step(self, observation: Any) -> Any: ...

    def predict_proba(self) -> dict[str, float]: ...

    def state_trace(self) -> dict[str, Any]: ...

    def work_counters(self) -> dict[str, int | float]: ...
