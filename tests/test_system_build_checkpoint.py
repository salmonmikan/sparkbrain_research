from pathlib import Path
from tempfile import TemporaryDirectory

from sparkbrain.system_build import PilotCheckpointManager, PredictiveRevisionPilot
from sparkbrain.v03_seed import SensorySample


def s(i: int, x: float) -> SensorySample:
    return SensorySample(str(i), float(i), f"s{i}", "synthetic", {"x": x})


def test_checkpoint_next_step_equality() -> None:
    pilot = PredictiveRevisionPilot()
    pilot.observe(s(1, 0.0))
    pilot.feedback(1.0)
    pilot.observe(s(2, 0.02))
    pilot.feedback(-1.0)
    pilot.observe(s(3, 0.0))
    with TemporaryDirectory() as tmp:
        root = Path(tmp) / "checkpoint"
        PilotCheckpointManager.save(pilot, root)
        restored = PilotCheckpointManager.load(root)
        assert restored.inspect() == pilot.inspect()
        left = pilot.feedback(1.05)
        right = restored.feedback(1.05)
        assert left == right
        assert restored.inspect() == pilot.inspect()
