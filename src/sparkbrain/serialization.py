from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .engine import SparkBrain
from .model import BrainConfig
from .validation import SCHEMA_VERSION, assert_json_finite, validate_config, validate_config_payload


def canonical_json(data: Any) -> str:
    assert_json_finite(data)
    return json.dumps(
        data,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def _write_utf8_lf(path: Path, contents: str) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(contents)


def state_hash(brain: SparkBrain, *, include_trace: bool = True) -> str:
    payload = canonical_json(brain.state_dict(include_trace=include_trace)).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def config_document(config: BrainConfig) -> dict[str, Any]:
    """Return the versioned, standalone JSON document for a configuration."""

    validate_config(config)
    return {"schema_version": SCHEMA_VERSION, "config": asdict(config)}


def dump_config(config: BrainConfig, path: str | Path) -> Path:
    """Persist a validated configuration without embedding it in a checkpoint."""

    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    _write_utf8_lf(output, canonical_json(config_document(config)) + "\n")
    return output


def load_config(path: str | Path) -> BrainConfig:
    """Load the explicit configuration document used by local experiments."""

    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Config document must be a JSON object")
    if set(payload) != {"schema_version", "config"}:
        raise ValueError("Config document must contain exactly schema_version and config")
    if payload["schema_version"] != SCHEMA_VERSION:
        raise ValueError(f"Unsupported config schema: {payload['schema_version']!r}")
    validate_config_payload(payload["config"])
    assert_json_finite(payload)
    return BrainConfig(**payload["config"])


def dump_state(
    brain: SparkBrain,
    path: str | Path,
    *,
    include_trace: bool = True,
) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    state = brain.state_dict(include_trace=include_trace)
    _write_utf8_lf(output, canonical_json(state) + "\n")
    return output


def load_state(path: str | Path) -> SparkBrain:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("State payload must be a JSON object")
    assert_json_finite(payload)
    return SparkBrain.from_state_dict(payload)
