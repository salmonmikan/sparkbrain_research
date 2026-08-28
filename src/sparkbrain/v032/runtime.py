from __future__ import annotations

import math
import threading
import weakref
from collections import Counter
from collections.abc import Mapping
from types import MappingProxyType
from typing import Any

from sparkbrain.v03 import IntegratedV03Brain, V03BrainConfig

from .contracts import SensoryChannelDecision, V032StepResult
from .jsonsafe import json_safe

_LOCK_REGISTRY_GUARD = threading.Lock()
_LOCK_REGISTRY: weakref.WeakKeyDictionary[IntegratedV03Brain, threading.RLock] = (
    weakref.WeakKeyDictionary()
)


def _shared_step_lock(brain: IntegratedV03Brain) -> threading.RLock:
    with _LOCK_REGISTRY_GUARD:
        lock = _LOCK_REGISTRY.get(brain)
        if lock is None:
            lock = threading.RLock()
            _LOCK_REGISTRY[brain] = lock
        return lock


def _deep_freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({str(key): _deep_freeze(child) for key, child in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_deep_freeze(child) for child in value)
    return value


def _number(data: Mapping[str, Any], *names: str) -> float | None:
    for name in names:
        value = data.get(name)
        if isinstance(value, bool):
            raise ValueError(f'sensory trace {name} must not be a boolean')
        if isinstance(value, (int, float)):
            numeric = float(value)
            if not math.isfinite(numeric):
                raise ValueError(f'sensory trace {name} must be finite')
            return numeric
    return None


def _normalise_trace(raw: Any) -> tuple[SensoryChannelDecision, ...]:
    if raw is None:
        return ()
    if isinstance(raw, dict):
        if all(isinstance(v, dict) for v in raw.values()):
            entries = [dict(v, channel=v.get('channel', str(k))) for k,v in raw.items()]
        else:
            entries = [raw]
    elif isinstance(raw, (list, tuple)):
        entries = list(raw)
    else:
        entries = [raw]
    decisions: list[SensoryChannelDecision] = []
    for index, entry in enumerate(entries):
        data = json_safe(entry)
        if not isinstance(data, dict):
            data = {'value': data}
        channel = str(data.get('channel', data.get('feature_id', data.get('feature', index))))
        accepted_value = data.get('accepted')
        if not isinstance(accepted_value, bool):
            raise ValueError('sensory trace accepted must be a boolean')
        accepted = accepted_value
        reason = data.get('reason') or data.get('suppression_reason') or data.get('decision_reason')

        decisions.append(SensoryChannelDecision(
            channel=channel,
            accepted=accepted,
            reason=str(reason) if reason is not None else None,
            activation=_number(data, 'activation', 'score', 'salience'),
            threshold=_number(data, 'threshold'),
            novelty=_number(data, 'normalized_novelty', 'novelty'),
            prediction_error=_number(data, 'prediction_error', 'error'),
            goal_contribution=_number(data, 'goal_contribution', 'goal_bias'),
            habituation=_number(data, 'habituation'),
            raw=_deep_freeze(data),
        ))
    return tuple(decisions)


class IntegratedV032Brain:
    """Additive v0.3.2 diagnostic facade around the accepted v0.3.1 runtime."""

    def __init__(
        self,
        config: V03BrainConfig | None = None,
        *,
        base: IntegratedV03Brain | None = None,
    ) -> None:
        if base is not None and config is not None:
            raise ValueError("config and base are mutually exclusive")
        if base is not None and type(base) is not IntegratedV03Brain:
            raise TypeError("base must be an exact IntegratedV03Brain instance")
        self._brain = base if base is not None else IntegratedV03Brain(config or V03BrainConfig())
        self._step_lock = _shared_step_lock(self._brain)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._brain, name)

    def step(
        self,
        sample: Any,
        *,
        goal_bias: Mapping[str, float] | None = None,
        world_feedback: Mapping[str, Any] | None = None,
    ) -> V032StepResult:
        with self._step_lock:
            field = self._brain.sensory_field
            original = field.observe_with_trace
            had_instance_override = "observe_with_trace" in vars(field)
            previous_override = vars(field).get("observe_with_trace")
            captured: list[tuple[Any, Any]] = []

            def observe_with_trace(*args: Any, **kwargs: Any) -> Any:
                output = original(*args, **kwargs)
                observed_sample = args[0] if args else kwargs.get("sample")
                captured.append((observed_sample, output))
                return output

            field.observe_with_trace = observe_with_trace
            try:
                base_result = self._brain.step(
                    sample,
                    goal_bias=goal_bias,
                    world_feedback=world_feedback,
                )
            finally:
                if had_instance_override:
                    field.observe_with_trace = previous_override
                else:
                    del field.observe_with_trace
            primary = [output for observed_sample, output in captured if observed_sample is sample]
            if len(primary) != 1:
                raise RuntimeError(
                    'v0.3 runtime did not produce exactly one primary sensory observation'
                )
            observation = primary[0]
            decisions = _normalise_trace(observation.channel_trace)
        accepted = tuple(item.channel for item in decisions if item.accepted)
        suppressed = tuple(item.channel for item in decisions if not item.accepted)
        reasons = Counter(item.reason or 'unspecified' for item in decisions if not item.accepted)
        return V032StepResult(
            base_result=base_result,
            sensory_channel_trace=decisions,
            accepted_channels=accepted,
            suppressed_channels=suppressed,
            suppression_reasons=MappingProxyType(dict(reasons)),
            dense_inspection_count=observation.work_delta.channels_inspected,
        )
