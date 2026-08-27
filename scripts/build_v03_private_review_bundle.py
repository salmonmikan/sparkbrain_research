from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sparkbrain.release_v03 import build_private_review_bundle  # noqa: E402


def _tracked_paths() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, check=False, capture_output=True
    )
    if result.returncode:
        raise ValueError("v0.3 private review build requires a tracked source tree")
    return [item for item in result.stdout.decode("utf-8").split("\0") if item]


def _current_clean_revision(expected: str) -> str:
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=False, capture_output=True
    )
    if revision.returncode:
        raise ValueError("v0.3 private review build requires a readable Git HEAD")
    actual = revision.stdout.decode("ascii").strip()
    if actual != expected:
        raise ValueError("v0.3 private review source_revision must match Git HEAD")
    for arguments in (("git", "diff", "--quiet"), ("git", "diff", "--cached", "--quiet")):
        result = subprocess.run(arguments, cwd=ROOT, check=False, capture_output=True)
        if result.returncode not in {0, 1}:
            raise ValueError("v0.3 private review build could not inspect Git changes")
        if result.returncode:
            raise ValueError("v0.3 private review build requires a clean tracked source tree")
    return actual


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a deterministic private SparkBrain v0.3 review ZIP"
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-date-epoch", type=int, required=True)
    parser.add_argument("--source-revision", required=True)
    args = parser.parse_args()
    try:
        _current_clean_revision(args.source_revision)
        result = build_private_review_bundle(
            ROOT,
            source_revision=args.source_revision,
            paths=_tracked_paths(),
            output=args.output.resolve(),
            source_date_epoch=args.source_date_epoch,
        )
    except (OSError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc
    print(result)


if __name__ == "__main__":
    main()
