from __future__ import annotations

from typing import Any

from forge_prototypes.hypothesis_revision_overlay import RevisionOverlayConfig, RevisionSnapshot
from forge_prototypes.multi_hypothesis_prediction_pool import PredictionPoolSnapshot
from forge_prototypes.stable_scope_hypothesis_revision import StableScopeHypothesisRevisionOverlay


class ManagedScopeHypothesisRevisionOverlay:
    """Add an explicit, replayable lifecycle boundary to stable-scope revision state.

    Closing a scope discards its accumulated evidence and tombstones the exact
    (Assembly, scope-token) pair so the token cannot accidentally resurrect stale
    support later. A caller that wants a fresh context must supply a new token.

    This remains ordinary session/cache lifecycle management, not a scientific
    mechanism or evidence-bearing authority.
    """

    def __init__(self, config: RevisionOverlayConfig | None = None) -> None:
        self._overlay = StableScopeHypothesisRevisionOverlay(config)
        self._closed: set[tuple[str, str]] = set()

    @staticmethod
    def _identity(base: PredictionPoolSnapshot, scope_token: str) -> tuple[str, str]:
        if base.assembly_id is None:
            raise ValueError("managed scope requires a concrete Assembly")
        if not isinstance(scope_token, str) or not scope_token.strip():
            raise ValueError("scope_token must be a non-empty opaque string")
        return base.assembly_id, scope_token

    def _ensure_open(self, base: PredictionPoolSnapshot, scope_token: str) -> None:
        if self._identity(base, scope_token) in self._closed:
            raise ValueError("scope token is closed for this Assembly; use a fresh token")

    def apply_evidence(
        self,
        base: PredictionPoolSnapshot,
        *,
        scope_token: str,
        value: str,
        strength: float = 1.0,
    ) -> RevisionSnapshot:
        self._ensure_open(base, scope_token)
        return self._overlay.apply_evidence(
            base,
            scope_token=scope_token,
            value=value,
            strength=strength,
        )

    def evaluate(
        self,
        base: PredictionPoolSnapshot,
        *,
        scope_token: str,
    ) -> RevisionSnapshot:
        self._ensure_open(base, scope_token)
        return self._overlay.evaluate(base, scope_token=scope_token)

    def close_scope(self, *, assembly_id: str, scope_token: str) -> bool:
        if not isinstance(assembly_id, str) or not assembly_id.strip():
            raise ValueError("assembly_id must be a non-empty string")
        if not isinstance(scope_token, str) or not scope_token.strip():
            raise ValueError("scope_token must be a non-empty opaque string")

        key = (assembly_id, scope_token)
        state = self._overlay.state_dict()
        before = len(state.get("scopes", []))
        state["scopes"] = [
            row
            for row in state.get("scopes", [])
            if (str(row["assembly_id"]), str(row["scope_token"])) != key
        ]
        self._overlay = StableScopeHypothesisRevisionOverlay.from_state_dict(state)
        self._closed.add(key)
        return len(state["scopes"]) != before

    def state_dict(self) -> dict[str, Any]:
        return {
            "overlay": self._overlay.state_dict(),
            "closed_scopes": [
                {"assembly_id": assembly_id, "scope_token": scope_token}
                for assembly_id, scope_token in sorted(self._closed)
            ],
        }

    @classmethod
    def from_state_dict(cls, state: dict[str, Any]) -> "ManagedScopeHypothesisRevisionOverlay":
        overlay_state = state["overlay"]
        result = cls(RevisionOverlayConfig(**overlay_state["config"]))
        result._overlay = StableScopeHypothesisRevisionOverlay.from_state_dict(overlay_state)
        for row in state.get("closed_scopes", []):
            assembly_id = str(row["assembly_id"])
            scope_token = str(row["scope_token"])
            if not assembly_id.strip() or not scope_token.strip():
                raise ValueError("persisted closed scope requires assembly_id and scope_token")
            result._closed.add((assembly_id, scope_token))
        return result
