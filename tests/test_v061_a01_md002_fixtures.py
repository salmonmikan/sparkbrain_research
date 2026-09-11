from __future__ import annotations

import pytest

from sparkbrain.v061_a01.md002_fixtures import (
    FrozenPartitionBytes,
    P2WorldOnlyFixture,
)
from sparkbrain.v061_a01.md002_protocol import bytes_sha256


def fixture() -> P2WorldOnlyFixture:
    return P2WorldOnlyFixture(
        checkpoint=FrozenPartitionBytes(
            local=b"local-state-v1",
            field=b"field-state-v1",
            consistency=b"consistency-state-v1",
            return_address=b"transient-r-v1",
        ),
        control_world_relation=b"anonymous-world-relation:a",
        intervention_world_relation=b"anonymous-world-relation:b",
        admissible_external_evidence=b"external-evidence:fixed",
    )


def test_p2_arms_restore_identical_partition_bytes_and_evidence() -> None:
    value = fixture()
    control = value.arm("control")
    intervention = value.arm("intervention")

    assert control.partitions == intervention.partitions == value.checkpoint
    assert (
        control.admissible_external_evidence
        == intervention.admissible_external_evidence
        == b"external-evidence:fixed"
    )
    assert control.world_relation != intervention.world_relation
    assert control.world_relation_sha256 != intervention.world_relation_sha256


def test_p2_fixture_builds_fail_closed_world_only_contract() -> None:
    value = fixture()
    contract = value.prospective_contract()
    expected = value.checkpoint.snapshot()

    assert contract.control == contract.intervention == expected
    assert contract.control_world_relation_sha256 == bytes_sha256(
        b"anonymous-world-relation:a"
    )
    assert contract.intervention_world_relation_sha256 == bytes_sha256(
        b"anonymous-world-relation:b"
    )
    assert contract.admissible_external_evidence_sha256 == bytes_sha256(
        b"external-evidence:fixed"
    )


def test_p2_fixture_rejects_equal_world_relations() -> None:
    value = P2WorldOnlyFixture(
        checkpoint=fixture().checkpoint,
        control_world_relation=b"same",
        intervention_world_relation=b"same",
        admissible_external_evidence=b"fixed",
    )
    with pytest.raises(ValueError, match="genuinely changed world relation"):
        value.validate()


def test_p2_fixture_rejects_empty_partition_or_evidence_bytes() -> None:
    with pytest.raises(ValueError, match="local must be non-empty"):
        FrozenPartitionBytes(
            local=b"",
            field=b"field",
            consistency=b"consistency",
            return_address=None,
        ).validate()

    value = P2WorldOnlyFixture(
        checkpoint=fixture().checkpoint,
        control_world_relation=b"a",
        intervention_world_relation=b"b",
        admissible_external_evidence=b"",
    )
    with pytest.raises(ValueError, match="admissible_external_evidence must be non-empty"):
        value.validate()


def test_p2_fixture_is_construction_only_and_does_not_apply_evidence() -> None:
    value = fixture()
    before = value.checkpoint.snapshot()
    value.prospective_contract()
    after = value.checkpoint.snapshot()
    assert before == after
