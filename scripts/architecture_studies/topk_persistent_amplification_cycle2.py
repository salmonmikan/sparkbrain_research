from __future__ import annotations

import argparse
import copy
from pathlib import Path
from typing import Any

import topk_persistent_amplification_cycle1 as cycle1

ANALYST_COMMIT = "5b63d21f44812ef8d4938c9ad968bb8ab481b3c5"
CONTINUATION_HEAD = "97f542d86dcd3a609cd039379fcda41ba61e0909"
MODEL_SEED = 42
CONFIG_PATH = Path("configs/experiments/phase2/main.json")
EXPECTED_PRIOR_MODEL_SEED = 41


def _verify_fixed_contract() -> None:
    expected: dict[str, Any] = {
        "EXPECTED_MAIN_SHA": "ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d",
        "DIRECTION_SEED": 20260919,
        "MAGNITUDES": (0.01, 0.05, 0.10),
        "PROBE_POSITIONS": (6, 12, 18, 24),
        "DIRECTIONS_PER_PROBE": 8,
        "HORIZON": 6,
        "TURNOVER_MINIMUM": 20,
        "STATE_RATIO_SIGNAL": 2.0,
        "OUTPUT_RATIO_SIGNAL": 1.5,
        "STATE_RATIO_ORDINARY": 1.25,
    }
    for name, value in expected.items():
        actual = getattr(cycle1, name)
        if actual != value:
            raise RuntimeError(
                f"Cycle-2 fixed contract mismatch for {name}: expected {value!r}, got {actual!r}"
            )


def run(output_dir: Path) -> dict[str, Any]:
    _verify_fixed_contract()
    original_read_json = cycle1._read_json
    original_analyst_commit = cycle1.ANALYST_COMMIT

    def read_json_with_replication_seed(path: Path) -> dict[str, Any]:
        value = original_read_json(path)
        if path == CONFIG_PATH:
            value = copy.deepcopy(value)
            observed_seed = value["learned"]["seed"]
            if observed_seed != EXPECTED_PRIOR_MODEL_SEED:
                raise RuntimeError(
                    "Cycle-2 replication expected source model seed "
                    f"{EXPECTED_PRIOR_MODEL_SEED}, got {observed_seed}"
                )
            value["learned"]["seed"] = MODEL_SEED
        return value

    cycle1._read_json = read_json_with_replication_seed
    cycle1.ANALYST_COMMIT = ANALYST_COMMIT
    try:
        return cycle1.run(output_dir)
    finally:
        cycle1._read_json = original_read_json
        cycle1.ANALYST_COMMIT = original_analyst_commit


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/architecture_studies/topk-persistent-amplification-cycle2"),
    )
    args = parser.parse_args()
    run(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
