from __future__ import annotations

import heapq
import math
import time
from dataclasses import asdict
from typing import Any

import torch

from ..model import BrainConfig, EngineStats, Event, EventKind, TraceFrame
from .config import LearnedConfig
from .contracts import PredictionRecord, WorkCounters
from .model import SparseRoutingModel, StepOutput


class LearnedBrainBackend:
    """C01-compatible inference backend for the learned sparse rate model."""

    def __init__(
        self, config: LearnedConfig | None = None, model: SparseRoutingModel | None = None
    ) -> None:
        self.learned_config = config or LearnedConfig()
        self.learned_config.validate()
        torch.manual_seed(self.learned_config.seed)
        self.model = model or SparseRoutingModel(self.learned_config)
        self.model.eval()
        self.config = BrainConfig(random_seed=self.learned_config.seed)
        self._stats = EngineStats()
        self.work = WorkCounters()
        self.time = 0.0
        self._queue: list[Event] = []
        self._sequence = 0
        self._prediction: str | None = None
        self._action: str | None = None
        self._last: StepOutput | None = None
        self._cached_record: PredictionRecord | None = None
        self._last_event: Event | None = None
        self.trace: list[TraceFrame] = []
        self.module_loads = [0] * self.learned_config.module_count

    @property
    def prediction(self) -> str | None:
        return self._prediction

    @property
    def action(self) -> str | None:
        return self._action

    @property
    def stats(self) -> EngineStats:
        return self._stats

    def reset(self, *, seed: int | None = None, config: BrainConfig | None = None) -> None:
        if config is not None:
            self.config = config
        if seed is not None:
            torch.manual_seed(seed)
        self.model.reset_runtime()
        self._stats = EngineStats()
        self.work = WorkCounters()
        self.time = 0.0
        self._queue = []
        self._sequence = 0
        self._prediction = None
        self._action = None
        self._last = None
        self._cached_record = None
        self._last_event = None
        self.trace = []
        self.module_loads = [0] * self.learned_config.module_count

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
        if time < self.time - 1e-9:
            raise ValueError(f"Cannot schedule an event in the past: {time} < {self.time}")
        if not math.isfinite(time) or not math.isfinite(strength):
            raise ValueError("Event time and strength must be finite")
        if isinstance(priority, bool) or not isinstance(priority, int):
            raise ValueError(f"Event priority must be an integer, got {priority!r}")
        event = Event(
            time,
            priority,
            self._sequence,
            EventKind(kind),
            source,
            target,
            strength,
            evidence_id,
            evidence_label,
            metadata or {},
        )
        self._sequence += 1
        heapq.heappush(self._queue, event)

    def run(self, *, max_events: int = 100_000) -> None:
        processed = 0
        while self._queue:
            if processed >= max_events:
                raise RuntimeError("Learned backend exceeded max_events")
            event = heapq.heappop(self._queue)
            self.time = event.time
            started = time.perf_counter()
            with torch.inference_mode():
                output = self.model.forward_step(
                    evidence=event.evidence_label or event.source,
                    source=event.source,
                    channel=str(event.metadata.get("channel", "evidence")),
                    strength=event.strength,
                    delay=float(event.metadata.get("delivery_delay", 0.0)),
                    condition=self.learned_config.condition,
                )
            self.work.wall_clock_seconds += time.perf_counter() - started
            self._consume(event, output)
            processed += 1

    def _consume(self, event: Event, output: StepOutput) -> None:
        self._last = output
        self._last_event = event
        probabilities = output.probabilities.tolist()
        order = sorted(range(len(probabilities)), key=probabilities.__getitem__, reverse=True)
        best, second = order[:2]
        confidence = probabilities[best]
        margin = confidence - probabilities[second]
        forced = self.learned_config.condition == "forced_prediction"
        ignited = forced or (
            confidence >= self.learned_config.confidence_threshold
            and margin >= self.learned_config.margin_threshold
        )
        self._prediction = self.learned_config.labels[best] if ignited else None
        self._action = self.learned_config.labels[int(output.action_logits.argmax())]
        selected = output.selected.tolist()
        for module in selected:
            self.module_loads[module] += 1
        k = len(selected)
        self.work.observations += 1
        self.work.conceptual_candidates += self.learned_config.module_count
        self.work.selected_modules += k
        self.work.state_updates += k
        self.work.evaluated_edges += k * k
        self.work.evaluated_messages += k * k
        self.work.dense_tensor_ops += 2  # encoder and router; local recurrent work is indexed
        self.work.kernel_launch_estimate += 12
        self.work.peak_memory_bytes = max(
            self.work.peak_memory_bytes,
            sum(
                parameter.numel() * parameter.element_size()
                for parameter in self.model.parameters()
            ),
        )
        self._stats.events_processed += 1
        self._stats.spark_updates += k
        self._stats.edge_evaluations += k * k
        self._stats.ignitions += int(ignited)
        self._stats.broadcasts += int(ignited and self.learned_config.workspace_broadcast)
        self._cached_record = self._build_prediction_record()

    def prediction_record(self) -> PredictionRecord:
        if self._last is None and self._cached_record is not None:
            return self._cached_record
        return self._build_prediction_record()

    def _build_prediction_record(self) -> PredictionRecord:
        if self._last is None:
            return PredictionRecord(None, None, {}, (), (), {})
        coalition = {
            "support": float(self._last.support),
            "diversity": float(self._last.diversity),
            "stability": float(self._last.stability),
            "contradiction": float(self._last.contradiction),
            "score": float(self._last.coalition_score),
        }
        return PredictionRecord(
            self.prediction,
            self.action,
            dict(zip(self.learned_config.labels, self._last.probabilities.tolist(), strict=True)),
            tuple(self._last.selected.tolist()),
            tuple(tuple(pair) for pair in self._last.selected_edges.tolist()),
            coalition,
        )

    def inspect_snapshot(self, *, external_event: str, truth: str | None = None) -> TraceFrame:
        record = self.prediction_record()
        selected = set(record.selected_modules)
        sparks = [
            {
                "id": f"learned:module:{index}",
                "kind": "feature",
                "selected": index in selected,
                "load": self.module_loads[index],
                "state_norm": float(self.model.module_state[index].norm()),
            }
            for index in range(self.learned_config.module_count)
        ]
        coalitions = ([{"label": record.belief, **record.coalition}] if record.coalition else [])
        workspace = (
            [{"label": record.belief, "action": record.action, "supports": list(selected)}]
            if record.belief is not None and self.learned_config.workspace_broadcast
            else []
        )
        return TraceFrame(
            self.time,
            external_event,
            truth,
            self.prediction,
            sparks,
            coalitions,
            workspace,
            [f"learned:module:{item}" for item in record.selected_modules],
            [(f"module:{a}", f"module:{b}", 1.0) for a, b in record.evidence_path],
            {**asdict(self._stats), **self.work.to_dict()},
        )

    def snapshot(self, *, external_event: str, truth: str | None = None) -> TraceFrame:
        frame = self.inspect_snapshot(external_event=external_event, truth=truth)
        self.trace.append(frame)
        return frame

    def state_dict(self, *, include_trace: bool = True) -> dict[str, Any]:
        return {
            "schema_version": "0.2",
            "backend": "learned-sparse-rate",
            "learned_config": self.learned_config.to_dict(),
            "model": {
                key: value.detach().cpu().tolist()
                for key, value in self.model.state_dict().items()
            },
            "module_state": self.model.module_state.detach().cpu().tolist(),
            "previous_probabilities": self.model.previous_probabilities.detach().cpu().tolist(),
            "time": self.time,
            "prediction": self._prediction,
            "action": self._action,
            "stats": asdict(self._stats),
            "work": self.work.to_dict(),
            "module_loads": self.module_loads,
            "queue": [asdict(item) for item in sorted(self._queue)],
            "sequence": self._sequence,
            "last_record": asdict(self.prediction_record()),
            "last_event": asdict(self._last_event) if self._last_event is not None else None,
            "trace": [asdict(item) for item in self.trace] if include_trace else [],
        }

    def load_state_dict(self, state: dict[str, Any]) -> None:
        if state.get("schema_version") != "0.2" or state.get("backend") != "learned-sparse-rate":
            raise ValueError("Unsupported learned backend state")
        current = self.model.state_dict()
        tensors = {
            key: torch.tensor(value, dtype=current[key].dtype)
            for key, value in state["model"].items()
        }
        self.model.load_state_dict(tensors)
        self.model.module_state = torch.tensor(state["module_state"], dtype=torch.float32)
        self.model.previous_probabilities = torch.tensor(
            state["previous_probabilities"], dtype=torch.float32
        )
        self.time = float(state["time"])
        self._prediction = state["prediction"]
        self._action = state["action"]
        self._stats = EngineStats(**state["stats"])
        self.work = WorkCounters(**state["work"])
        self.module_loads = list(state["module_loads"])
        self._queue = [
            Event(
                float(row["time"]),
                int(row["priority"]),
                int(row["sequence"]),
                EventKind(row["kind"]),
                row["source"],
                row.get("target"),
                float(row.get("strength", 0.0)),
                row.get("evidence_id"),
                row.get("evidence_label"),
                dict(row.get("metadata", {})),
            )
            for row in state.get("queue", [])
        ]
        sequences = [item.sequence for item in self._queue]
        if len(sequences) != len(set(sequences)):
            raise ValueError("Learned backend queue sequences must be unique")
        if any(
            not math.isfinite(item.time) or not math.isfinite(item.strength)
            for item in self._queue
        ):
            raise ValueError("Queued event time and strength must be finite")
        if any(item.time < self.time - 1e-9 for item in self._queue):
            raise ValueError("Learned backend state contains a queued event in the past")
        heapq.heapify(self._queue)
        self._sequence = int(state.get("sequence", 0))
        if sequences and self._sequence <= max(sequences):
            raise ValueError("Next event sequence must exceed queued event sequences")
        record = state.get("last_record")
        self._cached_record = (
            PredictionRecord(
                record["belief"],
                record["action"],
                dict(record["probabilities"]),
                tuple(record["selected_modules"]),
                tuple(tuple(pair) for pair in record["evidence_path"]),
                dict(record["coalition"]),
            )
            if record
            else None
        )
        self.trace = [TraceFrame(**row) for row in state.get("trace", [])]
        last_event = state.get("last_event")
        self._last_event = (
            Event(
                float(last_event["time"]),
                int(last_event["priority"]),
                int(last_event["sequence"]),
                EventKind(last_event["kind"]),
                last_event["source"],
                last_event.get("target"),
                float(last_event.get("strength", 0.0)),
                last_event.get("evidence_id"),
                last_event.get("evidence_label"),
                dict(last_event.get("metadata", {})),
            )
            if last_event
            else None
        )
