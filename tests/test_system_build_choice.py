from sparkbrain.system_build import PredictiveRevisionPilot
from sparkbrain.v03_seed import SensorySample


def obs(i: int, x: float) -> SensorySample:
    return SensorySample(str(i), float(i), f"s{i}", "synthetic", {"x": x})


def test_choice_with_two_models() -> None:
    pilot = PredictiveRevisionPilot()
    pilot.observe(obs(1, 0.0))
    pilot.feedback(1.0)
    pilot.observe(obs(2, 0.02))
    pilot.feedback(-1.0)
    decision = pilot.observe(obs(3, 0.01))
    assert decision.decision == "abstain"
