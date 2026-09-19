"""EXPLORATORY / NON_EVIDENTIARY refractory-current accounting probe."""

from __future__ import annotations

import math

from sparkbrain.v04.contracts import SynapticArrival
from sparkbrain.v04.field import ExcitableFieldConfig, TemporalExcitableField
from sparkbrain.v04.topology import UnitState, explicit_topology


def _field() -> TemporalExcitableField:
    topology = explicit_topology(
        (
            UnitState(
                unit_id=0,
                x=0.0,
                y=0.0,
                potential=0.5,
                base_threshold=1.0,
                refractory_until_ms=5.0,
                last_update_ms=0.0,
            ),
        ),
        (),
        receptor_ids=(),
    )
    return TemporalExcitableField(topology, ExcitableFieldConfig())


def _arrival(current: float, pulse_id: str, *, time_ms: float) -> SynapticArrival:
    return SynapticArrival(
        time_ms=time_ms,
        target_id=0,
        current=current,
        source_id=None,
        pulse_id=pulse_id,
    )


def _run_arm(currents: tuple[float, ...]) -> tuple[float, tuple[object, ...], float]:
    field = _field()
    for index, current in enumerate(currents):
        field.schedule_arrival(_arrival(current, f"load-{index}", time_ms=1.0))
    refractory_spikes = field.run_until(1.0)
    potential_after_load = field.units[0].potential

    field.schedule_arrival(_arrival(0.70, "probe", time_ms=5.1))
    probe_spikes = field.run_until(5.1)
    return potential_after_load, refractory_spikes + probe_spikes, field.units[0].potential


def test_refractory_positive_current_cancels_same_time_inhibition() -> None:
    inhibition_potential, inhibition_spikes, inhibition_final = _run_arm((-0.5,))
    paired_potential, paired_spikes, paired_final = _run_arm((-0.5, 0.5))
    excitation_potential, excitation_spikes, excitation_final = _run_arm((0.5,))

    # No arm may spike while the unit is inside its absolute refractory window.
    assert all(getattr(spike, "time_ms") > 5.0 for spike in inhibition_spikes)
    assert all(getattr(spike, "time_ms") > 5.0 for spike in paired_spikes)
    assert all(getattr(spike, "time_ms") > 5.0 for spike in excitation_spikes)

    # Current implementation nets positive and negative arrivals before applying
    # the refractory clamp, so paired input retains the same membrane state as
    # excitation-only input instead of preserving the inhibition-only effect.
    assert math.isclose(paired_potential, excitation_potential, rel_tol=0.0, abs_tol=1e-12)
    assert paired_potential > inhibition_potential

    inhibition_probe_spikes = [spike for spike in inhibition_spikes if spike.time_ms == 5.1]
    paired_probe_spikes = [spike for spike in paired_spikes if spike.time_ms == 5.1]
    excitation_probe_spikes = [spike for spike in excitation_spikes if spike.time_ms == 5.1]

    # The pre-bound +0.70 post-refractory probe exposes a functional difference.
    assert inhibition_probe_spikes == []
    assert len(paired_probe_spikes) == 1
    assert len(excitation_probe_spikes) == 1
    assert math.isclose(paired_final, excitation_final, rel_tol=0.0, abs_tol=1e-12)
    assert inhibition_final > 0.0
