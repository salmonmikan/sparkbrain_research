from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sparkbrain.release import build_release_archive  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a deterministic public release archive")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-date-epoch", type=int, required=True)
    args = parser.parse_args()
    try:
        result = build_release_archive(
            ROOT, args.output.resolve(), source_date_epoch=args.source_date_epoch
        )
    except (PermissionError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
