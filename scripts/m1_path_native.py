"""Dormant native adapter for the prospective PR188 path pilot.

SOURCE-ONLY / UNEXECUTED / NON_EVIDENTIARY. The constructor's first operation is
sealed admission. Importing this module or reading its configuration never imports
SparkBrain. There is no CLI, execution switch, synthetic permit, or seed search.

PR182's dictionary ``source_pin`` identifies the historical projection definition,
not this execution's source. It is deliberately unchanged. ``execution_source_commit``
is a separate binding to the repaired runtime; admission binds its complete sources.

Predictive checkpoint readback is a compatibility test, NOT an alias-preserving joint
clone. The native codec writes a value tree: repeated references are expanded and
mapping keys sorted. Comparison checks the complete raw-brain native codec tree,
the complete predictive payload, exact-type graph census and cross-owner isolation.
The schedule's independent full joint graph oracle retains alias and mapping-order
requirements for producer, M1 coordinator, router, pending bindings and receipt ledger.
"""
from __future__ import annotations

import ast
import base64
import dataclasses
import hashlib
import importlib
import importlib.machinery
import json
import math
import random
import re
import sys
from collections.abc import Callable
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from scripts.g0_joint_ownership import capture_graph
from scripts.m1_path_inputs import validate_observation
from scripts.m1_path_pilot import PathError, canonical, detach, require

EXECUTION_SOURCE_COMMIT = "46bbd9b8b28c2404c73f028f8736ed83c3b5c3fe"
PROJECTION_ORIGIN_SOURCE_PIN = "9b1179aa18060436e4a05f2ff21f4cffc098f79d"
PR182_PROTOCOL = "artifacts/research/v05_history_export_20261002/protocol.json"
PR182_PROTOCOL_SHA256 = "48b2925fac2fb56200e59a9fb88df60c18868d5553e4390fe6c47864b6ac9c82"
CHECKPOINT_FILES = ("reference-brain.json", "pilot-state.json")
CHECKPOINT_SCHEMA = "m1-path-native-predictive-package-v1"
CHANNELS = ("signal", *(f"temporal_{index:03d}" for index in range(7)))
M1_CONFIG_TYPES = {
    "v03": ("v03/runtime.py", "V03BrainConfig"),
    "predictive": ("system_build/predictive_revision.py", "PilotConfig"),
    "scope": ("system_build/causal_scope_revision.py", "ScopeRevisionConfig"),
}


def _ast_defaults(path: Path, class_name: str) -> dict:
    """Literal declarations only; reject expressions/factories instead of executing."""
    tree = ast.parse(path.read_bytes())
    constants = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            try:
                value = ast.literal_eval(node.value)
            except (ValueError, TypeError):
                continue
            for target in node.targets:
                if isinstance(target, ast.Name):
                    constants[target.id] = value
    classes = [node for node in tree.body
               if isinstance(node, ast.ClassDef) and node.name == class_name]
    require(len(classes) == 1, "configuration declaration missing or ambiguous")
    fields = {}
    for node in classes[0].body:
        if isinstance(node, ast.AnnAssign):
            require(isinstance(node.target, ast.Name) and node.value is not None,
                    "configuration field requires a literal default")
            if isinstance(node.value, ast.Name):
                require(node.value.id in constants, "nonliteral configuration constant")
                value = constants[node.value.id]
            else:
                try:
                    value = ast.literal_eval(node.value)
                except (ValueError, TypeError) as exc:
                    raise PathError("nonliteral configuration default") from exc
            fields[node.target.id] = detach(value)
    require(bool(fields), "empty configuration declaration")
    return fields


def source_configuration(root: Path) -> dict:
    """Freeze the first exposed PR182 recipe and complete M1 defaults without models.

    PR182's two development input seeds share this single producer configuration
    (topology seed 41). Literal inputs independently select its first seed, 910071.
    No historical execution-source equality is asserted against the repaired tree.
    """
    from scripts.v05_history_export_probe import source_configuration_preflight

    root = Path(root)
    raw = (root / PR182_PROTOCOL).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == PR182_PROTOCOL_SHA256,
            "historical PR182 protocol bytes changed")
    protocol = json.loads(raw)
    require(protocol["source_pin"] == PROJECTION_ORIGIN_SOURCE_PIN,
            "historical projection origin changed")
    source_configuration_preflight(root, protocol)
    defaults = {key: _ast_defaults(root / "src/sparkbrain" / relative, name)
                for key, (relative, name) in M1_CONFIG_TYPES.items()}
    require(defaults["v03"]["input_track"] == "I1_local_compositional"
            and defaults["v03"]["entity_track"] == "E0_global",
            "M1 default I1/E0 contract changed")
    require(defaults["scope"]["max_components"] == 2
            and defaults["scope"]["maximum_dimensions"] == 8
            and defaults["predictive"]["max_context_scalars"] >= 8,
            "M1 default inlet capacity changed")
    return {"producer": detach(protocol["configuration"]), "m1": defaults,
            "projection_origin_source_pin": PROJECTION_ORIGIN_SOURCE_PIN,
            "execution_source_commit": EXECUTION_SOURCE_COMMIT}


def _strict_json(raw: bytes) -> Any:
    def pairs(rows: list) -> dict:
        result = {}
        for key, value in rows:
            require(key not in result, "duplicate checkpoint package key")
            result[key] = value
        return result
    return detach(json.loads(raw, object_pairs_hook=pairs))


def package_checkpoint(files: dict[str, bytes]) -> bytes:
    """Store complete untouched native bytes, not decoded or regenerated JSON."""
    require(set(files) == set(CHECKPOINT_FILES), "predictive checkpoint file inventory")
    require(all(type(raw) is bytes for raw in files.values()), "checkpoint bytes required")
    return canonical({"schema": CHECKPOINT_SCHEMA,
                      "files": {name: base64.b64encode(files[name]).decode("ascii")
                                for name in CHECKPOINT_FILES}})


def unpack_checkpoint(payload: bytes) -> dict[str, bytes]:
    require(type(payload) is bytes, "checkpoint package must be exact bytes")
    value = _strict_json(payload)
    require(type(value) is dict and set(value) == {"schema", "files"}
            and value["schema"] == CHECKPOINT_SCHEMA
            and type(value["files"]) is dict
            and set(value["files"]) == set(CHECKPOINT_FILES), "checkpoint package schema")
    require(canonical(value) == payload, "checkpoint package must be canonical")
    files = {}
    for name in CHECKPOINT_FILES:
        require(type(value["files"][name]) is str, "checkpoint file encoding")
        files[name] = base64.b64decode(value["files"][name], validate=True)
    return files


class NativeBackend:
    """Native paths remain unreachable until separately reviewed sealed admission.

    Tests bypass construction only with model-free exact stand-ins. This is not an
    in-memory adversarial code-attestation boundary. NativeBackend cannot admit itself.
    """

    def __init__(self, permit: Any) -> None:
        from scripts.m1_path_admission import require_permit
        require_permit(permit)  # MUST precede source preparation and all native imports.
        self.permit = permit
        self.configuration = source_configuration(permit.root)
        require(self.configuration == permit.freeze["configuration"],
                "admitted complete configuration drift")
        require(not any(name == "sparkbrain" or name.startswith("sparkbrain.")
                        for name in sys.modules), "native modules must not be preloaded")
        from scripts.v05_history_export_probe import (
            CONFIG_TYPES,
            config_arguments,
            export_native,
            freeze_dictionary,
        )
        from scripts.verify_m1_path_source import CONTRACT

        contract = json.loads((permit.root / CONTRACT).read_bytes())
        self.modules = {}
        classes = [random.Random]
        require(bool(sys.path) and Path(sys.path[0]) == permit.root / "src",
                "launcher must establish frozen source import path before permit admission")
        for relative, row in sorted(contract["files"].items()):
            name = relative.removeprefix("src/").removesuffix(".py").replace("/", ".")
            module = importlib.import_module(name)
            self.modules[name] = module
            classes.extend(getattr(module, cls) for cls in row["classes"])
        for relative, _ in (*CONFIG_TYPES.values(), *M1_CONFIG_TYPES.values()):
            name = "sparkbrain." + relative.removesuffix(".py").replace("/", ".")
            self.modules[name] = importlib.import_module(name)
        for name in ("sparkbrain.v032.checkpoint", "sparkbrain.v04.contracts"):
            self.modules[name] = importlib.import_module(name)
        for name, module in tuple(sys.modules.items()):
            if name == "sparkbrain" or name.startswith("sparkbrain."):
                expected = permit.root / "src" / Path(*name.split("."))
                expected = (expected / "__init__.py" if hasattr(module, "__path__")
                            else expected.with_suffix(".py"))
                require(type(module.__loader__) is importlib.machinery.SourceFileLoader
                        and Path(module.__file__) == expected
                        and Path(module.__spec__.origin) == expected,
                        "native source origin or loader mismatch")
        self.loaded_classes = tuple(classes)
        self._export_native, self._freeze_dictionary = export_native, freeze_dictionary
        self.prepared = {}
        for key, (relative, cls) in CONFIG_TYPES.items():
            name = "sparkbrain." + relative.removesuffix(".py").replace("/", ".")
            self.prepared[key] = getattr(self.modules[name], cls)(
                **config_arguments(key, self.configuration["producer"][key]))
        require(detach({key: dataclasses.asdict(value) for key, value in self.prepared.items()})
                == self.configuration["producer"], "actual producer config object drift")
        self._graph_context = None
        self._readbacks: dict[int, Any] = {}

    def configure_graph_context(self, registry: Any, resources: Any,
                                retained_roots_callable: Callable[[], tuple]) -> None:
        require(self._graph_context is None and callable(retained_roots_callable),
                "graph context already set or invalid")
        require(resources is not None, "native readback requires resource boundary")
        registry.validate_resources(resources)
        self._graph_context = (registry, resources, retained_roots_callable)

    def producer(self) -> Any:
        from scripts.v05_history_export_probe import actual_configuration

        cls = self.modules["sparkbrain.v05.brain"].IntegratedV05Brain
        brain = cls(dataclasses.replace(self.prepared["brain"]), **{
            key + "_config": dataclasses.replace(self.prepared[key])
            for key in ("receptor", "assembly", "homeostasis", "plasticity", "action")})
        require(detach(actual_configuration(brain)) == self.configuration["producer"],
                "complete actual producer configuration drift")
        return brain

    def m1(self) -> Any:
        m1 = self.modules["sparkbrain.system_build.integrated_m1"].IntegratedM1Pilot()
        base = m1.predictive.reference_brain._brain
        require(base.config.input_track == "I1_local_compositional"
                and base.config.entity_track == "E0_global"
                and base._provided_revision_model is None,
                "default I1/E0 M1 without supplied revision model required")
        self._check_m1_configuration(m1)
        return m1

    def _check_m1_configuration(self, m1: Any) -> None:
        actual = {"v03": dataclasses.asdict(m1.predictive.reference_brain._brain.config),
                  "predictive": dataclasses.asdict(m1.predictive.config),
                  "scope": dataclasses.asdict(m1.scoped.config)}
        require(detach(actual) == self.configuration["m1"], "complete actual M1 config drift")
        require(m1.scoped._router.config is m1.scoped.config,
                "actual injected router config alias drift")

    def dictionary(self, root: dict) -> dict:
        result = detach(self._freeze_dictionary(root["producer"].assemblies))
        require(result["binding"]["source_pin"] == PROJECTION_ORIGIN_SOURCE_PIN,
                "historical projection binding changed")
        return result

    def process(self, root: dict, observation: dict, acquisition: bool) -> dict:
        validate_observation(observation)
        require(type(acquisition) is bool, "acquisition must be a boolean")
        external = detach(observation)
        pulse_type = self.modules["sparkbrain.v04.contracts"].SignalPulse
        owned = tuple(pulse_type(**detach(row)) for row in external["pulses"])
        require(all(type(pulse) is pulse_type for pulse in owned), "exact native pulse required")
        require([detach(pulse.as_dict()) for pulse in owned] == external["pulses"],
                "native pulse conversion drift")
        require(not {id(pulse.metadata) for pulse in owned}
                & {id(row["metadata"]) for row in external["pulses"]}, "pulse ingress alias")
        result = root["producer"].process_episode(
            owned, episode_id=external["occurrence_id"], learn_assembly=acquisition,
            learn_field=acquisition, explore_action=False, metadata={})
        require(result.end_ms == external["start_ms"] + 72.0, "native decision clock drift")
        outward = {"result": detach(result.as_dict()), "observation": external,
                   "execution_source_commit": EXECUTION_SOURCE_COMMIT,
                   "projection_origin_source_pin": PROJECTION_ORIGIN_SOURCE_PIN}
        if not acquisition:
            exported, audit = self._export_native(
                root["producer"], result, external, detach(root["dictionary"]),
                self.modules["sparkbrain.v05.assemblies"].pattern_similarity)
            outward.update(export=detach(exported), matching=detach(audit))
        require(observation == external, "native processing mutated caller input")
        root["raw_history"].append(detach(external))
        return detach(outward)

    def check_capacity(self, root: dict, dimensions: int = 8, context_scalars: int = 8) -> None:
        require(type(dimensions) is int and type(context_scalars) is int
                and dimensions == context_scalars == 8, "exact eight-scalar inlets required")
        m1 = root["m1"]
        self._check_m1_configuration(m1)
        require(m1.scoped._router.config.maximum_dimensions >= dimensions
                and m1.predictive.config.max_context_scalars >= context_scalars
                and m1.scoped.config.max_components == 2, "actual injected inlet capacity")

    def observe(self, root: dict, wire: dict) -> dict:
        external = detach(wire)
        require(type(external) is dict and set(external) == {
            "event_id", "time", "sensory_values", "routing_features"}, "M1 wire fields")
        sensory, routing = external["sensory_values"], external["routing_features"]
        require(type(sensory) is dict and set(sensory) == set(CHANNELS)
                and type(routing) is list and len(routing) == 8, "M1 fixed channel schema")
        require(sensory["signal"] == 0.0 and routing[0] == 0.0,
                "original current signal/route coordinate changed")
        require(all(type(v) in (int, float) and math.isfinite(v) and 0 <= v <= 1
                    for v in (*sensory.values(), *routing)), "finite unit inlet coordinates")
        require(type(external["event_id"]) is str
                and re.fullmatch(r"[A-Za-z0-9._:-]{1,128}", external["event_id"]) is not None
                and type(external["time"]) in (int, float)
                and math.isfinite(external["time"]) and external["time"] >= 0,
                "M1 event/time binding")
        self.check_capacity(root)
        cls = self.modules["sparkbrain.system_build.integrated_m1"].M1Observation
        native = cls(external["event_id"], external["time"], detach(sensory), tuple(routing))
        action = root["m1"].observe(native)
        raw = detach(action.as_dict())
        require(wire == external, "M1 observation mutated caller wire")
        # These are fields/compositor choices already produced by the single native
        # observe. No second prediction, scope query, save, replay or constructor.
        return {"native_action": raw, "prediction": raw["prediction"],
                "predictive_choice": (None if raw["prediction"] is None
                                      else "alpha" if raw["prediction"] >= 0 else "beta"),
                "route_choice": raw["route_candidate"], "route_token": raw["route_token"],
                "selected_state_id": raw["selected_state_id"],
                "final_action": raw["decision"], "reason": raw["reason"]}

    def outcome(self, root: dict, receipt: dict) -> dict:
        external = detach(receipt)
        require(type(external) is dict and set(external) == {
            "receipt_id", "event_id", "outcome"}, "receipt schema")
        cls = self.modules["sparkbrain.system_build.integrated_m1"].M1OutcomeReceipt
        revision = root["m1"].apply_outcome(cls(**detach(external)))
        require(receipt == external, "native outcome mutated caller receipt")
        return detach(revision.as_dict())

    def _checkpoint_manager(self) -> Any:
        return self.modules["sparkbrain.system_build.predictive_revision"].PilotCheckpointManager

    def save_predictive(self, root: dict) -> bytes:
        require(self._graph_context is not None, "checkpoint graph context required")
        manager = self._checkpoint_manager()
        require((manager.BRAIN_FILE, manager.PILOT_FILE) == CHECKPOINT_FILES,
                "native checkpoint filename contract drift")
        with TemporaryDirectory(prefix="m1-path-predictive-") as directory:
            path = Path(directory) / "predictive"
            manager.save(root["m1"].predictive, path)
            require({entry.name for entry in path.iterdir()} == set(CHECKPOINT_FILES),
                    "unexpected native checkpoint member")
            # Read both files as bytes before any adapter decode. Internal native
            # save-validation bytes must ALSO be preserved by the admitted profiler.
            files = {name: (path / name).read_bytes() for name in CHECKPOINT_FILES}
            return package_checkpoint(files)

    def load_predictive(self, payload: bytes) -> dict:
        require(self._graph_context is not None and not self._readbacks,
                "one live predictive readback with configured graph context required")
        _, resources, _ = self._graph_context
        baseline = resources.ledger()
        files = unpack_checkpoint(payload)
        try:
            restored = self._load_checkpoint_files(files)
        except BaseException as error:
            # Failed native decode/load may retain a just-constructed facade in its
            # traceback. Release those frames before checking weak-registry cleanup.
            error.__traceback__ = None
            error.__context__ = None
            error.__cause__ = None
            resources.verify_cleanup(baseline)
            raise error from None
        self._readbacks[id(restored)] = baseline
        return restored

    def _load_checkpoint_files(self, files: dict[str, bytes]) -> dict:
        with TemporaryDirectory(prefix="m1-path-readback-") as directory:
            path = Path(directory)
            for name, raw in files.items():
                with (path / name).open("xb") as stream:
                    stream.write(raw)
            predictive = self._checkpoint_manager().load(path)
        return {"predictive": predictive,
                "checkpoint_files_hex": {name: raw.hex() for name, raw in files.items()}}

    def compare_predictive(self, root: dict, restored: dict) -> None:
        try:
            self._compare_predictive(root, restored)
        except BaseException as error:
            # A terminal comparison error must not keep native readback objects alive
            # through helper-frame locals while the schedule disposes its wrapper.
            error.__traceback__ = None
            error.__context__ = None
            error.__cause__ = None
            raise error from None

    def _compare_predictive(self, root: dict, restored: dict) -> None:
        require(self._graph_context is not None and id(restored) in self._readbacks,
                "unowned predictive readback")
        registry, resources, retained = self._graph_context
        originals = retained()
        require(type(originals) is tuple, "retained graph roots must be a tuple")
        left, right = root["m1"].predictive, restored["predictive"]
        left_graph = capture_graph(left, registry, resources,
                                   retained_roots=(*originals, restored))
        right_graph = capture_graph(right, registry, resources,
                                    retained_roots=(*originals, root))
        require(not left_graph.mutable_ids & right_graph.mutable_ids,
                "predictive readback shares mutable owner state")
        for owner in originals:
            if owner is restored:
                continue
            graph = capture_graph(owner, registry, resources,
                                  retained_roots=(*originals, restored, root))
            require(not graph.mutable_ids & right_graph.mutable_ids,
                    "predictive readback shares retained-owner mutable state")
        files = {name: bytes.fromhex(restored["checkpoint_files_hex"][name])
                 for name in CHECKPOINT_FILES}
        pilot = _strict_json(files["pilot-state.json"])
        direct = _strict_json(files["reference-brain.json"])
        codec = self.modules["sparkbrain.v032.checkpoint"]
        for candidate in (left, right):
            require(detach(candidate._checkpoint_payload()) == pilot,
                    "complete predictive payload differs from preserved bytes")
            raw = candidate.reference_brain._brain
            require(detach(codec._encode(dict(vars(raw)))) == direct["state"],
                    "complete raw-brain codec tree differs from preserved bytes")
        # Successful graph capture above rejects extra/missing fields and unknown
        # exact types. Codec projection relaxes ONLY alias topology and map order.

    def dispose_readback(self, restored: dict) -> None:
        require(id(restored) in self._readbacks and self._graph_context is not None,
                "unowned/already disposed readback")
        baseline = self._readbacks.pop(id(restored))
        restored.clear()  # Drop the sole owned model reference; never edit native state.
        self._graph_context[1].verify_cleanup(baseline)
