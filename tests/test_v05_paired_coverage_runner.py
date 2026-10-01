"""Model-free runner tests. Never import/construct SparkBrain or execute the probe.

Run this file with unittest (not broad repository test discovery). A meta-path
sentinel also rejects accidental SparkBrain imports in these tests.
"""
from __future__ import annotations

import ast
import dataclasses
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts/v05_paired_coverage_probe.py"


class RejectSparkBrain:
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "sparkbrain" or fullname.startswith("sparkbrain."):
            raise AssertionError("MODEL IMPORT FORBIDDEN in model-free tests")
        return None


SENTINEL = RejectSparkBrain()
sys.meta_path.insert(0, SENTINEL)
SPEC = importlib.util.spec_from_file_location("paired_coverage_runner", RUNNER)
runner = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = runner
try:
    SPEC.loader.exec_module(runner)
finally:
    sys.meta_path.remove(SENTINEL)


@dataclasses.dataclass
class MockConfig:
    flag: bool = True
    threshold: float = 0.76


class RunnerModelFreeTests(unittest.TestCase):
    def setUp(self):
        self.modules_before = set(sys.modules)
        sys.meta_path.insert(0, SENTINEL)

    def tearDown(self):
        sys.meta_path.remove(SENTINEL)
        self.assertFalse(any(n == "sparkbrain" or n.startswith("sparkbrain.")
                             for n in set(sys.modules) - self.modules_before))

    def test_source_check_rejects_model_imports(self):
        code = '''
import importlib.abc, runpy, sys
class Reject(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == 'sparkbrain' or fullname.startswith('sparkbrain.'):
            raise AssertionError('model import forbidden')
sys.meta_path.insert(0, Reject())
sys.argv = [sys.argv[1], '--check-source']
runpy.run_path(sys.argv[0], run_name='__main__')
'''
        result = subprocess.run([sys.executable, "-B", "-c", code, str(RUNNER)],
                                capture_output=True, text=True, check=True)
        value = json.loads(result.stdout)
        self.assertEqual(value["source_files"], 27)
        self.assertFalse(value["model_imported"])
        self.assertEqual(value["protocol_sha256"], runner.PROTOCOL_SHA256)

    def test_module_imports_are_stdlib_and_unique_execution_sites(self):
        tree = ast.parse(RUNNER.read_text())
        for node in tree.body:
            if isinstance(node, ast.Import):
                names = [alias.name.split(".")[0] for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module.split(".")[0]]
            else:
                continue
            self.assertTrue(set(names) <= sys.stdlib_module_names, names)
        calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)]
        self.assertEqual(sum(isinstance(n.func, ast.Attribute)
                             and n.func.attr == "process_episode" for n in calls), 1)
        self.assertEqual(sum(isinstance(n.func, ast.Name)
                             and n.func.id == "IntegratedV05Brain" for n in calls), 1)
        forbidden = {"learn_outcome", "load_checkpoint", "from_state_dict", "deepcopy"}
        self.assertFalse(any(isinstance(n.func, ast.Attribute)
                             and n.func.attr in forbidden for n in calls))

    def test_protocol_hash_mismatch_fails_before_source_use(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / runner.PROTOCOL_PATH
            path.parent.mkdir(parents=True)
            path.write_text("{}")
            with self.assertRaisesRegex(runner.BindingError, "protocol SHA"):
                runner.read_protocol(root)

    def test_source_hash_mismatch_stops(self):
        original = runner.digest_file
        damaged = "src/sparkbrain/v05/brain.py"

        def digest(path):
            return "0" * 64 if str(path).endswith(damaged) else original(path)

        with patch.object(runner, "digest_file", digest):
            with self.assertRaisesRegex(runner.BindingError, "source hashes mismatch"):
                runner.read_protocol(ROOT)

    def test_complete_freeze_rejects_missing_and_extra_sources(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            package = root / "src/sparkbrain"
            package.mkdir(parents=True)
            source = package / "__init__.py"
            source.write_text("# model-free fixture\n")
            frozen = {
                "schema": "v05-paired-coverage-runner-freeze-1",
                "protocol_sha256": runner.PROTOCOL_SHA256,
                "runner_sha256": runner.digest_file(RUNNER),
                "package_sources_sha256": {"src/sparkbrain/__init__.py":
                                           runner.digest_file(source)},
            }
            path = root / "freeze.json"
            path.write_text(json.dumps(frozen))
            sha = runner.digest_file(path)
            self.assertEqual(runner.verify_freeze(root, path, sha), frozen)
            (package / "extra.py").write_text("# additional source\n")
            with self.assertRaisesRegex(runner.BindingError, "complete package"):
                runner.verify_freeze(root, path, sha)
            with self.assertRaisesRegex(runner.BindingError, "freeze SHA"):
                runner.verify_freeze(root, path, "0" * 64)

    def test_all_twelve_configuration_projections_are_complete_and_typed(self):
        brain = SimpleNamespace()
        for path in runner.CONFIG_PATHS.values():
            node = brain
            parts = path.split(".")
            for key in parts[:-1]:
                if not hasattr(node, key):
                    setattr(node, key, SimpleNamespace())
                node = getattr(node, key)
            setattr(node, parts[-1], MockConfig())
        result = runner.actual_configuration(brain)
        self.assertEqual(len(result), 12)
        self.assertEqual(set(result), set(runner.CONFIG_PATHS))
        self.assertEqual(result["brain"], {"flag": True, "threshold": 0.76})
        self.assertNotEqual(runner.canonical(result["brain"]),
                            runner.canonical({"flag": 1, "threshold": 0.76}))

    def test_no_clobber_and_manifest_hashes_exclude_manifest(self):
        with tempfile.TemporaryDirectory() as folder:
            directory = Path(folder) / "output"
            writer = runner.EvidenceWriter(directory)
            writer.write("raw.json", {"value": [1, 2, 3]})
            original = (directory / "raw.json").read_bytes()
            with self.assertRaises(FileExistsError):
                writer.write("raw.json", {"overwrite": True})
            with self.assertRaises(FileExistsError):
                runner.EvidenceWriter(directory)
            manifest = writer.manifest()
            self.assertNotIn("manifest.json", manifest)
            self.assertTrue(manifest["raw.json"]["complete_json"])
            self.assertEqual(manifest["raw.json"]["sha256"],
                             hashlib.sha256(original).hexdigest())
            self.assertEqual(writer.bytes_written, len(original))
            self.assertEqual((directory / "raw.json").read_bytes(), original)

    def test_partial_output_and_finalization_reserve_stay_inside_limit(self):
        with tempfile.TemporaryDirectory() as folder:
            writer = runner.EvidenceWriter(Path(folder) / "output")
            with patch.dict(runner.LIMITS, artifact_bytes=160), \
                    patch.dict(runner.RESERVE, artifact_bytes=80):
                with self.assertRaises(runner.BudgetError):
                    writer.write("partial.json", {"small": 1, "too_big": "x" * 200})
                self.assertFalse(writer.manifest()["partial.json"]["complete_json"])
                writer.finalizing = True
                writer.write("error.json", {"status": "stopped"})
                self.assertLessEqual(sum(p.stat().st_size for p in writer.directory.iterdir()),
                                     160)

    @staticmethod
    def observation():
        ids = ["target-1", "target-2", "target-3"]
        pending = {"assembly_id": "a", "mature": True, "suppressed": False}
        candidate = {"assembly_id": "a", "episode_ids": ids, "episode_count": 3}
        witness = {"brain_results_are_retained": True,
                   "candidate_prototypes": {"a": {"pattern_matches": [
                       {"result_index": 0, "item_index": 0}]}},
                   "pending_activation_matches": [{"result_index": 2, "item_index": 0}]}
        return {"candidates": {"a": candidate}, "pending_activation": pending,
                "identity_witnesses": witness, "retained_result_episode_ids": ids,
                "suppressed_units": [], "suppressed_assemblies": []}, ids

    def test_target_requires_actual_pending_exact_ids_and_both_aliases(self):
        obs, ids = self.observation()
        self.assertTrue(runner.target_gate(obs, ids)["covered"])
        for failure in ("pending", "ids", "prototype", "activation", "suppression", "third"):
            obs, ids = self.observation()
            if failure == "pending":
                obs["pending_activation"] = None
            elif failure == "ids":
                obs["candidates"]["a"]["episode_ids"] = ["one", "two", "three"]
            elif failure == "prototype":
                obs["identity_witnesses"]["candidate_prototypes"]["a"]["pattern_matches"] = []
            elif failure == "activation":
                obs["identity_witnesses"]["pending_activation_matches"] = []
            elif failure == "suppression":
                obs["pending_activation"]["suppressed"] = True
            else:
                obs["retained_result_episode_ids"] = ids[:2]
            self.assertFalse(runner.target_gate(obs, ids)["covered"], failure)

    def test_first_episode_gate_rejects_each_maturity_violation(self):
        obs = {"candidates": {}, "pending_activation": None}
        result = {"assembly_activations": []}
        self.assertTrue(runner.first_episode_gate(obs, result, 3)["passed"])
        obs["candidates"]["a"] = {"episode_count": 3}
        self.assertFalse(runner.first_episode_gate(obs, result, 3)["passed"])
        obs["candidates"] = {}
        result["assembly_activations"] = [{"mature": True}]
        self.assertFalse(runner.first_episode_gate(obs, result, 3)["passed"])
        result["assembly_activations"] = []
        obs["pending_activation"] = {"mature": False}
        self.assertFalse(runner.first_episode_gate(obs, result, 3)["passed"])

    def test_identity_witnesses_use_is_not_equality(self):
        prototype, activation = [1], [2]
        equal_prototype, equal_activation = [1], [2]
        result = SimpleNamespace(patterns=(prototype,), assembly_activations=(activation,))
        candidate = SimpleNamespace(prototype=prototype)
        brain = SimpleNamespace(results=[result], pending_activation=activation,
                                assemblies=SimpleNamespace(candidates={"a": candidate}))
        good = runner.identity_witnesses(brain, [result])
        self.assertTrue(good["pending_activation_matches"])
        candidate.prototype = equal_prototype
        brain.pending_activation = equal_activation
        bad = runner.identity_witnesses(brain, [result])
        self.assertFalse(bad["pending_activation_matches"])
        self.assertFalse(bad["candidate_prototypes"]["a"]["pattern_matches"])

    def test_audit_denial_is_python_level_and_covers_socket_and_escape_launches(self):
        for event in ("socket.connect", "socket.getaddrinfo", "socket.__new__",
                      "subprocess.Popen", "os.system", "os.exec", "os.fork", "ctypes.dlopen"):
            with self.assertRaises(PermissionError):
                runner.deny_network_and_subprocess(event, ())
        runner.deny_network_and_subprocess("open", ())

    def test_resource_finalization_keeps_hard_bounds(self):
        budget = runner.Budget()
        with patch.object(runner.resource, "setrlimit") as limits, \
                patch.object(runner.signal, "setitimer") as timer:
            budget.finish()
        self.assertEqual(limits.call_args.args,
                         (runner.resource.RLIMIT_CPU, (60, 60)))
        self.assertGreater(timer.call_args.args[1], 0)
        self.assertLessEqual(timer.call_args.args[1], 120)


if __name__ == "__main__":
    unittest.main()
