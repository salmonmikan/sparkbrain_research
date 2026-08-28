from __future__ import annotations

from sparkbrain.v05 import (
    ActivityPattern,
    AssemblyConfig,
    TemporalAssemblyMemory,
    pattern_similarity,
)


def pattern(name: str, ordered: tuple[int, ...], bins: tuple[int, ...]) -> ActivityPattern:
    return ActivityPattern(
        name,
        0.0,
        float(max(bins, default=0)),
        ordered,
        bins,
        tuple(sorted(set(ordered))),
        len(ordered),
    )


def test_repeated_pattern_matures_only_across_distinct_episodes() -> None:
    memory = TemporalAssemblyMemory(AssemblyConfig(mature_episodes=3))
    p = pattern("p", (1, 2, 3), (0, 2, 4))
    same_episode = [memory.observe(p, time_ms=float(i), episode_id="episode-a") for i in range(3)]
    assert same_episode[-1] is not None
    assert not same_episode[-1].mature
    assert same_episode[-1].occurrences == 3
    assert same_episode[-1].episode_count == 1

    memory.observe(p, time_ms=4.0, episode_id="episode-b")
    row = memory.observe(p, time_ms=5.0, episode_id="episode-c")
    assert row is not None and row.mature
    assert row.episode_count == 3
    assert row.assembly_id.startswith("assembly-")


def test_order_changes_pattern_similarity() -> None:
    abc = pattern("abc", (1, 2, 3), (0, 2, 4))
    cba = pattern("cba", (3, 2, 1), (0, 2, 4))
    same = pattern("same", (1, 2, 3), (0, 2, 4))
    assert pattern_similarity(abc, same) > pattern_similarity(abc, cba)


def test_suppression_and_round_trip_preserve_episode_lineage() -> None:
    memory = TemporalAssemblyMemory()
    row = memory.observe(
        pattern("p", (1, 2), (0, 1)),
        time_ms=0.0,
        episode_id="episode-a",
    )
    assert row is not None
    memory.suppress(row.assembly_id)
    restored = TemporalAssemblyMemory.from_state_dict(memory.state_dict())
    assert row.assembly_id in restored.suppressed
    assert restored.candidates[row.assembly_id].episode_ids == {"episode-a"}
