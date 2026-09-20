from __future__ import annotations

import pytest

from sparkbrain.v04 import SignalPulse
from sparkbrain.v05 import MultiTimescaleReceptorBank


def _run(order: tuple[float, float]) -> tuple[MultiTimescaleReceptorBank, tuple, tuple]:
    bank = MultiTimescaleReceptorBank()
    emitted, traces = bank.process(
        [SignalPulse(0.0, "A", magnitude) for magnitude in order]
    )
    return bank, emitted, traces


def test_exploratory_same_time_same_channel_permutation_changes_emitted_drive() -> None:
    large_then_small = _run((1.0, 0.2))
    small_then_large = _run((0.2, 1.0))

    first_bank, first_emitted, first_traces = large_then_small
    second_bank, second_emitted, second_traces = small_then_large

    assert first_bank.state_dict() == second_bank.state_dict()
    assert first_traces[-1].fast_trace == pytest.approx(second_traces[-1].fast_trace)
    assert first_traces[-1].medium_trace == pytest.approx(second_traces[-1].medium_trace)
    assert first_traces[-1].slow_trace == pytest.approx(second_traces[-1].slow_trace)
    assert first_traces[-1].gain == pytest.approx(second_traces[-1].gain)

    first_magnitudes = tuple(row.magnitude for row in first_emitted)
    second_magnitudes = tuple(row.magnitude for row in second_emitted)
    assert first_magnitudes == pytest.approx((1.14, 0.19))
    assert second_magnitudes == pytest.approx((0.456, 0.95))

    first_signed_drive = sum(row.magnitude * row.polarity for row in first_emitted)
    second_signed_drive = sum(row.magnitude * row.polarity for row in second_emitted)
    assert first_signed_drive == pytest.approx(1.33)
    assert second_signed_drive == pytest.approx(1.406)
    assert first_signed_drive != pytest.approx(second_signed_drive)
