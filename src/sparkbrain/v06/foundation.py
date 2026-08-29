from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Iterable, Mapping
from dataclasses import asdict, dataclass, field, replace
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType
from typing import Any, Literal, Protocol

FORBIDDEN_RUNTIME_FIELDS = frozenset(
    {
        "assembly_id",
        "assembly_label",
        "assembly_membership",
        "assembly_prototype",
        "assembly_state",
        "motif_id",
        "hidden_state_id",
        "missing_target",
        "correct_action",
        "outcome_label",
    }
)
CHECKPOINT_SCHEMA = "0.6-dev1"


def canonical_json(value: object) -> str:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def digest(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _finite(name: str, value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def validate_runtime_mapping(value: Mapping[str, Any], *, path: str = "runtime") -> None:
    """Reject evaluator labels and explicit Assembly state anywhere in runtime data."""

    for raw_key, item in value.items():
        key = str(raw_key)
        if key in FORBIDDEN_RUNTIME_FIELDS:
            raise ValueError(f"forbidden runtime field at {path}.{key}")
        if isinstance(item, Mapping):
            validate_runtime_mapping(item, path=f"{path}.{key}")
        elif isinstance(item, (list, tuple)):
            for index, child in enumerate(item):
                if isinstance(child, Mapping):
                    validate_runtime_mapping(child, path=f"{path}.{key}[{index}]")


class EventOrigin(StrEnum):
    EXTERNAL = "external"
    ENDOGENOUS_UNCONFIRMED = "endogenous-unconfirmed"
    ENDOGENOUS_CONFIRMED = "endogenous-confirmed"
    ENDOGENOUS_CONTRADICTED = "endogenous-contradicted"
    ENDOGENOUS_EXPIRED = "endogenous-expired"

    @property
    def is_observation(self) -> bool:
        return self is EventOrigin.EXTERNAL

    @property
    def is_endogenous(self) -> bool:
        return self is not EventOrigin.EXTERNAL


@dataclass(frozen=True, slots=True)
class RuntimePulse:
    event_id: str
    time_ms: float
    target: str
    magnitude: float
    polarity: int
    origin: EventOrigin
    generation_depth: int = 0
    parent_event_ids: tuple[str, ...] = ()
    source_path_ids: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "time_ms", _finite("time_ms", self.time_ms))
        object.__setattr__(self, "magnitude", _finite("magnitude", self.magnitude))
        if self.time_ms < 0 or self.magnitude < 0:
            raise ValueError("time and magnitude must be non-negative")
        if not self.event_id or not self.target:
            raise ValueError("event_id and target must be non-empty")
        if self.polarity not in (-1, 1):
            raise ValueError("polarity must be -1 or 1")
        if self.generation_depth < 0:
            raise ValueError("generation_depth must be non-negative")
        if not isinstance(self.origin, EventOrigin):
            object.__setattr__(self, "origin", EventOrigin(self.origin))
        metadata = dict(self.metadata)
        validate_runtime_mapping(metadata, path="pulse.metadata")
        object.__setattr__(self, "metadata", metadata)

    @property
    def counts_as_external_observation(self) -> bool:
        return self.origin.is_observation

    def as_dict(self) -> dict[str, Any]:
        row = asdict(self)
        row["origin"] = self.origin.value
        row["parent_event_ids"] = list(self.parent_event_ids)
        row["source_path_ids"] = list(self.source_path_ids)
        return row


@dataclass(frozen=True, slots=True)
class EndogenousPulseProposal:
    proposal_id: str
    created_at_ms: float
    target: str
    predicted_arrival_ms: float
    magnitude: float
    polarity: int
    confidence: float
    origin_state_hash: str
    parent_proposal_ids: tuple[str, ...] = ()
    local_path_ids: tuple[str, ...] = ()
    generation_depth: int = 0
    valid_until_ms: float = 0.0
    energy_cost: float = 0.0

    def __post_init__(self) -> None:
        for name in (
            "created_at_ms",
            "predicted_arrival_ms",
            "magnitude",
            "confidence",
            "valid_until_ms",
            "energy_cost",
        ):
            object.__setattr__(self, name, _finite(name, getattr(self, name)))
        if not self.proposal_id or not self.target or not self.origin_state_hash:
            raise ValueError("proposal identifiers, target, and state hash must be non-empty")
        if self.created_at_ms < 0 or self.predicted_arrival_ms < self.created_at_ms:
            raise ValueError("proposal times must be ordered and non-negative")
        if self.valid_until_ms < self.predicted_arrival_ms:
            raise ValueError("valid_until_ms must not precede arrival")
        if self.magnitude < 0 or self.energy_cost < 0:
            raise ValueError("magnitude and energy_cost must be non-negative")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be in [0, 1]")
        if self.polarity not in (-1, 1):
            raise ValueError("polarity must be -1 or 1")
        if self.generation_depth < 0:
            raise ValueError("generation_depth must be non-negative")

    def to_runtime_pulse(self) -> RuntimePulse:
        return RuntimePulse(
            event_id=f"endo:{self.proposal_id}",
            time_ms=self.predicted_arrival_ms,
            target=self.target,
            magnitude=self.magnitude,
            polarity=self.polarity,
            origin=EventOrigin.ENDOGENOUS_UNCONFIRMED,
            generation_depth=self.generation_depth,
            parent_event_ids=tuple(f"endo:{row}" for row in self.parent_proposal_ids),
            source_path_ids=self.local_path_ids,
            metadata={
                "confidence": self.confidence,
                "energy_cost": self.energy_cost,
                "origin_state_hash": self.origin_state_hash,
                "valid_until_ms": self.valid_until_ms,
            },
        )


RealityStatus = Literal["matched", "contradicted", "expired", "downstream-confirmed"]


@dataclass(frozen=True, slots=True)
class RealityMatchRecord:
    proposal_id: str
    external_event_id: str | None
    status: RealityStatus
    target_error: float | None = None
    timing_error_ms: float | None = None
    magnitude_error: float | None = None
    polarity_match: bool | None = None
    confirmed_at_ms: float | None = None

    def __post_init__(self) -> None:
        if self.status in {"matched", "downstream-confirmed", "contradicted"}:
            if not self.external_event_id:
                raise ValueError(f"{self.status} requires an external event")
        if self.status in {"matched", "downstream-confirmed"} and self.confirmed_at_ms is None:
            raise ValueError("confirmation requires confirmed_at_ms")


@dataclass(frozen=True, slots=True)
class EndogenousChainRecord:
    chain_id: str
    root_state_hash: str
    proposal_ids: tuple[str, ...]
    generated_event_ids: tuple[str, ...]
    predicted_external_targets: tuple[str, ...]
    confirmation_state: EventOrigin = EventOrigin.ENDOGENOUS_UNCONFIRMED
    eligibility: float = 0.0

    def __post_init__(self) -> None:
        object.__setattr__(self, "eligibility", _finite("eligibility", self.eligibility))
        if not self.chain_id or not self.root_state_hash:
            raise ValueError("chain_id and root_state_hash must be non-empty")
        if self.eligibility < 0:
            raise ValueError("eligibility must be non-negative")
        if not self.confirmation_state.is_endogenous:
            raise ValueError("chain state must remain endogenous")


@dataclass(frozen=True, slots=True)
class LearningEligibility:
    eligibility_id: str
    chain_id: str
    path_ids: tuple[str, ...]
    candidate_delta: float
    created_at_ms: float
    valid_until_ms: float
    committed: bool = False
    confirming_external_event_id: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "candidate_delta", _finite("candidate_delta", self.candidate_delta)
        )
        object.__setattr__(self, "created_at_ms", _finite("created_at_ms", self.created_at_ms))
        object.__setattr__(self, "valid_until_ms", _finite("valid_until_ms", self.valid_until_ms))
        if not self.eligibility_id or not self.chain_id:
            raise ValueError("eligibility_id and chain_id must be non-empty")
        if self.valid_until_ms < self.created_at_ms:
            raise ValueError("eligibility validity must not move backwards")
        if self.committed and not self.confirming_external_event_id:
            raise ValueError("committed eligibility requires external confirmation")


class ProvenanceLedger:
    """Separates observations from predictions and blocks self-confirming learning."""

    def __init__(self) -> None:
        self.events: dict[str, RuntimePulse] = {}
        self.proposals: dict[str, EndogenousPulseProposal] = {}
        self.chains: dict[str, EndogenousChainRecord] = {}
        self.matches: dict[str, RealityMatchRecord] = {}
        self.eligibilities: dict[str, LearningEligibility] = {}
        self.external_observation_count = 0
        self.endogenous_event_count = 0
        self.committed_positive_updates = 0
        self.rejected_or_expired_updates = 0

    def register_event(self, pulse: RuntimePulse) -> None:
        if pulse.event_id in self.events:
            raise ValueError(f"duplicate event_id: {pulse.event_id}")
        self.events[pulse.event_id] = pulse
        if pulse.origin is EventOrigin.EXTERNAL:
            self.external_observation_count += 1
        else:
            self.endogenous_event_count += 1

    def register_external(self, pulse: RuntimePulse) -> None:
        if pulse.origin is not EventOrigin.EXTERNAL:
            raise ValueError("register_external accepts only external events")
        self.register_event(pulse)

    def register_proposal(self, proposal: EndogenousPulseProposal) -> RuntimePulse:
        if proposal.proposal_id in self.proposals:
            raise ValueError(f"duplicate proposal_id: {proposal.proposal_id}")
        self.proposals[proposal.proposal_id] = proposal
        pulse = proposal.to_runtime_pulse()
        self.register_event(pulse)
        return pulse

    def register_chain(self, chain: EndogenousChainRecord) -> None:
        if chain.chain_id in self.chains:
            raise ValueError(f"duplicate chain_id: {chain.chain_id}")
        unknown = set(chain.proposal_ids) - set(self.proposals)
        if unknown:
            raise ValueError(f"chain references unknown proposals: {sorted(unknown)}")
        self.chains[chain.chain_id] = chain

    def register_eligibility(self, row: LearningEligibility) -> None:
        if row.eligibility_id in self.eligibilities:
            raise ValueError(f"duplicate eligibility_id: {row.eligibility_id}")
        if row.chain_id not in self.chains:
            raise ValueError("eligibility references an unknown chain")
        if row.committed:
            raise ValueError("new eligibility must be uncommitted")
        self.eligibilities[row.eligibility_id] = row

    def _require_external(self, event_id: str | None) -> RuntimePulse:
        if not event_id:
            raise ValueError("external confirmation ID is required")
        pulse = self.events.get(event_id)
        if pulse is None or pulse.origin is not EventOrigin.EXTERNAL:
            raise ValueError("confirmation must reference a registered external event")
        return pulse

    def record_match(self, record: RealityMatchRecord) -> None:
        if record.proposal_id not in self.proposals:
            raise ValueError("reality match references an unknown proposal")
        if record.proposal_id in self.matches:
            raise ValueError("proposal already has a terminal reality match")
        if record.status in {"matched", "downstream-confirmed", "contradicted"}:
            self._require_external(record.external_event_id)
        self.matches[record.proposal_id] = record
        if record.status in {"matched", "downstream-confirmed"}:
            origin = EventOrigin.ENDOGENOUS_CONFIRMED
        elif record.status == "contradicted":
            origin = EventOrigin.ENDOGENOUS_CONTRADICTED
        else:
            origin = EventOrigin.ENDOGENOUS_EXPIRED
        event_id = f"endo:{record.proposal_id}"
        self.events[event_id] = replace(self.events[event_id], origin=origin)

    def commit_eligibility(
        self,
        eligibility_id: str,
        *,
        external_event_id: str,
        now_ms: float,
    ) -> LearningEligibility:
        self._require_external(external_event_id)
        row = self.eligibilities[eligibility_id]
        if row.committed:
            raise ValueError("eligibility already committed")
        if now_ms > row.valid_until_ms:
            raise ValueError("eligibility expired before confirmation")
        proposal_ids = self.chains[row.chain_id].proposal_ids
        confirmed = any(
            proposal_id in self.matches
            and self.matches[proposal_id].external_event_id == external_event_id
            and self.matches[proposal_id].status in {"matched", "downstream-confirmed"}
            for proposal_id in proposal_ids
        )
        if not confirmed:
            raise ValueError("external event has not confirmed this endogenous chain")
        committed = replace(
            row,
            committed=True,
            confirming_external_event_id=external_event_id,
        )
        self.eligibilities[eligibility_id] = committed
        self.committed_positive_updates += 1
        return committed

    def expire(self, now_ms: float) -> tuple[str, ...]:
        expired: list[str] = []
        for proposal_id, proposal in sorted(self.proposals.items()):
            if proposal_id not in self.matches and now_ms > proposal.valid_until_ms:
                self.record_match(
                    RealityMatchRecord(
                        proposal_id=proposal_id,
                        external_event_id=None,
                        status="expired",
                    )
                )
                expired.append(proposal_id)
        for eligibility_id, row in tuple(self.eligibilities.items()):
            if not row.committed and now_ms > row.valid_until_ms:
                self.eligibilities.pop(eligibility_id)
                self.rejected_or_expired_updates += 1
        return tuple(expired)

    def state_dict(self) -> dict[str, Any]:
        return {
            "events": {key: value.as_dict() for key, value in sorted(self.events.items())},
            "proposals": {
                key: asdict(value) for key, value in sorted(self.proposals.items())
            },
            "matches": {key: asdict(value) for key, value in sorted(self.matches.items())},
            "eligibilities": {
                key: asdict(value) for key, value in sorted(self.eligibilities.items())
            },
            "counters": {
                "external_observation_count": self.external_observation_count,
                "endogenous_event_count": self.endogenous_event_count,
                "committed_positive_updates": self.committed_positive_updates,
                "rejected_or_expired_updates": self.rejected_or_expired_updates,
            },
        }

    def state_hash(self) -> str:
        return digest(self.state_dict())


@dataclass(slots=True)
class AssemblyFreeRuntimeState:
    field_state: dict[str, Any] = field(default_factory=dict)
    external_queue: tuple[RuntimePulse, ...] = ()
    endogenous_queue: tuple[RuntimePulse, ...] = ()
    persistent_traces: dict[str, float] = field(default_factory=dict)
    local_transition_state: dict[str, Any] = field(default_factory=dict)
    homeostatic_state: dict[str, Any] = field(default_factory=dict)
    generation_budget_state: dict[str, Any] = field(default_factory=dict)
    reality_state: dict[str, Any] = field(default_factory=dict)
    counters: dict[str, int] = field(default_factory=dict)
    current_time_ms: float = 0.0

    def __post_init__(self) -> None:
        if self.current_time_ms < 0:
            raise ValueError("current_time_ms must be non-negative")
        validate_runtime_mapping(self.state_dict(), path="brain_state")

    def state_dict(self) -> dict[str, Any]:
        return {
            "field_state": self.field_state,
            "external_queue": [row.as_dict() for row in self.external_queue],
            "endogenous_queue": [row.as_dict() for row in self.endogenous_queue],
            "persistent_traces": dict(sorted(self.persistent_traces.items())),
            "local_transition_state": self.local_transition_state,
            "homeostatic_state": self.homeostatic_state,
            "generation_budget_state": self.generation_budget_state,
            "reality_state": self.reality_state,
            "counters": dict(sorted(self.counters.items())),
            "current_time_ms": float(self.current_time_ms),
        }

    def state_hash(self) -> str:
        return digest(self.state_dict())


@dataclass(frozen=True, slots=True)
class ImmutableRuntimeTrace:
    frames: tuple[Mapping[str, Any], ...]
    runtime_hash: str

    @classmethod
    def from_frames(cls, frames: Iterable[Mapping[str, Any]]) -> ImmutableRuntimeTrace:
        plain: list[dict[str, Any]] = []
        frozen: list[Mapping[str, Any]] = []
        for index, frame in enumerate(frames):
            row = _deep_plain(frame)
            validate_runtime_mapping(row, path=f"trace[{index}]")
            plain.append(row)
            frozen.append(_deep_freeze(row))
        return cls(frames=tuple(frozen), runtime_hash=digest(plain))


class RuntimeObserver(Protocol):
    def observe(self, trace: ImmutableRuntimeTrace) -> Mapping[str, Any]: ...


def run_observer(observer: RuntimeObserver, trace: ImmutableRuntimeTrace) -> Mapping[str, Any]:
    before = trace.runtime_hash
    artifact = dict(observer.observe(trace))
    if trace.runtime_hash != before:
        raise RuntimeError("observer mutated runtime trace identity")
    return artifact


def verify_non_interference(
    *,
    runtime_with_observer: Mapping[str, Any],
    runtime_without_observer: Mapping[str, Any],
) -> str:
    left = _deep_plain(runtime_with_observer)
    right = _deep_plain(runtime_without_observer)
    validate_runtime_mapping(left, path="observer_on")
    validate_runtime_mapping(right, path="observer_off")
    if left != right:
        raise AssertionError("observer ON/OFF runtime states differ")
    return digest(left)


def _deep_plain(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _deep_plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_deep_plain(item) for item in value]
    return value


def _deep_freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({str(key): _deep_freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_deep_freeze(item) for item in value)
    return value


def build_checkpoint(runtime_state: dict[str, Any]) -> dict[str, Any]:
    validate_runtime_mapping(runtime_state, path="checkpoint.runtime_state")
    payload = {"runtime_state": runtime_state, "schema_version": CHECKPOINT_SCHEMA}
    return {**payload, "state_hash": digest(payload)}


def validate_checkpoint(value: dict[str, Any]) -> dict[str, Any]:
    if value.get("schema_version") != CHECKPOINT_SCHEMA:
        raise ValueError("unsupported v0.6 checkpoint schema")
    payload = {
        "runtime_state": value.get("runtime_state"),
        "schema_version": value.get("schema_version"),
    }
    if not isinstance(payload["runtime_state"], dict):
        raise ValueError("runtime_state must be an object")
    validate_runtime_mapping(payload["runtime_state"], path="checkpoint.runtime_state")
    if value.get("state_hash") != digest(payload):
        raise ValueError("v0.6 checkpoint integrity mismatch")
    return payload["runtime_state"]


def save_checkpoint(path: str | Path, runtime_state: dict[str, Any]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(canonical_json(build_checkpoint(runtime_state)) + "\n", encoding="utf-8")


def load_checkpoint(path: str | Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("checkpoint must contain an object")
    return validate_checkpoint(value)
