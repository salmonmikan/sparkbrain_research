"""EXPLORATORY / NON_EVIDENTIARY assembly prototype lock-in probe.

Uses only stable v0.5 TemporalAssemblyMemory semantics and synthetic ActivityPattern
objects. No repository datasets, checkpoints, formal raw material, held-out TEST
inputs, consumed identities, or official scorers are accessed.
"""

from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

from sparkbrain.v05 import ActivityPattern, AssemblyConfig, TemporalAssemblyMemory
from sparkbrain.v05.assemblies import pattern_similarity

SOURCE_SEMANTICS = "main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d"
RESULT_PATH = Path(
    "analysis/discovery/assembly_prototype_lockin_order_sensitivity_20260919.json"
)
THRESHOLD = 0.66
MATURE_EPISODES = 3


def pattern(name: str, ordered: tuple[int, ...]) -> ActivityPattern:
    bins = (0, 1, 2, 3)
    return ActivityPattern(
        name,
        0.0,
        3.0,
        ordered,
        bins,
        tuple(sorted(set(ordered))),
        len(ordered),
    )


PATTERNS = {
    "A": pattern("A", (1, 3, 2, 5)),
    "B": pattern("B", (1, 5, 2, 3)),
    "C": pattern("C", (5, 2, 1, 3)),
}


def run_order(order: tuple[str, ...]) -> tuple[tuple[str, ...], tuple[int, ...], int]:
    memory = TemporalAssemblyMemory(
        AssemblyConfig(
            similarity_threshold=THRESHOLD,
            mature_episodes=MATURE_EPISODES,
        )
    )
    for index, label in enumerate(order):
        memory.observe(
            PATTERNS[label],
            time_ms=float(index),
            episode_id=f"episode-{index:02d}",
        )
    candidates = tuple(memory.candidates.values())
    return (
        tuple(candidate.prototype.pattern_id for candidate in candidates),
        tuple(candidate.episode_count for candidate in candidates),
        sum(candidate.episode_count >= MATURE_EPISODES for candidate in candidates),
    )


def main() -> None:
    pairwise = {
        left: {
            right: pattern_similarity(PATTERNS[left], PATTERNS[right])
            for right in PATTERNS
        }
        for left in PATTERNS
    }
    orders = sorted(set(itertools.permutations("AAABBBCCC")))
    outcomes: Counter[tuple[tuple[str, ...], tuple[int, ...], int]] = Counter(
        run_order(order) for order in orders
    )

    rows = [
        {
            "prototype_order": list(prototypes),
            "episode_counts": list(counts),
            "mature_assemblies": mature,
            "permutation_count": count,
        }
        for (prototypes, counts, mature), count in sorted(outcomes.items())
    ]
    result = {
        "label": "EXPLORATORY / NON_EVIDENTIARY",
        "source_semantics": SOURCE_SEMANTICS,
        "question": (
            "Can frozen first-exemplar prototypes make mature assembly cardinality "
            "depend on episode order for an identical multiset of patterns?"
        ),
        "protocol": {
            "similarity_threshold": THRESHOLD,
            "mature_episodes": MATURE_EPISODES,
            "pattern_multiset": {"A": 3, "B": 3, "C": 3},
            "unique_episode_orders": len(orders),
            "all_episode_ids_distinct": True,
        },
        "pairwise_similarity": pairwise,
        "outcomes": rows,
        "summary": {
            "one_mature_assembly_orders": sum(
                row["permutation_count"]
                for row in rows
                if row["mature_assemblies"] == 1
            ),
            "two_mature_assembly_orders": sum(
                row["permutation_count"]
                for row in rows
                if row["mature_assemblies"] == 2
            ),
            "first_B_orders": sum(1 for order in orders if order[0] == "B"),
            "first_A_or_C_orders": sum(1 for order in orders if order[0] != "B"),
            "order_invariant_similarity_graph_components": 1,
            "interpretation": (
                "A-B and B-C exceed the fixed similarity threshold while A-C does "
                "not. TemporalAssemblyMemory never updates an accepted candidate's "
                "prototype, so the first exemplar determines whether B bridges A/C "
                "into one mature assembly or whether A/C seed two mature assemblies. "
                "The similarity graph itself is connected, so the path dependence is "
                "specific to greedy frozen-prototype assignment rather than the metric "
                "alone."
            ),
        },
        "evidentiary_status": "NON_EVIDENTIARY",
        "recommendation": "PROMOTE_TO_ARCHITECTURE_STUDY",
    }
    RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
