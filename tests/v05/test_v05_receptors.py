from __future__ import annotations

import pytest

from sparkbrain.v04 import SignalPulse
from sparkbrain.v05 import MultiTimescaleReceptorBank, ReceptorConfig


def test_receptor_emits_multiscale_trace_and_round_trips() -> None:
    bank = MultiTimescaleReceptorBank()
    emitted, traces = bank.process(
        [
            SignalPulse(0.0, "A", 1.0),
            SignalPulse(5.0, "A", 0.8),
        ]
    )
    assert emitted
    assert traces[-1].fast_trace != traces[-1].slow_trace
    restored = MultiTimescaleReceptorBank.from_state_dict(bank.state_dict())
    assert restored.state_dict() == bank.state_dict()


def test_receptor_rejects_backward_time() -> None:
    bank = MultiTimescaleReceptorBank()
    bank.process([SignalPulse(5.0, "A", 1.0)])
    with pytest.raises(ValueError, match="backwards"):
        bank.process([SignalPulse(4.0, "A", 1.0)])


def test_receptor_gain_is_bounded() -> None:
    config = ReceptorConfig(min_gain=0.5, max_gain=0.8, target_abs_input=20.0)
    bank = MultiTimescaleReceptorBank(config)
    _, traces = bank.process([SignalPulse(0.0, "A", 0.1)])
    assert traces[0].gain == pytest.approx(0.8)
