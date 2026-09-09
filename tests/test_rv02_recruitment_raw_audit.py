"""Independent post-run audit negatives on reserved synthetic probes only."""

import copy
import importlib.util
import unittest
from pathlib import Path

from sparkbrain.research.rv01.physical_learner_bridge import build_physical_field
from sparkbrain.research.rv02_recruitment import run_probe

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit_rv02_recruitment.py"
SPEC = importlib.util.spec_from_file_location("rd001_raw_audit_test", SCRIPT)
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


class RecruitmentRawAuditTests(unittest.TestCase):
    def setUp(self):
        field = build_physical_field(
            unit_count=48, directed_edges=((0, 36), (36, 37)),
            threshold=0.5, initial_weight=0.05, initial_delay_ms=5.0)
        self.probe = run_probe(field, 0)

    def test_reserved_probe_reconstructs(self):
        result = AUDIT.verify_probe_metrics(self.probe, 48)
        self.assertEqual(result["hidden_positive_current_units"], 1)
        self.assertEqual(result["hidden_spikes"], 0)

    def test_hidden_current_ratio_and_projection_drift_rejected(self):
        for key in ("positive_current", "maximum_potential_threshold_ratio",
                    "projected_final_potential", "stored_final_potential", "arrival_count"):
            with self.subTest(key=key):
                forged = copy.deepcopy(self.probe)
                forged["hidden_units"][0][key] += 1
                with self.assertRaises(ValueError):
                    AUDIT.verify_probe_metrics(forged, 48)

    def test_group_current_cannot_be_changed_with_only_aggregate_update(self):
        forged = copy.deepcopy(self.probe)
        forged["arrival_observations"][1]["positive_current"] += 0.1
        forged["hidden_units"][0]["positive_current"] += 0.1
        with self.assertRaises(ValueError):
            AUDIT.verify_probe_metrics(forged, 48)

    def test_reported_native_budget_overrun_rejected(self):
        for key, value in (("actual_arrivals", 4097), ("actual_spikes", 513)):
            with self.subTest(key=key):
                forged = copy.deepcopy(self.probe)
                forged[key] = value
                with self.assertRaises(ValueError):
                    AUDIT.verify_probe_metrics(forged, 48)

    def test_missing_hidden_units_and_invented_spike_rejected(self):
        forged = copy.deepcopy(self.probe)
        forged["hidden_units"].pop()
        with self.assertRaises(ValueError):
            AUDIT.verify_probe_metrics(forged, 48)
        forged = copy.deepcopy(self.probe)
        forged["arrival_observations"][1]["spiked"] = True
        with self.assertRaises(ValueError):
            AUDIT.verify_probe_metrics(forged, 48)

    def test_silent_unit_undefined_peak_is_not_zero_imputed(self):
        forged = copy.deepcopy(self.probe)
        forged["hidden_units"][-1]["maximum_potential_threshold_ratio"] = 0.0
        with self.assertRaises(ValueError):
            AUDIT.verify_probe_metrics(forged, 48)


if __name__ == "__main__":
    unittest.main()
