from __future__ import annotations

import pytest

from sparkbrain.v05 import ActivityPattern, AssemblyConfig, TemporalAssemblyMemory, pattern_similarity


def _pattern(name: str, ordered: tuple[int, ...]) -> ActivityPattern:
    bins = (0, 1, 2, 3)
    return ActivityPattern(
        pattern_id=name,
        start_ms=0.0,
        end_ms=3.0,
        ordered_units=ordered,
        relative_bins=bins,
        unit_ids=tuple(sorted(set(ordered))),
        spike_count=len(ordered),
    )


def _run(order: tuple[ActivityPattern, ...]) -> tuple[TemporalAssemblyMemory, tuple[str, ...]]:
    memory = TemporalAssemblyMemory(AssemblyConfig(similarity_threshold=0.66, mature_episodes=3))
    assignments: list[str] = []
    for index, pattern in enumerate(order):
        activation = memory.observe(
            pattern,
            time_ms=float(index),
            episode_id=f"episode-{index}",
            learn=True,
        )
        assert activation is not None
        assignments.append(activation.assembly_id)
    return memory, tuple(assignments)


def test_same_pattern_multiset_can_partition_differently_by_first_prototype() -> None:
    a = _pattern("A", (1, 2, 3, 4))
    b = _pattern("B", (1, 2, 3, 5))
    c = _pattern("C", (1, 2, 4, 5))

    assert pattern_similarity(a, b) == pytest.approx(0.7625)
    assert pattern_similarity(b, c) == pytest.approx(0.7625)
    assert pattern_similarity(a, c) == pytest.approx(0.6250)

    abc_memory, abc_assignments = _run((a, b, c))
    bac_memory, bac_assignments = _run((b, a, c))

    assert len(abc_memory.candidates) == 2
    assert abc_assignments[0] == abc_assignments[1]
    assert abc_assignments[2] != abc_assignments[0]

    assert len(bac_memory.candidates) == 1
    assert len(set(bac_assignments)) == 1
