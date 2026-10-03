"""Synthetic metadata tests only: no engine, model, experiment or network access."""

from __future__ import annotations

import hashlib
import importlib.util
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


if __name__ == "__main__":
    unittest.main()
