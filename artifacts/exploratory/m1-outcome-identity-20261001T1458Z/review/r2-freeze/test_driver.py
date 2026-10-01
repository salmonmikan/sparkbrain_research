"""Outcome-independent fake tests; no SparkBrain runtime invocation."""

import copy
import tempfile
import unittest
from pathlib import Path

from driver import record_call, same_state


class FakePilot:
    def __init__(self):
        self.sequence = 0


def fake_snapshot(pilot, directory):
    directory.mkdir()
    return {
        "inspection": {"sequence": pilot.sequence},
        "inspection_hash": str(pilot.sequence),
        "serialized_components": {"hidden": [17, pilot.sequence]},
    }


class FakeResult:
    def as_dict(self):
        return {"value": "retained"}


class RecorderTests(unittest.TestCase):
    def test_failed_observation_verifier_is_total(self):
        from verify_results import check_run

        root = Path(__file__).resolve().parent.parent
        result = check_run(root / "run1", root / "freeze" / "matrix.json")
        self.assertFalse(result["all_expected_checks_pass"])
        self.assertEqual(len(result["case_findings"]), 8)
        self.assertTrue(all(row["predicted_route"] is None for row in result["case_findings"]))

    def test_local_runtime_schema_dependencies_are_present(self):
        import json

        from jsonschema import Draft202012Validator

        root = Path(__file__).resolve().parent / "source" / "schemas"
        for filename in ("trace-v0.3.schema.json", "checkpoint-v0.3.schema.json"):
            schema = json.loads((root / filename).read_text())
            Draft202012Validator.check_schema(schema)

    def test_success_preserves_input_output_and_state_change(self):
        pilot = FakePilot()

        def invoke():
            pilot.sequence += 1
            return FakeResult()

        with tempfile.TemporaryDirectory() as tmp:
            row = record_call(
                pilot,
                "outcome",
                {"id": "unit-only"},
                Path(tmp) / "record",
                invoke,
                fake_snapshot,
            )
        self.assertIsNone(row["exception"])
        self.assertEqual(row["output"], {"value": "retained"})
        self.assertEqual(row["input"], {"id": "unit-only"})
        self.assertEqual(row["sequence_delta"], 1)
        self.assertFalse(row["complete_serialized_state_equal"])

    def test_exception_is_retained_as_exact_failed_record(self):
        pilot = FakePilot()

        def invoke():
            raise RuntimeError("intentional test-only rejection")

        with tempfile.TemporaryDirectory() as tmp:
            row = record_call(
                pilot,
                "outcome",
                {"id": "unit-only"},
                Path(tmp) / "record",
                invoke,
                fake_snapshot,
            )
            self.assertTrue((Path(tmp) / "record" / "record.json").is_file())
        self.assertIsNone(row["output"])
        self.assertEqual(row["exception"]["type"], "RuntimeError")
        self.assertEqual(row["exception"]["message"], "intentional test-only rejection")
        self.assertTrue(row["complete_serialized_state_equal"])
        self.assertEqual(row["sequence_delta"], 0)

    def test_hidden_checkpoint_difference_is_not_masked_by_inspection(self):
        a = {
            "inspection": {"sequence": 0},
            "inspection_hash": "same",
            "serialized_components": {"hidden_rng": 17},
        }
        b = copy.deepcopy(a)
        b["serialized_components"]["hidden_rng"] = 18
        self.assertFalse(same_state(a, b))

    def test_rejection_mutation_is_preserved_then_stops(self):
        pilot = FakePilot()

        def invoke():
            pilot.sequence = 1
            raise RuntimeError("mutating failure")

        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(RuntimeError, "changed complete serialized state"):
                record_call(
                    pilot,
                    "outcome",
                    {"id": "unit-only"},
                    Path(tmp) / "record",
                    invoke,
                    fake_snapshot,
                )
            self.assertTrue((Path(tmp) / "record" / "record.json").is_file())


if __name__ == "__main__":
    unittest.main()
