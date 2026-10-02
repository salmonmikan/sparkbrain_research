"""Model-free mechanics only: no SparkBrain import/construction or real G0 evidence."""
from __future__ import annotations

import os
import random
import subprocess
import sys
import threading
import weakref
from collections import OrderedDict, deque
from contextlib import contextmanager
from pathlib import Path
from types import MappingProxyType, ModuleType

import pytest

from scripts.g0_joint_ownership import (
    OwnershipError,
    ResourceBoundary,
    SerialOwner,
    SourceRegistry,
    TypeSpec,
    capture_graph,
    clone_joint,
)


class ModelFreeBox:
    def __init__(self, state):
        self.state = state

    def __deepcopy__(self, memo):
        raise AssertionError("custom copy must never run")

    def __reduce_ex__(self, protocol):
        raise AssertionError("custom reducer must never run")


class ModelFreeSlots:
    __slots__ = ("left", "right")


class ModelFreeMixed:
    __slots__ = ("slot", "__dict__")


class ModelFreeRaw:
    def __init__(self):
        self.history = [{"values": [1.0, -0.0]}]
        self.rng = random.Random(701)
        self.rng.gauss(0.0, 1.0)  # Leave a real cached Gaussian, model-free RNG only.


class ModelFreeField:
    def __init__(self):
        self.state = []

    def observe_with_trace(self):
        return None


def schema(*extra):
    return SourceRegistry((
        TypeSpec(ModelFreeBox, "synthetic:box", ("state",)),
        TypeSpec(ModelFreeSlots, "synthetic:slots", None, ("left", "right")),
        TypeSpec(ModelFreeMixed, "synthetic:mixed", ("field",), ("slot",)),
        TypeSpec(ModelFreeRaw, "synthetic:raw", ("history", "rng")),
        TypeSpec(ModelFreeField, "synthetic:field", ("state",)),
        TypeSpec(random.Random, "stdlib:Random:synthetic-test", ("gauss_next",)),
        *extra,
    ))


@contextmanager
def resource_fixture():
    with SerialOwner() as owner:
        registry = weakref.WeakKeyDictionary()
        guard = threading.Lock()
        modes = {"fail": False, "leak": False, "wrong_lock": False, "mutate": False,
                 "interrupt": False, "swap_target": None}
        leaks = []

        class ModelFreeFacade:
            def __init__(self, *, base):
                self._brain = base
                with guard:
                    self._step_lock = registry.get(base)
                    if self._step_lock is None:
                        self._step_lock = threading.RLock()
                        registry[base] = self._step_lock
                if modes["swap_target"] is not None:
                    modes["swap_target"]["twins"].reverse()
                    modes["swap_target"] = None
                if modes["wrong_lock"]:
                    self._step_lock = threading.RLock()
                if modes["mutate"]:
                    base.history.append("factory mutation")
                if modes["leak"]:
                    leaks.append(base)
                if modes["interrupt"]:
                    raise KeyboardInterrupt("model-free interrupted constructor")
                if modes["fail"]:
                    raise RuntimeError("model-free constructor fault after resource birth")

            def __getattr__(self, name):
                return getattr(self._brain, name)

        def setup():
            raw = ModelFreeRaw()
            first = ModelFreeFacade(base=raw)
            second = ModelFreeFacade(base=raw)
            contract = schema(TypeSpec(ModelFreeFacade, "synthetic:facade",
                                       ("_brain", "_step_lock")))
            boundary = ResourceBoundary(
                owner, registry, guard, raw_type=ModelFreeRaw, facade_type=ModelFreeFacade,
                facade_factory=ModelFreeFacade, factory_source_tag="synthetic:facade:constructor",
            )
            root = {"facade_dict": vars(first), "first": first, "second": second,
                    "raw": raw, "producer": ModelFreeBox(raw.history),
                    "raw_dict": vars(raw), "rng_dict": vars(raw.rng)}
            return root, contract, boundary

        root, contract, boundary = owner.call(setup)
        yield owner, root, contract, boundary, modes, leaks, ModelFreeFacade


def test_aliases_cycles_and_actual_instance_dictionary_nodes():
    box = ModelFreeBox([])
    box.state.extend([box, vars(box)])
    root = [vars(box), box, box.state, box]
    before = capture_graph(root, schema())
    candidate = clone_joint(root, schema())
    clone = candidate.root
    assert clone[0] is vars(clone[1])
    assert clone[1] is clone[3]
    assert clone[2] is clone[1].state
    assert clone[2][0] is clone[1]
    assert clone[2][1] is vars(clone[1])
    assert before.equivalent(candidate.candidate_graph)
    assert not before.mutable_ids & candidate.candidate_graph.mutable_ids
    clone[2].append("private")
    assert len(box.state) == 2
    assert capture_graph(root, schema()).equivalent(before)


def test_shared_instance_dictionary_is_preserved():
    left, right = ModelFreeBox([]), ModelFreeBox(None)
    right.__dict__ = left.__dict__
    candidate = clone_joint([left, right, vars(left)], schema())
    a, b, fields = candidate.root
    assert a is not b
    assert vars(a) is vars(b) is fields
    assert fields is not vars(left)


def test_slots_and_mixed_storage_are_disjoint_and_preserve_alias():
    slots = ModelFreeSlots()
    mixed = ModelFreeMixed()
    slots.left = slots.right = mixed
    mixed.slot = []
    mixed.field = mixed.slot
    clone = clone_joint([slots, mixed, vars(mixed)], schema()).root
    assert clone[0].left is clone[0].right is clone[1]
    assert clone[1].slot is clone[1].field
    assert clone[2] is vars(clone[1])
    assert clone[1].slot is not mixed.slot


def test_tuple_cycle_with_list_is_preserved():
    contents = []
    knot = (contents,)
    contents.append(knot)
    clone = clone_joint([knot, contents], schema()).root
    assert clone[0][0] is clone[1]
    assert clone[1][0] is clone[0]


def test_random_exact_state_gauss_cache_attrs_and_dictionary_alias(monkeypatch):
    rng = random.Random(45)
    rng.gauss(0.0, 1.0)
    rng.note = {"cached": rng.gauss_next}
    contract = SourceRegistry((TypeSpec(random.Random, "synthetic:random-extra",
                                       ("gauss_next", "note")),))
    state = rng.getstate()
    seeds = []
    original_seed = random.Random.seed

    def checked_seed(self, seed=None, version=2):
        seeds.append(seed)
        assert seed == 0, "cloning must not read OS entropy"
        return original_seed(self, seed, version)

    monkeypatch.setattr(random.Random, "seed", checked_seed)
    candidate = clone_joint([rng, vars(rng), rng.note], contract)
    clone, fields, note = candidate.root
    assert seeds == [0]
    assert rng.getstate() == state == clone.getstate()
    assert vars(clone) is fields and clone.note is note
    assert vars(clone) is not vars(rng)
    assert clone.gauss_next is not None
    # Calling the candidate cannot advance the caller's RNG.
    clone.gauss(0.0, 1.0)
    clone.random()
    assert rng.getstate() == state


def test_typed_scalars_container_distinctions_order_and_signed_zero():
    contract = schema()
    values = [None, False, 0, "0", 0.0, -0.0, ["x"], ("x",),
              {"x"}, deque(["x"], maxlen=7), {(None, "x"), ("None", "x")},
              {"b": 1, "a": 2}]
    result = clone_joint(values, contract)
    assert result.source_graph.equivalent(result.candidate_graph)
    assert result.root[9].maxlen == 7
    assert tuple(result.root[-1]) == ("b", "a")
    for a, b in [(False, 0), (0, 0.0), (0.0, -0.0), ([1], (1,)),
                 (deque([1], maxlen=2), deque([1], maxlen=3)),
                 ({"a": 1, "b": 2}, {"b": 2, "a": 1})]:
        assert not capture_graph(a, contract).equivalent(capture_graph(b, contract))


@pytest.mark.parametrize("bad", [OrderedDict(), MappingProxyType({}), frozenset(), object(),
                                 lambda: None, float("nan"), float("inf")])
def test_unknown_mapping_types_callables_and_nonfinite_values_reject(bad):
    with pytest.raises(OwnershipError):
        clone_joint({"bad": bad}, schema())


def test_unknown_subclass_and_extra_missing_fields_reject():
    class Derived(ModelFreeBox):
        pass
    for value in (Derived([]), ModelFreeBox([]), ModelFreeBox([])):
        if type(value) is ModelFreeBox:
            if "state" in vars(value):
                value.extra = 1
        with pytest.raises(OwnershipError):
            clone_joint(value, schema())
    missing = ModelFreeBox([])
    del missing.state
    with pytest.raises(OwnershipError, match="fields"):
        clone_joint(missing, schema())


def test_transient_observe_with_trace_callback_is_rejected():
    field = ModelFreeField()
    field.observe_with_trace = lambda: None
    with pytest.raises(OwnershipError, match="fields"):
        clone_joint(field, schema())


def test_invalid_slot_schema_uninitialized_slot_and_source_runtime_rejected():
    with pytest.raises(OwnershipError, match="slot schema"):
        SourceRegistry((TypeSpec(ModelFreeSlots, "bad", None, ("left",)),))
    slot = ModelFreeSlots()
    slot.left = 1
    with pytest.raises(OwnershipError, match="uninitialized"):
        clone_joint(slot, schema())
    pretended_runtime = type("NotARealRuntime", (), {"__module__": "sparkbrain.synthetic_test"})
    with pytest.raises(OwnershipError, match="verified-source binder"):
        SourceRegistry((TypeSpec(pretended_runtime, "mere-label", ()),))


def test_facade_raw_rng_shared_memo_and_resource_equivalence():
    with resource_fixture() as (owner, root, contract, boundary, _, _, _):
        before = owner.call(capture_graph, root, contract, boundary)
        candidate = owner.call(clone_joint, root, contract, boundary)
        clone = candidate.root
        assert clone["first"]._brain is clone["second"]._brain is clone["raw"]
        assert clone["first"]._step_lock is clone["second"]._step_lock
        assert clone["first"]._step_lock is not root["first"]._step_lock
        assert clone["producer"].state is clone["raw"].history
        assert clone["raw_dict"] is vars(clone["raw"])
        assert clone["facade_dict"] is vars(clone["first"])
        assert clone["rng_dict"] is vars(clone["raw"].rng)
        assert before.equivalent(candidate.candidate_graph)
        assert len(owner.call(boundary.ledger).bindings) == 2
        assert candidate.baseline_resources.bindings != candidate.candidate_resources.bindings
        del clone
        owner.call(candidate.discard_and_verify)
        assert len(owner.call(boundary.ledger).bindings) == 1
        assert before.equivalent(owner.call(capture_graph, root, contract, boundary))


def test_complete_graph_preflight_precedes_factory_and_does_not_mutate():
    with resource_fixture() as (owner, root, contract, boundary, modes, _, _):
        root["late_unknown"] = object()
        modes["fail"] = True
        baseline = owner.call(boundary.ledger)
        with pytest.raises(OwnershipError, match="unregistered"):
            owner.call(clone_joint, root, contract, boundary)
        assert owner.call(boundary.ledger) == baseline


@pytest.mark.parametrize("kind", ["missing", "replaced", "unexpected", "duplicate", "wrong_type"])
def test_resource_inventory_rejects_corruption(kind):
    with resource_fixture() as (owner, root, contract, boundary, _, _, facade_type):
        retained = []

        def corrupt():
            raw = root["raw"]
            if kind == "missing":
                del boundary.registry[raw]  # Test adversary, never the cleanup helper.
            elif kind == "replaced":
                boundary.registry[raw] = threading.RLock()
            elif kind in ("unexpected", "duplicate"):
                extra = ModelFreeRaw()
                retained.append(extra)
                facade_type(base=extra)
                if kind == "duplicate":
                    boundary.registry[extra] = boundary.registry[raw]
            else:
                boundary.registry[raw] = threading.Lock()

        owner.call(corrupt)
        with pytest.raises(OwnershipError):
            owner.call(clone_joint, root, contract, boundary)


def test_same_base_facades_with_different_locks_reject():
    with resource_fixture() as (owner, root, contract, boundary, _, _, _):
        root["second"]._step_lock = threading.RLock()
        with pytest.raises(OwnershipError, match="inconsistent facade locks"):
            owner.call(clone_joint, root, contract, boundary)


def test_lock_in_unapproved_graph_position_rejects_even_if_already_seen():
    with resource_fixture() as (owner, root, contract, boundary, _, _, _):
        root["leaked_lock"] = root["first"]._step_lock
        with pytest.raises(OwnershipError, match="outside"):
            owner.call(clone_joint, root, contract, boundary)


def test_locked_resources_wrong_thread_and_guard_probes_are_balanced():
    with resource_fixture() as (owner, root, contract, boundary, _, _, _):
        with pytest.raises(OwnershipError, match="owner thread"):
            clone_joint(root, contract, boundary)
        lock = root["first"]._step_lock

        def locked_here():
            with lock:
                with pytest.raises(OwnershipError, match="already owned"):
                    clone_joint(root, contract, boundary)
                assert lock._is_owned()

        owner.call(locked_here)
        with lock:
            with pytest.raises(OwnershipError, match="another thread"):
                owner.call(clone_joint, root, contract, boundary)
        with boundary.guard:
            with pytest.raises(OwnershipError, match="guard is not quiescent"):
                owner.call(clone_joint, root, contract, boundary)
        owner.call(boundary.ledger)
        assert boundary.guard.acquire(blocking=False)
        boundary.guard.release()
        assert lock.acquire(blocking=False)
        lock.release()


def test_guard_released_after_inventory_failure_and_exact_resource_types():
    with resource_fixture() as (owner, root, _, boundary, _, _, _):
        boundary.registry[root["raw"]] = threading.Lock()
        with pytest.raises(OwnershipError):
            owner.call(boundary.ledger)
        assert boundary.guard.acquire(blocking=False)
        boundary.guard.release()
        boundary.guard = threading.RLock()
        with pytest.raises(OwnershipError, match="implementation changed"):
            owner.call(boundary.ledger)


def test_raw_to_facade_cycle_is_rejected_before_factory():
    with resource_fixture() as (owner, root, contract, boundary, modes, _, _):
        root["raw"].history.append(root["first"])
        modes["fail"] = True
        with pytest.raises(OwnershipError, match="raw-base graph reaches"):
            owner.call(clone_joint, root, contract, boundary)


@pytest.mark.parametrize("mode", ["fail", "wrong_lock", "mutate"])
def test_failed_clone_cleans_resources_and_preserves_owner(mode):
    with resource_fixture() as (owner, root, contract, boundary, modes, _, _):
        before = owner.call(capture_graph, root, contract, boundary)
        baseline = owner.call(boundary.ledger)
        modes[mode] = True
        with pytest.raises(OwnershipError) as caught:
            owner.call(clone_joint, root, contract, boundary)
        assert "cleanup failed" not in str(caught.value)
        assert owner.call(boundary.ledger) == baseline
        assert before.equivalent(owner.call(capture_graph, root, contract, boundary))


def test_failed_factory_external_leak_fails_closed_until_caller_releases():
    with resource_fixture() as (owner, root, contract, boundary, modes, leaks, _):
        baseline = owner.call(boundary.ledger)
        modes.update(fail=True, leak=True)
        with pytest.raises(OwnershipError, match="cleanup failed"):
            owner.call(clone_joint, root, contract, boundary)
        assert len(owner.call(boundary.ledger).bindings) == 2
        leaks.clear()
        owner.call(boundary.verify_cleanup, baseline)


def test_discard_checks_external_alias_and_does_not_retain_via_reports():
    with resource_fixture() as (owner, root, contract, boundary, _, _, _):
        candidate = owner.call(clone_joint, root, contract, boundary)
        leaked = candidate.root["raw"]
        reference = weakref.ref(leaked)
        report = (candidate.candidate_graph, candidate.candidate_resources)
        with pytest.raises(OwnershipError, match="resource leak"):
            owner.call(candidate.discard_and_verify)
        del leaked
        owner.call(candidate.discard_and_verify)
        assert reference() is None
        assert report[0].nodes and report[1].bindings


def test_replacement_facade_birth_and_held_traceback_cleanup():
    with resource_fixture() as (owner, root, contract, boundary, _, _, facade_type):
        candidate = owner.call(clone_joint, root, contract, boundary)
        held = []

        def replace_then_fail():
            try:
                old_base = candidate.root["raw"]
                new_base = ModelFreeRaw()
                candidate.root["replacement"] = facade_type(base=new_base)
                raise RuntimeError("simulated candidate replacement failure")
            except RuntimeError as exc:
                held.append(exc)
                assert old_base is not new_base

        owner.call(replace_then_fail)
        assert len(owner.call(boundary.ledger).bindings) == 3
        with pytest.raises(OwnershipError, match="resource leak"):
            owner.call(candidate.discard_and_verify)
        held.clear()
        owner.call(candidate.discard_and_verify)
        assert len(owner.call(boundary.ledger).bindings) == 1


def test_constructor_reordering_still_preserves_actual_facade_dict_order():
    with resource_fixture() as (owner, root, contract, boundary, _, _, _):
        fields = vars(root["first"])
        base = fields.pop("_brain")
        fields["_brain"] = base
        candidate = owner.call(clone_joint, root, contract, boundary)
        assert tuple(vars(candidate.root["first"])) == ("_step_lock", "_brain")
        owner.call(candidate.discard_and_verify)


def test_subprocess_blocks_all_sparkbrain_imports():
    repo = Path(__file__).resolve().parents[1]
    script = '''
import importlib.abc
import sys
class Block(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "sparkbrain" or fullname.startswith("sparkbrain."):
            raise AssertionError("forbidden real runtime import")
sys.meta_path.insert(0, Block())
from scripts.g0_joint_ownership import SourceRegistry, clone_joint
result = clone_joint({"model_free": [1, -0.0, (None, "x")]}, SourceRegistry(()))
assert result.root["model_free"][0] == 1
assert not any(n == "sparkbrain" or n.startswith("sparkbrain.") for n in sys.modules)
'''
    result = subprocess.run([sys.executable, "-B", "-c", script], cwd=repo,
                            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                            capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("kind", ["rng", "duplicate_slots", "inherited_dict", "custom_new"])
def test_hidden_or_inherited_storage_classes_are_rejected_without_getters(kind):
    called = []

    class RandomChild(random.Random):
        pass

    class FirstSlots:
        __slots__ = ("x",)

    class DuplicateSlots(FirstSlots):
        __slots__ = ("x",)

    class DictProperty:
        @property
        def __dict__(self):
            called.append("getter called")
            return {}

    class InheritedDictionary(DictProperty):
        pass

    class CustomAllocation:
        def __new__(cls):
            return object.__new__(cls)

    bad, fields, slots = {
        "rng": (RandomChild, ("gauss_next",), ()),
        "duplicate_slots": (DuplicateSlots, None, ("x",)),
        "inherited_dict": (InheritedDictionary, (), ()),
        "custom_new": (CustomAllocation, (), ()),
    }[kind]
    with pytest.raises(OwnershipError):
        SourceRegistry((TypeSpec(bad, "synthetic:invalid", fields, slots),))
    assert not called


def test_interrupted_factory_performs_cleanup_proof(monkeypatch):
    with resource_fixture() as (owner, root, contract, boundary, modes, _, _):
        verified = []
        original = boundary.verify_cleanup

        def checked_cleanup(baseline):
            original(baseline)
            verified.append(True)

        monkeypatch.setattr(boundary, "verify_cleanup", checked_cleanup)
        modes["interrupt"] = True
        with pytest.raises(OwnershipError, match="KeyboardInterrupt"):
            owner.call(clone_joint, root, contract, boundary)
        assert verified == [True]
        assert len(owner.call(boundary.ledger).bindings) == 1


def test_verified_source_binder_does_not_load_runtime_and_rejects_unknown_classes():
    repo = Path(__file__).resolve().parents[1]
    before = set(sys.modules)
    bound = SourceRegistry.from_verified_source(repo, (random.Random,))
    assert bound.domain == "VERIFIED_SOURCE_PREPARATION"
    assert bound.spec(random.Random).dict_fields == ("gauss_next",)
    assert not any(name.startswith("sparkbrain") for name in set(sys.modules) - before)
    with pytest.raises(OwnershipError, match="absent from the pinned source contract"):
        SourceRegistry.from_verified_source(repo, (ModelFreeBox,))


def test_verified_source_binder_rejects_tampered_contract(tmp_path):
    from scripts.verify_g0_joint_source_contract import CONTRACT

    target = tmp_path / CONTRACT
    target.parent.mkdir(parents=True)
    target.write_text('{"not": "a real contract"}')
    with pytest.raises(OwnershipError, match="digest mismatch"):
        SourceRegistry.from_verified_source(tmp_path, ())


def test_verified_source_mode_rejects_lookalike_registry_binding():
    repo = Path(__file__).resolve().parents[1]
    bound = SourceRegistry.from_verified_source(repo, ())
    with resource_fixture() as (owner, root, _, boundary, _, _, _):
        with pytest.raises(OwnershipError, match="exact runtime module bindings"):
            owner.call(clone_joint, root, bound, boundary)


@pytest.mark.parametrize("kind", ["not_class", "missing_module", "wrong_identity", "nested_name",
                                 "wrong_path"])
def test_verified_source_binder_rejects_loaded_identity_impostors(kind, monkeypatch, tmp_path):
    # These are metadata-only impostors, never imported/executed production classes.
    repo = Path(__file__).resolve().parents[1]
    module_name = "sparkbrain.v032.runtime"
    impostor = type("IntegratedV032Brain", (), {"__module__": module_name})
    module = ModuleType(module_name)
    module.IntegratedV032Brain = impostor
    other_source = tmp_path / "model_free_impostor.py"
    other_source.write_text("# Model-free metadata impostor only\n")
    module.__file__ = str(other_source)
    monkeypatch.setitem(sys.modules, module_name, module)
    loaded = impostor
    if kind == "not_class":
        loaded = object()
    elif kind == "missing_module":
        monkeypatch.delitem(sys.modules, module_name)
    elif kind == "wrong_identity":
        module.IntegratedV032Brain = object()
    elif kind == "nested_name":
        impostor.__qualname__ = "Outer.IntegratedV032Brain"
    with pytest.raises(OwnershipError):
        SourceRegistry.from_verified_source(repo, (loaded,))


def test_no_unapproved_guard_or_registry_class_and_balanced_wrong_guard():
    class WeakSubclass(weakref.WeakKeyDictionary):
        pass

    with resource_fixture() as (owner, root, _, boundary, _, _, facade_type):
        for registry, guard in ((WeakSubclass(), threading.Lock()),
                                (weakref.WeakKeyDictionary(), threading.RLock())):
            with pytest.raises(OwnershipError, match="exact weak registry"):
                owner.call(ResourceBoundary, owner, registry, guard,
                           raw_type=type(root["raw"]), facade_type=facade_type,
                           facade_factory=facade_type, factory_source_tag="synthetic")
        boundary.registry = WeakSubclass()
        with pytest.raises(OwnershipError, match="implementation changed"):
            owner.call(boundary.ledger)



def test_multiple_candidates_declared_roots_pairwise_isolation_and_lifo_cleanup():
    with resource_fixture() as (owner, root, contract, boundary, _, _, _):
        first = owner.call(clone_joint, root, contract, boundary)
        with pytest.raises(OwnershipError, match="unexpected live registry binding"):
            owner.call(clone_joint, root, contract, boundary)
        second = owner.call(clone_joint, root, contract, boundary,
                            retained_roots=(first.root,))
        assert len(owner.call(boundary.ledger).bindings) == 3
        assert not first.candidate_graph.mutable_ids & second.candidate_graph.mutable_ids
        assert not second.candidate_graph.mutable_ids & first.source_graph.mutable_ids
        first_root_ref = weakref.ref(first.root["raw"])
        with pytest.raises(OwnershipError, match="reverse allocation order"):
            owner.call(first.discard_and_verify)
        assert first.root is not None and first_root_ref() is not None
        captured = owner.call(capture_graph, second.root, contract, boundary,
                              retained_roots=(root, first.root))
        assert captured.equivalent(second.candidate_graph)
        owner.call(second.discard_and_verify)
        assert len(owner.call(boundary.ledger).bindings) == 2
        owner.call(first.discard_and_verify)
        assert len(owner.call(boundary.ledger).bindings) == 1


def test_clone_new_owner_with_predecessor_retained():
    with resource_fixture() as (owner, root, contract, boundary, _, _, _):
        next_owner = owner.call(clone_joint, root, contract, boundary)
        later = owner.call(clone_joint, next_owner.root, contract, boundary,
                           retained_roots=(root,))
        assert later.source_graph.equivalent(next_owner.candidate_graph)
        assert len(later.candidate_resources.bindings) == 1
        owner.call(later.discard_and_verify)
        owner.call(next_owner.discard_and_verify)


def test_retained_root_schema_and_overlap_are_preflighted():
    with resource_fixture() as (owner, root, contract, boundary, modes, _, _):
        modes["fail"] = True
        with pytest.raises(OwnershipError, match="unregistered"):
            owner.call(clone_joint, root, contract, boundary, retained_roots=(object(),))
        with pytest.raises(OwnershipError, match="share mutable"):
            owner.call(clone_joint, root, contract, boundary, retained_roots=(root,))
        assert len(owner.call(boundary.ledger).bindings) == 1


def test_failed_clone_restores_declared_multiple_live_root_baseline():
    with resource_fixture() as (owner, root, contract, boundary, modes, _, _):
        retained = owner.call(clone_joint, root, contract, boundary)
        baseline = owner.call(boundary.ledger)
        modes["fail"] = True
        with pytest.raises(OwnershipError, match="constructor fault"):
            owner.call(clone_joint, root, contract, boundary, retained_roots=(retained.root,))
        assert owner.call(boundary.ledger) == baseline
        owner.call(retained.discard_and_verify)



@pytest.mark.parametrize("target_kind", ["source", "retained"])
def test_noninterference_rejects_symmetric_mutable_identity_swap(target_kind):
    with resource_fixture() as (owner, root, contract, boundary, modes, _, _):
        root["twins"] = [[1], [1]]
        retained = None
        if target_kind == "retained":
            retained = owner.call(clone_joint, root, contract, boundary)
        target = root if retained is None else retained.root
        first_identity = id(target["twins"][0])
        modes["swap_target"] = target
        with pytest.raises(OwnershipError, match="graph changed during reconstruction"):
            owner.call(clone_joint, root, contract, boundary,
                       retained_roots=() if retained is None else (retained.root,))
        assert id(target["twins"][0]) != first_identity
        assert target["twins"] == [[1], [1]]
        if retained is not None:
            del target
            owner.call(retained.discard_and_verify)
