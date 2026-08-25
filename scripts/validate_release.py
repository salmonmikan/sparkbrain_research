from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sparkbrain.release import release_validation  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate C10 release preparation/public gates")
    parser.add_argument(
        "--preparation-only",
        action="store_true",
        help="return success when non-public preparation passes, while still reporting blockers",
    )
    args = parser.parse_args()
    validation = release_validation(ROOT)
    non_owner_problems = [
        *validation["integrity_problems"],
        *validation["preparation_problems"],
        *validation["evidence_blockers"],
    ]
    problems = [*non_owner_problems, *validation["owner_blockers"]]
    status = (
        "invalid"
        if non_owner_problems
        else "blocked"
        if validation["owner_blockers"]
        else "ready"
    )
    payload = {
        "status": status,
        "preparation_status": "fail" if non_owner_problems else "pass",
        **validation,
        "problems": problems,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if non_owner_problems or (validation["owner_blockers"] and not args.preparation_only):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
