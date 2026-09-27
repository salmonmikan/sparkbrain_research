"""Build the RD006 v3 deterministic static-preflight report."""

from __future__ import annotations

import argparse
from pathlib import Path

from sparkbrain.research.rv02_rd006_external_learning_reachability_v3 import (
    build_static_preflight,
    replay_static_preflight,
    serialize_static_preflight,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = serialize_static_preflight(build_static_preflight())
    replay_static_preflight(payload)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(payload)


if __name__ == "__main__":
    main()
