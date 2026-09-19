#!/usr/bin/env python3
"""EXPLORATORY / NON_EVIDENTIARY plasticity update-cap scaling diagnostic."""

from __future__ import annotations

import json
import random
from itertools import combinations

from sparkbrain.v04.field import TemporalExcitableField
from sparkbrain.v05.topology import layered_reservoir_topology

RECEPTOR_COUNT = 16
MAX_UPDATES_PER_STEP = 2000
TOPOLOGY_SEED = 505
RELABEL_SEED = 20260919
RELABELINGS = 24
SCALES = [(8, 6), (16, 12), (20, 15), (24, 18), (32, 24)]


def effective_edge_keys(width: int, height: int) -> list[tuple[int, int]]:
    topology = layered_reservoir_topology(
        receptor_count=RECEPTOR_COUNT,
        reservoir_width=width,
        reservoir_height=height,
        seed=TOPOLOGY_SEED,
    )
    field = TemporalExcitableField(topology)
    return sorted(field.connections)


def random_relabeling(
    reservoir_count: int,
    rng: random.Random,
) -> dict[int, int]:
    """Relabel reservoir numeric IDs while preserving semantic identity."""
    first = RECEPTOR_COUNT
    original = list(range(first, first + reservoir_count))
    permuted = original.copy()
    rng.shuffle(permuted)
    return dict(zip(original, permuted, strict=True))


def select_semantic_edges(
    semantic_edges: list[tuple[int, int]],
    relabeling: dict[int, int],
) -> set[tuple[int, int]]:
    """Mirror sorted-edge cap selection after an isomorphic numeric relabel."""
    inverse = {new: old for old, new in relabeling.items()}

    def relabel(node_id: int) -> int:
        return relabeling.get(node_id, node_id)

    numeric_edges = sorted((relabel(src), relabel(dst)) for src, dst in semantic_edges)
    selected_numeric = numeric_edges[:MAX_UPDATES_PER_STEP]

    def semantic(node_id: int) -> int:
        return inverse.get(node_id, node_id)

    return {(semantic(src), semantic(dst)) for src, dst in selected_numeric}


def jaccard(left: set[tuple[int, int]], right: set[tuple[int, int]]) -> float:
    if not left and not right:
        return 1.0
    return len(left & right) / len(left | right)


def summarize(width: int, height: int) -> dict[str, float | int | bool]:
    reservoir_count = width * height
    semantic_edges = effective_edge_keys(width, height)
    rng = random.Random(RELABEL_SEED + reservoir_count)
    selections = [
        select_semantic_edges(
            semantic_edges,
            random_relabeling(reservoir_count, rng),
        )
        for _ in range(RELABELINGS)
    ]
    pairwise = [
        jaccard(left, right)
        for left, right in combinations(selections, 2)
    ]
    source_counts = [
        len({src for src, _ in selected if src >= RECEPTOR_COUNT})
        for selected in selections
    ]

    edge_count = len(semantic_edges)
    selected_count = min(edge_count, MAX_UPDATES_PER_STEP)
    return {
        "width": width,
        "height": height,
        "reservoir_units": reservoir_count,
        "effective_edges": edge_count,
        "cap_active": edge_count > MAX_UPDATES_PER_STEP,
        "fraction_edges_updated": selected_count / edge_count,
        "mean_pairwise_semantic_edge_jaccard": sum(pairwise) / len(pairwise),
        "min_pairwise_semantic_edge_jaccard": min(pairwise),
        "max_pairwise_semantic_edge_jaccard": max(pairwise),
        "mean_reservoir_sources_touched": sum(source_counts) / len(source_counts),
    }


def main() -> None:
    results = [summarize(width, height) for width, height in SCALES]
    payload = {
        "status": "EXPLORATORY / NON_EVIDENTIARY",
        "assumption": (
            "All effective plastic edges are eligible in the synthetic step, "
            "isolating only sorted-edge update-budget scheduling."
        ),
        "question": (
            "Does the fixed plasticity update cap create numeric-ID-dependent "
            "semantic update privilege as topology scale crosses the cap?"
        ),
        "max_updates_per_step": MAX_UPDATES_PER_STEP,
        "topology_seed": TOPOLOGY_SEED,
        "relabel_seed": RELABEL_SEED,
        "relabelings_per_scale": RELABELINGS,
        "results": results,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
