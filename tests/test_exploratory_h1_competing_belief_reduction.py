from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

MODULE_PATH = (
    Path(__file__).parents[1]
    / "scripts"
    / "exploratory_h1_competing_belief_reduction.py"
)
SPEC = importlib.util.spec_from_file_location(
    "exploratory_h1_competing_belief_reduction",
    MODULE_PATH,
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_probe_is_deterministic_and_non_evidentiary() -> None:
    first = MODULE.run_probe()
    second = MODULE.run_probe()

    assert first == second
    assert first["evidentiary_status"] == "NON_EVIDENTIARY"


def test_dev_and_test_seeds_are_disjoint_and_budgets_are_matched() -> None:
    contract = MODULE.run_probe()["synthetic_contract"]

    assert set(contract["dev_seeds"]).isdisjoint(contract["test_seeds"])
    assert contract["sequences_per_seed"] == 256
    assert contract["sequence_length"] == 72
    assert "three scalar state values" in contract["memory_budget"]
    assert "two DEV-selected control parameters" in contract["memory_budget"]


def test_matched_probabilistic_baseline_is_near_equivalent_on_fixed_surface() -> None:
    summary = MODULE.run_probe()["summary"]

    assert summary["probabilistic_wins"] == 4
    assert summary["competing_wins"] == 2
    assert summary["max_absolute_test_utility_gap"] < 0.003
    assert summary["mean_absolute_test_utility_gap"] < 0.001
