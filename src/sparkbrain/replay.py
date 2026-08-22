from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

from .validation import SCHEMA_VERSION, assert_json_finite


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
    if not isinstance(payload, dict):
        raise ValueError("Trace payload must be a JSON object")
    schema_version = str(payload.get("schema_version", SCHEMA_VERSION))
    if schema_version != SCHEMA_VERSION:
        raise ValueError(f"Unsupported trace schema: {schema_version}")
    graph = payload.get("graph")
    frames = payload.get("frames")
    ignitions = payload.get("ignitions", [])
    if not isinstance(graph, dict):
        raise ValueError("Trace graph must be an object")
    if not isinstance(frames, list):
        raise ValueError("Trace frames must be a list")
    if not isinstance(ignitions, list):
        raise ValueError("Trace ignitions must be a list")
    assert_json_finite(payload)
    return TraceReplay(
        graph=graph,
        frames=tuple(frames),
        ignitions=tuple(ignitions),
        schema_version=schema_version,
    )
