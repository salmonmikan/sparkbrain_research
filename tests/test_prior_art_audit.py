from __future__ import annotations

import importlib.util
from pathlib import Path


def load_validator():
    path = Path(__file__).resolve().parents[1] / "scripts/validate_prior_art_audit.py"
    spec = importlib.util.spec_from_file_location("validate_prior_art_audit", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_prior_art_matrix_and_generated_report_are_consistent() -> None:
    validator = load_validator()
    assert validator.validate() == []


def test_every_required_target_has_a_ranked_counterexample() -> None:
    validator = load_validator()
    rows = validator.load_rows()
    for target in validator.TARGETS:
        assert validator.strongest(rows, target)
