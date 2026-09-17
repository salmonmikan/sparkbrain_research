from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parents[1]
MODULE_PATH = ROOT / "scripts" / "exploratory_rv01_delay_filter_reduction.py"
RESULT_PATH = ROOT / "artifacts" / "exploratory_rv01_delay_filter_reduction" / "result.json"
SPEC = importlib.util.spec_from_file_location(
    "exploratory_rv01_delay_filter_reduction",
    MODULE_PATH,
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def _normalized(value: Any) -> Any:
    """Normalize insignificant cross-Python floating-point variation for artifact binding."""
    if isinstance(value, float):
        return round(value, 10)
    if isinstance(value, dict):
        return {key: _normalized(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_normalized(item) for item in value]
    return value


def test_probe_is_deterministic_and_non_evidentiary() -> None:
    first = MODULE.run_probe()
    second = MODULE.run_probe()

    assert first == second
    assert first["evidentiary_status"] == "NON_EVIDENTIARY"


def test_committed_result_matches_probe() -> None:
    committed = json.loads(RESULT_PATH.read_text(encoding="utf-8"))

    assert _normalized(committed) == _normalized(MODULE.run_probe())


def test_dev_test_are_disjoint_and_resources_are_matched() -> None:
    contract = MODULE.run_probe()["synthetic_contract"]

    assert set(contract["dev_seeds"]).isdisjoint(contract["test_seeds"])
    assert "one persistent scalar delay estimate" in contract["resource_match"]
    assert "exactly two control parameters" in contract["resource_match"]


def test_fixed_parameter_sensitivity_has_a_crossover() -> None:
    result = MODULE.run_probe()
    selected = result["selected_on_dev"]
    rows = result["rows"]

    assert selected["deadzone_delay_learner"] == {"eta": 0.8, "deadzone_ms": 0.35}
    assert selected["generic_clipped_ewma"] == {
        "alpha": 0.65,
        "innovation_clip_ms": 4.0,
    }
    assert result["summary"] == {
        "deadzone_wins": 4,
        "generic_wins": 1,
        "crossover_observed": True,
    }
    assert float(rows[0]["generic_minus_deadzone_utility"]) < 0.0
    assert float(rows[-1]["generic_minus_deadzone_utility"]) > 0.0
