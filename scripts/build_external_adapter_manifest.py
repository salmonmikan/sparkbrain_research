from __future__ import annotations

import argparse
import json
from pathlib import Path

from sparkbrain.external_validation.adapters import build_frozen_adapter_manifest

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "configs/external_validation/model_adapters.json"


def _render(payload: dict[str, object]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build or verify the dev-only C04/C05 external adapter manifest."
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--write", action="store_true", help="write the deterministic manifest")
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    rendered = _render(build_frozen_adapter_manifest(ROOT))
    if args.write:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8", newline="\n")
        print(f"wrote {output}")
        return
    if not output.is_file():
        raise FileNotFoundError(f"adapter manifest missing: {output}")
    if output.read_text(encoding="utf-8") != rendered:
        raise ValueError("adapter manifest is stale; regenerate with --write")
    print(f"verified {output}")


if __name__ == "__main__":
    main()
