from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from sparkbrain.external_validation.belief_r import acquire_or_verify, load_belief_r_spec


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Acquire or verify the official pinned Belief-R test-only cache."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/external_validation/belief_r.json"),
    )
    parser.add_argument(
        "--cache",
        type=Path,
        default=Path("data/external/belief_r/test.csv"),
    )
    parser.add_argument(
        "--acquire",
        action="store_true",
        help="Allow one HTTPS download. Without this flag the command is verify-only/offline.",
    )
    args = parser.parse_args()
    spec = load_belief_r_spec(args.config)
    report = acquire_or_verify(args.cache, spec, acquire=args.acquire)
    print(json.dumps(asdict(report), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
