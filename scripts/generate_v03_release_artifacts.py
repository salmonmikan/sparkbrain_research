from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sparkbrain.release_v03_artifacts import generate_v03_release_artifacts  # noqa: E402


def _require_clean_head(source_revision: str) -> None:
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=False, capture_output=True
    )
    if head.returncode or head.stdout.decode("ascii").strip() != source_revision:
        raise ValueError("v0.3 artifact generation requires source_revision equal to Git HEAD")
    for command in (("git", "diff", "--quiet"), ("git", "diff", "--cached", "--quiet")):
        result = subprocess.run(command, cwd=ROOT, check=False, capture_output=True)
        if result.returncode not in {0, 1}:
            raise ValueError("v0.3 artifact generation could not inspect tracked source state")
        if result.returncode:
            raise ValueError("v0.3 artifact generation requires a clean tracked source tree")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate v0.3 release evidence into a staging root"
    )
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--source-revision", required=True)
    args = parser.parse_args()
    try:
        _require_clean_head(args.source_revision)
        result = generate_v03_release_artifacts(
            ROOT,
            output_root=args.output_root.resolve(),
            source_revision=args.source_revision,
        )
    except (OSError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
