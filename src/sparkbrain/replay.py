from __future__ import annotations

import json
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .validation import SCHEMA_VERSION, validate_trace_payload


@dataclass(frozen=True, slots=True)
class TraceReplay:
    graph: dict[str, Any]
    frames: tuple[dict[str, Any], ...]
    ignitions: tuple[dict[str, Any], ...]
    schema_version: str = SCHEMA_VERSION

    def __iter__(self) -> Iterator[dict[str, Any]]:
        return iter(self.frames)

    def frame(self, index: int) -> dict[str, Any]:
        return self.frames[index]

    @property
    def final_prediction(self) -> str | None:
        if not self.frames:
            return None
        return self.frames[-1].get("prediction")


def load_trace(path: str | Path) -> TraceReplay:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    validate_trace_payload(payload)
    return TraceReplay(
        graph=payload["graph"],
        frames=tuple(payload["frames"]),
        ignitions=tuple(payload["ignitions"]),
        schema_version=payload["schema_version"],
    )
