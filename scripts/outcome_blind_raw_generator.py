from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

RAW_SCHEMA_VERSION = 1


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n"
    ).encode("utf-8")


def generate_raw(*, fixture_path: Path, output_path: Path, seed: int) -> dict[str, Any]:
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    if fixture.get("synthetic_only") is not True:
        raise ValueError("fixture must be explicitly synthetic_only")
    if fixture.get("seed") != seed:
        raise ValueError("seed does not match frozen synthetic fixture")
    values = fixture.get("values")
    if not isinstance(values, list) or not values or not all(isinstance(v, int) for v in values):
        raise ValueError("fixture values must be a non-empty integer list")

    raw = {
        "schema_version": RAW_SCHEMA_VERSION,
        "fixture_id": fixture["fixture_id"],
        "surface": fixture["surface"],
        "seed": seed,
        "values": values,
    }
    if any(key in raw for key in ("score", "classification", "threshold", "result")):
        raise ValueError("raw payload must not contain scoring fields")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as handle:
        handle.write(canonical_json_bytes(raw))
        handle.flush()
        os.fsync(handle.fileno())
    return raw


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    generate_raw(fixture_path=args.fixture, output_path=args.output, seed=args.seed)


if __name__ == "__main__":
    main()
