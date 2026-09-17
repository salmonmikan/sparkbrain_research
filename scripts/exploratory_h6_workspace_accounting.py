"""EXPLORATORY / NON_EVIDENTIARY H6 workspace accounting sensitivity probe."""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass

TOTAL_CONSUMERS = 31
DIRECT_BUDGET = 4
FANOUTS = (1, 2, 4, 8, 16)
ROUTER_KNOWLEDGE = (0.25, 0.50, 0.75, 1.00)


@dataclass(frozen=True)
class Scenario:
    fanout: int
    router_knowledge: float
    direct_expected_relevant_deliveries: float
    direct_recall: float
    direct_relevant_deliveries_per_send: float
    workspace_recall: float
    workspace_efficiency_shared_slot: float
    workspace_efficiency_recipient_charged: float


def expected_direct_deliveries(fanout: int, router_knowledge: float) -> float:
    """Exact expectation for a budgeted direct router with imperfect destination knowledge."""
    if not 1 <= fanout <= TOTAL_CONSUMERS:
        raise ValueError("fanout must be within the consumer population")
    if not 0.0 <= router_knowledge <= 1.0:
        raise ValueError("router_knowledge must be in [0, 1]")

    budget = min(DIRECT_BUDGET, fanout)
    expected = 0.0
    for known in range(fanout + 1):
        probability = (
            math.comb(fanout, known)
            * router_knowledge**known
            * (1.0 - router_knowledge) ** (fanout - known)
        )
        if known >= budget:
            delivered = float(budget)
        else:
            remaining_slots = budget - known
            remaining_relevant = fanout - known
            remaining_population = TOTAL_CONSUMERS - known
            delivered = known + (
                remaining_slots * remaining_relevant / remaining_population
            )
        expected += probability * delivered
    return expected


def scenario(fanout: int, router_knowledge: float) -> Scenario:
    direct_deliveries = expected_direct_deliveries(fanout, router_knowledge)
    direct_sends = min(DIRECT_BUDGET, fanout)

    # Two deliberately different accounting contracts expose whether an apparent
    # broadcast advantage is a property of coordination or of fan-out charging.
    # Shared-slot: one publish is charged once regardless of readership.
    # Recipient-charged: one publish plus exposure to every potential consumer.
    return Scenario(
        fanout=fanout,
        router_knowledge=router_knowledge,
        direct_expected_relevant_deliveries=direct_deliveries,
        direct_recall=direct_deliveries / fanout,
        direct_relevant_deliveries_per_send=direct_deliveries / direct_sends,
        workspace_recall=1.0,
        workspace_efficiency_shared_slot=float(fanout),
        workspace_efficiency_recipient_charged=fanout / (TOTAL_CONSUMERS + 1),
    )


def build_report() -> dict[str, object]:
    scenarios = [
        scenario(fanout, knowledge)
        for fanout in FANOUTS
        for knowledge in ROUTER_KNOWLEDGE
    ]
    shared_wins = sum(
        item.workspace_efficiency_shared_slot
        > item.direct_relevant_deliveries_per_send
        for item in scenarios
    )
    shared_ties = sum(
        math.isclose(
            item.workspace_efficiency_shared_slot,
            item.direct_relevant_deliveries_per_send,
            abs_tol=1e-12,
        )
        for item in scenarios
    )
    direct_recipient_charged_wins = sum(
        item.direct_relevant_deliveries_per_send
        > item.workspace_efficiency_recipient_charged
        for item in scenarios
    )

    return {
        "status": "EXPLORATORY_NON_EVIDENTIARY",
        "hypothesis": (
            "H6 workspace broadcast advantage may depend on fan-out accounting and "
            "direct-router destination knowledge"
        ),
        "total_consumers": TOTAL_CONSUMERS,
        "direct_budget": DIRECT_BUDGET,
        "scenarios": [asdict(item) for item in scenarios],
        "summary": {
            "scenario_count": len(scenarios),
            "shared_slot_workspace_strict_efficiency_wins": shared_wins,
            "shared_slot_ties": shared_ties,
            "recipient_charged_direct_strict_efficiency_wins": (
                direct_recipient_charged_wins
            ),
        },
    }


def main() -> None:
    print(json.dumps(build_report(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
