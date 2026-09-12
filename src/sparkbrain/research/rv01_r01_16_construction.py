"""Fresh-output construction runner for prospective RV01 R01-16.

This module is deliberately construction-only. It consumes retained pre/post
connection inventories, builds the preregistered F0/FW/FD/FWD factorization,
and writes auditable construction artifacts into a new directory. It does not
train a learner, run a probe, score capability, reveal held-out data, or grant
formal execution authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .rv01_r01_16_factorization import (
    ConnectionState,
    QueuedPropagationSnapshot,
    R01_16FactorizationConstruction,
    R01_16_PROTOCOL_ID,
)

_INPUT_KEYS = frozenset(
    {
        "source_git_sha",
        "source_manifest_sha256",
        "collision_registry_sha256",
        "package_plan_sha256",
        "pre_training",
        "post_training",
        "queued_propagation",
    }
)
_CONNECTION_KEYS = frozenset(
    {"source_id", "target_id", "weight", "delay_ms", "plastic"}
)
_QUEUE_KEYS = frozenset(
    {"event_id", "source_id", "target_id", "queued_weight", "queued_delay_ms"}
)


def _sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _canonical_json(value: object) -> bytes:
    return (
        json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def _require_hash(value: object, *, label: str, length: int) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{label} must be a string")
    if len(value) != length or any(char not in "0123456789abcdef" for char in value):
        raise ValueError(f"{label} must be a {length}-character lowercase hex digest")
    return value


def _require_object(
    value: object,
    *,
    label: str,
    expected_keys: frozenset[str],
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TypeError(f"{label} must be a JSON object")
    keys = frozenset(value)
    if keys != expected_keys:
        raise ValueError(
            f"{label} keys must exactly match {sorted(expected_keys)}; "
            f"got {sorted(keys)}"
        )
    return value


def _connection(value: object, *, label: str) -> ConnectionState:
    row = _require_object(value, label=label, expected_keys=_CONNECTION_KEYS)
    connection = ConnectionState(
        source_id=row["source_id"],
        target_id=row["target_id"],
        weight=row["weight"],
        delay_ms=row["delay_ms"],
        plastic=row["plastic"],
    )
    connection.validate()
    return connection


def _queued(value: object, *, label: str) -> QueuedPropagationSnapshot:
    row = _require_object(value, label=label, expected_keys=_QUEUE_KEYS)
    queued = QueuedPropagationSnapshot(
        event_id=row["event_id"],
        source_id=row["source_id"],
        target_id=row["target_id"],
        queued_weight=row["queued_weight"],
        queued_delay_ms=row["queued_delay_ms"],
    )
    queued.validate()
    return queued


def _rows(value: object, *, label: str) -> list[object]:
    if not isinstance(value, list):
        raise TypeError(f"{label} must be a JSON array")
    return value


def _load_construction(raw: bytes) -> tuple[
    dict[str, str],
    R01_16FactorizationConstruction,
]:
    try:
        decoded = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("R01-16 construction input must be valid UTF-8 JSON") from exc
    payload = _require_object(
        decoded,
        label="construction input",
        expected_keys=_INPUT_KEYS,
    )
    identities = {
        "source_git_sha": _require_hash(
            payload["source_git_sha"],
            label="source_git_sha",
            length=40,
        ),
        "source_manifest_sha256": _require_hash(
            payload["source_manifest_sha256"],
            label="source_manifest_sha256",
            length=64,
        ),
        "collision_registry_sha256": _require_hash(
            payload["collision_registry_sha256"],
            label="collision_registry_sha256",
            length=64,
        ),
        "package_plan_sha256": _require_hash(
            payload["package_plan_sha256"],
            label="package_plan_sha256",
            length=64,
        ),
    }
    pre_training = tuple(
        _connection(row, label=f"pre_training[{index}]")
        for index, row in enumerate(_rows(payload["pre_training"], label="pre_training"))
    )
    post_training = tuple(
        _connection(row, label=f"post_training[{index}]")
        for index, row in enumerate(_rows(payload["post_training"], label="post_training"))
    )
    queued = tuple(
        _queued(row, label=f"queued_propagation[{index}]")
        for index, row in enumerate(
            _rows(payload["queued_propagation"], label="queued_propagation")
        )
    )
    return identities, R01_16FactorizationConstruction(
        pre_training=pre_training,
        post_training=post_training,
        queued_propagation=queued,
    )


def _write_json(path: Path, value: object) -> None:
    path.write_bytes(_canonical_json(value))


def run_construction(*, input_path: Path, output_dir: Path) -> Path:
    """Run construction once into a fresh directory and retain failures."""

    output_dir.mkdir(parents=True, exist_ok=False)
    raw = input_path.read_bytes()
    input_sha256 = _sha256_bytes(raw)
    (output_dir / "construction_input.json").write_bytes(raw)
    _write_json(
        output_dir / "input_identity.json",
        {"construction_input_sha256": input_sha256},
    )

    try:
        identities, construction = _load_construction(raw)
        summary = construction.require_any_prospective_contrast()
        runtime = {
            "python_implementation": platform.python_implementation(),
            "python_version": platform.python_version(),
            "python_executable": sys.executable,
            "runner_module": "sparkbrain.research.rv01_r01_16_construction",
            "protocol_id": R01_16_PROTOCOL_ID,
        }
        _write_json(output_dir / "runtime.json", runtime)
        _write_json(output_dir / "source_binding.json", identities)
        summary_state = asdict(summary)
        _write_json(output_dir / "construction_summary.json", summary_state)

        arms_dir = output_dir / "arms"
        arms_dir.mkdir(exist_ok=False)
        for arm in ("F0", "FW", "FD", "FWD"):
            _write_json(
                arms_dir / f"{arm}.json",
                [row.state_dict() for row in construction.arm_inventory(arm)],
            )

        _write_json(
            output_dir / "COMPLETE.json",
            {
                "status": "CONSTRUCTION_COMPLETE_CAPABILITY_UNOPENED",
                "construction_input_sha256": input_sha256,
                "construction_summary_sha256": _sha256_bytes(
                    _canonical_json(summary_state)
                ),
                "capability_output_opened": False,
                "learner_or_probe_executed": False,
                "formal_execution_allowed": False,
            },
        )
    except Exception as exc:
        _write_json(
            output_dir / "FAILED.json",
            {
                "status": "CONSTRUCTION_FAILED_TERMINAL_FOR_THIS_OUTPUT_IDENTITY",
                "construction_input_sha256": input_sha256,
                "exception_type": type(exc).__name__,
                "message": str(exc),
                "retry_same_output_identity_allowed": False,
            },
        )
        raise

    return output_dir


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build R01-16 construction artifacts without capability execution."
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    run_construction(input_path=args.input, output_dir=args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["main", "run_construction"]
