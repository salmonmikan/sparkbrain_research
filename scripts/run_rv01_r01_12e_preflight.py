from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from sparkbrain.research.rv01.interference_freeze import build_r01_12e_preflight


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build the capability-free RV01 R01-12E held-out freeze preflight."
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--source-git-sha",
        default=os.environ.get("GITHUB_SHA", ""),
        help="Full source SHA being reviewed for the held-out freeze.",
    )
    args = parser.parse_args()

    payload = build_r01_12e_preflight(source_git_sha=args.source_git_sha)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "candidate_id": payload["candidate_id"],
                "held_out_capability_executed": payload[
                    "held_out_capability_executed"
                ],
                "held_out_world_grid_hash": payload["held_out_world_grid_hash"],
                "preflight_payload_hash": payload["preflight_payload_hash"],
                "source_git_sha": payload["source_git_sha"],
                "status": payload["status"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
