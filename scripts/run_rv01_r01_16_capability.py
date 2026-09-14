from __future__ import annotations

import argparse
from pathlib import Path

from sparkbrain.research.rv01_r01_16_capability_package import execute_capability_once


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Execute the frozen R01-16 exposed-development capability once."
    )
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--source-manifest", type=Path, required=True)
    parser.add_argument("--construction-census", type=Path, required=True)
    parser.add_argument(
        "--control-mode",
        choices=("distributed-github", "local-offline"),
        required=True,
    )
    parser.add_argument(
        "--assert-single-host-ownership",
        action="store_true",
        help=(
            "Required for local-offline mode. Records the caller's assertion that "
            "no other host can execute the same frozen capability identity."
        ),
    )
    args = parser.parse_args()
    output = execute_capability_once(
        repo_root=args.repo_root,
        source_manifest_path=args.source_manifest,
        construction_census_path=args.construction_census,
        control_mode=args.control_mode,
        single_host_ownership_asserted=args.assert_single_host_ownership,
    )
    print(output.as_posix())


if __name__ == "__main__":
    main()
