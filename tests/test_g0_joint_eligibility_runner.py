"""All execution tests are MODEL-FREE; every SparkBrain import is a tripwire."""
from __future__ import annotations

import builtins
import copy
import gc
import hashlib
import importlib
import json
import random
import subprocess
import sys
import tempfile
import threading
import time
import unittest
import weakref
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from scripts.g0_joint_ownership import ResourceBoundary, SerialOwner, SourceRegistry, TypeSpec
from scripts.run_g0_joint_eligibility import (
    ARTIFACT_ROOT,
    EXPECTED,
    BindingError,
    ExecutionEngine,
    InvariantError,
    detach,
    execute_reviewed,
    load_real_runtime,
    mutate_primitive_tree,
    normalize_plan,
    validate_export,
)

ROOT = Path(__file__).resolve().parents[1]


class MemoryWriter:
    def __init__(self, fail_at=None):
        self.rows = {}
        self.fail_at = fail_at

    def raw_json(self, name, value):
        if name == self.fail_at:
            raise OSError("injected evidence write failure")
        if name in self.rows:
            raise AssertionError("duplicate evidence filename: " + name)
        self.rows[name] = json.loads(json.dumps(value))


class NoLimitBudget:
    def __init__(self):
        self.failure = False

    def check(self):
        if self.failure:
            raise KeyboardInterrupt("sticky budget failure")

    def sample(self):
        return {"model_free": True}


class ModelFreeRaw:
    def __init__(self):
        self.state = []
        self.rng = random.Random(0)


class ModelFreeFacade:
    registry = weakref.WeakKeyDictionary()
    guard = threading.Lock()

    def __init__(self, *, base):
        self._brain = base
        with self.guard:
            self._step_lock = self.registry.get(base)
            if self._step_lock is None:
                self._step_lock = threading.RLock()
                self.registry[base] = self._step_lock


class ModelFreeRuntime:
    """Primitive transaction stand-in; no production model or native checkpoint use."""

    def __init__(self, *, resources=False, output_alias=False, wrong_reference=False):
        self.calls = []
        self.resources = resources
        self.output_alias = output_alias
        self.wrong_reference = wrong_reference
        self.feedback = 0
        self.scope = 0
        self.observes = 0
        self.query_input_ids = []

    def construct_producer(self):
        self.calls.append("producer_init")
        return {"history": [], "pulses": []}

    def construct_m1(self):
        self.calls.append("m1_init")
        result = {"history": [], "pending": None, "receipts": {}}
        if self.resources:
            result["facade"] = ModelFreeFacade(base=ModelFreeRaw())
        return result

    @staticmethod
    def capacity(root):
        return 8

    @staticmethod
    def freeze_dictionary(root):
        return {"binding": {"N": 1, "canonical_prototypes": ["stand-in"]},
                "coordinates": [{"assembly_id": "stand-in"}], "collisions": []}

    def process(self, root, observation, *, acquisition):
        self.calls.append("process")
        if not acquisition:
            self.query_input_ids.append(observation["occurrence_id"])
        callers = copy.deepcopy(observation["pulses"])
        owned = copy.deepcopy(callers)
        root["producer"]["history"].append(observation["occurrence_id"])
        root["producer"]["pulses"] = owned
        root["clock"]["decision_ms"] = observation["start_ms"] + 72.0
        raw = {"result": {"decision_ms": root["clock"]["decision_ms"]},
               "observation": copy.deepcopy(observation)}
        if not acquisition:
            raw["export"] = {"schema": "v05-history-export-1",
                             "occurrence_id": observation["occurrence_id"],
                             "decision_ms": root["clock"]["decision_ms"], "accepted": True,
                             "status": "accepted_match", "features": [1.0],
                             "binding": copy.deepcopy(root["dictionary"]["binding"])}
        if self.output_alias:
            raw["bad_alias"] = root["producer"]["history"]
        return {"raw": raw, "caller_pulses": callers, "caller_sensory": None}

    def observe(self, root, exported, external):
        self.calls.append("observe")
        self.observes += 1
        sensory = {"signal": 0.1, "assembly_000": 1.0}
        external["caller_sensory"] = sensory
        native = {"id": exported["occurrence_id"], "sensory": copy.deepcopy(sensory),
                  "time": exported["decision_ms"] / 1000.0}
        if self.wrong_reference and self.observes == 5:
            native["drift"] = True
        root["m1"]["pending"] = native
        root["m1"]["history"].append(native)
        root["pending"] = {"native_export": detach(exported), "event_id": native["id"]}
        return {"event_id": native["id"], "decision": "abstain"}

    def outcome(self, root, receipt, *, fault=False):
        self.calls.append("outcome")
        old = root["m1"]["receipts"].get(receipt["receipt_id"])
        if old is not None:
            if old["receipt"] != receipt:
                raise ValueError("receipt identity conflict")
            return copy.deepcopy(old["revision"])
        self.feedback += 1
        if fault:
            if self.resources:
                oldbase = root["m1"]["facade"]._brain
                replacement = ModelFreeRaw()
                replacement.state = copy.deepcopy(oldbase.state)
                replacement.rng.setstate(oldbase.rng.getstate())
                root["m1"]["facade"] = ModelFreeFacade(base=replacement)
            raise RuntimeError("injected after predictive revision")
        self.scope += 1
        revision = {"committed": True, "receipt_id": receipt["receipt_id"]}
        root["m1"]["receipts"][receipt["receipt_id"]] = {
            "receipt": detach(receipt), "revision": detach(revision)}
        root["receipts"][receipt["receipt_id"]] = {
            "receipt": detach(receipt), "pending": root["pending"], "revision": detach(revision)}
        root["pending"] = None
        root["m1"]["pending"] = None
        return revision

    @staticmethod
    def nonempty(root):
        return bool(root["m1"]["history"] and root["m1"]["receipts"] and root["receipts"])

    @staticmethod
    def external_snapshot(external):
        return copy.deepcopy(external)

    @staticmethod
    def mutate_external(external):
        for pulse in external["caller_pulses"]:
            pulse["metadata"]["caller_after_preservation"] = [991]
        if external["caller_sensory"] is not None:
            external["caller_sensory"]["signal"] = -999.0
        mutate_primitive_tree(external["raw"])


def input_plan():
    return json.loads((ROOT / ARTIFACT_ROOT / "inputs.json").read_text())


def standin_registry():
    return SourceRegistry((TypeSpec(ModelFreeRaw, "stand-in:raw", ("state", "rng")),
                           TypeSpec(ModelFreeFacade, "stand-in:facade", ("_brain", "_step_lock")),
                           TypeSpec(random.Random, "stand-in:rng", ("gauss_next",))))


class G0RunnerTests(unittest.TestCase):
    def setUp(self):
        self.imports = []
        original_import = builtins.__import__
        original_import_module = importlib.import_module

        def guarded_import(name, *args, **kwargs):
            if name == "sparkbrain" or name.startswith("sparkbrain."):
                self.imports.append(name)
                raise AssertionError("real import forbidden in source-only test: " + name)
            return original_import(name, *args, **kwargs)

        def guarded_module(name, *args, **kwargs):
            if name == "sparkbrain" or name.startswith("sparkbrain."):
                self.imports.append(name)
                raise AssertionError("real import forbidden in source-only test: " + name)
            return original_import_module(name, *args, **kwargs)

        self.addCleanup(patch.stopall)
        patch("builtins.__import__", side_effect=guarded_import).start()
        patch("importlib.import_module", side_effect=guarded_module).start()

    def tearDown(self):
        self.assertEqual(self.imports, [])

    def make_engine(self, runtime=None, writer=None, plan=None):
        return ExecutionEngine(runtime or ModelFreeRuntime(), SourceRegistry(()), None,
                               writer or MemoryWriter(), NoLimitBudget(), plan or input_plan())

    def test_complete_fixed_plan_is_only_model_free(self):
        engine = self.make_engine()
        result = engine.execute()
        self.assertEqual(result["actual"], EXPECTED)
        self.assertEqual(result["owner_generation"], 4)
        self.assertEqual(engine.runtime.feedback, 4)
        self.assertEqual(engine.runtime.scope, 3)
        self.assertEqual(engine.runtime.observes, 5)
        self.assertEqual(engine.runtime.query_input_ids,
                         ["g0-20261002-000064"] + ["g0-20261002-000065"] * 5)
        self.assertFalse(engine.live)
        self.assertFalse(engine.candidates)
        self.assertIsNone(engine.pointer)
        names = list(engine.writer.rows)
        self.assertEqual(result["runtime_domain"], "SYNTHETIC_MODEL_FREE")
        for number in (5, 6):
            self.assertTrue(engine.writer.rows[
                f"case-{number:02d}-abort-expected-failure.json"]["matched"])
        self.assertLess(names.index("case-07-invalid-export-before-validation.json"),
                        names.index("case-07-export-expected-failure.json"))
        disposals = [name for name in names if name.endswith("-disposed.json")]
        self.assertEqual(disposals, [f"candidate-{i:02d}-disposed.json" for i in
                                    (4, 3, 5, 6, 7, 8, 10, 11, 13, 14, 12, 9, 2, 1)])
        for number in (1, 2, 9, 12):
            self.assertLess(names.index(f"candidate-{number:02d}-publish-ready-witness.json"),
                            names.index(f"candidate-{number:02d}-publication.json"))

    def test_full_plan_with_real_locks_but_model_free_facades_and_rollback(self):
        gc.collect()
        self.assertFalse(ModelFreeFacade.registry)
        runtime = ModelFreeRuntime(resources=True)
        writer = MemoryWriter()
        with SerialOwner() as owner:
            def execute():
                boundary = ResourceBoundary(
                    owner, ModelFreeFacade.registry, ModelFreeFacade.guard,
                    raw_type=ModelFreeRaw, facade_type=ModelFreeFacade,
                    facade_factory=ModelFreeFacade, factory_source_tag="stand-in:facade")
                engine = ExecutionEngine(runtime, standin_registry(), boundary,
                                         writer, NoLimitBudget(), input_plan())
                return engine.execute()
            result = owner.call(execute)
        self.assertEqual(result["case_count"], 14)
        self.assertFalse(ModelFreeFacade.registry)

    def test_failed_resource_case_cleans_up_before_owner_thread_closes(self):
        gc.collect()
        self.assertFalse(ModelFreeFacade.registry)
        with SerialOwner() as owner:
            def execute_and_cleanup():
                boundary = ResourceBoundary(
                    owner, ModelFreeFacade.registry, ModelFreeFacade.guard,
                    raw_type=ModelFreeRaw, facade_type=ModelFreeFacade,
                    facade_factory=ModelFreeFacade, factory_source_tag="stand-in:facade")
                engine = ExecutionEngine(ModelFreeRuntime(resources=True), standin_registry(),
                                         boundary, MemoryWriter("candidate-09-publication.json"),
                                         NoLimitBudget(), input_plan())
                try:
                    engine.execute()
                except OSError as error:
                    error.__traceback__ = None
                    result = engine.abort_cleanup()
                    return result, len(boundary.ledger().bindings)
                raise AssertionError("planned writer failure did not occur")
            cleanup, resources = owner.call(execute_and_cleanup)
        self.assertEqual(cleanup["status"], "verified")
        self.assertEqual(cleanup["disposed_lifo"], [9, 2, 1])
        self.assertTrue(cleanup["all_runner_strong_roots_released"])
        self.assertEqual(resources, 0)
        self.assertFalse(ModelFreeFacade.registry)

    def test_publication_write_failure_keeps_old_owner_pointer(self):
        writer = MemoryWriter(fail_at="candidate-09-publication.json")
        engine = self.make_engine(writer=writer)
        with self.assertRaisesRegex(OSError, "evidence"):
            engine.execute()
        self.assertEqual(engine.pointer[1], 2)
        self.assertIs(engine.pointer[0], engine.live["candidate-02"])
        self.assertNotIn("plan-complete-before-cleanup.json", writer.rows)
        self.assertEqual(engine.counts["m1.apply_outcome"], 1)

    def test_output_alias_is_detected_before_mutation_or_any_m1_observation(self):
        runtime = ModelFreeRuntime(output_alias=True)
        engine = self.make_engine(runtime=runtime)
        with self.assertRaisesRegex(InvariantError, "aliases owner"):
            engine.execute()
        self.assertEqual(engine.counts["producer.process_episode"], 1)
        self.assertEqual(engine.counts["m1.observe"], 0)
        self.assertNotIn("caller_after_preservation", engine.live["initial"]["producer"])

    def test_observe_reference_mismatch_stops_without_publication(self):
        engine = self.make_engine(runtime=ModelFreeRuntime(wrong_reference=True))
        with self.assertRaisesRegex(InvariantError, "reference full graph"):
            engine.execute()
        self.assertEqual(engine.pointer[1], 2)
        self.assertNotIn("candidate-09-publication.json", engine.writer.rows)

    def test_malformed_literal_rejects_before_constructors(self):
        plan = input_plan()
        plan["acquisition"][0]["unexpected"] = 0
        runtime = ModelFreeRuntime()
        with self.assertRaisesRegex(BindingError, "schema"):
            self.make_engine(runtime=runtime, plan=plan)
        self.assertEqual(runtime.calls, [])

    def test_branches_cannot_change_query_shape_or_event_id(self):
        for change in ("time", "event", "magnitude"):
            with self.subTest(change=change):
                plan = input_plan()
                row = plan["queries"]["reference_observe"]
                if change == "time":
                    row["start_ms"] += 1
                elif change == "event":
                    row["occurrence_id"] = "different"
                else:
                    row["pulses"][0]["magnitude"] += 0.1
                with self.assertRaisesRegex(BindingError, "identical literal"):
                    normalize_plan(plan)

    def test_no_extra_acquisition_or_outcome_change(self):
        plan = input_plan()
        plan["acquisition"].append(copy.deepcopy(plan["acquisition"][-1]))
        with self.assertRaisesRegex(BindingError, "64 literal"):
            normalize_plan(plan)
        plan = input_plan()
        plan["receipts"]["teach"]["outcome"] = -0.8
        with self.assertRaisesRegex(BindingError, "receipt"):
            normalize_plan(plan)

    def test_native_capacity_includes_base_signal(self):
        row = {"schema": "v05-history-export-1", "occurrence_id": "model-free",
               "decision_ms": 0.0, "accepted": True, "status": "accepted_match",
               "features": [0.0] * 8, "binding": {"N": 8}}
        with self.assertRaisesRegex(BindingError, "capacity"):
            validate_export(row, {"binding": {"N": 8}}, capacity=8)

    def test_call_ceiling_checked_before_operation_body(self):
        engine = self.make_engine()
        engine.counts["m1.observe"] = EXPECTED["m1.observe"]
        calls = []
        with self.assertRaisesRegex(InvariantError, "ceiling"):
            engine.call("m1.observe", lambda: calls.append(True))
        self.assertEqual(calls, [])

    def test_budget_failure_never_counts_as_expected_fault(self):
        engine = self.make_engine()
        def fail():
            engine.budget.failure = True
            raise RuntimeError("injected after predictive revision")
        with self.assertRaisesRegex(KeyboardInterrupt, "sticky"):
            engine.expected_failure("sticky", fail, RuntimeError, "injected")

    def test_gate_denies_missing_or_forged_permit_before_native_import(self):
        from scripts.g0_execution_support import AdmissionError, ExecutionPermit
        for permit in (None, object(), object.__new__(ExecutionPermit)):
            with self.subTest(permit=type(permit).__name__):
                with self.assertRaisesRegex(AdmissionError, "unissued"):
                    load_real_runtime(permit)

    def test_synthetic_driver_failure_and_writer_failure_cleanup_and_one_shot(self):
        # SYNTHETIC ADMISSION ONLY: no real permit is minted, no actual native loader,
        # no resource limits or native profile hooks are installed by this test.
        from contextlib import nullcontext

        from scripts import g0_execution_support as support
        from scripts import run_g0_joint_eligibility as runner

        class SyntheticModelFailure(ModelFreeRuntime):
            def observe(self, root, exported, external):
                result = super().observe(root, exported, external)
                if self.observes == 2:
                    raise RuntimeError("synthetic post-observe model failure")
                return result

        class SyntheticMonitor:
            complete_counts = False
            active = False

            def __init__(self, root, caps, budget, writer):
                self.budget = budget

            def __enter__(self):
                type(self).active = True
                return self

            def __exit__(self, *args):
                type(self).active = False
                return None

            def check(self):
                return self.budget.check()

            def snapshot(self):
                return {"synthetic": True, "counts": (dict(support.CALL_CAPS)
                        if self.complete_counts else dict.fromkeys(support.CALL_CAPS, 0))}

        class SyntheticBudget(support.ResourceBudget):
            def __init__(self):
                # A shared full-suite process can legitimately exceed the real G0
                # envelope. This driver test uses stand-in resource observations.
                super().__init__(sampler=lambda: {"cpu_seconds": 0.0,
                                                 "wall_seconds": 0.0,
                                                 "address_space_bytes": 0})

        class SyntheticFailingWriter(support.ExclusiveEvidenceWriter):
            def raw_json(self, name, value):
                if name == "candidate-09-publication.json":
                    raise OSError("synthetic publication evidence failure")
                return super().raw_json(name, value)

        for fault in ("model", "writer", "late_mapping", "lifecycle", "final_integrity"):
            with self.subTest(fault=fault), tempfile.TemporaryDirectory() as directory:
                output = Path(directory) / "synthetic-only"
                source_files = {ARTIFACT_ROOT + "/" + name: hashlib.sha256(
                    (ROOT / ARTIFACT_ROOT / name).read_bytes()).hexdigest()
                    for name in ("protocol.json", "inputs.json")}
                permit = SimpleNamespace(root=ROOT, output_directory=output,
                                         freeze_path=ROOT / ARTIFACT_ROOT / "inputs.json",
                                         approval_path=ROOT / ARTIFACT_ROOT / "protocol.json",
                                         freeze={"environment": {"synthetic_test_only": True},
                                                 "source_files_sha256": source_files})
                reservation = {"consumed": 0}
                mapping_calls = {"count": 0}
                SyntheticMonitor.complete_counts = fault in {
                    "late_mapping", "lifecycle", "final_integrity"}
                validation_calls = []
                observed_owner_closed = []
                original_cleanup = ExecutionEngine.abort_cleanup

                def synthetic_consume(value, destination, *, budget, permit=permit,
                                      output=output, reservation=reservation):
                    self.assertIs(value, permit)
                    self.assertEqual(destination, output)
                    if reservation["consumed"]:
                        raise support.AdmissionError("synthetic permit already consumed")
                    reservation["consumed"] += 1

                def boundary(owner, modules):
                    return ResourceBoundary(
                        owner, ModelFreeFacade.registry, ModelFreeFacade.guard,
                        raw_type=ModelFreeRaw, facade_type=ModelFreeFacade,
                        facade_factory=ModelFreeFacade, factory_source_tag="stand-in:facade")

                def cleanup(engine, observed_owner_closed=observed_owner_closed,
                            original_cleanup=original_cleanup):
                    observed_owner_closed.append(engine.resources.owner._closed)
                    return original_cleanup(engine)

                def synthetic_mapping_check(environment, calls=mapping_calls,
                                            fault=fault, **kwargs):
                    calls["count"] += 1
                    if fault == "late_mapping" and calls["count"] == 2:
                        raise support.AdmissionError("synthetic late mapped-library drift")
                    return {"synthetic_mapping_check": "no_native_library_admission"}

                def synthetic_lifecycle_check(snapshot, fault=fault):
                    self.assertTrue(snapshot["synthetic"])
                    if fault == "lifecycle":
                        raise support.AdmissionError("synthetic incomplete lifecycle")
                    return {"synthetic_lifecycle_admission_only": True}

                def synthetic_validation(value, *, checkpoint, fault=fault,
                                         calls=validation_calls, permit=permit):
                    self.assertIs(value, permit)
                    self.assertFalse(SyntheticMonitor.active)
                    checkpoint()
                    calls.append("unprofiled validation")
                    if fault == "final_integrity" and len(calls) == 2:
                        raise support.AdmissionError("synthetic final environment drift")

                runtime = (SyntheticModelFailure(resources=True) if fault == "model"
                           else ModelFreeRuntime(resources=True))
                writer_class = (SyntheticFailingWriter if fault == "writer"
                                else support.ExclusiveEvidenceWriter)
                with patch.object(sys, "pycache_prefix", None), \
                        patch.object(support, "require_execution_permit", synthetic_validation), \
                        patch.object(support, "consume_execution_permit", synthetic_consume), \
                        patch.object(support, "runtime_admission",
                                     side_effect=lambda *args: nullcontext(object())), \
                        patch.object(support, "install_runtime_limits", return_value={
                            "synthetic_no_limits_installed": True,
                            "started_monotonic_seconds": time.monotonic()}), \
                        patch.object(support, "verify_mapped_libraries", synthetic_mapping_check), \
                        patch.object(support, "ResourceBudget", SyntheticBudget), \
                        patch.object(support, "validate_completed_lifecycle",
                                     synthetic_lifecycle_check), \
                        patch.object(support, "PassiveCallMonitor", SyntheticMonitor), \
                        patch.object(support, "ExclusiveEvidenceWriter", writer_class), \
                        patch.object(runner, "load_real_runtime", return_value=(
                            runtime, standin_registry(), {})), \
                        patch.object(runner, "native_resource_boundary", boundary), \
                        patch.object(ExecutionEngine, "abort_cleanup", cleanup):
                    terminal = execute_reviewed(permit, output)
                    validations_before_retry = len(validation_calls)
                    with self.assertRaisesRegex(support.AdmissionError, "already consumed"):
                        execute_reviewed(permit, output)
                self.assertIsNotNone(terminal["failure"])
                self.assertIsNone(terminal["result"])
                saved = json.loads((output / "TERMINAL.json").read_text())
                self.assertEqual(saved["status"], "STOPPED")
                if fault in {"late_mapping", "lifecycle", "final_integrity"}:
                    self.assertEqual(mapping_calls["count"], 2 if fault == "late_mapping" else 1)
                    expected = {"late_mapping": "mapped-library drift",
                                "lifecycle": "lifecycle",
                                "final_integrity": "final environment drift"}[fault]
                    self.assertIn(expected, terminal["failure"]["message"])
                    self.assertTrue(json.loads((output / "final-cleanup.json").read_text())[
                        "all_live_roots_released"])
                    self.assertFalse((output / "failure-owner-cleanup.json").exists())
                    self.assertEqual(observed_owner_closed, [])
                else:
                    self.assertEqual(mapping_calls["count"], 1)
                    saved_cleanup = json.loads((output / "failure-owner-cleanup.json").read_text())
                    self.assertEqual(saved_cleanup["status"], "verified")
                    self.assertTrue(saved_cleanup["all_runner_strong_roots_released"])
                    self.assertEqual(observed_owner_closed, [False])
                self.assertEqual(validations_before_retry,
                                 2 if fault in {"late_mapping", "final_integrity"} else 1)
                self.assertFalse(ModelFreeFacade.registry)
                self.assertEqual(reservation["consumed"], 1)
                self.assertFalse((output / "engineering-verdict.json").exists())

    def test_execution_orchestrator_rejects_before_output_or_native_loading(self):
        from scripts.g0_execution_support import AdmissionError
        with self.assertRaisesRegex(AdmissionError, "unissued"):
            execute_reviewed(None, ROOT / "never-created-model-free-output")
        self.assertFalse((ROOT / "never-created-model-free-output").exists())

    def test_negative_cases_are_all_recorded_before_first_constructor(self):
        writer = MemoryWriter(fail_at="attempt-001.json")
        runtime = ModelFreeRuntime()
        engine = self.make_engine(runtime=runtime, writer=writer)
        with self.assertRaisesRegex(OSError, "write failure"):
            engine.execute()
        self.assertEqual(runtime.calls, [])
        self.assertEqual(writer.rows["negative-preflight.json"]["case_count"], 5)
        for name in ("malformed_primitive_pulse", "privileged_sensory_name", "nonfinite_export",
                     "native_coordinate_capacity_exceeds_actual_M1_headroom", "schema_mismatch"):
            self.assertIn("negative-" + name + "-input.json", writer.rows)
            self.assertTrue(writer.rows["negative-" + name + "-expected-failure.json"]["matched"])

    def test_cli_default_root_preserves_symlink_for_common_guard_rejection(self):
        from scripts import run_g0_joint_eligibility as runner

        with tempfile.TemporaryDirectory() as directory:
            real = Path(directory) / "real"
            real.mkdir()
            (real / "nested").mkdir()
            alias = Path(directory) / "alias"
            alias.symlink_to(real, target_is_directory=True)
            for candidate_root in (alias, alias / "nested"):
                with self.subTest(root=str(candidate_root)), \
                        patch.object(runner, "__file__", str(
                            candidate_root / "scripts" / "run_g0_joint_eligibility.py")), \
                        patch.object(sys, "argv", ["runner", "--check-source"]):
                    with self.assertRaisesRegex(ValueError, "symlink"):
                        runner.main()

    def test_module_import_does_not_import_runtime(self):
        code = """import sys
class BlockNative:
    def find_spec(self, name, path=None, target=None):
        if name == 'sparkbrain' or name.startswith('sparkbrain.'):
            raise AssertionError('native runtime imported by source-only runner')
sys.meta_path.insert(0, BlockNative())
from scripts import run_g0_joint_eligibility
assert not any(n == 'sparkbrain' or n.startswith('sparkbrain.') for n in sys.modules)
"""
        result = subprocess.run([sys.executable, "-B", "-s", "-c", code], cwd=ROOT,
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(EXPECTED["clone_joint"], 14)


if __name__ == "__main__":
    unittest.main()
