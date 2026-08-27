from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

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


def _state(value: object) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != STATE_KEYS:
        raise ValueError("state has unexpected fields")
    if not all(
        isinstance(value[key], expected)
        for key, expected in (
            ("evidence", dict),
            ("beliefs", dict),
            ("concept_candidates", dict),
            ("suppressed_modules", list),
        )
    ):
        raise ValueError("state has invalid nested type")
    return _copy(value)


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

    def as_dict(self) -> dict[str, Any]:
        initial, state = _state(self.initial_state), _state(self.state)
        if (
            _hash(self.config) != self.config_hash
            or _hash(
                {
                    "config_hash": self.config_hash,
                    "initial_state": initial,
                    "schema_version": TRACE_SCHEMA_VERSION,
                }
            )
            != self.initial_state_hash
            or _hash(state) != self.state_hash
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
            "schema_version": TRACE_SCHEMA_VERSION,
            "state": state,
            "state_hash": self.state_hash,
            "trace": [item.as_dict() for item in self.trace],
        }

    @classmethod
    def from_dict(cls, value: object) -> V03Checkpoint:
        required = {
            "branch_id",
            "checkpoint_id",
            "config",
            "config_hash",
            "initial_state",
            "initial_state_hash",
            "parent_checkpoint_id",
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
        )
        item.as_dict()
        return item


@dataclass(slots=True)
class V03TraceSession:
    config: Mapping[str, Any]
    branch_id: str = "main"
    state: dict[str, Any] = field(default_factory=dict)
    parent_checkpoint_id: str | None = None
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
        self.initial_hash = _hash(
            {
                "config_hash": self.config_hash,
                "initial_state": self.initial_state,
                "schema_version": TRACE_SCHEMA_VERSION,
            }
        )

    @property
    def events(self) -> tuple[V03TraceEvent, ...]:
        return tuple(self._events)

    def state_hash(self) -> str:
        return self.initial_hash if not self._events else _hash(self.state)

    def inspect(self) -> dict[str, Any]:
        return _copy(self.state)

    def record(
        self, kind: str, payload: Mapping[str, Any], delta: Mapping[str, Any]
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
        candidate.update(_copy(delta))
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
            _hash(self.state),
            self.events,
            self.parent_checkpoint_id,
        )
        item.as_dict()
        return item

    def fork(
        self, checkpoint: V03Checkpoint, *, branch_id: str, intervention: Mapping[str, Any]
    ) -> V03TraceSession:
        from .replay import replay_trace

        replay_trace(checkpoint)
        child = V03TraceSession(
            checkpoint.config, branch_id, _copy(checkpoint.state), checkpoint.checkpoint_id
        )
        child.record(
            "intervention",
            {"cited_evidence_ids": [], "intervention": _copy(intervention)},
            {"intervention": _copy(intervention)},
        )
        return child
