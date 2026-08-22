from __future__ import annotations

import argparse
from pathlib import Path

from sparkbrain.serialization import dump_state, load_state, state_hash
from sparkbrain.worlds import SwitchWorld, run_scenario


def main() -> None:
    parser = argparse.ArgumentParser(description="Demonstrate SparkBrain JSON checkpointing")
    parser.add_argument("--output", type=Path, default=Path("artifacts/demo/checkpoint.json"))
    args = parser.parse_args()

    events = SwitchWorld.canonical_scenario()
    brain, _ = run_scenario(events[:3])
    before_hash = state_hash(brain)
    dump_state(brain, args.output)
    restored = load_state(args.output)
    after_hash = state_hash(restored)
    if before_hash != after_hash:
        raise SystemExit("checkpoint round trip changed normalized state")

    print(f"checkpoint={args.output.resolve()}")
    print(f"state_sha256={before_hash}")
    print(f"prediction={restored.prediction}")


if __name__ == "__main__":
    main()
