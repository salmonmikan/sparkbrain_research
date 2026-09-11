from __future__ import annotations

import pytest

from sparkbrain.research.rv01_r01_16_factorization import (
    ConnectionState,
    R01_16FactorizationConstruction,
)
from sparkbrain.research.rv01_r01_16_reachability import (
    build_factor_reachability_certificate,
)


def _construction() -> R01_16FactorizationConstruction:
    pre = (
        ConnectionState(0, 1, 0.10, 2.0, True),
        ConnectionState(1, 2, 0.20, 4.0, True),
        ConnectionState(0, 3, 0.10, 3.0, True),
        ConnectionState(3, 4, 0.10, 20.0, True),
    )
    post = (
        ConnectionState(0, 1, 0.15, 2.0, True),
        ConnectionState(1, 2, 0.20, 1.5, True),
        ConnectionState(0, 3, 0.10, 3.0, True),
        ConnectionState(3, 4, 0.30, 20.0, True),
    )
    return R01_16FactorizationConstruction(pre_training=pre, post_training=post)


def test_reachability_uses_conservative_pre_post_delay_and_fixed_horizon() -> None:
    certificate = build_factor_reachability_certificate(
        _construction(),
        cue_source_ids=(0,),
        probe_horizon_ms=10.0,
    )

    assert certificate.weight_changed_edges == ((0, 1), (3, 4))
    assert certificate.delay_changed_edges == ((1, 2),)
    assert tuple(
        edge.key for edge in certificate.reachable_weight_edges
    ) == ((0, 1),)
    assert tuple(
        edge.key for edge in certificate.reachable_delay_edges
    ) == ((1, 2),)
    assert certificate.reachable_delay_edges[0].conservative_edge_delay_ms == 4.0
    assert certificate.reachable_delay_edges[0].earliest_target_arrival_ms == 6.0
    assert certificate.weight_eligible is True
    assert certificate.delay_eligible is True
    assert certificate.combined_eligible is True
    assert len(certificate.sha256) == 64


def test_off_route_changed_edge_is_not_a_behavioral_negative_eligibility_cell() -> None:
    certificate = build_factor_reachability_certificate(
        _construction(),
        cue_source_ids=(1,),
        probe_horizon_ms=5.0,
    )

    assert certificate.weight_changed_edges == ((0, 1), (3, 4))
    assert certificate.reachable_weight_edges == ()
    assert tuple(
        edge.key for edge in certificate.reachable_delay_edges
    ) == ((1, 2),)
    assert certificate.weight_eligible is False
    assert certificate.delay_eligible is True


def test_reachability_fails_closed_on_invalid_cue_or_horizon() -> None:
    with pytest.raises(ValueError, match="at least one cue source"):
        build_factor_reachability_certificate(
            _construction(),
            cue_source_ids=(),
            probe_horizon_ms=10.0,
        )

    with pytest.raises(ValueError, match="not present"):
        build_factor_reachability_certificate(
            _construction(),
            cue_source_ids=(999,),
            probe_horizon_ms=10.0,
        )

    with pytest.raises(ValueError, match="finite and positive"):
        build_factor_reachability_certificate(
            _construction(),
            cue_source_ids=(0,),
            probe_horizon_ms=0.0,
        )


def test_reachability_is_deterministic_under_connection_inventory_order() -> None:
    original = _construction()
    reordered = R01_16FactorizationConstruction(
        pre_training=tuple(reversed(original.pre_training)),
        post_training=tuple(reversed(original.post_training)),
    )

    left = build_factor_reachability_certificate(
        original,
        cue_source_ids=(0,),
        probe_horizon_ms=10.0,
    )
    right = build_factor_reachability_certificate(
        reordered,
        cue_source_ids=(0,),
        probe_horizon_ms=10.0,
    )

    assert left.state_dict() == right.state_dict()
    assert left.sha256 == right.sha256
