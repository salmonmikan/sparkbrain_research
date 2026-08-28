from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sparkbrain.v03 import (  # noqa: E402
    evaluate_engineering_runtime,
    validate_engineering_evaluation,
)

OUTPUT_NAME = "v031_integrated_engineering_evaluation.json"


def write_engineering_evaluation(output_dir: Path) -> tuple[Path, str]:
    """Atomically write and revalidate one canonical engineering-only result."""

    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / OUTPUT_NAME
    staging = output_dir / f".{OUTPUT_NAME}.staging"
    document = evaluate_engineering_runtime()
    validate_engineering_evaluation(document)
    payload = (
        json.dumps(
            document,
            allow_nan=False,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")
    staging.write_bytes(payload)
    reloaded = json.loads(staging.read_text(encoding="utf-8"))
    validate_engineering_evaluation(reloaded)
    if staging.read_bytes() != payload:
        raise RuntimeError("engineering evaluation staging bytes changed during verification")
    staging.replace(target)
    persisted = target.read_bytes()
    if persisted != payload:
        raise RuntimeError("engineering evaluation bytes changed after atomic replace")
    validate_engineering_evaluation(json.loads(persisted.decode("utf-8")))
    return target, hashlib.sha256(persisted).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Write the deterministic v0.3.1 engineering-only integrated runtime evaluation."
        )
    )
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    output_dir = args.output_dir if args.output_dir.is_absolute() else ROOT / args.output_dir
    target, digest = write_engineering_evaluation(output_dir)
    print(f"wrote engineering-only evaluation: {target}")
    print(f"sha256 {digest}")


if __name__ == "__main__":
    main()
