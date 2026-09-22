from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import torch

from sparkbrain.learned.h7_formal_r3 import (
    exact_runtime_observation,
    load_and_assert_r3_contract,
    preidentity_sentinel,
)


def _pip_freeze() -> str:
    completed = subprocess.run(
        ["python", "-m", "pip", "freeze", "--all"],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout


def _write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build H7 FORMAL-R3 non-result preidentity design/runtime diagnostics."
    )
    parser.add_argument(
        "--contract",
        type=Path,
        default=Path("artifacts/formal_h7_r3/contract_design.json"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/formal_h7_r3/preidentity_ci"),
    )
    args = parser.parse_args()

    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)

    contract = load_and_assert_r3_contract(args.contract)
    runtime = exact_runtime_observation(_pip_freeze())
    sentinel = preidentity_sentinel(contract)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    _write_json(args.output_dir / "runtime_observation.json", runtime)
    _write_json(args.output_dir / "preidentity_sentinel.json", sentinel)

    print("H7_R3_RUNTIME_OBSERVATION_JSON=" + json.dumps(runtime, sort_keys=True))
    print("H7_R3_PREIDENTITY_SENTINEL_JSON=" + json.dumps(sentinel, sort_keys=True))


if __name__ == "__main__":
    main()
