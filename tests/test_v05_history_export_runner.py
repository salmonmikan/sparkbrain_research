"""Model-free source/helper tests for the prospective PR182 runner.

Use python -B tests/test_v05_history_export_runner.py. These stdlib-only checks
never import SparkBrain, construct a model, process a trial, load a checkpoint,
or execute an old probe. They provide no scientific or runtime ownership evidence.
The scoped import guard and graph tests are source-adapted from PR180's harness.
"""

from __future__ import annotations

import ast
import builtins
import copy
import dataclasses
import hashlib
import importlib.util
import json
import math
import subprocess
import sys
import tempfile
import unittest
from collections import deque
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts/v05_history_export_probe.py"


class RejectSparkBrain:
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "sparkbrain" or fullname.startswith("sparkbrain."):
            raise AssertionError("MODEL IMPORT FORBIDDEN in harness-only tests")
        return None


SENTINEL = RejectSparkBrain()


@contextmanager
def model_import_guard():
    original_import = builtins.__import__
    original_import_module = importlib.import_module

    def guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
        absolute_name = name
        if level:
            namespace = globals or {}
            package = namespace.get("__package__")
            if package is None:
                spec = namespace.get("__spec__")
                if spec is not None:
                    package = spec.parent
                else:
                    package = namespace.get("__name__", "")
                    if "__path__" not in namespace:
                        package = package.rpartition(".")[0]
            absolute_name = importlib.util.resolve_name("." * level + name, package)
        SENTINEL.find_spec(absolute_name)
        return original_import(name, globals, locals, fromlist, level)

    def guarded_import_module(name, package=None):
        SENTINEL.find_spec(importlib.util.resolve_name(name, package))
        return original_import_module(name, package)

    sys.meta_path.insert(0, SENTINEL)
    try:
        with (
            patch.object(builtins, "__import__", guarded_import),
            patch.object(importlib, "import_module", guarded_import_module),
        ):
            yield
    finally:
        sys.meta_path.remove(SENTINEL)


with model_import_guard():
    SPEC = importlib.util.spec_from_file_location("history_export_runner", RUNNER)
    runner = importlib.util.module_from_spec(SPEC)
    sys.modules[SPEC.name] = runner
    SPEC.loader.exec_module(runner)


def sparkbrain_modules():
    return {
        name: module
        for name, module in sys.modules.items()
        if name == "sparkbrain" or name.startswith("sparkbrain.")
    }


@dataclasses.dataclass
class Box:
    payload: object


@dataclasses.dataclass
class FakeCandidate:
    assembly_id: str
    prototype: object
    episode_ids: set[str] = dataclasses.field(default_factory=lambda: {"e1", "e2", "e3"})
    occurrences: int = 3
    first_seen_ms: float = 1.0
    last_seen_ms: float = 3.0
    similarity_sum: float = 3.0

    @property
    def episode_count(self):
        return len(self.episode_ids)


class RunnerModelFreeTests(unittest.TestCase):
    def setUp(self):
        self.preexisting_modules = sparkbrain_modules()
        self.enterContext(model_import_guard())

    def tearDown(self):
        self.assertEqual(sparkbrain_modules(), self.preexisting_modules)

    @staticmethod
    def audit():
        return runner.GraphAudit({Box: {"payload"}})

    def graph_bytes(self, value):
        return runner.canonical(self.audit().inspect(value)[0])

    @staticmethod
    def protocol():
        return json.loads((ROOT / runner.PROTOCOL_PATH).read_text())

    def freeze_fixture(self):
        spec = self.protocol()
        return {
            "schema": "v05-history-export-runner-freeze-1",
            "protocol_sha256": runner.PROTOCOL_SHA256,
            "document_sha256": runner.DOCUMENT_SHA256,
            "inputs_sha256": runner.INPUTS_SHA256,
            "graph_schema_sha256": runner.SCHEMA_SHA256,
            "source_pin": runner.SOURCE_PIN,
            "configuration_sha256": hashlib.sha256(
                runner.canonical(spec["configuration"]).encode()
            ).hexdigest(),
            "pythonhashseed": "0",
            "external_timeout_argv": ["timeout", "-s", "KILL", "180s"],
            "implementation_sources_sha256": {
                path: runner.digest_file(ROOT / path) for path in runner.IMPLEMENTATION_PATHS
            },
            "package_sources_sha256": spec["package_sources_sha256"],
            "reuse_sources_sha256": spec["reuse_sources_sha256"],
            "output_directory": "/tmp/model-free-history-export-never-executed",
        }

    def test_source_precheck_preserves_all_fixed_contract_bytes_without_model_import(self):
        spec, schema, records = runner.read_protocol(ROOT)
        self.assertEqual(len(spec["package_sources_sha256"]), 157)
        self.assertEqual(sum(len(row["classes"]) for row in schema["files"].values()), 50)
        self.assertEqual(len(records), 136)
        self.assertEqual(sum(len(row["observation"]["pulses"]) for row in records), 816)
        self.assertEqual(
            runner.PROTOCOL_SHA256,
            "48b2925fac2fb56200e59a9fb88df60c18868d5553e4390fe6c47864b6ac9c82",
        )
        self.assertEqual(
            runner.DOCUMENT_SHA256,
            "d0e3e9e30d5c11bc95aada3d69e7ca9f761b7031a28a8303fffca8abd1ef30e6",
        )
        self.assertEqual(
            runner.INPUTS_SHA256, "69a25de3c3aef84743d45494a1193df0eac695b4d0c8a0beb8f07fad5129ee39"
        )

    def test_protocol_input_schema_document_package_and_reuse_hash_drift_fail_closed(self):
        original = runner.digest_file
        spec = self.protocol()
        targets = [
            runner.PROTOCOL_PATH,
            runner.DOCUMENT_PATH,
            runner.INPUTS_PATH,
            runner.SCHEMA_PATH,
            "src/sparkbrain/v05/brain.py",
            next(path for path in spec["reuse_sources_sha256"] if path != runner.SCHEMA_PATH),
        ]
        for target in targets:

            def altered(path, target=target):
                return "0" * 64 if path == ROOT / target else original(path)

            with self.subTest(target=target), patch.object(runner, "digest_file", altered):
                with self.assertRaises(runner.BindingError):
                    runner.read_protocol(ROOT)
        hashes = runner.package_hashes(ROOT)
        hashes.pop(next(iter(hashes)))
        with patch.object(runner, "package_hashes", return_value=hashes):
            with self.assertRaisesRegex(runner.BindingError, "package source"):
                runner.read_protocol(ROOT)

    def test_source_configuration_rejects_missing_extra_fields_and_native_gate_changes(self):
        source = self.protocol()
        for key in ("brain", "base", "assembly", "action"):
            changed = copy.deepcopy(source)
            changed["configuration"][key]["unknown"] = 1
            with self.subTest(key=key), self.assertRaises(runner.BindingError):
                runner.source_configuration_preflight(ROOT, changed)
        for key, value in (("max_candidates", 31), ("mature_episodes", 2)):
            changed = copy.deepcopy(source)
            changed["configuration"]["assembly"][key] = value
            with self.subTest(key=key), self.assertRaises(runner.BindingError):
                runner.source_configuration_preflight(ROOT, changed)

    def test_configuration_arguments_detach_wire_lists_and_restore_native_action_tuple(self):
        settings = self.protocol()["configuration"]["action"]
        original = copy.deepcopy(settings)
        arguments = runner.config_arguments("action", settings)
        self.assertIs(type(settings["actions"]), list)
        self.assertIs(type(arguments["actions"]), tuple)
        self.assertEqual(arguments["actions"], tuple(settings["actions"]))
        self.assertEqual(
            {key: value for key, value in arguments.items() if key != "actions"},
            {key: value for key, value in settings.items() if key != "actions"},
        )
        arguments["actions"] += ("detached",)
        self.assertEqual(settings, original)
        other = {"nested": {"values": [1, 2]}, "flag": False}
        arguments = runner.config_arguments("brain", other)
        self.assertEqual(arguments, other)
        arguments["nested"]["values"].append(3)
        self.assertEqual(other, {"nested": {"values": [1, 2]}, "flag": False})

    def test_separate_freeze_binds_exact_source_files_inputs_configuration_and_launch(self):
        frozen = self.freeze_fixture()
        spec = self.protocol()
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "freeze.json"

            def verify(value):
                path.write_text(json.dumps(value))
                return runner.verify_freeze(ROOT, path, runner.digest_file(path), spec)

            self.assertEqual(verify(frozen), frozen)
            for field in (
                "schema",
                "protocol_sha256",
                "document_sha256",
                "inputs_sha256",
                "graph_schema_sha256",
                "source_pin",
                "configuration_sha256",
                "pythonhashseed",
                "external_timeout_argv",
            ):
                altered = copy.deepcopy(frozen)
                altered[field] = "wrong"
                with self.subTest(field=field), self.assertRaises(runner.BindingError):
                    verify(altered)
            for field in (
                "implementation_sources_sha256",
                "package_sources_sha256",
                "reuse_sources_sha256",
            ):
                for change in ("missing", "changed", "extra"):
                    altered = copy.deepcopy(frozen)
                    key = next(iter(altered[field]))
                    if change == "missing":
                        del altered[field][key]
                    elif change == "changed":
                        altered[field][key] = "0" * 64
                    else:
                        altered[field]["unauthorized-extra.py"] = "0" * 64
                    with self.subTest(field=field, change=change):
                        with self.assertRaises(runner.BindingError):
                            verify(altered)
            altered = copy.deepcopy(frozen)
            altered["output_directory"] = "relative-output"
            with self.assertRaisesRegex(runner.BindingError, "absolute"):
                verify(altered)
            verify(frozen)
            with self.assertRaisesRegex(runner.BindingError, "freeze SHA"):
                runner.verify_freeze(ROOT, path, "0" * 64, spec)

    def test_literal_input_guards_reject_extra_model_information_and_reordered_queries(self):
        records = [
            json.loads(line) for line in (ROOT / runner.INPUTS_PATH).read_text().splitlines()
        ]
        mutations = (
            lambda rows: rows.pop(),
            lambda rows: rows[0]["observation"].update(branch="A"),
            lambda rows: rows[0].update(seed=0),
            lambda rows: rows[64].update(branch="B"),
            lambda rows: rows[64]["observation"].update(start_ms=13000.0),
            lambda rows: rows[0]["observation"]["pulses"][0]["metadata"].update(target=1),
            lambda rows: rows[0]["observation"]["pulses"][0].update(novelty=0.1),
            lambda rows: rows[66]["observation"].update(occurrence_id="changed"),
        )
        for index, mutate in enumerate(mutations):
            altered = copy.deepcopy(records)
            mutate(altered)
            with self.subTest(index=index), self.assertRaises(runner.BindingError):
                runner.validate_inputs(altered)

    @staticmethod
    def raster_observation(*pulses):
        return {
            "start_ms": 100.0,
            "pulses": [
                {"time_ms": 100.0 + time, "channel": channel, "magnitude": magnitude}
                for time, channel, magnitude in pulses
            ],
        }

    @staticmethod
    def pattern(index=1, **fields):
        values = {
            "pattern_id": f"pattern-{index}",
            "start_ms": 10.0,
            "end_ms": 12.0,
            "ordered_units": (index, index + 1),
            "relative_bins": (0, 1),
            "unit_ids": (index, index + 1),
            "spike_count": 2,
            "source_cascade_id": f"cascade-{index}",
            "source_kind": "internal_reservoir",
        }
        values.update(fields)
        return SimpleNamespace(**values)

    @staticmethod
    def bank(*candidates):
        return SimpleNamespace(
            config=SimpleNamespace(mature_episodes=3, similarity_threshold=0.66, max_candidates=32),
            candidates={row.assembly_id: row for row in candidates},
            suppressed=set(),
        )

    @staticmethod
    def activation(candidate, pattern, score, **fields):
        values = {
            "assembly_id": candidate.assembly_id,
            "pattern_id": pattern.pattern_id,
            "time_ms": pattern.end_ms,
            "similarity": score,
            "occurrences": candidate.occurrences,
            "episode_count": candidate.episode_count,
            "mature": candidate.episode_count >= 3,
            "unit_ids": candidate.prototype.unit_ids,
            "suppressed": False,
        }
        values.update(fields)
        return SimpleNamespace(**values)

    def export_fixture(self):
        candidate = FakeCandidate("native-a", self.pattern())
        bank = self.bank(candidate)
        query = self.pattern(20)
        activation = self.activation(candidate, query, 0.7123456789012345)
        return {
            "brain": SimpleNamespace(
                config=SimpleNamespace(min_pattern_spikes=2),
                assemblies=bank,
                pending_activation=activation,
            ),
            "result": SimpleNamespace(
                patterns=(query,), assembly_activations=(activation,), end_ms=12872.0
            ),
            "observation": {"occurrence_id": "opaque-query", "start_ms": 12800.0, "pulses": []},
            "dictionary": runner.freeze_dictionary(bank),
            "similarity": lambda *_: 0.7123456789012345,
        }

    def assert_export_status(self, case, status):
        exported, audit = runner.export_native(**case)
        self.assertEqual(exported["status"], status)
        self.assertEqual(exported["accepted"], status.startswith("accepted_"))
        if not exported["accepted"]:
            self.assertEqual(exported["features"], [])
        self.assertEqual(
            set(exported),
            {
                "schema",
                "occurrence_id",
                "decision_ms",
                "accepted",
                "status",
                "features",
                "binding",
            },
        )
        runner.primitive_tree(exported)
        return exported, audit

    def test_dictionary_uses_complete_canonical_content_without_identity_or_time(self):
        first = FakeCandidate("unfavorable-native-id", self.pattern(9))
        second = FakeCandidate("favorable-native-id", self.pattern(1))
        immature = FakeCandidate("immature", self.pattern(0), {"only", "two"}, occurrences=100)
        dictionary = runner.freeze_dictionary(self.bank(first, immature, second))
        expected = [
            runner.canonical_content(second.prototype),
            runner.canonical_content(first.prototype),
        ]
        self.assertEqual(dictionary["binding"]["N"], 2)
        self.assertEqual(
            dictionary["binding"]["canonical_prototypes"], json.loads(runner.canonical(expected))
        )
        self.assertEqual(
            [row["assembly_id"] for row in dictionary["coordinates"]],
            [second.assembly_id, first.assembly_id],
        )
        self.assertEqual(
            dictionary["binding"]["dictionary_sha256"],
            hashlib.sha256(runner.canonical(expected).encode()).hexdigest(),
        )
        original_binding = copy.deepcopy(dictionary["binding"])
        for candidate in (first, second):
            candidate.assembly_id += "-renamed"
            candidate.episode_ids = {"other1", "other2", "other3"}
            candidate.first_seen_ms = 1e9
            candidate.last_seen_ms = 2e9
            candidate.prototype.pattern_id = "renamed"
            candidate.prototype.source_cascade_id = "renamed"
            candidate.prototype.start_ms = 1e9
            candidate.prototype.end_ms = 1e9 + 2
        self.assertEqual(
            runner.freeze_dictionary(self.bank(second, first))["binding"], original_binding
        )
        for field, value in (
            ("ordered_units", (1, 3)),
            ("relative_bins", (0, 2)),
            ("unit_ids", (1, 4)),
            ("spike_count", 3),
            ("source_kind", "another-native-source"),
        ):
            changed = copy.deepcopy(second)
            setattr(changed.prototype, field, value)
            self.assertNotEqual(
                runner.freeze_dictionary(self.bank(changed, first))["binding"],
                original_binding,
                field,
            )

    def test_dictionary_retains_every_mature_candidate_above_future_capacity(self):
        candidates = [FakeCandidate(f"native-{index}", self.pattern(index)) for index in range(32)]
        dictionary = runner.freeze_dictionary(self.bank(*reversed(candidates)))
        self.assertEqual(dictionary["binding"]["N"], 32)
        self.assertEqual(len(dictionary["coordinates"]), 32)
        self.assertEqual(
            dictionary["binding"]["canonical_prototypes"],
            json.loads(
                runner.canonical([runner.canonical_content(row.prototype) for row in candidates])
            ),
        )
        case = self.export_fixture()
        case["brain"].assemblies = self.bank(*candidates)
        chosen = candidates[15]
        activation = self.activation(chosen, case["result"].patterns[0], 0.75)
        case["brain"].pending_activation = activation
        case["result"].assembly_activations = (activation,)
        case["dictionary"] = dictionary
        case["similarity"] = lambda prototype, _: 0.75 if prototype is chosen.prototype else 0.1
        exported, _ = self.assert_export_status(case, "accepted_match")
        self.assertEqual(exported["features"], [0.75 if i == 15 else 0.0 for i in range(32)])

    def test_export_keeps_native_scalar_exact_and_detaches_entire_primitive_binding(self):
        case = self.export_fixture()
        exported, audit = self.assert_export_status(case, "accepted_match")
        scalar = case["brain"].pending_activation.similarity
        self.assertEqual(exported["features"], [scalar])
        self.assertEqual(exported["features"][0].hex(), scalar.hex())
        self.assertEqual(exported["occurrence_id"], "opaque-query")
        self.assertEqual(exported["decision_ms"], 12872.0)
        self.assertTrue(audit["pending_is_native_strongest"])
        self.assertEqual(audit["pending_returned_identity_indices"], [0])
        original_dictionary = copy.deepcopy(case["dictionary"])
        self.assertFalse(
            set(runner.primitive_tree(exported)) & set(runner.primitive_tree(case["dictionary"]))
        )
        exported["features"].append(-1.0)
        exported["binding"]["canonical_prototypes"][0][0].append(999)
        exported["binding"]["external_mutation_probe"] = True
        self.assertEqual(case["dictionary"], original_dictionary)
        self.assertEqual(
            case["brain"].assemblies.candidates["native-a"].prototype.ordered_units, (1, 2)
        )

    def test_export_single_candidate_match_no_match_and_empty_dictionary(self):
        case = self.export_fixture()
        case["similarity"] = lambda *_: 0.5
        case["result"].assembly_activations = ()
        case["brain"].pending_activation = None
        exported, audit = self.assert_export_status(case, "accepted_no_match")
        self.assertEqual(exported["features"], [0.0])
        self.assertEqual(audit["patterns"][0]["best_score"], 0.5)
        case["brain"].assemblies = self.bank()
        case["dictionary"] = runner.freeze_dictionary(case["brain"].assemblies)
        exported, _ = self.assert_export_status(case, "no_mature_dictionary")
        self.assertEqual(exported["binding"]["N"], 0)

    def test_immature_or_suppressed_native_activations_are_explicit_no_match(self):
        for mode in ("immature", "suppressed"):
            case = self.export_fixture()
            candidate = FakeCandidate(
                "unusable",
                self.pattern(5),
                {"one", "two"} if mode == "immature" else {"a", "b", "c"},
            )
            case["brain"].assemblies.candidates[candidate.assembly_id] = candidate
            if mode == "suppressed":
                case["brain"].assemblies.suppressed.add(candidate.assembly_id)
            activation = self.activation(
                candidate, case["result"].patterns[0], 0.9, suppressed=mode == "suppressed"
            )
            case["result"].assembly_activations = (activation,)
            case["brain"].pending_activation = None
            case["dictionary"] = runner.freeze_dictionary(case["brain"].assemblies)
            case["similarity"] = lambda prototype, _, candidate=candidate: (
                0.9 if prototype is candidate.prototype else 0.2
            )
            with self.subTest(mode=mode):
                exported, _ = self.assert_export_status(case, "accepted_no_match")
                self.assertEqual(exported["features"], [0.0] * exported["binding"]["N"])

    def test_canonical_collision_is_retained_and_withholds_export(self):
        case = self.export_fixture()
        existing = case["brain"].assemblies.candidates["native-a"]
        other = copy.deepcopy(existing)
        other.assembly_id = "native-b"
        other.prototype.pattern_id = "identity-excluded"
        case["brain"].assemblies.candidates[other.assembly_id] = other
        case["dictionary"] = runner.freeze_dictionary(case["brain"].assemblies)
        self.assertEqual(case["dictionary"]["binding"]["N"], 2)
        self.assertEqual(case["dictionary"]["collisions"], [["native-a", "native-b"]])
        _, audit = self.assert_export_status(case, "canonical_collision")
        self.assertEqual(
            set(audit["withheld_reasons"]), {"canonical_collision", "native_match_tie"}
        )

    def test_best_match_ties_include_immature_candidates_and_scores_below_threshold(self):
        for score in (0.5, 0.7123456789012345):
            case = self.export_fixture()
            other = FakeCandidate("native-z", self.pattern(9), {"one"})
            case["brain"].assemblies.candidates[other.assembly_id] = other
            case["similarity"] = lambda *_, score=score: score
            if score < 0.66:
                case["result"].assembly_activations = ()
                case["brain"].pending_activation = None
            with self.subTest(score=score):
                _, audit = self.assert_export_status(case, "native_match_tie")
                row = audit["patterns"][0]
                self.assertEqual(row["best_ties"], ["native-a", "native-z"])
                self.assertEqual(len(row["scores"]), 2)
                self.assertEqual(row["native_id_tiebreak_winner"], "native-a")
                self.assertFalse(row["scores"][1]["mature"])

    def test_strongest_numeric_ties_are_retained_before_native_id_tiebreak(self):
        case = self.export_fixture()
        first = case["brain"].assemblies.candidates["native-a"]
        second = FakeCandidate("native-z", self.pattern(9))
        queries = (self.pattern(20), self.pattern(30))
        first_activation = self.activation(first, queries[0], 0.8)
        second_activation = self.activation(second, queries[1], 0.8)
        case["brain"].assemblies.candidates[second.assembly_id] = second
        case["brain"].pending_activation = second_activation
        case["result"].patterns = queries
        case["result"].assembly_activations = (first_activation, second_activation)
        case["dictionary"] = runner.freeze_dictionary(case["brain"].assemblies)
        case["similarity"] = lambda prototype, query: (
            0.8 if (prototype is first.prototype) == (query is queries[0]) else 0.1
        )
        _, audit = self.assert_export_status(case, "native_strongest_tie")
        self.assertEqual(
            [row["assembly_id"] for row in audit["strongest_ties"]], ["native-a", "native-z"]
        )
        self.assertTrue(audit["pending_is_native_strongest"])

    def test_strongest_selection_uses_episode_count_without_rescaling_similarity(self):
        case = self.export_fixture()
        first = case["brain"].assemblies.candidates["native-a"]
        second = FakeCandidate("native-z", self.pattern(9), {"one", "two", "three", "four"}, 4)
        queries = (self.pattern(20), self.pattern(30))
        activations = (
            self.activation(first, queries[0], 0.8),
            self.activation(second, queries[1], 0.8),
        )
        case["brain"].assemblies.candidates[second.assembly_id] = second
        case["brain"].pending_activation = activations[1]
        case["result"].patterns = queries
        case["result"].assembly_activations = activations
        case["dictionary"] = runner.freeze_dictionary(case["brain"].assemblies)
        case["similarity"] = lambda prototype, query: (
            0.8 if (prototype is first.prototype) == (query is queries[0]) else 0.1
        )
        exported, audit = self.assert_export_status(case, "accepted_match")
        self.assertEqual(exported["features"], [0.0, 0.8])
        self.assertEqual(len(audit["strongest_ties"]), 1)

    def test_pending_native_identity_and_returned_activation_bindings_are_mandatory(self):
        mutations = (
            lambda case: setattr(
                case["brain"], "pending_activation", copy.deepcopy(case["brain"].pending_activation)
            ),
            lambda case: setattr(case["brain"], "pending_activation", None),
            lambda case: setattr(case["result"].assembly_activations[0], "pattern_id", "other"),
            lambda case: setattr(case["result"].assembly_activations[0], "time_ms", 13.0),
            lambda case: setattr(case["result"].assembly_activations[0], "occurrences", 99),
            lambda case: setattr(case["result"].assembly_activations[0], "unit_ids", (999,)),
            lambda case: case["brain"].assemblies.candidates.clear(),
        )
        for index, mutate in enumerate(mutations):
            case = self.export_fixture()
            mutate(case)
            with self.subTest(index=index):
                self.assert_export_status(case, "binding_error")

    def test_changed_or_missing_dictionary_binding_withholds_without_index_error(self):
        mutations = (
            lambda binding: binding.update(dictionary_sha256="0" * 64),
            lambda binding: binding.update(source_pin="wrong"),
            lambda binding: binding.update(N=0),
            lambda binding: binding.update(canonical_prototypes=[]),
            lambda binding: binding["canonical_prototypes"][0][0].append(999),
        )
        for index, mutate in enumerate(mutations):
            case = self.export_fixture()
            mutate(case["dictionary"]["binding"])
            with self.subTest(index=index):
                self.assert_export_status(case, "binding_error")
        case = self.export_fixture()
        case["dictionary"]["coordinates"] = []
        self.assert_export_status(case, "binding_error")

    def test_invalid_scores_and_pending_values_never_get_clipped_or_accepted(self):
        for value in (float("nan"), float("inf"), -0.001, 1.001, True, "0.8"):
            case = self.export_fixture()
            case["similarity"] = lambda *_, value=value: value
            with self.subTest(value=repr(value), location="score"):
                self.assert_export_status(case, "value_error")
            case = self.export_fixture()
            case["brain"].pending_activation.similarity = value
            with self.subTest(value=repr(value), location="pending"):
                self.assert_export_status(case, "value_error")

    def test_patterns_below_native_spike_cutoff_are_retained_but_not_matched(self):
        case = self.export_fixture()
        case["result"].patterns[0].spike_count = 1
        case["result"].assembly_activations = ()
        case["brain"].pending_activation = None
        with patch.object(runner, "canonical_content", wraps=runner.canonical_content):
            case["similarity"] = lambda *_: self.fail("subthreshold pattern was matched")
            exported, audit = self.assert_export_status(case, "accepted_no_match")
        self.assertEqual(exported["features"], [0.0])
        self.assertEqual(audit["patterns"], [{"index": 0, "accepted_internal_pattern": False}])

    def test_exports_repeat_exactly_and_never_leak_audit_labels_into_features(self):
        case = self.export_fixture()
        original, _ = self.assert_export_status(case, "accepted_match")
        repeated, _ = self.assert_export_status(copy.deepcopy(case), "accepted_match")
        self.assertEqual(runner.canonical(original), runner.canonical(repeated))
        case["observation"].update(branch="B", resource_seconds=999, target="forbidden")
        relabeled, _ = self.assert_export_status(case, "accepted_match")
        self.assertEqual(runner.canonical(original), runner.canonical(relabeled))

    def test_raw_raster_uses_linear_split_integer_bins_all_channels_and_total_magnitude(self):
        observation = self.raster_observation((0, "A", 2), (1.25, "C", 4), (40, "Q", 2))
        raster = runner.raw_raster(observation)
        expected = [0.0] * 410
        expected[0] = 0.25
        expected[41 + 1] = 0.375
        expected[41 + 2] = 0.125
        expected[9 * 41 + 40] = 0.25
        self.assertEqual(raster, expected)
        self.assertEqual(math.fsum(raster), 1.0)
        all_channels = self.raster_observation(*[(0, channel, 1) for channel in runner.CHANNELS])
        self.assertEqual([runner.raw_raster(all_channels)[41 * i] for i in range(10)], [0.1] * 10)

    def test_raw_raster_rejects_outside_cutoff_unknown_channels_and_invalid_magnitude(self):
        for pulse in (
            (-0.01, "A", 1),
            (40.01, "Q", 1),
            (0, "Z", 1),
            (0, "A", -1),
            (0, "A", float("nan")),
            (0, "A", float("inf")),
            (float("nan"), "A", 1),
            (float("inf"), "A", 1),
            (0, "A", 0),
        ):
            with self.subTest(pulse=pulse), self.assertRaises(runner.BindingError):
                runner.raw_raster(self.raster_observation(pulse))
        with self.assertRaises(runner.BindingError):
            runner.raw_raster(self.raster_observation((0, "A", 1e308), (1, "C", 1e308)))

    def test_raw_raster_uses_only_causal_pulses_and_exact_repeat_pairs(self):
        records = [
            json.loads(line) for line in (ROOT / runner.INPUTS_PATH).read_text().splitlines()
        ]
        for offset in (0, 68):
            a, b, ar, br = [row["observation"] for row in records[offset + 64 : offset + 68]]
            vectors = [runner.raw_raster(value) for value in (a, b, ar, br)]
            self.assertEqual(vectors[0], vectors[2])
            self.assertEqual(vectors[1], vectors[3])
            self.assertNotEqual(vectors[0], vectors[1])
            self.assertEqual(vectors[0][9 * 41 :], vectors[1][9 * 41 :])
            for vector in vectors:
                self.assertEqual(len(vector), 410)
                self.assertAlmostEqual(math.fsum(vector), 1.0)
            changed = copy.deepcopy(a)
            changed.update(outcome="not-read", candidate_id="not-read", label="not-read")
            self.assertEqual(runner.raw_raster(changed), vectors[0])

    def test_graph_aliases_cycles_and_copy_isolation(self):
        shared = [Box({"x": [1, 2]})]
        original = {"a": shared, "b": shared}
        original["self"] = original
        clone = copy.deepcopy(original, {})
        left, left_ids = self.audit().inspect(original)
        right, right_ids = self.audit().inspect(clone)
        self.assertEqual(runner.canonical(left), runner.canonical(right))
        self.assertFalse(left_ids & right_ids)
        clone["b"] = copy.deepcopy(clone["b"])
        self.assertNotEqual(self.graph_bytes(original), self.graph_bytes(clone))

    def test_four_independent_fake_graph_copies_have_all_ten_disjoint_pairs(self):
        shared = Box({"cache": deque([[1.0]], maxlen=4)})
        root = {"active": [shared], "inactive": shared, "retained": []}
        root["retained"].append(root["active"])
        copies = [copy.deepcopy(root, {}) for _ in range(4)]
        inventories = [self.audit().inspect(value) for value in [root, *copies]]
        for graph, _ in inventories:
            self.assertTrue(graph["complete"])
            self.assertEqual(runner.canonical(graph), runner.canonical(inventories[0][0]))
        pairs = [(left, right) for left in range(5) for right in range(left + 1, 5)]
        self.assertEqual(len(pairs), 10)
        self.assertTrue(all(not inventories[a][1] & inventories[b][1] for a, b in pairs))
        before = self.graph_bytes(root)
        copies[0]["inactive"].payload["cache"][0].append(2.0)
        self.assertEqual(self.graph_bytes(root), before)
        self.assertNotEqual(self.graph_bytes(copies[0]), before)

    def test_graph_declared_slots_and_missing_fields_are_not_omitted(self):
        @dataclasses.dataclass(slots=True)
        class Slotted:
            retained: object

        value = Slotted([Box({"inactive": []})])
        audit = runner.GraphAudit({Slotted: {"retained"}, Box: {"payload"}})
        graph, identities = audit.inspect(value)
        self.assertTrue(graph["complete"])
        self.assertIn(id(value), identities)
        self.assertIn("inactive", runner.canonical(graph))
        del value.retained[0].payload
        with self.assertRaisesRegex(runner.InvariantError, "fields"):
            audit.inspect(value)
        self.assertFalse(audit.partial["complete"])

    def test_schema_binding_rejects_custom_copy_and_reduce_hooks_before_copy(self):
        for hook in ("__copy__", "__deepcopy__", "__reduce__", "__reduce_ex__"):
            with self.subTest(hook=hook):
                unsafe = type("Unsafe", (), {"__module__": "fake_schema", hook: lambda *_: None})
                module = SimpleNamespace(__name__="fake_schema", Unsafe=unsafe)
                schema = {
                    "files": {
                        "src/fake_schema.py": {
                            "classes": {
                                "Unsafe": {"declared_fields": []},
                            }
                        }
                    }
                }
                with patch.object(runner.importlib, "import_module", return_value=module):
                    with self.assertRaisesRegex(runner.BindingError, "custom copy hook"):
                        runner.GraphAudit.from_schema(schema)

    def test_schema_binding_rejects_a_reexported_class(self):
        module = SimpleNamespace(__name__="fake_schema", Box=Box)
        schema = {
            "files": {
                "src/fake_schema.py": {
                    "classes": {
                        "Box": {"declared_fields": ["payload"]},
                    }
                }
            }
        }
        with patch.object(runner.importlib, "import_module", return_value=module):
            with self.assertRaisesRegex(runner.BindingError, "origin"):
                runner.GraphAudit.from_schema(schema)

    def test_graph_preserves_primitive_types_order_capacity_and_fields(self):
        self.assertNotEqual(self.graph_bytes([True]), self.graph_bytes([1]))
        self.assertNotEqual(self.graph_bytes([1]), self.graph_bytes([1.0]))
        self.assertNotEqual(self.graph_bytes([0.0]), self.graph_bytes([-0.0]))
        self.assertNotEqual(self.graph_bytes({"a": 1, "b": 2}), self.graph_bytes({"b": 2, "a": 1}))
        self.assertNotEqual(
            self.graph_bytes(deque([1], maxlen=2)), self.graph_bytes(deque([1], maxlen=3))
        )
        self.assertNotEqual(self.graph_bytes([1, 2]), self.graph_bytes((1, 2)))
        self.assertEqual(self.graph_bytes({"a", "b"}), self.graph_bytes({"b", "a"}))
        value = Box([1])
        value.extra = 1
        with self.assertRaisesRegex(runner.InvariantError, "fields"):
            self.audit().inspect(value)

    def test_unknown_handles_nonfinite_and_subclasses_rejected_with_partial_graph(self):
        class Sublist(list):
            pass

        for unsupported in (object(), Sublist([1]), float("inf"), {object()}):
            audit = self.audit()
            with self.assertRaises(runner.InvariantError):
                audit.inspect({"known": [1, 2], "unsupported": unsupported})
            self.assertFalse(audit.partial["complete"])
            self.assertTrue(audit.partial["nodes"])
            self.assertIn("known", runner.canonical(audit.partial))

    def test_primitive_export_rejects_handles_aliases_cycles_and_nonstring_keys(self):
        shared = []
        cycle = []
        cycle.append(cycle)
        for bad in (Box(1), (1, 2), [shared, shared], cycle, {1: "x"}, float("nan")):
            with self.assertRaises(runner.InvariantError):
                runner.primitive_tree(bad)
        value = {"a": [{"x": 1}], "b": []}
        ids = runner.primitive_tree(value)
        self.assertEqual(len(ids), 4)

    def test_twelve_constructor_config_projections(self):
        brain = SimpleNamespace()
        for path in runner.CONFIG_PATHS.values():
            target = brain
            parts = path.split(".")
            for name in parts[:-1]:
                if not hasattr(target, name):
                    setattr(target, name, SimpleNamespace())
                target = getattr(target, name)
            setattr(target, parts[-1], Box(True))
        values = runner.actual_configuration(brain)
        self.assertEqual(len(values), 12)
        self.assertTrue(all(value == {"payload": True} for value in values.values()))

    def test_writer_is_exclusive_and_preserves_partial_under_finalization_cap(self):
        with tempfile.TemporaryDirectory() as folder:
            directory = Path(folder) / "out"
            writer = runner.EvidenceWriter(directory)
            writer.write("raw.json", {"x": 1})
            raw = (directory / "raw.json").read_bytes()
            with self.assertRaises(FileExistsError):
                writer.write("raw.json", {"changed": True})
            with self.assertRaises(FileExistsError):
                runner.EvidenceWriter(directory)
            self.assertEqual(
                writer.manifest()["raw.json"]["sha256"], hashlib.sha256(raw).hexdigest()
            )
            with (
                patch.dict(runner.LIMITS, artifact_bytes=250),
                patch.dict(runner.RESERVE, artifact_bytes=100),
            ):
                with self.assertRaises(runner.BudgetError):
                    writer.write("partial.json", {"known": 1, "long": "x" * 500})
                self.assertFalse(writer.manifest()["partial.json"]["complete_json"])
                writer.finalizing = True
                writer.write("stopped.json", {"status": "stopped"})
                self.assertLessEqual(sum(p.stat().st_size for p in directory.iterdir()), 250)

    def test_writer_rejects_nested_paths_and_manifest_reports_exact_utf8_bytes(self):
        with tempfile.TemporaryDirectory() as folder:
            directory = Path(folder) / "out"
            writer = runner.EvidenceWriter(directory)
            for name in ("../escape.json", "nested/file.json", str(Path(folder) / "absolute")):
                with self.subTest(name=name), self.assertRaises(runner.BindingError):
                    writer.write(name, {})
            writer.write("unicode.json", {"message": "証拠"})
            data = (directory / "unicode.json").read_bytes()
            self.assertEqual(writer.bytes_written, len(data))
            self.assertEqual(
                writer.manifest()["unicode.json"],
                {
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "bytes": len(data),
                    "complete_json": True,
                },
            )

    def test_raw_byte_preservation_uses_the_same_cumulative_evidence_ceiling(self):
        with tempfile.TemporaryDirectory() as folder:
            directory = Path(folder) / "out"
            writer = runner.EvidenceWriter(directory)
            data = b'{"literal": 1}\n  \n'
            writer.write_bytes("literal.jsonl", data)
            self.assertEqual((directory / "literal.jsonl").read_bytes(), data)
            self.assertEqual(writer.bytes_written, len(data))
            self.assertEqual(
                writer.manifest()["literal.jsonl"]["sha256"], hashlib.sha256(data).hexdigest()
            )
            with self.assertRaises(FileExistsError):
                writer.write_bytes("literal.jsonl", b"replace")
            with (
                patch.dict(runner.LIMITS, artifact_bytes=len(data) + 7),
                patch.dict(runner.RESERVE, artifact_bytes=4),
            ):
                with self.assertRaises(runner.BudgetError):
                    writer.write_bytes("partial.raw", b"four")
                self.assertFalse(writer.manifest()["partial.raw"]["complete_json"])
                writer.finalizing = True
                writer.write_bytes("final.raw", b"four")
                self.assertEqual(writer.bytes_written, len(data) + 4)
                self.assertLessEqual(
                    sum(path.stat().st_size for path in directory.iterdir()), len(data) + 7
                )

    def test_execution_reserve_boundaries_are_checked_without_installing_limits(self):
        budget = runner.Budget()
        wall = runner.LIMITS["wall_seconds"] - runner.RESERVE["wall_seconds"]
        cpu = runner.LIMITS["cpu_seconds"] - runner.RESERVE["cpu_seconds"]
        with patch.object(
            budget, "sample", return_value={"wall_seconds": wall - 1, "cpu_seconds": cpu - 1}
        ):
            budget.check()
        for sample in (
            {"wall_seconds": wall, "cpu_seconds": 0},
            {"wall_seconds": 0, "cpu_seconds": cpu},
        ):
            with patch.object(budget, "sample", return_value=sample):
                with self.assertRaises(runner.BudgetError):
                    budget.check()

    def test_finalization_may_use_reserved_budget_but_never_exceed_hard_caps(self):
        budget = runner.Budget()
        sample = {"cpu_seconds": 118.0, "wall_seconds": 171.0}
        with patch.object(budget, "sample", return_value=sample):
            with self.assertRaises(runner.BudgetError):
                budget.check()
            budget.finalizing = True
            budget.check()
        for sample in (
            {"cpu_seconds": 120.0, "wall_seconds": 171.0},
            {"cpu_seconds": 118.0, "wall_seconds": 180.0},
        ):
            with patch.object(budget, "sample", return_value=sample):
                with self.assertRaises(runner.BudgetError):
                    budget.check()

    def test_finalization_uses_remaining_hard_limit_and_is_idempotent(self):
        budget = runner.Budget()
        budget.wall_start = 100.0
        budget.installed = True
        budget.memory_reserve = bytearray(8)
        with (
            patch.object(runner.time, "monotonic", return_value=260.0),
            patch.object(runner.resource, "setrlimit") as limits,
            patch.object(runner.signal, "setitimer") as timer,
        ):
            budget.finish()
            budget.finish()
        limits.assert_called_once_with(runner.resource.RLIMIT_CPU, (120, 120))
        timer.assert_called_once_with(runner.signal.ITIMER_REAL, 20.0)
        self.assertTrue(budget.finalizing)
        self.assertIsNone(budget.memory_reserve)

    def test_uninstalled_budget_finalization_does_not_change_process_resources(self):
        budget = runner.Budget()
        self.assertFalse(budget.installed)
        with (
            patch.object(runner.resource, "setrlimit") as limits,
            patch.object(runner.signal, "setitimer") as timer,
            patch.object(runner.os, "_exit") as hard_exit,
        ):
            budget.finish()
            budget.finish()
        limits.assert_not_called()
        timer.assert_not_called()
        hard_exit.assert_not_called()
        self.assertTrue(budget.finalizing)

    def test_timeout_parent_requires_exact_child_argv_and_specific_hashseed_state(self):
        own = ["python", "-B", str(RUNNER), "--run-reviewed"]
        parent = ["timeout", "-s", "KILL", "180s", *own]

        def check(
            parent_args=parent,
            own_args=own,
            current="0",
            randomized=0,
        ):
            def read(path):
                self.assertIn(
                    str(path), {"/proc/self/cmdline", f"/proc/{runner.os.getppid()}/cmdline"}
                )
                args = own_args if str(path) == "/proc/self/cmdline" else parent_args
                return b"\0".join(word.encode() for word in args)

            with (
                patch.object(Path, "read_bytes", read),
                patch.dict(runner.os.environ, {"PYTHONHASHSEED": current}),
                patch.object(runner.sys, "flags", SimpleNamespace(hash_randomization=randomized)),
            ):
                return runner.verify_timeout_parent()

        self.assertEqual(check()["parent_argv"], parent)
        for fields in (
            {"parent_args": own},
            {"parent_args": ["timeout", "-s", "KILL", "181s", *own]},
            {"own_args": [*own, "unexpected-argument"]},
            {"current": ""},
            {"current": "1"},
            {"randomized": 1},
        ):
            with self.subTest(fields=fields), self.assertRaises(runner.BindingError):
                check(**fields)

    def test_loaded_source_origin_and_code_origin_guards_use_fake_module_records_only(self):
        name = "sparkbrain.v05.brain"
        path = ROOT / "src/sparkbrain/v05/brain.py"
        module = SimpleNamespace(__file__=str(path), __spec__=SimpleNamespace(origin=str(path)))
        modules = {
            key: value
            for key, value in sys.modules.items()
            if key != "sparkbrain" and not key.startswith("sparkbrain.")
        }
        modules[name] = module
        spec = self.protocol()
        with patch.object(runner.sys, "modules", modules):
            self.assertEqual(
                runner.loaded_source_origins(ROOT, spec), {name: "src/sparkbrain/v05/brain.py"}
            )
            for attribute, bad in (
                ("__file__", str(ROOT / "outside.py")),
                ("__spec__", SimpleNamespace(origin=str(ROOT / "outside.py"))),
                ("__spec__", None),
            ):
                with patch.object(module, attribute, bad), self.assertRaises(runner.BindingError):
                    runner.loaded_source_origins(ROOT, spec)

            def fixture_call():
                return None

            fixture_call.__module__ = name
            module.fixture_call = fixture_call
            with self.assertRaisesRegex(runner.BindingError, "code origin"):
                runner.loaded_source_origins(ROOT, spec)
            del module.fixture_call
            with patch.object(runner, "digest_file", return_value="0" * 64):
                with self.assertRaisesRegex(runner.BindingError, "loaded source SHA"):
                    runner.loaded_source_origins(ROOT, spec)
            modules["sparkbrain.system_build"] = SimpleNamespace()
            with self.assertRaisesRegex(runner.BindingError, "M1"):
                runner.loaded_source_origins(ROOT, spec)

    def test_source_limits_and_forbidden_operations_are_structurally_bounded(self):
        self.assertEqual(
            runner.MAX_COUNTS,
            {
                "roots": 2,
                "acquisition_process_attempts": 128,
                "query_process_attempts": 8,
                "total_process_attempts": 136,
                "submitted_pulses": 816,
                "whole_brain_copies": 8,
                "external_object_mutations": 64,
                "commits": 0,
                "m1_calls": 0,
                "native_loads": 0,
                "outcome_updates": 0,
            },
        )
        self.assertEqual(
            runner.LIMITS,
            {
                "address_space_bytes": 512 * 1024**2,
                "artifact_bytes": 96 * 1024**2,
                "cpu_seconds": 120,
                "wall_seconds": 180,
            },
        )
        self.assertEqual(runner.BRANCHES, ["A", "B", "A_repeat", "B_repeat"])
        self.assertEqual(runner.SEEDS, [910071, 910072])
        tree = ast.parse(RUNNER.read_text())
        for node in tree.body:
            if isinstance(node, ast.Import):
                names = [alias.name.split(".")[0] for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module.split(".")[0]]
            else:
                continue
            self.assertTrue(set(names) <= sys.stdlib_module_names, names)
        imports = [
            node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))
        ]
        imports_text = ast.dump(ast.Module(imports, []))
        for forbidden in (
            "temporal_reuse_loop_probe",
            "v05_acquired_ownership_probe",
            "v05_owned_state_probe",
            "system_build",
            "integrated_m1",
        ):
            self.assertNotIn(forbidden, imports_text)
        calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)]
        forbidden_calls = {
            "learn_outcome",
            "load_checkpoint",
            "checkpoint_dict",
            "from_state_dict",
            "state_dict",
            "transact",
            "commit",
            "restore",
        }
        self.assertFalse(
            any(
                isinstance(node.func, ast.Attribute) and node.func.attr in forbidden_calls
                for node in calls
            )
        )
        process_calls = [
            node
            for node in calls
            if isinstance(node.func, ast.Attribute) and node.func.attr == "process_episode"
        ]
        self.assertEqual(len(process_calls), 1)
        self.assertNotIn("platform.platform", RUNNER.read_text())
        owner = next(
            node
            for node in tree.body
            if isinstance(node, ast.ClassDef) and node.name == "PrivateOwner"
        )
        self.assertEqual(
            [node.name for node in owner.body if isinstance(node, ast.FunctionDef)], ["__init__"]
        )

    def test_source_constructs_all_copies_before_queries_and_preserves_before_mutation(self):
        tree = ast.parse(RUNNER.read_text())
        probe = next(
            node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "Probe"
        )
        execute = next(
            node
            for node in probe.body
            if isinstance(node, ast.FunctionDef) and node.name == "execute"
        )
        loops = [node for node in ast.walk(execute) if isinstance(node, ast.For)]
        copy_loop = next(node for node in loops if ast.unparse(node.iter) == "BRANCHES")
        query_loop = next(node for node in loops if ast.unparse(node.iter) == "rows[64:]")
        self.assertLess(copy_loop.end_lineno, query_loop.lineno)
        self.assertFalse(
            any(isinstance(node, (ast.Break, ast.Continue)) for node in ast.walk(execute))
        )
        copy_calls = [
            node
            for node in ast.walk(copy_loop)
            if isinstance(node, ast.Call) and ast.unparse(node.func) == "copy.deepcopy"
        ]
        self.assertEqual(len(copy_calls), 1)
        self.assertEqual(ast.unparse(copy_calls[0]), "copy.deepcopy(root, {})")
        query_calls = [node for node in ast.walk(query_loop) if isinstance(node, ast.Call)]
        mutator = next(
            node for node in query_calls if ast.unparse(node.func) == "self.mutate_external"
        )
        export_write = next(
            node
            for node in query_calls
            if ast.unparse(node.func) == "self.writer.write"
            and "-export.json" in ast.unparse(node.args[0])
        )
        self.assertLess(export_write.lineno, mutator.lineno)
        self.assertEqual(sum(ast.unparse(node.func) == "self.step" for node in query_calls), 1)
        self.assertLess(
            next(node.lineno for node in query_calls if ast.unparse(node.func) == "self.step"),
            mutator.lineno,
        )
        mutator_method = next(
            node
            for node in probe.body
            if isinstance(node, ast.FunctionDef) and node.name == "mutate_external"
        )
        self.assertFalse(
            any(
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr in {"step", "process_episode"}
                for node in ast.walk(mutator_method)
            )
        )

    def test_frozen_learning_flags_disable_outcomes_actions_and_query_learning(self):
        spec = self.protocol()
        self.assertEqual(
            spec["call_flags"],
            {
                "acquisition": {
                    "learn_assembly": True,
                    "learn_field": True,
                    "explore_action": False,
                    "metadata": {},
                },
                "query": {
                    "learn_assembly": False,
                    "learn_field": False,
                    "explore_action": False,
                    "metadata": {},
                },
            },
        )
        for field in ("enable_prediction", "enable_action", "enable_reward_modulation"):
            self.assertIs(spec["configuration"]["brain"][field], False)

    def test_source_freeze_and_origin_guards_precede_native_import_and_execution(self):
        tree = ast.parse(RUNNER.read_text())
        run = next(
            node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "run"
        )
        model_imports = [
            node
            for node in ast.walk(run)
            if isinstance(node, ast.ImportFrom) and node.module.startswith("sparkbrain")
        ]
        self.assertTrue(model_imports)
        calls = [node for node in ast.walk(run) if isinstance(node, ast.Call)]
        first_model_import = min(node.lineno for node in model_imports)
        for guard in ("verify_timeout_parent", "read_protocol", "verify_freeze"):
            call = next(node for node in calls if ast.unparse(node.func) == guard)
            self.assertLess(call.lineno, first_model_import, guard)
        execute = next(node for node in calls if ast.unparse(node.func) == "probe.execute")
        origins = [node for node in calls if ast.unparse(node.func) == "loaded_source_origins"]
        self.assertGreaterEqual(sum(node.lineno < execute.lineno for node in origins), 2)
        main = next(
            node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "main"
        )
        source_branch = next(
            node
            for node in main.body
            if isinstance(node, ast.If) and ast.unparse(node.test) == "args.check_source"
        )
        self.assertFalse(
            any(
                isinstance(node, ast.Call) and ast.unparse(node.func) == "run"
                for node in ast.walk(source_branch)
            )
        )

    def test_network_and_subprocess_audit_denies_only_relevant_events(self):
        for event in (
            "socket.connect",
            "socket.getaddrinfo",
            "subprocess.Popen",
            "os.system",
            "os.fork",
            "os.exec",
            "os.posix_spawn",
            "ctypes.dlopen",
        ):
            with self.subTest(event=event), self.assertRaises(PermissionError):
                runner.deny_network_and_subprocess(event, ())
        runner.deny_network_and_subprocess("open", ())


class HarnessIsolationTests(unittest.TestCase):
    def test_collection_restores_import_hooks_with_or_without_preloaded_modules(self):
        code = """
import builtins, importlib.util, sys, types
if sys.argv[2] == 'preloaded':
    sys.modules['sparkbrain'] = types.ModuleType('sparkbrain')
    sys.modules['sparkbrain.preloaded'] = types.ModuleType('sparkbrain.preloaded')
before = list(sys.meta_path)
before_import = builtins.__import__
before_import_module = importlib.import_module
modules = dict(sys.modules)
spec = importlib.util.spec_from_file_location('isolated_harness', sys.argv[1])
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
assert sys.meta_path == before
assert builtins.__import__ is before_import
assert importlib.import_module is before_import_module
assert module.sparkbrain_modules() == {
    name: value for name, value in modules.items()
    if name == 'sparkbrain' or name.startswith('sparkbrain.')
}
"""
        for state in ("clean", "preloaded"):
            with self.subTest(state=state):
                subprocess.run(
                    [sys.executable, "-B", "-c", code, __file__, state],
                    check=True,
                    capture_output=True,
                    text=True,
                )

    def test_per_test_guard_rejects_import_and_cleans_up_even_after_failure(self):
        code = """
import builtins, importlib.util, sys, types, unittest
sys.modules['sparkbrain'] = types.ModuleType('sparkbrain')
sys.modules['sparkbrain.preloaded'] = types.ModuleType('sparkbrain.preloaded')
before = list(sys.meta_path)
before_import = builtins.__import__
before_import_module = importlib.import_module
spec = importlib.util.spec_from_file_location('isolated_harness', sys.argv[1])
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
class LifecycleCase(module.RunnerModelFreeTests):
    def test_lifecycle(self):
        for call in (
            lambda: __import__('sparkbrain'),
            lambda: importlib.import_module('sparkbrain'),
            lambda: importlib.import_module('.preloaded', 'sparkbrain'),
            lambda: __import__('preloaded', {'__package__': 'sparkbrain'}, fromlist=['x'], level=1),
            lambda: __import__(
                'preloaded', {'__spec__': types.SimpleNamespace(parent='sparkbrain')},
                fromlist=['x'], level=1),
            lambda: __import__(
                'preloaded', {'__name__': 'sparkbrain.caller'}, fromlist=['x'], level=1),
            lambda: __import__(
                'preloaded', {'__name__': 'sparkbrain', '__path__': []},
                fromlist=['x'], level=1),
            lambda: module.SENTINEL.find_spec('sparkbrain.forbidden'),
        ):
            with self.assertRaisesRegex(AssertionError, 'MODEL IMPORT FORBIDDEN'):
                call()
        if sys.argv[2] == 'failure':
            self.fail('synthetic test failure')
result = unittest.TestResult()
LifecycleCase('test_lifecycle').run(result)
assert len(result.failures) == (1 if sys.argv[2] == 'failure' else 0)
assert not result.errors
assert sys.meta_path == before
assert builtins.__import__ is before_import
assert importlib.import_module is before_import_module
assert set(module.sparkbrain_modules()) == {'sparkbrain', 'sparkbrain.preloaded'}
"""
        for outcome in ("success", "failure"):
            with self.subTest(outcome=outcome):
                subprocess.run(
                    [sys.executable, "-B", "-c", code, __file__, outcome],
                    check=True,
                    capture_output=True,
                    text=True,
                )


if __name__ == "__main__":
    unittest.main()
