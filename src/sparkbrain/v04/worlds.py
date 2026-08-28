from __future__ import annotations

import random
from collections.abc import Iterable
from dataclasses import dataclass

from .contracts import SignalPulse
from .transduction import pulse_train


@dataclass(frozen=True, slots=True)
class TemporalSequenceCase:
    name: str
    pulses: tuple[SignalPulse, ...]


def order_cases(
    *, start_ms: float = 0.0, interval_ms: float = 4.0
) -> tuple[TemporalSequenceCase, ...]:
    return (
        TemporalSequenceCase(
            "abc",
            pulse_train(("A", "B", "C"), start_ms=start_ms, interval_ms=interval_ms),
        ),
        TemporalSequenceCase(
            "cba",
            pulse_train(("C", "B", "A"), start_ms=start_ms, interval_ms=interval_ms),
        ),
        TemporalSequenceCase(
            "simultaneous",
            tuple(
                SignalPulse(
                    time_ms=start_ms,
                    channel=channel,
                    magnitude=0.8,
                    source_id="order-world",
                )
                for channel in ("A", "B", "C")
            ),
        ),
    )


def weak_coincidence_cases(*, start_ms: float = 0.0) -> tuple[TemporalSequenceCase, ...]:
    weak = 0.44
    return (
        TemporalSequenceCase(
            "aligned",
            (
                SignalPulse(start_ms, "A", weak, source_id="coincidence"),
                SignalPulse(start_ms + 3.0, "B", weak, source_id="coincidence"),
                SignalPulse(start_ms + 6.0, "C", weak, source_id="coincidence"),
            ),
        ),
        TemporalSequenceCase(
            "dispersed",
            (
                SignalPulse(start_ms, "A", weak, source_id="coincidence"),
                SignalPulse(start_ms + 18.0, "B", weak, source_id="coincidence"),
                SignalPulse(start_ms + 36.0, "C", weak, source_id="coincidence"),
            ),
        ),
    )


def repetition_train(
    *,
    channel: str = "tick",
    start_ms: float = 0.0,
    interval_ms: float = 12.0,
    count: int = 8,
    magnitude: float = 0.85,
) -> tuple[SignalPulse, ...]:
    return tuple(
        SignalPulse(
            time_ms=start_ms + index * interval_ms,
            channel=channel,
            magnitude=magnitude,
            source_id="repetition-world",
        )
        for index in range(count)
    )


def noisy_motif_stream(
    *,
    motif: tuple[str, ...] = ("A", "F", "C"),
    repeats: int = 8,
    noise_per_repeat: int = 4,
    start_ms: float = 0.0,
    seed: int = 904,
) -> tuple[SignalPulse, ...]:
    rng = random.Random(seed)
    pulses: list[SignalPulse] = []
    time_ms = start_ms
    noise_channels = tuple("DEGHIJK")
    for _ in range(repeats):
        for _ in range(noise_per_repeat):
            pulses.append(
                SignalPulse(
                    time_ms=time_ms,
                    channel=rng.choice(noise_channels),
                    magnitude=0.35,
                    novelty=0.2,
                    source_id="noise",
                )
            )
            time_ms += rng.uniform(1.0, 4.0)
        for offset, channel in zip((0.0, 5.0, 7.0), motif, strict=True):
            pulses.append(
                SignalPulse(
                    time_ms=time_ms + offset,
                    channel=channel,
                    magnitude=0.82,
                    novelty=0.4,
                    source_id="motif",
                )
            )
        time_ms += 14.0
    return tuple(sorted(pulses, key=lambda row: (row.time_ms, row.channel)))


def moving_point_frames(
    *,
    width: int = 5,
    height: int = 3,
    reverse: bool = False,
) -> tuple[tuple[tuple[float, ...], ...], ...]:
    positions: Iterable[int] = range(width - 1, -1, -1) if reverse else range(width)
    frames: list[tuple[tuple[float, ...], ...]] = []
    for x_position in positions:
        frame = []
        for y in range(height):
            row = [0.0] * width
            if y == height // 2:
                row[x_position] = 1.0
            frame.append(tuple(row))
        frames.append(tuple(frame))
    return tuple(frames)
