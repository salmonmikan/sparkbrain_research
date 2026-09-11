from __future__ import annotations

import pytest

from sparkbrain.research.rv02_rd005_gate_construction import (
    INHERITED_MAXIMUM_LAG_MS,
    INHERITED_MINIMUM_LAG_MS,
    ConnectionSnapshot,
    EligibilityEvent,
    ExternalReturnEvent,
    RD005GateConstruction,
)


def _construction() -> RD005GateConstruction:
    return RD005GateConstruction(
        eligibility_events=(
            EligibilityEvent("eligibility-a", 10, 10.0),
            EligibilityEvent("eligibility-b", 11, 10.0),
        ),
        return_events=(
            ExternalReturnEvent(
                "return-a",
                "eligibility-a",
                20,
                12.0,
                outcome_blind=True,
            ),
        ),
        connections=(
            ConnectionSnapshot(10, 20, plastic=True, initial_weight=0.25),
        ),
        shuffled_assignment={10: 11, 11: 10},
    )


def test_e1_es_share_event_budget_but_retain_assignment_reachability_difference() -> None:
    construction = _construction()
    e1 = construction.certificates("E1")
    es = construction.certificates("ES")

    assert len(e1) == len(es) == 1
    assert e1[0].eligibility_event_id == es[0].eligibility_event_id
    assert e1[0].return_event_id == es[0].return_event_id
    assert e1[0].trace_time_ms == es[0].trace_time_ms
    assert e1[0].return_time_ms == es[0].return_time_ms
    assert e1[0].target_id == es[0].target_id
    assert e1[0].observed_source_id == es[0].observed_source_id

    assert e1[0].assigned_source_id == 10
    assert e1[0].reachable is True
    assert es[0].assigned_source_id == 11
    assert es[0].edge_exists is False
    assert es[0].reachable is False

    summary = construction.assert_development_matrix_reachable()
    assert summary.eligibility_event_count == 2
    assert summary.return_event_count == 1
    assert summary.e1_reachable_count == 1
    assert summary.es_reachable_count == 0
    assert len(summary.shared_budget_sha256) == 64


def test_lag_window_boundaries_are_inherited_and_inclusive() -> None:
    construction = RD005GateConstruction(
        eligibility_events=(
            EligibilityEvent("lower", 1, 10.0),
            EligibilityEvent("upper", 2, 10.0),
        ),
        return_events=(
            ExternalReturnEvent(
                "lower-return",
                "lower",
                9,
                10.0 + INHERITED_MINIMUM_LAG_MS,
            ),
            ExternalReturnEvent(
                "upper-return",
                "upper",
                9,
                10.0 + INHERITED_MAXIMUM_LAG_MS,
            ),
        ),
        connections=(
            ConnectionSnapshot(1, 9, plastic=True, initial_weight=0.0),
            ConnectionSnapshot(2, 9, plastic=True, initial_weight=0.5),
        ),
        shuffled_assignment={1: 2, 2: 1},
    )
    assert [row.reachable for row in construction.certificates("E1")] == [True, True]


def test_outcome_dependent_return_schedule_fails_closed() -> None:
    with pytest.raises(ValueError, match="outcome-blind"):
        RD005GateConstruction(
            eligibility_events=(
                EligibilityEvent("eligibility-a", 10, 10.0),
                EligibilityEvent("eligibility-b", 11, 10.0),
            ),
            return_events=(
                ExternalReturnEvent(
                    "return-a",
                    "eligibility-a",
                    20,
                    12.0,
                    outcome_blind=False,
                ),
            ),
            connections=(
                ConnectionSnapshot(10, 20, plastic=True, initial_weight=0.25),
            ),
            shuffled_assignment={10: 11, 11: 10},
        )


def test_es_assignment_must_be_a_nonidentity_bijection() -> None:
    with pytest.raises(ValueError, match="must not preserve"):
        RD005GateConstruction(
            eligibility_events=(
                EligibilityEvent("eligibility-a", 10, 10.0),
                EligibilityEvent("eligibility-b", 11, 10.0),
            ),
            return_events=(
                ExternalReturnEvent("return-a", "eligibility-a", 20, 12.0),
            ),
            connections=(
                ConnectionSnapshot(10, 20, plastic=True, initial_weight=0.25),
            ),
            shuffled_assignment={10: 10, 11: 11},
        )


def test_d1_fails_closed_when_causal_arm_has_no_reachable_gate() -> None:
    construction = RD005GateConstruction(
        eligibility_events=(
            EligibilityEvent("eligibility-a", 10, 10.0),
            EligibilityEvent("eligibility-b", 11, 10.0),
        ),
        return_events=(
            ExternalReturnEvent("return-a", "eligibility-a", 20, 20.0),
        ),
        connections=(
            ConnectionSnapshot(10, 20, plastic=True, initial_weight=0.25),
        ),
        shuffled_assignment={10: 11, 11: 10},
    )

    certificate = construction.certificates("E1")[0]
    assert certificate.edge_exists is True
    assert certificate.lag_in_window is False
    assert certificate.reachable is False
    with pytest.raises(RuntimeError, match="RD005 D1 failed"):
        construction.assert_development_matrix_reachable()


def test_nonplastic_or_negative_edges_remain_certified_unreachable() -> None:
    construction = RD005GateConstruction(
        eligibility_events=(
            EligibilityEvent("nonplastic", 1, 1.0),
            EligibilityEvent("negative", 2, 1.0),
        ),
        return_events=(
            ExternalReturnEvent("gate-1", "nonplastic", 9, 2.0),
            ExternalReturnEvent("gate-2", "negative", 9, 2.0),
        ),
        connections=(
            ConnectionSnapshot(1, 9, plastic=False, initial_weight=0.2),
            ConnectionSnapshot(2, 9, plastic=True, initial_weight=-0.2),
        ),
        shuffled_assignment={1: 2, 2: 1},
    )

    certificates = construction.certificates("E1")
    assert certificates[0].edge_exists is True
    assert certificates[0].edge_plastic is False
    assert certificates[0].reachable is False
    assert certificates[1].nonnegative_initial_weight is False
    assert certificates[1].reachable is False
