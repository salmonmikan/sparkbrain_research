from __future__ import annotations

from sparkbrain.v04 import contracts, field, topology

WEIGHT = 1.20
DELAY_MS = 4.0
END_MS = 80.0


def _field(*, close_recurrent_loop: bool) -> field.TemporalExcitableField:
    units = (
        topology.UnitState(0, 0.0, 0.0, base_threshold=0.52),
        topology.UnitState(1, 1.0, 0.0, base_threshold=0.80),
        topology.UnitState(2, 2.0, 0.0, base_threshold=0.80),
        topology.UnitState(3, 3.0, 0.0, base_threshold=0.80),
    )
    connections = [
        topology.Connection(0, 1, WEIGHT, DELAY_MS, plastic=False),
        topology.Connection(1, 2, WEIGHT, DELAY_MS, plastic=False),
        topology.Connection(2, 3, WEIGHT, DELAY_MS, plastic=False),
    ]
    if close_recurrent_loop:
        connections.append(topology.Connection(3, 1, WEIGHT, DELAY_MS, plastic=False))
    graph = topology.explicit_topology(units, connections, receptor_ids=(0,))
    return field.TemporalExcitableField(
        graph,
        field.ExcitableFieldConfig(
            receptor_fanout=1,
            max_events_per_run=1_000,
            max_spikes_per_run=1_000,
        ),
    )


def _run(*, close_recurrent_loop: bool) -> tuple[tuple[float, int], ...]:
    excitable_field = _field(close_recurrent_loop=close_recurrent_loop)
    excitable_field.schedule_pulse(
        contracts.SignalPulse(
            time_ms=0.0,
            channel="forge-recurrent-continuation-cue",
            magnitude=1.0,
        )
    )
    return tuple(
        (spike.time_ms, spike.unit_id) for spike in excitable_field.run_until(END_MS)
    )


def test_recurrent_closure_adds_post_drive_continuation_over_matched_cut() -> None:
    """NON_EVIDENTIARY Forge probe: cheapest kill for recurrent continuation."""
    loop = _run(close_recurrent_loop=True)
    cut = _run(close_recurrent_loop=False)

    loop_post_drive = tuple(row for row in loop if row[0] > 0.0)
    cut_post_drive = tuple(row for row in cut if row[0] > 0.0)
    continuation_gap = len(loop_post_drive) - len(cut_post_drive)

    # The metric and matched cut are fixed before interpreting the result.
    assert cut_post_drive == ((4.0, 1), (8.0, 2), (12.0, 3))
    assert continuation_gap > 0
    assert loop[-1][0] > cut[-1][0]
