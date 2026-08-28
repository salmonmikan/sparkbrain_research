from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from sparkbrain.v03_seed import RevisionBeliefField


@dataclass(frozen=True)
class ResidualStateDiff:
    before: Mapping[str, Any]
    after: Mapping[str, Any]
    changed_paths: tuple[str, ...]


def _snapshot(obj: Any) -> Any:
    serialize = getattr(obj, 'serialize_state', None)
    if not callable(serialize):
        raise TypeError('belief field must expose serialize_state()')
    value = json.loads(serialize())
    if not isinstance(value, dict):
        raise TypeError('belief field serialization must be a JSON object')
    return value


def _diff(before: Any, after: Any, prefix: str = '') -> list[str]:
    if type(before) is not type(after):
        return [prefix or '$']
    if isinstance(before, dict):
        out: list[str] = []
        for key in sorted(set(before) | set(after)):
            path = f'{prefix}.{key}' if prefix else str(key)
            if key not in before or key not in after:
                out.append(path)
            else:
                out.extend(_diff(before[key], after[key], path))
        return out
    if isinstance(before, list):
        if len(before) != len(after):
            return [prefix]
        out: list[str] = []
        for i, (a, b) in enumerate(zip(before, after, strict=True)):
            out.extend(_diff(a, b, f'{prefix}[{i}]'))
        return out
    return [] if before == after else [prefix]


def disable_loser_residual_only(belief_field: Any) -> ResidualStateDiff:
    """Disable loser retention without resetting winners, entities, or inventory.

    This corrective helper intentionally supports only the C15
    ``RevisionBeliefField``, whose update rule applies ``loser_retention`` only
    to non-winning states. The generic v0.3 ``PersistentBeliefField`` applies
    its retention factor to every state before winner gain, so changing that
    config cannot be described as a pure loser-only ablation and is rejected.
    """
    if type(belief_field) is not RevisionBeliefField:
        raise NotImplementedError(
            'pure loser-only ablation is available only for RevisionBeliefField'
        )
    before = _snapshot(belief_field)
    original_retention = belief_field.loser_retention
    belief_field.loser_retention = 0.0
    after = _snapshot(belief_field)
    changed = tuple(_diff(before, after))
    if any(path != 'config.loser_retention' for path in changed):
        belief_field.loser_retention = original_retention
        raise RuntimeError('loser-only ablation changed runtime state unexpectedly')
    return ResidualStateDiff(before=before, after=after, changed_paths=changed)
