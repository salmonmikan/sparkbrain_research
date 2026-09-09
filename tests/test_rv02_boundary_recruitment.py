"""RD002 independent pre-execution tests on reserved synthetic states."""
import copy
import unittest
from dataclasses import replace
from unittest.mock import patch

from sparkbrain.research.rv01.physical_learner_bridge import build_physical_field
from sparkbrain.research.rv02_recruitment import run_probe as old_run_probe
from sparkbrain.research.rv02_boundary_recruitment import apply_boundary_gain, score_probe, run_probe


def reserved_field():
    return build_physical_field(
        unit_count=48, directed_edges=((0, 36), (36, 0), (36, 37), (0, 1)),
        threshold=0.5, initial_weight=0.05, initial_delay_ms=5.0)


class BoundaryInterventionTests(unittest.TestCase):
    def test_gain_changes_only_visible_to_hidden_weights_on_fresh_clone(self):
        field = reserved_field()
        original = copy.deepcopy(field.state_dict())
        changed, _ = apply_boundary_gain(field, 4.0)
        self.assertEqual(field.state_dict(), original)
        self.assertIsNot(changed, field)
        self.assertEqual(set(changed.connections), set(field.connections))
        for key, edge in changed.connections.items():
            baseline = field.connections[key]
            self.assertEqual(edge.weight, baseline.weight * (4 if key == (0, 36) else 1))
            self.assertEqual(edge.delay_ms, baseline.delay_ms)
        self.assertEqual(changed.config, field.config)
        self.assertEqual(changed.units, field.units)

    def test_gain_one_is_exact_baseline_including_observation_and_provenance(self):
        field = reserved_field()
        baseline, _ = apply_boundary_gain(field, 1.0)
        self.assertEqual(baseline.state_dict(), field.state_dict())
        self.assertEqual(run_probe(baseline, 0), old_run_probe(field, 0))

    def test_extended_horizon_is_not_authorized(self):
        for horizon in (160.0, 0, 80, True, float('nan')):
            with self.subTest(horizon=horizon), self.assertRaises(ValueError):
                run_probe(reserved_field(), 0, horizon_ms=horizon)

    def test_frozen_gain_domain_rejects_adaptive_and_invalid_values(self):
        for gain in (0, -1, 1.5, 8, True, float('nan'), float('inf')):
            with self.subTest(gain=gain), self.assertRaises(ValueError):
                apply_boundary_gain(reserved_field(), gain)

    def test_synthetic_threshold_crossing_demonstrates_intended_recruitment(self):
        field = reserved_field()
        field.connections[(0, 36)].weight = 0.2
        baseline = run_probe(field, 0)
        gained, _ = apply_boundary_gain(field, 4.0)
        probe = run_probe(gained, 0)
        self.assertFalse(any(s['unit_id'] == 36 for s in baseline['spikes']))
        self.assertTrue(any(s['unit_id'] == 36 for s in probe['spikes']))
        self.assertTrue(probe['observer_equivalence'])
        self.assertEqual(probe['probe_connection_hash_before'], probe['probe_connection_hash_after'])
        self.assertEqual(probe['observed_state_hash'], probe['reference_state_hash'])

    def test_native_guard_retains_partial_evidence_without_success_scores(self):
        field = reserved_field()
        field.config = replace(field.config, max_events_per_run=1)
        probe = run_probe(field, 0)
        self.assertEqual(probe['status'], 'incomplete_native_guard')
        self.assertIs(probe['metrics_available'], False)
        self.assertNotIn('behavior', probe)
        self.assertTrue(probe['observer_equivalence'])
        self.assertEqual(probe['error'], probe['reference_error'])
        self.assertEqual(probe['spikes'], probe['reference_spikes'])
        self.assertEqual(probe['observed_state_hash'], probe['reference_state_hash'])
        self.assertIn('partial_state', probe)

    def test_observer_failure_cannot_be_misclassified_as_native_guard(self):
        with patch('sparkbrain.research.rv02_boundary_recruitment.PartialObservedField.run_until',
                   side_effect=RuntimeError('max_events_per_run exceeded')):
            with self.assertRaisesRegex(RuntimeError, 'observer noninterference'):
                run_probe(reserved_field(), 0)

    def test_boundary_cut_blocks_gain_without_touching_hidden_recurrence(self):
        field = reserved_field()
        gained, _ = apply_boundary_gain(field, 4.0)
        plain_cut = run_probe(field, 0, cut_hidden_boundary=True)
        gained_cut = run_probe(gained, 0, cut_hidden_boundary=True)
        for key in ('spikes', 'arrival_observations', 'hidden_units', 'visible_final_state',
                    'observed_state_hash', 'probe_connection_hash_before'):
            self.assertEqual(plain_cut[key], gained_cut[key])
        self.assertEqual(gained.connections[(36, 37)].weight, 0.05)


class BoundaryScoringTests(unittest.TestCase):
    def score(self, units):
        return score_probe([{'time_ms': 100.0 if i == 0 else 105.0 + i,
                             'unit_id': unit} for i, unit in enumerate(units)],
                           (0, 1, 2), 48)

    def test_exact_route_excludes_initial_cue_and_hidden_activity(self):
        score = self.score([0, 36, 1, 37, 2])
        self.assertEqual(tuple(score['generated_units']), (1, 2))
        self.assertTrue(score['exact_sequence_recovered'])
        self.assertEqual(score['ordered_retention'], 1.0)
        self.assertEqual(score['missing_expected_count'], 0)
        self.assertEqual(score['excess_route_event_count'], 0)
        self.assertEqual(score['raw_contamination'], 0)

    def test_later_cue_duplicates_and_offroute_errors_remain_counted(self):
        score = self.score([0, 1, 1, 2, 0, 3, 36])
        self.assertEqual(tuple(score['generated_units']), (1, 1, 2, 0, 3))
        self.assertFalse(score['exact_sequence_recovered'])
        self.assertEqual(score['ordered_retention'], 1.0)
        self.assertEqual(score['excess_route_event_count'], 2)
        self.assertEqual(score['raw_contamination'], 1)

    def test_no_ignition_and_wrong_order_never_force_success(self):
        for units, retained, missing in (([0], 0.0, 2), ([0, 2, 1], 0.5, 1)):
            score = self.score(units)
            self.assertEqual(score['ordered_retention'], retained)
            self.assertEqual(score['missing_expected_count'], missing)
            self.assertFalse(score['exact_sequence_recovered'])


if __name__ == '__main__':
    unittest.main()
