from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def score_preserved_raw(
    *,
    preserved_raw_path: Path,
    expected_raw_sha256: str,
    plan_path: Path,
) -> dict[str, Any]:
    observed_sha256 = sha256_file(preserved_raw_path)
    if observed_sha256 != expected_raw_sha256:
        raise ValueError("preserved raw digest mismatch")

    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    if plan.get("transform") != "identity":
        raise ValueError("unexpected transform")
    if plan.get("comparator") != "none":
        raise ValueError("unexpected comparator")
    if plan.get("score") != "sum":
        raise ValueError("unexpected score rule")
    threshold = plan.get("threshold")
    if not isinstance(threshold, int):
        raise ValueError("threshold must be an integer")

    raw = json.loads(preserved_raw_path.read_text(encoding="utf-8"))
    forbidden = {"score", "classification", "threshold", "result"}
    if forbidden.intersection(raw):
        raise ValueError("raw payload contains scoring fields")

    score = sum(raw["values"])
    classification = "ABOVE_OR_EQUAL" if score >= threshold else "BELOW"
    return {
        "score": score,
        "classification": classification,
        "threshold": threshold,
        "raw_sha256": observed_sha256,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--raw-sha256", required=True)
    parser.add_argument("--plan", type=Path, required=True)
    args = parser.parse_args()
    result = score_preserved_raw(
        preserved_raw_path=args.raw,
        expected_raw_sha256=args.raw_sha256,
        plan_path=args.plan,
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
