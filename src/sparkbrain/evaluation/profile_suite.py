from __future__ import annotations

import argparse
import json
import platform
import time
from pathlib import Path
from statistics import median

from ..tasks import generate_episode
from .run_suite import _condition_pairs
from .runner import run_episode


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--episodes", type=int, default=25)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists() and any(args.output.iterdir()):
        raise FileExistsError(args.output)
    args.output.mkdir(parents=True, exist_ok=True)
    config = json.loads(args.config.read_text(encoding="utf-8"))
    rows = []
    for world, condition in _condition_pairs(config):
        for seed in range(5):
            run_episode(
                generate_episode(
                    world, seed=seed, split="smoke", steps=int(config.get("steps", 30))
                ),
                condition=condition,
            )
        elapsed = []
        for repeat in range(args.repeats):
            start = time.perf_counter()
            for index in range(args.episodes):
                run_episode(
                    generate_episode(
                        world,
                        seed=10_000 + repeat * args.episodes + index,
                        split="smoke",
                        steps=int(config.get("steps", 30)),
                    ),
                    condition=condition,
                )
            elapsed.append((time.perf_counter() - start) / args.episodes)
        per_episode = median(elapsed)
        rows.append(
            {
                "world": world,
                "condition": condition,
                "median_seconds_per_episode": per_episode,
                "forecast_1000_seconds": 1000 * per_episode,
                "forecast_with_20_percent_contingency": 1200 * per_episode,
            }
        )
    payload = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "episodes_per_repeat": args.episodes,
        "repeats": args.repeats,
        "conditions": rows,
        "serial_forecast_seconds": sum(row["forecast_1000_seconds"] for row in rows),
    }
    (args.output / "runtime_estimate.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
