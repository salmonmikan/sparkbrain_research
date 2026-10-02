"""Exact synthetic wiring and source checks only: native execution remains prohibited."""
from __future__ import annotations

import ast
import copy
import importlib.abc
import json
import sys
from dataclasses import dataclass, make_dataclass
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]


class DenyModels(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "sparkbrain" or fullname.startswith("sparkbrain."):
            raise AssertionError("SparkBrain import forbidden during source-only tests")
        return None


# Block even collection-time imports; fixtures start too late to guard module loading.
_collection_blocker = DenyModels()
sys.meta_path.insert(0, _collection_blocker)
try:
    native = __import__("scripts.m1_path_native", fromlist=["NativeBackend"])
    adapt = __import__("scripts.m1_path_inputs", fromlist=["adapt"]).adapt
    pilot = __import__("scripts.m1_path_pilot", fromlist=["PathError", "canonical"])
    PathError, canonical = pilot.PathError, pilot.canonical
finally:
    sys.meta_path.remove(_collection_blocker)


@pytest.fixture(autouse=True)
def deny_model_imports():
    blocker = DenyModels()
    sys.meta_path.insert(0, blocker)
    yield
    sys.meta_path.remove(blocker)


def configuration_object(values):
    values = copy.deepcopy(values)
    for key in ("candidates", "ablations"):
        if key in values:
            values[key] = tuple(values[key])
    cls = make_dataclass("SyntheticConfiguration", [(key, object) for key in values])
    return cls(**values)


@dataclass
class Pulse:
    time_ms: float
    channel: str
    magnitude: float
    polarity: int
    location: object
    novelty: float
    prediction_error: float
    source_id: str
    metadata: dict

    def as_dict(self):
        return copy.deepcopy(vars(self))


@dataclass
class Observation:
    event_id: str
    time: float
    sensory_values: dict
    routing_features: tuple


@dataclass
class Receipt:
    receipt_id: str
    event_id: str
    outcome: float


class Result:
    def __init__(self, value):
        self.value = value

    def as_dict(self):
        return self.value


class Consumer:
    def __init__(self, defaults):
        self.calls = []
        self.outcomes = []
        self.predictive = SimpleNamespace(
            config=configuration_object(defaults["predictive"]),
            reference_brain=SimpleNamespace(_brain=SimpleNamespace(
                config=configuration_object(defaults["v03"]), _provided_revision_model=None)))
        scope = configuration_object(defaults["scope"])
        self.scoped = SimpleNamespace(config=scope, _router=SimpleNamespace(config=scope))
        self.output = {"event_id": "synthetic-native-1", "decision": "abstain",
                       "reason": "predictive_scope_disagreement", "prediction": 0.8,
                       "selected_state_id": "synthetic-state", "route_token": "synthetic-route",
                       "route_candidate": "beta"}

    def observe(self, observation):
        assert type(observation) is Observation
        self.calls.append(observation)
        return Result(self.output)

    def apply_outcome(self, receipt):
        assert type(receipt) is Receipt
        self.outcomes.append(receipt)
        return Result({"committed": True, "receipt_id": receipt.receipt_id})


def standin_backend():
    # Explicit test-only shell: constructor admission is never bypassed for native modules.
    backend = object.__new__(native.NativeBackend)
    backend.configuration = native.source_configuration(ROOT)
    backend.modules = {
        "sparkbrain.v04.contracts": SimpleNamespace(SignalPulse=Pulse),
        "sparkbrain.v05.assemblies": SimpleNamespace(pattern_similarity=object()),
        "sparkbrain.system_build.integrated_m1": SimpleNamespace(
            M1Observation=Observation, M1OutcomeReceipt=Receipt),
    }
    backend._graph_context = None
    backend._readbacks = {}
    return backend


def observation():
    return {"occurrence_id": "synthetic-native-1", "start_ms": 0.0,
            "pulses": [{"channel": channel, "time_ms": at, "magnitude": 1.0,
                        "polarity": 1, "location": None, "novelty": 0.0,
                        "prediction_error": 0.0, "source_id": "probe-input", "metadata": {}}
                       for channel, at in (("A", 0.0), ("C", 40.0))]}


def test_source_defaults_and_projection_provenance_are_separate():
    before = {name for name in sys.modules
              if name == "sparkbrain" or name.startswith("sparkbrain.")}
    frozen = native.source_configuration(ROOT)
    assert frozen["m1"]["v03"]["input_track"] == "I1_local_compositional"
    assert frozen["m1"]["v03"]["entity_track"] == "E0_global"
    assert frozen["m1"]["scope"]["max_components"] == 2
    assert frozen["m1"]["scope"]["maximum_dimensions"] == 8
    assert frozen["m1"]["predictive"]["max_context_scalars"] == 64
    assert frozen["producer"]["brain"]["topology_seed"] == 41
    for key in ("enable_prediction", "enable_action", "enable_reward_modulation"):
        assert frozen["producer"]["brain"][key] is False
    assert frozen["projection_origin_source_pin"] != frozen["execution_source_commit"]
    after = {name for name in sys.modules
             if name == "sparkbrain" or name.startswith("sparkbrain.")}
    assert after == before


def test_defaults_ast_rejects_factories_and_unknown_constants(tmp_path):
    path = tmp_path / "source.py"
    for expression in ("factory()", "UNKNOWN"):
        path.write_text(f"class Config:\n    number: int = {expression}\n")
        with pytest.raises(PathError, match="nonliteral"):
            native._ast_defaults(path, "Config")
    path.write_text("VALUE = 'literal'\nclass Config:\n    number: str = VALUE\n")
    assert native._ast_defaults(path, "Config") == {"number": "literal"}


def test_constructor_source_requires_sealed_gate_before_any_work():
    tree = ast.parse((ROOT / "scripts/m1_path_native.py").read_bytes())
    cls = next(row for row in tree.body if isinstance(row, ast.ClassDef)
               and row.name == "NativeBackend")
    init = next(row for row in cls.body if isinstance(row, ast.FunctionDef)
                and row.name == "__init__")
    assert isinstance(init.body[0], ast.ImportFrom)
    assert init.body[0].module == "scripts.m1_path_admission"
    assert ast.unparse(init.body[1]) == "require_permit(permit)"
    assert [arg.arg for arg in init.args.args] == ["self", "permit"]
    assert all(not isinstance(row, (ast.Import, ast.ImportFrom))
               or "sparkbrain" not in ast.unparse(row).lower() for row in tree.body)


def test_denied_permit_does_not_import_models(monkeypatch):
    from scripts import m1_path_admission

    calls = []
    def denied(permit):
        calls.append(permit)
        raise ValueError("synthetic gate denial")
    monkeypatch.setattr(m1_path_admission, "require_permit", denied)
    token = object()
    with pytest.raises(ValueError, match="synthetic gate denial"):
        native.NativeBackend(token)
    assert calls == [token]


def test_process_uses_detached_native_inputs_and_native_projection():
    backend = standin_backend()
    calls = []
    projected = {"features": [0.4], "binding": {"source_pin": native.PROJECTION_ORIGIN_SOURCE_PIN}}
    class Producer:
        def process_episode(self, pulses, **kwargs):
            calls.append((pulses, kwargs))
            result = Result({"raw": [1, 2]})
            result.end_ms = 72.0
            return result
    backend._export_native = lambda *args: (projected, {"matching": []})
    root = {"producer": Producer(), "dictionary": {"binding": {}}, "raw_history": []}
    external = observation()
    before = copy.deepcopy(external)
    acquired = backend.process(root, external, True)
    queried = backend.process(root, external, False)
    assert "export" not in acquired and queried["export"] == projected
    assert calls[0][1] == {"episode_id": external["occurrence_id"], "learn_assembly": True,
                          "learn_field": True, "explore_action": False, "metadata": {}}
    assert calls[1][1]["learn_assembly"] is calls[1][1]["learn_field"] is False
    calls[0][0][0].metadata["synthetic_mutation"] = [1]
    projected["features"].append(99)
    root["raw_history"][0]["pulses"][0]["metadata"]["synthetic_mutation"] = 2
    assert external == before and queried["export"]["features"] == [0.4]
    with pytest.raises(ValueError):
        backend.process(root, {**external, "start_ms": 1.0}, True)
    assert len(calls) == 2


def test_observe_wires_both_eight_dimensional_inlets_once_and_detaches_output():
    backend = standin_backend()
    consumer = Consumer(backend.configuration["m1"])
    root = {"m1": consumer}
    wire = adapt(observation(), [1., 0., 0., 0., 0., 0., 0.], [0., 1., 0., 0., 0., 0., 0.])
    original = copy.deepcopy(wire)
    output = backend.observe(root, wire)
    assert len(consumer.calls) == 1
    actual = consumer.calls[0]
    assert set(actual.sensory_values) == set(native.CHANNELS)
    assert len(actual.sensory_values) == len(actual.routing_features) == 8
    assert actual.sensory_values["signal"] == actual.routing_features[0] == 0.0
    assert actual.sensory_values["temporal_000"] == 1.0
    assert actual.routing_features[2] == 1.0
    assert output["predictive_choice"] == "alpha" and output["route_choice"] == "beta"
    assert output["final_action"] == "abstain"
    actual.sensory_values["temporal_000"] = 0.5
    consumer.output["decision"] = "act_alpha"
    assert wire == original and output["native_action"]["decision"] == "abstain"
    receipt = {"receipt_id": "synthetic-receipt", "event_id": wire["event_id"], "outcome": 0.8}
    assert backend.outcome(root, receipt)["committed"] is True
    assert len(consumer.outcomes) == 1


def test_capacity_and_wire_reject_before_native_observe():
    backend = standin_backend()
    consumer = Consumer(backend.configuration["m1"])
    root = {"m1": consumer}
    wire = adapt(observation(), [0.] * 7, [0.] * 7)
    for broken in (
        {**wire, "routing_features": [0.] * 9},
        {**wire, "sensory_values": {"signal": 0.0}},
        {**wire, "routing_features": [True, *([0.] * 7)]},
        {**wire, "routing_features": [0.5, *([0.] * 7)]},
    ):
        with pytest.raises(PathError):
            backend.observe(root, broken)
    consumer.scoped._router.config = copy.deepcopy(consumer.scoped.config)
    with pytest.raises(PathError, match="alias"):
        backend.observe(root, wire)
    assert not consumer.calls


def test_checkpoint_package_keeps_exact_bytes_without_decoding_native_json():
    # Deliberately not valid native JSON: packaging must never decode or rewrite it.
    files = {"reference-brain.json": b"\x00\xff untouched native bytes \n",
             "pilot-state.json": b'{ "keep": "original spacing" }\n'}
    payload = native.package_checkpoint(files)
    assert native.unpack_checkpoint(payload) == files
    malformed = json.loads(payload)
    malformed["files"]["unexpected"] = ""
    with pytest.raises(PathError):
        native.unpack_checkpoint(canonical(malformed))
    with pytest.raises(PathError, match="duplicate"):
        native.unpack_checkpoint(b'{"schema":1,"schema":1,"files":{}}')


def test_checkpoint_routes_once_each_then_disposes_and_removes_temp_files():
    backend = standin_backend()
    calls = []
    files = {"reference-brain.json": b'{"state":{}}\n', "pilot-state.json": b'{}\n'}
    sentinel = object()
    class Manager:
        BRAIN_FILE, PILOT_FILE = native.CHECKPOINT_FILES
        @staticmethod
        def save(predictive, directory):
            assert predictive is sentinel
            calls.append(("save", directory))
            directory.mkdir()
            for name, raw in files.items():
                (directory / name).write_bytes(raw)
        @staticmethod
        def load(directory):
            calls.append(("load", directory))
            assert {name: (directory / name).read_bytes() for name in files} == files
            return sentinel
    class Resources:
        def ledger(self):
            return ("synthetic-ledger",)
        def verify_cleanup(self, baseline):
            assert baseline == ("synthetic-ledger",)
            calls.append(("cleanup", None))
    backend.modules["sparkbrain.system_build.predictive_revision"] = SimpleNamespace(
        PilotCheckpointManager=Manager)
    backend._graph_context = (None, Resources(), lambda: ())
    payload = backend.save_predictive({"m1": SimpleNamespace(predictive=sentinel)})
    assert native.unpack_checkpoint(payload) == files
    restored = backend.load_predictive(payload)
    assert restored["predictive"] is sentinel
    assert restored["checkpoint_files_hex"] == {name: raw.hex() for name, raw in files.items()}
    assert not calls[0][1].exists() and not calls[1][1].exists()
    with pytest.raises(PathError, match="one live"):
        backend.load_predictive(payload)
    backend.dispose_readback(restored)
    assert restored == {} and not backend._readbacks
    assert [row[0] for row in calls] == ["save", "load", "cleanup"]


def test_compare_source_uses_full_census_and_tree_projection_not_extra_checkpoint():
    tree = ast.parse((ROOT / "scripts/m1_path_native.py").read_bytes())
    cls = next(row for row in tree.body if isinstance(row, ast.ClassDef)
               and row.name == "NativeBackend")
    method = next(row for row in cls.body if isinstance(row, ast.FunctionDef)
                  and row.name == "_compare_predictive")
    calls = [ast.unparse(node.func) for node in ast.walk(method) if isinstance(node, ast.Call)]
    assert "capture_graph" in calls and "codec._encode" in calls
    assert "candidate._checkpoint_payload" in calls
    assert not any(call.endswith((".save", ".load", "._load_bytes", "._decode")) for call in calls)


class SyntheticRaw:
    def __init__(self, data):
        self.data = data


class SyntheticFacade:
    def __init__(self, brain):
        self._brain = brain


class SyntheticPredictive:
    def __init__(self, data, payload):
        self.reference_brain = SyntheticFacade(SyntheticRaw(data))
        self.payload = payload

    def _checkpoint_payload(self):
        return copy.deepcopy(self.payload)


class SyntheticM1:
    def __init__(self, predictive):
        self.predictive = predictive


class SyntheticResources:
    facade_type = object  # Stand-ins contain no native locks/facades.
    owner = SimpleNamespace(assert_owner=lambda: None)

    def __init__(self):
        self.cleanups = 0

    def inspect(self, *walks):
        return self.ledger()

    def ledger(self):
        return ("synthetic",)

    def verify_cleanup(self, baseline):
        assert baseline == self.ledger()
        self.cleanups += 1


def comparison_fixture():
    from scripts.g0_joint_ownership import SourceRegistry, TypeSpec

    backend = standin_backend()
    registry = SourceRegistry((
        TypeSpec(SyntheticRaw, "synthetic:raw", ("data",)),
        TypeSpec(SyntheticFacade, "synthetic:facade", ("_brain",)),
        TypeSpec(SyntheticPredictive, "synthetic:predictive", ("reference_brain", "payload")),
        TypeSpec(SyntheticM1, "synthetic:m1", ("predictive",)),
    ))
    shared = [1., 2.]
    left = SyntheticPredictive({"left": shared, "right": shared}, {"pending": [0., 1.]})
    # JSON tree readback deliberately expands repeated aliases, just like native codec.
    right = SyntheticPredictive(json.loads(json.dumps(left.reference_brain._brain.data)),
                                copy.deepcopy(left.payload))
    right_data = right.reference_brain._brain.data
    assert right_data["left"] is not right_data["right"]
    files = {"reference-brain.json": canonical({"state": vars(left.reference_brain._brain)}),
             "pilot-state.json": canonical(left.payload)}
    restored = {"predictive": right,
                "checkpoint_files_hex": {name: raw.hex() for name, raw in files.items()}}
    root = {"m1": SyntheticM1(left)}
    resources = SyntheticResources()
    backend.configure_graph_context(registry, resources, lambda: (root, restored))
    backend._readbacks[id(restored)] = resources.ledger()
    backend.modules["sparkbrain.v032.checkpoint"] = SimpleNamespace(
        _encode=lambda value: json.loads(json.dumps(value)))
    return backend, root, restored, resources


def test_comparator_accepts_codec_tree_alias_expansion_and_rejects_state_loss():
    backend, root, restored, _ = comparison_fixture()
    backend.compare_predictive(root, restored)
    restored["predictive"].reference_brain._brain.data["left"].append(9.)
    with pytest.raises(PathError, match="complete raw-brain"):
        backend.compare_predictive(root, restored)
    backend.dispose_readback(restored)


def test_comparator_rejects_hidden_fields_shared_mutables_and_payload_drift():
    from scripts.g0_joint_ownership import OwnershipError

    backend, root, restored, _ = comparison_fixture()
    restored["predictive"].payload["pending"].append(9.)
    with pytest.raises(PathError, match="complete predictive"):
        backend.compare_predictive(root, restored)
    backend.dispose_readback(restored)
    backend, root, restored, _ = comparison_fixture()
    restored["predictive"].reference_brain._brain.extra = "synthetic-unknown-field"
    with pytest.raises(OwnershipError, match="unexpected instance fields"):
        backend.compare_predictive(root, restored)
    backend.dispose_readback(restored)
    backend, root, restored, _ = comparison_fixture()
    restored["predictive"].reference_brain._brain.data = (
        root["m1"].predictive.reference_brain._brain.data)
    with pytest.raises(PathError, match="shares mutable"):
        backend.compare_predictive(root, restored)
    backend.dispose_readback(restored)


def test_failed_native_load_cleans_temporary_files_and_checks_resource_baseline():
    backend = standin_backend()
    resources = SyntheticResources()
    paths = []
    class FailingManager:
        @staticmethod
        def load(path):
            paths.append(path)
            raise RuntimeError("synthetic decode failure")
    backend.modules["sparkbrain.system_build.predictive_revision"] = SimpleNamespace(
        PilotCheckpointManager=FailingManager)
    backend._graph_context = (None, resources, lambda: ())
    payload = native.package_checkpoint({name: b"{}\n" for name in native.CHECKPOINT_FILES})
    with pytest.raises(RuntimeError, match="synthetic decode failure"):
        backend.load_predictive(payload)
    assert resources.cleanups == 1 and not backend._readbacks
    assert len(paths) == 1 and not paths[0].exists()
