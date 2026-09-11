from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from sparkbrain.v061_a01.mechanism_discrimination import (
    run_a01_mechanism_discrimination,
)


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Execute the source-bound A01 P1-P5 mechanism discrimination.",
    )
    parser.add_argument(
        "--source-sha",
        default=os.environ.get("GITHUB_SHA", "UNBOUND_LOCAL_EXECUTION"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/v061/a01/A01_MD_001.json"),
    )
    return parser.parse_args()


def main() -> int:
    args = _arguments()
    result = run_a01_mechanism_discrimination(source_sha=args.source_sha)
    payload = json.dumps(
        result,
        allow_nan=False,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(payload + "\n", encoding="utf-8")
    temporary.replace(args.output)
    print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
