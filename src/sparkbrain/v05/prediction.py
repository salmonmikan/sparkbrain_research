from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .contracts import AssemblyActivation, PredictionDecision


@dataclass(slots=True)
class AssemblyPredictor:
    counts: dict[str, dict[str, int]] = field(default_factory=dict)

    def predict(self, activation: AssemblyActivation | None) -> PredictionDecision:
        if activation is None or activation.suppressed or not activation.mature:
            return PredictionDecision(None, None, 0.0)
        table = self.counts.get(activation.assembly_id, {})
        total = sum(table.values())
        if not table or total <= 0:
            return PredictionDecision(activation.assembly_id, None, 0.0)
        value = max(sorted(table), key=lambda item: table[item])
        return PredictionDecision(
            activation.assembly_id,
            value,
            table[value] / total,
        )

    def observe(self, activation: AssemblyActivation | None, value: str | None) -> None:
        if (
            activation is None
            or activation.suppressed
            or not activation.mature
            or value is None
        ):
            return
        table = self.counts.setdefault(activation.assembly_id, {})
        table[value] = table.get(value, 0) + 1

    def state_dict(self) -> dict[str, Any]:
        return {
            "counts": {
                assembly_id: dict(sorted(table.items()))
                for assembly_id, table in sorted(self.counts.items())
            }
        }

    @classmethod
    def from_state_dict(cls, value: dict[str, Any]) -> AssemblyPredictor:
        row = cls()
        row.counts = {
            str(assembly_id): {str(k): int(v) for k, v in table.items()}
            for assembly_id, table in value["counts"].items()
        }
        return row
