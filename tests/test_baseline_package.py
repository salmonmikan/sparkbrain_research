from __future__ import annotations

from sparkbrain.baselines import (
    BaselineStep,
    EvidenceAccumulator,
    HardWinnerTakeAll,
    InstantClassifier,
    run_baseline,
)
from sparkbrain.baselines.classic import EvidenceAccumulator as DirectAccumulator
from sparkbrain.worlds import SwitchWorld


def test_legacy_and_direct_baseline_imports_share_symbols() -> None:
    assert DirectAccumulator is EvidenceAccumulator
    assert BaselineStep.__module__ == "sparkbrain.baselines.classic"
    assert HardWinnerTakeAll.name == "hard_wta"
    assert InstantClassifier.name == "instant"


def test_legacy_baseline_results_and_inspection_are_compatible() -> None:
    events = SwitchWorld.canonical_scenario()
    model = EvidenceAccumulator()
    rows = run_baseline(model, events)
    before = model.work_counters()
    probabilities = model.predict_proba()
    state = model.state_trace()
    assert len(rows) == len(events)
    assert rows[-1].prediction == "cat"
    assert abs(sum(probabilities.values()) - 1.0) < 1e-12
    assert state["prediction"] == rows[-1].prediction
    assert model.work_counters() == before


def test_reset_clears_streaming_state() -> None:
    model = EvidenceAccumulator()
    model.step(SwitchWorld.canonical_scenario()[0])
    model.reset()
    assert model.work_counters()["state_updates"] == 0
    assert model.state_trace()["prediction"] is None
