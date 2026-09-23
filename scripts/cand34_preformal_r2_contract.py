from __future__ import annotations

import argparse
import json
from pathlib import Path

from sparkbrain.v05.route_preformal_r2 import bind_preformal_r2_contract_closure


def _write_once(path: Path, payload: object) -> None:
    if path.exists():
        raise FileExistsError(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    path.write_text(rendered, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Materialize candidate34 PRE_FORMAL R2 non-result contract closure."
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    closure, queue = bind_preformal_r2_contract_closure()
    if closure.response_bearing_execution_allowed:
        raise RuntimeError("R2 closure must not enable response-bearing execution")
    if queue.response_bearing_execution_performed:
        raise RuntimeError("R2 queue materialization must not execute responses")
    _write_once(args.output_dir / "cand34-preformal-r2-contract.json", closure.as_dict())
    _write_once(args.output_dir / "cand34-preformal-r2-queue.json", queue.as_dict())


if __name__ == "__main__":
    main()
