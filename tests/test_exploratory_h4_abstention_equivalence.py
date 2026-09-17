from scripts.exploratory_h4_abstention_equivalence import (
    build_examples,
    build_report,
    matched_feature_frontier,
    workspace_no_ignition_metrics,
)


def test_workspace_gate_has_fixed_selective_profile() -> None:
    examples = build_examples()
    result = workspace_no_ignition_metrics(examples)

    assert result.accepted == 48
    assert result.total == 192
    assert result.coverage == 0.25
    assert result.selective_risk == 0.125


def test_matched_feature_abstention_can_dominate_workspace_gate() -> None:
    examples = build_examples()
    frontier = matched_feature_frontier(examples)
    threshold_point = next(point for point in frontier if point["threshold"] == 0.8)

    assert threshold_point["accepted"] == 52
    assert threshold_point["coverage"] == 0.2708333333333333
    assert threshold_point["selective_risk"] == 0.11538461538461542


def test_report_separates_weak_and_information_matched_comparators() -> None:
    report = build_report()
    comparison = report["comparison"]

    assert report["status"] == "EXPLORATORY_NON_EVIDENTIARY"
    assert comparison["workspace_dominated_when_information_matched"] is True
    assert comparison["matched_feature_dominator_count"] == 1
    assert comparison["best_margin_only_at_or_above_workspace_coverage"] == {
        "threshold": 0.8,
        "accepted": 64,
        "total": 192,
        "coverage": 0.3333333333333333,
        "selective_risk": 0.21875,
    }
