from __future__ import annotations

import pytest

from sparkbrain.research.rv01.physical_learner_bridge import build_physical_field
from sparkbrain.research.rv02_recruitment import PORTS
from sparkbrain.research.rv02_rd004_probe_clock import (
    RD004_HORIZON_MS,
    prepare_rd004_probe_snapshot,
    run_rd004_probe,
    score_rd004_probe,
)


def probe_field():
    field = build_physical_field(
        unit_count=37,
        directed_edges=((0, 36), (36, 1)),
        threshold=0.5,
        initial_weight=0.6,
        initial_delay_ms=5.0,
    )
    field.receptor_ids = PORTS
    field.run_until(250.0)
    return field


def test_rd004_snapshot_uses_relative_tail_and_washout_after_training_clock() -> None:
    field = probe_field()
    prepared = prepare_rd004_probe_snapshot(field)

    assert prepared["source_clock_ms"] == 250.0
    assert prepared["tail_end_ms"] == 256.5
    assert prepared["cue_time_ms"] == 356.5
    assert prepared["snapshot_state"]["current_time_ms"] == 356.5
    assert field.current_time_ms == 250.0

    with pytest.raises(ValueError, match="washout is fixed"):
        prepare_rd004_probe_snapshot(field, washout_ms=99.0)


def test_rd004_probe_runs_when_old_absolute_100ms_cue_would_be_in_the_past() -> None:
    prepared = prepare_rd004_probe_snapshot(probe_field())
    natural = run_rd004_probe(
        prepared["snapshot_state"],
        0,
        cut_hidden_boundary=False,
    )
    cut = run_rd004_probe(
        prepared["snapshot_state"],
        0,
        cut_hidden_boundary=True,
    )

    assert natural["status"] == "complete"
    assert cut["status"] == "complete"
    assert natural["cue_time_ms"] == cut["cue_time_ms"] == 356.5
    assert natural["shared_snapshot_hash"] == cut["shared_snapshot_hash"]
    assert natural["shared_connection_hash"] == cut["shared_connection_hash"]
    assert natural["probe_connection_hash_before"] == natural["probe_connection_hash_after"]
    assert cut["probe_connection_hash_before"] == cut["probe_connection_hash_after"]
    assert natural["final_clock_ms"] == 356.5 + RD004_HORIZON_MS

    natural_score = score_rd004_probe(
        natural["spikes"],
        (0, 1),
        37,
        cue_time_ms=natural["cue_time_ms"],
    )
    cut_score = score_rd004_probe(
        cut["spikes"],
        (0, 1),
        37,
        cue_time_ms=cut["cue_time_ms"],
    )
    assert natural_score["ordered_retention"] == 1.0
    assert cut_score["ordered_retention"] == 0.0


def test_rd004_scoring_excludes_forced_cue_at_relative_anchor() -> None:
    cue = 5000.0
    score = score_rd004_probe(
        [
            {"time_ms": cue, "unit_id": 0},
            {"time_ms": cue + 5.0, "unit_id": 1},
        ],
        (0, 1),
        37,
        cue_time_ms=cue,
    )
    assert score["ordered_retention"] == 1.0
    assert score["cue_recurrence_spikes"] == 0
