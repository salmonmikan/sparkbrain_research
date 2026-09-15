from __future__ import annotations

from scripts.run_v061_a01_md002_p2_shared_probe import build_registered_fixture_and_schedule
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


def test_shared_probe_reports_fixed_selective_circulation_criterion() -> None:
    fixture, schedule = build_registered_fixture_and_schedule()
    result = execute_p2_shared_probe(fixture, schedule)
    # This is the prospectively fixed development criterion. If the mechanism
    # does not satisfy it, the experiment must return NOT_SUPPORTED rather than
    # changing the criterion after observing output.
    assert result.verdict == "SUPPORTED_SELECTIVE_CIRCULATION"
