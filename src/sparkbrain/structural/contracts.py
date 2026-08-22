from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class StructuralIdentity:
    logical_id: str
    slot: int
    version: int
    status: str
    created_by: int | None
    parents: tuple[str, ...] = ()
    tombstone_reason: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(order=True, slots=True)
class StructuralEvent:
    boundary: int
    priority: int
    sequence: int
    kind: str = field(compare=False)
    source_slot: int | None = field(compare=False, default=None)
    target_slot: int | None = field(compare=False, default=None)
    score: float = field(compare=False, default=0.0)
    reason: str = field(compare=False, default="")
    status: str = field(compare=False, default="pending")
    rejection: str | None = field(compare=False, default=None)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class StructuralStats:
    routing_load: list[float]
    coactivation: list[list[float]]
    edge_credit: list[list[float]]
    confidence_delta: list[float]

    def validate(self, capacity: int) -> None:
        if len(self.routing_load) != capacity or len(self.confidence_delta) != capacity:
            raise ValueError("StructuralStats vector capacity mismatch")
        if any(len(row) != capacity for row in self.coactivation):
            raise ValueError("StructuralStats coactivation capacity mismatch")
        if any(len(row) != capacity for row in self.edge_credit):
            raise ValueError("StructuralStats edge credit capacity mismatch")
