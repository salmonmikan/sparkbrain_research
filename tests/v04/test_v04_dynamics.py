from __future__ import annotations

from sparkbrain.v04.contracts import CascadeEvent, SpikeEvent
from sparkbrain.v04.dynamics import (
    AssemblyMemory,
    BurstDetector,
    BurstDetectorConfig,
    CascadeTracker,
    CascadeTrackerConfig,
    IgnitionGate,
    IgnitionGateConfig,
)


def spike(time_ms: float, unit_id: int, x: float = 0.0, y: float = 0.0) -> SpikeEvent:
    return SpikeEvent(
        time_ms=time_ms,
        unit_id=unit_id,
        potential_before_reset=1.0,
        dynamic_threshold=0.8,
        x=x,
        y=y,
        source_pulse_ids=("p",),
        novelty=0.2,
        prediction_error=0.1,
        excitatory_drive=1.0,
        inhibitory_drive=0.0,
    )


def test_burst_detector_requires_multiple_units() -> None:
    detector = BurstDetector(BurstDetectorConfig(window_ms=5.0, min_spikes=3, min_units=3))
    rows = detector.update((spike(0.0, 0), spike(1.0, 1), spike(2.0, 2)))
    assert rows
    assert rows[-1].spike_count == 3


def test_cascade_signature_is_timing_order_sensitive() -> None:
    first = CascadeTracker(CascadeTrackerConfig(max_gap_ms=5.0, temporal_bin_ms=1.0))
    second = CascadeTracker(CascadeTrackerConfig(max_gap_ms=5.0, temporal_bin_ms=1.0))
    a = first.update((spike(0.0, 0), spike(1.0, 1)), flush_until_ms=10.0)[0]
    b = second.update((spike(0.0, 1), spike(1.0, 0)), flush_until_ms=10.0)[0]
    assert a.signature != b.signature


def test_assembly_memory_marks_repeated_signature() -> None:
    memory = AssemblyMemory()
    tracker = CascadeTracker(CascadeTrackerConfig(max_gap_ms=2.0), memory=memory)
    first = tracker.update((spike(0.0, 0), spike(1.0, 1)), flush_until_ms=5.0)[0]
    second = tracker.update((spike(10.0, 0), spike(11.0, 1)), flush_until_ms=15.0)[0]
    assert first.recurrence == 0.0
    assert second.recurrence > 0.0


def test_ignition_gate_rejects_small_cascade_and_accepts_large_one() -> None:
    gate = IgnitionGate(IgnitionGateConfig(threshold=2.0, min_spikes=3, min_units=3))
    small = CascadeEvent("c1", 0, 1, 2, (0, 1), (0, 1), 1.0, 0.0, 0.0, 0.0, "s")
    large = CascadeEvent("c2", 0, 3, 5, (0, 1, 2, 3), (0, 1, 2, 3, 0), 3.0, 0.5, 0.2, 0.3, "l")
    assert gate.evaluate((small,)) == ()
    accepted = gate.evaluate((large,))
    assert len(accepted) == 1
    assert accepted[0].cascade_id == "c2"
