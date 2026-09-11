from __future__ import annotations

import argparse
import json
from pathlib import Path

from sparkbrain.research.rv01.post_spike_suppression_contract import R01_15_PROTOCOL_ID
from sparkbrain.research.rv01.post_spike_suppression_runner import (
    run_development_post_spike_suppression_suite,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the fixed exposed-development RV01 R01-15 post-spike suppression suite."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/research/rv01/r01_15/development_result.json"),
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    output = args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise FileExistsError(f"refusing to overwrite existing R01-15 result: {output}")

    suite = run_development_post_spike_suppression_suite()
    payload = {
        "protocol_id": R01_15_PROTOCOL_ID,
        "phase": "development",
        "held_out_capability_executed": False,
        "suite": suite,
    }
    output.write_text(
        json.dumps(payload, allow_nan=False, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "protocol_id": R01_15_PROTOCOL_ID,
                "phase": "development",
                "held_out_capability_executed": False,
                "output": str(output),
                "world_count": suite["world_count"],
                "probe_count": suite["probe_count"],
                "world_grid_hash": suite["world_grid_hash"],
                "suite_hash": suite["suite_hash"],
                "overall_summary": suite["overall_summary"],
            },
            allow_nan=False,
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
