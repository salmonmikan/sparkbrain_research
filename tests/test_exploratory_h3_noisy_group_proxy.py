from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

MODULE_PATH = (
    Path(__file__).parents[1]
    / "scripts"
    / "exploratory_h3_noisy_group_proxy.py"
)
SPEC = importlib.util.spec_from_file_location(
    "exploratory_h3_noisy_group_proxy",
    MODULE_PATH,
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_fixed_corruption_grid_and_information_symmetry() -> None:
    result = MODULE.run_probe()
    contract = result["synthetic_contract"]

    assert contract["corruption_rates"] == [0.0, 0.1, 0.25, 0.5, 1.0]
    assert contract["samples"] == 4096
    assert contract["world_seed"] == 1337
    assert contract["proxy_seed"] == 20260918
    assert len(result["rows"]) == 5


def test_non_proxy_baselines_are_invariant_to_proxy_corruption() -> None:
    rows = MODULE.run_probe()["rows"]
    naive = {row["accuracy"]["naive"] for row in rows}
    source_dedup = {row["accuracy"]["source_dedup"] for row in rows}

    assert len(naive) == 1
    assert len(source_dedup) == 1


def test_probe_is_deterministic_and_non_evidentiary() -> None:
    first = MODULE.run_probe()
    second = MODULE.run_probe()

    assert first == second
    assert first["evidentiary_status"] == "NON_EVIDENTIARY"
