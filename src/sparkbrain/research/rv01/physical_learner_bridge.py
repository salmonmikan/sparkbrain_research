from __future__ import annotations

import dataclasses
import hashlib
import importlib
import inspect
import json
import math
from dataclasses import dataclass
from types import ModuleType
from typing import Any

from sparkbrain.v04.field import ExcitableFieldConfig, TemporalExcitableField
from sparkbrain.v04.topology import UnitState, explicit_topology
from sparkbrain.v06.foundation import EventOrigin, RuntimePulse

_PHYSICAL_MODULE = "sparkbrain.research.rv01.physical_plasticity"


def _canonical_json(value: object) -> str:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def _digest(value: object) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class ResolvedPhysicalLearnerApi:
    module_name: str
    learner_class_name: str
    observe_method_name: str
    observe_mode: str
    constructor_parameters: tuple[str, ...]
    observe_parameters: tuple[str, ...]
    connection_class_module: str
    connection_class_name: str
    api_hash: str

    def state_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)


@dataclass(frozen=True, slots=True)
class PhysicalConnectionSnapshot:
    source_id: int
    target_id: int
    weight: float
    delay_ms: float

    def validate(self) -> None:
        if self.source_id < 0 or self.target_id < 0:
            raise ValueError("connection endpoints must be non-negative")
        if not math.isfinite(self.weight):
            raise ValueError("connection weight must be finite")
        if not math.isfinite(self.delay_ms) or self.delay_ms <= 0.0:
            raise ValueError("connection delay must be positive and finite")

    def state_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)


@dataclass(frozen=True, slots=True)
class LearnerObservationResult:
    accepted: bool
    ignored_or_rejected: bool
    method_name: str
    mode: str
    connection_hash_before: str
    connection_hash_after: str

    def state_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)


class CurrentPhysicalLearnerBridge:
    """Reuse the current RV01 physical learner without duplicating its rule.

    The bridge resolves one concrete learner and observation method from the
    existing ``physical_plasticity`` module. Resolution is deterministic and
    fail-closed. It does not inspect capability outcomes and does not select a
    learner by whichever one performs best.

    This bridge is development integration scaffolding. Before held-out freeze,
    the resolved API hash must be reviewed and replaced by an explicit frozen
    import contract.
    """

    def __init__(self, field: TemporalExcitableField) -> None:
        self.field = field
        self._module = importlib.import_module(_PHYSICAL_MODULE)
        self._connection_class = _resolve_connection_class()
        (
            self._learner_class,
            self._observe_method_name,
            self._observe_mode,
        ) = _resolve_learner_contract(self._module)
        self._learner = _instantiate_learner(self._learner_class, field)
        self.api = _api_record(
            self._learner_class,
            self._observe_method_name,
            self._observe_mode,
            self._connection_class,
        )

    def observe_sequence(self, pulses: tuple[RuntimePulse, ...]) -> tuple[LearnerObservationResult, ...]:
        if len(pulses) < 2:
            raise ValueError("physical learner sequence requires at least two pulses")
        if any(
            right.time_ms <= left.time_ms
            for left, right in zip(pulses, pulses[1:], strict=False)
        ):
            raise ValueError("physical learner pulses must be strictly time ordered")
        if self._observe_mode == "stream":
            rows = []
            for pulse in pulses:
                rows.append(self._observe_stream_pulse(pulse))
            return tuple(rows)
        return tuple(
            self._observe_pair(source, target)
            for source, target in zip(pulses, pulses[1:], strict=False)
        )

    def observe_pair(
        self,
        source: RuntimePulse,
        target: RuntimePulse,
    ) -> LearnerObservationResult:
        if self._observe_mode == "stream":
            first = self._observe_stream_pulse(source)
            second = self._observe_stream_pulse(target)
            return LearnerObservationResult(
                accepted=first.accepted or second.accepted,
                ignored_or_rejected=(
                    first.ignored_or_rejected and second.ignored_or_rejected
                ),
                method_name=self._observe_method_name,
                mode=self._observe_mode,
                connection_hash_before=first.connection_hash_before,
                connection_hash_after=second.connection_hash_after,
            )
        return self._observe_pair(source, target)

    def _observe_stream_pulse(self, pulse: RuntimePulse) -> LearnerObservationResult:
        before = connection_state_hash(self.field)
        method = getattr(self._learner, self._observe_method_name)
        ignored = False
        try:
            result = _call_stream_method(method, pulse, self.field)
            ignored = _result_declares_ignored(result)
        except (TypeError, ValueError):
            if pulse.origin is EventOrigin.ENDOGENOUS:
                ignored = True
            else:
                raise
        after = connection_state_hash(self.field)
        accepted = after != before or not ignored
        return LearnerObservationResult(
            accepted=accepted,
            ignored_or_rejected=ignored,
            method_name=self._observe_method_name,
            mode=self._observe_mode,
            connection_hash_before=before,
            connection_hash_after=after,
        )

    def _observe_pair(
        self,
        source: RuntimePulse,
        target: RuntimePulse,
    ) -> LearnerObservationResult:
        before = connection_state_hash(self.field)
        method = getattr(self._learner, self._observe_method_name)
        ignored = False
        try:
            result = _call_pair_method(method, source, target, self.field)
            ignored = _result_declares_ignored(result)
        except (TypeError, ValueError):
            if (
                source.origin is EventOrigin.ENDOGENOUS
                or target.origin is EventOrigin.ENDOGENOUS
            ):
                ignored = True
            else:
                raise
        after = connection_state_hash(self.field)
        accepted = after != before or not ignored
        return LearnerObservationResult(
            accepted=accepted,
            ignored_or_rejected=ignored,
            method_name=self._observe_method_name,
            mode=self._observe_mode,
            connection_hash_before=before,
            connection_hash_after=after,
        )


def build_physical_field(
    *,
    unit_count: int,
    directed_edges: tuple[tuple[int, int], ...],
    threshold: float,
    initial_weight: float,
    initial_delay_ms: float,
) -> TemporalExcitableField:
    if unit_count < 1:
        raise ValueError("unit_count must be positive")
    if not math.isfinite(threshold) or threshold <= 0.0:
        raise ValueError("threshold must be positive and finite")
    if not math.isfinite(initial_weight):
        raise ValueError("initial_weight must be finite")
    if not math.isfinite(initial_delay_ms) or initial_delay_ms <= 0.0:
        raise ValueError("initial_delay_ms must be positive and finite")
    if len(set(directed_edges)) != len(directed_edges):
        raise ValueError("directed_edges must be unique")
    connection_class = _resolve_connection_class()
    connections = tuple(
        _new_connection(
            connection_class,
            source_id=source_id,
            target_id=target_id,
            weight=initial_weight,
            delay_ms=initial_delay_ms,
        )
        for source_id, target_id in directed_edges
    )
    topology = explicit_topology(
        tuple(
            UnitState(
                unit_id=unit_id,
                x=float(unit_id),
                y=0.0,
                base_threshold=threshold,
            )
            for unit_id in range(unit_count)
        ),
        connections,
        receptor_ids=tuple(range(unit_count)),
    )
    return TemporalExcitableField(
        topology,
        ExcitableFieldConfig(
            adaptation_increment=0.0,
            receptor_fanout=1,
            refractory_ms=max(1.0, initial_delay_ms * 0.25),
        ),
    )


def runtime_pulse(
    *,
    event_id: str,
    time_ms: float,
    unit_id: int,
    magnitude: float,
    origin: EventOrigin = EventOrigin.EXTERNAL,
) -> RuntimePulse:
    return RuntimePulse(
        event_id=event_id,
        time_ms=time_ms,
        target=f"unit:{unit_id}",
        magnitude=magnitude,
        polarity=1,
        origin=origin,
    )


def connection_snapshots(
    field: TemporalExcitableField,
) -> tuple[PhysicalConnectionSnapshot, ...]:
    rows: dict[tuple[int, int], PhysicalConnectionSnapshot] = {}

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            keys = set(value)
            if {"source_id", "target_id", "weight", "delay_ms"}.issubset(keys):
                row = PhysicalConnectionSnapshot(
                    source_id=int(value["source_id"]),
                    target_id=int(value["target_id"]),
                    weight=float(value["weight"]),
                    delay_ms=float(value["delay_ms"]),
                )
                row.validate()
                rows[(row.source_id, row.target_id)] = row
                return
            for item in value.values():
                visit(item)
        elif isinstance(value, (list, tuple)):
            for item in value:
                visit(item)

    visit(field.state_dict())
    if not rows:
        raise RuntimeError("no physical connection state found in Field state_dict")
    return tuple(rows[key] for key in sorted(rows))


def connection_state_hash(field: TemporalExcitableField) -> str:
    return _digest([row.state_dict() for row in connection_snapshots(field)])


def _resolve_connection_class() -> type[Any]:
    modules = (
        importlib.import_module("sparkbrain.v04.topology"),
        importlib.import_module("sparkbrain.v04.contracts"),
    )
    candidates: list[type[Any]] = []
    for module in modules:
        for value in vars(module).values():
            if not inspect.isclass(value) or not dataclasses.is_dataclass(value):
                continue
            names = {row.name for row in dataclasses.fields(value)}
            if {"source_id", "target_id", "weight", "delay_ms"}.issubset(names):
                candidates.append(value)
    unique = {(row.__module__, row.__name__): row for row in candidates}
    if len(unique) != 1:
        raise RuntimeError(
            "physical connection contract resolution must produce exactly one class"
        )
    return next(iter(unique.values()))


def _new_connection(
    connection_class: type[Any],
    *,
    source_id: int,
    target_id: int,
    weight: float,
    delay_ms: float,
) -> Any:
    kwargs = {
        "source_id": source_id,
        "target_id": target_id,
        "weight": weight,
        "delay_ms": delay_ms,
    }
    return connection_class(**kwargs)


def _resolve_learner_contract(
    module: ModuleType,
) -> tuple[type[Any], str, str]:
    rows: list[tuple[str, str, str, type[Any]]] = []
    priority = (
        "observe_external_transition",
        "observe_external_pair",
        "observe_external",
    )
    for value in vars(module).values():
        if not inspect.isclass(value) or value.__module__ != module.__name__:
            continue
        if value.__name__.endswith(("Config", "Result", "Report", "Suite")):
            continue
        for method_name in priority:
            if not hasattr(value, method_name):
                continue
            signature = inspect.signature(getattr(value, method_name))
            parameters = tuple(
                row
                for name, row in signature.parameters.items()
                if name != "self"
            )
            required = tuple(
                row
                for row in parameters
                if row.default is inspect.Parameter.empty
                and row.kind
                not in {
                    inspect.Parameter.VAR_KEYWORD,
                    inspect.Parameter.VAR_POSITIONAL,
                }
            )
            mode = "stream" if len(required) <= 1 else "pair"
            rows.append((value.__name__, method_name, mode, value))
            break
    rows.sort(key=lambda row: (priority.index(row[1]), row[0]))
    if len(rows) != 1:
        names = [f"{row[0]}.{row[1]}:{row[2]}" for row in rows]
        raise RuntimeError(
            "physical learner contract resolution must produce exactly one learner: "
            + ", ".join(names)
        )
    _, method_name, mode, learner_class = rows[0]
    return learner_class, method_name, mode


def _instantiate_learner(
    learner_class: type[Any],
    field: TemporalExcitableField,
) -> Any:
    signature = inspect.signature(learner_class)
    kwargs: dict[str, Any] = {}
    for name, parameter in signature.parameters.items():
        if name in {"field", "runtime", "physical_field"}:
            kwargs[name] = field
        elif name in {"topology", "network"}:
            kwargs[name] = field.topology
        elif parameter.default is not inspect.Parameter.empty:
            continue
        elif name == "config":
            annotation = parameter.annotation
            if inspect.isclass(annotation):
                kwargs[name] = annotation()
            else:
                raise RuntimeError("required learner config is not constructible")
        else:
            raise RuntimeError(
                f"unsupported required learner constructor parameter: {name}"
            )
    return learner_class(**kwargs)


def _api_record(
    learner_class: type[Any],
    observe_method_name: str,
    observe_mode: str,
    connection_class: type[Any],
) -> ResolvedPhysicalLearnerApi:
    constructor_parameters = tuple(inspect.signature(learner_class).parameters)
    observe_parameters = tuple(
        name
        for name in inspect.signature(
            getattr(learner_class, observe_method_name)
        ).parameters
        if name != "self"
    )
    raw = {
        "connection_class": (
            f"{connection_class.__module__}.{connection_class.__name__}"
        ),
        "constructor_parameters": constructor_parameters,
        "learner_class": f"{learner_class.__module__}.{learner_class.__name__}",
        "observe_method_name": observe_method_name,
        "observe_mode": observe_mode,
        "observe_parameters": observe_parameters,
    }
    return ResolvedPhysicalLearnerApi(
        module_name=learner_class.__module__,
        learner_class_name=learner_class.__name__,
        observe_method_name=observe_method_name,
        observe_mode=observe_mode,
        constructor_parameters=constructor_parameters,
        observe_parameters=observe_parameters,
        connection_class_module=connection_class.__module__,
        connection_class_name=connection_class.__name__,
        api_hash=_digest(raw),
    )


def _call_stream_method(
    method: Any,
    pulse: RuntimePulse,
    field: TemporalExcitableField,
) -> Any:
    signature = inspect.signature(method)
    parameters = tuple(signature.parameters.values())
    if len(parameters) == 1:
        return method(pulse)
    kwargs = _mapped_kwargs(parameters, pulse, None, field)
    return method(**kwargs)


def _call_pair_method(
    method: Any,
    source: RuntimePulse,
    target: RuntimePulse,
    field: TemporalExcitableField,
) -> Any:
    signature = inspect.signature(method)
    parameters = tuple(signature.parameters.values())
    if len(parameters) == 2:
        return method(source, target)
    kwargs = _mapped_kwargs(parameters, source, target, field)
    return method(**kwargs)


def _mapped_kwargs(
    parameters: tuple[inspect.Parameter, ...],
    source: RuntimePulse,
    target: RuntimePulse | None,
    field: TemporalExcitableField,
) -> dict[str, Any]:
    current = target or source
    source_unit = int(source.target.split(":", maxsplit=1)[1])
    current_unit = int(current.target.split(":", maxsplit=1)[1])
    mapping: dict[str, Any] = {
        "current": current,
        "current_event": current,
        "event": current,
        "external_event": current,
        "field": field,
        "physical_field": field,
        "previous": source,
        "previous_event": source,
        "pulse": current,
        "source": source,
        "source_event": source,
        "source_id": source_unit,
        "source_time_ms": source.time_ms,
        "source_unit_id": source_unit,
        "target": current,
        "target_event": current,
        "target_id": current_unit,
        "target_time_ms": current.time_ms,
        "target_unit_id": current_unit,
        "time_ms": current.time_ms,
        "topology": field.topology,
    }
    kwargs: dict[str, Any] = {}
    for parameter in parameters:
        if parameter.kind in {
            inspect.Parameter.VAR_KEYWORD,
            inspect.Parameter.VAR_POSITIONAL,
        }:
            continue
        if parameter.name in mapping:
            kwargs[parameter.name] = mapping[parameter.name]
        elif parameter.default is inspect.Parameter.empty:
            raise RuntimeError(
                "unsupported physical learner observation parameter: "
                + parameter.name
            )
    return kwargs


def _result_declares_ignored(result: Any) -> bool:
    if result is None:
        return False
    if isinstance(result, bool):
        return not result
    if dataclasses.is_dataclass(result):
        value = dataclasses.asdict(result)
    elif isinstance(result, dict):
        value = result
    else:
        value = vars(result) if hasattr(result, "__dict__") else {}
    for key in ("ignored", "rejected", "skipped"):
        if bool(value.get(key, False)):
            return True
    accepted = value.get("accepted")
    return accepted is False
