from __future__ import annotations

import argparse
import json
from pathlib import Path

from sparkbrain.learned.h7_formal_r2_runner import preidentity_preflight


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preidentity-preflight", action="store_true")
    args = parser.parse_args()
    if not args.preidentity_preflight:
        parser.error("cycle-8 authority permits preidentity preflight only")
    root = Path(__file__).resolve().parents[1]
    result = preidentity_preflight(root)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
