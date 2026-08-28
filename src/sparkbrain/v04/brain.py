from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

from .action import ActionAssociator
from .contracts import SignalPulse, V04StepResult, canonical_json
from .dynamics import (
    AssemblyMemory,
    BurstDetector,
    BurstDetectorConfig,
    CascadeTracker,
    CascadeTrackerConfig,
    IgnitionGate,
    IgnitionGateConfig,
)
from .field import ExcitableFieldConfig, TemporalExcitableField
from .plasticity import TimingPlasticityConfig, TimingPlasticityRule
from .topology import FieldTopology, grid_topology
from .transduction import (
    FrameDeltaTransducer,
    ScalarDeltaTransducer,
    TemporalExpectationTracker,
    TextPulseTransducer,
)


def _digest(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class V04BrainConfig:
    width: int = 8
    height: int = 8
    receptor_rows: int = 1
    topology_seed: int = 41
    settle_ms: float = 35.0
    enable_plasticity: bool = True
    enable_expectations: bool = True
    ignition_threshold: float = 4.2
    max_cascade_gap_ms: float = 6.0

    def validate(self) -> None:
        if self.width < 2 or self.height < 2:
            raise ValueError("width and height must be at least 2")
        if self.receptor_rows < 1 or self.receptor_rows > self.height:
            raise ValueError("receptor_rows must be within the field height")
        if self.settle_ms <= 0:
            raise ValueError("settle_ms must be positive")
        if self.ignition_threshold < 0:
            raise ValueError("ignition_threshold must be non-negative")
        if self.max_cascade_gap_ms <= 0:
            raise ValueError("max_cascade_gap_ms must be positive")


class IntegratedV04Brain:
    """Local event-driven reference brain for pre-semantic signal dynamics.

    The default path contains no text parser, concept labels, or answer-key
    adapter.  Raw sources are transduced into local pulses; timing, delayed
    propagation, adaptation, inhibition, recurrence, and optional plasticity
    determine whether activity becomes a burst, cascade, or ignition.
    """

    CHECKPOINT_SCHEMA = "sparkbrain-v04-checkpoint-1"

    def __init__(
        self,
        config: V04BrainConfig | None = None,
        *,
        topology: FieldTopology | None = None,
        field_config: ExcitableFieldConfig | None = None,
        burst_config: BurstDetectorConfig | None = None,
        cascade_config: CascadeTrackerConfig | None = None,
        ignition_config: IgnitionGateConfig | None = None,
        plasticity_config: TimingPlasticityConfig | None = None,
    ) -> None:
        self.config = config or V04BrainConfig()
        self.config.validate()
        self._topology = topology or grid_topology(
            width=self.config.width,
            height=self.config.height,
            receptor_rows=self.config.receptor_rows,
            seed=self.config.topology_seed,
        )
        self.field = TemporalExcitableField(self._topology, field_config)
        self.assembly_memory = AssemblyMemory()
        self.burst_detector = BurstDetector(burst_config)
        self.cascade_tracker = CascadeTracker(
            cascade_config
            or CascadeTrackerConfig(max_gap_ms=self.config.max_cascade_gap_ms),
            memory=self.assembly_memory,
        )
        self.ignition_gate = IgnitionGate(
            ignition_config or IgnitionGateConfig(threshold=self.config.ignition_threshold)
        )
        self.plasticity = TimingPlasticityRule(plasticity_config)
        self.action_associator = ActionAssociator()
        self.expectations = TemporalExpectationTracker()
        self.scalar_transducer = ScalarDeltaTransducer()
        self.text_transducer = TextPulseTransducer()
        self.frame_transducer = FrameDeltaTransducer()
        self.results: list[V04StepResult] = []
        self.trace: list[dict[str, Any]] = []
        self._step_index = 0

    @property
    def current_time_ms(self) -> float:
        return self.field.current_time_ms

    def _record_result(self, result: V04StepResult) -> None:
        self.results.append(result)
        self.trace.append(
            {
                "result": result.as_dict(),
                "step_index": self._step_index,
            }
        )
        self._step_index += 1

    def ingest_pulses(
        self,
        pulses: Iterable[SignalPulse],
        *,
        settle_ms: float | None = None,
    ) -> V04StepResult:
        rows = tuple(sorted(pulses, key=lambda row: (row.time_ms, row.channel)))
        start_ms = self.current_time_ms
        if rows and rows[0].time_ms < start_ms:
            raise ValueError("input pulse predates current brain time")
        for pulse in rows:
            self.field.schedule_pulse(pulse)
            if self.config.enable_expectations and not pulse.channel.startswith("omission:"):
                self.expectations.observe(pulse)
        last_input_ms = rows[-1].time_ms if rows else start_ms
        end_ms = last_input_ms + (self.config.settle_ms if settle_ms is None else settle_ms)
        omission_pulses: tuple[SignalPulse, ...] = ()
        if self.config.enable_expectations:
            omission_pulses = self.expectations.poll(until_ms=end_ms)
            for pulse in omission_pulses:
                self.field.schedule_pulse(pulse)
        all_pulses = tuple(
            sorted(rows + omission_pulses, key=lambda row: (row.time_ms, row.channel))
        )
        spikes = self.field.run_until(end_ms)
        bursts = self.burst_detector.update(spikes)
        cascades = self.cascade_tracker.update(spikes, flush_until_ms=end_ms)
        ignitions = self.ignition_gate.evaluate(cascades)
        if self.config.enable_plasticity:
            self.plasticity.apply(self.field, spikes)
        action = self.action_associator.choose(ignitions)
        trace_payload = {
            "bursts": [row.as_dict() for row in bursts],
            "cascades": [row.as_dict() for row in cascades],
            "ignitions": [row.as_dict() for row in ignitions],
            "pulses": [row.as_dict() for row in all_pulses],
            "spikes": [row.as_dict() for row in spikes],
        }
        result = V04StepResult(
            start_ms=start_ms,
            end_ms=end_ms,
            input_pulses=all_pulses,
            spikes=spikes,
            bursts=bursts,
            cascades=cascades,
            ignitions=ignitions,
            action=action,
            field_state_hash=self.field.state_hash(),
            trace_hash=_digest(trace_payload),
        )
        self._record_result(result)
        return result

    def advance(self, until_ms: float) -> V04StepResult:
        if until_ms < self.current_time_ms:
            raise ValueError("until_ms cannot move backwards")
        start = self.current_time_ms
        omissions: tuple[SignalPulse, ...] = ()
        if self.config.enable_expectations:
            omissions = self.expectations.poll(until_ms=until_ms)
            for pulse in omissions:
                self.field.schedule_pulse(pulse)
        spikes = self.field.run_until(until_ms)
        bursts = self.burst_detector.update(spikes)
        cascades = self.cascade_tracker.update(spikes, flush_until_ms=until_ms)
        ignitions = self.ignition_gate.evaluate(cascades)
        if self.config.enable_plasticity:
            self.plasticity.apply(self.field, spikes)
        action = self.action_associator.choose(ignitions)
        trace_payload = {
            "bursts": [row.as_dict() for row in bursts],
            "cascades": [row.as_dict() for row in cascades],
            "ignitions": [row.as_dict() for row in ignitions],
            "pulses": [row.as_dict() for row in omissions],
            "spikes": [row.as_dict() for row in spikes],
        }
        result = V04StepResult(
            start_ms=start,
            end_ms=until_ms,
            input_pulses=omissions,
            spikes=spikes,
            bursts=bursts,
            cascades=cascades,
            ignitions=ignitions,
            action=action,
            field_state_hash=self.field.state_hash(),
            trace_hash=_digest(trace_payload),
        )
        self._record_result(result)
        return result

    def observe_text(self, text: str, *, start_ms: float | None = None) -> V04StepResult:
        start = self.current_time_ms if start_ms is None else start_ms
        return self.ingest_pulses(self.text_transducer.encode(text, start_ms=start))

    def observe_scalar(
        self,
        channel: str,
        value: float,
        *,
        time_ms: float | None = None,
    ) -> V04StepResult:
        time = self.current_time_ms if time_ms is None else time_ms
        return self.ingest_pulses(self.scalar_transducer.observe(channel, value, time_ms=time))

    def observe_frame(
        self,
        frame: Sequence[Sequence[float]],
        *,
        time_ms: float | None = None,
    ) -> V04StepResult:
        time = self.current_time_ms if time_ms is None else time_ms
        return self.ingest_pulses(self.frame_transducer.observe(frame, time_ms=time))

    def reward(self, value: float) -> None:
        self.plasticity.reward(value)
        self.action_associator.reward(value)

    def inspect(self) -> dict[str, Any]:
        return {
            "action_state": self.action_associator.state_dict(),
            "assembly_memory": self.assembly_memory.state_dict(),
            "config": asdict(self.config),
            "current_time_ms": self.current_time_ms,
            "field_state_hash": self.field.state_hash(),
            "last_result": self.results[-1].as_dict() if self.results else None,
            "plasticity_updates": self.plasticity.update_count,
            "result_count": len(self.results),
            "trace_hash": _digest(self.trace),
        }

    def state_hash(self) -> str:
        return _digest(self.inspect())

    def checkpoint_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "action": self.action_associator.state_dict(),
            "assembly_memory": self.assembly_memory.state_dict(),
            "brain_config": asdict(self.config),
            "field": self.field.state_dict(),
            "results": [row.as_dict() for row in self.results],
            "schema": self.CHECKPOINT_SCHEMA,
            "step_index": self._step_index,
            "trace": self.trace,
        }
        return {"payload": payload, "sha256": _digest(payload)}

    def save_checkpoint(self, path: str | Path) -> None:
        target = Path(path)
        if target.exists():
            raise FileExistsError(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(canonical_json(self.checkpoint_dict()) + "\n", encoding="utf-8")

    @classmethod
    def load_checkpoint(cls, path: str | Path) -> IntegratedV04Brain:
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        if set(raw) != {"payload", "sha256"}:
            raise ValueError("checkpoint wrapper is invalid")
        payload = raw["payload"]
        if _digest(payload) != raw["sha256"]:
            raise ValueError("checkpoint hash mismatch")
        if payload.get("schema") != cls.CHECKPOINT_SCHEMA:
            raise ValueError("unsupported checkpoint schema")
        config = V04BrainConfig(**payload["brain_config"])
        brain = cls(config)
        brain.field = TemporalExcitableField.from_state_dict(payload["field"])
        memory = payload["assembly_memory"]
        brain.assembly_memory.counts = {str(k): int(v) for k, v in memory["counts"].items()}
        brain.assembly_memory.last_seen_ms = {
            str(k): float(v) for k, v in memory["last_seen_ms"].items()
        }
        action = payload["action"]
        brain.action_associator.actions = tuple(action["actions"])
        brain.action_associator.learning_rate = float(action["learning_rate"])
        brain.action_associator.scores = {
            str(signature): {str(k): float(v) for k, v in table.items()}
            for signature, table in action["scores"].items()
        }
        brain.action_associator.last_signature = action["last_signature"]
        brain.action_associator.last_action = action["last_action"]
        brain.trace = list(payload["trace"])
        brain._step_index = int(payload["step_index"])
        # Results remain in the immutable trace; direct field continuation is
        # the checkpoint's operational contract.
        return brain
