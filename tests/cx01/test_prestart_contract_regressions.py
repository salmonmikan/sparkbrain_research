from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from sparkbrain.comparison.cx01.development import _evaluate_loop
from sparkbrain.comparison.cx01.formal_revision import (
    build_revised_formal_world,
)
from sparkbrain.comparison.cx01.worlds import CX01Family


class _RecordingLoopModel:
    def __init__(self, expected_generated: str) -> None:
        self.expected_generated = expected_generated
        self.events: list[tuple[Any, bool]] = []
        self.observed_external_events = 0

    def observe_external(
        self,
        event: Any,
        *,
        learn: bool = True,
    ) -> None:
        self.events.append((event, learn))
        self.observed_external_events += 1

    def generate(
        self,
        *,
        max_steps: int,
    ) -> tuple[SimpleNamespace, ...]:
        assert max_steps == 1
        timestamp = self.events[-1][0].timestamp_ms + 1.0
        return (
            SimpleNamespace(
                token=self.expected_generated,
                timestamp_ms=timestamp,
            ),
        )

    def finalize_episode(self) -> None:
        pass


def test_loop_evaluation_uses_declared_probe_timing() -> None:
    world = build_revised_formal_world(
        "cx01-fixture-loop-timing-regression",
        CX01Family.LOOP,
        5001,
    )
    assert world.loop is not None
    probe = world.probes[0]
    assert probe.lags_ms
    assert probe.lags_ms != (5.0,) * len(probe.lags_ms)

    model = _RecordingLoopModel(world.loop.expected_generated)
    evidence, _ = _evaluate_loop(model, world, 100.0)

    cue_events = [
        event
        for event, _ in model.events[: len(probe.prefix)]
    ]
    observed_lags = tuple(
        right.timestamp_ms - left.timestamp_ms
        for left, right in zip(
            cue_events[:-1],
            cue_events[1:],
            strict=True,
        )
    )
    assert observed_lags == probe.lags_ms
    assert evidence.correct_probes == 1
    assert evidence.self_confirmation_violations == 0
