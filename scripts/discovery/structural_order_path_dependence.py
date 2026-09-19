#!/usr/bin/env python3
"""EXPLORATORY / NON_EVIDENTIARY structural-order path-dependence probe.

This standalone synthetic probe mirrors the structural event-selection/apply semantics
relevant to source-module activation, duplicate/prune, edge grow/prune, event priority,
per-boundary cap, and total run budget. It never reads repository datasets, checkpoints,
held-out TEST, preserved formal raw, or official scorers.

Question: for the same multiset of unlabeled routing-load and edge-credit frames, how
sensitive is the final structural graph to observation order, and is that sensitivity
explained only by the finite total event budget?
"""
from __future__ import annotations

from dataclasses import dataclass
import json
import random
import statistics

MAX_MODULES = 18
SOURCE_MODULES = 12
MAX_ACTIVE_EDGES = 96
MAX_EVENTS_PER_BOUNDARY = 2
MIN_LIVE_MODULES = 6
MIN_IN_DEGREE = 1
LOAD_HIGH = 1.65
LOAD_LOW = 0.12
GROW_CREDIT = 0.08
PRUNE_CREDIT = 0.005
EVENT_PRIORITY = {
    "edge_prune": 10,
    "module_prune": 20,
    "duplicate": 50,
    "edge_grow": 70,
}


@dataclass(frozen=True)
class Frame:
    routing_load: tuple[float, ...]
    edge_credit: tuple[tuple[float, ...], ...]


class ControllerSim:
    def __init__(self, *, total_budget: int, enabled: frozenset[str]) -> None:
        self.active = [False] * MAX_MODULES
        for index in range(SOURCE_MODULES):
            self.active[index] = True
        self.edges = [[False] * MAX_MODULES for _ in range(MAX_MODULES)]
        for index in range(SOURCE_MODULES):
            self.edges[index][index] = True
            self.edges[index][(index + 1) % SOURCE_MODULES] = True
        self.remaining_budget = total_budget
        self.enabled = enabled
        self.applied_events = 0

    def discover(self, frame: Frame) -> list[tuple[float, str, int | None, int | None]]:
        active = [index for index, value in enumerate(self.active) if value]
        inactive = [index for index, value in enumerate(self.active) if not value]
        total = sum(frame.routing_load[index] for index in active) or 1.0
        mean_load = total / len(active)
        candidates: list[tuple[float, str, int | None, int | None]] = []

        if "duplicate" in self.enabled and inactive:
            overloaded = max(active, key=lambda index: frame.routing_load[index])
            ratio = frame.routing_load[overloaded] / max(mean_load, 1e-9)
            if ratio >= LOAD_HIGH:
                candidates.append((ratio, "duplicate", overloaded, inactive[0]))

        if "module_prune" in self.enabled and len(active) > MIN_LIVE_MODULES:
            underused = min(active, key=lambda index: frame.routing_load[index])
            ratio = frame.routing_load[underused] / max(mean_load, 1e-9)
            if ratio <= LOAD_LOW:
                candidates.append((1.0 - ratio, "module_prune", underused, None))

        best_grow: tuple[float, int, int] | None = None
        best_prune: tuple[float, int, int] | None = None
        for source in active:
            for target in active:
                credit = frame.edge_credit[source][target]
                if (
                    "edge_grow" in self.enabled
                    and not self.edges[source][target]
                    and credit >= GROW_CREDIT
                    and (best_grow is None or credit > best_grow[0])
                ):
                    best_grow = (credit, source, target)
                if (
                    "edge_prune" in self.enabled
                    and self.edges[source][target]
                    and credit <= PRUNE_CREDIT
                    and (best_prune is None or credit < best_prune[0])
                ):
                    best_prune = (credit, source, target)

        if best_grow is not None:
            candidates.append((best_grow[0], "edge_grow", best_grow[1], best_grow[2]))
        if best_prune is not None:
            candidates.append((1.0 - best_prune[0], "edge_prune", best_prune[1], best_prune[2]))

        candidates.sort(
            key=lambda row: (
                -row[0],
                EVENT_PRIORITY[row[1]],
                row[2] if row[2] is not None else -1,
            )
        )
        return candidates[:MAX_EVENTS_PER_BOUNDARY]

    def apply_boundary(self, frame: Frame) -> None:
        for _, kind, source, target in self.discover(frame):
            if self.remaining_budget <= 0:
                return
            if self._apply(kind, source, target):
                self.remaining_budget -= 1
                self.applied_events += 1

    def _apply(self, kind: str, source: int | None, target: int | None) -> bool:
        if kind == "duplicate":
            if source is None or not self.active[source]:
                return False
            inactive = [index for index, value in enumerate(self.active) if not value]
            if not inactive:
                return False
            target = inactive[0]
            self.active[target] = True
            self.edges[target][target] = True
            return True

        if kind == "module_prune":
            if source is None or not self.active[source]:
                return False
            if sum(self.active) <= MIN_LIVE_MODULES:
                return False
            self.active[source] = False
            for index in range(MAX_MODULES):
                self.edges[source][index] = False
                self.edges[index][source] = False
            return True

        if kind == "edge_grow":
            if source is None or target is None:
                return False
            if not self.active[source] or not self.active[target]:
                return False
            if self.edges[source][target]:
                return False
            if sum(sum(row) for row in self.edges) >= MAX_ACTIVE_EDGES:
                return False
            self.edges[source][target] = True
            return True

        if kind == "edge_prune":
            if source is None or target is None or not self.edges[source][target]:
                return False
            if sum(self.edges[index][target] for index in range(MAX_MODULES)) <= MIN_IN_DEGREE:
                return False
            self.edges[source][target] = False
            return True

        raise ValueError(kind)

    def graph_key(self) -> tuple[tuple[int, ...], tuple[tuple[int, int], ...]]:
        modules = tuple(index for index, value in enumerate(self.active) if value)
        edges = tuple(
            (source, target)
            for source in range(MAX_MODULES)
            for target in range(MAX_MODULES)
            if self.edges[source][target]
        )
        return modules, edges


def make_frames(seed: int) -> list[Frame]:
    rng = random.Random(seed)
    frames: list[Frame] = []
    for step in range(12):
        routing = [rng.uniform(0.6, 1.4) for _ in range(MAX_MODULES)]
        high = step % SOURCE_MODULES
        low = (step * 5 + 3) % SOURCE_MODULES
        if low == high:
            low = (low + 1) % SOURCE_MODULES
        routing[high] = rng.uniform(4.2, 5.2)
        routing[low] = rng.uniform(0.01, 0.04)

        credit = [
            [rng.uniform(0.01, 0.06) for _ in range(MAX_MODULES)]
            for _ in range(MAX_MODULES)
        ]
        grow_source = (step * 7 + 1) % SOURCE_MODULES
        grow_target = (grow_source + 4 + step % 3) % SOURCE_MODULES
        credit[grow_source][grow_target] = rng.uniform(0.12, 0.20)

        prune_source = (step * 3 + 2) % SOURCE_MODULES
        prune_target = (prune_source + 1) % SOURCE_MODULES
        credit[prune_source][prune_target] = rng.uniform(0.0001, 0.002)
        frames.append(
            Frame(
                tuple(routing),
                tuple(tuple(row) for row in credit),
            )
        )
    return frames


def jaccard_distance(left: set[object], right: set[object]) -> float:
    union = left | right
    if not union:
        return 0.0
    return 1.0 - len(left & right) / len(union)


def run_seed(
    *, seed: int, budget: int, enabled: frozenset[str], orders: int = 120
) -> dict[str, object]:
    frames = make_frames(seed)
    order_rng = random.Random(seed ^ 0x5A17)
    graphs: list[tuple[tuple[int, ...], tuple[tuple[int, int], ...]]] = []
    applied: list[int] = []
    remaining: list[int] = []

    for _ in range(orders):
        order = list(range(len(frames)))
        order_rng.shuffle(order)
        sim = ControllerSim(total_budget=budget, enabled=enabled)
        for frame_index in order:
            sim.apply_boundary(frames[frame_index])
        graphs.append(sim.graph_key())
        applied.append(sim.applied_events)
        remaining.append(sim.remaining_budget)

    pair_rng = random.Random(seed ^ budget ^ len(enabled) ^ 0xA55A)
    module_distances: list[float] = []
    edge_distances: list[float] = []
    for _ in range(300):
        left_index, right_index = pair_rng.sample(range(orders), 2)
        left_modules, left_edges = graphs[left_index]
        right_modules, right_edges = graphs[right_index]
        module_distances.append(jaccard_distance(set(left_modules), set(right_modules)))
        edge_distances.append(jaccard_distance(set(left_edges), set(right_edges)))

    return {
        "seed": seed,
        "orders": orders,
        "unique_final_graphs": len(set(graphs)),
        "pairwise_module_jaccard_mean": statistics.fmean(module_distances),
        "pairwise_edge_jaccard_mean": statistics.fmean(edge_distances),
        "median_applied_events": statistics.median(applied),
        "mean_remaining_budget": statistics.fmean(remaining),
    }


def summarize() -> dict[str, object]:
    conditions = {
        "full": frozenset({"duplicate", "module_prune", "edge_grow", "edge_prune"}),
        "module_only": frozenset({"duplicate", "module_prune"}),
        "edge_only": frozenset({"edge_grow", "edge_prune"}),
    }
    seeds = [20260919, 20260920, 20260921, 20260922, 20260923]
    rows: list[dict[str, object]] = []
    aggregate: list[dict[str, object]] = []

    for budget in (16, 64):
        for condition, enabled in conditions.items():
            cell = [
                run_seed(seed=seed, budget=budget, enabled=enabled)
                for seed in seeds
            ]
            for row in cell:
                rows.append({"budget": budget, "condition": condition, **row})
            aggregate.append(
                {
                    "budget": budget,
                    "condition": condition,
                    "unique_final_graphs_mean_of_120": statistics.fmean(
                        row["unique_final_graphs"] for row in cell
                    ),
                    "unique_final_graphs_range": [
                        min(row["unique_final_graphs"] for row in cell),
                        max(row["unique_final_graphs"] for row in cell),
                    ],
                    "pairwise_module_jaccard_mean": statistics.fmean(
                        row["pairwise_module_jaccard_mean"] for row in cell
                    ),
                    "pairwise_edge_jaccard_mean": statistics.fmean(
                        row["pairwise_edge_jaccard_mean"] for row in cell
                    ),
                    "median_applied_events_mean": statistics.fmean(
                        row["median_applied_events"] for row in cell
                    ),
                    "remaining_budget_mean": statistics.fmean(
                        row["mean_remaining_budget"] for row in cell
                    ),
                }
            )

    return {
        "evidentiary_status": "NON_EVIDENTIARY",
        "source_semantics_reference": {
            "main": "ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d",
            "controller": "src/sparkbrain/structural/controller.py",
            "config": "src/sparkbrain/structural/config.py",
            "model_initial_mask": "src/sparkbrain/structural/model.py",
        },
        "question": (
            "For the same multiset of synthetic unlabeled routing-load and edge-credit "
            "frames, is final structural topology order-sensitive, and is any sensitivity "
            "explained only by the production total-event budget?"
        ),
        "replicate_seeds": seeds,
        "orders_per_seed": 120,
        "aggregate": aggregate,
        "per_seed": rows,
        "interpretation_boundary": (
            "Synthetic architecture diagnostic only. No C08 formal run, checkpoint, dataset, "
            "preserved raw, held-out TEST, official scorer, or consumed identity is read or "
            "reinterpreted."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(summarize(), indent=2, sort_keys=True))
