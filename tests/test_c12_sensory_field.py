from __future__ import annotations

import json
from dataclasses import replace

import pytest

from sparkbrain.v03_seed import (
    AdaptiveSensoryField,
    PerceptualSpark,
    SensorySample,
)


def _sample(
    index: int,
    values: dict[str, float],
    *,
    omitted: tuple[str, ...] = (),
    metadata: dict[str, object] | None = None,
) -> SensorySample:
    return SensorySample(
        sample_id=f"sample:{index}",
        time=float(index),
        source_id="sensor:a",
        modality="vision",
        values=values,
        metadata=metadata or {},
        omitted_channels=omitted,
    )


def test_contracts_have_strict_canonical_round_trip() -> None:
    sample = _sample(0, {"猫": 0.4}, metadata={"nested": [1, "local"]})
    payload = sample.to_canonical_json()
    assert SensorySample.from_canonical_json(payload) == sample
    with pytest.raises(ValueError, match="strict canonical"):
        SensorySample.from_canonical_json(json.dumps(json.loads(payload), ensure_ascii=False))

    field = AdaptiveSensoryField()
    spark = field.observe(sample)[0]
    spark_payload = spark.to_canonical_json()
    assert PerceptualSpark.from_canonical_json(spark_payload) == spark
    with pytest.raises(ValueError, match="strict canonical"):
        PerceptualSpark.from_canonical_json(json.dumps(json.loads(spark_payload)))


@pytest.mark.parametrize(
    "metadata",
    [
        {"nested": {"truth": True}},
        {"items": [{"label": "gold"}]},
        {"test-only": 1},
        {"numeric": float("nan")},
        {"numeric": float("inf")},
        {"non_json": {1, 2}},
    ],
)
def test_forbidden_or_non_json_metadata_is_atomic(metadata: dict[str, object]) -> None:
    field = AdaptiveSensoryField()
    field.observe(_sample(0, {"stable": 1.0}))
    before = field.serialize_state()
    with pytest.raises(ValueError):
        field.observe(_sample(1, {"good": 1.0, "later": 2.0}, metadata=metadata))
    assert field.serialize_state() == before


def test_multichannel_midstream_error_is_atomic() -> None:
    field = AdaptiveSensoryField()
    field.observe(_sample(1, {"later": 1.0}))
    before = field.serialize_state()
    with pytest.raises(ValueError, match="backward"):
        field.observe(_sample(0, {"first": 1.0, "later": 0.0}))
    assert field.serialize_state() == before


def test_goal_is_bounded_traced_and_forbidden_key_is_atomic() -> None:
    field = AdaptiveSensoryField()
    field.observe(_sample(0, {"weak": 1.0}))
    field.observe(_sample(1, {"weak": 1.0}))
    result = field.observe_with_trace(
        _sample(2, {"weak": 0.4}), goal_bias={"vision:weak": 999.0}
    )
    row = result.channel_trace[0]
    assert row.goal_bias_requested == 999.0
    assert row.goal_bias_applied == 0.35
    assert result.sparks
    before = field.serialize_state()
    with pytest.raises(ValueError, match="forbidden goal"):
        field.observe(_sample(3, {"weak": 0.4}), goal_bias={"test-only": 0.1})
    assert field.serialize_state() == before


def test_all_channels_have_complete_accepted_or_suppressed_trace_and_counters() -> None:
    field = AdaptiveSensoryField()
    field.observe(_sample(0, {"change": 1.0, "repeat": 1.0, "quiet": 0.0}))
    result = field.observe_with_trace(
        _sample(1, {"change": -1.0, "repeat": 1.0, "quiet": 0.0})
    )
    assert {row.feature_id for row in result.channel_trace} == {
        "vision:change",
        "vision:quiet",
        "vision:repeat",
    }
    assert any(row.accepted for row in result.channel_trace)
    assert any(not row.accepted for row in result.channel_trace)
    for row in result.channel_trace:
        assert row.final_salience >= 0
        assert row.threshold >= 0
        assert row.goal_bias_applied <= 0.35
    counters = result.work_delta
    assert counters.channels_inspected == 3
    assert counters.features_scored == 3
    assert counters.state_updates == 3
    assert counters.sparks_emitted == counters.downstream_active_work == len(result.sparks)
    assert counters.suppressed_channels + counters.sparks_emitted == 3


def test_true_explicit_omission_recovers_after_habituation() -> None:
    field = AdaptiveSensoryField()
    for index in range(4):
        field.observe(_sample(index, {"tone": 1.0}))
    omitted = field.observe_with_trace(_sample(4, {}, omitted=("tone",)))
    assert omitted.sparks
    assert omitted.channel_trace[0].omission is True
    assert omitted.channel_trace[0].prediction_error > 0
    unseen = AdaptiveSensoryField()
    before = unseen.serialize_state()
    with pytest.raises(ValueError, match="previously observed"):
        unseen.observe(_sample(0, {}, omitted=("tone",)))
    assert unseen.serialize_state() == before


def test_serialization_replay_and_inspection_are_state_neutral() -> None:
    field = AdaptiveSensoryField()
    field.observe(_sample(0, {"a": 1.0, "b": 0.2}))
    snapshot = field.serialize_state()
    hash_before = field.state_hash()
    assert field.inspect_state()["sequence"] == 2
    assert field.feature_state("vision:a")["initialized"] is True
    assert field.state_hash() == hash_before

    replay = AdaptiveSensoryField.from_serialized_state(snapshot)
    next_sample = _sample(1, {"a": -1.0, "b": 0.2})
    original_result = field.observe_with_trace(next_sample)
    replay_result = replay.observe_with_trace(next_sample)
    assert original_result == replay_result
    assert field.serialize_state() == replay.serialize_state()

    for invalid in ("{", None):
        with pytest.raises(ValueError):
            AdaptiveSensoryField.from_serialized_state(invalid)  # type: ignore[arg-type]
    assert field.serialize_state() == replay.serialize_state()


def test_spark_validation_rejects_nonfinite_and_duplicate_parents() -> None:
    spark = AdaptiveSensoryField().observe(_sample(0, {"a": 1.0}))[0]
    with pytest.raises(ValueError, match="finite"):
        replace(spark, salience=float("nan")).to_canonical_json()
    with pytest.raises(ValueError, match="unique"):
        replace(spark, parents=("same", "same")).to_canonical_json()


@pytest.mark.parametrize(
    "ablation,zero_term",
    [
        ("no_goal", "goal_contribution"),
        ("no_habituation", "habituation_contribution"),
        ("no_prediction_error", "prediction_error_contribution"),
        ("no_novelty", "novelty_contribution"),
        ("no_magnitude", "magnitude_contribution"),
    ],
)
def test_each_salience_term_is_individually_ablatable(
    ablation: str, zero_term: str
) -> None:
    field = AdaptiveSensoryField()
    field.observe(_sample(0, {"a": 1.0}))
    result = field.observe_with_trace(
        _sample(1, {"a": -1.0}),
        goal_bias={"vision:a": 0.35},
        ablations=frozenset({ablation}),
    )
    assert getattr(result.channel_trace[0], zero_term) == 0.0
    assert result.channel_trace[0].ablations == (ablation,)


def test_bypass_emits_below_threshold_without_hiding_dense_work() -> None:
    field = AdaptiveSensoryField()
    values = {f"quiet-{index}": 0.0 for index in range(10)}
    result = field.observe_with_trace(_sample(0, values), bypass=True)
    assert len(result.sparks) == len(values) == 10
    assert result.work_delta.channels_inspected == result.work_delta.features_scored == 10
    assert result.work_delta.downstream_active_work == 10
