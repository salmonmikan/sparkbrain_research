from forge_prototypes.assembly_completion import AssemblyCompletionProbe
from sparkbrain.v05 import ActivityPattern, AssemblyConfig, TemporalAssemblyMemory


def _pattern(name: str, units: tuple[int, ...], bins: tuple[int, ...]) -> ActivityPattern:
    return ActivityPattern(
        pattern_id=name,
        start_ms=0.0,
        end_ms=float(bins[-1]),
        ordered_units=units,
        relative_bins=bins,
        unit_ids=tuple(sorted(set(units))),
        spike_count=len(units),
    )


def _observe_twice(memory: TemporalAssemblyMemory, pattern: ActivityPattern, prefix: str) -> None:
    memory.observe(pattern, time_ms=0.0, episode_id=f"{prefix}-1")
    memory.observe(pattern, time_ms=10.0, episode_id=f"{prefix}-2")


def test_partial_cue_proposes_missing_structure_without_mutating_memory() -> None:
    memory = TemporalAssemblyMemory(AssemblyConfig(mature_episodes=2))
    full = _pattern("full", (1, 2, 3, 4), (0, 1, 2, 3))
    _observe_twice(memory, full, "a")
    before = memory.state_dict()

    proposal = AssemblyCompletionProbe(memory).propose(
        _pattern("partial", (1, 3), (0, 2))
    )

    assert proposal.abstained is False
    assert proposal.assembly_id == "assembly-0001"
    assert round(proposal.similarity, 6) == 0.6
    assert proposal.missing_positions == (1, 3)
    assert proposal.missing_unit_ids == (2, 4)
    assert memory.state_dict() == before


def test_ambiguous_partial_cue_abstains() -> None:
    memory = TemporalAssemblyMemory(AssemblyConfig(mature_episodes=2))
    _observe_twice(
        memory,
        _pattern("a", (1, 2, 3, 4), (0, 1, 2, 3)),
        "a",
    )
    _observe_twice(
        memory,
        _pattern("b", (1, 5, 3, 6), (0, 1, 2, 3)),
        "b",
    )

    proposal = AssemblyCompletionProbe(memory).propose(
        _pattern("partial", (1, 3), (0, 2))
    )

    assert proposal.abstained is True
    assert proposal.reason == "ambiguous_candidate"
    assert round(proposal.similarity, 6) == 0.6
    assert proposal.margin == 0.0
    assert proposal.assembly_id is None
    assert proposal.missing_unit_ids == ()


def test_complete_cue_does_not_emit_a_completion() -> None:
    memory = TemporalAssemblyMemory(AssemblyConfig(mature_episodes=2))
    full = _pattern("full", (1, 2, 3, 4), (0, 1, 2, 3))
    _observe_twice(memory, full, "a")

    proposal = AssemblyCompletionProbe(memory).propose(full)

    assert proposal.abstained is True
    assert proposal.reason == "already_complete"
