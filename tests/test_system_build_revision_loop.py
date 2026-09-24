from sparkbrain.system_build import PredictiveRevisionPilot
from sparkbrain.v03_seed import SensorySample


def row(i: int, x: float) -> SensorySample:
    return SensorySample(
        sample_id=str(i),
        time=float(i),
        source_id=f"s{i}",
        modality="synthetic",
        values={"x": x},
    )


def test_revision_loop() -> None:
    pilot = PredictiveRevisionPilot()
    assert pilot.observe(row(1, 0.0)).decision == "abstain"
    assert pilot.feedback(1.0).action == "create"
    pilot.observe(row(2, 0.02))
    assert pilot.feedback(-1.0).action == "split"
    assert len(pilot.inspect()["hypotheses"]) == 2
