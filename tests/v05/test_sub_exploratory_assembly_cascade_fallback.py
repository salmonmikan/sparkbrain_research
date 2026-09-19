from __future__ import annotations

from sparkbrain.v04.contracts import CascadeEvent, SpikeEvent
from sparkbrain.v05 import AssemblyConfig, TemporalAssemblyMemory, patterns_from_step


def _spike(time_ms: float, unit_id: int) -> SpikeEvent:
    return SpikeEvent(
        time_ms=time_ms,
        unit_id=unit_id,
        potential_before_reset=1.0,
        dynamic_threshold=0.5,
        x=0.0,
        y=0.0,
        source_pulse_ids=(f"p-{time_ms}-{unit_id}",),
        novelty=0.0,
        prediction_error=0.0,
        excitatory_drive=1.0,
        inhibitory_drive=0.0,
    )


def _cascade(
    name: str,
    start_ms: float,
    end_ms: float,
    internal_unit: int,
) -> CascadeEvent:
    return CascadeEvent(
        cascade_id=name,
        start_ms=start_ms,
        end_ms=end_ms,
        spike_count=2,
        unit_ids=(0, internal_unit),
        ordered_units=(0, internal_unit),
        spatial_spread=1.0,
        novelty=0.0,
        prediction_error=0.0,
        recurrence=0.0,
        signature=f"sig-{name}",
    )


def _bridged_pattern():
    cascades = (
        _cascade("c1", 0.0, 1.0, 101),
        _cascade("c2", 20.0, 21.0, 102),
    )
    spikes = (
        _spike(0.0, 0),
        _spike(1.0, 101),
        _spike(20.0, 0),
        _spike(21.0, 102),
    )
    return patterns_from_step(cascades, spikes, excluded_unit_ids=(0,))


def test_fallback_bridges_distinct_cascades_after_receptor_exclusion() -> None:
    patterns = _bridged_pattern()

    assert len(patterns) == 1
    pattern = patterns[0]
    assert pattern.source_cascade_id is None
    assert pattern.ordered_units == (101, 102)
    assert pattern.unit_ids == (101, 102)
    assert pattern.start_ms == 1.0
    assert pattern.end_ms == 21.0


def test_bridged_fallback_is_assembly_facing_and_can_mature() -> None:
    pattern = _bridged_pattern()[0]
    memory = TemporalAssemblyMemory(AssemblyConfig(mature_episodes=3))

    first = memory.observe(pattern, time_ms=21.0, episode_id="episode-1")
    second = memory.observe(pattern, time_ms=42.0, episode_id="episode-2")
    third = memory.observe(pattern, time_ms=63.0, episode_id="episode-3")

    assert first is not None and not first.mature
    assert second is not None and not second.mature
    assert third is not None and third.mature
    assert third.episode_count == 3


def test_successful_cascade_pattern_prevents_cross_cascade_fallback() -> None:
    cascades = (
        CascadeEvent(
            cascade_id="c1",
            start_ms=0.0,
            end_ms=2.0,
            spike_count=3,
            unit_ids=(0, 101, 103),
            ordered_units=(0, 101, 103),
            spatial_spread=1.0,
            novelty=0.0,
            prediction_error=0.0,
            recurrence=0.0,
            signature="sig-c1",
        ),
        _cascade("c2", 20.0, 21.0, 102),
    )
    spikes = (
        _spike(0.0, 0),
        _spike(1.0, 101),
        _spike(2.0, 103),
        _spike(20.0, 0),
        _spike(21.0, 102),
    )

    patterns = patterns_from_step(cascades, spikes, excluded_unit_ids=(0,))

    assert len(patterns) == 1
    pattern = patterns[0]
    assert pattern.source_cascade_id == "c1"
    assert pattern.ordered_units == (101, 103)
    assert pattern.end_ms == 2.0
