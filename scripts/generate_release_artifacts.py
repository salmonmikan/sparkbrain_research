from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sparkbrain.release_artifacts import generate_release_artifacts  # noqa: E402


def main() -> None:
    hashes = generate_release_artifacts(ROOT)
    print(json.dumps({"status": "generated", "outputs": hashes}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
