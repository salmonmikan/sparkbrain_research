from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from typing import Any

from .events import ComparatorEvent, EventOrigin
from .schedule import build_balanced_exposure_schedule
from .worlds import CX01World


@dataclass(frozen=True, slots=True)
class TrainingTranscript:
    world_hash: str
    schedule_hash: str
    events: tuple[ComparatorEvent, ...]
    end_time_ms: float

    def validate(self) -> None:
        if len(self.world_hash) != 64 or len(self.schedule_hash) != 64:
            raise ValueError("transcript hashes must be SHA-256")
        if not self.events:
            raise ValueError("training transcript must contain external events")
        if not math.isfinite(self.end_time_ms):
            raise ValueError("training transcript end time must be finite")
        previous = -1.0
        episode_starts = 0
        for event in self.events:
            event.validate()
            if event.origin is not EventOrigin.EXTERNAL:
                raise ValueError("training transcript may contain external events only")
            if event.timestamp_ms < previous:
                raise ValueError("training transcript must be chronological")
            previous = event.timestamp_ms
            episode_starts += int(event.episode_start)
        if self.end_time_ms <= previous:
            raise ValueError("training transcript end time must follow the final event")
        if episode_starts < 1:
            raise ValueError("training transcript requires explicit episode boundaries")

    def state_dict(self) -> dict[str, Any]:
        self.validate()
        return {
            "end_time_ms": self.end_time_ms,
            "events": [event.state_dict() for event in self.events],
            "schedule_hash": self.schedule_hash,
            "world_hash": self.world_hash,
        }

    def transcript_hash(self) -> str:
        encoded = json.dumps(
            self.state_dict(),
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()


def build_training_transcript(
    world: CX01World,
    *,
    initial_time_ms: float = 0.0,
    episode_gap_ms: float = 25.0,
) -> TrainingTranscript:
    """Build the exact training stream before any architecture is instantiated."""

    world.validate()
    if initial_time_ms < 0 or episode_gap_ms <= 0:
        raise ValueError("training transcript timing configuration is invalid")
    schedule = build_balanced_exposure_schedule(tuple(row.exposures for row in world.training))
    events: list[ComparatorEvent] = []
    now = float(initial_time_ms)
    for episode in schedule.episodes:
        row = world.training[episode.sequence_index]
        events.append(
            ComparatorEvent(
                token=row.tokens[0],
                timestamp_ms=now,
                origin=EventOrigin.EXTERNAL,
                episode_start=True,
            )
        )
        for token, lag in zip(row.tokens[1:], row.lags_ms, strict=True):
            now += lag
            events.append(
                ComparatorEvent(
                    token=token,
                    timestamp_ms=now,
                    origin=EventOrigin.EXTERNAL,
                )
            )
        now += episode_gap_ms
    transcript = TrainingTranscript(
        world_hash=world.specification_hash(),
        schedule_hash=schedule.schedule_hash(),
        events=tuple(events),
        end_time_ms=now,
    )
    transcript.validate()
    return transcript
