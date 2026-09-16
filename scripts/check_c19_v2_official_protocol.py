from __future__ import annotations

import json
from pathlib import Path

from sparkbrain.v03_external_validation.official_protocol import (
    load_and_validate_protocol,
)

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "artifacts/v03/c19_external_validation/v2/official_protocol.json"


def main() -> None:
    summary = load_and_validate_protocol(PROTOCOL)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
