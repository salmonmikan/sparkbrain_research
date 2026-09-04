from __future__ import annotations

from typing import Any

from sparkbrain.baselines.v06.g3_recurrent import (
    GenericRecurrentPredictor,
    RecurrentPredictorConfig,
)

from .contract import ComparatorKind
from .events import ComparatorEvent, EventOrigin, PredictionDistribution


class G3FirstOrderAnchor:
    """CX01 adapter over the historically used first-order G3 model.

    This preserves G3 semantics instead of silently upgrading it into a neural
    RNN. Timestamps are ignored by the learned transition model. Episode
    boundaries only delimit architecture-neutral CX01 sequences.
    """

    kind = ComparatorKind.G3_FIRST_ORDER

    def __init__(self, *, retention: float = 0.8) -> None:
        self.model = GenericRecurrentPredictor(
            RecurrentPredictorConfig(retention=retention, maximum_rollout_steps=8)
        )
        self._last_token: str | None = None
        self._time_ms = 0.0
        self._suppressed: set[str] = set()
        self._observed_events = 0

    def observe_external(self, event: ComparatorEvent, *, learn: bool = True) -> None:
        event.validate()
        if event.origin is not EventOrigin.EXTERNAL:
            raise ValueError("G3 anchor accepts external observations only")
        if event.timestamp_ms < self._time_ms:
            raise ValueError("events must be chronological")
        if event.episode_start:
            self._last_token = None
        if learn and self._last_token is not None:
            self.model.observe(self._last_token, event.token)
        self._last_token = event.token
        self._time_ms = event.timestamp_ms
        self._observed_events += 1

    def finalize_episode(self) -> None:
        self._last_token = None

    def advance(self, timestamp_ms: float) -> None:
        if timestamp_ms < self._time_ms:
            raise ValueError("time cannot move backwards")
        self._time_ms = timestamp_ms

    def generate(self, *, max_steps: int = 1) -> tuple[ComparatorEvent, ...]:
        if self._last_token is None:
            return ()
        tokens = self.model.rollout(
            self._last_token,
            steps=max_steps,
            suppressed_sources=tuple(sorted(self._suppressed)),
        )
        return tuple(
            ComparatorEvent(
                token=token,
                timestamp_ms=self._time_ms + float(index + 1),
                origin=EventOrigin.GENERATED,
            )
            for index, token in enumerate(tokens)
        )

    def distribution(self) -> PredictionDistribution:
        if self._last_token is None or self._last_token in self._suppressed:
            return PredictionDistribution(())
        row = self.model.learned_state_dict()["scores"].get(self._last_token, {})
        return PredictionDistribution.from_scores(row)

    def suppress(self, token: str) -> None:
        if not token:
            raise ValueError("suppressed token must be non-empty")
        self._suppressed.add(token)

    def clear_suppression(self) -> None:
        self._suppressed.clear()

    def snapshot(self) -> dict[str, Any]:
        return {
            "kind": self.kind.value,
            "last_token": self._last_token,
            "model": self.model.learned_state_dict(),
            "observed_events": self._observed_events,
            "suppressed": sorted(self._suppressed),
            "time_ms": self._time_ms,
        }

    def restore(self, state: dict[str, Any]) -> None:
        if state.get("kind") != self.kind.value:
            raise ValueError("snapshot kind mismatch")
        self.model = GenericRecurrentPredictor.from_learned_state_dict(state["model"])
        self._last_token = state["last_token"]
        self._observed_events = int(state.get("observed_events", self.model.observation_count))
        self._suppressed = set(state["suppressed"])
        self._time_ms = float(state["time_ms"])

    def learned_state_dict(self) -> dict[str, Any]:
        return self.model.learned_state_dict()

    @property
    def parameter_count(self) -> int:
        return self.model.state_entry_count

    @property
    def state_entry_count(self) -> int:
        return self.model.state_entry_count

    @property
    def observed_external_events(self) -> int:
        return self._observed_events

    @property
    def generated_internal_events(self) -> int:
        return self.model.generated_token_count
