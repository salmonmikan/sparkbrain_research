from __future__ import annotations

import heapq
import time
from pathlib import Path
from typing import Any

import torch

from ..learned.backend import LearnedBrainBackend
from ..learned.checkpoint import load_checkpoint
from ..learned.config import LearnedConfig
from .config import StructuralConfig
from .contracts import StructuralStats
from .controller import StructuralController
from .model import StructuralSparseModel, StructuralStep


class StructuralBrainBackend(LearnedBrainBackend):
    """C01 backend with fixed-capacity structural masks and boundary events."""

    def __init__(
        self,
        learned_config: LearnedConfig,
        structural_config: StructuralConfig,
        model: StructuralSparseModel,
    ) -> None:
        expanded = LearnedConfig.from_dict(
            {
                **learned_config.to_dict(),
                "module_count": structural_config.max_modules,
                "active_k": structural_config.active_k,
            }
        )
        super().__init__(expanded, model)  # type: ignore[arg-type]
        self.structural_config = structural_config
        self.structural_model = model
        self.controller = StructuralController(structural_config, model)
        self.optimizer_state: dict[str, Any] = {}
        self._structural_stats = self._empty_stats()
        self._previous_confidence = 1 / len(expanded.labels)

    @classmethod
    def from_c04_checkpoint(
        cls, checkpoint: str | Path, structural_config: StructuralConfig
    ) -> StructuralBrainBackend:
        learned, source_model, _ = load_checkpoint(checkpoint)
        if learned.module_count != structural_config.source_modules:
            raise ValueError("C04 source module count does not match structural config")
        torch.manual_seed(structural_config.seed)
        model = StructuralSparseModel(learned, structural_config)
        model.import_source(source_model.state_dict(), structural_config.source_modules)
        model.eval()
        return cls(learned, structural_config, model)

    def _empty_stats(self) -> StructuralStats:
        size = self.structural_config.max_modules
        return StructuralStats(
            [0.0] * size,
            [[0.0] * size for _ in range(size)],
            [[0.0] * size for _ in range(size)],
            [0.0] * size,
        )

    def reset(self, *, seed=None, config=None) -> None:
        super().reset(seed=seed, config=config)
        self._structural_stats = self._empty_stats()
        self._previous_confidence = 1 / len(self.learned_config.labels)

    def run(self, *, max_events: int = 100_000) -> None:
        processed = 0
        while self._queue:
            if processed >= max_events:
                raise RuntimeError("Structural backend exceeded max_events")
            event = heapq.heappop(self._queue)
            self.time = event.time
            started = time.perf_counter()
            with torch.inference_mode():
                output = self.structural_model.forward_step(
                    evidence=event.evidence_label or event.source,
                    source=event.source,
                    channel=str(event.metadata.get("channel", "evidence")),
                    strength=event.strength,
                    delay=float(event.metadata.get("delivery_delay", 0.0)),
                )
            self.work.wall_clock_seconds += time.perf_counter() - started
            self._consume_structural(event, output)
            processed += 1

    def _consume_structural(self, event, output: StructuralStep) -> None:
        super()._consume(event, output)  # type: ignore[arg-type]
        selected = output.selected.tolist()
        conceptual = len(selected) ** 2
        actual = int(output.selected_edges.shape[0])
        self.work.evaluated_edges += actual - conceptual
        self.work.evaluated_messages += actual - conceptual
        self._stats.edge_evaluations += actual - conceptual
        confidence = float(output.probabilities.max())
        delta = confidence - self._previous_confidence
        self._previous_confidence = confidence
        decay = self.structural_config.credit_decay
        for index in range(self.structural_config.max_modules):
            self._structural_stats.routing_load[index] *= decay
            self._structural_stats.confidence_delta[index] *= decay
            for target in range(self.structural_config.max_modules):
                self._structural_stats.coactivation[index][target] *= decay
                self._structural_stats.edge_credit[index][target] *= decay
        for source in selected:
            self._structural_stats.routing_load[source] += 1.0
            self._structural_stats.confidence_delta[source] += delta
            for target in selected:
                self._structural_stats.coactivation[source][target] += 1.0
        for source, target in output.selected_edges.tolist():
            self._structural_stats.edge_credit[source][target] += max(0.0, delta) + 0.01

    def structural_stats(self) -> StructuralStats:
        return StructuralStats(
            list(self._structural_stats.routing_load),
            [list(row) for row in self._structural_stats.coactivation],
            [list(row) for row in self._structural_stats.edge_credit],
            list(self._structural_stats.confidence_delta),
        )

    def discover_and_queue(self, *, next_boundary: int):
        return self.controller.discover(self.structural_stats(), next_boundary=next_boundary)

    def apply_reward_eligibility(self, reward: float) -> None:
        if not self.structural_config.reward_eligibility:
            return
        for source, target in torch.nonzero(
            self.structural_model.active_edge_mask, as_tuple=False
        ).tolist():
            self._structural_stats.edge_credit[source][target] += reward * 0.01

    def apply_boundary(self, boundary: int):
        return self.controller.apply_boundary(boundary)

    def inspect_snapshot(self, *, external_event: str, truth: str | None = None):
        frame = super().inspect_snapshot(external_event=external_event, truth=truth)
        identities = self.controller.identities
        for index, row in enumerate(frame.sparks):
            identity = identities.get(index)
            row["active"] = bool(self.structural_model.active_module_mask[index])
            row["logical_id"] = identity.logical_id if identity else None
            row["version"] = identity.version if identity else None
            row["lineage"] = list(identity.parents) if identity else []
        frame.stats.update(
            {
                "active_modules": int(self.structural_model.active_module_mask.sum()),
                "active_edges": int(self.structural_model.active_edge_mask.sum()),
                "structural_events": self.controller.events_applied,
                "structural_rejections": self.controller.events_rejected,
                "homeostatic_updates": self.controller.homeostatic_updates,
            }
        )
        return frame

    def state_dict(self, *, include_trace: bool = True) -> dict[str, Any]:
        state = super().state_dict(include_trace=include_trace)
        state["backend"] = "structural-sparse-rate"
        state["structural_config"] = self.structural_config.to_dict()
        state["structural_controller"] = self.controller.state_dict()
        state["structural_stats"] = {
            "routing_load": self._structural_stats.routing_load,
            "coactivation": self._structural_stats.coactivation,
            "edge_credit": self._structural_stats.edge_credit,
            "confidence_delta": self._structural_stats.confidence_delta,
        }
        state["previous_confidence"] = self._previous_confidence
        state["optimizer_state"] = self.optimizer_state
        return state

    def load_state_dict(self, state: dict[str, Any]) -> None:
        if state.get("backend") != "structural-sparse-rate":
            raise ValueError("Unsupported structural backend state")
        restored_config = StructuralConfig.from_dict(state.get("structural_config", {}))
        if restored_config != self.structural_config:
            raise ValueError("Structural checkpoint config does not match backend config")
        parent_state = dict(state)
        parent_state["backend"] = "learned-sparse-rate"
        super().load_state_dict(parent_state)
        self.controller.load_state_dict(state["structural_controller"])
        stats = state["structural_stats"]
        self._structural_stats = StructuralStats(
            list(stats["routing_load"]),
            [list(row) for row in stats["coactivation"]],
            [list(row) for row in stats["edge_credit"]],
            list(stats["confidence_delta"]),
        )
        self._structural_stats.validate(self.structural_config.max_modules)
        self._previous_confidence = float(state["previous_confidence"])
        self.optimizer_state = dict(state.get("optimizer_state", {}))
