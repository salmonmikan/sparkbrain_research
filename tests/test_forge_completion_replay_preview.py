from forge_prototypes.completion_replay_preview import CompletionReplayPreview
from sparkbrain.v04 import (
    Connection,
    ExcitableFieldConfig,
    TemporalExcitableField,
    UnitState,
    explicit_topology,
)
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


def _field(*, recurrent: bool = True) -> TemporalExcitableField:
    connections = (
        (
            Connection(1, 2, 0.60, 1.0, plastic=False),
            Connection(3, 4, 0.60, 1.0, plastic=False),
            Connection(1, 5, 0.20, 1.0, plastic=False),
        )
        if recurrent
        else ()
    )
    topology = explicit_topology(
        tuple(
            UnitState(unit_id, float(unit_id), 0.0, base_threshold=0.50)
            for unit_id in (1, 2, 3, 4, 5)
        ),
        connections,
        receptor_ids=(),
    )
    return TemporalExcitableField(
        topology,
        ExcitableFieldConfig(receptor_fanout=1),
    )


def _memory() -> TemporalAssemblyMemory:
    memory = TemporalAssemblyMemory(AssemblyConfig(mature_episodes=2))
    _observe_twice(
        memory,
        _pattern("full", (1, 2, 3, 4), (0, 1, 2, 3)),
        "a",
    )
    return memory


def test_counterfactual_replay_recruits_missing_units_via_existing_recurrence() -> None:
    memory = _memory()
    field = _field(recurrent=True)
    before = field.state_hash()

    result = CompletionReplayPreview(memory).preview(
        field,
        _pattern("partial", (1, 3), (0, 2)),
    )

    assert result.route == "counterfactual_replay"
    assert result.reason == "missing_units_recruited"
    assert result.trigger_unit_ids == (1, 3)
    assert result.baseline_spike_unit_ids == ()
    assert result.replay_spike_unit_ids == (1, 2, 3, 4)
    assert result.recovered_missing_unit_ids == (2, 4)
    assert result.spillover_unit_ids == ()
    assert result.missing_recovery_fraction == 1.0
    assert result.prototype_recovery_fraction == 1.0
    assert result.live_state_unchanged is True
    assert field.state_hash() == before


def test_counterfactual_replay_does_not_directly_force_missing_units() -> None:
    memory = _memory()
    field = _field(recurrent=False)

    result = CompletionReplayPreview(memory).preview(
        field,
        _pattern("partial", (1, 3), (0, 2)),
    )

    assert result.reason == "no_missing_units_recruited"
    assert result.replay_spike_unit_ids == (1, 3)
    assert result.recovered_missing_unit_ids == ()
    assert result.missing_recovery_fraction == 0.0
    assert result.prototype_recovery_fraction == 0.5


def test_ambiguous_completion_abstains_without_touching_live_field() -> None:
    memory = _memory()
    _observe_twice(
        memory,
        _pattern("competing", (1, 5, 3, 4), (0, 1, 2, 3)),
        "b",
    )
    field = _field(recurrent=True)
    before = field.state_hash()

    result = CompletionReplayPreview(memory).preview(
        field,
        _pattern("partial", (1, 3), (0, 2)),
    )

    assert result.route == "abstain"
    assert result.reason == "ambiguous_candidate"
    assert result.replay_spike_unit_ids == ()
    assert result.live_state_unchanged is True
    assert field.state_hash() == before
