"""SOURCE-ONLY joint-graph clone mechanics; no SparkBrain imports or execution authority.

The caller supplies an independently reviewed, exact-class source registry. Its tags
are provenance labels, not a substitute for the separate source-digest audit. Tests
use only model-free stand-ins. Passing them is not real G0 evidence.

The supported domain is deliberately closed: exact built-in containers, finite
scalar values, explicit instance dictionaries/slots, Random and one reviewed facade
constructor. All state is preflighted before reconstruction. Raw-base subgraphs must
not reach facades or lock resources: the base must be complete before its facade's
constructor runs. Such cycles are rejected rather than silently approximated.
"""
from __future__ import annotations

import _thread
import copy
import gc
import hashlib
import inspect
import json
import math
import queue
import random
import sys
import threading
import types
import weakref
from collections import deque
from collections.abc import Callable
from concurrent.futures import Future
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SOURCE_ONLY = True
RLOCK_TYPE = _thread.RLock
GUARD_TYPE = _thread.LockType


class OwnershipError(ValueError):
    """An unsupported graph, unsafe resource boundary, or failed proof."""


@dataclass(frozen=True)
class TypeSpec:
    """Exact reviewed Python class and its complete storage schema.

    ``dict_fields=None`` means no instance dictionary. Fields are an exact set;
    their actual insertion order is part of the graph, not taken from this schema.
    ``source_tag`` must identify the caller's independently verified source binding.
    """

    cls: type
    source_tag: str
    dict_fields: tuple[str, ...] | None = None
    slot_fields: tuple[str, ...] = ()


class SourceRegistry:
    """Exact-type registry with distinct synthetic and verified-source entry points.

    The ordinary constructor is SYNTHETIC_MODEL_FREE-only. Provenance labels never
    enable real types. ``from_verified_source`` does not load any runtime module and
    is only for a future separately authorized runner supplying preloaded classes.
    """

    def __init__(self, specs: tuple[TypeSpec, ...]) -> None:
        self.domain = "SYNTHETIC_MODEL_FREE"
        for spec in specs:
            if type(spec) is not TypeSpec or type(spec.cls) is not type:
                raise OwnershipError("type schema must bind an exact Python class")
            if spec.cls.__module__ == "sparkbrain" or spec.cls.__module__.startswith("sparkbrain."):
                raise OwnershipError("real runtime classes require the verified-source binder")
        self._populate(specs)

    def _populate(self, specs: tuple[TypeSpec, ...]) -> None:
        self._specs: dict[type, TypeSpec] = {}
        tags: set[str] = set()
        for spec in specs:
            if type(spec) is not TypeSpec or type(spec.cls) is not type:
                raise OwnershipError("type schema must bind an exact Python class")
            if spec.cls is not random.Random:
                if spec.cls.__bases__ != (object,):
                    raise OwnershipError("ordinary schema classes must directly inherit object")
                if spec.cls.__new__ is not object.__new__:
                    raise OwnershipError(
                        "ordinary schema classes require default object allocation")
            if not spec.source_tag or type(spec.source_tag) is not str:
                raise OwnershipError("missing source-class tag")
            if spec.cls in self._specs or spec.source_tag in tags:
                raise OwnershipError("duplicate class or source-class tag")
            if spec.cls in (dict, list, tuple, set, deque, RLOCK_TYPE, GUARD_TYPE):
                raise OwnershipError("built-in containers/resources cannot be rebound")
            if (type(spec.slot_fields) is not tuple
                    or (spec.dict_fields is not None and type(spec.dict_fields) is not tuple)):
                raise OwnershipError("field schema must use tuples")
            fields = (() if spec.dict_fields is None else spec.dict_fields) + spec.slot_fields
            if (any(type(name) is not str for name in fields)
                    or len(set(fields)) != len(fields)):
                raise OwnershipError("invalid or duplicate field schema")
            # Only genuine Python storage descriptors are admitted. Properties and
            # extension-state classes would make the alleged field list incomplete.
            slots: set[str] = set()
            dictionary = None
            for base in spec.cls.__mro__:
                if base not in (object, random.Random, random.Random.__base__):
                    if base.__module__ == "builtins":
                        raise OwnershipError("unreviewed built-in instance state")
                for name, descriptor in vars(base).items():
                    if type(descriptor) is types.MemberDescriptorType:
                        slots.add(name)
                    if name == "__dict__":
                        dictionary = descriptor
            if slots != set(spec.slot_fields):
                raise OwnershipError("slot schema differs from actual storage")
            if (dictionary is not None) != (spec.dict_fields is not None):
                raise OwnershipError("instance dictionary schema differs from storage")
            if dictionary is not None and type(dictionary) is not types.GetSetDescriptorType:
                raise OwnershipError("custom instance dictionary descriptor")
            if spec.cls is random.Random and spec.dict_fields is None:
                raise OwnershipError("Random requires its explicit Python field schema")
            self._specs[spec.cls] = spec
            tags.add(spec.source_tag)

    @classmethod
    def from_verified_source(cls, root: Path, loaded_classes: tuple[type, ...]) -> SourceRegistry:
        """Bind already-loaded classes to pinned source without importing runtime code.

        This is a dormant preparation entry point, not execution clearance. File
        hashes, class identity in the already-loaded module, module/name and source
        path must all match. It does not attest arbitrary monkey-patching of Python
        process memory; that remains excluded by the dedicated runner contract.
        """
        from scripts.verify_g0_joint_source_contract import CONTRACT, verify

        root = Path(root).resolve(strict=True)
        try:
            verified = verify(root)
            raw_contract = (root / CONTRACT).read_bytes()
            if hashlib.sha256(raw_contract).hexdigest() != verified["contract_sha256"]:
                raise ValueError("source contract changed after verification")
            contract = json.loads(raw_contract)
        except (OSError, ValueError, KeyError) as exc:
            raise OwnershipError(f"source verification failed: {exc}") from None
        specs = []
        for loaded in loaded_classes:
            if type(loaded) is not type:
                raise OwnershipError("loaded registry entries must be exact class objects")
            if loaded is random.Random:
                specs.append(TypeSpec(random.Random, "stdlib:random.Random:exact-state-v1",
                                      ("gauss_next",)))
                continue
            module_name = loaded.__module__
            module = sys.modules.get(module_name)
            if (type(module) is not types.ModuleType
                    or loaded.__qualname__ != loaded.__name__
                    or vars(module).get(loaded.__name__) is not loaded):
                raise OwnershipError("loaded class is not its exact module-level binding")
            relative = "src/" + module_name.replace(".", "/") + ".py"
            record = contract["files"].get(relative)
            if record is None or loaded.__name__ not in record["classes"]:
                raise OwnershipError("loaded class is absent from the pinned source contract")
            expected_path = (root / relative).resolve(strict=True)
            try:
                module_path = Path(vars(module)["__file__"]).resolve(strict=True)
                class_path = Path(inspect.getsourcefile(loaded)).resolve(strict=True)
            except (KeyError, OSError, TypeError):
                raise OwnershipError("loaded class source path is unavailable") from None
            if module_path != expected_path or class_path != expected_path:
                raise OwnershipError("loaded class source path differs from verified root")
            if hashlib.sha256(expected_path.read_bytes()).hexdigest() != record["sha256"]:
                raise OwnershipError("loaded class source bytes changed after verification")
            witness = record["classes"][loaded.__name__]
            slots = tuple(witness["slot_fields"])
            dictionary = None if slots else tuple(witness["dict_fields"])
            specs.append(TypeSpec(loaded,
                                  f"{relative}:{loaded.__name__}@{record['sha256']}",
                                  dictionary, slots))
        bound = object.__new__(cls)
        bound.domain = "VERIFIED_SOURCE_PREPARATION"
        bound.contract_sha256 = verified["contract_sha256"]
        bound.source_root = root
        bound._populate(tuple(specs))
        return bound

    def validate_resources(self, resources: ResourceBoundary) -> None:
        if self.domain != "VERIFIED_SOURCE_PREPARATION":
            return
        facade = resources.facade_type
        raw = resources.raw_type
        module = sys.modules.get("sparkbrain.v032.runtime")
        raw_module = sys.modules.get("sparkbrain.v03.runtime")
        if (type(module) is not types.ModuleType or type(raw_module) is not types.ModuleType
                or vars(module).get("IntegratedV032Brain") is not facade
                or vars(raw_module).get("IntegratedV03Brain") is not raw
                or resources.facade_factory is not facade
                or vars(module).get("_LOCK_REGISTRY") is not resources.registry
                or vars(module).get("_LOCK_REGISTRY_GUARD") is not resources.guard):
            raise OwnershipError("verified resources differ from exact runtime module bindings")
        self.spec(facade)
        self.spec(raw)

    def spec(self, cls: type) -> TypeSpec:
        try:
            return self._specs[cls]
        except KeyError:
            raise OwnershipError(f"unregistered exact type: {cls.__module__}.{cls.__qualname__}") \
                from None


@dataclass(frozen=True)
class GraphSnapshot:
    """Reference graph and identity sets only; never retains source/candidate objects."""

    root: tuple
    nodes: tuple[tuple, ...]
    mutable_ids: frozenset[int]

    def equivalent(self, other: GraphSnapshot) -> bool:
        return self.root == other.root and self.nodes == other.nodes


@dataclass(frozen=True)
class ResourceLedger:
    """Controlled live base→lock identities, separate from computational graph values."""

    bindings: tuple[tuple[int, int], ...]


class SerialOwner:
    """One newly created, dedicated serial thread; no work runs on its caller thread."""

    def __init__(self) -> None:
        self._queue: queue.Queue = queue.Queue()
        self._thread = threading.Thread(target=self._loop, name="g0-source-only-owner")
        self._closed = False
        self._thread.start()

    def _loop(self) -> None:
        while True:
            job = self._queue.get()
            if job is None:
                return
            fn, args, kwargs, future = job
            try:
                value = fn(*args, **kwargs)
            except BaseException as exc:
                # Exceptions leaving a worker must not retain candidate locals via
                # tracebacks. The public error intentionally contains only text.
                message = f"{type(exc).__name__}: {exc}"
                exc.__traceback__ = None
                future.set_exception(OwnershipError(message))
                del message
            else:
                future.set_result(value)
                del value
            del job, fn, args, kwargs, future

    def assert_owner(self) -> None:
        if self._closed or threading.current_thread() is not self._thread:
            raise OwnershipError("operation requires the dedicated live owner thread")

    def call(self, fn: Callable, *args: Any, **kwargs: Any) -> Any:
        if self._closed:
            raise OwnershipError("owner thread is closed")
        if threading.current_thread() is self._thread:
            return fn(*args, **kwargs)
        future: Future = Future()
        self._queue.put((fn, args, kwargs, future))
        return future.result()

    def close(self) -> None:
        if threading.current_thread() is self._thread:
            raise OwnershipError("owner cannot join itself")
        if not self._closed:
            self._closed = True
            self._queue.put(None)
            self._thread.join()

    def __enter__(self) -> SerialOwner:
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()


def _probe_lock(lock: Any) -> None:
    if sys.implementation.name != "cpython" or type(lock) is not RLOCK_TYPE:
        raise OwnershipError("unsupported reentrant lock implementation")
    if not all(hasattr(RLOCK_TYPE, name) for name in ("_is_owned", "acquire", "release")):
        raise OwnershipError("required CPython lock API unavailable")
    if RLOCK_TYPE._is_owned(lock):
        raise OwnershipError("resource lock is already owned at quiescent boundary")
    if not RLOCK_TYPE.acquire(lock, blocking=False):
        raise OwnershipError("resource lock is held by another thread")
    RLOCK_TYPE.release(lock)


class ResourceBoundary:
    """Explicit registry/guard plus a reviewed facade reconstruction entry point.

    The registry must contain exactly the controlled graph's bases (or owner plus
    candidate during proof). The guard is acquired nonblocking before any registry
    read, and released on every path. This is a serial/quiescent boundary contract,
    not proof of arbitrary concurrent process behavior.
    """

    def __init__(
        self, owner: SerialOwner, registry: weakref.WeakKeyDictionary, guard: Any,
        *, raw_type: type, facade_type: type, facade_factory: Callable,
        factory_source_tag: str,
    ) -> None:
        owner.assert_owner()
        if type(registry) is not weakref.WeakKeyDictionary or type(guard) is not GUARD_TYPE:
            raise OwnershipError("exact weak registry and CPython guard required")
        if (facade_factory is not facade_type
                and type(facade_factory) is not types.FunctionType):
            raise OwnershipError("unreviewed facade factory type")
        if type(factory_source_tag) is not str or not factory_source_tag:
            raise OwnershipError("missing reviewed factory source tag")
        self.owner = owner
        self.registry = registry
        self.guard = guard
        self.raw_type = raw_type
        self.facade_type = facade_type
        self.facade_factory = facade_factory
        self.factory_source_tag = factory_source_tag
        self._candidate_stack: list[object] = []

    def ledger(self) -> ResourceLedger:
        self.owner.assert_owner()
        if (sys.implementation.name != "cpython"
                or type(self.registry) is not weakref.WeakKeyDictionary
                or type(self.guard) is not GUARD_TYPE):
            raise OwnershipError("resource boundary implementation changed")
        if not GUARD_TYPE.acquire(self.guard, blocking=False):
            raise OwnershipError("registry guard is not quiescent")
        try:
            rows: list[tuple[int, int]] = []
            for base, lock in self.registry.items():
                if type(base) is not self.raw_type:
                    raise OwnershipError("unexpected raw-base type in registry")
                _probe_lock(lock)
                rows.append((id(base), id(lock)))
            if len({lock for _, lock in rows}) != len(rows):
                raise OwnershipError("distinct bases share one resource lock")
            return ResourceLedger(tuple(sorted(rows)))
        finally:
            GUARD_TYPE.release(self.guard)

    def inspect(self, *walks: _Walk) -> ResourceLedger:
        expected: dict[int, int] = {}
        raw_ids: set[int] = set()
        for walk in walks:
            for value in walk.objects:
                if type(value) is self.raw_type:
                    raw_ids.add(id(value))
                if type(value) is self.facade_type:
                    fields = object.__getattribute__(value, "__dict__")
                    base, lock = fields["_brain"], fields["_step_lock"]
                    if type(base) is not self.raw_type or type(lock) is not RLOCK_TYPE:
                        raise OwnershipError("facade has wrong base or resource type")
                    if id(base) in expected and expected[id(base)] != id(lock):
                        raise OwnershipError("same base has inconsistent facade locks")
                    expected[id(base)] = id(lock)
        if set(expected) != raw_ids:
            raise OwnershipError("every controlled raw base must have a facade")
        actual = self.ledger()
        if actual.bindings != tuple(sorted(expected.items())):
            raise OwnershipError("missing, replaced, or unexpected live registry binding")
        return actual

    def verify_cleanup(self, baseline: ResourceLedger) -> None:
        self.owner.assert_owner()
        gc.collect()
        if self.ledger() != baseline:
            raise OwnershipError("candidate resource leak or baseline registry change")


def _atom(value: Any) -> tuple | None:
    cls = type(value)
    if value is None:
        return ("none",)
    if cls in (bool, int, str):
        return (cls.__name__, value)
    if cls is float:
        if not math.isfinite(value):
            raise OwnershipError("nonfinite float is outside the exact-hex domain")
        return ("float", value.hex())
    return None


def _key(value: Any) -> tuple:
    atom = _atom(value)
    if atom is not None:
        return atom
    if type(value) is tuple:
        return ("tuple", tuple(_key(child) for child in value))
    raise OwnershipError("unapproved dictionary key or set member")


def _rng_state(value: random.Random) -> tuple:
    def encode(child: Any) -> tuple:
        atom = _atom(child)
        if atom is not None:
            return atom
        if type(child) is tuple:
            return ("tuple", tuple(encode(item) for item in child))
        raise OwnershipError("unsupported Random.getstate representation")
    return encode(random.Random.getstate(value))


class _Walk:
    def __init__(
        self, root: Any, schema: SourceRegistry, resources: ResourceBoundary | None,
        *, max_nodes: int = 100_000, max_depth: int = 200,
    ) -> None:
        self.schema, self.resources = schema, resources
        self.max_nodes, self.max_depth = max_nodes, max_depth
        self.objects: list[Any] = []
        self.indices: dict[int, int] = {}
        self.nodes: list[tuple] = []
        self.mutable: set[int] = set()
        self.facade_dicts: set[int] = set()
        self.resource_dicts: set[int] = set()
        self.root = self.visit(root)
        if not self.resource_dicts <= self.facade_dicts:
            raise OwnershipError("resource handle outside an approved facade field")
        self.snapshot = GraphSnapshot(self.root, tuple(self.nodes), frozenset(self.mutable))

    def visit(self, value: Any, depth: int = 0, *, resource_edge: bool = False) -> tuple:
        atom = _atom(value)
        if atom is not None:
            return atom
        cls = type(value)
        if cls is RLOCK_TYPE and not resource_edge:
            raise OwnershipError("resource handle outside an approved facade field")
        if callable(value):
            raise OwnershipError("callable state is not eligible")
        if id(value) in self.indices:
            return ("ref", self.indices[id(value)])
        if depth > self.max_depth or len(self.nodes) >= self.max_nodes:
            raise OwnershipError("graph preflight bound exceeded")
        index = len(self.nodes)
        self.indices[id(value)] = index
        self.objects.append(value)
        self.nodes.append(())
        def child(item: Any) -> tuple:
            return self.visit(item, depth + 1)
        if cls is RLOCK_TYPE:
            node = ("resource", "CPython._thread.RLock")
        elif cls is dict:
            self.mutable.add(id(value))
            edges = []
            for key, item in value.items():
                _key(key)
                allowed = key == "_step_lock" and type(item) is RLOCK_TYPE
                if allowed:
                    self.resource_dicts.add(id(value))
                edges.append((child(key), self.visit(item, depth + 1, resource_edge=allowed)))
            node = ("dict", tuple(edges))
        elif cls in (list, tuple, deque):
            if cls is not tuple:
                self.mutable.add(id(value))
            node = (cls.__name__, value.maxlen if cls is deque else None,
                    tuple(child(item) for item in value))
        elif cls is set:
            self.mutable.add(id(value))
            node = ("set", tuple(child(item) for item in sorted(value, key=_key)))
        else:
            spec = self.schema.spec(cls)
            self.mutable.add(id(value))
            dictionary = None
            if spec.dict_fields is not None:
                dictionary = object.__getattribute__(value, "__dict__")
                if (type(dictionary) is not dict or any(type(k) is not str for k in dictionary)
                        or set(dictionary) != set(spec.dict_fields)):
                    raise OwnershipError(f"unexpected instance fields: {spec.source_tag}")
            if self.resources and cls is self.resources.facade_type:
                if set(spec.dict_fields or ()) != {"_brain", "_step_lock"} or spec.slot_fields:
                    raise OwnershipError("facade requires the exact two-field schema")
                self.facade_dicts.add(id(dictionary))
            slots = []
            for name in spec.slot_fields:
                descriptor = next(vars(base)[name] for base in cls.__mro__ if name in vars(base))
                if type(descriptor) is not types.MemberDescriptorType:
                    raise OwnershipError("slot has a non-storage descriptor")
                try:
                    item = descriptor.__get__(value, cls)
                except AttributeError:
                    raise OwnershipError(f"uninitialized required slot: {name}") from None
                slots.append((name, child(item)))
            state = _rng_state(value) if cls is random.Random else None
            dictionary_edge = child(dictionary) if dictionary is not None else None
            node = ("object", spec.source_tag, dictionary_edge, tuple(slots), state)
        self.nodes[index] = node
        return ("ref", index)


def capture_graph(
    root: Any, schema: SourceRegistry, resources: ResourceBoundary | None = None,
    *, retained_roots: tuple[Any, ...] = (),
) -> GraphSnapshot:
    """Preflight and inventory without copying, advancing RNG, or retaining graph refs."""
    if resources:
        resources.owner.assert_owner()
        schema.validate_resources(resources)
    if type(retained_roots) is not tuple:
        raise OwnershipError("retained_roots must be an explicit tuple")
    walk = _Walk(root, schema, resources)
    retained = tuple(_Walk(value, schema, resources) for value in retained_roots)
    if resources:
        resources.inspect(walk, *retained)
    return walk.snapshot


def _descendants(walk: _Walk, start: Any) -> set[int]:
    """Follow recorded references rather than accessing instance callbacks."""
    result: set[int] = set()

    def visit(token: Any) -> None:
        if type(token) is not tuple:
            return
        if len(token) == 2 and token[0] == "ref" and type(token[1]) is int:
            index = token[1]
            if index not in result:
                result.add(index)
                visit(walk.nodes[index])
        else:
            for item in token:
                visit(item)
    visit(("ref", walk.indices[id(start)]))
    return result


def _base_preflight(walk: _Walk, resources: ResourceBoundary) -> set[int]:
    early: set[int] = set()
    forbidden = {id(value) for value in walk.objects
                 if type(value) in (resources.facade_type, RLOCK_TYPE)} | walk.facade_dicts
    for base in walk.objects:
        if type(base) is resources.raw_type:
            reachable = _descendants(walk, base)
            if any(id(walk.objects[index]) in forbidden for index in reachable):
                raise OwnershipError(
                    "raw-base graph reaches a facade/resource before reconstruction")
            early.update(reachable)
    return early


def _construct(root: Any, walk: _Walk, resources: ResourceBoundary | None, early: set[int]) -> Any:
    memo: dict[int, Any] = {}
    regular: list[Any] = []
    facades: list[Any] = []
    try:
        # Seed exact-class shells before any descent. Generic object reducers,
        # __deepcopy__, __getattr__, and constructors never run on this path.
        for value in walk.objects:
            cls = type(value)
            if cls in (dict, list, tuple, set, deque, RLOCK_TYPE):
                continue
            if resources and cls is resources.facade_type:
                facades.append(value)
                continue
            if cls is random.Random:
                clone = random.Random(0)  # Explicit seed: no entropy read.
                random.Random.setstate(clone, random.Random.getstate(value))
            else:
                clone = object.__new__(cls)
            memo[id(value)] = clone
            regular.append(value)
            spec = walk.schema.spec(cls)
            if spec.dict_fields is not None:
                original_dict = object.__getattribute__(value, "__dict__")
                new_dict = memo.setdefault(id(original_dict), {})
                object.__setattr__(clone, "__dict__", new_dict)

        filled_dicts: set[int] = set()

        def fill(value: Any) -> None:
            clone, spec = memo[id(value)], walk.schema.spec(type(value))
            if spec.dict_fields is not None:
                original_dict = object.__getattribute__(value, "__dict__")
                if id(original_dict) not in filled_dicts:
                    target_dict = memo[id(original_dict)]
                    for key, item in original_dict.items():
                        target_dict[copy.deepcopy(key, memo)] = copy.deepcopy(item, memo)
                    filled_dicts.add(id(original_dict))
            for name in spec.slot_fields:
                item = object.__getattribute__(value, name)
                object.__setattr__(clone, name, copy.deepcopy(item, memo))

        for value in regular:
            if walk.indices[id(value)] in early:
                fill(value)
        if resources:
            for facade in facades:
                fields = object.__getattribute__(facade, "__dict__")
                base = memo[id(fields["_brain"])]
                clone = resources.facade_factory(base=base)
                if type(clone) is not resources.facade_type:
                    raise OwnershipError("factory returned an unapproved facade type")
                clone_fields = object.__getattribute__(clone, "__dict__")
                if (set(clone_fields) != {"_brain", "_step_lock"}
                        or clone_fields["_brain"] is not base):
                    raise OwnershipError("factory returned invalid facade fields")
                _probe_lock(clone_fields["_step_lock"])
                previous_lock = memo.setdefault(id(fields["_step_lock"]),
                                                clone_fields["_step_lock"])
                if previous_lock is not clone_fields["_step_lock"]:
                    raise OwnershipError("factory did not share locks for the same base")
                memo[id(facade)] = clone
                target_dict = memo.setdefault(id(fields), clone_fields)
                object.__setattr__(clone, "__dict__", target_dict)
                # Keep the real source insertion order, even if constructor order differs.
                target_dict.clear()
                for key, item in fields.items():
                    target_dict[key] = memo[id(item)]
                filled_dicts.add(id(fields))
        for value in regular:
            if walk.indices[id(value)] not in early:
                fill(value)
        return copy.deepcopy(root, memo)
    finally:
        # deepcopy's private keep-alive list and every candidate strong ref here
        # must disappear before weak-registry cleanup is judged.
        memo.clear()


class CloneCandidate:
    """An unpublished private candidate. Caller aliases must be dropped before discard."""

    def __init__(
        self, root: Any, source: GraphSnapshot, candidate: GraphSnapshot,
        resources: ResourceBoundary | None, baseline: ResourceLedger | None,
        candidate_resources: ResourceLedger | None,
    ) -> None:
        self.root = root
        self.source_graph = source
        self.candidate_graph = candidate
        self.resources = resources
        self.baseline_resources = baseline
        self.candidate_resources = candidate_resources
        self._disposed = False
        self._cleanup_token = object()
        if resources:
            resources._candidate_stack.append(self._cleanup_token)

    def discard_and_verify(self) -> None:
        """Dispose in reverse allocation order; reject wrong order before dropping refs."""
        if self.resources:
            self.resources.owner.assert_owner()
        if self._disposed:
            return
        if self.resources and (not self.resources._candidate_stack
                               or self.resources._candidate_stack[-1] is not self._cleanup_token):
            raise OwnershipError("candidate disposal requires reverse allocation order")
        self.root = None
        gc.collect()
        if self.resources:
            self.resources.verify_cleanup(self.baseline_resources)
            self.resources._candidate_stack.pop()
        self._disposed = True


def clone_joint(
    root: Any, schema: SourceRegistry, resources: ResourceBoundary | None = None,
    *, retained_roots: tuple[Any, ...] = (),
) -> CloneCandidate:
    """Preflight, reconstruct with one memo, and prove graph/isolation/resource checks.

    Declare every other live owner/candidate in ``retained_roots``. They are audited
    but never copied, and must be mutable-disjoint from each other and the source.
    Dispose resource candidates in reverse allocation order (checked before disposal).
    No publication or model transition occurs. On failure, internal candidate refs
    and tracebacks are discarded before checking that the weak registry returned to
    its baseline. This helper never removes registry entries directly.
    """
    if resources:
        resources.owner.assert_owner()
        schema.validate_resources(resources)
        facade_spec = schema.spec(resources.facade_type)
        schema.spec(resources.raw_type)
        if (set(facade_spec.dict_fields or ()) != {"_brain", "_step_lock"}
                or facade_spec.slot_fields):
            raise OwnershipError("facade requires the exact two-field schema")
    if type(retained_roots) is not tuple:
        raise OwnershipError("retained_roots must be an explicit tuple")
    before = _Walk(root, schema, resources)
    retained = tuple(_Walk(value, schema, resources) for value in retained_roots)
    protected_ids = set(before.snapshot.mutable_ids)
    for walk in retained:
        if protected_ids & walk.snapshot.mutable_ids:
            raise OwnershipError("declared live roots share mutable computational identities")
        protected_ids.update(walk.snapshot.mutable_ids)
    baseline = resources.inspect(before, *retained) if resources else None
    early = _base_preflight(before, resources) if resources else set()
    candidate = None
    after = None
    failure = None
    candidate_ledger = None
    unchanged = None
    retained_unchanged = None
    try:
        candidate = _construct(root, before, resources, early)
        after = _Walk(candidate, schema, resources)
        if not before.snapshot.equivalent(after.snapshot):
            raise OwnershipError("candidate canonical graph differs from source")
        if protected_ids & after.snapshot.mutable_ids:
            raise OwnershipError("candidate shares mutable computational identity")
        unchanged = _Walk(root, schema, resources)
        if (not before.snapshot.equivalent(unchanged.snapshot)
                or before.indices != unchanged.indices):
            raise OwnershipError("caller graph changed during reconstruction")
        retained_unchanged = tuple(_Walk(value, schema, resources) for value in retained_roots)
        for previous, current in zip(retained, retained_unchanged, strict=True):
            if (not previous.snapshot.equivalent(current.snapshot)
                    or previous.indices != current.indices):
                raise OwnershipError("retained graph changed during reconstruction")
        if resources:
            combined = resources.inspect(before, *retained, after)
            candidate_bindings = tuple(
                row for row in combined.bindings if row not in baseline.bindings)
            source_base_count = sum(type(value) is resources.raw_type for value in before.objects)
            if len(candidate_bindings) != source_base_count:
                raise OwnershipError("candidate resource cardinality differs from source")
            if {lock for _, lock in baseline.bindings} & {lock for _, lock in candidate_bindings}:
                raise OwnershipError("candidate reused owner synchronization resource")
            candidate_ledger = ResourceLedger(candidate_bindings)
    except BaseException as exc:
        failure = f"{type(exc).__name__}: {exc}"
        exc.__traceback__ = None
    if failure is not None:
        candidate = None
        after = None
        unchanged = None
        retained_unchanged = None
        gc.collect()
        if resources:
            try:
                resources.verify_cleanup(baseline)
            except OwnershipError as exc:
                raise OwnershipError(f"{failure}; cleanup failed: {exc}") from None
        raise OwnershipError(failure) from None
    return CloneCandidate(candidate, before.snapshot, after.snapshot, resources, baseline,
                          candidate_ledger)
