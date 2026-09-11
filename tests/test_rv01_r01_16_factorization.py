from __future__ import annotations

from dataclasses import replace

import pytest

from sparkbrain.research.rv01_r01_16_factorization import (
    ConnectionState,
    QueuedPropagationSnapshot,
    R01_16FactorizationConstruction,
)


def _pre() -> tuple[ConnectionState, ...]:
    return (
        ConnectionState(0, 1, 0.10, 5.0, True),
        ConnectionState(1, 2, 0.20, 6.0, True),
        ConnectionState(2, 3, 0.30, 7.0, False),
    )


def _post() -> tuple[ConnectionState, ...]:
    return (
        ConnectionState(0, 1, 0.15, 5.0, True),
        ConnectionState(1, 2, 0.20, 4.5, True),
        ConnectionState(2, 3, 0.30, 7.0, False),
    )


def test_r01_16_constructs_exact_factorization_arms() -> None:
    construction = R01_16FactorizationConstruction(
        pre_training=_pre(),
        post_training=_post(),
    )

    by_arm = {
        arm: {row.key: row for row in construction.arm_inventory(arm)}
        for arm in ("F0", "FW", "FD", "FWD")
    }
    assert by_arm["F0"][(0, 1)].weight == 0.15
    assert by_arm["FW"][(0, 1)].weight == 0.10
    assert by_arm["FD"][(0, 1)].weight == 0.15
    assert by_arm["FWD"][(0, 1)].weight == 0.10

    assert by_arm["F0"][(1, 2)].delay_ms == 4.5
    assert by_arm["FW"][(1, 2)].delay_ms == 4.5
    assert by_arm["FD"][(1, 2)].delay_ms == 6.0
    assert by_arm["FWD"][(1, 2)].delay_ms == 6.0

    summary = construction.require_any_prospective_contrast()
    assert summary.weight_changed_edges == ((0, 1),)
    assert summary.delay_changed_edges == ((1, 2),)
    assert summary.weight_contrast_ready is True
    assert summary.delay_contrast_ready is True
    assert len(set(summary.arm_sha256.values())) == 4


def test_r01_16_rejects_stale_queue_on_changed_connection() -> None:
    queued = (
        QueuedPropagationSnapshot(
            event_id="queued-0-1",
            source_id=0,
            target_id=1,
            queued_weight=0.15,
            queued_delay_ms=5.0,
        ),
    )

    with pytest.raises(RuntimeError, match="queue-integrity gate failed"):
        R01_16FactorizationConstruction(
            pre_training=_pre(),
            post_training=_post(),
            queued_propagation=queued,
        )


def test_r01_16_allows_queue_on_unchanged_connection() -> None:
    queued = (
        QueuedPropagationSnapshot(
            event_id="queued-2-3",
            source_id=2,
            target_id=3,
            queued_weight=0.30,
            queued_delay_ms=7.0,
        ),
    )
    construction = R01_16FactorizationConstruction(
        pre_training=_pre(),
        post_training=_post(),
        queued_propagation=queued,
    )

    assert construction.require_any_prospective_contrast().queue_sha256


def test_r01_16_rejects_topology_and_plasticity_drift() -> None:
    missing = _post()[:-1]
    with pytest.raises(ValueError, match="topology drifted"):
        R01_16FactorizationConstruction(
            pre_training=_pre(),
            post_training=missing,
        )

    plasticity_drift = (
        _post()[0],
        _post()[1],
        replace(_post()[2], plastic=True),
    )
    with pytest.raises(ValueError, match="plastic flag drifted"):
        R01_16FactorizationConstruction(
            pre_training=_pre(),
            post_training=plasticity_drift,
        )


def test_r01_16_rejects_coercible_and_boolean_numeric_fields() -> None:
    string_weight = replace(_pre()[0], weight="0.10")  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="real numeric value"):
        R01_16FactorizationConstruction(
            pre_training=(string_weight, *_pre()[1:]),
            post_training=_post(),
        )

    boolean_delay = replace(_pre()[0], delay_ms=True)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="real numeric value"):
        R01_16FactorizationConstruction(
            pre_training=(boolean_delay, *_pre()[1:]),
            post_training=_post(),
        )


def test_r01_16_rejects_zero_connection_and_queued_delays() -> None:
    zero_delay = replace(_pre()[0], delay_ms=0.0)
    with pytest.raises(ValueError, match="delay_ms must be positive"):
        R01_16FactorizationConstruction(
            pre_training=(zero_delay, *_pre()[1:]),
            post_training=_post(),
        )

    queued = (
        QueuedPropagationSnapshot(
            event_id="queued-zero-delay",
            source_id=2,
            target_id=3,
            queued_weight=0.30,
            queued_delay_ms=0.0,
        ),
    )
    with pytest.raises(ValueError, match="queued delay_ms must be positive"):
        R01_16FactorizationConstruction(
            pre_training=_pre(),
            post_training=_post(),
            queued_propagation=queued,
        )


def test_r01_16_hashes_connection_inventories_in_canonical_edge_order() -> None:
    construction = R01_16FactorizationConstruction(
        pre_training=tuple(reversed(_pre())),
        post_training=tuple(reversed(_post())),
    )

    summary = construction.summary()
    assert summary.pre_training_sha256 == construction.inventory_sha256(_pre())
    assert summary.post_training_sha256 == construction.inventory_sha256(_post())
    assert summary.arm_sha256["F0"] == summary.post_training_sha256


def test_r01_16_stops_when_factorization_is_structurally_noop() -> None:
    construction = R01_16FactorizationConstruction(
        pre_training=_pre(),
        post_training=_pre(),
    )

    summary = construction.summary()
    assert summary.weight_changed_edges == ()
    assert summary.delay_changed_edges == ()
    with pytest.raises(RuntimeError, match="no learned weight or delay contrast"):
        construction.require_any_prospective_contrast()
