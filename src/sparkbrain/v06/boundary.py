from __future__ import annotations

import math
from collections.abc import Iterable, Mapping
from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any, Protocol

from .foundation import digest, validate_runtime_mapping


class BoundaryDirection(StrEnum):
    FIELD_TO_WORLD = "field-to-world"


class StructuralSpark(Protocol):
    spark_id: str
    time_ms: float
    unit_id: int
    generation_depth: int
    proposal_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class BoundaryCoupling:
    source_unit_id: int
    port_id: str
    delay_ms: float = 0.0
    magnitude: float = 1.0
    polarity: int = 1

    def __post_init__(self) -> None:
        if self.source_unit_id < 0:
            raise ValueError("source_unit_id must be non-negative")
        if not self.port_id:
            raise ValueError("port_id must be non-empty")
        for name in ("delay_ms", "magnitude"):
            value = float(getattr(self, name))
            if not math.isfinite(value) or value < 0:
                raise ValueError(f"{name} must be finite and non-negative")
        if self.polarity not in (-1, 1):
            raise ValueError("polarity must be -1 or 1")


@dataclass(frozen=True, slots=True)
class BoundaryIntervention:
    suppressed_port_ids: tuple[str, ...] = ()
    suppressed_source_unit_ids: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        if any(not port_id for port_id in self.suppressed_port_ids):
            raise ValueError("suppressed port IDs must be non-empty")
        if any(unit_id < 0 for unit_id in self.suppressed_source_unit_ids):
            raise ValueError("suppressed source units must be non-negative")


@dataclass(frozen=True, slots=True)
class BoundaryEvent:
    event_id: str
    time_ms: float
    port_id: str
    magnitude: float
    polarity: int
    direction: BoundaryDirection
    source_spark_id: str
    source_unit_id: int
    source_proposal_ids: tuple[str, ...]
    generation_depth: int
    source_state_hash: str

    def __post_init__(self) -> None:
        if not self.event_id or not self.port_id or not self.source_spark_id:
            raise ValueError("boundary identifiers must be non-empty")
        if not self.source_state_hash:
            raise ValueError("source_state_hash must be non-empty")
        if self.time_ms < 0 or self.magnitude < 0:
            raise ValueError("boundary time and magnitude must be non-negative")
        if self.polarity not in (-1, 1):
            raise ValueError("polarity must be -1 or 1")
        if self.source_unit_id < 0 or self.generation_depth < 0:
            raise ValueError("unit and generation depth must be non-negative")
        if self.direction is not BoundaryDirection.FIELD_TO_WORLD:
            raise ValueError("Primary boundary events must leave the Field")

    def state_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["direction"] = self.direction.value
        validate_runtime_mapping(value, path="v06.boundary.event")
        return value


@dataclass(frozen=True, slots=True)
class BoundarySuppressionRecord:
    source_spark_id: str
    source_unit_id: int
    port_id: str
    time_ms: float
    reason: str

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


class AnonymousBoundaryEmitter:
    """Convert selected actual Field Sparks into anonymous outbound events."""

    def __init__(
        self,
        couplings: Iterable[BoundaryCoupling],
        *,
        intervention: BoundaryIntervention | None = None,
    ) -> None:
        rows = tuple(couplings)
        if len({(row.source_unit_id, row.port_id) for row in rows}) != len(rows):
            raise ValueError("boundary couplings must be unique by source and port")
        self.couplings = rows
        self.intervention = intervention or BoundaryIntervention()
        grouped: dict[int, list[BoundaryCoupling]] = {}
        for row in rows:
            grouped.setdefault(row.source_unit_id, []).append(row)
        self._by_unit = {
            unit_id: tuple(sorted(items, key=lambda item: item.port_id))
            for unit_id, items in grouped.items()
        }
        self.events: list[BoundaryEvent] = []
        self.suppressions: list[BoundarySuppressionRecord] = []
        self._emitted_keys: set[tuple[str, str]] = set()

    def emit(
        self,
        sparks: Iterable[StructuralSpark],
        *,
        source_state_hash: str,
    ) -> tuple[BoundaryEvent, ...]:
        if not source_state_hash:
            raise ValueError("source_state_hash must be non-empty")
        created: list[BoundaryEvent] = []
        for spark in sparks:
            for coupling in self._by_unit.get(spark.unit_id, ()):
                key = (spark.spark_id, coupling.port_id)
                if key in self._emitted_keys:
                    continue
                self._emitted_keys.add(key)
                reason = self._suppression_reason(coupling)
                if reason is not None:
                    self.suppressions.append(
                        BoundarySuppressionRecord(
                            source_spark_id=spark.spark_id,
                            source_unit_id=spark.unit_id,
                            port_id=coupling.port_id,
                            time_ms=spark.time_ms,
                            reason=reason,
                        )
                    )
                    continue
                identity = {
                    "generation_depth": spark.generation_depth,
                    "port_id": coupling.port_id,
                    "source_spark_id": spark.spark_id,
                    "source_unit_id": spark.unit_id,
                    "time_ms": spark.time_ms + coupling.delay_ms,
                }
                event = BoundaryEvent(
                    event_id=f"boundary:{digest(identity)[:24]}",
                    time_ms=spark.time_ms + coupling.delay_ms,
                    port_id=coupling.port_id,
                    magnitude=coupling.magnitude,
                    polarity=coupling.polarity,
                    direction=BoundaryDirection.FIELD_TO_WORLD,
                    source_spark_id=spark.spark_id,
                    source_unit_id=spark.unit_id,
                    source_proposal_ids=spark.proposal_ids,
                    generation_depth=spark.generation_depth,
                    source_state_hash=source_state_hash,
                )
                self.events.append(event)
                created.append(event)
        return tuple(created)

    def _suppression_reason(self, coupling: BoundaryCoupling) -> str | None:
        if coupling.port_id in self.intervention.suppressed_port_ids:
            return "suppressed_port"
        if coupling.source_unit_id in self.intervention.suppressed_source_unit_ids:
            return "suppressed_source_unit"
        return None

    def state_dict(self) -> dict[str, Any]:
        value = {
            "couplings": [asdict(row) for row in self.couplings],
            "emitted_keys": [list(row) for row in sorted(self._emitted_keys)],
            "events": [row.state_dict() for row in self.events],
            "intervention": asdict(self.intervention),
            "suppressions": [row.state_dict() for row in self.suppressions],
        }
        validate_runtime_mapping(value, path="v06.boundary")
        return value

    def state_hash(self) -> str:
        return digest(self.state_dict())

    def events_by_port(self) -> Mapping[str, tuple[BoundaryEvent, ...]]:
        grouped: dict[str, list[BoundaryEvent]] = {}
        for event in self.events:
            grouped.setdefault(event.port_id, []).append(event)
        return {
            port_id: tuple(items)
            for port_id, items in sorted(grouped.items())
        }
