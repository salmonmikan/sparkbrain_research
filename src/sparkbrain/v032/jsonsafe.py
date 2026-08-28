from __future__ import annotations

import dataclasses
import enum
import json
import math
from collections import deque
from collections.abc import Mapping
from pathlib import Path
from types import MappingProxyType
from typing import Any


def json_safe(value: Any) -> Any:
    return _json_safe(value, set())


def _json_safe(value: Any, stack: set[int]) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError('non-finite floats are not JSON-safe')
        return value
    if isinstance(value, enum.Enum):
        return _json_safe(value.value, stack)
    if isinstance(value, Path):
        return str(value)
    object_id = id(value)
    if object_id in stack:
        raise ValueError('cycle detected while producing JSON-safe data')
    stack.add(object_id)
    try:
        if dataclasses.is_dataclass(value):
            return {
                field.name: _json_safe(getattr(value, field.name), stack)
                for field in dataclasses.fields(value)
            }
        if isinstance(value, (Mapping, MappingProxyType)):
            result: dict[str, Any] = {}
            for key, child in value.items():
                normalized = key if isinstance(key, str) else repr(key)
                if normalized in result:
                    raise ValueError('mapping keys collide after JSON normalization')
                result[normalized] = _json_safe(child, stack)
            return {key: result[key] for key in sorted(result)}
        if isinstance(value, (list, tuple, deque)):
            return [_json_safe(item, stack) for item in value]
        if isinstance(value, (set, frozenset)):
            items = [_json_safe(item, stack) for item in value]
            return sorted(
                items,
                key=lambda item: json.dumps(
                    item,
                    allow_nan=False,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(',', ':'),
                ),
            )
        to_dict = getattr(value, 'to_dict', None)
        if callable(to_dict):
            return _json_safe(to_dict(), stack)
        if hasattr(value, '__dict__'):
            return {
                str(key): _json_safe(child, stack)
                for key, child in sorted(vars(value).items())
                if not callable(child)
            }
        value_type = type(value)
        raise TypeError(
            f'unsupported JSON-safe value: {value_type.__module__}.{value_type.__qualname__}'
        )
    finally:
        stack.remove(object_id)
