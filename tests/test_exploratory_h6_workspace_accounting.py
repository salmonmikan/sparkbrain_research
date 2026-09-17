import math

from scripts.exploratory_h6_workspace_accounting import build_report, scenario


def test_perfect_direct_router_matches_small_fanout_and_saturates_budget() -> None:
    assert math.isclose(scenario(1, 1.0).direct_recall, 1.0)
    assert math.isclose(scenario(2, 1.0).direct_recall, 1.0)
    assert math.isclose(scenario(4, 1.0).direct_recall, 1.0)
    assert math.isclose(scenario(8, 1.0).direct_recall, 0.5)
    assert math.isclose(scenario(16, 1.0).direct_recall, 0.25)


def test_accounting_contract_flips_efficiency_conclusion() -> None:
    report = build_report()
    summary = report["summary"]

    assert summary["scenario_count"] == 20
    assert summary["shared_slot_workspace_strict_efficiency_wins"] == 19
    assert summary["shared_slot_ties"] == 1
    assert summary["recipient_charged_direct_strict_efficiency_wins"] == 20


def test_low_knowledge_case_still_depends_on_fanout_charging() -> None:
    result = scenario(8, 0.25)

    assert result.workspace_recall == 1.0
    assert result.direct_recall < 0.31
    assert (
        result.workspace_efficiency_shared_slot
        > result.direct_relevant_deliveries_per_send
    )
    assert (
        result.workspace_efficiency_recipient_charged
        < result.direct_relevant_deliveries_per_send
    )
