from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "exploratory_h3_correlation_reduction.py"
SPEC = importlib.util.spec_from_file_location("exploratory_h3_correlation_reduction", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_correlation_aware_scalar_reduction_improves_fixed_synthetic_grid() -> None:
    result = MODULE.run_probe()
    accuracy = result["accuracy"]

    assert accuracy["naive"] < accuracy["source_dedup"]
    assert accuracy["source_dedup"] < accuracy["group_normalized"]
    assert accuracy["group_normalized"] >= 0.80
    assert abs(accuracy["group_normalized"] - accuracy["group_majority"]) < 0.01
    assert result["group_normalized_vs_group_majority_agreement"] > 0.97


def test_known_correlation_groups_prevent_distinct_source_overcounting() -> None:
    rows = MODULE.run_probe()["adversarial_correlated_sweep"]
    heavy_rows = [row for row in rows if row["correlated_wrong_sources"] >= 4]

    assert all(row["naive"] == -1 for row in heavy_rows)
    assert all(row["source_dedup"] == -1 for row in heavy_rows)
    assert all(row["group_normalized"] == 1 for row in heavy_rows)
    assert all(row["group_majority"] == 1 for row in heavy_rows)
