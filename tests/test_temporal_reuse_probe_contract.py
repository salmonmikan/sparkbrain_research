"""Pure helper checks: no diagnostic generator or model is executed here."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "temporal_reuse_loop_probe.py"
SPEC = importlib.util.spec_from_file_location("temporal_reuse_probe", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
probe = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(probe)


def test_literal_raster_preserves_fractional_timing_and_mass() -> None:
    obs = {"start_ms": 200.0, "pulses": [probe.pulse(208.25, "A", 1.0)]}
    vector = probe.raster(obs)
    assert len(vector) == 410
    assert sum(vector) == 1
    assert vector[8] == 0.75 and vector[9] == 0.25


def test_raster_rejects_query_suffix() -> None:
    with pytest.raises(RuntimeError, match="outside"):
        probe.raster({"start_ms": 0.0, "pulses": [probe.pulse(41, "A", 1)]})


def test_abstention_metrics_keep_all_rows() -> None:
    assert probe.hard_label(0.5) is None
    assert probe.hard_label(0.4) == 0
    assert probe.hard_label(0.6) == 1
    report = probe.metrics(
        [
            {"p1": 0.5, "native": None, "outcome": 0},
            {"p1": 0.75, "native": 1, "outcome": 1},
        ]
    )
    assert report["coverage"] == 0.5
    assert report["accuracy_all"] == 0.5
    assert report["brier"] == (0.25 + 0.0625) / 2


def prefix_row(aid: str, outcome: int) -> dict:
    return {"assembly_id": aid, "mature": True, "outcome": outcome}


def test_target_selector_requires_an_active_matched_control() -> None:
    a = [prefix_row("a", 0)] * 10
    assert probe.select_target(a)["status"] == "intervention_not_identifiable"
    result = probe.select_target(a + [prefix_row("b", 1)] * 8)
    assert result["target"] == "a" and result["matched"] == "b"
    assert probe.select_target(a + [prefix_row("b", 1)] * 7)["matched"] is None
    assert probe.select_target(a + [prefix_row("b", 1)] * 13)["matched"] is None


def test_target_label_leak_and_tie_cases_fail_closed() -> None:
    mixed = [prefix_row("a", 0)] * 10 + [prefix_row("a", 1)]
    assert probe.select_target(mixed)["target"] is None
    values = [prefix_row("z", 0)] * 10 + [prefix_row("a", 0)] * 10
    assert probe.select_target(values)["target"] == "a"


def test_explicit_network_and_nonfinite_guards() -> None:
    with pytest.raises(RuntimeError, match="network_disabled"):
        probe.deny_network("socket.connect", ())
    with pytest.raises(ValueError):
        probe.canonical({"value": float("nan")})


def test_deadline_rejects_consumed_budget_before_entering() -> None:
    with pytest.raises(RuntimeError, match="no remaining time"):
        with probe.deadline(0, 1):
            raise AssertionError("must not enter")
