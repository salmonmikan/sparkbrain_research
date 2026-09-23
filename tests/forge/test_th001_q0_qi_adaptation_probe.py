from __future__ import annotations

import math

from sparkbrain.v04 import contracts, field, topology

BASE_THRESHOLD = 0.80
HISTORY_END_MS = 100.0
OBSERVATION_END_MS = 110.0
ENVIRONMENT_DRIVE = 0.90
LOCAL_INTERVENTION_CURRENT = 0.825
DOWNSTREAM_WEIGHT = 1.00
DOWNSTREAM_DELAY_MS = 4.0


def _new_field() -> field.TemporalExcitableField:
    units = (
        topology.UnitState(0, 0.0, 0.0, base_threshold=BASE_THRESHOLD),
        topology.UnitState(1, 1.0, 0.0, base_threshold=BASE_THRESHOLD),
        topology.UnitState(2, 2.0, 0.0, base_threshold=BASE_THRESHOLD),
    )
    graph = topology.explicit_topology(
        units,
        (
            topology.Connection(
                1,
                2,
                DOWNSTREAM_WEIGHT,
                DOWNSTREAM_DELAY_MS,
                plastic=False,
            ),
        ),
        receptor_ids=(0, 1),
    )
    return field.TemporalExcitableField(
        graph,
        field.ExcitableFieldConfig(
            receptor_fanout=1,
            max_events_per_run=100,
            max_spikes_per_run=100,
        ),
    )


def _history(*, warm_hidden_unit: bool) -> field.TemporalExcitableField:
    excitable_field = _new_field()
    if warm_hidden_unit:
        excitable_field.schedule_pulse(
            contracts.SignalPulse(
                time_ms=0.0,
                channel="forge-th001-history",
                magnitude=1.0,
                location=(1.0, 0.0),
            )
        )
    excitable_field.run_until(HISTORY_END_MS)
    return excitable_field


def _future_signature(
    history: field.TemporalExcitableField,
    *,
    intervene: bool,
) -> tuple[tuple[float, int], ...]:
    excitable_field = field.TemporalExcitableField.from_state_dict(history.state_dict())
    excitable_field.schedule_pulse(
        contracts.SignalPulse(
            time_ms=HISTORY_END_MS,
            channel="forge-th001-environment",
            magnitude=ENVIRONMENT_DRIVE,
            location=(0.0, 0.0),
        )
    )
    if intervene:
        excitable_field.schedule_arrival(
            contracts.SynapticArrival(
                time_ms=HISTORY_END_MS,
                target_id=1,
                current=LOCAL_INTERVENTION_CURRENT,
                source_id=None,
                pulse_id="forge-th001-fixed-local-intervention",
            )
        )
    return tuple(
        (spike.time_ms, spike.unit_id)
        for spike in excitable_field.run_until(OBSERVATION_END_MS)
    )


def test_th001_q0_pair_splits_only_because_ordinary_adaptation_is_exposed() -> None:
    """NON_EVIDENTIARY Theory Forge probe for the frozen Q0-vs-QI discriminator."""
    warm = _history(warm_hidden_unit=True)
    quiet = _history(warm_hidden_unit=False)

    # Q0 is the predeclared unperturbed environment: future input targets unit 0.
    # Unit 1 is disconnected from that environment, so its different history is
    # behaviorally silent unless the separate local intervention is applied.
    warm_q0 = _future_signature(warm, intervene=False)
    quiet_q0 = _future_signature(quiet, intervene=False)
    assert warm_q0 == quiet_q0 == ((100.0, 0),)

    # The same fixed local intervention forces QI to split the histories.
    warm_qi = _future_signature(warm, intervene=True)
    quiet_qi = _future_signature(quiet, intervene=True)
    assert warm_qi == ((100.0, 0),)
    assert quiet_qi == ((100.0, 0), (100.0, 1), (104.0, 2))

    # Cheapest ordinary reduction: the warm history left only standard
    # adaptation on unit 1. Its analytically decayed threshold predicts the
    # intervention split before reading the downstream response.
    config = warm.config
    warm_adaptation_at_intervention = config.adaptation_increment * math.exp(
        -HISTORY_END_MS / config.adaptation_tau_ms
    )
    quiet_threshold = BASE_THRESHOLD
    warm_threshold = BASE_THRESHOLD + warm_adaptation_at_intervention
    assert quiet_threshold < LOCAL_INTERVENTION_CURRENT < warm_threshold

    # The downstream difference then follows the fixed ordinary edge exactly.
    assert DOWNSTREAM_WEIGHT > BASE_THRESHOLD
