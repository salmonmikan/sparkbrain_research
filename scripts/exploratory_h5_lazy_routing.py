"""EXPLORATORY / NON_EVIDENTIARY H5 lazy-routing operation-accounting probe."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass

DECAY = 0.97
DEFAULT_HORIZON = 200
DEFAULT_DEGREE = 8
DEFAULT_SIZES = (100, 400, 1600)
DEFAULT_ACTIVITY_RATES = (0.01, 0.05, 0.10, 0.25, 0.50, 1.00)


@dataclass(frozen=True)
class ScenarioResult:
    n_nodes: int
    out_degree: int
    horizon: int
    activity_rate: float
    active_sources_per_step: int
    dense_work_units: int
    lazy_core_work_units: int
    lazy_to_dense_ratio: float
    break_even_extra_bookkeeping_per_active_source: float
    max_abs_state_error: float


def ring_graph(n_nodes: int, out_degree: int) -> tuple[tuple[int, ...], ...]:
    if n_nodes <= out_degree:
        raise ValueError("n_nodes must exceed out_degree")
    return tuple(
        tuple((source + offset) % n_nodes for offset in range(1, out_degree + 1))
        for source in range(n_nodes)
    )


def active_sources(n_nodes: int, activity_rate: float, timestep: int) -> tuple[int, ...]:
    if not 0.0 < activity_rate <= 1.0:
        raise ValueError("activity_rate must be in (0, 1]")
    count = max(1, round(n_nodes * activity_rate))
    start = (7 * timestep) % n_nodes
    return tuple((start + offset) % n_nodes for offset in range(count))


def message_value(source: int, timestep: int, out_degree: int) -> float:
    sign = 1.0 if (17 * source + 31 * timestep) % 2 == 0 else -1.0
    return sign / out_degree


def accounting_only(
    n_nodes: int,
    activity_rate: float,
    *,
    horizon: int = DEFAULT_HORIZON,
    out_degree: int = DEFAULT_DEGREE,
) -> tuple[int, int, float, float]:
    active_per_step = max(1, round(n_nodes * activity_rate))
    active_events = horizon * active_per_step
    edge_count = n_nodes * out_degree
    message_adds = active_events * out_degree

    # Dense-equivalent accounting: touch every node and inspect every edge each step,
    # then perform the same successful message additions as the lazy implementation.
    dense_work = n_nodes * horizon + edge_count * horizon + message_adds

    # Conservative lazy accounting: one queue/source touch, one edge traversal,
    # one destination-state touch and one addition per delivered message, plus a
    # final materialization/read of every node. This intentionally does not give
    # lazy routing a free pass for bookkeeping.
    lazy_core_work = active_events + 3 * message_adds + n_nodes
    ratio = lazy_core_work / dense_work
    slack = dense_work - lazy_core_work
    break_even_extra = slack / active_events
    return dense_work, lazy_core_work, ratio, break_even_extra


def run_scenario(
    n_nodes: int,
    activity_rate: float,
    *,
    horizon: int = DEFAULT_HORIZON,
    out_degree: int = DEFAULT_DEGREE,
) -> ScenarioResult:
    graph = ring_graph(n_nodes, out_degree)
    dense = [0.0] * n_nodes
    lazy = [0.0] * n_nodes
    last_touch = [-1] * n_nodes

    for timestep in range(horizon):
        dense = [value * DECAY for value in dense]
        sources = active_sources(n_nodes, activity_rate, timestep)

        for source in sources:
            value = message_value(source, timestep, out_degree)
            for destination in graph[source]:
                dense[destination] += value

                gap = timestep - last_touch[destination]
                if gap > 0:
                    lazy[destination] *= DECAY**gap
                lazy[destination] += value
                last_touch[destination] = timestep

    for index, touched_at in enumerate(last_touch):
        if touched_at >= 0 and touched_at < horizon - 1:
            lazy[index] *= DECAY ** ((horizon - 1) - touched_at)

    max_error = max(
        abs(dense_value - lazy_value)
        for dense_value, lazy_value in zip(dense, lazy, strict=True)
    )
    dense_work, lazy_work, ratio, break_even_extra = accounting_only(
        n_nodes,
        activity_rate,
        horizon=horizon,
        out_degree=out_degree,
    )
    return ScenarioResult(
        n_nodes=n_nodes,
        out_degree=out_degree,
        horizon=horizon,
        activity_rate=activity_rate,
        active_sources_per_step=max(1, round(n_nodes * activity_rate)),
        dense_work_units=dense_work,
        lazy_core_work_units=lazy_work,
        lazy_to_dense_ratio=ratio,
        break_even_extra_bookkeeping_per_active_source=break_even_extra,
        max_abs_state_error=max_error,
    )


def build_report() -> dict[str, object]:
    scenarios = [
        asdict(run_scenario(n_nodes, rate))
        for n_nodes in DEFAULT_SIZES
        for rate in DEFAULT_ACTIVITY_RATES
    ]
    return {
        "status": "EXPLORATORY_NON_EVIDENTIARY",
        "hypothesis": (
            "H5 lazy decay/event routing can reduce audited algorithmic work in sparse regimes"
        ),
        "decay": DECAY,
        "horizon": DEFAULT_HORIZON,
        "out_degree": DEFAULT_DEGREE,
        "scenarios": scenarios,
    }


def main() -> None:
    print(json.dumps(build_report(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
