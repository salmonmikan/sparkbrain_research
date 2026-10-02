"""Only source-shaped stand-ins are executed; no model imports or native calls."""
from __future__ import annotations

import importlib.abc
import sys

import pytest

from scripts.m1_path_census import CensusError, PassiveCensus, source_functions


class Deny(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "sparkbrain" or fullname.startswith("sparkbrain."):
            raise AssertionError("native import forbidden")


@pytest.fixture(autouse=True)
def no_models(request):
    if sys.version_info >= (3, 14) and request.node.name != "test_unsupported_python_is_rejected":
        pytest.skip("prospective census is reviewed only on CPython 3.11 through 3.13")
    blocker = Deny()
    sys.meta_path.insert(0, blocker)
    yield
    sys.meta_path.remove(blocker)


class Budget:
    def check(self):
        return {}

    def poison(self, message):
        raise CensusError(message)


class Writer:
    def __init__(self):
        self.rows = []
        self.order = []

    def raw_json(self, name, row):
        self.rows.append((name, row))

    def raw_bytes(self, name, raw):
        self.order.append("preserved")
        self.rows.append((name, raw))


def source(root, path, text, namespace):
    file = root / path
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(text)
    exec(compile(text, str(file), "exec"), namespace)


def make(tmp_path, caps=None):
    writer = Writer()
    namespace = {"__name__": "sparkbrain.fixture", "order": writer.order}
    source(tmp_path, "src/sparkbrain/fixture.py", """
class Item:
    def __init__(self):
        self.value = 1
""", namespace)
    source(tmp_path, "scripts/g0_joint_ownership.py", """
def _construct(value):
    cls = type(value)
    clone = object.__new__(cls)
    clone.value = value.value
    return clone
""", namespace)
    source(tmp_path, "src/sparkbrain/v032/checkpoint.py", """
class DirectCheckpointManager:
    @staticmethod
    def _load_bytes(raw):
        order.append("decoded")
        return raw
""", namespace)
    files = ["src/sparkbrain/fixture.py", "scripts/g0_joint_ownership.py",
             "src/sparkbrain/v032/checkpoint.py"]
    targets = {"load": (files[2], "DirectCheckpointManager._load_bytes")}
    census = PassiveCensus(tmp_path, targets=targets, call_caps={"load": 1},
        type_caps=caps or {"sparkbrain.fixture:Item": {"init": 1, "shell": 1}},
        allowed_functions=source_functions(tmp_path, files), budget=Budget(), writer=writer)
    return census, namespace, writer


def test_init_and_shell_births_are_distinct_and_decoder_input_precedes_body(tmp_path):
    census, ns, writer = make(tmp_path)
    census.install()
    try:
        item = ns["Item"]()
        clone = ns["_construct"](item)
        assert clone is not item and clone.value == item.value
        assert ns["DirectCheckpointManager"]._load_bytes(b"fixture") == b"fixture"
    finally:
        census.close()
    snapshot = census.snapshot()
    assert snapshot["types"]["sparkbrain.fixture:Item"] == {
        "init": 1, "shell": 1, "init_return": 1, "shell_return": 1}
    assert snapshot["call_attempts"] == snapshot["call_returns"] == {"load": 1}
    assert snapshot["pending_calls"] == snapshot["pending_shells"] == 0
    assert writer.order == ["preserved", "decoded"]
    births = [row for _, row in writer.rows if type(row) is dict and row["kind"] == "type_birth"]
    assert [row["birth"] for row in births] == [1, 2]
    assert births[0]["runtime_id"] != births[1]["runtime_id"]


def test_type_ceiling_precedes_constructor_body_and_poison_is_terminal(tmp_path):
    census, ns, _ = make(tmp_path, {"sparkbrain.fixture:Item": {"init": 0, "shell": 0}})
    census.install()
    try:
        with pytest.raises(CensusError, match="type cap before allocation"):
            ns["Item"]()
    finally:
        census.close()
    assert census.failure
    assert census.snapshot()["types"]["sparkbrain.fixture:Item"]["init"] == 0


def test_unknown_type_fails_closed(tmp_path):
    census, ns, _ = make(tmp_path, {"sparkbrain.fixture:Other": {"init": 1, "shell": 1}})
    census.install()
    try:
        with pytest.raises(CensusError, match="unknown exact"):
            ns["Item"]()
    finally:
        census.close()


def test_missing_or_invalid_type_caps_never_install_hooks(tmp_path):
    with pytest.raises(ValueError, match="every admitted"):
        PassiveCensus(tmp_path, targets={}, call_caps={}, type_caps={},
                      allowed_functions=set(), budget=Budget(), writer=Writer())
    assert sys.getprofile() is None


def test_native_shaped_deepcopy_shell_cannot_bypass_zero_shell_cap(tmp_path):
    import copy
    census, ns, _ = make(tmp_path, {"sparkbrain.fixture:Item": {"init": 1, "shell": 0}})
    census.install()
    try:
        item = ns["Item"]()
        with pytest.raises(CensusError, match="copyreg native shell"):
            copy.deepcopy(item)
    finally:
        census.close()
    assert census.types["sparkbrain.fixture:Item"]["shell"] == 0
    assert census.types["sparkbrain.fixture:Item"]["init_return"] == 1


def test_predictive_rollback_file_bytes_precede_pilot_decoder_body(tmp_path):
    census, ns, writer = make(tmp_path)
    path = "src/sparkbrain/system_build/predictive_revision.py"
    source(tmp_path, path, """
class PilotCheckpointManager:
    @staticmethod
    def load(directory):
        order.append("pilot-decoded")
        return None
""", ns)
    census.allowed = frozenset((*census.allowed, (path, "PilotCheckpointManager.load")))
    census.budget.limits = {"output_bytes": 1024}
    census.budget.reserves = {"output_bytes": 128}
    census.budget.output_bytes = 0
    checkpoint = tmp_path / "checkpoint"
    checkpoint.mkdir()
    (checkpoint / "pilot-state.json").write_bytes(b'{"fixture":true}\n')
    census.install()
    try:
        ns["PilotCheckpointManager"].load(checkpoint)
    finally:
        census.close()
    assert writer.order == ["preserved", "pilot-decoded"]
    assert writer.rows[-1][1] == b'{"fixture":true}\n'


def test_inherited_c_constructor_is_excluded_before_native_shaped_call(tmp_path):
    writer = Writer()
    ns = {"__name__": "sparkbrain.fixture"}
    relative = "src/sparkbrain/fixture.py"
    source(tmp_path, relative, """
class Rejected(ValueError):
    pass

def rejected():
    raise Rejected("unobservable C constructor")
""", ns)
    census = PassiveCensus(tmp_path, targets={}, call_caps={},
        type_caps={"sparkbrain.fixture:Rejected": {"init": 0, "shell": 0}},
        allowed_functions=source_functions(tmp_path, [relative]), budget=Budget(), writer=writer)
    census.install()
    try:
        with pytest.raises(CensusError, match="inherited-C native constructor before call"):
            ns["rejected"]()
    finally:
        census.close()
    assert census.types["sparkbrain.fixture:Rejected"]["init"] == 0
    assert census.failure is not None


def test_source_shaped_strenum_import_initializers_are_counted(tmp_path):
    from enum import StrEnum
    writer = Writer()
    ns = {"__name__": "sparkbrain.fixture", "StrEnum": StrEnum}
    relative = "src/sparkbrain/fixture.py"
    path = tmp_path / relative
    path.parent.mkdir(parents=True)
    text = 'class Kind(StrEnum):\n    ONE = "one"\n    TWO = "two"\n'
    path.write_text(text)
    census = PassiveCensus(tmp_path, targets={}, call_caps={},
        type_caps={"sparkbrain.fixture:Kind": {"init": 2, "shell": 0}},
        allowed_functions=source_functions(tmp_path, [relative]), budget=Budget(), writer=writer)
    census.install()
    try:
        exec(compile(text, str(path), "exec"), ns)
    finally:
        census.close()
    assert census.types["sparkbrain.fixture:Kind"] == {
        "init": 2, "init_return": 2, "shell": 0, "shell_return": 0}
    routes = [row["route"] for _, row in writer.rows
              if type(row) is dict and row["kind"] == "type_birth"]
    assert routes == [["stdlib/enum.py", "Enum.__init__"]] * 2


def test_dataclass_generated_initializer_has_declared_source_route(tmp_path, monkeypatch):
    import dataclasses
    import types
    writer = Writer()
    module = types.ModuleType("sparkbrain.fixture")
    monkeypatch.setitem(sys.modules, module.__name__, module)
    ns = module.__dict__
    ns["dataclass"] = dataclasses.dataclass
    relative = "src/sparkbrain/fixture.py"
    source(tmp_path, relative, '@dataclass\nclass Data:\n    value: int = 1\n', ns)
    census = PassiveCensus(tmp_path, targets={}, call_caps={},
        type_caps={"sparkbrain.fixture:Data": {"init": 1, "shell": 0}},
        allowed_functions=source_functions(tmp_path, [relative]), budget=Budget(), writer=writer)
    census.install()
    try:
        ns["Data"]()
    finally:
        census.close()
    births = [row for _, row in writer.rows if row["kind"] == "type_birth"]
    assert len(births) == 1
    assert births[0]["route"] == [relative, "Data.__init__[dataclass-generated]"]
    assert births[0]["type"] == "sparkbrain.fixture:Data"


def test_unsupported_python_is_rejected(tmp_path, monkeypatch):
    import scripts.m1_path_census as module
    with monkeypatch.context() as patch:
        patch.setattr(module.sys, "version_info", (3, 14, 0))
        with pytest.raises(ValueError, match="CPython 3.11 through 3.13"):
            PassiveCensus(tmp_path, targets={}, call_caps={},
                          type_caps={"fixture:Type": {"init": 0, "shell": 0}},
                          allowed_functions=set(), budget=Budget(), writer=Writer())
    assert sys.getprofile() is None and sys.gettrace() is None


def feature_fixture(tmp_path, monkeypatch, *, method_body=None, shell_cap=2):
    """Synthetic class definitions at reviewed source-shaped paths; never native imports."""
    import copy
    import dataclasses
    import types

    writer = Writer()
    module = types.ModuleType("sparkbrain.v03_seed.sensory_field")
    monkeypatch.setitem(sys.modules, module.__name__, module)
    module.__dict__.update(copy=copy, dataclass=dataclasses.dataclass)
    relative = PassiveCensus.FEATURE_COPY[0]
    body = method_body or (
        "        working_states = copy.deepcopy(self._states)\n"
        "        return working_states\n")
    text = '''
@dataclass(slots=True)
class _FeatureState:
    prediction: float = 0.0
    variability: float = 1.0
    habituation: float = 0.0
    threshold: float = 0.90
    initialized: bool = False
    last_value: float = 0.0
    last_time: float = 0.0

class AdaptiveSensoryField:
    def __init__(self, states):
        self._states = states

    def observe_with_trace(self):
''' + body
    source(tmp_path, relative, text, module.__dict__)
    # Fixture construction is synthetic setup, outside the counted observation route.
    first = module._FeatureState()
    second = module._FeatureState(prediction=0.5)
    owner = module.AdaptiveSensoryField({"first": first, "alias": first, "second": second})
    census = PassiveCensus(tmp_path, targets={}, call_caps={},
        type_caps={PassiveCensus.FEATURE_TYPE: {"init": 0, "shell": shell_cap}},
        allowed_functions=source_functions(tmp_path, [relative]), budget=Budget(), writer=writer)
    return census, owner, module, writer


def test_feature_deepcopy_counts_shells_preserves_alias_and_detaches(tmp_path, monkeypatch):
    census, owner, _, writer = feature_fixture(tmp_path, monkeypatch)
    census.install()
    try:
        copied = owner.observe_with_trace()
    finally:
        census.close()
    assert copied is not owner._states
    assert copied["first"] is copied["alias"]
    assert copied["first"] is not owner._states["first"]
    assert copied["second"] is not owner._states["second"]
    copied["first"].prediction = 9.0
    assert owner._states["first"].prediction == 0.0
    assert census.types[PassiveCensus.FEATURE_TYPE] == {
        "init": 0, "init_return": 0, "shell": 2, "shell_return": 2}
    assert census.snapshot()["pending_calls"] == census.snapshot()["pending_shells"] == 0
    attempts = [row for _, row in writer.rows if row["kind"] == "type_attempt"]
    births = [row for _, row in writer.rows if row["kind"] == "type_birth"]
    assert [row["route"] for row in attempts] == [list(PassiveCensus.COPYREG_ROUTE)] * 2
    assert [row["route"] for row in births] == [list(PassiveCensus.COPYREG_ROUTE)] * 2
    assert all(row["allocation"] == "shell" for row in (*attempts, *births))
    assert attempts[0]["sequence"] < births[0]["sequence"] < attempts[1]["sequence"]
    assert sys.getprofile() is None and sys.gettrace() is None


def test_feature_deepcopy_zero_cap_blocks_before_shell_birth(tmp_path, monkeypatch):
    census, owner, _, _ = feature_fixture(tmp_path, monkeypatch, shell_cap=0)
    before = dict(owner._states)
    census.install()
    try:
        with pytest.raises(CensusError, match="type cap before allocation"):
            owner.observe_with_trace()
    finally:
        census.close()
    assert census.types[PassiveCensus.FEATURE_TYPE]["shell"] == 0
    assert census.types[PassiveCensus.FEATURE_TYPE]["shell_return"] == 0
    assert owner._states == before
    assert sys.getprofile() is None and sys.gettrace() is None


def test_feature_deepcopy_different_site_and_newobj_ex_still_denied(tmp_path, monkeypatch):
    import copy
    import copyreg
    census, owner, module, _ = feature_fixture(tmp_path, monkeypatch)
    census.install()
    try:
        with pytest.raises(CensusError, match="stdlib route|callsite"):
            copy.deepcopy(owner._states)
    finally:
        census.close()
    assert census.types[PassiveCensus.FEATURE_TYPE]["shell"] == 0
    # A separately installed fresh census tests the explicitly excluded allocator.
    census, _, module, _ = feature_fixture(tmp_path, monkeypatch)
    census.install()
    try:
        with pytest.raises(CensusError, match="copyreg native shell allocation"):
            copyreg.__newobj_ex__(module._FeatureState, (), {})
    finally:
        census.close()
    assert census.types[PassiveCensus.FEATURE_TYPE]["shell"] == 0


def feature_frames(census, owner, module):
    """Primitive source-shaped frames for hostile binding tests, no allocator invoked."""
    import copy
    import copyreg
    from types import SimpleNamespace

    feature = owner._states["first"]
    memo = {id(owner._states): {}}
    native = SimpleNamespace(f_code=module.AdaptiveSensoryField.observe_with_trace.__code__,
        f_globals=module.__dict__, f_locals={"self": owner}, f_lineno=census.feature_copy_line,
        f_back=None)
    locals_chain = [
        {"cls": module._FeatureState, "args": ()},
        {"x": feature, "memo": memo, "func": copyreg.__newobj__, "listiter": None,
         "dictiter": None, "state": (None, {name: getattr(feature, name)
                                             for name in census.FEATURE_SLOTS})},
        {"x": feature, "memo": memo},
        {"x": owner._states, "memo": memo},
        {"x": owner._states, "memo": memo},
    ]
    frames = []
    tail = native
    functions = (copyreg.__newobj__, copy._reconstruct, copy.deepcopy,
                 copy._deepcopy_dict, copy.deepcopy)
    for function, local in reversed(list(zip(functions, locals_chain, strict=True))):
        tail = SimpleNamespace(f_code=function.__code__, f_globals=function.__globals__,
                               f_locals=local, f_back=tail)
        frames.insert(0, tail)
    return frames, native


@pytest.mark.parametrize("mutation", [
    "memo", "root", "item", "caller_line", "caller_frame", "owner", "args",
    "func", "state", "class_binding", "hook", "thread",
])
def test_feature_copy_rejects_each_wrong_binding(tmp_path, monkeypatch, mutation):
    import copyreg
    from types import SimpleNamespace

    census, owner, module, _ = feature_fixture(tmp_path, monkeypatch)
    frames, caller = feature_frames(census, owner, module)
    if mutation == "memo":
        frames[1].f_locals["memo"] = dict(frames[1].f_locals["memo"])
    elif mutation == "root":
        frames[4].f_locals["x"] = dict(owner._states)
    elif mutation == "item":
        frames[2].f_locals["x"] = owner._states["second"]
    elif mutation == "caller_line":
        caller.f_lineno += 1
    elif mutation == "caller_frame":
        caller.f_code = feature_frames.__code__
    elif mutation == "owner":
        caller.f_locals["self"] = SimpleNamespace(_states=owner._states)
    elif mutation == "args":
        frames[0].f_locals["args"] = (1,)
    elif mutation == "func":
        frames[1].f_locals["func"] = copyreg.__newobj_ex__
    elif mutation == "state":
        frames[1].f_locals["state"][1]["prediction"] = 0.25
    elif mutation == "class_binding":
        monkeypatch.setattr(module, "_FeatureState", type("Other", (), {}))
    elif mutation == "hook":
        monkeypatch.setattr(module._FeatureState, "__reduce_ex__", lambda self, n: None)
    elif mutation == "thread":
        census.owner_thread -= 1
    cls = frames[0].f_locals["cls"]
    with pytest.raises(CensusError, match="copy|owner thread"):
        census._feature_copy_route(frames[0], cls)
    assert census.types[PassiveCensus.FEATURE_TYPE]["shell"] == 0
    assert not census.pending and not census.shells
    assert sys.getprofile() is None and sys.gettrace() is None


def test_feature_copy_partial_failure_counts_shells_and_restores_hooks(tmp_path, monkeypatch):
    census, owner, _, _ = feature_fixture(tmp_path, monkeypatch, shell_cap=1)
    originals = dict(owner._states)
    census.install()
    try:
        with pytest.raises(CensusError, match="type cap before allocation"):
            owner.observe_with_trace()
    finally:
        census.close()
    assert census.types[PassiveCensus.FEATURE_TYPE] == {
        "init": 0, "init_return": 0, "shell": 1, "shell_return": 1}
    assert owner._states == originals
    assert all(owner._states[name] is value for name, value in originals.items())
    assert sys.getprofile() is None and sys.gettrace() is None


def test_feature_copy_allocator_exception_keeps_attempt_without_birth(tmp_path, monkeypatch):
    import threading

    census, owner, module, writer = feature_fixture(tmp_path, monkeypatch)
    frames, _ = feature_frames(census, owner, module)
    frame = frames[0]
    frame.f_lasti = 0  # Synthetic unwinding event, not a RETURN instruction.
    census.charge_type(census.FEATURE_TYPE, "shell", census.COPYREG_ROUTE)
    census.pending[(threading.get_ident(), id(frame))] = [{
        "kind": "copyreg_shell", "name": census.FEATURE_TYPE,
        "route": census.COPYREG_ROUTE, "class_id": id(module._FeatureState),
        "original_id": id(owner._states["first"])}]
    census.profile(frame, "return", None)
    assert census.types[census.FEATURE_TYPE]["shell"] == 1
    assert census.types[census.FEATURE_TYPE]["shell_return"] == 0
    assert not census.pending
    assert writer.rows[-1][1]["kind"] == "type_exception"
    assert writer.rows[-1][1]["route"] == list(census.COPYREG_ROUTE)


@pytest.mark.parametrize("wrong_return", ["original", "foreign_type"])
def test_feature_copy_shell_return_must_be_exact_and_fresh(tmp_path, monkeypatch, wrong_return):
    import dis
    import threading

    census, owner, module, _ = feature_fixture(tmp_path, monkeypatch)
    frames, _ = feature_frames(census, owner, module)
    frame = frames[0]
    frame.f_lasti = next(row.offset for row in dis.get_instructions(frame.f_code)
                        if row.opname.startswith("RETURN_"))
    census.charge_type(census.FEATURE_TYPE, "shell", census.COPYREG_ROUTE)
    census.pending[(threading.get_ident(), id(frame))] = [{
        "kind": "copyreg_shell", "name": census.FEATURE_TYPE,
        "route": census.COPYREG_ROUTE, "class_id": id(module._FeatureState),
        "original_id": id(owner._states["first"])}]
    value = owner._states["first"] if wrong_return == "original" else object()
    with pytest.raises(CensusError, match="not exact fresh"):
        census.profile(frame, "return", value)
    assert census.types[census.FEATURE_TYPE]["shell"] == 1
    assert census.types[census.FEATURE_TYPE]["shell_return"] == 0
    assert not census.pending


def test_census_install_wrong_thread_leaves_all_hooks_unchanged(tmp_path, monkeypatch):
    import threading

    census, _, _, _ = feature_fixture(tmp_path, monkeypatch)
    owner_hooks = (sys.getprofile(), sys.gettrace(), threading.getprofile(), threading.gettrace())
    results = []
    def install_on_other_thread():
        before = (sys.getprofile(), sys.gettrace(), threading.getprofile(), threading.gettrace())
        try:
            census.install()
        except ValueError as error:
            results.append(str(error))
        else:
            results.append("unexpected installation")
        after = (sys.getprofile(), sys.gettrace(), threading.getprofile(), threading.gettrace())
        results.append(before == after)
    thread = threading.Thread(target=install_on_other_thread)
    thread.start()
    thread.join(timeout=5)
    assert not thread.is_alive()
    assert results == ["census installation requires its construction owner thread", True]
    assert not census.active and census._previous is None
    assert (sys.getprofile(), sys.gettrace(), threading.getprofile(), threading.gettrace()) == (
        owner_hooks)
    assert census.snapshot()["pending_calls"] == census.snapshot()["pending_shells"] == 0
    assert census.types[census.FEATURE_TYPE] == {
        "init": 0, "init_return": 0, "shell": 0, "shell_return": 0}
    # A rejected cross-thread attempt does not prevent legitimate owner installation.
    census.install()
    census.close()
    assert (sys.getprofile(), sys.gettrace(), threading.getprofile(), threading.gettrace()) == (
        owner_hooks)
