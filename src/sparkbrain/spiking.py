from __future__ import annotations

import math
import time
from dataclasses import asdict, dataclass, replace
from typing import Any

from .model import BrainConfig, EngineStats, EventKind, TraceFrame
from .worlds import SwitchEvent, build_reference_brain


@dataclass(frozen=True, slots=True)
class LIFConfig:
    """Frozen reduced LIF encoder parameters for the C07 CPU comparison."""

    membrane_decay: float = 0.5
    spike_threshold: float = 0.75
    filtered_decay: float = 0.8

    def validate(self) -> None:
        if not 0.0 <= self.membrane_decay < 1.0:
            raise ValueError("membrane_decay must be in [0, 1)")
        if not self.spike_threshold > 0.0 or not math.isfinite(self.spike_threshold):
            raise ValueError("spike_threshold must be positive and finite")
        if not 0.0 <= self.filtered_decay < 1.0:
            raise ValueError("filtered_decay must be in [0, 1)")


class SnnTorchLIFHybridBackend:
    """snnTorch CPU LIF input encoder with rate Coalition/Workspace semantics.

    The substrate boundary is narrow: external currents are encoded by deterministic
    LIF sensory units. The signed evidence graph, hypothesis state, Coalition scoring,
    ignition, and Workspace remain the C01 algorithmic implementation. This is a hybrid
    behavioral-equivalence backend, not a fully spiking cognitive architecture.
    """

    backend_name = "snntorch-lif-hybrid"

    def __init__(
        self,
        config: BrainConfig | None = None,
        *,
        lif_config: LIFConfig | None = None,
    ) -> None:
        try:
            import snntorch as snn
            import torch
        except ImportError as exc:
            raise RuntimeError(
                "SnnTorchLIFHybridBackend requires the optional 'spiking' dependencies"
            ) from exc
        self._torch = torch
        self._snn = snn
        self.lif_config = lif_config or LIFConfig()
        self.lif_config.validate()
        self._neuron = snn.Leaky(
            beta=self.lif_config.membrane_decay,
            threshold=self.lif_config.spike_threshold,
            reset_mechanism="zero",
        )
        self.engine = build_reference_brain(config)
        self.membrane: dict[str, float] = {}
        self.filtered_spikes: dict[str, float] = {}
        self.spike_count = 0
        self.message_count = 0
        self.lif_steps = 0
        self.cpu_seconds = 0.0
        self.spike_events: list[dict[str, float | str]] = []

    @property
    def prediction(self) -> str | None:
        return self.engine.prediction

    @property
    def stats(self) -> EngineStats:
        return self.engine.stats

    @property
    def config(self) -> BrainConfig:
        return self.engine.config

    @property
    def time(self) -> float:
        return self.engine.time

    @property
    def sparks(self):
        return self.engine.sparks

    @property
    def connections(self):
        return self.engine.connections

    @property
    def workspace(self):
        return self.engine.workspace

    @property
    def ignitions(self):
        return self.engine.ignitions

    @property
    def trace(self):
        return self.engine.trace

    @property
    def last_coalitions(self):
        return self.engine.last_coalitions

    def reset(
        self,
        *,
        seed: int | None = None,
        config: BrainConfig | None = None,
    ) -> None:
        selected = config or self.engine.config
        if seed is not None:
            selected = replace(selected, random_seed=seed)
        self.engine = build_reference_brain(selected)
        self.membrane.clear()
        self.filtered_spikes.clear()
        self.spike_count = self.message_count = self.lif_steps = 0
        self.cpu_seconds = 0.0
        self.spike_events.clear()

    def _encode_current(self, target: str, current: float, event_time: float) -> float:
        torch = self._torch
        membrane = torch.tensor(self.membrane.get(target, 0.0), dtype=torch.float64)
        spike, next_membrane = self._neuron(
            torch.tensor(current, dtype=torch.float64), membrane
        )
        spike_value = float(spike.item())
        filtered = (
            self.lif_config.filtered_decay * self.filtered_spikes.get(target, 0.0)
            + (1.0 - self.lif_config.filtered_decay) * spike_value
        )
        self.membrane[target] = float(next_membrane.item())
        self.filtered_spikes[target] = filtered
        self.lif_steps += 1
        self.spike_count += int(spike_value)
        if spike_value:
            self.message_count += 1
            self.spike_events.append(
                {
                    "target": target,
                    "time": event_time,
                    "input_current": current,
                    "filtered_spike": filtered,
                }
            )
            return current
        return 0.0

    def schedule(
        self,
        *,
        time: float,
        kind: EventKind,
        source: str,
        target: str | None,
        strength: float = 0.0,
        priority: int = 10,
        evidence_id: str | None = None,
        evidence_label: str | None = None,
        metadata: dict | None = None,
    ) -> None:
        encoded = strength
        merged = dict(metadata or {})
        if kind is EventKind.STIMULUS and target is not None:
            encoded = self._encode_current(target, strength, time)
            merged["spiking_backend"] = self.backend_name
            merged["lif_spike"] = bool(encoded)
        self.engine.schedule(
            time=time,
            kind=kind,
            source=source,
            target=target,
            strength=encoded,
            priority=priority,
            evidence_id=evidence_id,
            evidence_label=evidence_label,
            metadata=merged,
        )

    def inject_stimulus(
        self,
        *,
        target: str,
        label: str,
        time: float,
        strength: float = 1.0,
        source: str = "world",
        evidence_id: str | None = None,
        metadata: dict | None = None,
    ) -> None:
        identifier = evidence_id or f"{source}:{label}:{time:.6f}"
        self.schedule(
            time=time,
            kind=EventKind.STIMULUS,
            source=source,
            target=target,
            strength=strength,
            priority=0,
            evidence_id=identifier,
            evidence_label=label,
            metadata={"origin_kind": "external", **(metadata or {})},
        )

    def run(self, *, max_events: int = 100_000) -> None:
        started = time.perf_counter()
        self.engine.run(max_events=max_events)
        self.cpu_seconds += time.perf_counter() - started

    def _with_spiking_stats(self, frame: TraceFrame) -> TraceFrame:
        return replace(
            frame,
            stats={
                **frame.stats,
                "lif_steps": self.lif_steps,
                "spikes": self.spike_count,
                "spiking_messages": self.message_count,
            },
        )

    def inspect_snapshot(
        self,
        *,
        external_event: str,
        truth: str | None = None,
    ) -> TraceFrame:
        frame = self.engine.inspect_snapshot(external_event=external_event, truth=truth)
        return self._with_spiking_stats(frame)

    def snapshot(self, *, external_event: str, truth: str | None = None) -> TraceFrame:
        frame = self._with_spiking_stats(
            self.engine.snapshot(external_event=external_event, truth=truth)
        )
        self.engine.trace[-1] = frame
        return frame

    def export_graph(self) -> dict:
        return self.engine.export_graph()

    def state_dict(self, *, include_trace: bool = True) -> dict[str, Any]:
        return {
            "backend": self.backend_name,
            "lif_config": asdict(self.lif_config),
            "membrane": dict(self.membrane),
            "filtered_spikes": dict(self.filtered_spikes),
            "spike_count": self.spike_count,
            "message_count": self.message_count,
            "lif_steps": self.lif_steps,
            "cpu_seconds": self.cpu_seconds,
            "spike_events": list(self.spike_events),
            "engine_state": self.engine.state_dict(include_trace=include_trace),
        }

    def load_state_dict(self, state: dict[str, Any]) -> None:
        if state.get("backend") != self.backend_name:
            raise ValueError("State is not an snntorch-lif-hybrid backend state")
        lif_config = LIFConfig(**state["lif_config"])
        lif_config.validate()
        self.lif_config = lif_config
        self._neuron = self._snn.Leaky(
            beta=self.lif_config.membrane_decay,
            threshold=self.lif_config.spike_threshold,
            reset_mechanism="zero",
        )
        self.engine.load_state_dict(state["engine_state"])
        self.membrane = {str(k): float(v) for k, v in state["membrane"].items()}
        self.filtered_spikes = {
            str(k): float(v) for k, v in state["filtered_spikes"].items()
        }
        self.spike_count = int(state["spike_count"])
        self.message_count = int(state["message_count"])
        self.lif_steps = int(state["lif_steps"])
        self.cpu_seconds = float(state["cpu_seconds"])
        self.spike_events = [dict(item) for item in state["spike_events"]]


def run_spiking_scenario(
    events: list[SwitchEvent],
    *,
    backend: SnnTorchLIFHybridBackend | None = None,
) -> tuple[SnnTorchLIFHybridBackend, list[TraceFrame]]:
    backend = backend or SnnTorchLIFHybridBackend()
    frames: list[TraceFrame] = []
    for index, item in enumerate(events):
        backend.inject_stimulus(
            target=f"sensory:{item.evidence}",
            label=item.evidence,
            time=item.time,
            source=f"sensor:{item.evidence}",
            evidence_id=f"event:{index}:{item.evidence}",
            metadata={"sensor": item.evidence, "truth": item.truth, "note": item.note},
        )
        backend.run()
        frames.append(backend.snapshot(external_event=item.evidence, truth=item.truth))
    return backend, frames
