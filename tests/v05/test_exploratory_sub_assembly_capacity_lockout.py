"""EXPLORATORY / NON_EVIDENTIARY SUB probe for assembly capacity behavior."""

from sparkbrain.v05 import ActivityPattern, AssemblyConfig, TemporalAssemblyMemory
from sparkbrain.v05.assemblies import pattern_similarity


def _pattern(name: str, units: tuple[int, int]) -> ActivityPattern:
    return ActivityPattern(
        pattern_id=f"pattern-{name}",
        start_ms=0.0,
        end_ms=2.0,
        ordered_units=units,
        relative_bins=(0, 1),
        unit_ids=units,
        spike_count=2,
    )


def _observe_twice(
    memory: TemporalAssemblyMemory,
    pattern: ActivityPattern,
    *,
    prefix: str,
    start_ms: float,
) -> None:
    memory.observe(pattern, time_ms=start_ms, episode_id=f"{prefix}-e1")
    memory.observe(pattern, time_ms=start_ms + 1.0, episode_id=f"{prefix}-e2")


def test_mature_capacity_lockout_vs_immature_reclamation() -> None:
    config = AssemblyConfig(
        similarity_threshold=0.66,
        mature_episodes=2,
        max_candidates=2,
        stale_after_ms=10.0,
        immature_stale_episodes=1,
    )
    p1 = _pattern("p1", (1, 2))
    p2 = _pattern("p2", (3, 4))
    p3 = _pattern("p3", (5, 6))

    assert pattern_similarity(p1, p2) == 0.2
    assert pattern_similarity(p1, p3) == 0.2
    assert pattern_similarity(p2, p3) == 0.2

    mature_saturated = TemporalAssemblyMemory(config)
    _observe_twice(mature_saturated, p1, prefix="p1", start_ms=0.0)
    _observe_twice(mature_saturated, p2, prefix="p2", start_ms=2.0)

    before = tuple(
        (candidate.assembly_id, candidate.prototype.pattern_id, candidate.episode_count)
        for candidate in mature_saturated.candidates.values()
    )
    assert before == (
        ("assembly-0001", "pattern-p1", 2),
        ("assembly-0002", "pattern-p2", 2),
    )

    first_probe = mature_saturated.observe(p3, time_ms=100.0, episode_id="p3-e1")
    second_probe = mature_saturated.observe(p3, time_ms=1000.0, episode_id="p3-e2")

    assert first_probe is None
    assert second_probe is None
    assert tuple(mature_saturated.candidates) == ("assembly-0001", "assembly-0002")
    assert all(
        candidate.prototype.pattern_id != "pattern-p3"
        for candidate in mature_saturated.candidates.values()
    )

    immature_reclaimable = TemporalAssemblyMemory(config)
    _observe_twice(immature_reclaimable, p1, prefix="p1", start_ms=0.0)
    immature_reclaimable.observe(p2, time_ms=2.0, episode_id="p2-e1")

    reclaimed_probe = immature_reclaimable.observe(
        p3,
        time_ms=100.0,
        episode_id="p3-e1",
    )

    assert reclaimed_probe is not None
    assert reclaimed_probe.assembly_id == "assembly-0003"
    assert tuple(immature_reclaimable.candidates) == ("assembly-0001", "assembly-0003")
    assert immature_reclaimable.candidates["assembly-0003"].prototype.pattern_id == "pattern-p3"
