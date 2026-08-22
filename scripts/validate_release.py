from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sparkbrain.release import validate_release_tree  # noqa: E402


def main() -> None:
    problems = validate_release_tree(ROOT)
    payload = {"status": "blocked" if problems else "ready", "problems": problems}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if problems:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
