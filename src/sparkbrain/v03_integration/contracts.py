from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

TRACE_SCHEMA_VERSION = "0.3"
EVENTS = frozenset(
    {
        "sensory_accepted",
        "sensory_suppressed",
        "evidence_added",
        "evidence_removed",
        "coalition_evaluated",
        "no_ignition",
        "workspace_broadcast",
        "intervention",
    }
)
STATE_KEYS = {
    "evidence",
    "beliefs",
    "concept_candidates",
    "suppressed_modules",
    "goal",
    "intervention",
}


def canonical_json(value: object) -> str:
    return json.dumps(
        value, allow_nan=False, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )


def _hash(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _copy(value: object) -> Any:
    return json.loads(canonical_json(value))


def validate_schema_document(kind: str, document: Mapping[str, Any]) -> None:
    filenames = {
        "checkpoint": "checkpoint-v0.3.schema.json",
        "trace": "trace-v0.3.schema.json",
    }
    filename = filenames[kind]
    root = Path(__file__).parents[3]
    schema = json.loads((root / "schemas" / filename).read_text(encoding="utf-8"))
    trace = json.loads((root / "schemas" / filenames["trace"]).read_text(encoding="utf-8"))
    registry = Registry().with_resource("trace-v0.3.schema.json", Resource.from_contents(trace))
    errors = list(Draft202012Validator(schema, registry=registry).iter_errors(document))
    if errors:
        raise ValueError(f"Draft202012 schema validation failed: {errors[0].message}")


def _state(value: object) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != STATE_KEYS:
        raise ValueError("state has unexpected fields")
    if not isinstance(value["goal"], (str, type(None))) or not isinstance(
        value["suppressed_modules"], list
    ):
        raise ValueError("state has invalid nested type")
    if any(not isinstance(item, str) for item in value["suppressed_modules"]):
        raise ValueError("suppressed modules have invalid items")
    if value["intervention"] is not None:
        intervention = value["intervention"]
        if (
            not isinstance(intervention, dict)
            or set(intervention) != {"evidence_id", "kind"}
            or not all(isinstance(intervention[key], str) for key in intervention)
        ):
            raise ValueError("intervention has invalid fields")
    exact_values = (
        ("evidence", {"active", "entity", "polarity", "source_id"}),
        ("beliefs", {"residual_losers", "winner"}),
        ("concept_candidates", {"activation", "label"}),
    )
    for name, fields in exact_values:
        values = value[name]
        if not isinstance(values, dict):
            raise ValueError("state has invalid nested type")
        for entry in values.values():
            if not isinstance(entry, dict) or set(entry) != fields:
                raise ValueError(f"{name} has invalid fields")
    for entry in value["evidence"].values():
        if (
            not isinstance(entry["active"], bool)
            or not all(isinstance(entry[key], str) for key in ("entity", "polarity", "source_id"))
        ):
            raise ValueError("evidence has invalid types")
    for entry in value["beliefs"].values():
        if not isinstance(entry["winner"], (str, type(None))) or (
            not isinstance(entry["residual_losers"], list)
            or any(not isinstance(item, str) for item in entry["residual_losers"])
        ):
            raise ValueError("belief has invalid types")
    for entry in value["concept_candidates"].values():
        if not isinstance(entry["activation"], (int, float)) or not isinstance(
            entry["label"], str
        ):
            raise ValueError("concept candidate has invalid types")
    return _copy(value)


def _initial_hash(
    *,
    config_hash: str,
    initial_state: Mapping[str, Any],
    parent_checkpoint_id: str | None,
    parent_checkpoint_hash: str | None,
    parent_state_hash: str | None,
    fork_point_event_hash: str | None,
    intervention_hash: str | None,
) -> str:
    material: dict[str, Any] = {
        "config_hash": config_hash,
        "initial_state": _copy(initial_state),
        "schema_version": TRACE_SCHEMA_VERSION,
    }
    bindings = (
        parent_checkpoint_hash,
        parent_state_hash,
        fork_point_event_hash,
        intervention_hash,
    )
    if parent_checkpoint_id is None:
        if any(item is not None for item in bindings):
            raise ValueError("root checkpoint has fork bindings")
    else:
        if not all(isinstance(item, str) and len(item) == 64 for item in bindings):
            raise ValueError("fork checkpoint bindings are invalid")
        material.update(
            {
                "parent_checkpoint_id": parent_checkpoint_id,
                "parent_checkpoint_hash": parent_checkpoint_hash,
                "parent_state_hash": parent_state_hash,
                "fork_point_event_hash": fork_point_event_hash,
                "intervention_hash": intervention_hash,
            }
        )
    return _hash(material)


@dataclass(frozen=True, slots=True)
class V03TraceEvent:
    sequence: int
    kind: str
    branch_id: str
    parent_event_hash: str
    state_hash_before: str
    state_hash_after: str
    payload: Mapping[str, Any]
    event_hash: str

    def as_dict(self) -> dict[str, Any]:
        if self.kind not in EVENTS or self.sequence < 0 or not self.branch_id:
            raise ValueError("invalid event")
        material = {
            "branch_id": self.branch_id,
            "kind": self.kind,
            "parent_event_hash": self.parent_event_hash,
            "payload": _copy(self.payload),
            "sequence": self.sequence,
            "state_hash_after": self.state_hash_after,
            "state_hash_before": self.state_hash_before,
        }
        if (
            any(
                not isinstance(item, str) or len(item) != 64
                for item in (
                    self.parent_event_hash,
                    self.state_hash_before,
                    self.state_hash_after,
                    self.event_hash,
                )
            )
            or _hash(material) != self.event_hash
        ):
            raise ValueError("event hash mismatch")
        return {**material, "event_hash": self.event_hash, "schema_version": TRACE_SCHEMA_VERSION}

    @classmethod
    def from_dict(cls, value: object) -> V03TraceEvent:
        if isinstance(value, Mapping):
            validate_schema_document("trace", value)
        required = {
            "branch_id",
            "event_hash",
            "kind",
            "parent_event_hash",
            "payload",
            "schema_version",
            "sequence",
            "state_hash_after",
            "state_hash_before",
        }
        if (
            not isinstance(value, dict)
            or set(value) != required
            or value["schema_version"] != TRACE_SCHEMA_VERSION
            or not isinstance(value["payload"], dict)
        ):
            raise ValueError("invalid trace event schema")
        event = cls(
            value["sequence"],
            value["kind"],
            value["branch_id"],
            value["parent_event_hash"],
            value["state_hash_before"],
            value["state_hash_after"],
            value["payload"],
            value["event_hash"],
        )
        event.as_dict()
        return event


@dataclass(frozen=True, slots=True)
class V03Checkpoint:
    checkpoint_id: str
    branch_id: str
    config: Mapping[str, Any]
    config_hash: str
    initial_state: Mapping[str, Any]
    initial_state_hash: str
    state: Mapping[str, Any]
    state_hash: str
    trace: tuple[V03TraceEvent, ...]
    parent_checkpoint_id: str | None = None
    parent_checkpoint_hash: str | None = None
    parent_state_hash: str | None = None
    fork_point_event_hash: str | None = None
    intervention_hash: str | None = None

    def as_dict(self) -> dict[str, Any]:
        initial, state = _state(self.initial_state), _state(self.state)
        if (
            _hash(self.config) != self.config_hash
            or _initial_hash(
                config_hash=self.config_hash,
                initial_state=initial,
                parent_checkpoint_id=self.parent_checkpoint_id,
                parent_checkpoint_hash=self.parent_checkpoint_hash,
                parent_state_hash=self.parent_state_hash,
                fork_point_event_hash=self.fork_point_event_hash,
                intervention_hash=self.intervention_hash,
            ) != self.initial_state_hash
            or (
                (
                    not self.trace
                    and (state != initial or self.state_hash != self.initial_state_hash)
                )
                or (bool(self.trace) and _hash(state) != self.state_hash)
            )
        ):
            raise ValueError("checkpoint root or state hash mismatch")
        return {
            "branch_id": self.branch_id,
            "checkpoint_id": self.checkpoint_id,
            "config": _copy(self.config),
            "config_hash": self.config_hash,
            "initial_state": initial,
            "initial_state_hash": self.initial_state_hash,
            "parent_checkpoint_id": self.parent_checkpoint_id,
            "parent_checkpoint_hash": self.parent_checkpoint_hash,
            "parent_state_hash": self.parent_state_hash,
            "fork_point_event_hash": self.fork_point_event_hash,
            "intervention_hash": self.intervention_hash,
            "schema_version": TRACE_SCHEMA_VERSION,
            "state": state,
            "state_hash": self.state_hash,
            "trace": [item.as_dict() for item in self.trace],
        }

    def canonical_hash(self) -> str:
        return _hash(self.as_dict())

    @classmethod
    def from_dict(cls, value: object) -> V03Checkpoint:
        if isinstance(value, Mapping):
            validate_schema_document("checkpoint", value)
        required = {
            "branch_id",
            "checkpoint_id",
            "config",
            "config_hash",
            "initial_state",
            "initial_state_hash",
            "parent_checkpoint_id",
            "parent_checkpoint_hash",
            "parent_state_hash",
            "fork_point_event_hash",
            "intervention_hash",
            "schema_version",
            "state",
            "state_hash",
            "trace",
        }
        if (
            not isinstance(value, dict)
            or set(value) != required
            or value["schema_version"] != TRACE_SCHEMA_VERSION
            or not isinstance(value["config"], dict)
            or not isinstance(value["trace"], list)
        ):
            raise ValueError("invalid checkpoint schema")
        item = cls(
            value["checkpoint_id"],
            value["branch_id"],
            value["config"],
            value["config_hash"],
            value["initial_state"],
            value["initial_state_hash"],
            value["state"],
            value["state_hash"],
            tuple(V03TraceEvent.from_dict(row) for row in value["trace"]),
            value["parent_checkpoint_id"],
            value["parent_checkpoint_hash"],
            value["parent_state_hash"],
            value["fork_point_event_hash"],
            value["intervention_hash"],
        )
        item.as_dict()
        return item


@dataclass(slots=True)
class V03TraceSession:
    config: Mapping[str, Any]
    branch_id: str = "main"
    state: dict[str, Any] = field(default_factory=dict)
    parent_checkpoint_id: str | None = None
    parent_checkpoint_hash: str | None = None
    parent_state_hash: str | None = None
    fork_point_event_hash: str | None = None
    intervention_hash: str | None = None
    _events: list[V03TraceEvent] = field(default_factory=list, init=False)
    initial_state: dict[str, Any] = field(default_factory=dict, init=False)
    config_hash: str = field(default="", init=False)
    initial_hash: str = field(default="", init=False)

    def __post_init__(self) -> None:
        self.config = _copy(self.config)
        defaults = {
            "evidence": {},
            "beliefs": {},
            "concept_candidates": {},
            "suppressed_modules": [],
            "goal": None,
            "intervention": None,
        }
        self.state = _copy({**defaults, **self.state})
        self.initial_state = _state(self.state)
        self.config_hash = _hash(self.config)
        self.initial_hash = _initial_hash(
            config_hash=self.config_hash,
            initial_state=self.initial_state,
            parent_checkpoint_id=self.parent_checkpoint_id,
            parent_checkpoint_hash=self.parent_checkpoint_hash,
            parent_state_hash=self.parent_state_hash,
            fork_point_event_hash=self.fork_point_event_hash,
            intervention_hash=self.intervention_hash,
        )

    @property
    def events(self) -> tuple[V03TraceEvent, ...]:
        return tuple(self._events)

    def state_hash(self) -> str:
        return self.initial_hash if not self._events else _hash(self.state)

    def inspect(self) -> dict[str, Any]:
        return _copy(self.state)

    def record(
        self, kind: str, payload: Mapping[str, Any], *, state_delta: Mapping[str, Any]
    ) -> V03TraceEvent:
        if kind not in EVENTS:
            raise ValueError("unsupported event")
        cited = payload.get("cited_evidence_ids", [])
        pre = self.state["evidence"]
        if (
            not isinstance(cited, list)
            or len(cited) != len(set(cited))
            or any(item not in pre or pre[item].get("active") is not True for item in cited)
        ):
            raise ValueError("citations require active pre-event evidence")
        if kind == "evidence_added" and payload.get("evidence_id") in cited:
            raise ValueError("same-event evidence citation is forbidden")
        before = self.state_hash()
        candidate = self.inspect()
        candidate.update(_copy(state_delta))
        candidate = _state(candidate)
        parent = self.initial_hash if not self._events else self._events[-1].event_hash
        material = {
            "branch_id": self.branch_id,
            "kind": kind,
            "parent_event_hash": parent,
            "payload": _copy(payload),
            "sequence": len(self._events),
            "state_hash_after": _hash(candidate),
            "state_hash_before": before,
        }
        event = V03TraceEvent(
            material["sequence"],
            kind,
            self.branch_id,
            parent,
            before,
            material["state_hash_after"],
            _copy(payload),
            _hash(material),
        )
        event.as_dict()
        self.state = candidate
        self._events.append(event)
        return event

    def checkpoint(self, checkpoint_id: str) -> V03Checkpoint:
        item = V03Checkpoint(
            checkpoint_id,
            self.branch_id,
            self.config,
            self.config_hash,
            self.initial_state,
            self.initial_hash,
            self.inspect(),
            self.state_hash(),
            self.events,
            self.parent_checkpoint_id,
            self.parent_checkpoint_hash,
            self.parent_state_hash,
            self.fork_point_event_hash,
            self.intervention_hash,
        )
        item.as_dict()
        return item

    def fork(
        self, checkpoint: V03Checkpoint, *, branch_id: str, intervention: Mapping[str, Any]
    ) -> V03TraceSession:
        from .replay import replay_trace

        if not isinstance(checkpoint, V03Checkpoint):
            raise ValueError("fork requires a checkpoint")
        replay_trace(checkpoint)
        parent_hash = checkpoint.canonical_hash()
        fork_point = (
            checkpoint.trace[-1].event_hash
            if checkpoint.trace
            else checkpoint.initial_state_hash
        )
        intervention_copy = _copy(intervention)
        child = V03TraceSession(
            checkpoint.config,
            branch_id,
            _copy(checkpoint.state),
            checkpoint.checkpoint_id,
            parent_hash,
            checkpoint.state_hash,
            fork_point,
            _hash(intervention_copy),
        )
        child.record(
            "intervention",
            {
                "cited_evidence_ids": [],
                "intervention": intervention_copy,
                "parent_checkpoint_hash": parent_hash,
                "parent_state_hash": checkpoint.state_hash,
            },
            state_delta={"intervention": intervention_copy},
        )
        return child
