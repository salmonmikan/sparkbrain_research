from __future__ import annotations

import importlib
import runpy
import tomllib
from pathlib import Path

from sparkbrain.external_validation.evaluation import network_blocked
from sparkbrain.v03_external_validation import official_execution as inherited_execution
from sparkbrain.v03_external_validation.implementation_binding import (
    baseline_registry,
    condition_executor,
)
from sparkbrain.v03_external_validation.official_execution_v3 import (
    ExecutionAdmissionV3,
    OneWayExecutionHarnessV3,
    assert_runtime_closed_v3,
)
from sparkbrain.v03_external_validation.official_protocol_v3 import REQUIRED_TORCH_VERSION

ROOT = Path(__file__).resolve().parents[1]


def _synthetic_examples() -> tuple[dict[str, object], ...]:
    examples: list[dict[str, object]] = []
    for pair_index in range(inherited_execution.EXPECTED_PAIRS_PER_ROW):
        for step_index in (0, 1):
            examples.append(
                {
                    "record_id": f"synthetic-{pair_index}-step-{step_index}",
                    "source_index": pair_index,
                    "pair_index": pair_index,
                    "step_index": step_index,
                    "question": (
                        f"Synthetic premise {pair_index} step {step_index}. "
                        "What necessarily had to follow from this visible synthetic premise?"
                    ),
                    "choices": ("alpha", "beta", "gamma"),
                }
            )
    return tuple(examples)


def _run_synthetic_acquisition_smoke() -> None:
    captured: list[str] = []
    harness = OneWayExecutionHarnessV3(boundary=inherited_execution.RuntimeBoundary())
    raw = harness.acquire(
        admission=ExecutionAdmissionV3.synthetic_dev(),
        examples=_synthetic_examples(),
        condition_executor=condition_executor,
        baseline_executors=baseline_registry(),
        raw_writer=lambda bundle: captured.append(bundle.sha256),
    )
    expected = 55 * inherited_execution.EXPECTED_PAIRS_PER_ROW
    if len(raw.records) != expected:
        raise RuntimeError(f"synthetic acquisition count drift: {len(raw.records)} != {expected}")
    if captured != [raw.sha256]:
        raise RuntimeError("synthetic acquisition did not cross the bound raw-writer boundary exactly once")


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
        runpy.run_path(
            str(ROOT / "scripts/run_c19_official_v3.py"),
            run_name="c19_official_v3_runner_smoke",
        )
        _run_synthetic_acquisition_smoke()

    print("C19 official-v3 runtime closure and synthetic acquisition smoke: PASS")


if __name__ == "__main__":
    main()
