from __future__ import annotations

import argparse
from pathlib import Path

from sparkbrain.v03_external_validation.readiness import write_blocked_readiness_bundle

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "artifacts/v03/c19_external_validation/blocked-readiness-v1"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Write the deterministic C19 blocked engineering-readiness exact-nine bundle."
    )
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    hashes = write_blocked_readiness_bundle(
        output,
        root=ROOT,
        source_commit=args.source_commit,
    )
    print(f"wrote blocked C19 exact-nine bundle: {output}")
    for name, value in hashes.items():
        print(f"{name} {value}")


if __name__ == "__main__":
    main()
