from __future__ import annotations

from sparkbrain.comparison.cx01.schedule import build_balanced_exposure_schedule
from sparkbrain.comparison.cx01.scoring import FamilyEvidence, decide_family
from sparkbrain.comparison.cx01.worlds import CX01Family


def test_balanced_schedule_matches_v06_fairness_shape() -> None:
    schedule = build_balanced_exposure_schedule((6, 5, 4))
    assert tuple(row.sequence_index for row in schedule.episodes[:12]) == (
        0,
        1,
        2,
        2,
        1,
        0,
        0,
        1,
        2,
        2,
        1,
        0,
    )
    assert tuple(row.sequence_index for row in schedule.episodes[-3:]) == (0, 1, 0)
    assert len(schedule.schedule_hash()) == 64


def test_family_gates_are_non_compensatory() -> None:
    high_order = decide_family(
        FamilyEvidence(CX01Family.HIGH_ORDER, correct_probes=2, total_probes=2)
    )
    timing = decide_family(FamilyEvidence(CX01Family.TIMING, correct_probes=1, total_probes=2))
    selectivity = decide_family(FamilyEvidence(CX01Family.SELECTIVITY, selective_effect=0.49))
    loop = decide_family(
        FamilyEvidence(
            CX01Family.LOOP,
            correct_probes=1,
            total_probes=1,
            self_confirmation_violations=1,
        )
    )
    assert high_order.passed
    assert not timing.passed
    assert not selectivity.passed
    assert not loop.passed


def test_cycle_requires_both_accuracy_and_reacquisition() -> None:
    assert decide_family(
        FamilyEvidence(
            CX01Family.CYCLE,
            cycle_correct_fraction=1.0,
            maximum_reacquisition_observations=2,
        )
    ).passed
    assert not decide_family(
        FamilyEvidence(
            CX01Family.CYCLE,
            cycle_correct_fraction=1.0,
            maximum_reacquisition_observations=3,
        )
    ).passed
