"""Build the RD006 v4 deterministic synthetic-preflight report."""

from __future__ import annotations

import argparse
from pathlib import Path

from sparkbrain.research.rv02_rd006_external_learning_reachability_v4 import (
    build_synthetic_preflight,
    replay_synthetic_preflight,
    serialize_synthetic_preflight,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = serialize_synthetic_preflight(build_synthetic_preflight())
    replay_synthetic_preflight(payload)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(payload)


if __name__ == "__main__":
    main()
