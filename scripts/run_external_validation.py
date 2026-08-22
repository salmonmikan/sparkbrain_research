from __future__ import annotations

import argparse
from pathlib import Path

from sparkbrain.external_validation.evaluation import run_external_evaluation

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the offline C06 external evaluation.")
    parser.add_argument(
        "--config",
        type=Path,
        default=ROOT / "configs/external_validation/final.json",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    config = args.config if args.config.is_absolute() else ROOT / args.config
    output = args.output
    if output is not None and not output.is_absolute():
        output = ROOT / output
    result = run_external_evaluation(config, output_override=output, root=ROOT)
    print(
        f"completed {result['run_manifest']['run_id']}: "
        f"{result['run_manifest']['belief_r_pairs']} Belief-R pairs"
    )


if __name__ == "__main__":
    main()
