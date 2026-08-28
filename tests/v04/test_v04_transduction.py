from __future__ import annotations

from sparkbrain.v04 import FrameDeltaTransducer, SignalPulse, TextPulseTransducer
from sparkbrain.v04.transduction import ScalarDeltaTransducer, TemporalExpectationTracker


def test_signal_pulse_rejects_invalid_values() -> None:
    try:
        SignalPulse(time_ms=-1.0, channel="x", magnitude=1.0)
    except ValueError as exc:
        assert "non-negative" in str(exc)
    else:
        raise AssertionError("negative time must be rejected")


def test_text_transducer_is_raw_symbol_and_transition_based() -> None:
    transducer = TextPulseTransducer(symbol_interval_ms=2.0)
    pulses = transducer.encode("ab", start_ms=5.0)
    assert [row.time_ms for row in pulses] == [5.0, 7.0, 7.0]
    assert all(row.channel.startswith(("symbol:", "transition:")) for row in pulses)
    assert not any("meaning" in row.metadata for row in pulses)


def test_frame_delta_emits_only_changed_pixels() -> None:
    transducer = FrameDeltaTransducer(threshold=0.2)
    assert transducer.observe(((0.0, 0.0), (0.0, 0.0)), time_ms=0.0) == ()
    pulses = transducer.observe(((0.0, 1.0), (0.0, 0.0)), time_ms=1.0)
    assert len(pulses) == 1
    assert pulses[0].location == (1.0, 0.0)
    assert pulses[0].polarity == 1


def test_scalar_delta_suppresses_subthreshold_change() -> None:
    transducer = ScalarDeltaTransducer(threshold=0.5)
    assert len(transducer.observe("sensor", 1.0, time_ms=0.0)) == 1
    assert transducer.observe("sensor", 1.2, time_ms=1.0) == ()
    pulse = transducer.observe("sensor", 2.0, time_ms=2.0)[0]
    assert abs(pulse.magnitude - 0.8) < 1e-12


def test_temporal_expectation_emits_omission_after_repetition() -> None:
    tracker = TemporalExpectationTracker(min_observations=3, tolerance_fraction=0.2)
    for time_ms in (0.0, 10.0, 20.0, 30.0):
        tracker.observe(SignalPulse(time_ms, "tick", 1.0))
    assert tracker.poll(until_ms=39.0) == ()
    pulses = tracker.poll(until_ms=43.0)
    assert len(pulses) == 1
    assert pulses[0].channel == "omission:tick"
    assert pulses[0].prediction_error == 1.0
    assert tracker.poll(until_ms=50.0) == ()
