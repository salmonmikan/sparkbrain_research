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


class StableScopeHypothesisRevisionOverlay:
    """Keep late-evidence state isolated by Assembly plus an explicit opaque scope token.

    Unlike hypothesis-set scoping, a stable scope preserves support for hypotheses that
    remain semantically continuous while the currently exposed pool changes. The caller
    owns scope lifetime; reusing a token intentionally reuses its prior evidence.
    """

    def __init__(self, config: RevisionOverlayConfig | None = None) -> None:
        self.config = config or RevisionOverlayConfig()
        self._overlays: dict[tuple[str, str], HypothesisRevisionOverlay] = {}

    @staticmethod
    def _key(base: PredictionPoolSnapshot, scope_token: str) -> tuple[str, str]:
        if base.assembly_id is None or not base.hypotheses:
            raise ValueError("stable scope requires a concrete Assembly and exposed hypotheses")
        values = tuple(row.value for row in base.hypotheses)
        if len(values) != len(set(values)):
            raise ValueError("hypothesis values must be unique")
        if not isinstance(scope_token, str) or not scope_token.strip():
            raise ValueError("scope_token must be a non-empty opaque string")
        return base.assembly_id, scope_token

    def apply_evidence(
        self,
        base: PredictionPoolSnapshot,
        *,
        scope_token: str,
        value: str,
        strength: float = 1.0,
    ) -> RevisionSnapshot:
        key = self._key(base, scope_token)
        overlay = self._overlays.setdefault(key, HypothesisRevisionOverlay(self.config))
        return overlay.apply_evidence(base, value=value, strength=strength)

    def evaluate(
        self,
        base: PredictionPoolSnapshot,
        *,
        scope_token: str,
    ) -> RevisionSnapshot:
        key = self._key(base, scope_token)
        overlay = self._overlays.get(key)
        return (overlay or HypothesisRevisionOverlay(self.config)).evaluate(base)

    def state_dict(self) -> dict[str, Any]:
        rows = []
        for (assembly_id, scope_token), overlay in sorted(self._overlays.items()):
            rows.append(
                {
                    "assembly_id": assembly_id,
                    "scope_token": scope_token,
                    "events": [event.as_dict() for event in overlay.events],
                }
            )
        return {"config": asdict(self.config), "scopes": rows}

    @classmethod
    def from_state_dict(cls, state: dict[str, Any]) -> StableScopeHypothesisRevisionOverlay:
        result = cls(RevisionOverlayConfig(**state["config"]))
        for row in state.get("scopes", []):
            assembly_id = str(row["assembly_id"])
            scope_token = str(row["scope_token"])
            if not assembly_id or not scope_token.strip():
                raise ValueError("persisted stable scope requires assembly_id and scope_token")
            overlay = HypothesisRevisionOverlay(result.config)
            overlay.events = [EvidenceUpdate(**event) for event in row.get("events", [])]
            result._overlays[(assembly_id, scope_token)] = overlay
        return result
