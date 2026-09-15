from __future__ import annotations

from scripts.run_v061_a01_md002_p2_shared_probe import (
    build_registered_fixture_and_schedule,
)
from sparkbrain.v061_a01.md002_p2_raw_pipeline import (
    P2SharedProbeRaw,
    acquire_p2_shared_probe,
    score_preserved_p2_shared_probe,
)


def test_raw_acquisition_contains_no_verdict() -> None:
    fixture, schedule = build_registered_fixture_and_schedule()
    raw = acquire_p2_shared_probe(fixture, schedule)
    state = raw.state_dict()
    assert state["scored"] is False
    assert "verdict" not in state
    assert len(state["observations"]) == 8


def test_preserved_raw_round_trip_then_score() -> None:
    fixture, schedule = build_registered_fixture_and_schedule()
    acquired = acquire_p2_shared_probe(fixture, schedule)
    restored = P2SharedProbeRaw.from_state_dict(acquired.state_dict())
    result = score_preserved_p2_shared_probe(restored)
    assert result.verdict in {"SUPPORTED_SELECTIVE_CIRCULATION", "NOT_SUPPORTED"}
    assert result.criteria == restored.criteria
