from __future__ import annotations

from dataclasses import replace

from sparkbrain.evaluation.v061_family_b_distributed_field_trace import (
    BELIEF_STATE_NULL_ID,
    FAMILY_B_GEN1_PROPOSAL,
    PROPOSAL_ID,
    PROTOCOL_BUNDLE_SOURCE_SHA,
)
from sparkbrain.evaluation.v061_family_b_readiness import (
    EXPECTED_NEGATIVE_STOP_ID,
    EXPECTED_NULL_IDS,
    EXPECTED_PROPOSAL_SPECIFICATION_HASH,
    EXPECTED_PROTOCOL_IDS,
    assess_family_b_gen1_readiness,
)
from sparkbrain.evaluation.v061_p3_p5_diagnostic_protocol import StateLocus
from sparkbrain.evaluation.v061_premechanism_admission import assess_premechanism_admission


def test_family_b_gen1_proposal_binding_is_exact_and_structurally_complete() -> None:
    proposal = FAMILY_B_GEN1_PROPOSAL
    admission = assess_premechanism_admission(proposal)

    assert proposal.proposal_id == PROPOSAL_ID
    assert proposal.protocol_bundle_source_sha == PROTOCOL_BUNDLE_SOURCE_SHA
    assert proposal.expected_p3_carrier_loci == (StateLocus.FIELD_STATE,)
    assert proposal.specification_hash() == EXPECTED_PROPOSAL_SPECIFICATION_HASH
    assert proposal.bound_specification_hash == EXPECTED_PROPOSAL_SPECIFICATION_HASH
    assert admission.admitted_for_implementation
    assert not admission.missing_requirements


def test_family_b_gen1_readiness_is_for_analyst_review_not_execution() -> None:
    readiness = assess_family_b_gen1_readiness()

    assert readiness.ready_for_evidence_analyst_review
    assert not readiness.execution_admitted
    assert not readiness.missing_requirements


def test_all_protocol_null_and_stop_ids_are_prospectively_fixed_and_distinct() -> None:
    proposal = FAMILY_B_GEN1_PROPOSAL
    protocol_ids = {
        proposal.lineage_swap_protocol_id,
        proposal.contradiction_protocol_id,
        proposal.future_competition_protocol_id,
        proposal.bounded_ambiguity_protocol_id,
        proposal.p3_protocol_id,
    }
    null_ids = {
        proposal.explicit_null_id,
        proposal.recurrent_null_id,
        BELIEF_STATE_NULL_ID,
    }

    assert protocol_ids == EXPECTED_PROTOCOL_IDS
    assert null_ids == EXPECTED_NULL_IDS
    assert proposal.negative_stop_observation_id == EXPECTED_NEGATIVE_STOP_ID
    assert protocol_ids.isdisjoint(null_ids)
    assert proposal.negative_stop_observation_id not in protocol_ids | null_ids


def test_hash_binding_fails_closed_if_protocol_identity_changes() -> None:
    modified = replace(
        FAMILY_B_GEN1_PROPOSAL,
        contradiction_protocol_id="post-outcome-retune-is-not-admissible",
    )
    admission = assess_premechanism_admission(modified)

    assert not admission.specification_binding_valid
    assert not admission.admitted_for_implementation
    assert admission.classification == "proposal-specification-binding-invalid"


def test_forbidden_privilege_fails_structural_admission() -> None:
    modified = replace(
        FAMILY_B_GEN1_PROPOSAL,
        uses_forbidden_privilege=True,
    ).bind()
    admission = assess_premechanism_admission(modified)

    assert not admission.admitted_for_implementation
    assert "no-forbidden-privilege" in admission.missing_requirements
