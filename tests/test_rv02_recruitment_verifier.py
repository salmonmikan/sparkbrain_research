"""RD001 integrity negatives use synthetic temporary files, never retained outputs."""

import gzip
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from sparkbrain.research.rv02_scale import ScaleStudyConfig

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "run_rv02_recruitment.py"
SPEC = importlib.util.spec_from_file_location("rd001_verifier_test", SCRIPT)
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


class RecruitmentVerifierTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="rd001-verifier-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "source"
        for relative in (RUNNER.RUNNER, RUNNER.CONTRACT, "src/tiny.py"):
            target = self.source / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("synthetic fixture\n", encoding="utf-8")
        self.output = self.root / "bundle"
        self.output.mkdir()
        self.manifest = {
            "protocol": "rv02-rd001-development", "source_git_sha": "a" * 40,
            "source_hashes": RUNNER.source_inventory(self.source),
            "config": ScaleStudyConfig().state_dict(),
            "planned_cells": RUNNER.planned_cells(), "formal_execution_allowed": False,
        }
        self.rows = [{"family": family, "scale": scale, "status": "not_started_total_deadline"}
                     for family, scale in RUNNER.planned_cells()]
        self.summary = {
            "statuses": self.rows.copy(), "complete_cells": 0, "complete_probes": 0,
            "formal_execution_allowed": False,
            "scientific_status": "not_evaluated_development_diagnosis",
        }
        self.save()

    def save(self):
        raw = "".join(json.dumps(row, sort_keys=True) + "\n" for row in self.rows).encode()
        compressed = gzip.compress(raw, mtime=0)
        self.summary["raw_sha256"] = hashlib.sha256(raw).hexdigest()
        self.summary["compressed_sha256"] = hashlib.sha256(compressed).hexdigest()
        (self.output / "raw_cells.jsonl.gz").write_bytes(compressed)
        self.save_metadata()

    def save_metadata(self):
        (self.output / "manifest.json").write_text(json.dumps(self.manifest), encoding="utf-8")
        (self.output / "summary.json").write_text(json.dumps(self.summary), encoding="utf-8")

    def verify(self):
        return RUNNER.verify_bundle(self.output, source_root=self.source)

    def test_intact_incomplete_bundle_verifies_without_acceptance(self):
        result = self.verify()
        self.assertIs(result["integrity_verified"], True)
        self.assertEqual(result["complete_cells"], 0)
        self.assertEqual(result["complete_probes"], 0)

    def test_missing_row_rejected_with_updated_hash(self):
        self.rows.pop()
        self.save()
        with self.assertRaises(ValueError):
            self.verify()

    def test_duplicate_identity_rejected_with_matching_hash_and_count(self):
        self.rows[-1] = self.rows[0].copy()
        self.summary["statuses"] = self.rows.copy()
        self.save()
        with self.assertRaises(ValueError):
            self.verify()

    def test_raw_and_compressed_hash_mismatch_each_rejected(self):
        for key in ("raw_sha256", "compressed_sha256"):
            with self.subTest(key=key):
                self.save()
                self.summary[key] = "0" * 64
                self.save_metadata()
                with self.assertRaises(ValueError):
                    self.verify()

    def test_runtime_source_omission_rejected(self):
        del self.manifest["source_hashes"]["src/tiny.py"]
        self.save_metadata()
        with self.assertRaises(ValueError):
            self.verify()

    def test_changed_contract_rejected(self):
        (self.source / RUNNER.CONTRACT).write_text("changed synthetic contract\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.verify()

    def test_forged_completion_rejected(self):
        self.summary["complete_cells"] = 18
        self.save_metadata()
        with self.assertRaises(ValueError):
            self.verify()


if __name__ == "__main__":
    unittest.main()
