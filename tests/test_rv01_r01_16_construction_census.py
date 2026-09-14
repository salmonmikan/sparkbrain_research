from __future__ import annotations

import hashlib
import json

from sparkbrain.research.rv01.interference_contract import RouteExposure
from sparkbrain.research.rv01_r01_16_construction_census import _world_construction_record


class _SyntheticConstructionWorld:
    world_id = "synthetic:r01-16:construction-test"
    unit_count = 8
    threshold = 0.5
    lag_ms = 5.0
    cue_magnitude = 0.95
    routes = (
        RouteExposure("route:a", (0, 1, 2, 3), 2),
        RouteExposure("route:b", (4, 5, 6, 7), 2),
    )
    training_order = ("route:a", "route:b")
    probe_order = ("route:b", "route:a")

    def probe_horizon_ms(self, route: RouteExposure) -> float:
        return self.lag_ms * (len(route.units) + 3)

    def state_dict(self) -> dict[str, object]:
        return {
            "world_id": self.world_id,
            "unit_count": self.unit_count,
            "routes": [route.state_dict() for route in self.routes],
            "training_order": list(self.training_order),
            "probe_order": list(self.probe_order),
            "synthetic_test_identity": True,
        }

    def specification_hash(self) -> str:
        payload = json.dumps(self.state_dict(), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def test_construction_census_mechanics_do_not_open_capability() -> None:
    row = _world_construction_record(_SyntheticConstructionWorld())

    assert row["world"]["synthetic_test_identity"] is True
    assert row["capability_output_opened"] is False
    assert row["probe_executed"] is False
    assert row["held_out_capability_executed"] is False
    assert row["formal_execution_allowed"] is False
    assert row["queue_integrity"]["common_checkpoint_queue_empty"] is True
    assert row["queue_integrity"]["queued_propagation_count"] == 0
    assert len(row["cells"]) == 2
    assert {cell["probe_route_id"] for cell in row["cells"]} == {"route:a", "route:b"}
    assert len(row["pre_training"]) == len(row["post_training"])
    assert row["learner_api_hash"]
