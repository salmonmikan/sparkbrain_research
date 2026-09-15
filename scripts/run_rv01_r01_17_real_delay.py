from __future__ import annotations

import argparse
import json
import platform
from pathlib import Path

from sparkbrain.research.rv01_r01_17_real_delay import (
    R01_17_PROTOCOL_ID,
    acquire_raw_suite,
    score_raw_suite,
)


def _write_new(path: Path, payload: dict[str, object]) -> None:
    if path.exists():
        raise FileExistsError(f"refusing to overwrite existing R01-17 output: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def _read_raw(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError("R01-17 raw payload must be a JSON object")
    if value.get("protocol_id") != R01_17_PROTOCOL_ID:
        raise ValueError("R01-17 raw payload protocol mismatch")
    return value


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Acquire or score the frozen R01-17 exposed-development real-delay probe."
    )
    subparsers = parser.add_subparsers(dest="mode", required=True)

    acquire = subparsers.add_parser("acquire")
    acquire.add_argument("--source-git-sha", required=True)
    acquire.add_argument("--output", type=Path, required=True)

    score = subparsers.add_parser("score")
    score.add_argument("--raw", type=Path, required=True)
    score.add_argument("--output", type=Path, required=True)

    args = parser.parse_args()
    if args.mode == "acquire":
        payload = acquire_raw_suite(
            source_git_sha=args.source_git_sha,
            python_runtime=platform.python_version(),
        )
        _write_new(args.output, payload)
    else:
        raw = _read_raw(args.raw)
        scored = score_raw_suite(raw)
        _write_new(args.output, scored)


if __name__ == "__main__":
    main()
