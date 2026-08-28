from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from sparkbrain.v04.brain import IntegratedV04Brain, V04BrainConfig
from sparkbrain.v04.contracts import SignalPulse, canonical_json
from sparkbrain.v04.dynamics import CascadeTrackerConfig, IgnitionGateConfig
from sparkbrain.v04.field import ExcitableFieldConfig, TemporalExcitableField

from .action import ActionPolicyConfig, AssemblyActionPolicy
from .assemblies import AssemblyConfig, TemporalAssemblyMemory, patterns_from_step
from .contracts import (
    ActionDecision,
    AssemblyActivation,
    PredictionDecision,
    V05StepResult,
)
from .homeostasis import HomeostasisConfig, HomeostaticController
from .plasticity import V05PlasticityConfig, V05PlasticityController
from .prediction import AssemblyPredictor
from .receptors import MultiTimescaleReceptorBank, ReceptorConfig
from .topology import layered_reservoir_topology


def _digest(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class V05BrainConfig:
    width: int = 8
    height: int = 8
    receptor_rows: int = 1
    topology_seed: int = 41
    settle_ms: float = 32.0
    enable_receptor_bank: bool = True
    enable_homeostasis: bool = True
    enable_weight_learning: bool = True
    enable_delay_learning: bool = True
    enable_reward_modulation: bool = False
    enable_assembly: bool = True
    enable_prediction: bool = True
    enable_action: bool = True
    pattern_temporal_bin_ms: float = 0.25
    min_pattern_spikes: int = 2


class IntegratedV05Brain:
    """Pre-semantic learning substrate built on the frozen v0.4 field.

    Runtime dynamics never receive motif IDs or evaluator labels.  Repeated
    spatiotemporal activity is clustered into anonymous Assembly candidates;
    only observed future events and scalar rewards attach function to them.
    """

    CHECKPOINT_SCHEMA = "sparkbrain-v05-checkpoint-1"

    def __init__(
        self,
        config: V05BrainConfig | None = None,
        *,
        receptor_config: ReceptorConfig | None = None,
        assembly_config: AssemblyConfig | None = None,
        homeostasis_config: HomeostasisConfig | None = None,
        plasticity_config: V05PlasticityConfig | None = None,
        action_config: ActionPolicyConfig | None = None,
    ) -> None:
        self.config = config or V05BrainConfig()
        base_config = V04BrainConfig(
            width=self.config.width,
            height=self.config.height,
            receptor_rows=self.config.receptor_rows,
            topology_seed=self.config.topology_seed,
            settle_ms=self.config.settle_ms,
            enable_plasticity=False,
            enable_expectations=False,
            ignition_threshold=4.0,
            max_cascade_gap_ms=6.0,
        )
        self.base = IntegratedV04Brain(
            base_config,
            topology=layered_reservoir_topology(seed=self.config.topology_seed),
            field_config=ExcitableFieldConfig(
                input_gain=1.35,
                receptor_fanout=2,
                max_events_per_run=120_000,
                max_spikes_per_run=20_000,
            ),
            cascade_config=CascadeTrackerConfig(max_gap_ms=6.0, min_spikes=2),
            ignition_config=IgnitionGateConfig(threshold=4.0, min_spikes=4, min_units=3),
        )
        self.receptors = MultiTimescaleReceptorBank(receptor_config or ReceptorConfig())
        self.assemblies = TemporalAssemblyMemory(assembly_config or AssemblyConfig())
        plastic_cfg = plasticity_config or V05PlasticityConfig(
            enable_weight_learning=self.config.enable_weight_learning,
            enable_delay_learning=self.config.enable_delay_learning,
        )
        self.plasticity = V05PlasticityController(plastic_cfg)
        self.homeostasis = HomeostaticController(homeostasis_config or HomeostasisConfig())
        self.predictor = AssemblyPredictor()
        self.action_policy = AssemblyActionPolicy(action_config or ActionPolicyConfig())
        self.results: list[V05StepResult] = []
        self.trace: list[dict[str, Any]] = []
        self.pending_activation: AssemblyActivation | None = None
        self.pending_action: ActionDecision | None = None
        self.suppressed_unit_ids: set[int] = set()
        self._episode_index = 0

    @property
    def current_time_ms(self) -> float:
        return self.base.current_time_ms

    def _apply_unit_suppression(self) -> dict[int, float]:
        original: dict[int, float] = {}
        for unit_id in self.suppressed_unit_ids:
            if unit_id not in self.base.field.units:
                continue
            unit = self.base.field.units[unit_id]
            original[unit_id] = unit.base_threshold
            unit.base_threshold = 1e9
        return original

    def _restore_unit_suppression(self, original: dict[int, float]) -> None:
        for unit_id, threshold in original.items():
            self.base.field.units[unit_id].base_threshold = threshold

    def process_episode(
        self,
        pulses: Iterable[SignalPulse],
        *,
        learn_assembly: bool = True,
        learn_field: bool = True,
        metadata: dict[str, Any] | None = None,
        episode_id: str | None = None,
        explore_action: bool | None = None,
    ) -> V05StepResult:
        resolved_episode_id = episode_id or f"runtime-episode-{self._episode_index:08d}"
        if not resolved_episode_id:
            raise ValueError("episode_id must be non-empty")
        raw = tuple(sorted(pulses, key=lambda row: (row.time_ms, row.channel)))
        if raw and raw[0].time_ms < self.current_time_ms:
            raise ValueError("episode pulses predate current brain time")
        if self.config.enable_receptor_bank:
            emitted, receptor_traces = self.receptors.process(raw)
        else:
            emitted, receptor_traces = raw, ()
        original_thresholds = self._apply_unit_suppression()
        try:
            base_result = self.base.ingest_pulses(emitted, settle_ms=self.config.settle_ms)
        finally:
            self._restore_unit_suppression(original_thresholds)
        if learn_field:
            self.plasticity.apply(self.base.field, base_result.spikes)
        if self.config.enable_homeostasis and learn_field:
            stability = self.homeostasis.observe(
                self.base.field,
                base_result.spikes,
                time_ms=base_result.end_ms,
            )
        else:
            stability = self.homeostasis.snapshot(
                self.base.field,
                base_result.spikes,
                time_ms=base_result.end_ms,
            )
        patterns = patterns_from_step(
            base_result.cascades,
            base_result.spikes,
            temporal_bin_ms=self.config.pattern_temporal_bin_ms,
            excluded_unit_ids=self.base.field.receptor_ids,
            source_kind="internal_reservoir",
        )
        activations: list[AssemblyActivation] = []
        if self.config.enable_assembly:
            for pattern in patterns:
                if pattern.spike_count < self.config.min_pattern_spikes:
                    continue
                activation = self.assemblies.observe(
                    pattern,
                    time_ms=pattern.end_ms,
                    episode_id=resolved_episode_id,
                    learn=learn_assembly,
                )
                if activation is not None:
                    activations.append(activation)
        usable = [row for row in activations if row.mature and not row.suppressed]
        strongest = max(
            usable,
            key=lambda row: (row.similarity, row.episode_count, row.assembly_id),
            default=None,
        )
        prediction = (
            self.predictor.predict(strongest)
            if self.config.enable_prediction
            else PredictionDecision(None, None, 0.0)
        )
        action = (
            self.action_policy.choose(
                strongest,
                explore=learn_assembly if explore_action is None else bool(explore_action),
            )
            if self.config.enable_action
            else ActionDecision(None, None, 0.0)
        )
        self.pending_activation = strongest
        self.pending_action = action
        payload = {
            "action": action.as_dict(),
            "activations": [row.as_dict() for row in activations],
            "base_trace_hash": base_result.trace_hash,
            "episode_id": resolved_episode_id,
            "prediction": prediction.as_dict(),
            "stability": stability.as_dict(),
        }
        result = V05StepResult(
            start_ms=base_result.start_ms,
            end_ms=base_result.end_ms,
            raw_pulses=raw,
            emitted_pulses=emitted,
            receptor_traces=receptor_traces,
            v04_result=base_result,
            patterns=patterns,
            assembly_activations=tuple(activations),
            prediction=prediction,
            action=action,
            stability=stability,
            state_hash=self.state_hash(),
            trace_hash=_digest(payload),
            metadata={"episode_id": resolved_episode_id, **dict(metadata or {})},
        )
        self.results.append(result)
        self.trace.append(
            {
                "episode_id": resolved_episode_id,
                "episode_index": self._episode_index,
                "result": result.as_dict(),
            }
        )
        self._episode_index += 1
        return result

    def learn_outcome(self, *, next_event: str | None, reward: float | None) -> None:
        if self.config.enable_prediction:
            self.predictor.observe(self.pending_activation, next_event)
        if reward is not None:
            # Assembly formation is driven by local temporal plasticity.  Scalar
            # action reward modulates field plasticity only in an explicit track;
            # otherwise early exploration would randomly reshape the substrate.
            if self.config.enable_reward_modulation:
                self.plasticity.reward(reward)
            if self.config.enable_action:
                self.action_policy.reward(reward)

    def suppress_assembly(self, assembly_id: str) -> None:
        self.assemblies.suppress(assembly_id)

    def unsuppress_assembly(self, assembly_id: str) -> None:
        self.assemblies.unsuppress(assembly_id)

    def suppress_units(self, unit_ids: Iterable[int]) -> None:
        self.suppressed_unit_ids.update(int(value) for value in unit_ids)

    def clear_unit_suppression(self) -> None:
        self.suppressed_unit_ids.clear()

    def _base_checkpoint(self) -> dict[str, Any]:
        """Return the operational v0.4 state without duplicating immutable results."""
        wrapper = self.base.checkpoint_dict()
        payload = json.loads(canonical_json(wrapper["payload"]))
        payload["results"] = []
        return {"payload": payload, "sha256": _digest(payload)}

    def state_dict(self) -> dict[str, Any]:
        return {
            "action": self.action_policy.state_dict(),
            "assemblies": self.assemblies.state_dict(),
            "base": self._base_checkpoint(),
            "config": asdict(self.config),
            "episode_index": self._episode_index,
            "homeostasis": self.homeostasis.state_dict(),
            "pending_action": (
                self.pending_action.as_dict() if self.pending_action is not None else None
            ),
            "pending_activation": (
                self.pending_activation.as_dict() if self.pending_activation is not None else None
            ),
            "plasticity": self.plasticity.state_dict(),
            "predictor": self.predictor.state_dict(),
            "receptors": self.receptors.state_dict(),
            "schema": self.CHECKPOINT_SCHEMA,
            "suppressed_unit_ids": sorted(self.suppressed_unit_ids),
            "trace": self.trace,
        }

    def state_hash(self) -> str:
        return _digest(self.state_dict())

    def save_checkpoint(self, path: str | Path) -> None:
        target = Path(path)
        if target.exists():
            raise FileExistsError(target)
        payload = self.state_dict()
        wrapper = {"payload": payload, "sha256": _digest(payload)}
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(canonical_json(wrapper) + "\n", encoding="utf-8")

    @classmethod
    def load_checkpoint(cls, path: str | Path) -> IntegratedV05Brain:
        wrapper = json.loads(Path(path).read_text(encoding="utf-8"))
        if set(wrapper) != {"payload", "sha256"}:
            raise ValueError("checkpoint wrapper is invalid")
        payload = wrapper["payload"]
        if _digest(payload) != wrapper["sha256"]:
            raise ValueError("checkpoint hash mismatch")
        if payload.get("schema") != cls.CHECKPOINT_SCHEMA:
            raise ValueError("unsupported checkpoint schema")
        brain = cls(V05BrainConfig(**payload["config"]))
        base_payload = payload["base"]["payload"]
        if _digest(base_payload) != payload["base"]["sha256"]:
            raise ValueError("nested v0.4 checkpoint hash mismatch")
        brain.base.field = TemporalExcitableField.from_state_dict(base_payload["field"])
        memory = base_payload["assembly_memory"]
        brain.base.assembly_memory.counts = {str(k): int(v) for k, v in memory["counts"].items()}
        brain.base.assembly_memory.last_seen_ms = {
            str(k): float(v) for k, v in memory["last_seen_ms"].items()
        }
        action = base_payload["action"]
        brain.base.action_associator.actions = tuple(action["actions"])
        brain.base.action_associator.learning_rate = float(action["learning_rate"])
        brain.base.action_associator.scores = {
            str(signature): {str(k): float(v) for k, v in table.items()}
            for signature, table in action["scores"].items()
        }
        brain.base.action_associator.last_signature = action["last_signature"]
        brain.base.action_associator.last_action = action["last_action"]
        brain.base.trace = list(base_payload["trace"])
        brain.base._step_index = int(base_payload["step_index"])
        brain.receptors = MultiTimescaleReceptorBank.from_state_dict(payload["receptors"])
        brain.assemblies = TemporalAssemblyMemory.from_state_dict(payload["assemblies"])
        brain.homeostasis = HomeostaticController.from_state_dict(payload["homeostasis"])
        brain.plasticity = V05PlasticityController.from_state_dict(payload["plasticity"])
        brain.predictor = AssemblyPredictor.from_state_dict(payload["predictor"])
        brain.action_policy = AssemblyActionPolicy.from_state_dict(payload["action"])
        pending_activation = payload.get("pending_activation")
        if pending_activation is not None:
            activation_row = dict(pending_activation)
            activation_row["unit_ids"] = tuple(activation_row["unit_ids"])
            activation_row.setdefault("episode_count", int(activation_row.get("occurrences", 0)))
            brain.pending_activation = AssemblyActivation(**activation_row)
        pending_action = payload.get("pending_action")
        if pending_action is not None:
            brain.pending_action = ActionDecision(**pending_action)
        brain._episode_index = int(payload["episode_index"])
        brain.suppressed_unit_ids = set(payload["suppressed_unit_ids"])
        brain.trace = list(payload["trace"])
        return brain
