"""Harness-only stdlib tests: no SparkBrain import, construction or processing.

Use python -B tests/test_v05_acquired_ownership_runner.py. These tests provide no
runtime ownership, coverage, scientific or M1 evidence. Do not broadly discover
repository tests for this source-only implementation review.
"""

from __future__ import annotations

import ast
import builtins
import copy
import dataclasses
import hashlib
import importlib.util
import json
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
CURRENT_ROOT = ROOT
# File loading keeps standalone and import-isolation tests independent of sys.path.
_FIXTURE_SPEC = importlib.util.spec_from_file_location(
    "historical_source_fixture", Path(__file__).with_name("historical_source_fixture.py")
)
_fixture_helper = importlib.util.module_from_spec(_FIXTURE_SPEC)
_FIXTURE_SPEC.loader.exec_module(_fixture_helper)
historical_source_root = _fixture_helper.historical_source_root
RUNNER = ROOT / "scripts/v05_acquired_ownership_probe.py"


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
    SPEC = importlib.util.spec_from_file_location("acquired_ownership_runner", RUNNER)
    runner = importlib.util.module_from_spec(SPEC)
    sys.modules[SPEC.name] = runner
    SPEC.loader.exec_module(runner)


def sparkbrain_modules():
    return {
        name: module for name, module in sys.modules.items()
        if name == "sparkbrain" or name.startswith("sparkbrain.")
    }


@dataclasses.dataclass
class Box:
    payload: object


@dataclasses.dataclass
class FakePulse:
    time_ms: float = 8.0
    channel: str = "Q"
    magnitude: float = 1.2
    polarity: int = 1
    location: object = None
    novelty: float = 0.0
    prediction_error: float = 0.0
    source_id: str = "acquired-ownership-probe"
    metadata: dict = dataclasses.field(default_factory=dict)


class RunnerModelFreeTests(unittest.TestCase):
    def setUp(self):
        self.preexisting_modules = sparkbrain_modules()
        self.enterContext(model_import_guard())
        root = self.enterContext(historical_source_root())
        path = root / RUNNER.relative_to(ROOT)
        spec = importlib.util.spec_from_file_location("historical_test_runner", path)
        historical_runner = importlib.util.module_from_spec(spec)
        self.enterContext(patch.dict(sys.modules, {spec.name: historical_runner}))
        spec.loader.exec_module(historical_runner)
        self.enterContext(patch.dict(globals(), ROOT=root, RUNNER=path, runner=historical_runner))

    def test_changed_current_runtime_is_not_a_historical_source(self):
        with self.assertRaises(runner.BindingError):
            runner.read_protocol(CURRENT_ROOT)

    def tearDown(self):
        self.assertEqual(sparkbrain_modules(), self.preexisting_modules)

    @staticmethod
    def audit():
        return runner.GraphAudit({Box: {"payload"}})

    def graph_bytes(self, value):
        return runner.canonical(self.audit().inspect(value)[0])

    def test_source_check_is_model_free_with_import_sentinel(self):
        code = """
import importlib.abc, runpy, sys
class Reject(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == 'sparkbrain' or fullname.startswith('sparkbrain.'):
            raise AssertionError('model import forbidden')
sys.meta_path.insert(0, Reject())
sys.argv = [sys.argv[1], '--check-source']
runpy.run_path(sys.argv[0], run_name='__main__')
"""
        completed = subprocess.run(
            [sys.executable, "-B", "-c", code, str(RUNNER)],
            check=True,
            capture_output=True,
            text=True,
        )
        result = json.loads(completed.stdout)
        self.assertEqual(result["package_source_files"], 157)
        self.assertEqual(result["schema_classes"], 50)
        self.assertFalse(result["model_imported"])

    def test_module_scope_imports_stdlib_no_old_probe_import(self):
        tree = ast.parse(RUNNER.read_text())
        for node in tree.body:
            names = []
            if isinstance(node, ast.Import):
                names = [alias.name.split(".")[0] for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module.split(".")[0]]
            self.assertTrue(set(names) <= sys.stdlib_module_names, names)
        imports = [
            node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))
        ]
        self.assertNotIn("v05_owned_state_probe", ast.dump(ast.Module(imports, [])))
        self.assertNotIn("v05_paired_coverage_probe", ast.dump(ast.Module(imports, [])))
        calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)]
        self.assertEqual(
            sum(
                isinstance(node.func, ast.Attribute) and node.func.attr == "process_episode"
                for node in calls
            ),
            1,
        )
        forbidden = {"learn_outcome", "load_checkpoint", "from_state_dict", "state_dict"}
        self.assertFalse(
            any(
                isinstance(node.func, ast.Attribute) and node.func.attr in forbidden
                for node in calls
            )
        )
        self.assertNotIn("platform.platform", RUNNER.read_text())

    def test_protocol_and_package_drift_rejected(self):
        original = runner.digest_file
        with patch.object(runner, "digest_file", return_value="0" * 64):
            with self.assertRaisesRegex(runner.BindingError, "protocol SHA"):
                runner.read_protocol(ROOT)

        def changed(path):
            if str(path).endswith("src/sparkbrain/v05/brain.py"):
                return "0" * 64
            return original(path)

        with patch.object(runner, "digest_file", changed):
            with self.assertRaisesRegex(runner.BindingError, "complete package"):
                runner.read_protocol(ROOT)

    def test_separate_freeze_binds_runner_tests_package_and_provenance(self):
        frozen = {
            "schema": "v05-acquired-ownership-runner-freeze-1",
            "protocol_sha256": runner.PROTOCOL_SHA256,
            "graph_schema_sha256": runner.SCHEMA_SHA256,
            "implementation_sources_sha256": {
                p: runner.digest_file(ROOT / p) for p in runner.IMPLEMENTATION_PATHS
            },
            "reuse_sources_sha256": {p: runner.digest_file(ROOT / p) for p in runner.REUSE_PATHS},
            "package_sources_sha256": runner.package_hashes(ROOT),
            "external_timeout_argv": ["timeout", "-s", "KILL", "120s"],
            "output_directory": "/tmp/model-free-freeze-fixture-never-executed",
        }
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "freeze.json"

            def verify(value):
                path.write_text(json.dumps(value))
                return runner.verify_freeze(ROOT, path, runner.digest_file(path))

            self.assertEqual(verify(frozen), frozen)
            for field, key in (
                ("implementation_sources_sha256", next(iter(runner.IMPLEMENTATION_PATHS))),
                ("package_sources_sha256", "src/sparkbrain/__init__.py"),
                ("reuse_sources_sha256", next(iter(runner.REUSE_PATHS))),
            ):
                altered = copy.deepcopy(frozen)
                del altered[field][key]
                with self.assertRaises(runner.BindingError):
                    verify(altered)
            verify(frozen)
            with self.assertRaisesRegex(runner.BindingError, "freeze SHA"):
                runner.verify_freeze(ROOT, path, "0" * 64)

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

    def test_actual_caller_pulse_guards_reject_subclasses_metadata_and_wrong_types(self):
        pulses = (FakePulse(), FakePulse(time_ms=12.0))
        episode = {"pulses": [dataclasses.asdict(p) for p in pulses]}
        runner.pulse_guard(pulses, FakePulse, episode)
        for bad in (list(pulses), pulses[:1]):
            with self.assertRaises(runner.BindingError):
                runner.pulse_guard(bad, FakePulse, episode)
        pulses[0].metadata["constructor_only_control_is_insufficient"] = True
        with self.assertRaisesRegex(runner.BindingError, "metadata"):
            runner.pulse_guard(pulses, FakePulse, episode)
        pulses[0].metadata.clear()
        pulses[0].polarity = True
        with self.assertRaisesRegex(runner.BindingError, "polarity"):
            runner.pulse_guard(pulses, FakePulse, episode)

    def test_owner_preparation_failure_never_commits_and_return_has_no_late_work(self):
        original, successor = object(), object()
        owner = runner.PrivateOwner(original)

        def failure():
            raise ValueError("synthetic prepare failed")

        with self.assertRaises(ValueError):
            owner.transact(failure)
        self.assertIs(owner._brain, original)
        output = {"only": "detached primitive tree"}
        self.assertIs(owner.transact(lambda: (successor, output)), output)
        self.assertIs(owner._brain, successor)
        tree = ast.parse(RUNNER.read_text())
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "PrivateOwner")
        method = next(
            n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "transact"
        )
        self.assertIsInstance(method.body[-2], ast.Assign)
        self.assertEqual(ast.unparse(method.body[-2].targets[0]), "self._brain")
        self.assertIsInstance(method.body[-1], ast.Return)
        self.assertIsInstance(method.body[-1].value, ast.Name)

    def test_maturity_gate_rejects_null_pending_wrong_ids_and_old_result_only(self):
        ids = ["one", "two", "three", "four"]
        activation = SimpleNamespace(assembly_id="a", mature=True, suppressed=False)
        candidate = SimpleNamespace(episode_ids=set(ids), episode_count=4)
        results = [
            SimpleNamespace(metadata={"episode_id": value}, assembly_activations=())
            for value in ids
        ]
        results[-1].assembly_activations = (activation,)
        brain = SimpleNamespace(
            pending_activation=activation,
            results=results,
            suppressed_unit_ids=set(),
            assemblies=SimpleNamespace(candidates={"a": candidate}, suppressed=set()),
        )
        witness = {
            "candidate_prototypes": {"a": {"retained_paths": ["result.pattern"]}},
            "pending_activation_paths": ["result.activation"],
        }
        with patch.object(runner, "identity_witnesses", return_value=witness):
            self.assertTrue(runner.mature_gate(brain, ids)["covered"])
            brain.pending_activation = None
            self.assertFalse(runner.mature_gate(brain, ids)["covered"])
            brain.pending_activation = activation
            candidate.episode_ids = {"one", "two", "three", "unexpected"}
            self.assertFalse(runner.mature_gate(brain, ids)["covered"])
            candidate.episode_ids = set(ids)
            results[0].assembly_activations = (activation,)
            results[-1].assembly_activations = ()
            self.assertFalse(runner.mature_gate(brain, ids)["covered"])
            results[-1].assembly_activations = (activation,)
            activation.suppressed = True
            self.assertFalse(runner.mature_gate(brain, ids)["covered"])
            activation.suppressed = False
            witness["candidate_prototypes"]["a"]["retained_paths"] = []
            self.assertFalse(runner.mature_gate(brain, ids)["covered"])

    def test_both_faults_and_commit_share_real_owner_boundary_in_source(self):
        tree = ast.parse(RUNNER.read_text())
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Probe")
        method = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "execute")
        transaction_calls = [
            n
            for n in ast.walk(method)
            if isinstance(n, ast.Call)
            and isinstance(n.func, ast.Attribute)
            and n.func.attr == "transact"
        ]
        self.assertEqual(
            {n.args[0].id for n in transaction_calls},
            {"prepare_export_abort", "prepare_event_cap_abort", "prepare_commit"},
        )
        copy_calls = [
            n
            for n in ast.walk(method)
            if isinstance(n, ast.Call)
            and isinstance(n.func, ast.Attribute)
            and n.func.attr == "pairwise_copies"
        ]
        self.assertEqual(len(copy_calls), 1)
        self.assertLess(copy_calls[0].lineno, min(n.lineno for n in transaction_calls))
        mutations = [
            n
            for n in ast.walk(method)
            if isinstance(n, ast.Call)
            and isinstance(n.func, ast.Attribute)
            and n.func.attr == "mutate_after_return"
        ]
        self.assertEqual(len(mutations), 1)
        self.assertGreater(mutations[0].lineno, max(n.lineno for n in transaction_calls))

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

    def test_timeout_parent_contract_and_python_audit_denials(self):
        good = b"\0".join([b"timeout", b"-s", b"KILL", b"120s", b"python", b"-B"])
        with patch.object(Path, "read_bytes", return_value=good):
            self.assertEqual(
                runner.verify_timeout_parent()["parent_argv"][1:4], ["-s", "KILL", "120s"]
            )
        with patch.object(Path, "read_bytes", return_value=b"python\0-B"):
            with self.assertRaisesRegex(runner.BindingError, "actual timeout"):
                runner.verify_timeout_parent()
        for event in (
            "socket.connect",
            "socket.getaddrinfo",
            "subprocess.Popen",
            "os.fork",
            "os.exec",
            "ctypes.dlopen",
        ):
            with self.assertRaises(PermissionError):
                runner.deny_network_and_subprocess(event, ())
        runner.deny_network_and_subprocess("open", ())

    def test_finalization_uses_remaining_hard_limit_not_extra_budget(self):
        budget = runner.Budget()
        with (
            patch.object(runner.resource, "setrlimit") as limits,
            patch.object(runner.signal, "setitimer") as timer,
        ):
            budget.finish()
        self.assertEqual(limits.call_args.args, (runner.resource.RLIMIT_CPU, (60, 60)))
        self.assertGreater(timer.call_args.args[1], 0)
        self.assertLessEqual(timer.call_args.args[1], 120)


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
                    check=True, capture_output=True, text=True,
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
                    check=True, capture_output=True, text=True,
                )


if __name__ == "__main__":
    unittest.main()
