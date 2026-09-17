from scripts.exploratory_h7_trace_causality import build_report, scenario


def test_no_bypass_makes_traced_route_fully_causal() -> None:
    result = scenario(0.0)

    assert result.baseline_accuracy == 1.0
    assert result.route_stability == 1.0
    assert result.trace_deletion_accuracy == 0.0
    assert result.wrong_route_replacement_accuracy == 0.0
    assert result.deletion_sensitivity == 1.0
    assert result.replacement_sensitivity == 1.0


def test_complete_bypass_masks_trace_interventions() -> None:
    result = scenario(1.0)

    assert result.baseline_accuracy == 1.0
    assert result.route_stability == 1.0
    assert result.trace_deletion_accuracy == 1.0
    assert result.wrong_route_replacement_accuracy == 1.0
    assert result.deletion_sensitivity == 0.0
    assert result.replacement_sensitivity == 0.0


def test_fixed_bypass_grid_separates_stability_from_causal_sensitivity() -> None:
    report = build_report()
    scenarios = report["scenarios"]

    assert report["status"] == "EXPLORATORY_NON_EVIDENTIARY"
    assert report["summary"]["route_stability_all_scenarios"] is True
    assert report["summary"]["baseline_accuracy_all_scenarios"] is True
    assert report["summary"]["deletion_sensitivity_range"] == [0.0, 1.0]
    assert report["summary"]["replacement_sensitivity_range"] == [0.0, 1.0]
    assert [item["trace_deletion_accuracy"] for item in scenarios] == [
        0.0,
        0.25,
        0.5,
        0.75,
        1.0,
    ]
