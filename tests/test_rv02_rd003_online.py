from __future__ import annotations

from sparkbrain.research.rv02_hidden_eligibility import HiddenEligibilityTrace
from sparkbrain.research.rv02_rd003_online import (
    RD003_GAIN,
    _budget_rows,
    _training_schedule,
    planned_rd003_cells,
)
from sparkbrain.research.rv02_scale import ScaleStudyConfig, development_worlds


def trace(unit_id: int, time_ms: float, magnitude: float) -> HiddenEligibilityTrace:
    return HiddenEligibilityTrace(
        observed_unit_id=unit_id,
        assigned_source_id=unit_id,
        time_ms=time_ms,
        magnitude=magnitude,
        event_id=f"trace-{unit_id}-{time_ms}",
        source_pulse_ids=("source",),
    )


def test_rd003_matrix_and_gain_are_fixed() -> None:
    config = ScaleStudyConfig()
    cells = planned_rd003_cells(config)
    assert len(cells) == 18
    assert {scale for _, scale in cells} == {1, 3, 10}
    assert RD003_GAIN == 4.0


def test_rd003_training_schedule_is_deterministic_and_semantically_anonymous() -> None:
    world = development_worlds(ScaleStudyConfig())[0]
    first = _training_schedule(world)
    second = _training_schedule(world)
    assert first == second
    assert len(first) == sum(
        len(route) * exposures
        for route, exposures in zip(world["routes"], world["exposures"], strict=True)
    )
    assert [row["ordinal"] for row in first] == list(range(len(first)))
    assert all(row["event_id"] == f"rd003-ext-{row['ordinal']:06d}" for row in first)
    assert all("route" not in row["event_id"] for row in first)
    assert all(
        right["time_ms"] > left["time_ms"]
        for left, right in zip(first, first[1:], strict=False)
    )


def test_rd003_eligibility_budget_ignores_only_shuffled_assignment_identity() -> None:
    causal = [trace(40, 5.0, 0.8), trace(41, 6.0, 1.1)]
    shuffled = [
        HiddenEligibilityTrace(
            observed_unit_id=40,
            assigned_source_id=41,
            time_ms=5.0,
            magnitude=0.8,
            event_id="shuffled-a",
            source_pulse_ids=("source",),
        ),
        HiddenEligibilityTrace(
            observed_unit_id=41,
            assigned_source_id=40,
            time_ms=6.0,
            magnitude=1.1,
            event_id="shuffled-b",
            source_pulse_ids=("source",),
        ),
    ]
    assert _budget_rows(causal) == _budget_rows(shuffled)

    mismatched = list(shuffled)
    mismatched[1] = HiddenEligibilityTrace(
        observed_unit_id=41,
        assigned_source_id=40,
        time_ms=6.5,
        magnitude=1.1,
        event_id="shuffled-c",
        source_pulse_ids=("source",),
    )
    assert _budget_rows(causal) != _budget_rows(mismatched)
