from __future__ import annotations

from sparkbrain.h5_work import dev_validate, quality_pass, score_rows, type7_quantile


def test_h5_dev_equivalence_and_counter_closure() -> None:
    rows = dev_validate()
    assert {row["family"] for row in rows} == {"uniform", "clustered", "bursty"}
    assert all(quality_pass(row) for row in rows)
    for row in rows:
        candidate = row["candidate_counters"]
        dense = row["dense_counters"]
        assert candidate["queue_pushes"] == candidate["queue_pops"]
        assert dense["queue_pushes"] == dense["queue_pops"]
        assert dense["route_edge_checks"] >= candidate["route_edge_checks"]
        assert dense["state_touches"] >= candidate["state_touches"]


def test_h5_type7_quantile_fixture() -> None:
    values = [0.0, 1.0, 2.0, 3.0, 4.0]
    assert type7_quantile(values, 0.0) == 0.0
    assert type7_quantile(values, 0.25) == 1.0
    assert type7_quantile(values, 0.5) == 2.0
    assert type7_quantile(values, 0.75) == 3.0
    assert type7_quantile(values, 1.0) == 4.0


def test_h5_scorer_rejects_quality_failure_before_work_classification() -> None:
    row = {
        "family": "uniform",
        "size": 128,
        "activity_fraction": 0.01,
        "horizon": 24,
        "seed": 51001,
        "candidate_work": 100,
        "dense_work": 200,
        "max_abs_activation_error": 1e-4,
        "fired_counts_exact": True,
        "events_processed_exact": True,
        "queue_empty_exact": True,
    }
    assert score_rows([row])["classification"] == "INVALID_QUALITY_GUARD"
