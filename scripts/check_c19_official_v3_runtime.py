from __future__ import annotations

import importlib
import tomllib
from pathlib import Path

from sparkbrain.external_validation.evaluation import network_blocked
from sparkbrain.v03_external_validation.official_execution_v3 import assert_runtime_closed_v3
from sparkbrain.v03_external_validation.official_protocol_v3 import REQUIRED_TORCH_VERSION

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    learned = project["project"]["optional-dependencies"]["learned"]
    exact = f"torch=={REQUIRED_TORCH_VERSION}"
    if exact not in learned:
        raise SystemExit(f"runtime contract drift: missing {exact}")

    assert_runtime_closed_v3()
    with network_blocked():
        importlib.import_module("sparkbrain.learned.backend")
        importlib.import_module("sparkbrain.external_validation.evaluation")
        importlib.import_module("sparkbrain.v03_external_validation.implementation_binding")
        importlib.import_module("scripts.run_c19_official_v3")

    print("C19 official-v3 runtime closure smoke: PASS")


if __name__ == "__main__":
    main()
