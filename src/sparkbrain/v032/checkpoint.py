from __future__ import annotations

import base64
import collections
import contextlib
import dataclasses
import enum
import hashlib
import importlib
import json
import math
import os
import random
import tempfile
from collections.abc import Mapping
from pathlib import Path
from typing import Any

SCHEMA = "sparkbrain.v032.direct-checkpoint"
SCHEMA_VERSION = 1
MAX_CHECKPOINT_BYTES = 32 * 1024 * 1024
MAX_NODE_DEPTH = 200
MAX_NODE_COUNT = 500_000
_BRAIN = "sparkbrain.v03.runtime:IntegratedV03Brain"
_FACADE = "sparkbrain.v032.runtime:IntegratedV032Brain"
_CLASSES = frozenset(
    {
        _BRAIN,
        "sparkbrain.v03.runtime:V03BrainConfig",
        "sparkbrain.v03.runtime:V03StepResult",
        "sparkbrain.v03_integration.contracts:V03TraceEvent",
        "sparkbrain.v03_integration.contracts:V03TraceSession",
        "sparkbrain.v03_seed.belief:BeliefFieldConfig",
        "sparkbrain.v03_seed.belief:PersistentBeliefField",
        "sparkbrain.v03_seed.coalition:CoalitionGate",
        "sparkbrain.v03_seed.coalition:CoalitionGateConfig",
        "sparkbrain.v03_seed.concepts:ConceptFormationConfig",
        "sparkbrain.v03_seed.concepts:OnlineConceptFormer",
        "sparkbrain.v03_seed.contracts:BeliefActivation",
        "sparkbrain.v03_seed.contracts:CoalitionState",
        "sparkbrain.v03_seed.contracts:EvidenceAuditRow",
        "sparkbrain.v03_seed.contracts:EvidenceRecord",
        "sparkbrain.v03_seed.contracts:IgnitionDecision",
        "sparkbrain.v03_seed.contracts:PerceptualSpark",
        "sparkbrain.v03_seed.evidence:EvidenceLedger",
        "sparkbrain.v03_seed.evidence:EvidenceLedgerConfig",
        "sparkbrain.v03_seed.sensory_field:_FeatureState",
        "sparkbrain.v03_seed.sensory_field:AdaptiveSensoryField",
        "sparkbrain.v03_seed.sensory_field:SensoryFieldConfig",
        "sparkbrain.v03_seed.sensory_field:SensoryWorkCounters",
    }
)
_BRAIN_ATTRS = frozenset(
    {
        "_candidate_keys",
        "_concept_observer",
        "_history",
        "_i3_evidence",
        "_last_action",
        "_last_attributions",
        "_last_concepts",
        "_last_feedback",
        "_last_no_ignition",
        "_last_revisions",
        "_model_hash",
        "_model_status",
        "_pending_i3",
        "_provided_revision_model",
        "_results",
        "_revision_controller",
        "_revision_model",
        "_rng",
        "_workspace",
        "belief_field",
        "coalition_gate",
        "config",
        "ledger",
        "sensory_field",
        "trace",
    }
)
_OBJECT_ATTRS = {
    "sparkbrain.v03_seed.belief:PersistentBeliefField": frozenset({"_states", "config"}),
    "sparkbrain.v03_seed.coalition:CoalitionGate": frozenset(
        {
            "_c14_signatures",
            "_c14_stability",
            "_last_top",
            "_last_top_signature",
            "_stability",
            "config",
        }
    ),
    "sparkbrain.v03_seed.concepts:OnlineConceptFormer": frozenset(
        {"_concepts", "config", "feature_counts", "pair_counts"}
    ),
    "sparkbrain.v03_seed.evidence:EvidenceLedger": frozenset(
        {
            "_active",
            "_audit",
            "_records",
            "_sample_ids",
            "_spark_to_samples",
            "config",
            "duplicate_deliveries",
        }
    ),
    "sparkbrain.v03_seed.sensory_field:AdaptiveSensoryField": frozenset(
        {"_counters", "_sequence", "_states", "config"}
    ),
}


def _class_path(value: Any) -> str:
    cls = value if isinstance(value, type) else type(value)
    return f"{cls.__module__}:{cls.__qualname__}"


def _resolve(path: str) -> type[Any]:
    if path not in _CLASSES:
        raise ValueError(f"checkpoint class is outside the exact registry: {path}")
    module_name, qualname = path.split(":", 1)
    obj: Any = importlib.import_module(module_name)
    for part in qualname.split("."):
        obj = getattr(obj, part)
    if not isinstance(obj, type) or _class_path(obj) != path:
        raise TypeError(f"checkpoint registry resolved an unexpected object: {path}")
    return obj


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _exact(node: Mapping[str, Any], expected: set[str], *, kind: str) -> None:
    if set(node) != expected:
        raise ValueError(f"malformed {kind} checkpoint node")


def _encode(value: Any, stack: set[int] | None = None) -> Any:
    stack = set() if stack is None else stack
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else {"__kind__": "float", "value": repr(value)}
    if isinstance(value, bytes):
        return {"__kind__": "bytes", "value": base64.b64encode(value).decode("ascii")}
    if isinstance(value, Path):
        return {"__kind__": "path", "value": str(value)}
    if isinstance(value, enum.Enum):
        path = _class_path(value)
        _resolve(path)
        return {"__kind__": "enum", "class": path, "value": _encode(value.value, stack)}
    object_id = id(value)
    if object_id in stack:
        raise ValueError(f"cycle detected while encoding {_class_path(value)}")
    stack.add(object_id)
    try:
        if dataclasses.is_dataclass(value):
            path = _class_path(value)
            _resolve(path)
            return {
                "__kind__": "dataclass",
                "class": path,
                "fields": {
                    field.name: _encode(getattr(value, field.name), stack)
                    for field in dataclasses.fields(value)
                },
            }
        if isinstance(value, Mapping):
            items = [[_encode(key, stack), _encode(child, stack)] for key, child in value.items()]
            items.sort(key=lambda item: _canonical(item[0]))
            return {"__kind__": "mapping", "items": items}
        if isinstance(value, (list, tuple, set, collections.deque)):
            items = [_encode(item, stack) for item in value]
            if isinstance(value, set):
                items.sort(key=_canonical)
            kind = type(value).__name__
            node = {"__kind__": kind, "items": items}
            if isinstance(value, collections.deque):
                node["maxlen"] = value.maxlen
            return node
        if isinstance(value, random.Random):
            return {"__kind__": "random", "state": _encode(value.getstate(), stack)}
        module = type(value).__module__
        if module.startswith("numpy"):
            import numpy as np

            if isinstance(value, np.ndarray):
                return {
                    "__kind__": "ndarray",
                    "dtype": str(value.dtype),
                    "shape": list(value.shape),
                    "data": value.tolist(),
                }
            if isinstance(value, np.generic):
                return value.item()
        if module.startswith("torch"):
            import torch

            if isinstance(value, torch.Tensor):
                cpu = value.detach().cpu()
                return {
                    "__kind__": "tensor",
                    "dtype": str(cpu.dtype),
                    "shape": list(cpu.shape),
                    "data": cpu.tolist(),
                }
        path = _class_path(value)
        _resolve(path)
        if not hasattr(value, "__dict__"):
            raise TypeError(f"unsupported direct-checkpoint value: {path}")
        return {
            "__kind__": "object",
            "class": path,
            "attrs": {
                key: _encode(child, stack)
                for key, child in sorted(vars(value).items())
                if not callable(child)
            },
        }
    finally:
        stack.remove(object_id)


def _decode(node: Any, *, depth: int = 0, budget: list[int] | None = None) -> Any:
    if depth > MAX_NODE_DEPTH:
        raise ValueError("direct checkpoint exceeds maximum node depth")
    budget = [MAX_NODE_COUNT] if budget is None else budget
    budget[0] -= 1
    if budget[0] < 0:
        raise ValueError("direct checkpoint exceeds maximum node count")
    if node is None or isinstance(node, (str, bool, int, float)):
        return node
    if not isinstance(node, dict) or "__kind__" not in node:
        raise ValueError("malformed checkpoint node")
    kind = node["__kind__"]

    def child(value: Any) -> Any:
        return _decode(value, depth=depth + 1, budget=budget)

    if kind in {"float", "bytes", "path"}:
        _exact(node, {"__kind__", "value"}, kind=kind)
        if kind == "float":
            if node["value"] not in {"inf", "-inf", "nan"}:
                raise ValueError("invalid encoded float")
            return float(node["value"])
        if kind == "bytes":
            return base64.b64decode(node["value"], validate=True)
        return Path(node["value"])
    if kind == "enum":
        _exact(node, {"__kind__", "class", "value"}, kind=kind)
        return _resolve(node["class"])(child(node["value"]))
    if kind in {"mapping", "list", "tuple", "set"}:
        _exact(node, {"__kind__", "items"}, kind=kind)
        if not isinstance(node["items"], list):
            raise ValueError(f"{kind} items must be a list")
        if kind == "mapping":
            result: dict[Any, Any] = {}
            for pair in node["items"]:
                if not isinstance(pair, list) or len(pair) != 2:
                    raise ValueError("mapping item must be a key/value pair")
                key = child(pair[0])
                if key in result:
                    raise ValueError("mapping contains a duplicate key")
                result[key] = child(pair[1])
            return result
        values = [child(item) for item in node["items"]]
        return values if kind == "list" else tuple(values) if kind == "tuple" else set(values)
    if kind == "deque":
        _exact(node, {"__kind__", "items", "maxlen"}, kind=kind)
        return collections.deque((child(item) for item in node["items"]), maxlen=node["maxlen"])
    if kind == "random":
        _exact(node, {"__kind__", "state"}, kind=kind)
        result = random.Random()
        result.setstate(child(node["state"]))
        return result
    if kind in {"ndarray", "tensor"}:
        _exact(node, {"__kind__", "data", "dtype", "shape"}, kind=kind)
        if kind == "ndarray":
            import numpy as np

            return np.asarray(node["data"], dtype=node["dtype"]).reshape(node["shape"])
        import torch

        dtype = getattr(torch, node["dtype"].split(".")[-1])
        return torch.tensor(node["data"], dtype=dtype).reshape(node["shape"])
    if kind in {"dataclass", "object"}:
        key = "fields" if kind == "dataclass" else "attrs"
        _exact(node, {"__kind__", "class", key}, kind=kind)
        if not isinstance(node[key], dict):
            raise ValueError(f"{kind} payload must be an object")
        cls = _resolve(node["class"])
        if kind == "dataclass":
            expected_names = {field.name for field in dataclasses.fields(cls)}
        else:
            expected_names = set(_OBJECT_ATTRS.get(node["class"], ()))
        if not expected_names or set(node[key]) != expected_names:
            raise ValueError(f"{kind} payload attributes do not match the exact contract")
        result = cls.__new__(cls)
        for name, value in node[key].items():
            if not isinstance(name, str) or not name:
                raise ValueError(f"{kind} attribute names must be non-empty strings")
            object.__setattr__(result, name, child(value))
        return result
    raise ValueError(f"unknown checkpoint node kind: {kind}")


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _publish_noreplace(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".staging", dir=path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.link(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


class DirectCheckpointManager:
    """Trusted-local direct checkpoint; the digest is not an authenticity signature."""

    @staticmethod
    def save(brain: Any, path: str | Path) -> str:
        from .runtime import IntegratedV032Brain

        facade = _FACADE if isinstance(brain, IntegratedV032Brain) else None
        target = brain._brain if facade is not None else brain
        if _class_path(target) != _BRAIN:
            raise TypeError("direct checkpoint supports only IntegratedV03Brain")
        lock = brain._step_lock if facade is not None else contextlib.nullcontext()
        with lock:
            body = {
                "brain_class": _BRAIN,
                "facade_class": facade,
                "runtime_state_hash": target.state_hash(),
                "schema": SCHEMA,
                "schema_version": SCHEMA_VERSION,
                "state": _encode(dict(target.__dict__)),
            }
            digest = hashlib.sha256(_canonical(body)).hexdigest()
            raw = _canonical({**body, "payload_hash": digest}) + b"\n"
            # Validate the complete bytes before the no-clobber publish. Direct
            # IntegratedV03Brain callers must keep the brain quiescent; the v032
            # facade shares this lock with step().
            DirectCheckpointManager._load_bytes(raw)
            _publish_noreplace(Path(path), raw)
        return digest

    @staticmethod
    def load(path: str | Path) -> Any:
        source = Path(path)
        if source.stat().st_size > MAX_CHECKPOINT_BYTES:
            raise ValueError("direct checkpoint exceeds maximum file size")
        return DirectCheckpointManager._load_bytes(source.read_bytes())

    @staticmethod
    def _load_bytes(raw: bytes) -> Any:
        try:
            payload = json.loads(raw, object_pairs_hook=_reject_duplicate_keys)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("direct checkpoint must be valid UTF-8 JSON") from exc
        expected = {
            "brain_class",
            "facade_class",
            "payload_hash",
            "runtime_state_hash",
            "schema",
            "schema_version",
            "state",
        }
        if not isinstance(payload, dict) or set(payload) != expected:
            raise ValueError("direct checkpoint has unexpected fields")
        if payload["schema"] != SCHEMA or payload["schema_version"] != SCHEMA_VERSION:
            raise ValueError("unsupported direct checkpoint schema")
        if payload["brain_class"] != _BRAIN or payload["facade_class"] not in {None, _FACADE}:
            raise ValueError("unsupported direct checkpoint class")
        body = {key: value for key, value in payload.items() if key != "payload_hash"}
        if hashlib.sha256(_canonical(body)).hexdigest() != payload["payload_hash"]:
            raise ValueError("direct checkpoint payload hash mismatch")
        if raw != _canonical(payload) + b"\n":
            raise ValueError("direct checkpoint is not strict canonical JSON")
        brain_class = _resolve(payload["brain_class"])
        brain = brain_class.__new__(brain_class)
        state = _decode(payload["state"])
        if not isinstance(state, dict):
            raise TypeError("checkpoint root state must be a mapping")
        if set(state) != _BRAIN_ATTRS:
            raise ValueError("checkpoint root state attributes do not match the exact contract")
        brain.__dict__.update(state)
        if brain.state_hash() != payload["runtime_state_hash"]:
            raise ValueError("direct checkpoint restored state hash mismatch")
        if payload["facade_class"] is not None:
            from .runtime import IntegratedV032Brain

            return IntegratedV032Brain(base=brain)
        return brain
