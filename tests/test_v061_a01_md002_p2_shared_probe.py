from __future__ import annotations

from scripts.run_v061_a01_md002_p2_shared_probe import (
    build_registered_fixture_and_schedule,
)
from sparkbrain.v061_a01.md002_p2_shared_probe import execute_p2_shared_probe


def test_shared_probe_executes_fixed_four_condition_matrix() -> None:
    fixture, schedule = build_registered_fixture_and_schedule()
    result = execute_p2_shared_probe(fixture, schedule)
    assert len(result.observations) == 8
    assert result.verdict in {"SUPPORTED_SELECTIVE_CIRCULATION", "NOT_SUPPORTED"}
    state = result.state_dict()
    assert state["development_only"] is True
    assert state["held_out_executed"] is False
    assert state["formal_execution_opened"] is False
    assert state["threshold_tuned"] is False
    assert state["criteria"] == [
        "withheld arms remain co-maximal at the shared root",
        "returned evidence changes only the causally addressed local target confidence",
        "exact-match raises and selects the requested target",
        "exact-contradiction lowers and deselects the requested target",
        "world permutation swaps match/contradiction status for each fixed proposal identity",
        "predicted arrival times remain unchanged by causal-support credit",
    ]


def test_shared_probe_retains_world_only_withheld_controls() -> None:
    fixture, schedule = build_registered_fixture_and_schedule()
    result = execute_p2_shared_probe(fixture, schedule)
    by_key = {
        (row.world_arm, row.returned_external_evidence, row.proposal_id): row
        for row in result.observations
    }
    for proposal_id in ("child", "other"):
        control = by_key[("control", False, proposal_id)]
        intervention = by_key[("intervention", False, proposal_id)]
        assert control.probe_rows == intervention.probe_rows
        assert len(control.selected_targets) == 2
        assert len(intervention.selected_targets) == 2
