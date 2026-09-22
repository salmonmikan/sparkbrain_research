from __future__ import annotations

import argparse
import json
from pathlib import Path

from sparkbrain.learned.h7_formal_r2_runner import preidentity_preflight, run_result_bearing


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preidentity-preflight", action="store_true")
    parser.add_argument("--authorized-run", action="store_true")
    parser.add_argument("--binding", type=Path)
    parser.add_argument("--started-marker", type=Path)
    parser.add_argument("--runtime-manifest", type=Path)
    parser.add_argument("--package-manifest", type=Path)
    parser.add_argument("--raw-output", type=Path)
    parser.add_argument("--actual-sha", default="")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]

    if args.preidentity_preflight:
        result = preidentity_preflight(root)
        print(json.dumps(result, indent=2, sort_keys=True))
        return

    if not args.authorized_run:
        parser.error("result-bearing path is disabled unless a later one-way authority invokes it")
    required = {
        "binding": args.binding,
        "started_marker": args.started_marker,
        "runtime_manifest": args.runtime_manifest,
        "package_manifest": args.package_manifest,
        "raw_output": args.raw_output,
        "actual_sha": args.actual_sha,
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        parser.error("authorized path requires: " + ", ".join(missing))
    result = run_result_bearing(
        root=root,
        binding_path=args.binding,
        started_marker=args.started_marker,
        runtime_manifest_path=args.runtime_manifest,
        package_manifest_path=args.package_manifest,
        raw_path=args.raw_output,
        actual_sha=args.actual_sha,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
