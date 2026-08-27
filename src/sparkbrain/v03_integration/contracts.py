from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Mapping


TRACE_SCHEMA_VERSION = "0.3"
_EVENT_KINDS = {
    "sensory_accepted",
    "sensory_suppressed",
    "evidence_added",
    "evidence_removed",
    "evidence_restored",
    "entity_assignment",
    "coalition_evaluated",
    "no_ignition",
    "workspace_broadcast",
    "concept_candidate",
    "intervention",
    "checkpoint",
}


def canonical_json(value: object) -> str:
    return json.dumps(value, allow_nan=False, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _hash(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _copy_json(value: Mapping[str, Any]) -> dict[str, Any]:
    return json.loads(canonical_json(dict(value)))


@dataclass(frozen=True, slots=True)
class V03TraceEvent:
    sequence: int
    kind: str
    branch_id: str
    state_hash_before: str
    state_hash_after: str
    payload: Mapping[str, Any]

    def as_dict(self) -> dict[str, Any]:
        if self.kind not in _EVENT_KINDS:
            raise ValueError(f"unsupported trace event: {self.kind}")
        if self.sequence < 0 or not self.branch_id:
            raise ValueError("trace sequence and branch_id are required")
        if len(self.state_hash_before) != 64 or len(self.state_hash_after) != 64:
            raise ValueError("trace state hashes must be SHA-256 values")
        return {
            "branch_id": self.branch_id,
            "kind": self.kind,
            "payload": _copy_json(self.payload),
            "schema_version": TRACE_SCHEMA_VERSION,
            "sequence": self.sequence,
            "state_hash_after": self.state_hash_after,
            "state_hash_before": self.state_hash_before,
        }


@dataclass(frozen=True, slots=True)
class V03Checkpoint:
    checkpoint_id: str
    branch_id: str
    sequence: int
    config: Mapping[str, Any]
    state: Mapping[str, Any]
    trace: tuple[V03TraceEvent, ...]
    state_hash: str
    parent_checkpoint_id: str | None = None

    def as_dict(self) -> dict[str, Any]:
        if self.sequence != len(self.trace) or self.state_hash != _hash(self.state):
            raise ValueError("checkpoint state or sequence is inconsistent")
        return {
            "branch_id": self.branch_id,
            "checkpoint_id": self.checkpoint_id,
            "config": _copy_json(self.config),
            "parent_checkpoint_id": self.parent_checkpoint_id,
            "schema_version": TRACE_SCHEMA_VERSION,
            "sequence": self.sequence,
            "state": _copy_json(self.state),
            "state_hash": self.state_hash,
            "trace": [event.as_dict() for event in self.trace],
        }


@dataclass(slots=True)
class V03TraceSession:
    """A deterministic, inspection-neutral ledger for v0.3 observability.

    The caller supplies only already-computed state deltas.  This prevents the
    UI/replay path from reconstructing evidence, beliefs, or attribution.
    """

    config: Mapping[str, Any]
    branch_id: str = "main"
    state: dict[str, Any] = field(default_factory=dict)
    parent_checkpoint_id: str | None = None
    _events: list[V03TraceEvent] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self) -> None:
        if not self.branch_id:
            raise ValueError("branch_id must not be empty")
        self.config = _copy_json(self.config)
        self.state = _copy_json(self.state)
        self.state.setdefault("evidence", {})
        self.state.setdefault("beliefs", {})
        self.state.setdefault("concept_candidates", {})
        self.state.setdefault("suppressed_modules", [])
        self.state.setdefault("goal", None)

    @property
    def events(self) -> tuple[V03TraceEvent, ...]:
        return tuple(self._events)

    def state_hash(self) -> str:
        return _hash(self.state)

    def inspect(self) -> dict[str, Any]:
        """Return a deep canonical snapshot without changing state or counters."""
        return _copy_json(self.state)

    def record(self, kind: str, payload: Mapping[str, Any], state_delta: Mapping[str, Any]) -> V03TraceEvent:
        if kind not in _EVENT_KINDS:
            raise ValueError(f"unsupported trace event: {kind}")
        before = self.state_hash()
        candidate = self.inspect()
        for key, value in state_delta.items():
            candidate[key] = _copy_json(value) if isinstance(value, Mapping) else copy.deepcopy(value)
        self._validate_attribution(kind, payload, candidate)
        self.state = candidate
        event = V03TraceEvent(
            sequence=len(self._events),
            kind=kind,
            branch_id=self.branch_id,
            state_hash_before=before,
            state_hash_after=self.state_hash(),
            payload=_copy_json(payload),
        )
        self._events.append(event)
        return event

    def checkpoint(self, checkpoint_id: str) -> V03Checkpoint:
        if not checkpoint_id:
            raise ValueError("checkpoint_id must not be empty")
        checkpoint = V03Checkpoint(
            checkpoint_id=checkpoint_id,
            branch_id=self.branch_id,
            sequence=len(self._events),
            config=self.config,
            state=self.inspect(),
            trace=self.events,
            state_hash=self.state_hash(),
            parent_checkpoint_id=self.parent_checkpoint_id,
        )
        checkpoint.as_dict()
        return checkpoint

    def fork(self, checkpoint: V03Checkpoint, *, branch_id: str, intervention: Mapping[str, Any]) -> V03TraceSession:
        if checkpoint.state_hash != _hash(checkpoint.state):
            raise ValueError("cannot fork an invalid checkpoint")
        child = V03TraceSession(
            config=checkpoint.config,
            branch_id=branch_id,
            state=_copy_json(checkpoint.state),
            parent_checkpoint_id=checkpoint.checkpoint_id,
        )
        child.record(
            "intervention",
            {"kind": "fork", "parent_checkpoint_id": checkpoint.checkpoint_id, "intervention": _copy_json(intervention)},
            {"intervention": _copy_json(intervention)},
        )
        return child

    @staticmethod
    def _validate_attribution(kind: str, payload: Mapping[str, Any], candidate: Mapping[str, Any]) -> None:
        cited = payload.get("cited_evidence_ids", ())
        if not isinstance(cited, (list, tuple)):
            raise ValueError("cited_evidence_ids must be a list when present")
        evidence = candidate.get("evidence", {})
        if not isinstance(evidence, Mapping) or any(item not in evidence for item in cited):
            raise ValueError("trace cites evidence absent from stored evidence state")
        if kind == "evidence_removed" and payload.get("evidence_id") in evidence:
            raise ValueError("removed evidence must not remain in the post-event state")
