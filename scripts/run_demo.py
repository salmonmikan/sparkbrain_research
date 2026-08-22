from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from sparkbrain.serialization import dump_config
from sparkbrain.visualizer import write_trace, write_visualizer
from sparkbrain.worlds import SwitchWorld, run_scenario


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the canonical SparkBrain demo")
    parser.add_argument("--output", type=Path, default=Path("artifacts/demo"))
    args = parser.parse_args()

    brain, frames = run_scenario(SwitchWorld.canonical_scenario())
    args.output.mkdir(parents=True, exist_ok=True)
    dump_config(brain.config, args.output / "config.json")
    write_trace(brain, args.output / "trace.json")
    write_visualizer(brain, args.output / "visualizer.html")

    summary = {
        "schema_version": "0.2",
        "frames": len(frames),
        "final_prediction": brain.prediction,
        "ignitions": [asdict(ignition) for ignition in brain.ignitions],
        "stats": asdict(brain.stats),
    }
    with (args.output / "summary.json").open("w", encoding="utf-8", newline="") as handle:
        handle.write(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")

    for frame in frames:
        top = frame.coalitions[0] if frame.coalitions else None
        score = f"{top['score']:.3f}" if top else "-"
        print(
            f"t={frame.time:4.2f} event={frame.external_event:14s} "
            f"truth={str(frame.truth):4s} belief={str(frame.prediction):4s} top={score}"
        )
    print(f"\nVisualizer: {(args.output / 'visualizer.html').resolve()}")


if __name__ == "__main__":
    main()
