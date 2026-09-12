from __future__ import annotations

from dataclasses import fields

import pytest

from sparkbrain.v061_a01.md002_p4_fixture import (
    P4BoundaryAncestrySpec,
    P4ConditionSpec,
    P4ProspectiveFixture,
)


def _fixture() -> P4ProspectiveFixture:
    return P4ProspectiveFixture(
        lineage_a_proposal_id="proposal:a",
        lineage_b_proposal_id="proposal:b",
    )


def test_p4_fixture_binds_separate_and_genuinely_merged_ancestry() -> None:
    fixture = _fixture()
    fixture.validate_matrix()

    separate_a, separate_b, merged = fixture.boundary_specs
    assert separate_a.source_proposal_ids == ("proposal:a",)
    assert separate_b.source_proposal_ids == ("proposal:b",)
    assert merged.source_proposal_ids == ("proposal:a", "proposal:b")
    assert not separate_a.is_merged
    assert not separate_b.is_merged
    assert merged.is_merged


def test_p4_matrix_is_fixed_to_six_preregistered_condition_shapes() -> None:
    fixture = _fixture()
    fixture.validate_matrix()

    assert tuple(row.condition_id for row in fixture.conditions) == (
        "p4-separate-confirmation",
        "p4-merged-confirmation",
        "p4-merged-separating-confirmation",
        "p4-merged-separating-contradiction",
        "p4-merged-absence",
        "p4-merged-replay",
    )
    assert [row.evidence_mode for row in fixture.conditions] == [
        "confirmation",
        "confirmation",
        "confirmation",
        "contradiction",
        "absence",
        "internal-replay",
    ]


def test_p4_fixture_does_not_accept_caller_selected_runtime_lineages() -> None:
    names = {field.name for field in fields(P4ConditionSpec)}
    assert "active_lineages_before" not in names
    assert "active_lineages_after" not in names
    assert "boundary_source_proposal_ids" not in names


def test_p4_absence_and_replay_controls_cannot_return_external_evidence() -> None:
    for evidence_mode in ("absence", "internal-replay"):
        row = P4ConditionSpec(
            condition_id=f"bad-{evidence_mode}",
            boundary_mode="merged",
            evidence_mode=evidence_mode,
            requires_later_separation=False,
            returned_external_evidence=True,
            positive_credit_permitted=False,
        )
        with pytest.raises(ValueError, match="cannot return external evidence"):
            row.validate()


def test_p4_absence_and_replay_controls_cannot_permit_positive_credit() -> None:
    row = P4ConditionSpec(
        condition_id="bad-replay-credit",
        boundary_mode="merged",
        evidence_mode="internal-replay",
        requires_later_separation=False,
        returned_external_evidence=False,
        positive_credit_permitted=True,
    )
    with pytest.raises(ValueError, match="cannot permit positive causal credit"):
        row.validate()


def test_p4_contradiction_cannot_be_declared_positive_credit() -> None:
    row = P4ConditionSpec(
        condition_id="bad-contradiction-credit",
        boundary_mode="merged",
        evidence_mode="contradiction",
        requires_later_separation=True,
        returned_external_evidence=True,
        positive_credit_permitted=True,
    )
    with pytest.raises(ValueError, match="contradiction cannot be declared positive-credit"):
        row.validate()


def test_p4_later_separation_requires_merged_external_evidence() -> None:
    row = P4ConditionSpec(
        condition_id="bad-separate-separation",
        boundary_mode="separate",
        evidence_mode="confirmation",
        requires_later_separation=True,
        returned_external_evidence=True,
        positive_credit_permitted=True,
    )
    with pytest.raises(ValueError, match="defined only for merged ancestry"):
        row.validate()


def test_p4_fixture_rejects_identical_lineages() -> None:
    fixture = P4ProspectiveFixture(
        lineage_a_proposal_id="proposal:same",
        lineage_b_proposal_id="proposal:same",
    )
    with pytest.raises(ValueError, match="two distinct proposal lineages"):
        fixture.validate()


def test_p4_boundary_spec_rejects_duplicate_proposal_ids() -> None:
    value = P4BoundaryAncestrySpec(
        boundary_id="boundary:merged",
        source_proposal_ids=("proposal:a", "proposal:a"),
    )
    with pytest.raises(ValueError, match="must be unique"):
        value.validate()
