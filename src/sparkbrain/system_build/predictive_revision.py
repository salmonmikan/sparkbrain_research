from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from sparkbrain.v03_seed import SensorySample
from sparkbrain.v032 import DirectCheckpointManager, IntegratedV032Brain

BUILD_ID = "BUILD-SB-001-PREDICTIVE-STATE-REVISION-PILOT"
SCHEMA_VERSION = 1
CLAIM_BOUNDARY = (
    "NON_EVIDENTIARY_BUILD: this pilot integrates established/reference mechanisms for "
    "engineering use. Build behavior carries zero confirmatory scientific credit and does not "
    "establish mechanism novelty, autonomous entity discovery, or emergent field memory."
)
FORGE_DESIGN_SOURCE = {
    "branch": "forge/20260925-predictive-state-revision-loop-a",
    "head": "02fd9d24337432ac7121599f3361392d87e2fc5e",
    "reuse": "design input only; MAIN implementation is fresh and independently verified",
    "scientific_credit": 0,
}
_FORBIDDEN_CONTEXT_NAMES = {
    "answer",
    "episode",
    "episode_id",
    "entity",
    "entity_id",
    "entity_key",
    "entity_slot",
    "evaluator",
    "gold",
    "label",
    "state",
    "state_id",
    "target",
    "test_only",
    "truth",
}


def _canonical(value: object) -> str:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _digest(value: object) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _finite(value: object, *, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite number")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be a finite number")
    return result


def _normalised_name(value: object) -> str:
    raw = str(value).strip()
    raw = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", raw)
    return re.sub(r"[^a-zA-Z0-9]+", "_", raw).strip("_").lower()


def _contains_privileged_name(value: object) -> bool:
    normalised = _normalised_name(value)
    padded = f"_{normalised}_"
    return any(f"_{name}_" in padded for name in _FORBIDDEN_CONTEXT_NAMES)


def _reject_privileged_names(value: object, *, path: str) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if _contains_privileged_name(key):
                raise ValueError(f"privileged build input is forbidden at {path}.{key}")
            _reject_privileged_names(child, path=f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            _reject_privileged_names(child, path=f"{path}[{index}]")


@dataclass(frozen=True, slots=True)
class PilotConfig:
    context_gate: float = 0.35
    reuse_error: float = 0.35
    ambiguity_prediction_gap: float = 0.50
    ambiguity_distance_margin: float = 0.05
    max_hypotheses: int = 16
    max_context_scalars: int = 64

    def validate(self) -> None:
        for name in (
            "context_gate",
            "reuse_error",
            "ambiguity_prediction_gap",
            "ambiguity_distance_margin",
        ):
            if _finite(getattr(self, name), name=name) < 0:
                raise ValueError(f"{name} must be non-negative")
        for name, ceiling in (("max_hypotheses", 16), ("max_context_scalars", 64)):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= ceiling:
                raise ValueError(f"{name} must be an integer in [1, {ceiling}]")

    def as_dict(self) -> dict[str, Any]:
        self.validate()
        return asdict(self)

    @classmethod
    def from_dict(cls, value: object) -> PilotConfig:
        expected = set(cls.__dataclass_fields__)
        if not isinstance(value, dict) or set(value) != expected:
            raise ValueError("pilot config has unexpected fields")
        result = cls(**value)
        result.validate()
        return result


@dataclass(slots=True)
class PredictiveHypothesis:
    state_id: str
    channels: tuple[str, ...]
    context_mean: tuple[float, ...]
    outcome_mean: float
    count: int
    last_used_step: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "channels": list(self.channels),
            "context_mean": list(self.context_mean),
            "count": self.count,
            "last_used_step": self.last_used_step,
            "outcome_mean": self.outcome_mean,
            "state_id": self.state_id,
        }


@dataclass(frozen=True, slots=True)
class CandidateView:
    state_id: str
    context_distance: float
    prediction: float
    count: int


@dataclass(frozen=True, slots=True)
class PilotPrediction:
    decision: str
    reason: str
    prediction: float | None
    selected_state_id: str | None
    candidates: tuple[CandidateView, ...]
    reference_action: str | None
    reference_state_hash: str


@dataclass(frozen=True, slots=True)
class PilotRevision:
    action: str
    state_id: str
    context_distance: float
    prediction_error_before: float
    state_count: int
    targeted_update_only: bool


class PredictiveRevisionPilot:
    """Bounded non-evidentiary integration loop for BUILD-SB-001.

    The predictive-state bank is explicit/reference memory implemented with an
    established prototype/latent-state pattern. It is not emergent field memory.
    The wrapped v0.3/v0.3.2 runtime remains a direct SparkBrain engineering
    component and is checkpointed through DirectCheckpointManager.
    """

    def __init__(
        self,
        config: PilotConfig | None = None,
        *,
        reference_brain: IntegratedV032Brain | None = None,
    ) -> None:
        self.config = config or PilotConfig()
        self.config.validate()
        if reference_brain is not None and type(reference_brain) is not IntegratedV032Brain:
            raise TypeError("reference_brain must be an exact IntegratedV032Brain")
        self.reference_brain = reference_brain or IntegratedV032Brain()
        self._states: list[PredictiveHypothesis] = []
        self._active_state_id: str | None = None
        self._context_channels: tuple[str, ...] | None = None
        self._pending_context: tuple[float, ...] | None = None
        self._pending_sample_id: str | None = None
        self._revision_step = 0

    @staticmethod
    def _distance(left: tuple[float, ...], right: tuple[float, ...]) -> float:
        if len(left) != len(right):
            raise ValueError("context dimensions must match")
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(left, right, strict=True)))

    def _sample_context(
        self,
        sample: SensorySample,
    ) -> tuple[tuple[str, ...], tuple[float, ...]]:
        sample.validate()
        if sample.entity_hint is not None:
            raise ValueError("entity_hint is forbidden in BUILD-SB-001 observation input")
        _reject_privileged_names(dict(sample.metadata), path="metadata")
        channels = tuple(sorted(sample.values))
        if not channels:
            raise ValueError("BUILD-SB-001 requires at least one observed scalar")
        if len(channels) > self.config.max_context_scalars:
            raise ValueError("observation exceeds max_context_scalars")
        for channel in channels:
            if _contains_privileged_name(channel):
                raise ValueError(f"privileged observation channel is forbidden: {channel}")
        context = tuple(
            _finite(sample.values[channel], name=f"values[{channel}]")
            for channel in channels
        )
        if self._context_channels is not None and channels != self._context_channels:
            raise ValueError("observation channels must match the established context schema")
        return channels, context

    def _candidate_views(self, context: tuple[float, ...]) -> tuple[CandidateView, ...]:
        rows = []
        for state in self._states:
            distance = self._distance(state.context_mean, context)
            if distance <= self.config.context_gate:
                rows.append(
                    CandidateView(
                        state_id=state.state_id,
                        context_distance=distance,
                        prediction=state.outcome_mean,
                        count=state.count,
                    )
                )
        return tuple(sorted(rows, key=lambda row: (row.context_distance, row.state_id)))

    def observe(self, sample: SensorySample) -> PilotPrediction:
        """Process one external observation and choose act vs explicit abstention."""

        if self._pending_context is not None:
            raise RuntimeError("feedback must resolve the pending observation before another observe")
        channels, context = self._sample_context(sample)
        reference_result = self.reference_brain.step(sample)
        if self._context_channels is None:
            self._context_channels = channels
        self._pending_context = context
        self._pending_sample_id = sample.sample_id
        candidates = self._candidate_views(context)
        reference_action = reference_result.base_result.action
        reference_state_hash = self.reference_brain.state_hash()
        if not candidates:
            return PilotPrediction(
                "abstain",
                "no_compatible_hypothesis",
                None,
                None,
                candidates,
                reference_action,
                reference_state_hash,
            )
        selected = candidates[0]
        if any(
            abs(selected.prediction - competitor.prediction)
            >= self.config.ambiguity_prediction_gap
            and abs(selected.context_distance - competitor.context_distance)
            <= self.config.ambiguity_distance_margin
            for competitor in candidates[1:]
        ):
            return PilotPrediction(
                "abstain",
                "competing_hypotheses_ambiguous",
                None,
                None,
                candidates,
                reference_action,
                reference_state_hash,
            )
        return PilotPrediction(
            "act",
            "nearest_compatible_hypothesis",
            selected.prediction,
            selected.state_id,
            candidates,
            reference_action,
            reference_state_hash,
        )

    def _create_state(
        self,
        context: tuple[float, ...],
        outcome: float,
        *,
        revision_step: int,
    ) -> PredictiveHypothesis:
        if len(self._states) >= self.config.max_hypotheses:
            raise RuntimeError("max_hypotheses reached; BUILD-SB-001 does not evict silently")
        if self._context_channels is None:
            raise RuntimeError("context schema must exist before state creation")
        state = PredictiveHypothesis(
            state_id=f"state-{len(self._states) + 1:03d}",
            channels=self._context_channels,
            context_mean=context,
            outcome_mean=outcome,
            count=1,
            last_used_step=revision_step,
        )
        self._states.append(state)
        return state

    @staticmethod
    def _running_mean(current: float, observed: float, count: int) -> float:
        new_count = count + 1
        observed_weight = 1.0 / new_count
        result = math.fsum(
            (
                current * (1.0 - observed_weight),
                observed * observed_weight,
            )
        )
        return _finite(result, name="running_mean")

    @staticmethod
    def _update_state(
        state: PredictiveHypothesis,
        context: tuple[float, ...],
        outcome: float,
        *,
        revision_step: int,
    ) -> None:
        new_count = state.count + 1
        context_mean = tuple(
            PredictiveRevisionPilot._running_mean(
                state.context_mean[index],
                context[index],
                state.count,
            )
            for index in range(len(context))
        )
        outcome_mean = PredictiveRevisionPilot._running_mean(
            state.outcome_mean,
            outcome,
            state.count,
        )
        state.context_mean = context_mean
        state.outcome_mean = outcome_mean
        state.count = new_count
        state.last_used_step = revision_step

    def feedback(self, outcome: float) -> PilotRevision:
        """Apply later evidence to exactly one compatible predictive hypothesis."""

        if self._pending_context is None:
            raise RuntimeError("feedback requires a pending observation")
        resolved_outcome = _finite(outcome, name="outcome")
        context = self._pending_context
        next_revision_step = self._revision_step + 1
        before = {state.state_id: state.as_dict() for state in self._states}
        compatible: list[tuple[float, float, PredictiveHypothesis]] = []
        for state in self._states:
            distance = self._distance(state.context_mean, context)
            if distance <= self.config.context_gate:
                compatible.append((abs(resolved_outcome - state.outcome_mean), distance, state))

        if not compatible:
            state = self._create_state(
                context,
                resolved_outcome,
                revision_step=next_revision_step,
            )
            action = "create"
            error = 0.0
            distance = 0.0
        else:
            error, distance, state = min(
                compatible,
                key=lambda row: (row[0], row[1], row[2].state_id),
            )
            if error <= self.config.reuse_error:
                action = (
                    "reuse"
                    if self._active_state_id is not None
                    and self._active_state_id != state.state_id
                    else "update"
                )
                self._update_state(
                    state,
                    context,
                    resolved_outcome,
                    revision_step=next_revision_step,
                )
            else:
                state = self._create_state(
                    context,
                    resolved_outcome,
                    revision_step=next_revision_step,
                )
                action = "split"
                distance = 0.0

        self._revision_step = next_revision_step
        self._active_state_id = state.state_id
        self._pending_context = None
        self._pending_sample_id = None
        changed_existing = {
            item.state_id
            for item in self._states
            if item.state_id in before and item.as_dict() != before[item.state_id]
        }
        if not changed_existing <= {state.state_id}:
            raise RuntimeError("selective revision invariant violated")
        return PilotRevision(
            action=action,
            state_id=state.state_id,
            context_distance=distance,
            prediction_error_before=error,
            state_count=len(self._states),
            targeted_update_only=True,
        )

    def inspect(self) -> dict[str, Any]:
        """Return a pure JSON-safe snapshot without advancing either component."""

        return json.loads(
            _canonical(
                {
                    "active_state_id": self._active_state_id,
                    "build_id": BUILD_ID,
                    "claim_boundary": CLAIM_BOUNDARY,
                    "component_provenance": {
                        "c15_revision_persistent_belief": (
                            "direct design lineage through the integrated v0.3 runtime; original "
                            "hand-set/reference limitations preserved"
                        ),
                        "forge_predictive_state": FORGE_DESIGN_SOURCE,
                        "integrated_v03": (
                            "direct engineering reference via IntegratedV032Brain"
                        ),
                        "integrated_v032": "direct diagnostic facade",
                        "predictive_bank": (
                            "explicit/reference memory; ordinary latent-state mechanism"
                        ),
                    },
                    "config": self.config.as_dict(),
                    "context_channels": (
                        list(self._context_channels)
                        if self._context_channels is not None
                        else None
                    ),
                    "evidentiary_status": "NON_EVIDENTIARY_BUILD",
                    "hypotheses": [state.as_dict() for state in self._states],
                    "pending_context": (
                        list(self._pending_context)
                        if self._pending_context is not None
                        else None
                    ),
                    "pending_sample_id": self._pending_sample_id,
                    "reference_brain": self.reference_brain.inspect(),
                    "revision_step": self._revision_step,
                    "scientific_credit": 0,
                }
            )
        )

    def state_hash(self) -> str:
        return _digest(self.inspect())

    def _checkpoint_payload(self) -> dict[str, Any]:
        return {
            "active_state_id": self._active_state_id,
            "build_id": BUILD_ID,
            "config": self.config.as_dict(),
            "context_channels": (
                list(self._context_channels) if self._context_channels is not None else None
            ),
            "hypotheses": [state.as_dict() for state in self._states],
            "pending_context": (
                list(self._pending_context) if self._pending_context is not None else None
            ),
            "pending_sample_id": self._pending_sample_id,
            "reference_brain_state_hash": self.reference_brain.state_hash(),
            "revision_step": self._revision_step,
            "schema_version": SCHEMA_VERSION,
        }

    @classmethod
    def _from_checkpoint_payload(
        cls,
        payload: object,
        *,
        reference_brain: IntegratedV032Brain,
    ) -> PredictiveRevisionPilot:
        expected = {
            "active_state_id",
            "build_id",
            "config",
            "context_channels",
            "hypotheses",
            "pending_context",
            "pending_sample_id",
            "reference_brain_state_hash",
            "revision_step",
            "schema_version",
        }
        if not isinstance(payload, dict) or set(payload) != expected:
            raise ValueError("pilot checkpoint has unexpected fields")
        if payload["schema_version"] != SCHEMA_VERSION or payload["build_id"] != BUILD_ID:
            raise ValueError("unsupported pilot checkpoint schema or build id")
        if reference_brain.state_hash() != payload["reference_brain_state_hash"]:
            raise ValueError("reference brain checkpoint binding mismatch")
        pilot = cls(PilotConfig.from_dict(payload["config"]), reference_brain=reference_brain)
        channels = payload["context_channels"]
        if channels is not None:
            if not isinstance(channels, list) or any(not isinstance(row, str) for row in channels):
                raise ValueError("invalid context_channels in checkpoint")
            pilot._context_channels = tuple(channels)
        rows = payload["hypotheses"]
        if not isinstance(rows, list):
            raise ValueError("hypotheses must be a list")
        expected_hypothesis = {
            "channels",
            "context_mean",
            "count",
            "last_used_step",
            "outcome_mean",
            "state_id",
        }
        for row in rows:
            if not isinstance(row, dict) or set(row) != expected_hypothesis:
                raise ValueError("invalid hypothesis checkpoint row")
            state = PredictiveHypothesis(
                state_id=str(row["state_id"]),
                channels=tuple(row["channels"]),
                context_mean=tuple(
                    _finite(value, name="context_mean") for value in row["context_mean"]
                ),
                outcome_mean=_finite(row["outcome_mean"], name="outcome_mean"),
                count=int(row["count"]),
                last_used_step=int(row["last_used_step"]),
            )
            if state.count < 1 or state.last_used_step < 0:
                raise ValueError("invalid hypothesis counters")
            if pilot._context_channels is not None and state.channels != pilot._context_channels:
                raise ValueError("hypothesis channels do not match checkpoint context schema")
            pilot._states.append(state)
        if len(pilot._states) > pilot.config.max_hypotheses:
            raise ValueError("checkpoint exceeds max_hypotheses")
        state_ids = [state.state_id for state in pilot._states]
        if len(state_ids) != len(set(state_ids)):
            raise ValueError("checkpoint hypothesis ids must be unique")
        active = payload["active_state_id"]
        if active is not None and active not in set(state_ids):
            raise ValueError("active state is absent from checkpoint hypotheses")
        pilot._active_state_id = active
        pending = payload["pending_context"]
        if pending is not None:
            pilot._pending_context = tuple(
                _finite(value, name="pending_context") for value in pending
            )
            if pilot._context_channels is None or len(pilot._pending_context) != len(
                pilot._context_channels
            ):
                raise ValueError("pending context shape mismatch")
        pending_sample_id = payload["pending_sample_id"]
        if (pending is None) != (pending_sample_id is None):
            raise ValueError("pending context and sample id must appear together")
        if pending_sample_id is not None and not isinstance(pending_sample_id, str):
            raise ValueError("pending_sample_id must be a string")
        pilot._pending_sample_id = pending_sample_id
        revision_step = payload["revision_step"]
        if (
            isinstance(revision_step, bool)
            or not isinstance(revision_step, int)
            or revision_step < 0
        ):
            raise ValueError("revision_step must be a non-negative integer")
        pilot._revision_step = revision_step
        return pilot


class PilotCheckpointManager:
    """Checkpoint the direct v0.3.2 runtime plus explicit/reference build memory."""

    BRAIN_FILE = "reference-brain.json"
    PILOT_FILE = "pilot-state.json"

    @staticmethod
    def save(pilot: PredictiveRevisionPilot, directory: str | Path) -> dict[str, str]:
        root = Path(directory)
        root.mkdir(parents=True, exist_ok=True)
        brain_path = root / PilotCheckpointManager.BRAIN_FILE
        pilot_path = root / PilotCheckpointManager.PILOT_FILE
        if brain_path.exists() or pilot_path.exists():
            raise FileExistsError("pilot checkpoint is no-clobber")
        payload = pilot._checkpoint_payload()
        pilot_raw = (_canonical(payload) + "\n").encode("utf-8")
        brain_digest = DirectCheckpointManager.save(pilot.reference_brain, brain_path)
        with pilot_path.open("xb") as handle:
            handle.write(pilot_raw)
        return {
            "brain_digest": brain_digest,
            "pilot_digest": hashlib.sha256(pilot_raw).hexdigest(),
        }

    @staticmethod
    def load(directory: str | Path) -> PredictiveRevisionPilot:
        root = Path(directory)
        brain_path = root / PilotCheckpointManager.BRAIN_FILE
        pilot_path = root / PilotCheckpointManager.PILOT_FILE
        raw = pilot_path.read_bytes()
        try:
            payload = json.loads(raw)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("pilot checkpoint must be valid UTF-8 JSON") from exc
        if raw != (_canonical(payload) + "\n").encode("utf-8"):
            raise ValueError("pilot checkpoint must use strict canonical JSON")
        reference_brain = DirectCheckpointManager.load(brain_path)
        if type(reference_brain) is not IntegratedV032Brain:
            raise TypeError("pilot checkpoint requires an IntegratedV032Brain facade")
        return PredictiveRevisionPilot._from_checkpoint_payload(
            payload,
            reference_brain=reference_brain,
        )
