from __future__ import annotations

from dataclasses import asdict
from typing import Any

from forge_prototypes.hypothesis_revision_overlay import (
    EvidenceUpdate,
    HypothesisRevisionOverlay,
    RevisionOverlayConfig,
    RevisionSnapshot,
)
from forge_prototypes.multi_hypothesis_prediction_pool import PredictionPoolSnapshot


class ScopedHypothesisRevisionOverlay:
    """Keep late-evidence state isolated by Assembly and exposed hypothesis set."""

    def __init__(self, config: RevisionOverlayConfig | None = None) -> None:
        self.config = config or RevisionOverlayConfig()
        self._overlays: dict[tuple[str, tuple[str, ...]], HypothesisRevisionOverlay] = {}

    @staticmethod
    def _key(base: PredictionPoolSnapshot) -> tuple[str, tuple[str, ...]] | None:
        if base.assembly_id is None or not base.hypotheses:
            return None
        values = tuple(sorted(row.value for row in base.hypotheses))
        if len(values) != len(set(values)):
            raise ValueError("hypothesis values must be unique")
        return base.assembly_id, values

    def apply_evidence(
        self, base: PredictionPoolSnapshot, *, value: str, strength: float = 1.0
    ) -> RevisionSnapshot:
        key = self._key(base)
        if key is None:
            raise ValueError("evidence requires a concrete Assembly and exposed hypotheses")
        overlay = self._overlays.setdefault(key, HypothesisRevisionOverlay(self.config))
        return overlay.apply_evidence(base, value=value, strength=strength)

    def evaluate(self, base: PredictionPoolSnapshot) -> RevisionSnapshot:
        key = self._key(base)
        overlay = None if key is None else self._overlays.get(key)
        return (overlay or HypothesisRevisionOverlay(self.config)).evaluate(base)

    def state_dict(self) -> dict[str, Any]:
        rows = []
        for (assembly_id, values), overlay in sorted(self._overlays.items()):
            rows.append(
                {
                    "assembly_id": assembly_id,
                    "hypothesis_values": list(values),
                    "events": [event.as_dict() for event in overlay.events],
                }
            )
        return {"config": asdict(self.config), "scopes": rows}

    @classmethod
    def from_state_dict(cls, state: dict[str, Any]) -> ScopedHypothesisRevisionOverlay:
        result = cls(RevisionOverlayConfig(**state["config"]))
        for row in state.get("scopes", []):
            key = (
                str(row["assembly_id"]),
                tuple(str(value) for value in row["hypothesis_values"]),
            )
            overlay = HypothesisRevisionOverlay(result.config)
            overlay.events = [EvidenceUpdate(**event) for event in row.get("events", [])]
            result._overlays[key] = overlay
        return result
