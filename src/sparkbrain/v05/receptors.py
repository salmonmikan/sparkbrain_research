from __future__ import annotations

import math
from dataclasses import asdict, dataclass, field
from typing import Any, Iterable

from sparkbrain.v04.contracts import SignalPulse

from .contracts import ReceptorTrace


@dataclass(frozen=True, slots=True)
class ReceptorConfig:
    fast_tau_ms: float = 5.0
    medium_tau_ms: float = 22.0
    slow_tau_ms: float = 120.0
    gain_tau_ms: float = 180.0
    direct_gain: float = 0.95
    derivative_gain: float = 0.42
    novelty_gain: float = 0.28
    prediction_error_gain: float = 0.45
    emission_threshold: float = 0.08
    target_abs_input: float = 1.20
    min_gain: float = 1.00
    max_gain: float = 2.4
    output_cap: float = 2.0

    def validate(self) -> None:
        for name in ("fast_tau_ms", "medium_tau_ms", "slow_tau_ms", "gain_tau_ms"):
            if getattr(self, name) <= 0:
                raise ValueError(f"{name} must be positive")
        if not 0 <= self.emission_threshold < self.output_cap:
            raise ValueError("emission_threshold must be in [0, output_cap)")
        if not 0 < self.min_gain <= self.max_gain:
            raise ValueError("gain bounds are invalid")


@dataclass(slots=True)
class _ChannelState:
    fast: float = 0.0
    medium: float = 0.0
    slow: float = 0.0
    mean_abs: float = 0.0
    last_time_ms: float = 0.0
    observations: int = 0


@dataclass(slots=True)
class MultiTimescaleReceptorBank:
    config: ReceptorConfig = field(default_factory=ReceptorConfig)
    channels: dict[str, _ChannelState] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.config.validate()

    @staticmethod
    def _decay(value: float, elapsed_ms: float, tau_ms: float) -> float:
        return value * math.exp(-max(0.0, elapsed_ms) / tau_ms)

    def _observe_one(self, pulse: SignalPulse) -> tuple[SignalPulse | None, ReceptorTrace]:
        state = self.channels.setdefault(pulse.channel, _ChannelState(last_time_ms=pulse.time_ms))
        if pulse.time_ms < state.last_time_ms:
            raise ValueError("receptor time cannot move backwards")
        elapsed = pulse.time_ms - state.last_time_ms
        state.fast = self._decay(state.fast, elapsed, self.config.fast_tau_ms)
        state.medium = self._decay(state.medium, elapsed, self.config.medium_tau_ms)
        state.slow = self._decay(state.slow, elapsed, self.config.slow_tau_ms)
        state.mean_abs = self._decay(state.mean_abs, elapsed, self.config.gain_tau_ms)

        signed = pulse.magnitude * pulse.polarity
        previous_fast = state.fast
        state.fast += signed
        state.medium += signed
        state.slow += signed
        state.mean_abs += abs(signed)
        state.last_time_ms = pulse.time_ms
        state.observations += 1

        derivative = state.fast - state.medium
        novelty = abs(state.fast - state.slow) / (0.20 + abs(state.slow))
        gain = self.config.target_abs_input / max(0.08, state.mean_abs)
        gain = max(self.config.min_gain, min(self.config.max_gain, gain))
        drive = gain * (
            self.config.direct_gain * abs(signed)
            + self.config.derivative_gain * abs(derivative)
            + self.config.novelty_gain * novelty
            + self.config.prediction_error_gain * pulse.prediction_error
        )
        emitted_magnitude = min(self.config.output_cap, drive)
        emitted = emitted_magnitude >= self.config.emission_threshold
        output: SignalPulse | None = None
        if emitted:
            direction = 1 if signed + derivative >= 0 else -1
            output = SignalPulse(
                time_ms=pulse.time_ms,
                channel=f"v05:{pulse.channel}",
                magnitude=emitted_magnitude,
                polarity=direction,
                location=pulse.location,
                novelty=min(1.0, max(pulse.novelty, novelty)),
                prediction_error=pulse.prediction_error,
                source_id="v05-receptor",
                metadata={
                    "origin_channel": pulse.channel,
                    "origin_source_id": pulse.source_id,
                    "previous_fast": previous_fast,
                    "receptor_observations": state.observations,
                },
            )
        trace = ReceptorTrace(
            time_ms=pulse.time_ms,
            channel=pulse.channel,
            signed_input=signed,
            fast_trace=state.fast,
            medium_trace=state.medium,
            slow_trace=state.slow,
            derivative=derivative,
            novelty=novelty,
            gain=gain,
            emitted_magnitude=emitted_magnitude,
            emitted=emitted,
        )
        return output, trace

    def process(
        self,
        pulses: Iterable[SignalPulse],
    ) -> tuple[tuple[SignalPulse, ...], tuple[ReceptorTrace, ...]]:
        emitted: list[SignalPulse] = []
        traces: list[ReceptorTrace] = []
        for pulse in sorted(pulses, key=lambda row: (row.time_ms, row.channel)):
            output, trace = self._observe_one(pulse)
            traces.append(trace)
            if output is not None:
                emitted.append(output)
        return tuple(emitted), tuple(traces)

    def state_dict(self) -> dict[str, Any]:
        return {
            "channels": {
                name: asdict(state) for name, state in sorted(self.channels.items())
            },
            "config": asdict(self.config),
        }

    @classmethod
    def from_state_dict(cls, value: dict[str, Any]) -> MultiTimescaleReceptorBank:
        bank = cls(ReceptorConfig(**value["config"]))
        bank.channels = {
            str(name): _ChannelState(**row) for name, row in value["channels"].items()
        }
        return bank
