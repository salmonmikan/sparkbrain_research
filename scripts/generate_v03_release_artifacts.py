from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sparkbrain.release_v03_artifacts import generate_v03_release_artifacts  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate v0.3 release evidence into a staging root"
    )
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--source-revision", required=True)
    parser.add_argument(
        "--c19-status", choices=("accepted", "blocked", "negative"), default="blocked"
    )
    parser.add_argument("--c19-artifact", action="append", default=[])
    args = parser.parse_args()
    try:
        result = generate_v03_release_artifacts(
            ROOT,
            output_root=args.output_root.resolve(),
            source_revision=args.source_revision,
            c19_status=args.c19_status,
            c19_artifacts=args.c19_artifact,
        )
    except (OSError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
