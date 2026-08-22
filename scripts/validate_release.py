from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sparkbrain.release import preparation_problems, validate_release_tree  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate C10 release preparation/public gates")
    parser.add_argument(
        "--preparation-only",
        action="store_true",
        help="return success when non-public preparation passes, while still reporting blockers",
    )
    args = parser.parse_args()
    preparation = preparation_problems(ROOT)
    problems = validate_release_tree(ROOT)
    payload = {
        "status": "blocked" if problems else "ready",
        "preparation_status": "pass" if not preparation else "fail",
        "problems": problems,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if preparation or (problems and not args.preparation_only):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
