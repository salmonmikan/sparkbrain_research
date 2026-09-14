from __future__ import annotations

from pathlib import Path

import pytest

from sparkbrain.research.rv01_r01_16_identity import (
    R01_16_DEVELOPMENT_SEEDS,
    development_identity_grid,
)
from sparkbrain.research.rv01_r01_16_retained_history import (
    RetainedHistorySnapshot,
    build_retained_history_snapshot,
    known_retained_namespace,
)


def test_r01_16_known_retained_namespace_is_deterministic_and_collision_free() -> None:
    seed_ids, world_ids = known_retained_namespace()

    assert len(seed_ids) == 58
    assert len(world_ids) == 290
    assert seed_ids == tuple(sorted(set(seed_ids)))
    assert world_ids == tuple(sorted(set(world_ids)))
    assert set(seed_ids).isdisjoint(R01_16_DEVELOPMENT_SEEDS)
    assert set(world_ids).isdisjoint(
        row.world_id for row in development_identity_grid()
    )


def test_r01_16_retained_history_builder_opens_only_after_bound_audits() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    snapshot = build_retained_history_snapshot(repo_root)

    assert snapshot.authoritative_complete is True
    assert snapshot.unresolved_evidence_classes == ()
    assert "pre-r01-12-repository-retained-identity-boundary" in (
        snapshot.verified_evidence_classes
    )
    assert "r01-12-development-contract-and-manifest" in (
        snapshot.verified_evidence_classes
    )
    assert "r01-15-raw-development-world-identity-audit" in (
        snapshot.verified_evidence_classes
    )
    assert "r01-15-reserved-held-out-identity-audit" in (
        snapshot.verified_evidence_classes
    )

    registry = snapshot.to_collision_registry()
    registry.validate()
    assert registry.authoritative_complete is True
    assert len(registry.consumed_or_reserved_seed_ids) == 58
    assert len(registry.consumed_or_reserved_world_ids) == 290


def test_r01_16_partial_snapshot_cannot_claim_authoritative_registry() -> None:
    snapshot = RetainedHistorySnapshot(
        source_paths=("docs/research/example.json",),
        consumed_or_reserved_seed_ids=(1,),
        consumed_or_reserved_world_ids=("development:disjoint-routes:1",),
        verified_evidence_classes=("example",),
        unresolved_evidence_classes=("unresolved-example",),
    )

    assert snapshot.state_dict()["authoritative_complete"] is False
    with pytest.raises(ValueError, match="cannot be opened"):
        snapshot.to_collision_registry()
