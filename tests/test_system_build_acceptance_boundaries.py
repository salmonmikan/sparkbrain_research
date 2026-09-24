import pytest

from sparkbrain.system_build import PilotConfig, PredictiveRevisionPilot
from sparkbrain.v03_seed import SensorySample


def sample(
    i: int,
    *,
    values: dict[str, float] | None = None,
    metadata: dict[str, object] | None = None,
    entity_hint: str | None = None,
) -> SensorySample:
    return SensorySample(
        sample_id=str(i),
        time=float(i),
        source_id=f"s{i}",
        modality="synthetic",
        values=values or {"x": 0.0},
        entity_hint=entity_hint,
        metadata=metadata or {},
    )


@pytest.mark.parametrize(
    "privileged_name",
    [
        "state",
        "state_id",
        "episode",
        "episode_id",
        "entity",
        "entity_id",
        "entity_key",
        "entity_slot",
        "evaluator",
        "gold",
        "target",
    ],
)
def test_privileged_observation_channels_are_rejected(privileged_name: str) -> None:
    pilot = PredictiveRevisionPilot()
    with pytest.raises(ValueError):
        pilot.observe(sample(1, values={privileged_name: 1.0}))


@pytest.mark.parametrize(
    "privileged_name",
    [
        "state",
        "episode",
        "entity",
        "entity_id",
        "entity_key",
        "entity_slot",
        "evaluator",
        "gold",
        "target",
    ],
)
def test_nested_privileged_metadata_is_rejected(privileged_name: str) -> None:
    pilot = PredictiveRevisionPilot()
    with pytest.raises(ValueError):
        pilot.observe(
            sample(
                1,
                metadata={"external": {"payload": {privileged_name: "blocked"}}},
            )
        )


def test_entity_hint_is_rejected_explicitly() -> None:
    pilot = PredictiveRevisionPilot()
    with pytest.raises(ValueError, match="entity_hint"):
        pilot.observe(sample(1, entity_hint="entity-001"))


def test_max_context_scalars_accepts_exact_boundary_and_rejects_overflow() -> None:
    allowed = {f"x{index:02d}": float(index) for index in range(64)}
    pilot = PredictiveRevisionPilot(PilotConfig(max_context_scalars=64))
    assert pilot.observe(sample(1, values=allowed)).decision == "abstain"
    pilot.feedback(0.0)

    overflow = {f"x{index:02d}": float(index) for index in range(65)}
    rejected = PredictiveRevisionPilot(PilotConfig(max_context_scalars=64))
    with pytest.raises(ValueError, match="max_context_scalars"):
        rejected.observe(sample(2, values=overflow))


def test_max_hypotheses_accepts_exact_boundary_and_fails_closed_on_overflow() -> None:
    pilot = PredictiveRevisionPilot(PilotConfig(max_hypotheses=16))
    for index in range(16):
        pilot.observe(sample(index + 1))
        revision = pilot.feedback(float(index))
        assert revision.state_count == index + 1

    assert len(pilot.inspect()["hypotheses"]) == 16
    pilot.observe(sample(17))
    with pytest.raises(RuntimeError, match="max_hypotheses"):
        pilot.feedback(16.0)
    assert len(pilot.inspect()["hypotheses"]) == 16


@pytest.mark.parametrize(
    ("config", "message"),
    [
        (PilotConfig(max_hypotheses=17), "max_hypotheses"),
        (PilotConfig(max_context_scalars=65), "max_context_scalars"),
    ],
)
def test_resource_budget_configuration_cannot_exceed_analyst_ceiling(
    config: PilotConfig,
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        config.validate()
