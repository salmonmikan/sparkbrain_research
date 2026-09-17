from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

MODULE_PATH = (
    Path(__file__).parents[1]
    / "scripts"
    / "exploratory_h2_residual_memory_reduction.py"
)
SPEC = importlib.util.spec_from_file_location(
    "exploratory_h2_residual_memory_reduction",
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


def test_dev_and_test_seeds_are_disjoint() -> None:
    contract = MODULE.run_probe()["synthetic_contract"]

    assert set(contract["dev_seeds"]).isdisjoint(contract["test_seeds"])
    assert contract["episodes_per_seed"] == 512
    assert contract["b_dwell_steps"] == [2, 4, 8, 16]


def test_symmetric_recurrent_wins_fixed_test_utilities() -> None:
    rows = MODULE.run_probe()["rows"]

    assert len(rows) == 7
    assert all(
        row["symmetric_minus_residual_test_utility"] > 0.0
        for row in rows
    )
