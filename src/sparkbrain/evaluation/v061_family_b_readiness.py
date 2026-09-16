from __future__ import annotations

from dataclasses import dataclass

from .v061_family_b_distributed_field_trace import (
    BELIEF_STATE_NULL_ID,
    FAMILY_B_GEN1_PROPOSAL,
    MECHANISM_RULE_SPEC_PATH,
    PROPOSAL_ID,
    PROTOCOL_BUNDLE_SOURCE_SHA,
    DistributedFieldTraceState,
)
from .v061_p3_p5_diagnostic_protocol import StateLocus
from .v061_premechanism_admission import assess_premechanism_admission

EXPECTED_PROPOSAL_SPECIFICATION_HASH = (
    "357f4a500164d31a3a851edc77c0870d3b59930c1766c1769671e9bdaf6ecf14"
)
EXPECTED_PROTOCOL_IDS = frozenset(
    {
        "v061-a01-bgen1-lineage-swap-v1",
        "v061-a01-bgen1-contradiction-v1",
        "v061-a01-bgen1-future-local-competition-v1",
        "v061-a01-bgen1-bounded-plurality-v1",
        "v061-a01-bgen1-field-only-functional-transfer-v1",
    }
)
EXPECTED_NULL_IDS = frozenset(
    {
        "v061-a01-bgen1-explicit-eligibility-return-address-null-v1",
        "v061-a01-bgen1-resource-matched-recurrent-causal-trace-null-v1",
        BELIEF_STATE_NULL_ID,
    }
)
EXPECTED_NEGATIVE_STOP_ID = "v061-a01-bgen1-stop-f-only-failure-or-null-reduction-v1"


@dataclass(frozen=True, slots=True)
class FamilyBGen1ReadinessAssessment:
    proposal_id: str
    protocol_bundle_source_sha: str
    specification_hash: str
    structural_admission_complete: bool
    field_only_carrier_fixed: bool
    protocol_ids_fixed: bool
    null_ids_fixed: bool
    negative_stop_fixed: bool
    carrier_has_only_anonymous_field_state: bool
    ready_for_evidence_analyst_review: bool
    execution_admitted: bool
    missing_requirements: tuple[str, ...]


def assess_family_b_gen1_readiness() -> FamilyBGen1ReadinessAssessment:
    """Verify construction/readiness bindings without admitting one-way execution."""

    proposal = FAMILY_B_GEN1_PROPOSAL
    admission = assess_premechanism_admission(proposal)
    protocol_ids = frozenset(
        {
            proposal.lineage_swap_protocol_id,
            proposal.contradiction_protocol_id,
            proposal.future_competition_protocol_id,
            proposal.bounded_ambiguity_protocol_id,
            proposal.p3_protocol_id,
        }
    )
    null_ids = frozenset(
        {
            proposal.explicit_null_id,
            proposal.recurrent_null_id,
            BELIEF_STATE_NULL_ID,
        }
    )
    field_only = proposal.expected_p3_carrier_loci == (StateLocus.FIELD_STATE,)
    carrier_fields = frozenset(DistributedFieldTraceState.__dataclass_fields__)
    anonymous_carrier = carrier_fields == frozenset({"eligibility", "credit", "decay"})
    exact_hash = proposal.bound_specification_hash == EXPECTED_PROPOSAL_SPECIFICATION_HASH
    source_fixed = proposal.protocol_bundle_source_sha == PROTOCOL_BUNDLE_SOURCE_SHA
    proposal_identity_fixed = proposal.proposal_id == PROPOSAL_ID
    spec_path_fixed = proposal.mechanism_rule_spec_path == MECHANISM_RULE_SPEC_PATH
    protocols_fixed = protocol_ids == EXPECTED_PROTOCOL_IDS
    nulls_fixed = null_ids == EXPECTED_NULL_IDS
    stop_fixed = proposal.negative_stop_observation_id == EXPECTED_NEGATIVE_STOP_ID

    requirements = (
        ("base-premechanism-admission", admission.admitted_for_implementation),
        ("proposal-identity-fixed", proposal_identity_fixed),
        ("protocol-bundle-source-fixed", source_fixed),
        ("proposal-specification-hash-fixed", exact_hash),
        ("mechanism-rule-spec-path-fixed", spec_path_fixed),
        ("field-only-carrier-fixed", field_only),
        ("protocol-ids-fixed", protocols_fixed),
        ("null-ids-fixed", nulls_fixed),
        ("negative-stop-fixed", stop_fixed),
        ("anonymous-field-carrier", anonymous_carrier),
    )
    missing = tuple(name for name, complete in requirements if not complete)
    ready = not missing
    return FamilyBGen1ReadinessAssessment(
        proposal_id=proposal.proposal_id,
        protocol_bundle_source_sha=proposal.protocol_bundle_source_sha,
        specification_hash=proposal.bound_specification_hash,
        structural_admission_complete=admission.admitted_for_implementation,
        field_only_carrier_fixed=field_only,
        protocol_ids_fixed=protocols_fixed,
        null_ids_fixed=nulls_fixed,
        negative_stop_fixed=stop_fixed,
        carrier_has_only_anonymous_field_state=anonymous_carrier,
        ready_for_evidence_analyst_review=ready,
        execution_admitted=False,
        missing_requirements=missing,
    )
