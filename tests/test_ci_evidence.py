"""Synthetic metadata tests only: no engine, model, experiment or network access."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "write_ci_evidence.py"
SPEC = importlib.util.spec_from_file_location("write_ci_evidence", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CiEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in (*MODULE.INPUT_PATHS, MODULE.MANIFEST_PATH):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("{}\n", encoding="utf-8")
        self.context = {
            "repository": "example/research",
            "event_name": "push",
            "event_sha": "a" * 40,
            "pull_request_head_sha": "",
            "run_id": "123",
            "run_attempt": "1",
            "matrix_python": "3.11",
        }
        self.steps = dict.fromkeys(MODULE.STEP_NAMES, "success")
        self.runtime = {
            "implementation": "CPython", "python": "3.11.16",
            "system": "Linux", "machine": "x86_64",
        }

    def record(self, **overrides: object) -> dict[str, object]:
        args = {
            "root": self.root, "context": self.context, "steps": self.steps,
            "checkout_sha": "a" * 40, "checkout_tree": "b" * 40,
            "tracked_source_unchanged": True, "runtime": self.runtime,
        }
        args.update(overrides)
        return MODULE.build_record(**args)

    def test_success_records_only_engineering_scope(self) -> None:
        record = self.record()
        self.assertTrue(record["configured_checks_passed"])
        self.assertEqual(set(record["input_sha256"]), set(MODULE.INPUT_PATHS))
        self.assertTrue(all(value is False for value in record["scope"].values()))
        expected = hashlib.sha256(b"{}\n").hexdigest()
        self.assertEqual(record["generated_validation_manifest_sha256"], expected)
        self.assertIsNone(record["source"]["pull_request_head_sha"])

    def test_pull_request_keeps_merge_checkout_distinct_from_head(self) -> None:
        self.context.update(event_name="pull_request", pull_request_head_sha="c" * 40)
        source = self.record()["source"]
        self.assertEqual(source["checkout_sha"], "a" * 40)
        self.assertEqual(source["pull_request_head_sha"], "c" * 40)

    def test_both_python_matrix_jobs_can_report_success(self) -> None:
        self.context["matrix_python"] = "3.13"
        self.runtime["python"] = "3.13.9"
        self.assertTrue(self.record()["configured_checks_passed"])

    def test_mismatched_checkout_python_or_dirty_source_is_not_success(self) -> None:
        for overrides in (
            {"checkout_sha": "c" * 40},
            {"tracked_source_unchanged": False},
            {"runtime": {**self.runtime, "python": "3.13.9"}},
        ):
            with self.subTest(overrides=overrides):
                self.assertFalse(self.record(**overrides)["configured_checks_passed"])

    def test_failure_cancellation_and_skip_never_claim_success(self) -> None:
        for status in ("failure", "cancelled", "skipped"):
            with self.subTest(status=status):
                self.steps["tests"] = status
                self.steps["validate_bundle"] = "skipped"
                record = self.record()
                self.assertFalse(record["configured_checks_passed"])
                self.assertIsNone(record["generated_validation_manifest_sha256"])

    def test_skipped_validation_does_not_hash_old_or_missing_output(self) -> None:
        (self.root / MODULE.MANIFEST_PATH).unlink()
        self.steps["validate_bundle"] = "skipped"
        self.assertIsNone(self.record()["generated_validation_manifest_sha256"])

    def test_successful_validation_requires_output_file(self) -> None:
        (self.root / MODULE.MANIFEST_PATH).unlink()
        with self.assertRaises(ValueError):
            self.record()

    def test_allowlisted_file_cannot_be_a_symlink(self) -> None:
        target = self.root / MODULE.MANIFEST_PATH
        target.unlink()
        target.symlink_to(self.root / "pyproject.toml")
        with self.assertRaises(ValueError):
            self.record()

    def test_unknown_context_field_is_rejected(self) -> None:
        self.context["secret"] = "do-not-publish"
        with self.assertRaises(ValueError):
            self.record()

    def test_missing_unknown_or_unfinished_steps_are_rejected(self) -> None:
        for steps in (
            {name: value for name, value in self.steps.items() if name != "lint"},
            {**self.steps, "secret_step": "success"},
            {**self.steps, "tests": "running"},
        ):
            with self.subTest(steps=steps), self.assertRaises(ValueError):
                self.record(steps=steps)

    def test_bad_identifiers_and_non_pr_head_are_rejected(self) -> None:
        for update in (
            {"event_sha": "main"},
            {"repository": "example/research\nsecret"},
            {"run_id": "0"},
            {"run_attempt": "-1"},
            {"event_name": "workflow_dispatch"},
            {"pull_request_head_sha": "c" * 40},
        ):
            with self.subTest(update=update), self.assertRaises(ValueError):
                self.record(context={**self.context, **update})

    def test_missing_pr_head_is_rejected(self) -> None:
        self.context["event_name"] = "pull_request"
        with self.assertRaises(ValueError):
            self.record()

    def test_extra_runtime_field_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.record(runtime={**self.runtime, "home": "/private"})

    def test_git_error_cannot_be_reported_as_clean(self) -> None:
        with patch.object(MODULE.subprocess, "run") as run:
            run.return_value.stdout = "a" * 40
            run.return_value.returncode = 128
            with self.assertRaises(ValueError):
                MODULE.git_identity(self.root)

    def test_preexisting_output_cannot_signal_collector_success(self) -> None:
        output, step_output = self.root / "record.json", self.root / "step-output"
        output.write_text("private-preexisting-bytes", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            MODULE.publish_record(self.record(), output, step_output)
        self.assertEqual(output.read_text(encoding="utf-8"), "private-preexisting-bytes")
        self.assertFalse(step_output.exists())

    def test_created_success_and_failure_records_have_separate_check_status(self) -> None:
        for status, expected in (("success", "true"), ("failure", "false")):
            with self.subTest(status=status):
                self.steps["tests"] = status
                output = self.root / f"record-{status}.json"
                step_output = self.root / f"step-output-{status}"
                MODULE.publish_record(self.record(), output, step_output)
                self.assertTrue(output.is_file())
                self.assertEqual(
                    step_output.read_text(encoding="utf-8"),
                    f"configured_checks_passed={expected}\n",
                )

    def test_output_error_does_not_signal_creation(self) -> None:
        output, step_output = self.root / "existing-directory", self.root / "step-output"
        output.mkdir()
        with self.assertRaises(OSError):
            MODULE.publish_record(self.record(), output, step_output)
        self.assertFalse(step_output.exists())

    def transfer(self, record: dict[str, object]) -> dict[str, object]:
        return MODULE.validate_transferred_record(
            json.dumps(record), self.root, self.context, "a" * 40, "b" * 40,
        )

    def test_transferred_success_and_negative_records_round_trip(self) -> None:
        for status in ("success", "failure"):
            with self.subTest(status=status):
                self.steps["tests"] = status
                self.assertEqual(self.transfer(self.record()), self.record())

    def test_matrix_job_outputs_have_distinct_keys_and_no_file_transfer(self) -> None:
        for minor, key in (("3.11", "py311"), ("3.13", "py313")):
            with self.subTest(minor=minor):
                self.context["matrix_python"] = minor
                self.runtime["python"] = f"{minor}.9"
                output = self.root / f"job-output-{key}"
                MODULE.emit_job_record(self.record(), output)
                line, status = output.read_text(encoding="utf-8").splitlines()
                name, raw = line.split("=", 1)
                self.assertEqual(name, key)
                self.assertEqual(status, "configured_checks_passed=true")
                # A producer-side replacement file is irrelevant to consumer reconstruction.
                (self.root / "ci-evidence.json").write_text("private-bytes", encoding="utf-8")
                self.assertEqual(
                    MODULE.validate_transferred_record(
                        raw, self.root, self.context, "a" * 40, "b" * 40,
                    ),
                    self.record(),
                )

    def test_transfer_rejects_unknown_fields_wrong_identity_and_claim_changes(self) -> None:
        updates = (
            {"secret": "private"},
            {"repository": "other/repository"},
            {"run_id": "456"},
            {"matrix_python": "3.13"},
            {"schema_version": True},
            {"scope": {**self.record()["scope"], "local_reproduction_verified": True}},
            {"source": {**self.record()["source"], "checkout_sha": "c" * 40}},
            {"source": {**self.record()["source"], "secret": "private"}},
            {"input_sha256": dict.fromkeys(MODULE.INPUT_PATHS, "c" * 64)},
            {"generated_validation_manifest_sha256": "private-data"},
            {"generated_validation_manifest_sha256": None},
            {"runtime": {**self.runtime, "machine": "private-data"}},
            {"step_outcomes": {**self.steps, "tests": ["success"]}},
        )
        for update in updates:
            with self.subTest(update=update), self.assertRaises(ValueError):
                self.transfer({**self.record(), **update})

    def test_transfer_requires_matching_input_hashes(self) -> None:
        record = self.record()
        (self.root / "pyproject.toml").write_text("# source changed\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.transfer(record)

    def test_transfer_rejects_empty_oversized_duplicate_and_nonobject_json(self) -> None:
        for raw in ("", " " * 8193, "[]", '{"run_id":"1","run_id":"2"}'):
            with self.subTest(raw_length=len(raw)), self.assertRaises(ValueError):
                MODULE.validate_transferred_record(
                    raw, self.root, self.context, "a" * 40, "b" * 40,
                )


if __name__ == "__main__":
    unittest.main()
