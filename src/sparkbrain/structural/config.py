from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from typing import Any


@dataclass(frozen=True, slots=True)
class StructuralConfig:
    schema_version: str = "0.2"
    seed: int = 83
    source_modules: int = 12
    max_modules: int = 18
    max_active_edges: int = 96
    active_k: int = 4
    max_events_per_boundary: int = 2
    max_events_total: int = 16
    min_live_modules: int = 6
    min_in_degree: int = 1
    load_high: float = 1.65
    load_low: float = 0.12
    grow_credit: float = 0.08
    prune_credit: float = 0.005
    homeostasis_rate: float = 0.05
    credit_decay: float = 0.90
    reward_eligibility: bool = False
    enabled_events: tuple[str, ...] = (
        "create",
        "duplicate",
        "split",
        "merge",
        "edge_grow",
        "edge_prune",
        "module_prune",
    )
    multiplicity_min_seeds: int = 2
    decisiveness_margin: float = 0.05
    fertility_min_effect: float = 0.01
    specificity_margin: float = 0.02
    unrelated_collateral_max: float = 0.02

    def validate(self) -> None:
        if self.schema_version != "0.2":
            raise ValueError("Structural schema must remain 0.2")
        if not self.source_modules <= self.max_modules:
            raise ValueError("max_modules must cover source modules")
        if not 1 <= self.active_k <= self.source_modules:
            raise ValueError("active_k must fit the initial active graph")
        if self.max_active_edges > self.max_modules**2:
            raise ValueError("edge capacity exceeds fixed tensor capacity")
        if self.min_live_modules < self.active_k:
            raise ValueError("min_live_modules must retain a routable active set")
        if self.max_events_per_boundary < 0 or self.max_events_total < 0:
            raise ValueError("event budgets must be non-negative")
        if self.specificity_margin < 0 or self.unrelated_collateral_max < 0:
            raise ValueError("specificity thresholds must be non-negative")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, row: dict[str, Any]) -> StructuralConfig:
        allowed = {item.name for item in fields(cls)}
        values = {key: value for key, value in row.items() if key in allowed}
        if "enabled_events" in values:
            values["enabled_events"] = tuple(values["enabled_events"])
        result = cls(**values)
        result.validate()
        return result
