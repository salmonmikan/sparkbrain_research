from sparkbrain.system_build import PilotConfig, PredictiveRevisionPilot
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


def test_choice_checks_all_nearby_hypotheses_before_acting() -> None:
    pilot = PredictiveRevisionPilot(PilotConfig(reuse_error=0.05))
    pilot.observe(obs(1, 0.0))
    assert pilot.feedback(0.0).action == "create"
    pilot.observe(obs(2, 0.02))
    assert pilot.feedback(0.1).action == "split"
    pilot.observe(obs(3, 0.04))
    assert pilot.feedback(1.0).action == "split"

    decision = pilot.observe(obs(4, 0.01))

    assert len(decision.candidates) == 3
    assert decision.decision == "abstain"
    assert decision.reason == "competing_hypotheses_ambiguous"
