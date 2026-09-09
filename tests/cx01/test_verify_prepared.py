from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from sparkbrain.comparison.cx01.candidate import CandidatePurpose, CandidateSpec
from sparkbrain.comparison.cx01.prepare import prepare_outcome_blind_bundle
from sparkbrain.comparison.cx01.verify_prepared import (
    PREPARED_FILES,
    verify_reserved_fixture_bundle,
)


class ReservedPackageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.output = Path(self.temporary.name) / "prepared"
        self.candidate = CandidateSpec(
            generation_id="cx01-fixture-integration-20260909",
            seeds=tuple(range(5000, 5010)),
            purpose=CandidatePurpose.STRUCTURE_FIXTURE,
        )
        self.expected = {
            "output_dir": self.output,
            "expected_candidate": self.candidate,
            "expected_source_git_sha": "0687c8db3efb8180c8599d32235751b93f3c1f77",
            "expected_builder": "engineering-fixture-builder",
            "expected_execution_command": "reserved-fixture-no-capability",
            "expected_artifact_root": "reserved-fixture-unused",
        }
        prepare_outcome_blind_bundle(
            generation_id=self.candidate.generation_id,
            seeds=self.candidate.seeds,
            purpose=self.candidate.purpose,
            source_git_sha=self.expected["expected_source_git_sha"],
            builder=self.expected["expected_builder"],
            execution_command=self.expected["expected_execution_command"],
            artifact_root=self.expected["expected_artifact_root"],
            output_dir=self.output,
        )

    def test_roundtrip_preserves_all_payload_bytes_without_formal_selection(self) -> None:
        before = {p.name: p.read_bytes() for p in self.output.iterdir()}
        with patch(
            "sparkbrain.comparison.cx01.prepare.select_outcome_blind_formal_seeds",
            side_effect=AssertionError("formal selection forbidden"),
        ), patch(
            "sparkbrain.comparison.cx01.freeze.select_outcome_blind_formal_seeds",
            side_effect=AssertionError("formal selection forbidden"),
        ):
            result = verify_reserved_fixture_bundle(**self.expected)
        self.assertEqual(set(result), PREPARED_FILES)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.output.iterdir()})
        rows = [json.loads(row) for row in before["declarations.jsonl"].splitlines()]
        self.assertEqual(len(rows), 420)
        self.assertTrue(all(row["status"] == "unscored" for row in rows))
        self.assertTrue(all(row["capability_result_present"] is False for row in rows))
        self.assertTrue(all(row["measurements_present"] is False for row in rows))

    def test_each_payload_tamper_is_rejected(self) -> None:
        for name in PREPARED_FILES:
            with self.subTest(name=name):
                path = self.output / name
                original = path.read_bytes()
                if name == "declarations.jsonl":
                    rows = [json.loads(row) for row in original.splitlines()]
                    rows[0]["capability_result_present"] = True
                    changed = "\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n"
                else:
                    value = json.loads(original)
                    key = {
                        "candidate.json": "generation_id",
                        "formal_seed_selection.json": "candidate_spec_hash",
                        "formal_structure_audit.json": "world_count",
                        "formal_identifiability_audit.json": "world_count",
                        "freeze_manifest.json": "formal_structure_audit_hash",
                    }[name]
                    value[key] = "tampered"
                    changed = json.dumps(value, indent=2, sort_keys=True) + "\n"
                path.write_text(changed)
                with self.assertRaisesRegex(ValueError, "payload differs"):
                    verify_reserved_fixture_bundle(**self.expected)
                path.write_bytes(original)

    def test_empty_false_audits_and_missing_declaration_rejected(self) -> None:
        for name, replacement in (
            ("formal_structure_audit.json", b"{}\n"),
            ("formal_identifiability_audit.json", b'{"passed":false}\n'),
            ("declarations.jsonl", b""),
        ):
            with self.subTest(name=name):
                path = self.output / name
                original = path.read_bytes()
                path.write_bytes(replacement)
                with self.assertRaisesRegex(ValueError, "payload differs"):
                    verify_reserved_fixture_bundle(**self.expected)
                path.write_bytes(original)

    def test_exact_inventory_and_regular_files(self) -> None:
        extra = self.output / "STARTED.json"
        extra.write_text("{}")
        with self.assertRaisesRegex(ValueError, "exactly"):
            verify_reserved_fixture_bundle(**self.expected)
        extra.unlink()
        target = self.output / "candidate.json"
        original = target.read_bytes()
        target.unlink()
        with self.assertRaisesRegex(ValueError, "exactly"):
            verify_reserved_fixture_bundle(**self.expected)
        outside = Path(self.temporary.name) / "candidate.json"
        outside.write_bytes(original)
        target.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "regular file"):
            verify_reserved_fixture_bundle(**self.expected)
        target.unlink()
        target.mkdir()
        with self.assertRaisesRegex(ValueError, "regular file"):
            verify_reserved_fixture_bundle(**self.expected)

    def test_source_and_metadata_expectations_are_external(self) -> None:
        for key, replacement in (
            ("expected_source_git_sha", "1" * 40),
            ("expected_builder", "different-builder"),
            ("expected_execution_command", "different-command"),
            ("expected_artifact_root", "different-root"),
        ):
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "payload differs"):
                verify_reserved_fixture_bundle(**{**self.expected, key: replacement})

    def test_formal_purpose_refused_before_reconstruction(self) -> None:
        formal = CandidateSpec(
            generation_id="cx01-candidate-verifier-denial-test",
            seeds=tuple(range(800000, 800010)),
            purpose=CandidatePurpose.FORMAL,
        )
        with patch(
            "sparkbrain.comparison.cx01.verify_prepared.prepare_outcome_blind_bundle",
            side_effect=AssertionError("reconstruction forbidden"),
        ), self.assertRaisesRegex(ValueError, "reserved structure fixtures"):
            verify_reserved_fixture_bundle(**{**self.expected, "expected_candidate": formal})


if __name__ == "__main__":
    unittest.main()
