"""Strict C17 contracts shared by pure fixtures, discovery, and evaluation."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any


def canonical(value: object) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def text_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def protocol_document() -> dict[str, Any]:
    root = Path(__file__).resolve().parents[3]
    path = root / "artifacts/v03/c17_functional_organs_v2/preregistration.json"
    return json.loads(path.read_text(encoding="utf-8"))


def require_finite_number(value: object, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite number")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be a finite number")
    return result


def validate_resource_conditions(protocol: dict[str, Any]) -> list[dict[str, Any]]:
    spec = protocol["resource_conditions"]
    rows = spec["rows"]
    order = spec["condition_order"]
    if not isinstance(rows, list) or len(rows) != 5:
        raise ValueError("C17 requires exactly five resource conditions")
    if [row.get("condition_id") for row in rows] != order:
        raise ValueError("resource condition order mismatch")
    if len({row["condition_id"] for row in rows}) != len(rows):
        raise ValueError("duplicate resource condition")
    numeric = (
        "spark_module_capacity",
        "communication_bandwidth",
        "workspace_capacity",
        "task_compositionality",
    )
    primary = rows[0]
    if primary.get("role") != "primary":
        raise ValueError("R0 must be primary")
    for key in numeric:
        value = primary.get(key)
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError("resource values must be positive integers")
    for row in rows[1:]:
        if row.get("role") != "secondary":
            raise ValueError("non-R0 cells must be secondary")
        changed = []
        for key in numeric:
            value = row.get(key)
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError("resource values must be positive integers")
            if value != primary[key]:
                changed.append(key)
        if len(changed) != 1:
            raise ValueError("each secondary condition must change exactly one factor")
    return [dict(row) for row in rows]


def exact_keys(value: dict[str, Any], keys: set[str], name: str) -> None:
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError(f"invalid {name} schema")
