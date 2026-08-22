from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .engine import SparkBrain
from .validation import assert_json_finite


def canonical_json(data: Any) -> str:
    assert_json_finite(data)
    return json.dumps(
        data,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def state_hash(brain: SparkBrain, *, include_trace: bool = True) -> str:
    payload = canonical_json(brain.state_dict(include_trace=include_trace)).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def dump_state(
    brain: SparkBrain,
    path: str | Path,
    *,
    include_trace: bool = True,
) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    state = brain.state_dict(include_trace=include_trace)
    output.write_text(canonical_json(state) + "\n", encoding="utf-8")
    return output


def load_state(path: str | Path) -> SparkBrain:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("State payload must be a JSON object")
    assert_json_finite(payload)
    return SparkBrain.from_state_dict(payload)
