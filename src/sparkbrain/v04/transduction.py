from __future__ import annotations

import hashlib
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field

from .contracts import SignalPulse


def _stable_bucket(value: str, size: int) -> int:
    digest = hashlib.sha256(value.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") % size


@dataclass(slots=True)
class ScalarDeltaTransducer:
    threshold: float = 0.1
    gain: float = 1.0
    previous: dict[str, float] = field(default_factory=dict)

    def observe(self, channel: str, value: float, *, time_ms: float) -> tuple[SignalPulse, ...]:
        value = float(value)
        previous = self.previous.get(channel)
        self.previous[channel] = value
        if previous is None:
            return (
                SignalPulse(
                    time_ms=time_ms,
                    channel=channel,
                    magnitude=abs(value) * self.gain,
                    polarity=1 if value >= 0 else -1,
                    novelty=1.0,
                    source_id="scalar",
                ),
            )
        delta = value - previous
        if abs(delta) < self.threshold:
            return ()
        return (
            SignalPulse(
                time_ms=time_ms,
                channel=channel,
                magnitude=abs(delta) * self.gain,
                polarity=1 if delta >= 0 else -1,
                novelty=min(1.0, abs(delta) / max(self.threshold, 1e-9)),
                source_id="scalar-delta",
            ),
        )


@dataclass(slots=True)
class TextPulseTransducer:
    """Turn text into raw symbol and transition pulses without semantic parsing."""

    symbol_interval_ms: float = 4.0
    magnitude: float = 0.72
    transition_magnitude: float = 0.38
    channel_buckets: int = 64

    def encode(self, text: str, *, start_ms: float = 0.0) -> tuple[SignalPulse, ...]:
        pulses: list[SignalPulse] = []
        previous: str | None = None
        for index, symbol in enumerate(text):
            time_ms = start_ms + index * self.symbol_interval_ms
            symbol_channel = f"symbol:{_stable_bucket(symbol, self.channel_buckets)}"
            pulses.append(
                SignalPulse(
                    time_ms=time_ms,
                    channel=symbol_channel,
                    magnitude=self.magnitude,
                    polarity=1,
                    novelty=0.3,
                    source_id="text-symbol",
                    metadata={"symbol_codepoint": ord(symbol), "position": index},
                )
            )
            if previous is not None:
                transition = f"{previous}\0{symbol}"
                pulses.append(
                    SignalPulse(
                        time_ms=time_ms,
                        channel=f"transition:{_stable_bucket(transition, self.channel_buckets)}",
                        magnitude=self.transition_magnitude,
                        polarity=1,
                        novelty=0.2,
                        source_id="text-transition",
                        metadata={"position": index},
                    )
                )
            previous = symbol
        return tuple(pulses)


@dataclass(slots=True)
class FrameDeltaTransducer:
    threshold: float = 0.15
    gain: float = 1.0
    previous: tuple[tuple[float, ...], ...] | None = None

    def observe(
        self,
        frame: Sequence[Sequence[float]],
        *,
        time_ms: float,
    ) -> tuple[SignalPulse, ...]:
        normalized = tuple(tuple(float(value) for value in row) for row in frame)
        if not normalized or not normalized[0]:
            raise ValueError("frame must be non-empty")
        width = len(normalized[0])
        if any(len(row) != width for row in normalized):
            raise ValueError("frame rows must have equal width")
        if self.previous is not None and (
            len(self.previous) != len(normalized) or len(self.previous[0]) != width
        ):
            raise ValueError("frame shape changed")

        pulses: list[SignalPulse] = []
        if self.previous is None:
            self.previous = normalized
            return ()
        for y, row in enumerate(normalized):
            for x, value in enumerate(row):
                delta = value - self.previous[y][x]
                if abs(delta) < self.threshold:
                    continue
                pulses.append(
                    SignalPulse(
                        time_ms=time_ms,
                        channel=f"pixel:{x}:{y}",
                        magnitude=abs(delta) * self.gain,
                        polarity=1 if delta >= 0 else -1,
                        location=(float(x), float(y)),
                        novelty=min(1.0, abs(delta) / max(self.threshold, 1e-9)),
                        source_id="frame-delta",
                    )
                )
        self.previous = normalized
        return tuple(pulses)


@dataclass(slots=True)
class TemporalExpectationTracker:
    """Learn a channel interval and emit an omission prediction-error pulse."""

    tolerance_fraction: float = 0.30
    min_observations: int = 3
    alpha: float = 0.35
    last_time: dict[str, float] = field(default_factory=dict)
    interval: dict[str, float] = field(default_factory=dict)
    observations: dict[str, int] = field(default_factory=dict)
    emitted_deadline: dict[str, float] = field(default_factory=dict)

    def observe(self, pulse: SignalPulse) -> None:
        channel = pulse.channel
        previous = self.last_time.get(channel)
        if previous is not None:
            observed = pulse.time_ms - previous
            if observed > 0:
                old = self.interval.get(channel, observed)
                self.interval[channel] = (1 - self.alpha) * old + self.alpha * observed
        self.last_time[channel] = pulse.time_ms
        self.observations[channel] = self.observations.get(channel, 0) + 1
        self.emitted_deadline.pop(channel, None)

    def poll(self, *, until_ms: float) -> tuple[SignalPulse, ...]:
        pulses: list[SignalPulse] = []
        for channel, last in sorted(self.last_time.items()):
            if self.observations.get(channel, 0) < self.min_observations:
                continue
            interval = self.interval.get(channel)
            if interval is None:
                continue
            deadline = last + interval * (1 + self.tolerance_fraction)
            if until_ms < deadline:
                continue
            if self.emitted_deadline.get(channel) == deadline:
                continue
            self.emitted_deadline[channel] = deadline
            pulses.append(
                SignalPulse(
                    time_ms=deadline,
                    channel=f"omission:{channel}",
                    magnitude=1.0,
                    polarity=1,
                    novelty=1.0,
                    prediction_error=1.0,
                    source_id="temporal-expectation",
                    metadata={"expected_channel": channel, "expected_interval_ms": interval},
                )
            )
        return tuple(pulses)


def pulse_train(
    channels: Iterable[str],
    *,
    start_ms: float = 0.0,
    interval_ms: float = 4.0,
    magnitude: float = 0.8,
) -> tuple[SignalPulse, ...]:
    return tuple(
        SignalPulse(
            time_ms=start_ms + index * interval_ms,
            channel=channel,
            magnitude=magnitude,
            source_id="pulse-train",
        )
        for index, channel in enumerate(channels)
    )
