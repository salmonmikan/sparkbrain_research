from sparkbrain.system_build import PredictiveRevisionPilot
from sparkbrain.v03_seed import SensorySample


def s(i: int, x: float) -> SensorySample:
    return SensorySample(str(i), float(i), f"s{i}", "synthetic", {"x": x})


def test_reuse() -> None:
    pilot = PredictiveRevisionPilot()
    pilot.observe(s(1, 0.0))
    pilot.feedback(1.0)
    pilot.observe(s(2, 0.02))
    pilot.feedback(-1.0)
    before = pilot.inspect()["hypotheses"][1].copy()
    pilot.observe(s(3, 0.0))
    result = pilot.feedback(1.05)
    assert result.action == "reuse"
    assert result.state_id == "state-001"
    assert pilot.inspect()["hypotheses"][1] == before
