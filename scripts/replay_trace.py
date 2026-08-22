from __future__ import annotations

import argparse
from pathlib import Path

from sparkbrain.replay import load_trace


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect a SparkBrain trace without dynamics")
    parser.add_argument("trace", type=Path, nargs="?", default=Path("artifacts/demo/trace.json"))
    args = parser.parse_args()

    replay = load_trace(args.trace)
    print(f"schema={replay.schema_version} frames={len(replay.frames)} final={replay.final_prediction}")
    for index, frame in enumerate(replay):
        top = frame.get("coalitions", [])
        top_label = top[0]["label"] if top else "-"
        top_score = top[0]["score"] if top else 0.0
        print(
            f"{index:02d} t={frame['time']:.3f} event={frame['external_event']:<14} "
            f"truth={str(frame.get('truth')):<4} belief={str(frame.get('prediction')):<4} "
            f"top={top_label}:{top_score:.3f}"
        )


if __name__ == "__main__":
    main()
