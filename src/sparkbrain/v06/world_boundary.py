from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from typing import Any

from .boundary import BoundaryEvent
from .foundation import EventOrigin, RuntimePulse, digest, validate_runtime_mapping


@dataclass(frozen=True, slots=True)
class AnonymousWorldLink:
    """Physical world-side mapping from an outbound port to a raw external pulse."""

    port_id: str
    target: str
    lag_ms: float
    magnitude: float
    polarity: int = 1

    def __post_init__(self) -> None:
        if not self.port_id or not self.target:
            raise ValueError("world-link identifiers must be non-empty")
        for name in ("lag_ms", "magnitude"):
            value = float(getattr(self, name))
            if not math.isfinite(value) or value < 0:
                raise ValueError(f"{name} must be finite and non-negative")
        if self.polarity not in (-1, 1):
            raise ValueError("polarity must be -1 or 1")


@dataclass(frozen=True, slots=True)
class WorldBoundaryIntervention:
    suppressed_port_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if any(not port_id for port_id in self.suppressed_port_ids):
            raise ValueError("suppressed port IDs must be non-empty")


class AnonymousBoundaryWorld:
    """Emit raw external events from anonymous outbound boundary events.

    This object is the world-side physical adapter. It does not send a correct
    port, scalar reward, utility value, semantic label, or functional category
    back to the Field.
    """

    def __init__(
        self,
        links: Iterable[AnonymousWorldLink],
        *,
        intervention: WorldBoundaryIntervention | None = None,
    ) -> None:
        rows = tuple(links)
        if len({row.port_id for row in rows}) != len(rows):
            raise ValueError("world links must be unique by port_id")
        self.links = rows
        self.intervention = intervention or WorldBoundaryIntervention()
        self._by_port = {row.port_id: row for row in rows}
        self.external_events: list[RuntimePulse] = []
        self.suppressed_boundary_event_ids: list[str] = []

    def receive(self, event: BoundaryEvent) -> tuple[RuntimePulse, ...]:
        if event.port_id in self.intervention.suppressed_port_ids:
            self.suppressed_boundary_event_ids.append(event.event_id)
            return ()
        link = self._by_port.get(event.port_id)
        if link is None:
            return ()
        identity = {
            "boundary_event_id": event.event_id,
            "port_id": event.port_id,
            "target": link.target,
            "time_ms": event.time_ms + link.lag_ms,
        }
        pulse = RuntimePulse(
            event_id=f"world:{digest(identity)[:24]}",
            time_ms=event.time_ms + link.lag_ms,
            target=link.target,
            magnitude=link.magnitude,
            polarity=link.polarity,
            origin=EventOrigin.EXTERNAL,
            parent_event_ids=(event.event_id,),
            metadata={
                "boundary_event_id": event.event_id,
                "boundary_port_id": event.port_id,
            },
        )
        self.external_events.append(pulse)
        return (pulse,)

    def state_dict(self) -> dict[str, Any]:
        value = {
            "external_events": [row.as_dict() for row in self.external_events],
            "intervention": asdict(self.intervention),
            "links": [asdict(row) for row in self.links],
            "suppressed_boundary_event_ids": list(self.suppressed_boundary_event_ids),
        }
        validate_runtime_mapping(value, path="v06.boundary_world")
        return value

    def state_hash(self) -> str:
        return digest(self.state_dict())
