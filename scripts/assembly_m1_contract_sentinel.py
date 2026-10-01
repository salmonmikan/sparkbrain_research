"""Model-free temporal-inlet contract sentinel; deliberately fake components only.

No SparkBrain module is imported. This is not an M1/v0.5 adapter or learned model.
The coordinator owns every mutable field; snapshots cover these fakes only.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import re
from dataclasses import asdict, dataclass, field, fields


@dataclass(frozen=True, slots=True)
class Window:
    event_id: str
    start_ms: int = 0
    input_cutoff_ms: int = 40
    decision_ms: int = 72
    pulses: tuple[tuple[int, str, float], ...] = ((40, "Q", 1.0),)
    sensory: tuple[tuple[str, float], ...] = (("signal", 0.0),)
    route: tuple[float, ...] = (0.0,)


@dataclass(frozen=True, slots=True)
class Caps:
    context_scalars: int = 64
    route_dimensions: int = 8


@dataclass(frozen=True, slots=True)
class AdaptedObservation:
    event_id: str
    time_seconds: float
    sensory: tuple[tuple[str, float], ...]
    route: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class Action:
    event_id: str
    prediction: float | None
    decision: str
    reason: str


@dataclass(frozen=True, slots=True)
class Receipt:
    receipt_id: str
    event_id: str
    outcome: float


@dataclass(frozen=True, slots=True)
class Revision:
    receipt_id: str
    event_id: str
    sequence: int


@dataclass(frozen=True, slots=True)
class Pending:
    window: Window
    observation: AdaptedObservation
    action: Action


def _finite(value: object) -> float:
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError("finite non-boolean number required")
    return float(value)


def _identifier(value: object) -> None:
    if not isinstance(value, str) or re.fullmatch(r"[A-Za-z0-9._:-]{1,128}", value) is None:
        raise ValueError("invalid opaque identifier")


def _integer(value: object, lower: int, upper: int) -> None:
    if type(value) is not int or not lower <= value <= upper:
        raise ValueError("invalid bounded integer")


def _context(values: tuple[float, float]) -> tuple[float, float]:
    if not isinstance(values, tuple) or len(values) != 2:
        raise ValueError("context must have exactly two coordinates")
    result = tuple(_finite(value) for value in values)
    if any(value < 0 or value > 1 for value in result):
        raise ValueError("context coordinates must be in [0,1]")
    return result


def adapt(window: Window, context: tuple[float, float]) -> AdaptedObservation:
    """The proposed wire only; callers must run the coordinator preflight first."""
    z0, z1 = _context(context)
    return AdaptedObservation(
        window.event_id, window.decision_ms / 1000,
        tuple(sorted((*window.sensory, ("temporal_0", z0), ("temporal_1", z1)))),
        (*window.route, z0, z1),
    )


def fake_decide(observation: AdaptedObservation) -> Action:
    """A deliberately invented readout exposes which copy actually reaches a consumer."""
    sensory = dict(observation.sensory)
    prediction = sensory["temporal_0"] - sensory["temporal_1"]
    route = observation.route[-2] - observation.route[-1]
    if prediction == 0 or route == 0:
        return Action(observation.event_id, None, "abstain", "unsupported_sentinel")
    if (prediction > 0) != (route > 0):
        return Action(observation.event_id, prediction, "abstain", "predictive_scope_disagreement")
    return Action(
        observation.event_id, prediction,
        "act_alpha" if prediction > 0 else "act_beta", "predictive_scope_agreement",
    )


@dataclass(slots=True)
class FakeTemporalBackend:
    advance_calls: int = 0
    clock_ms: int = 0
    transient_buffer: list[tuple[int, str, float]] = field(default_factory=list)

    def advance(self, window: Window, supplied: tuple[float, float]) -> tuple[float, float]:
        # Supplied by the test; this fake does not infer it from the pulses.
        self.advance_calls += 1
        self.clock_ms = window.decision_ms
        self.transient_buffer.extend(window.pulses)
        return supplied


@dataclass(slots=True)
class FakeM1Consumer:
    observe_calls: int = 0
    feedback_calls: int = 0
    pending: AdaptedObservation | None = None
    credited: list[tuple[AdaptedObservation, float]] = field(default_factory=list)

    def observe(self, observation: AdaptedObservation) -> Action:
        if self.pending is not None:
            raise RuntimeError("consumer already pending")
        self.observe_calls += 1
        self.pending = observation
        return fake_decide(observation)

    def feedback(self, outcome: float) -> None:
        if self.pending is None:
            raise RuntimeError("consumer requires pending context")
        self.feedback_calls += 1
        self.credited.append((self.pending, outcome))
        self.pending = None


@dataclass(slots=True)
class SentinelCoordinator:
    caps: Caps = Caps()
    _backend: FakeTemporalBackend = field(default_factory=FakeTemporalBackend, init=False)
    _consumer: FakeM1Consumer = field(default_factory=FakeM1Consumer, init=False)
    _pending: Pending | None = field(default=None, init=False)
    _events: dict[str, str] = field(default_factory=dict, init=False)
    _receipts: dict[str, tuple[Receipt, Revision]] = field(default_factory=dict, init=False)
    _channels: tuple[str, ...] | None = field(default=None, init=False)
    _bound_caps: Caps = field(init=False)
    _last_receipt_ms: int = field(default=-1, init=False)

    def __post_init__(self) -> None:
        self._bound_caps = self.caps

    def inspect(self) -> dict[str, object]:
        return copy.deepcopy(asdict(self))

    def render(self) -> str:
        """An actual pure observation/export path exercised by the frozen observer case."""
        return json.dumps(self.inspect(), sort_keys=True, allow_nan=False)

    def _restore(self, before: SentinelCoordinator) -> None:
        # Enumerating dataclass fields covers all state of these slots-only owned fakes.
        for descriptor in fields(self):
            setattr(self, descriptor.name, copy.deepcopy(getattr(before, descriptor.name)))

    def _preflight(self, window: Window) -> None:
        if self._pending is not None:
            raise RuntimeError("one unresolved occurrence allowed")
        if self.caps != self._bound_caps:
            raise ValueError("configured ceilings changed")
        _integer(self.caps.context_scalars, 3, 64)
        _integer(self.caps.route_dimensions, 3, 8)
        _identifier(window.event_id)
        if window.event_id in self._events:
            raise ValueError("event identity reused")
        if not isinstance(window.sensory, tuple) or not isinstance(window.route, tuple):
            raise ValueError("immutable original feature tuples required")
        _integer(len(window.sensory), 1, self.caps.context_scalars - 2)
        _integer(len(window.route), 1, self.caps.route_dimensions - 2)
        for row in window.sensory:
            if not isinstance(row, tuple) or len(row) != 2:
                raise ValueError("immutable sensory pairs required")
            if not isinstance(row[0], str):
                raise ValueError("sensory channel must be text")
        names = tuple(sorted(name for name, _ in window.sensory))
        if len(set(names)) != len(names) or any(
            not isinstance(name, str) or not name or name in {"temporal_0", "temporal_1"}
            for name in names
        ):
            raise ValueError("invalid or reserved sensory channel")
        if self._channels is not None and names != self._channels:
            raise ValueError("original channel schema changed")
        for _, value in window.sensory:
            _finite(value)
        for value in window.route:
            _finite(value)
        for value in (window.start_ms, window.input_cutoff_ms, window.decision_ms):
            _integer(value, 0, 1_000_000)
        if not window.start_ms <= window.input_cutoff_ms < window.decision_ms:
            raise ValueError("invalid window clock")
        if window.start_ms <= self._last_receipt_ms or window.start_ms < self._backend.clock_ms:
            raise ValueError("window predates committed clock")
        if not isinstance(window.pulses, tuple) or not 1 <= len(window.pulses) <= 4:
            raise ValueError("bounded immutable pulse tuple required")
        previous = window.start_ms
        for pulse in window.pulses:
            if not isinstance(pulse, tuple) or len(pulse) != 3:
                raise ValueError("immutable pulse triples required")
            time_ms, channel, magnitude = pulse
            _integer(time_ms, window.start_ms, window.input_cutoff_ms)
            if time_ms < previous or not isinstance(channel, str) or not channel:
                raise ValueError("invalid pulse ordering or channel")
            if _finite(magnitude) < 0:
                raise ValueError("negative pulse magnitude")
            previous = time_ms

    def observe(
        self, window: Window, *, supplied_context: tuple[float, float], fault_at: str | None = None,
    ) -> Action:
        self._preflight(window)
        before = copy.deepcopy(self)
        try:
            features = self._backend.advance(window, supplied_context)
            if fault_at == "after_backend":
                raise RuntimeError("injected after backend advance")
            observation = adapt(window, features)
            action = self._consumer.observe(observation)
            if fault_at == "after_observe":
                raise RuntimeError("injected after consumer observation")
            self._pending = Pending(window, observation, action)
            self._channels = tuple(sorted(name for name, _ in window.sensory))
            self._events[window.event_id] = hashlib.sha256(
                json.dumps(asdict(window), sort_keys=True, allow_nan=False).encode()
            ).hexdigest()
            return action
        except Exception:
            self._restore(before)
            raise

    def deliver(
        self, receipt: Receipt, *, delivered_ms: int, fault_at: str | None = None,
    ) -> Revision:
        _identifier(receipt.receipt_id)
        _identifier(receipt.event_id)
        _finite(receipt.outcome)
        previous = self._receipts.get(receipt.receipt_id)
        if previous is not None:
            if previous[0] == receipt:
                return previous[1]
            raise ValueError("receipt identity conflict")
        if self._pending is None or receipt.event_id != self._pending.window.event_id:
            raise ValueError("receipt does not bind pending occurrence")
        _integer(delivered_ms, 0, 1_000_000)
        if delivered_ms <= self._pending.window.decision_ms:
            raise ValueError("receipt must follow decision")
        before = copy.deepcopy(self)
        try:
            self._consumer.feedback(receipt.outcome)
            if fault_at == "after_feedback":
                raise RuntimeError("injected after consumer feedback")
            revision = Revision(receipt.receipt_id, receipt.event_id, len(self._receipts) + 1)
            self._receipts[receipt.receipt_id] = (receipt, revision)
            self._pending = None
            self._last_receipt_ms = delivered_ms
            if fault_at == "after_commit":
                raise RuntimeError("injected after coordinator ledger commit")
            return revision
        except Exception:
            self._restore(before)
            raise
