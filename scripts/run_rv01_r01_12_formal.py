from __future__ import annotations

import argparse
import json
from pathlib import Path

from sparkbrain.research.rv01.interference_formal import (
    run_sealed_held_out_interference,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Execute the sealed one-way RV01 R01-12 held-out programme."
    )
    parser.add_argument("--seal", type=Path, required=True)
    parser.add_argument("--source-git-sha", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if args.output.exists():
        raise RuntimeError("formal output already exists; one-way execution will not clobber it")
    seal = json.loads(args.seal.read_text(encoding="utf-8"))
    result = run_sealed_held_out_interference(
        seal,
        checked_out_source_sha=args.source_git_sha,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(result, handle, ensure_ascii=False, sort_keys=True, indent=2)
        handle.write("\n")
    print(
        json.dumps(
            {
                "candidate_id": result["candidate_id"],
                "field_suite_hash": result["field_suite_hash"],
                "held_out_capability_executed": result[
                    "held_out_capability_executed"
                ],
                "held_out_world_grid_hash": result["held_out_world_grid_hash"],
                "reservoir_suite_hash": result["reservoir_suite_hash"],
                "seal_payload_hash": result["seal_payload_hash"],
                "source_git_sha": result["source_git_sha"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
