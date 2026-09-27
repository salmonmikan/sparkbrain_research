from __future__ import annotations

from sparkbrain.research.rv02_rd006_external_learning_reachability import (
    training_schedule as v1_training_schedule,
)
from sparkbrain.research.rv02_rd006_external_learning_reachability_v2 import (
    PARENT_AUDIT_HEAD,
    PROTOCOL_ID,
    WITHIN_ROUTE_EXTERNAL_EVENT_POSITION_INTERVAL_MS,
    RD006Config,
    development_worlds,
    training_schedule,
)


def test_v2_changes_only_within_route_timing_and_event_namespace() -> None:
    config = RD006Config()
    world = development_worlds(config)[0]
    v1_rows = v1_training_schedule(world)
    v2_rows = training_schedule(world)
    assert len(v1_rows) == len(v2_rows)
    for old, new in zip(v1_rows, v2_rows, strict=True):
        assert {
            key: value for key, value in old.items() if key not in {"time_ms", "event_id"}
        } == {
            key: value for key, value in new.items() if key not in {"time_ms", "event_id"}
        }
        expected = float(
            new["route_index"] * 10000
            + new["episode"] * 100
            + new["position"] * 5.5
        )
        assert new["time_ms"] == expected
        assert new["event_id"].startswith("rd006-v2-ext-")


def test_v2_prospective_identity_and_fixed_constants() -> None:
    assert PROTOCOL_ID == (
        "rv02-rd006-external-learning-reachability-a-v2-lag-alignment"
    )
    assert PARENT_AUDIT_HEAD == "2e4b27b620c7fdd2d4d1803df0f11f13b5ed28e8"
    assert WITHIN_ROUTE_EXTERNAL_EVENT_POSITION_INTERVAL_MS == 5.5
    assert RD006Config().initial_delay_ms == 5.0
    assert RD006Config().minimum_return_lag_ms == 0.5
    assert RD006Config().maximum_return_lag_ms == 6.5
