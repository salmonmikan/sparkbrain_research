from __future__ import annotations

from sparkbrain.research.rv01.physical_learner_bridge import (
    CurrentPhysicalLearnerBridge,
    build_physical_field,
    connection_state_hash,
    runtime_pulse,
)
from sparkbrain.v06.foundation import EventOrigin


def _field():
    return build_physical_field(
        unit_count=3,
        directed_edges=((0, 1), (1, 2)),
        threshold=0.5,
        initial_weight=0.05,
        initial_delay_ms=4.0,
    )


def test_bridge_resolves_one_explicit_current_physical_learner() -> None:
    bridge = CurrentPhysicalLearnerBridge(_field())
    assert bridge.api.module_name == "sparkbrain.research.rv01.physical_plasticity"
    assert bridge.api.learner_class_name == "ExternalOnlyPhysicalPlasticity"
    assert bridge.api.observe_method_name == "observe_external"
    assert bridge.api.observe_mode == "stream"


def test_external_sequence_changes_only_ordinary_connection_state() -> None:
    field = _field()
    bridge = CurrentPhysicalLearnerBridge(field)
    before = connection_state_hash(field)
    rows = bridge.observe_sequence(
        (
            runtime_pulse(
                event_id="external:0",
                time_ms=10.0,
                unit_id=0,
                magnitude=1.0,
                origin=EventOrigin.EXTERNAL,
            ),
            runtime_pulse(
                event_id="external:1",
                time_ms=14.0,
                unit_id=1,
                magnitude=1.0,
                origin=EventOrigin.EXTERNAL,
            ),
            runtime_pulse(
                event_id="external:2",
                time_ms=18.0,
                unit_id=2,
                magnitude=1.0,
                origin=EventOrigin.EXTERNAL,
            ),
        )
    )
    assert len(rows) == 3
    assert connection_state_hash(field) != before


def test_endogenous_observations_cannot_write_connection_state() -> None:
    field = _field()
    bridge = CurrentPhysicalLearnerBridge(field)
    before = connection_state_hash(field)
    bridge.observe_pair(
        runtime_pulse(
            event_id="endogenous:0",
            time_ms=20.0,
            unit_id=0,
            magnitude=1.0,
            origin=EventOrigin.ENDOGENOUS,
        ),
        runtime_pulse(
            event_id="endogenous:1",
            time_ms=24.0,
            unit_id=1,
            magnitude=1.0,
            origin=EventOrigin.ENDOGENOUS,
        ),
    )
    assert connection_state_hash(field) == before
