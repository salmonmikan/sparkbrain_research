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
