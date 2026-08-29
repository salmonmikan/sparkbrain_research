from __future__ import annotations

from sparkbrain.v06 import EventOrigin, RuntimePulse
from sparkbrain.v06.local_expectation import (
    LocalExpectationConfig,
    LocalTemporalExpectation,
)


def pulse(
    event_id: str,
    *,
    time_ms: float,
    target: str,
    magnitude: float = 0.8,
    polarity: int = 1,
    origin: EventOrigin = EventOrigin.EXTERNAL,
) -> RuntimePulse:
    return RuntimePulse(
        event_id=event_id,
        time_ms=time_ms,
        target=target,
        magnitude=magnitude,
        polarity=polarity,
        origin=origin,
    )


def trained_model() -> LocalTemporalExpectation:
    model = LocalTemporalExpectation(
        LocalExpectationConfig(
            minimum_observations=2,
            minimum_confidence=0.1,
        )
    )
    model.observe_external_transition(
        pulse("a-1", time_ms=0, target="unit:1"),
        pulse("b-1", time_ms=5, target="unit:2", magnitude=0.6),
    )
    model.observe_external_transition(
        pulse("a-2", time_ms=20, target="unit:1"),
        pulse("b-2", time_ms=25, target="unit:2", magnitude=0.8),
    )
    return model


def test_repeated_external_lag_creates_local_proposal() -> None:
    model = trained_model()
    rows = model.proposals_for(
        pulse("a-test", time_ms=100, target="unit:1"),
        origin_state_hash="s" * 64,
    )
    assert len(rows) == 1
    assert rows[0].target == "unit:2"
    assert rows[0].predicted_arrival_ms == 105
    assert rows[0].magnitude == 0.7
    assert rows[0].local_path_ids == ("local:unit:1->unit:2",)


def test_prediction_is_read_only_for_learned_transition_counts() -> None:
    model = trained_model()
    before = model.external_transition_count
    before_stats = model.state_dict()["transitions"]
    model.proposals_for(
        pulse("a-test", time_ms=100, target="unit:1"),
        origin_state_hash="s" * 64,
    )
    assert model.external_transition_count == before
    assert model.state_dict()["transitions"] == before_stats


def test_endogenous_target_cannot_train_model() -> None:
    model = LocalTemporalExpectation()
    try:
        model.observe_external_transition(
            pulse("a", time_ms=0, target="unit:1"),
            pulse(
                "endo:p",
                time_ms=5,
                target="unit:2",
                origin=EventOrigin.ENDOGENOUS_UNCONFIRMED,
            ),
        )
    except ValueError as exc:
        assert "target must be an external observation" in str(exc)
    else:
        raise AssertionError("endogenous target was accepted as training evidence")


def test_endogenous_source_cannot_train_model() -> None:
    model = LocalTemporalExpectation()
    try:
        model.observe_external_transition(
            pulse(
                "endo:p",
                time_ms=0,
                target="unit:1",
                origin=EventOrigin.ENDOGENOUS_CONFIRMED,
            ),
            pulse("b", time_ms=5, target="unit:2"),
        )
    except ValueError as exc:
        assert "source must be an external observation" in str(exc)
    else:
        raise AssertionError("endogenous source was accepted as training evidence")


def test_insufficient_observations_produce_no_proposal() -> None:
    model = LocalTemporalExpectation(LocalExpectationConfig(minimum_observations=2))
    model.observe_external_transition(
        pulse("a", time_ms=0, target="unit:1"),
        pulse("b", time_ms=5, target="unit:2"),
    )
    assert (
        model.proposals_for(
            pulse("test", time_ms=20, target="unit:1"),
            origin_state_hash="s" * 64,
        )
        == ()
    )


def test_high_lag_variance_reduces_confidence() -> None:
    stable = LocalTemporalExpectation(
        LocalExpectationConfig(minimum_observations=2, minimum_confidence=0)
    )
    variable = LocalTemporalExpectation(
        LocalExpectationConfig(minimum_observations=2, minimum_confidence=0)
    )
    for index, lag in enumerate((5.0, 5.0), start=1):
        stable.observe_external_transition(
            pulse(f"sa-{index}", time_ms=index * 20, target="unit:1"),
            pulse(f"sb-{index}", time_ms=index * 20 + lag, target="unit:2"),
        )
    for index, lag in enumerate((1.0, 9.0), start=1):
        variable.observe_external_transition(
            pulse(f"va-{index}", time_ms=index * 20, target="unit:1"),
            pulse(f"vb-{index}", time_ms=index * 20 + lag, target="unit:2"),
        )
    source = pulse("test", time_ms=100, target="unit:1")
    stable_confidence = stable.proposals_for(
        source,
        origin_state_hash="s" * 64,
    )[0].confidence
    variable_confidence = variable.proposals_for(
        source,
        origin_state_hash="s" * 64,
    )[0].confidence
    assert stable_confidence > variable_confidence


def test_reverse_direction_is_a_distinct_local_transition() -> None:
    model = trained_model()
    assert (
        model.proposals_for(
            pulse("reverse", time_ms=100, target="unit:2"),
            origin_state_hash="s" * 64,
        )
        == ()
    )


def test_endogenous_source_can_query_but_not_train() -> None:
    model = trained_model()
    source = pulse(
        "endo:p-0",
        time_ms=100,
        target="unit:1",
        origin=EventOrigin.ENDOGENOUS_CONFIRMED,
    )
    rows = model.proposals_for(source, origin_state_hash="s" * 64)
    assert rows[0].generation_depth == 1
    assert rows[0].parent_proposal_ids == ("p-0",)
    assert model.external_transition_count == 2


def test_state_round_trip_is_deterministic() -> None:
    model = trained_model()
    restored = LocalTemporalExpectation.from_state_dict(model.state_dict())
    assert restored.state_dict() == model.state_dict()
    assert restored.state_hash() == model.state_hash()


def test_state_contains_no_explicit_assembly_fields() -> None:
    state = trained_model().state_dict()
    serialized = str(state).lower()
    assert "assembly_id" not in serialized
    assert "motif_id" not in serialized
