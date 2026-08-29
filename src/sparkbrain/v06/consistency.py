from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any, Literal

from .boundary import BoundaryEvent
from .foundation import (
    EventOrigin,
    ProvenanceLedger,
    RuntimePulse,
    digest,
    validate_runtime_mapping,
)


@dataclass(frozen=True, slots=True)
class AnonymousConsistencyConfig:
    maximum_pair_lag_ms: float = 30.0
    pending_ttl_ms: float = 40.0
    prior_consistent: float = 1.0
    prior_inconsistent: float = 1.0
    maximum_pending: int = 256
    single_external_per_boundary: bool = True

    def validate(self) -> None:
        for name in (
            "maximum_pair_lag_ms",
            "pending_ttl_ms",
            "prior_consistent",
            "prior_inconsistent",
        ):
            value = float(getattr(self, name))
            if not math.isfinite(value) or value <= 0:
                raise ValueError(f"{name} must be positive and finite")
        if self.maximum_pending < 1:
            raise ValueError("maximum_pending must be positive")


@dataclass(slots=True)
class AnonymousLinkState:
    port_id: str
    target: str
    polarity: int
    consistent_count: int = 0
    inconsistent_count: int = 0
    mean_lag_ms: float = 0.0
    lag_m2: float = 0.0
    mean_magnitude_ratio: float = 0.0
    last_boundary_event_id: str | None = None
    last_external_event_id: str | None = None

    def observe_consistency(
        self,
        *,
        boundary: BoundaryEvent,
        external: RuntimePulse,
    ) -> None:
        lag_ms = external.time_ms - boundary.time_ms
        ratio = external.magnitude / max(boundary.magnitude, 1e-12)
        self.consistent_count += 1
        delta = lag_ms - self.mean_lag_ms
        self.mean_lag_ms += delta / self.consistent_count
        self.lag_m2 += delta * (lag_ms - self.mean_lag_ms)
        self.mean_magnitude_ratio += (
            ratio - self.mean_magnitude_ratio
        ) / self.consistent_count
        self.last_boundary_event_id = boundary.event_id
        self.last_external_event_id = external.event_id

    def observe_inconsistency(self) -> None:
        self.inconsistent_count += 1

    def reliability(self, config: AnonymousConsistencyConfig) -> float:
        numerator = config.prior_consistent + self.consistent_count
        denominator = (
            config.prior_consistent
            + config.prior_inconsistent
            + self.consistent_count
            + self.inconsistent_count
        )
        return numerator / denominator

    @property
    def lag_variance(self) -> float:
        if self.consistent_count < 2:
            return 0.0
        return self.lag_m2 / (self.consistent_count - 1)

    def state_dict(self, config: AnonymousConsistencyConfig) -> dict[str, Any]:
        value = asdict(self)
        value["lag_variance"] = self.lag_variance
        value["reliability"] = self.reliability(config)
        return value

    def learned_state_dict(self) -> dict[str, Any]:
        """Return persistent learned quantities without derived or working state."""

        return asdict(self)

    @classmethod
    def from_learned_state_dict(cls, value: dict[str, Any]) -> AnonymousLinkState:
        row = cls(
            port_id=str(value["port_id"]),
            target=str(value["target"]),
            polarity=int(value["polarity"]),
            consistent_count=int(value["consistent_count"]),
            inconsistent_count=int(value["inconsistent_count"]),
            mean_lag_ms=float(value["mean_lag_ms"]),
            lag_m2=float(value["lag_m2"]),
            mean_magnitude_ratio=float(value["mean_magnitude_ratio"]),
            last_boundary_event_id=(
                str(value["last_boundary_event_id"])
                if value.get("last_boundary_event_id") is not None
                else None
            ),
            last_external_event_id=(
                str(value["last_external_event_id"])
                if value.get("last_external_event_id") is not None
                else None
            ),
        )
        if not row.port_id or not row.target:
            raise ValueError("learned anonymous link identifiers must be non-empty")
        if row.polarity not in (-1, 1):
            raise ValueError("learned anonymous link polarity must be -1 or 1")
        if row.consistent_count < 0 or row.inconsistent_count < 0:
            raise ValueError("learned anonymous link counts must be non-negative")
        for name in ("mean_lag_ms", "lag_m2", "mean_magnitude_ratio"):
            number = float(getattr(row, name))
            if not math.isfinite(number) or number < 0:
                raise ValueError(f"learned anonymous link {name} must be non-negative")
        if row.consistent_count == 0 and (
            row.mean_lag_ms != 0.0
            or row.lag_m2 != 0.0
            or row.mean_magnitude_ratio != 0.0
        ):
            raise ValueError("unobserved anonymous link cannot carry learned moments")
        return row


@dataclass(slots=True)
class PortExposureState:
    boundary_count: int = 0
    externally_paired_count: int = 0
    expired_count: int = 0

    def state_dict(self) -> dict[str, int]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class PendingBoundaryEvent:
    event: BoundaryEvent
    valid_until_ms: float

    def state_dict(self) -> dict[str, Any]:
        return {
            "event": self.event.state_dict(),
            "valid_until_ms": self.valid_until_ms,
        }


ConsistencyStatus = Literal["externally-consistent", "unpaired-external"]


@dataclass(frozen=True, slots=True)
class AnonymousConsistencyResolution:
    status: ConsistencyStatus
    boundary_event_id: str | None
    external_event_id: str
    port_id: str | None
    target: str
    lag_ms: float | None
    link_id: str | None
    reliability_before: float | None
    reliability_after: float | None

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


class UntypedBoundaryConsistency:
    """Stabilize anonymous port-to-external links only through external events.

    Boundary events create pending source exposures but cannot strengthen a
    link. A registered external event may externally pair with at most one
    pending boundary event. No scalar reward, correct port, outcome class,
    functional role, or relation type enters this state.
    """

    def __init__(
        self,
        ledger: ProvenanceLedger,
        config: AnonymousConsistencyConfig | None = None,
    ) -> None:
        self.ledger = ledger
        self.config = config or AnonymousConsistencyConfig()
        self.config.validate()
        self._pending: dict[str, PendingBoundaryEvent] = {}
        self._links: dict[tuple[str, str, int], AnonymousLinkState] = {}
        self._ports: dict[str, PortExposureState] = {}
        self.resolutions: list[AnonymousConsistencyResolution] = []

    def register_boundary(self, event: BoundaryEvent) -> None:
        if event.event_id in self._pending:
            raise ValueError("boundary event is already pending")
        if len(self._pending) >= self.config.maximum_pending:
            raise RuntimeError("anonymous consistency pending budget exceeded")
        self._pending[event.event_id] = PendingBoundaryEvent(
            event=event,
            valid_until_ms=event.time_ms + self.config.pending_ttl_ms,
        )
        self._ports.setdefault(event.port_id, PortExposureState()).boundary_count += 1

    def observe_external(self, external: RuntimePulse) -> AnonymousConsistencyResolution:
        if external.origin is not EventOrigin.EXTERNAL:
            raise ValueError("anonymous consistency accepts only external events")
        registered = self.ledger.events.get(external.event_id)
        if registered is None or registered != external:
            raise ValueError("external event must be registered in the shared ledger")
        candidates = self._candidate_boundary_ids(external)
        if not candidates:
            resolution = AnonymousConsistencyResolution(
                status="unpaired-external",
                boundary_event_id=None,
                external_event_id=external.event_id,
                port_id=None,
                target=external.target,
                lag_ms=None,
                link_id=None,
                reliability_before=None,
                reliability_after=None,
            )
            self.resolutions.append(resolution)
            return resolution

        boundary_id = min(
            candidates,
            key=lambda event_id: (
                external.time_ms - self._pending[event_id].event.time_ms,
                event_id,
            ),
        )
        pending = self._pending.pop(boundary_id)
        boundary = pending.event
        key = (boundary.port_id, external.target, external.polarity)
        state = self._links.get(key)
        before = (
            state.reliability(self.config)
            if state is not None
            else self._prior_reliability()
        )

        if self.config.single_external_per_boundary:
            for other_key, other_state in self._links.items():
                if other_key[0] == boundary.port_id and other_key != key:
                    other_state.observe_inconsistency()

        if state is None:
            state = AnonymousLinkState(
                port_id=boundary.port_id,
                target=external.target,
                polarity=external.polarity,
            )
            self._links[key] = state
        state.observe_consistency(boundary=boundary, external=external)
        self._ports[boundary.port_id].externally_paired_count += 1
        lag_ms = external.time_ms - boundary.time_ms
        resolution = AnonymousConsistencyResolution(
            status="externally-consistent",
            boundary_event_id=boundary.event_id,
            external_event_id=external.event_id,
            port_id=boundary.port_id,
            target=external.target,
            lag_ms=lag_ms,
            link_id=self._link_id(key),
            reliability_before=before,
            reliability_after=state.reliability(self.config),
        )
        self.resolutions.append(resolution)
        return resolution

    def expire(self, now_ms: float) -> tuple[str, ...]:
        if not math.isfinite(float(now_ms)):
            raise ValueError("now_ms must be finite")
        expired = tuple(
            event_id
            for event_id, pending in sorted(self._pending.items())
            if now_ms > pending.valid_until_ms
        )
        for event_id in expired:
            boundary = self._pending.pop(event_id).event
            self._ports[boundary.port_id].expired_count += 1
            for key, state in self._links.items():
                if key[0] == boundary.port_id:
                    state.observe_inconsistency()
        return expired

    def link_state(
        self,
        *,
        port_id: str,
        target: str,
        polarity: int = 1,
    ) -> AnonymousLinkState | None:
        return self._links.get((port_id, target, polarity))

    def reliability(
        self,
        *,
        port_id: str,
        target: str,
        polarity: int = 1,
    ) -> float | None:
        state = self.link_state(port_id=port_id, target=target, polarity=polarity)
        return state.reliability(self.config) if state is not None else None

    def learned_state_dict(self) -> dict[str, Any]:
        """Return persistent relation state without queues, exposures, or reports."""

        value = {
            "config": asdict(self.config),
            "links": {
                self._link_id(key): state.learned_state_dict()
                for key, state in sorted(self._links.items())
            },
        }
        validate_runtime_mapping(value, path="v06.anonymous_consistency.learned")
        return value

    @classmethod
    def from_learned_state_dict(
        cls,
        value: dict[str, Any],
        *,
        ledger: ProvenanceLedger,
    ) -> UntypedBoundaryConsistency:
        validate_runtime_mapping(value, path="v06.anonymous_consistency.learned")
        model = cls(
            ledger,
            AnonymousConsistencyConfig(**value["config"]),
        )
        for stored_link_id, row_value in value["links"].items():
            state = AnonymousLinkState.from_learned_state_dict(dict(row_value))
            key = (state.port_id, state.target, state.polarity)
            expected_link_id = model._link_id(key)
            if str(stored_link_id) != expected_link_id:
                raise ValueError("anonymous learned link ID does not match its content")
            if key in model._links:
                raise ValueError("duplicate anonymous learned link")
            model._links[key] = state
        return model

    def _candidate_boundary_ids(self, external: RuntimePulse) -> tuple[str, ...]:
        parent_ids = set(external.parent_event_ids)
        exact = tuple(
            event_id
            for event_id in sorted(parent_ids)
            if event_id in self._pending
            and self._valid_pair(self._pending[event_id], external)
        )
        if exact:
            return exact
        return tuple(
            event_id
            for event_id, pending in sorted(self._pending.items())
            if self._valid_pair(pending, external)
        )

    def _valid_pair(
        self,
        pending: PendingBoundaryEvent,
        external: RuntimePulse,
    ) -> bool:
        lag_ms = external.time_ms - pending.event.time_ms
        return (
            0 <= lag_ms <= self.config.maximum_pair_lag_ms
            and external.time_ms <= pending.valid_until_ms
        )

    def _prior_reliability(self) -> float:
        return self.config.prior_consistent / (
            self.config.prior_consistent + self.config.prior_inconsistent
        )

    @staticmethod
    def _link_id(key: tuple[str, str, int]) -> str:
        return (
            f"link:{digest({'port_id': key[0], 'target': key[1], 'polarity': key[2]})[:24]}"
        )

    def state_dict(self) -> dict[str, Any]:
        value = {
            "config": asdict(self.config),
            "links": {
                self._link_id(key): state.state_dict(self.config)
                for key, state in sorted(self._links.items())
            },
            "pending": {
                event_id: pending.state_dict()
                for event_id, pending in sorted(self._pending.items())
            },
            "ports": {
                port_id: state.state_dict()
                for port_id, state in sorted(self._ports.items())
            },
            "resolutions": [row.state_dict() for row in self.resolutions],
        }
        validate_runtime_mapping(value, path="v06.anonymous_consistency")
        return value

    def state_hash(self) -> str:
        return digest(self.state_dict())
