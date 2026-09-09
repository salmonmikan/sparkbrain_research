"""Independent RD002 audit mutations on reserved synthetic evidence."""
import copy
import importlib.util
from pathlib import Path
import unittest
from sparkbrain.research.rv01.physical_learner_bridge import build_physical_field
from sparkbrain.research.rv02_recruitment import run_probe
from sparkbrain.research.rv02_boundary_recruitment import score_probe

PATH = Path(__file__).resolve().parents[1] / 'scripts/audit_rv02_boundary_recruitment.py'
SPEC = importlib.util.spec_from_file_location('rd002_audit_test', PATH)
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)

class BoundaryRawAuditTests(unittest.TestCase):
    def setUp(self):
        field = build_physical_field(unit_count=48, directed_edges=((0,36), (0,1)),
                                     threshold=.5, initial_weight=.05, initial_delay_ms=5.)
        self.probe = run_probe(field, 0)
        self.route = (0, 1, 2)
        self.score = score_probe(self.probe['spikes'], self.route, 48)

    def test_independent_score_and_membrane_reconstruction(self):
        AUDIT.verify_probe(self.probe, self.score, self.route, 48)

    def test_each_score_field_is_verified(self):
        for key in self.score:
            forged = copy.deepcopy(self.score)
            value = forged[key]
            forged[key] = ([99] if isinstance(value, (list, tuple)) else
                           not value if isinstance(value, bool) else
                           999 if value is None else value + 1)
            with self.subTest(key=key), self.assertRaises(ValueError):
                AUDIT.verify_probe(self.probe, forged, self.route, 48)

    def test_arrival_and_observer_and_learning_drift_are_rejected(self):
        for key, value in (('observer_equivalence', False),
                           ('reference_state_hash', 'forged'),
                           ('probe_connection_hash_after', 'forged'),
                           ('actual_arrivals', 4096), ('actual_spikes', 512)):
            forged = copy.deepcopy(self.probe)
            forged[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                AUDIT.verify_probe(forged, self.score, self.route, 48)

if __name__ == '__main__':
    unittest.main()
