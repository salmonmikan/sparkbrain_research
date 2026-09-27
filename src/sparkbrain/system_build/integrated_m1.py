from __future__ import annotations

import hashlib
import json
import math
import os
import re
import shutil
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from sparkbrain.v03_seed import SensorySample

from .causal_scope_revision import (
    CandidateEvidence,
    CausalScopeRevisionPilot,
    ScopeRevisionCheckpointManager,
)
from .predictive_revision import PilotCheckpointManager, PredictiveRevisionPilot

BUILD_ID = "BUILD-SB-M1-001-INTEGRATED-CONTINUOUS-REVISION-PILOT"
SCHEMA_VERSION = 1
MAX_CYCLES = 64
CLAIM_BOUNDARY = (
    "NON_EVIDENTIARY_BUILD: bounded deterministic integration of established/reference "
    "predictive revision and repaired causal-scope revision. This build carries zero "
    "scientific credit and does not establish comparative support, composition contribution, "
    "real-task capability, biological equivalence, energy efficiency or scientific novelty."
)
COMPONENT_PROVENANCE = {
    "predictive_revision": {
        "build_id": "BUILD-SB-001-PREDICTIVE-STATE-REVISION-PILOT",
        "reuse": "integrated public component; explicit/reference memory",
        "scientific_credit": 0,
    },
    "causal_scope_revision": {
        "build_id": "BUILD-SB-002-CAUSAL-SCOPE-REVISION-PILOT",
        "reuse": "integrated public component after R161 integrity repair",
        "scientific_credit": 0,
    },
    "compositor_and_world": {
        "reuse": "fresh bounded engineering glue and deterministic local fixture",
        "scientific_credit": 0,
    },
}
_ID_PATTERN = re.compile(r"[A-Za-z0-9._:-]{1,128}")
_FORBIDDEN_INPUT_NAMES = {
    "answer",
    "entity",
    "entity_id",
    "episode",
    "evaluator",
    "future",
    "gold",
    "held_out",
    "heldout",
    "label",
    "oracle",
    "regime",
    "scope",
    "target",
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


def _strict_dict(value: object, expected: set[str], *, name: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != expected:
        raise ValueError(f"{name} has unexpected fields")
    return value


def _identifier(value: object, *, name: str) -> str:
    if not isinstance(value, str) or _ID_PATTERN.fullmatch(value) is None:
        raise ValueError(f"{name} must be a bounded ASCII identifier")
    return value


def _finite(value: object, *, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be finite")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _normalised_name(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower()).strip("_")


def _reject_privileged_names(values: dict[str, float]) -> None:
    for key in values:
        normalised = _normalised_name(key)
        padded = f"_{normalised}_"
        if any(f"_{name}_" in padded for name in _FORBIDDEN_INPUT_NAMES):
            raise ValueError(f"privileged runtime input name is forbidden: {key}")


@dataclass(frozen=True, slots=True)
class M1Observation:
    event_id: str
    time: float
    sensory_values: dict[str, float]
    routing_features: tuple[float, ...]

    def validate(self) -> None:
        _identifier(self.event_id, name="event_id")
        if _finite(self.time, name="time") < 0:
            raise ValueError("time must be non-negative")
        if not isinstance(self.sensory_values, dict) or not self.sensory_values:
            raise ValueError("sensory_values must be a non-empty object")
        _reject_privileged_names(self.sensory_values)
        for key, value in self.sensory_values.items():
            if not isinstance(key, str) or not key:
                raise ValueError("sensory value names must be non-empty strings")
            _finite(value, name=f"sensory_values[{key}]")
        if not isinstance(self.routing_features, tuple) or not self.routing_features:
            raise ValueError("routing_features must be a non-empty tuple")
        if len(self.routing_features) > 8:
            raise ValueError("routing_features exceeds the SB002 dimension ceiling")
        for value in self.routing_features:
            _finite(value, name="routing feature")

    def as_dict(self) -> dict[str, Any]:
        self.validate()
        return {
            "event_id": self.event_id,
            "routing_features": list(self.routing_features),
            "sensory_values": dict(sorted(self.sensory_values.items())),
            "time": self.time,
        }

    @classmethod
    def from_dict(cls, value: object) -> M1Observation:
        row = _strict_dict(
            value,
            {"event_id", "routing_features", "sensory_values", "time"},
            name="M1 observation",
        )
        features = row["routing_features"]
        if not isinstance(features, list):
            raise ValueError("routing_features must be a list in persisted state")
        result = cls(
            row["event_id"],
            row["time"],
            row["sensory_values"],
            tuple(features),
        )
        result.validate()
        return result


@dataclass(frozen=True, slots=True)
class M1Action:
    event_id: str
    decision: str
    reason: str
    prediction: float | None
    selected_state_id: str | None
    route_token: str | None
    route_candidate: str | None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: object) -> M1Action:
        row = _strict_dict(value, set(cls.__dataclass_fields__), name="M1 action")
        result = cls(**row)
        _identifier(result.event_id, name="event_id")
        if result.decision not in {"act_alpha", "act_beta", "abstain"}:
            raise ValueError("invalid persisted M1 action")
        return result


@dataclass(frozen=True, slots=True)
class M1OutcomeReceipt:
    receipt_id: str
    event_id: str
    outcome: float

    def validate(self) -> None:
        _identifier(self.receipt_id, name="receipt_id")
        _identifier(self.event_id, name="event_id")
        _finite(self.outcome, name="outcome")

    def as_dict(self) -> dict[str, Any]:
        self.validate()
        return asdict(self)

    @classmethod
    def from_dict(cls, value: object) -> M1OutcomeReceipt:
        row = _strict_dict(value, set(cls.__dataclass_fields__), name="M1 outcome receipt")
        result = cls(**row)
        result.validate()
        return result


@dataclass(frozen=True, slots=True)
class M1Revision:
    receipt_id: str
    event_id: str
    committed: bool
    reason: str
    predictive_revision: dict[str, Any] | None
    scope_revision: dict[str, Any] | None
    sequence: int

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: object) -> M1Revision:
        row = _strict_dict(value, set(cls.__dataclass_fields__), name="M1 revision")
        result = cls(**row)
        _identifier(result.receipt_id, name="receipt_id")
        _identifier(result.event_id, name="event_id")
        if (
            isinstance(result.sequence, bool)
            or not isinstance(result.sequence, int)
            or result.sequence < 0
        ):
            raise ValueError("invalid M1 revision sequence")
        return result


@dataclass(frozen=True, slots=True)
class ReceiptBinding:
    event_id: str
    outcome: float
    revision: M1Revision

    def as_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "outcome": self.outcome,
            "revision": self.revision.as_dict(),
        }


class IntegratedM1Pilot:
    """Bounded transaction joining SB001 prediction with repaired SB002 scope revision."""

    def __init__(
        self,
        *,
        predictive: PredictiveRevisionPilot | None = None,
        scoped: CausalScopeRevisionPilot | None = None,
    ) -> None:
        self.predictive = predictive or PredictiveRevisionPilot()
        self.scoped = scoped or CausalScopeRevisionPilot()
        self._pending_observation: M1Observation | None = None
        self._pending_action: M1Action | None = None
        self._event_bindings: dict[str, str] = {}
        self._receipt_bindings: dict[str, ReceiptBinding] = {}
        self._trace: list[dict[str, Any]] = []
        self._sequence = 0

    @staticmethod
    def _sensory_sample(observation: M1Observation) -> SensorySample:
        return SensorySample(
            sample_id=observation.event_id,
            time=observation.time,
            source_id="m1-local-fixture",
            modality="bounded-synthetic",
            values=observation.sensory_values,
        )

    def _own_payload(self) -> dict[str, Any]:
        return {
            "build_id": BUILD_ID,
            "event_bindings": dict(sorted(self._event_bindings.items())),
            "pending_action": (
                None if self._pending_action is None else self._pending_action.as_dict()
            ),
            "pending_observation": (
                None
                if self._pending_observation is None
                else self._pending_observation.as_dict()
            ),
            "predictive_state_hash": self.predictive.state_hash(),
            "receipt_bindings": {
                receipt_id: binding.as_dict()
                for receipt_id, binding in sorted(self._receipt_bindings.items())
            },
            "schema_version": SCHEMA_VERSION,
            "scope_state_hash": self.scoped.state_hash(),
            "sequence": self._sequence,
            "trace": json.loads(_canonical(self._trace)),
        }

    def _restore_own_payload(self, value: object) -> None:
        row = _strict_dict(
            value,
            {
                "build_id",
                "event_bindings",
                "pending_action",
                "pending_observation",
                "predictive_state_hash",
                "receipt_bindings",
                "schema_version",
                "scope_state_hash",
                "sequence",
                "trace",
            },
            name="M1 compositor state",
        )
        if row["build_id"] != BUILD_ID or row["schema_version"] != SCHEMA_VERSION:
            raise ValueError("unsupported M1 compositor state identity")
        if row["predictive_state_hash"] != self.predictive.state_hash():
            raise ValueError("M1 compositor predictive binding mismatch")
        if row["scope_state_hash"] != self.scoped.state_hash():
            raise ValueError("M1 compositor scope binding mismatch")
        pending_observation = row["pending_observation"]
        pending_action = row["pending_action"]
        if (pending_observation is None) != (pending_action is None):
            raise ValueError("pending observation and action must appear together")
        self._pending_observation = (
            None if pending_observation is None else M1Observation.from_dict(pending_observation)
        )
        self._pending_action = (
            None if pending_action is None else M1Action.from_dict(pending_action)
        )
        event_bindings = row["event_bindings"]
        if not isinstance(event_bindings, dict):
            raise ValueError("event_bindings must be an object")
        for event_id, digest in event_bindings.items():
            _identifier(event_id, name="event_id")
            if not isinstance(digest, str) or len(digest) != 64:
                raise ValueError("invalid event binding digest")
        self._event_bindings = dict(event_bindings)
        raw_receipts = row["receipt_bindings"]
        if not isinstance(raw_receipts, dict):
            raise ValueError("receipt_bindings must be an object")
        self._receipt_bindings = {}
        for receipt_id, raw_binding in raw_receipts.items():
            _identifier(receipt_id, name="receipt_id")
            binding = _strict_dict(
                raw_binding,
                {"event_id", "outcome", "revision"},
                name="receipt binding",
            )
            revision = M1Revision.from_dict(binding["revision"])
            resolved = ReceiptBinding(
                _identifier(binding["event_id"], name="event_id"),
                _finite(binding["outcome"], name="outcome"),
                revision,
            )
            if revision.receipt_id != receipt_id or revision.event_id != resolved.event_id:
                raise ValueError("receipt binding identity mismatch")
            self._receipt_bindings[receipt_id] = resolved
        sequence = row["sequence"]
        if isinstance(sequence, bool) or not isinstance(sequence, int) or sequence < 0:
            raise ValueError("M1 sequence must be a non-negative integer")
        if sequence != len(self._receipt_bindings):
            raise ValueError("M1 sequence does not match committed receipts")
        if not isinstance(row["trace"], list) or len(row["trace"]) != sequence:
            raise ValueError("M1 trace does not match committed sequence")
        self._sequence = sequence
        self._trace = json.loads(_canonical(row["trace"]))

    def _restore_components(
        self,
        *,
        predictive_root: Path,
        scope_payload: dict[str, Any],
        own_payload: dict[str, Any],
    ) -> None:
        self.predictive = PilotCheckpointManager.load(predictive_root)
        self.scoped._restore_payload(scope_payload)
        self._restore_own_payload(own_payload)

    def observe(self, observation: M1Observation) -> M1Action:
        observation.validate()
        if self._pending_observation is not None:
            raise RuntimeError(
                "later outcome must resolve the pending event before another observe"
            )
        digest = _digest(observation.as_dict())
        if observation.event_id in self._event_bindings:
            raise ValueError("event_id has already been used")

        with TemporaryDirectory() as tmp:
            predictive_root = Path(tmp) / "predictive"
            PilotCheckpointManager.save(self.predictive, predictive_root)
            scope_before = self.scoped._checkpoint_payload()
            own_before = self._own_payload()
            try:
                prediction = self.predictive.observe(self._sensory_sample(observation))
                route = self.scoped.query(observation.routing_features)
                route_candidate = (
                    None if route.revision is None else route.revision.selected_candidate
                )
                predicted_candidate = (
                    None
                    if prediction.prediction is None
                    else "alpha"
                    if prediction.prediction >= 0
                    else "beta"
                )
                if prediction.decision != "act":
                    decision = "abstain"
                    reason = f"predictive_{prediction.reason}"
                elif route.routing.abstained or route_candidate is None:
                    decision = "abstain"
                    reason = f"scope_{route.routing.reason}"
                elif predicted_candidate != route_candidate:
                    decision = "abstain"
                    reason = "predictive_scope_disagreement"
                else:
                    decision = f"act_{predicted_candidate}"
                    reason = "predictive_scope_agreement"
                action = M1Action(
                    observation.event_id,
                    decision,
                    reason,
                    prediction.prediction,
                    prediction.selected_state_id,
                    route.routing.token,
                    route_candidate,
                )
                self._pending_observation = observation
                self._pending_action = action
                self._event_bindings[observation.event_id] = digest
                return action
            except Exception:
                self._restore_components(
                    predictive_root=predictive_root,
                    scope_payload=scope_before,
                    own_payload=own_before,
                )
                raise

    def apply_outcome(
        self,
        receipt: M1OutcomeReceipt,
        *,
        _fault_at: str | None = None,
    ) -> M1Revision:
        receipt.validate()
        prior = self._receipt_bindings.get(receipt.receipt_id)
        if prior is not None:
            if prior.event_id == receipt.event_id and prior.outcome == float(receipt.outcome):
                return prior.revision
            raise ValueError("receipt identity conflict")
        if self._pending_observation is None or self._pending_action is None:
            raise RuntimeError("outcome requires a pending observation")
        if receipt.event_id != self._pending_observation.event_id:
            raise ValueError("outcome event_id does not match the pending observation")

        with TemporaryDirectory() as tmp:
            predictive_root = Path(tmp) / "predictive"
            PilotCheckpointManager.save(self.predictive, predictive_root)
            scope_before = self.scoped._checkpoint_payload()
            own_before = self._own_payload()
            try:
                if _fault_at == "before_predictive_revision":
                    raise RuntimeError("injected before predictive revision")
                predictive_revision = self.predictive.feedback(receipt.outcome)
                if _fault_at == "after_predictive_revision":
                    raise RuntimeError("injected after predictive revision")
                candidate = "alpha" if receipt.outcome >= 0 else "beta"
                strength = min(1.0, abs(float(receipt.outcome)))
                if _fault_at == "before_scope_revision":
                    raise RuntimeError("injected before scope revision")
                scope_revision = self.scoped.step(
                    self._pending_observation.routing_features,
                    CandidateEvidence(candidate, receipt.receipt_id, strength),
                )
                if not scope_revision.committed:
                    raise RuntimeError(f"scope revision rejected: {scope_revision.reason}")
                if _fault_at == "after_scope_revision":
                    raise RuntimeError("injected after scope revision")
                next_sequence = self._sequence + 1
                revision = M1Revision(
                    receipt.receipt_id,
                    receipt.event_id,
                    True,
                    "committed_integrated_revision",
                    asdict(predictive_revision),
                    asdict(scope_revision),
                    next_sequence,
                )
                self._sequence = next_sequence
                self._receipt_bindings[receipt.receipt_id] = ReceiptBinding(
                    receipt.event_id,
                    float(receipt.outcome),
                    revision,
                )
                self._trace.append(
                    {
                        "action": self._pending_action.as_dict(),
                        "observation": self._pending_observation.as_dict(),
                        "receipt": receipt.as_dict(),
                        "revision": revision.as_dict(),
                        "sequence": next_sequence,
                    }
                )
                self._pending_observation = None
                self._pending_action = None
                return revision
            except Exception:
                self._restore_components(
                    predictive_root=predictive_root,
                    scope_payload=scope_before,
                    own_payload=own_before,
                )
                raise

    def inspect(self) -> dict[str, Any]:
        return json.loads(
            _canonical(
                {
                    "build_id": BUILD_ID,
                    "claim_boundary": CLAIM_BOUNDARY,
                    "component_provenance": COMPONENT_PROVENANCE,
                    "event_bindings": dict(sorted(self._event_bindings.items())),
                    "evidentiary_status": "NON_EVIDENTIARY_BUILD",
                    "pending_action": (
                        None if self._pending_action is None else self._pending_action.as_dict()
                    ),
                    "pending_observation": (
                        None
                        if self._pending_observation is None
                        else self._pending_observation.as_dict()
                    ),
                    "predictive": self.predictive.inspect(),
                    "receipt_bindings": {
                        receipt_id: binding.as_dict()
                        for receipt_id, binding in sorted(self._receipt_bindings.items())
                    },
                    "scientific_credit": 0,
                    "scope_revision": self.scoped.inspect(),
                    "sequence": self._sequence,
                    "trace": self._trace,
                }
            )
        )

    def state_hash(self) -> str:
        return _digest(self.inspect())


class DeterministicM1World:
    """Bounded action-coupled local fixture; hidden state never enters runtime input."""

    _ROUTE_PATTERN = (0, 0, 1, 1, 0, 1, 0, 1)

    def __init__(self) -> None:
        self._index = 0
        self._actions: list[str] = []

    def next_observation(self) -> M1Observation:
        if self._index >= MAX_CYCLES:
            raise RuntimeError("M1 world exceeded its 64-cycle ceiling")
        route = self._ROUTE_PATTERN[self._index % len(self._ROUTE_PATTERN)]
        signal = 0.0 if route == 0 else 0.45
        return M1Observation(
            event_id=f"event-{self._index + 1:04d}",
            time=float(self._index),
            sensory_values={"signal": signal},
            routing_features=(signal,),
        )

    def resolve(self, action: M1Action) -> M1OutcomeReceipt:
        expected = self.next_observation()
        if action.event_id != expected.event_id:
            raise ValueError("action does not match the current world event")
        base = 0.8 if expected.routing_features[0] < 0.225 else -0.8
        action_effect = {"act_alpha": 0.1, "act_beta": -0.1, "abstain": 0.0}[action.decision]
        outcome = base + action_effect
        self._actions.append(action.decision)
        self._index += 1
        return M1OutcomeReceipt(f"receipt-{action.event_id}", action.event_id, outcome)

    def state_dict(self) -> dict[str, Any]:
        return {"actions": list(self._actions), "index": self._index}

    @classmethod
    def from_state_dict(cls, value: object) -> DeterministicM1World:
        row = _strict_dict(value, {"actions", "index"}, name="M1 world state")
        index = row["index"]
        actions = row["actions"]
        if (
            isinstance(index, bool)
            or not isinstance(index, int)
            or not 0 <= index <= MAX_CYCLES
            or not isinstance(actions, list)
            or len(actions) != index
            or any(action not in {"act_alpha", "act_beta", "abstain"} for action in actions)
        ):
            raise ValueError("invalid M1 world state")
        world = cls()
        world._index = index
        world._actions = list(actions)
        return world


@dataclass(frozen=True, slots=True)
class M1Cycle:
    observation: M1Observation
    action: M1Action
    receipt: M1OutcomeReceipt
    revision: M1Revision

    def as_dict(self) -> dict[str, Any]:
        return {
            "action": self.action.as_dict(),
            "observation": self.observation.as_dict(),
            "receipt": self.receipt.as_dict(),
            "revision": self.revision.as_dict(),
        }


class IntegratedM1Session:
    def __init__(
        self,
        *,
        pilot: IntegratedM1Pilot | None = None,
        world: DeterministicM1World | None = None,
    ) -> None:
        self.pilot = pilot or IntegratedM1Pilot()
        self.world = world or DeterministicM1World()

    def cycle(self, *, _fault_at: str | None = None) -> M1Cycle:
        with TemporaryDirectory() as tmp:
            checkpoint = Path(tmp) / "session"
            IntegratedM1CheckpointManager.save(self, checkpoint)
            try:
                observation = self.world.next_observation()
                if _fault_at == "before_action":
                    raise RuntimeError("injected before action")
                action = self.pilot.observe(observation)
                if _fault_at == "after_action":
                    raise RuntimeError("injected after action")
                receipt = self.world.resolve(action)
                if _fault_at == "after_outcome":
                    raise RuntimeError("injected after outcome")
                revision = self.pilot.apply_outcome(receipt, _fault_at=_fault_at)
                return M1Cycle(observation, action, receipt, revision)
            except Exception:
                restored = IntegratedM1CheckpointManager.load(checkpoint)
                self.pilot = restored.pilot
                self.world = restored.world
                raise

    def inspect(self) -> dict[str, Any]:
        return {
            "build_id": BUILD_ID,
            "pilot": self.pilot.inspect(),
            "world": self.world.state_dict(),
        }

    def state_hash(self) -> str:
        return _digest(self.inspect())


class IntegratedM1CheckpointManager:
    MANIFEST = "manifest.json"
    PILOT = "pilot-state.json"
    WORLD = "world-state.json"

    @staticmethod
    def _write_canonical(path: Path, value: object) -> None:
        path.write_text(_canonical(value) + "\n", encoding="utf-8")

    @staticmethod
    def _read_canonical(path: Path) -> object:
        raw = path.read_bytes()
        value = json.loads(raw)
        if raw != (_canonical(value) + "\n").encode("utf-8"):
            raise ValueError(f"checkpoint file is not strict canonical JSON: {path.name}")
        return value

    @staticmethod
    def save(session: IntegratedM1Session, directory: str | Path) -> str:
        target = Path(directory)
        if target.exists():
            raise FileExistsError("M1 checkpoint is no-clobber")
        target.parent.mkdir(parents=True, exist_ok=True)
        staging_parent = Path(tempfile.mkdtemp(prefix=".m1-checkpoint-", dir=target.parent))
        staging = staging_parent / "payload"
        try:
            staging.mkdir()
            PilotCheckpointManager.save(session.pilot.predictive, staging / "predictive")
            ScopeRevisionCheckpointManager.save(session.pilot.scoped, staging / "scope")
            IntegratedM1CheckpointManager._write_canonical(
                staging / IntegratedM1CheckpointManager.PILOT,
                session.pilot._own_payload(),
            )
            IntegratedM1CheckpointManager._write_canonical(
                staging / IntegratedM1CheckpointManager.WORLD,
                session.world.state_dict(),
            )
            files = {}
            for path in sorted(staging.rglob("*")):
                if path.is_file():
                    files[str(path.relative_to(staging))] = hashlib.sha256(
                        path.read_bytes()
                    ).hexdigest()
            manifest = {
                "build_id": BUILD_ID,
                "files": files,
                "schema_version": SCHEMA_VERSION,
                "state_hash": session.state_hash(),
            }
            IntegratedM1CheckpointManager._write_canonical(
                staging / IntegratedM1CheckpointManager.MANIFEST,
                manifest,
            )
            manifest_digest = hashlib.sha256(
                (staging / IntegratedM1CheckpointManager.MANIFEST).read_bytes()
            ).hexdigest()
            os.replace(staging, target)
            return manifest_digest
        finally:
            shutil.rmtree(staging_parent, ignore_errors=True)

    @staticmethod
    def load(directory: str | Path) -> IntegratedM1Session:
        root = Path(directory)
        manifest = _strict_dict(
            IntegratedM1CheckpointManager._read_canonical(
                root / IntegratedM1CheckpointManager.MANIFEST
            ),
            {"build_id", "files", "schema_version", "state_hash"},
            name="M1 checkpoint manifest",
        )
        if manifest["build_id"] != BUILD_ID or manifest["schema_version"] != SCHEMA_VERSION:
            raise ValueError("unsupported M1 checkpoint identity")
        files = manifest["files"]
        if not isinstance(files, dict):
            raise ValueError("M1 checkpoint file manifest must be an object")
        observed = {
            str(path.relative_to(root))
            for path in root.rglob("*")
            if path.is_file() and path.name != IntegratedM1CheckpointManager.MANIFEST
        }
        if observed != set(files):
            raise ValueError("M1 checkpoint file set mismatch")
        for relative, digest in files.items():
            if hashlib.sha256((root / relative).read_bytes()).hexdigest() != digest:
                raise ValueError(f"M1 checkpoint digest mismatch: {relative}")
        predictive = PilotCheckpointManager.load(root / "predictive")
        scoped = ScopeRevisionCheckpointManager.load(root / "scope")
        pilot = IntegratedM1Pilot(predictive=predictive, scoped=scoped)
        pilot._restore_own_payload(
            IntegratedM1CheckpointManager._read_canonical(
                root / IntegratedM1CheckpointManager.PILOT
            )
        )
        world = DeterministicM1World.from_state_dict(
            IntegratedM1CheckpointManager._read_canonical(
                root / IntegratedM1CheckpointManager.WORLD
            )
        )
        session = IntegratedM1Session(pilot=pilot, world=world)
        if session.state_hash() != manifest["state_hash"]:
            raise ValueError("restored M1 state hash mismatch")
        return session


__all__ = [
    "BUILD_ID",
    "CLAIM_BOUNDARY",
    "COMPONENT_PROVENANCE",
    "DeterministicM1World",
    "IntegratedM1CheckpointManager",
    "IntegratedM1Pilot",
    "IntegratedM1Session",
    "M1Action",
    "M1Cycle",
    "M1Observation",
    "M1OutcomeReceipt",
    "M1Revision",
    "MAX_CYCLES",
]
