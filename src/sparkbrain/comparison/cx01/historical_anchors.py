from __future__ import annotations

from typing import Any

from sparkbrain.baselines.v06.g4_assembly import ExplicitAssemblyComparator
from sparkbrain.baselines.v06.g5_typed import TypedFunctionalHeadComparator

from .contract import ComparatorKind
from .events import ComparatorEvent, EventOrigin, PredictionDistribution


def _leaf_count(value: Any) -> int:
    if isinstance(value, dict):
        return sum(_leaf_count(row) for row in value.values())
    if isinstance(value, (list, tuple, set, frozenset)):
        return sum(_leaf_count(row) for row in value)
    return 1


class G4AssemblyAnchor:
    """Historical explicit-Assembly comparator behind the CX01 event facade."""

    kind = ComparatorKind.G4_ASSEMBLY

    def __init__(self) -> None:
        self.model = ExplicitAssemblyComparator()
        self._episode: list[str] = []
        self._time_ms = 0.0
        self._suppressed: set[str] = set()
        self._observed_events = 0

    def _commit_pending(self) -> None:
        if len(self._episode) >= 2:
            self.model.observe_sequence(tuple(self._episode), repetitions=1)
        self._episode.clear()

    def observe_external(self, event: ComparatorEvent) -> None:
        event.validate()
        if event.origin is not EventOrigin.EXTERNAL:
            raise ValueError("G4 anchor accepts external observations only")
        if event.timestamp_ms < self._time_ms:
            raise ValueError("events must be chronological")
        if event.episode_start:
            self._commit_pending()
        self._episode.append(event.token)
        self._time_ms = event.timestamp_ms
        self._observed_events += 1

    def advance(self, timestamp_ms: float) -> None:
        if timestamp_ms < self._time_ms:
            raise ValueError("time cannot move backwards")
        self._time_ms = timestamp_ms

    def _selected_members(self) -> tuple[str, ...]:
        if not self._episode:
            return ()
        assembly_id = self.model.activate(self._episode[0])
        if assembly_id is None:
            return ()
        state = self.model.learned_state_dict()["assemblies"]
        return tuple(state[assembly_id]["members"])

    def distribution(self) -> PredictionDistribution:
        members = self._selected_members()
        position = len(self._episode)
        if not members or position >= len(members):
            return PredictionDistribution(())
        return PredictionDistribution.from_scores({members[position]: 1.0})

    def generate(self, *, max_steps: int = 1) -> tuple[ComparatorEvent, ...]:
        members = self._selected_members()
        if not members:
            return ()
        start = len(self._episode)
        generated: list[ComparatorEvent] = []
        for index, member in enumerate(members[start : start + max_steps]):
            generated.append(
                ComparatorEvent(member, self._time_ms + index + 1.0, EventOrigin.GENERATED)
            )
            self.model.generated_token_count += 1
            if member in self._suppressed:
                break
        return tuple(generated)

    def suppress(self, token: str) -> None:
        if not token:
            raise ValueError("suppressed token must be non-empty")
        self._suppressed.add(token)

    def clear_suppression(self) -> None:
        self._suppressed.clear()

    def snapshot(self) -> dict[str, Any]:
        # Inspection is pure: an unfinished episode remains pending and is
        # serialized instead of being silently converted into learned Assembly state.
        return {
            "episode": list(self._episode),
            "kind": self.kind.value,
            "model": self.model.learned_state_dict(),
            "observed_events": self._observed_events,
            "suppressed": sorted(self._suppressed),
            "time_ms": self._time_ms,
        }

    def restore(self, state: dict[str, Any]) -> None:
        if state.get("kind") != self.kind.value:
            raise ValueError("snapshot kind mismatch")
        self.model = ExplicitAssemblyComparator.from_learned_state_dict(state["model"])
        self._episode = [str(token) for token in state.get("episode", [])]
        self._observed_events = int(state["observed_events"])
        self._suppressed = set(str(token) for token in state["suppressed"])
        self._time_ms = float(state["time_ms"])

    @property
    def parameter_count(self) -> int:
        return _leaf_count(self.model.learned_state_dict())

    @property
    def state_entry_count(self) -> int:
        return self.parameter_count + len(self._episode)

    @property
    def observed_external_events(self) -> int:
        return self._observed_events

    @property
    def generated_internal_events(self) -> int:
        return self.model.generated_token_count


class G5TypedAnchor:
    """Historical typed prediction-head comparator behind anonymous events.

    The prediction head is exercised by CX01 sequence worlds. Historical typed
    action/reward/memory privilege remains disclosed separately; no hidden
    target or reward is injected through this facade.
    """

    kind = ComparatorKind.G5_TYPED

    def __init__(self) -> None:
        self.model = TypedFunctionalHeadComparator()
        self._last_token: str | None = None
        self._time_ms = 0.0
        self._suppressed: set[str] = set()
        self._observed_events = 0

    def observe_external(self, event: ComparatorEvent) -> None:
        event.validate()
        if event.origin is not EventOrigin.EXTERNAL:
            raise ValueError("G5 anchor accepts external observations only")
        if event.timestamp_ms < self._time_ms:
            raise ValueError("events must be chronological")
        if event.episode_start:
            self._last_token = None
        if self._last_token is not None:
            self.model.train_prediction_sequence((self._last_token, event.token), repetitions=1)
        self._last_token = event.token
        self._time_ms = event.timestamp_ms
        self._observed_events += 1

    def advance(self, timestamp_ms: float) -> None:
        if timestamp_ms < self._time_ms:
            raise ValueError("time cannot move backwards")
        self._time_ms = timestamp_ms

    def distribution(self) -> PredictionDistribution:
        if self._last_token is None or self._last_token in self._suppressed:
            return PredictionDistribution(())
        return PredictionDistribution.from_scores(
            self.model.prediction_head.get(self._last_token, {})
        )

    def generate(self, *, max_steps: int = 1) -> tuple[ComparatorEvent, ...]:
        if self._last_token is None:
            return ()
        tokens = self.model.predict_rollout(
            self._last_token,
            steps=max_steps,
            suppressed_sources=tuple(sorted(self._suppressed)),
        )
        return tuple(
            ComparatorEvent(token, self._time_ms + index + 1.0, EventOrigin.GENERATED)
            for index, token in enumerate(tokens)
        )

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
        self.model = TypedFunctionalHeadComparator.from_learned_state_dict(state["model"])
        self._last_token = state["last_token"]
        self._observed_events = int(state["observed_events"])
        self._suppressed = set(str(token) for token in state["suppressed"])
        self._time_ms = float(state["time_ms"])

    @property
    def parameter_count(self) -> int:
        return _leaf_count(self.model.learned_state_dict())

    @property
    def state_entry_count(self) -> int:
        return self.parameter_count

    @property
    def observed_external_events(self) -> int:
        return self._observed_events

    @property
    def generated_internal_events(self) -> int:
        return self.model.generated_count
