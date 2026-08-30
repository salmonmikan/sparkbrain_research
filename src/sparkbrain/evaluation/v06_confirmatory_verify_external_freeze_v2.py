from __future__ import annotations

import argparse
import json
from pathlib import Path

from .v06_confirmatory_external_verification_v2 import verify_external_bundle_cli


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Independently rebuild and verify an external freeze bundle.",
    )
    parser.add_argument("--unsigned-bundle", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--reviewer", required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--issue-approval", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    report = verify_external_bundle_cli(
        unsigned_bundle_path=args.unsigned_bundle,
        source_root=args.source_root.expanduser().resolve(strict=True),
        reviewer=args.reviewer,
        output_root=args.output_root,
        issue_approval=args.issue_approval,
    )
    print(json.dumps(report.state_dict(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
