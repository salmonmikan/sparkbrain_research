from __future__ import annotations

from pathlib import Path

from sparkbrain.evaluation.v061_causal_lineage_information_audit import (
    audit_causal_lineage_information,
)


def _repository_root() -> Path:
    return Path(__file__).parents[2]


def test_boundary_event_contains_an_outbound_causal_lineage() -> None:
    audit = audit_causal_lineage_information(_repository_root())
    assert audit.boundary_has_causal_lineage is True
    assert {
        "source_spark_id",
        "source_proposal_ids",
        "source_unit_id",
        "generation_depth",
        "source_state_hash",
    }.issubset(audit.boundary_event.fields)
    assert "source_proposal_ids" in audit.boundary_event.return_address_fields


def test_consistency_state_retains_no_proposal_or_path_return_address() -> None:
    audit = audit_causal_lineage_information(_repository_root())
    forbidden = {
        "source_proposal_ids",
        "parent_proposal_ids",
        "local_path_ids",
    }
    assert audit.consistency_classes
    for row in audit.consistency_classes:
        assert forbidden.isdisjoint(row.fields), row.state_dict()
        assert row.return_address_fields == ()
    assert audit.consistency_retains_proposal_return_address is False


def test_register_boundary_does_not_copy_the_outbound_proposal_return_address() -> None:
    audit = audit_causal_lineage_information(_repository_root())
    assert "event_id" in audit.register_boundary_references
    assert "port_id" in audit.register_boundary_references
    assert "source_proposal_ids" not in audit.register_boundary_references
    assert "parent_proposal_ids" not in audit.register_boundary_references
    assert "local_path_ids" not in audit.register_boundary_references
    assert audit.register_boundary_consumes_proposal_return_address is False


def test_reentry_cannot_recover_historical_lineage_from_compressed_relation_state() -> None:
    audit = audit_causal_lineage_information(_repository_root())
    # Relation re-entry may use lineage attached to a new/current boundary event.
    # It cannot recover the historical proposal/path lineage that originally
    # produced the relation because that return address is absent from the
    # stored consistency state.
    assert audit.consistency_retains_proposal_return_address is False
    assert audit.relation_reentry_recovers_original_return_address is False


def test_first_information_loss_is_at_boundary_to_consistency_compression() -> None:
    audit = audit_causal_lineage_information(_repository_root())
    assert audit.lineage_information_loss_confirmed is True
    assert audit.first_loss_boundary == (
        "BoundaryEvent -> PendingBoundaryExposure/AnonymousLinkState"
    )


def test_information_audit_is_deterministic_and_observer_only() -> None:
    first = audit_causal_lineage_information(_repository_root())
    second = audit_causal_lineage_information(_repository_root())
    assert first == second
    lowered = str(first.state_dict()).lower()
    for forbidden in (
        "correct_action",
        "reward_value",
        "meaning_state",
        "functional_role",
        "expected_answer",
    ):
        assert forbidden not in lowered
