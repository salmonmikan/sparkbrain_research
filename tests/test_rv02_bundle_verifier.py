"""Fail-closed bundle checks on isolated synthetic temporary directories only."""

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from sparkbrain.research.rv02_scale import ScaleStudyConfig, digest

RUNNER_PATH = Path(__file__).resolve().parents[1] / "scripts" / "run_rv02_development.py"
SPEC = importlib.util.spec_from_file_location("rv02_runner_independent_test", RUNNER_PATH)
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


class BundleVerifierTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="rv02-verifier-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "source"
        self.source.mkdir()
        (self.source / "scripts").mkdir()
        self.source_file = self.source / "scripts" / "run_rv02_development.py"
        self.source_file.write_text("VALUE = 1\n", encoding="utf-8")
        (self.source / "src").mkdir()
        self.extra_source = self.source / "src" / "tiny.py"
        self.extra_source.write_text("OTHER = 2\n", encoding="utf-8")
        self.output = self.root / "bundle"
        self.output.mkdir()
        config = ScaleStudyConfig().state_dict()
        planned = [
            ["disjoint-routes", scale, architecture]
            for scale in (1, 3, 10)
            for architecture in ("field", "reservoir")
        ]
        self.manifest = {
            "protocol": "rv02-development-feasibility-v1",
            "config": config,
            "config_hash": digest(config),
            "planned_cells": planned,
            "formal_execution_allowed": False,
            "comparative_capability_claim_allowed": False,
            "source_hashes": {
                "scripts/run_rv02_development.py": hashlib.sha256(
                    self.source_file.read_bytes()
                ).hexdigest(),
                "src/tiny.py": hashlib.sha256(self.extra_source.read_bytes()).hexdigest(),
            },
            "smoke": True,
            "python": "synthetic-test",
            "platform": "synthetic-test",
            "cell_timeout_seconds": 1,
            "total_timeout_seconds": 6,
            "memory_limit_bytes": 1024**3,
        }
        # A valid incomplete bundle is integrity-verifiable, but never successful science.
        self.rows = [
            {
                "family": family,
                "scale": scale,
                "architecture": architecture,
                "status": "not_started_total_deadline",
            }
            for family, scale, architecture in planned
        ]
        self.summary = {
            "statuses": self.rows.copy(),
            "complete_cell_count": 0,
            "planned_cell_count": 6,
            "scientific_status": "not_evaluated_development_feasibility",
            "formal_execution_allowed": False,
            "comparative_capability_claim_allowed": False,
        }
        self.write_fixture()

    def write_fixture(self):
        raw = "".join(json.dumps(row, sort_keys=True) + "\n" for row in self.rows).encode()
        (self.output / "raw_cells.jsonl").write_bytes(raw)
        self.summary["raw_sha256"] = hashlib.sha256(raw).hexdigest()
        (self.output / "manifest.json").write_text(json.dumps(self.manifest), encoding="utf-8")
        (self.output / "summary.json").write_text(json.dumps(self.summary), encoding="utf-8")

    def verify(self):
        return RUNNER.verify_bundle(self.output, source_root=self.source)

    def test_intact_incomplete_fixture_is_not_mistaken_for_integrity_failure(self):
        self.verify()

    def test_missing_row_rejected_even_with_updated_raw_hash(self):
        self.rows.pop()
        self.write_fixture()
        with self.assertRaises(ValueError):
            self.verify()

    def test_duplicate_identity_rejected_even_with_matching_counts_and_hash(self):
        self.rows[-1] = self.rows[0].copy()
        self.summary["statuses"] = self.rows.copy()
        self.write_fixture()
        with self.assertRaises(ValueError):
            self.verify()

    def test_raw_hash_drift_rejected(self):
        self.summary["raw_sha256"] = "0" * 64
        (self.output / "summary.json").write_text(json.dumps(self.summary), encoding="utf-8")
        with self.assertRaises(ValueError):
            self.verify()

    def test_source_manifest_mismatch_rejected(self):
        self.source_file.write_text("VALUE = 2\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.verify()

    def test_forged_complete_count_rejected(self):
        self.summary["complete_cell_count"] = 6
        self.write_fixture()
        with self.assertRaises(ValueError):
            self.verify()

    def test_omitted_runtime_source_cannot_evade_manifest_verification(self):
        del self.manifest["source_hashes"]["src/tiny.py"]
        self.write_fixture()
        with self.assertRaises(ValueError):
            self.verify()


if __name__ == "__main__":
    unittest.main()
