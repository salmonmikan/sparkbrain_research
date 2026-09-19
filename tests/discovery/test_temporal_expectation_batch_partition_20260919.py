from __future__ import annotations

from sparkbrain.v04 import IntegratedV04Brain, SignalPulse, V04BrainConfig


def _pulse(time_ms: float) -> SignalPulse:
    return SignalPulse(time_ms=time_ms, channel="A", magnitude=0.72, source_id="discovery")


def _omission_times(*results: object) -> list[float]:
    times: list[float] = []
    for result in results:
        for pulse in result.input_pulses:  # type: ignore[attr-defined]
            if pulse.channel.startswith("omission:"):
                times.append(pulse.time_ms)
    return times


def test_same_input_timeline_changes_omission_history_when_ingestion_partition_changes() -> None:
    """EXPLORATORY / NON_EVIDENTIARY.

    The physical input timeline is identical in both arms. Only the API batching
    differs. This intentionally characterizes current semantics; it is not a
    regression contract for desired future behavior.
    """

    config = V04BrainConfig(enable_plasticity=False, enable_expectations=True)

    batched = IntegratedV04Brain(config)
    batched_result = batched.ingest_pulses(
        tuple(_pulse(time_ms) for time_ms in (0.0, 10.0, 20.0, 100.0)),
        settle_ms=35.0,
    )

    split = IntegratedV04Brain(config)
    split_first = split.ingest_pulses(
        tuple(_pulse(time_ms) for time_ms in (0.0, 10.0, 20.0)),
        settle_ms=35.0,
    )
    split_second = split.ingest_pulses((_pulse(100.0),), settle_ms=35.0)

    assert batched_result.end_ms == split_second.end_ms == 135.0
    assert _omission_times(batched_result) == []
    assert _omission_times(split_first, split_second) == [33.0]

    # Both arms have observed the same external pulses and converge to the same
    # learned interval, but the internally generated omission history differs.
    assert batched.expectations.interval["A"] == split.expectations.interval["A"] == 34.5
    assert batched.expectations.last_time["A"] == split.expectations.last_time["A"] == 100.0

    # The extra internally generated omission pulse reaches the field, so the
    # final integrated field trajectory is no longer partition-invariant.
    assert batched.field.state_hash() != split.field.state_hash()
