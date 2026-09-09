"""RD001 independent instrumentation tests on reserved synthetic states only."""

import math
import unittest
from unittest.mock import patch

from sparkbrain.research.rv01.physical_learner_bridge import (
    build_physical_field,
    connection_state_hash,
    runtime_pulse,
)
from sparkbrain.research.rv01.physical_plasticity import ExternalOnlyPhysicalPlasticity
from sparkbrain.research.rv02_recruitment import (
    ArrivalObservedField,
    run_probe,
    run_recruitment_cell,
)
from sparkbrain.research.rv02_scale import ScaleStudyConfig, development_worlds
from sparkbrain.v04.contracts import SynapticArrival
from sparkbrain.v04.field import TemporalExcitableField
from sparkbrain.v06.foundation import EventOrigin


def reserved_field():
    return build_physical_field(
        unit_count=48, directed_edges=((0, 36), (36, 37)),
        threshold=0.5, initial_weight=0.05, initial_delay_ms=5.0,
    )


def arrival(time, current, pulse, target=36):
    return SynapticArrival(time_ms=time, target_id=target, current=current,
                           source_id=0, pulse_id=pulse)


class RecruitmentObserverTests(unittest.TestCase):
    def test_grouped_subthreshold_arrivals_are_observed_without_inventing_spikes(self):
        observed = ArrivalObservedField.from_state_dict(reserved_field().state_dict())
        observed.schedule_arrival(arrival(100.0, 0.05, "reserved-a"))
        observed.schedule_arrival(arrival(100.0, 0.05, "reserved-b"))
        spikes = observed.run_until(100.0)
        row = observed.arrival_observations[0]
        self.assertEqual(spikes, ())
        self.assertEqual(row["arrival_count"], 2)
        self.assertAlmostEqual(row["positive_current"], 0.1)
        self.assertAlmostEqual(row["negative_current"], 0.0)
        self.assertAlmostEqual(row["potential_before_reset"], 0.1)
        self.assertEqual(row["threshold"], 0.5)
        self.assertIs(row["spiked"], False)
        self.assertEqual(row["target_id"], 36)

    def test_observation_is_state_and_spike_noninterfering(self):
        base = reserved_field().state_dict()
        plain = TemporalExcitableField.from_state_dict(base)
        observed = ArrivalObservedField.from_state_dict(base)
        for field in (plain, observed):
            field.schedule_arrival(arrival(100.0, 0.30, "reserved-a"))
            field.schedule_arrival(arrival(100.0, 0.30, "reserved-b"))
            field.schedule_arrival(arrival(100.0, -0.05, "reserved-inhibition"))
        self.assertEqual(observed.run_until(110.0), plain.run_until(110.0))
        self.assertEqual(observed.state_dict(), plain.state_dict())
        self.assertEqual(observed.state_hash(), plain.state_hash())
        row = next(r for r in observed.arrival_observations if r["target_id"] == 36)
        self.assertEqual(row["arrival_count"], 3)
        self.assertAlmostEqual(row["positive_current"], 0.6)
        self.assertAlmostEqual(row["negative_current"], 0.05)
        self.assertAlmostEqual(row["potential_before_reset"], 0.55)
        self.assertIs(row["spiked"], True)

    def test_membrane_decay_is_measured_before_threshold_comparison(self):
        field = reserved_field()
        field.units[36].potential = 0.4
        field.units[36].last_update_ms = 90.0
        observed = ArrivalObservedField.from_state_dict(field.state_dict())
        observed.schedule_arrival(arrival(100.0, 0.05, "reserved-decay"))
        observed.run_until(100.0)
        row = observed.arrival_observations[0]
        expected = 0.4 * math.exp(-10.0 / field.config.membrane_tau_ms)
        self.assertAlmostEqual(row["decayed_potential"], expected)
        self.assertAlmostEqual(row["potential_before_reset"], expected + 0.05)

    def test_refractory_positive_current_does_not_become_integrated_potential(self):
        field = reserved_field()
        field.units[36].refractory_until_ms = 102.0
        observed = ArrivalObservedField.from_state_dict(field.state_dict())
        observed.schedule_arrival(arrival(100.0, 1.0, "reserved-refractory"))
        self.assertEqual(observed.run_until(100.0), ())
        row = observed.arrival_observations[0]
        self.assertIs(row["refractory"], True)
        self.assertEqual(row["potential_before_reset"], 0.0)
        self.assertEqual(row["positive_current"], 1.0)
        self.assertIs(row["spiked"], False)

    def test_endogenous_hidden_activity_does_not_create_external_learning_eligibility(self):
        field = reserved_field()
        learner = ExternalOnlyPhysicalPlasticity(field)
        learner.observe_external(runtime_pulse(
            event_id="reserved-source", time_ms=0.0, unit_id=0, magnitude=1.0))
        before = connection_state_hash(field)
        changed = learner.observe_external(runtime_pulse(
            event_id="reserved-hidden-endogenous", time_ms=5.0, unit_id=36,
            magnitude=1.0, origin=EventOrigin.ENDOGENOUS_UNCONFIRMED))
        self.assertEqual(changed, ())
        self.assertEqual(connection_state_hash(field), before)
        self.assertEqual(learner.external_observation_count, 1)
        self.assertEqual(learner.ignored_endogenous_count, 1)
        # A separately declared real external observation is a different intervention.
        self.assertTrue(learner.observe_external(runtime_pulse(
            event_id="reserved-hidden-external", time_ms=5.0, unit_id=36, magnitude=1.0)))

    def test_predeclared_extended_horizon_preserves_original_prefix(self):
        field = reserved_field()
        original_state = field.state_dict()
        short = run_probe(field, 0, horizon_ms=40.0)
        extended = run_probe(field, 0, horizon_ms=160.0)
        self.assertEqual(short["spikes"],
                         [s for s in extended["spikes"] if s["time_ms"] <= 140.0])
        self.assertEqual(short["arrival_observations"],
                         [r for r in extended["arrival_observations"] if r["time_ms"] <= 140.0])
        self.assertEqual(field.state_dict(), original_state)
        self.assertTrue(short["queue_drained"])
        self.assertTrue(extended["queue_drained"])
        self.assertEqual(short["spikes"], extended["spikes"])
        self.assertEqual(short["probe_connection_hash_before"],
                         extended["probe_connection_hash_after"])

    def test_arbitrary_success_seeking_horizons_and_port_remapping_rejected(self):
        field = reserved_field()
        for horizon in (0.0, 80.0, 320.0, float("nan"), True):
            with self.subTest(horizon=horizon), self.assertRaises(ValueError):
                run_probe(field, 0, horizon_ms=horizon)
        with self.assertRaises(ValueError):
            run_probe(field, 0, ports=tuple(range(48)))

    def test_boundary_cut_preserves_hidden_hidden_edges_and_original_state(self):
        field = build_physical_field(
            unit_count=48, directed_edges=((0, 36), (36, 0), (36, 37), (0, 1)),
            threshold=0.5, initial_weight=0.05, initial_delay_ms=5.0)
        original = field.state_dict()
        row = run_probe(field, 0, cut_hidden_boundary=True)
        changed = {tuple(r["edge"]) for r in row["boundary_interventions"]}
        self.assertEqual(changed, {(0, 36), (36, 0)})
        self.assertNotEqual(row["initial_connection_hash"], row["probe_connection_hash_before"])
        self.assertEqual(row["probe_connection_hash_before"], row["probe_connection_hash_after"])
        self.assertEqual(field.state_dict(), original)

    def test_direct_positive_control_is_not_natural_hidden_recruitment(self):
        field = reserved_field()
        natural = run_probe(field, 0)
        positive = run_probe(field, 36)
        self.assertFalse(any(s["unit_id"] >= 36 for s in natural["spikes"]))
        self.assertTrue(any(s["unit_id"] == 36 and s["time_ms"] == 100.0
                            for s in positive["spikes"]))
        hidden = {r["unit_id"]: r for r in natural["hidden_units"]}
        self.assertGreater(hidden[36]["arrival_count"], 0)
        self.assertGreater(hidden[36]["positive_current"], 0)
        self.assertEqual(hidden[36]["spike_count"], 0)
        self.assertGreater(hidden[36]["maximum_potential_threshold_ratio"], 0)
        self.assertEqual(hidden[47]["arrival_count"], 0)
        self.assertIsNone(hidden[47]["maximum_potential_threshold_ratio"])
        self.assertEqual(natural["initial_connection_hash"], positive["initial_connection_hash"])

    def test_cell_retains_original_physical_defaults_without_running_a_world(self):
        config = ScaleStudyConfig()
        world = development_worlds(config)[0]
        with patch("sparkbrain.research.rv02_recruitment.build_physical_field",
                   side_effect=RuntimeError("reserved-constructor-stop")) as constructor:
            with self.assertRaisesRegex(RuntimeError, "reserved-constructor-stop"):
                run_recruitment_cell(config, world, 1)
        self.assertEqual(constructor.call_args.kwargs["threshold"], 0.5)
        self.assertEqual(constructor.call_args.kwargs["initial_weight"], 0.05)
        self.assertEqual(constructor.call_args.kwargs["initial_delay_ms"], 5.0)
        self.assertEqual(constructor.call_args.kwargs["unit_count"], 48)
        with self.assertRaises(ValueError):
            run_recruitment_cell(ScaleStudyConfig(seed=92002), world, 1)

    def test_refractory_mixed_currents_use_net_not_negative_only(self):
        for positive, negative, expected in ((0.3, 0.2, 0.0), (0.2, 0.3, -0.1)):
            with self.subTest(positive=positive):
                field = reserved_field()
                field.units[36].refractory_until_ms = 102.0
                observed = ArrivalObservedField.from_state_dict(field.state_dict())
                plain = TemporalExcitableField.from_state_dict(field.state_dict())
                for instance in (observed, plain):
                    instance.schedule_arrival(arrival(100.0, positive, "reserved-positive"))
                    instance.schedule_arrival(arrival(100.0, -negative, "reserved-negative"))
                self.assertEqual(observed.run_until(100.0), plain.run_until(100.0))
                self.assertEqual(observed.state_dict(), plain.state_dict())
                row = observed.arrival_observations[0]
                self.assertAlmostEqual(row["integrated_net_current"], expected)
                self.assertAlmostEqual(row["potential_before_reset"], expected)

    def test_zero_weight_arrivals_are_not_nonzero_hidden_current(self):
        row = run_probe(reserved_field(), 0, cut_hidden_boundary=True)
        hidden = {r["unit_id"]: r for r in row["hidden_units"]}
        self.assertGreater(hidden[36]["arrival_count"], 0)
        self.assertEqual(hidden[36]["positive_current"], 0.0)
        self.assertEqual(hidden[36]["integrated_net_current"], 0.0)
        self.assertEqual(hidden[36]["spike_count"], 0)


if __name__ == "__main__":
    unittest.main()
