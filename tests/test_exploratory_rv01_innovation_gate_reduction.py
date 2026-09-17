from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parents[1]
MODULE_PATH = ROOT / "scripts" / "exploratory_rv01_innovation_gate_reduction.py"
sys.path.insert(0, str(ROOT / "scripts"))
RESULT_PATH = (
    ROOT / "artifacts" / "exploratory_rv01_innovation_gate_reduction" / "result.json"
)

SPEC = importlib.util.spec_from_file_location("exploratory_rv01_innovation_gate_reduction", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def _normalized(value: Any) -> Any:
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
    assert first["mode"] == "exploratory_incubator"
    assert first["summary"]["hard_stop_reached"] is True
    assert first["summary"]["promotion_recommendation"] == "REJECT"


def test_committed_result_matches_probe() -> None:
    committed = json.loads(RESULT_PATH.read_text(encoding="utf-8"))

    assert _normalized(committed) == _normalized(MODULE.run_probe())


def test_dev_test_are_disjoint_and_resources_are_matched() -> None:
    result = MODULE.run_probe()
    contract = result["synthetic_contract"]

    assert set(contract["dev_seeds"]).isdisjoint(contract["test_seeds"])
    assert "exactly one persistent scalar" in contract["resource_match"]
    assert "exactly two controls on DEV only" in contract["resource_match"]
    assert "No TEST-driven comparator selection or tuning" in contract["selection_rule"]


def test_fixed_dev_selection_matches_expected_predeclared_search() -> None:
    selected = MODULE.run_probe()["selected_on_dev"]

    assert selected["deadzone_delay_learner"] == {
        "eta": 0.8,
        "deadzone_ms": 0.35,
    }
    assert selected["generic_innovation_gated_ewma"] == {
        "alpha": 0.65,
        "gate_threshold_ms": 0.75,
    }


def test_stronger_generic_filter_exposes_regime_dependent_crossover() -> None:
    result = MODULE.run_probe()
    deltas = [float(row["generic_minus_deadzone_utility"]) for row in result["rows"]]

    assert result["summary"]["deadzone_wins"] == 3
    assert result["summary"]["generic_wins"] == 2
    assert result["summary"]["crossover_observed"] is True
    assert all(delta < 0.0 for delta in deltas[:3])
    assert all(delta > 0.0 for delta in deltas[3:])
