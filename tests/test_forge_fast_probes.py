from __future__ import annotations

import math

import pytest

from sparkbrain.v04.contracts import SignalPulse
from sparkbrain.v05.assemblies import AssemblyConfig, TemporalAssemblyMemory
from sparkbrain.v05.contracts import ActivityPattern
from sparkbrain.v05.receptors import MultiTimescaleReceptorBank, ReceptorConfig


def _pulse(time_ms: float, magnitude: float) -> SignalPulse:
    return SignalPulse(time_ms=time_ms, channel="forge-a", magnitude=magnitude)


def _expected_primed_cue(gap_ms: float, cue: float = 0.10, prime: float = 1.0) -> float:
    cfg = ReceptorConfig()
    fast = prime * math.exp(-gap_ms / cfg.fast_tau_ms) + cue
    medium = prime * math.exp(-gap_ms / cfg.medium_tau_ms) + cue
    slow = prime * math.exp(-gap_ms / cfg.slow_tau_ms) + cue
    mean_abs = prime * math.exp(-gap_ms / cfg.gain_tau_ms) + cue
    derivative = fast - medium
    novelty = abs(fast - slow) / (0.20 + abs(slow))
    gain = cfg.target_abs_input / max(0.08, mean_abs)
    gain = max(cfg.min_gain, min(cfg.max_gain, gain))
    drive = gain * (
        cfg.direct_gain * cue
        + cfg.derivative_gain * abs(derivative)
        + cfg.novelty_gain * novelty
    )
    return min(cfg.output_cap, drive)


def _cue_after_prime(gap_ms: float) -> float:
    bank = MultiTimescaleReceptorBank()
    bank.process((_pulse(0.0, 1.0),))
    _, traces = bank.process((_pulse(gap_ms, 0.10),))
    return traces[0].emitted_magnitude


def test_receptor_memory_priming_is_exactly_the_declared_multitimescale_filter() -> None:
    fresh = MultiTimescaleReceptorBank()
    _, fresh_traces = fresh.process((_pulse(1000.0, 0.10),))
    fresh_mag = fresh_traces[0].emitted_magnitude

    observed = {gap: _cue_after_prime(gap) for gap in (10.0, 120.0, 1000.0)}
    expected = {gap: _expected_primed_cue(gap) for gap in observed}

    assert fresh_mag == pytest.approx(0.228)
    for gap in observed:
        assert observed[gap] == pytest.approx(expected[gap], rel=0.0, abs=1e-12)

    # The same cue can be amplified long after the prime, but the effect relaxes
    # back toward the fresh-bank response as the explicit traces decay.
    assert observed[10.0] > 2.0 * fresh_mag
    assert observed[120.0] > 2.0 * fresh_mag
    assert observed[1000.0] == pytest.approx(fresh_mag, abs=0.001)


def _pattern() -> ActivityPattern:
    return ActivityPattern(
        pattern_id="forge-pattern",
        start_ms=0.0,
        end_ms=1.0,
        ordered_units=(10, 11, 12),
        relative_bins=(0, 2, 4),
        unit_ids=(10, 11, 12),
        spike_count=3,
    )


def test_suppressed_assembly_still_accumulates_learning_history() -> None:
    memory = TemporalAssemblyMemory(AssemblyConfig(mature_episodes=2))
    pattern = _pattern()

    memory.observe(pattern, time_ms=1.0, episode_id="ep-1", learn=True)
    mature = memory.observe(pattern, time_ms=2.0, episode_id="ep-2", learn=True)
    assert mature is not None and mature.mature
    assembly_id = mature.assembly_id

    memory.suppress(assembly_id)
    muted_3 = memory.observe(pattern, time_ms=3.0, episode_id="ep-3", learn=True)
    muted_4 = memory.observe(pattern, time_ms=4.0, episode_id="ep-4", learn=True)
    assert muted_3 is not None and muted_3.suppressed
    assert muted_4 is not None and muted_4.suppressed
    assert memory.candidates[assembly_id].episode_count == 4

    memory.unsuppress(assembly_id)
    restored = memory.observe(pattern, time_ms=5.0, episode_id="probe", learn=False)
    assert restored is not None and not restored.suppressed
    assert restored.episode_count == 4
