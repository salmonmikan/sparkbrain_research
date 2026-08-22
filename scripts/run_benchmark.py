from __future__ import annotations

import argparse
from pathlib import Path

from sparkbrain.benchmark import write_benchmark_outputs


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the SwitchWorld benchmark")
    parser.add_argument("--episodes", type=int, default=50)
    parser.add_argument("--steps", type=int, default=30)
    parser.add_argument("--output", type=Path, default=Path("artifacts/benchmarks"))
    args = parser.parse_args()

    paths = write_benchmark_outputs(
        args.output,
        episodes=args.episodes,
        steps=args.steps,
    )
    for path in paths:
        print(path.resolve())


if __name__ == "__main__":
    main()
