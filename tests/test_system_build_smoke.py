from sparkbrain.system_build import PredictiveRevisionPilot


def test_system_build_smoke() -> None:
    pilot = PredictiveRevisionPilot()
    assert pilot.inspect()["scientific_credit"] == 0
