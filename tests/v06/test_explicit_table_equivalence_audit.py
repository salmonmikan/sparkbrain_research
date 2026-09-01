from __future__ import annotations

from sparkbrain.evaluation.v061_explicit_table_equivalence_audit import (
    MechanismDescriptor,
    StateLocality,
    UpdateGate,
    audit_table_equivalence,
    canonical_mechanism_descriptors,
)


def _assessments():
    return {
        row.mechanism_id: audit_table_equivalence(row)
        for row in canonical_mechanism_descriptors()
    }


def test_explicit_lineage_target_lookup_is_not_emergent_field_organization() -> None:
    result = _assessments()["explicit-lineage-target-lookup"]
    assert result.explicit_target_lookup_equivalent is True
    assert result.explicit_transition_memory is True
    assert result.classification == "explicit-target-lookup"
    assert result.accepted_as_emergent_field_organization is False


def test_assembly_and_typed_reward_structures_fail_privilege_boundary() -> None:
    assessments = _assessments()
    assembly = assessments["assembly-conditioned-target"]
    typed = assessments["typed-reward-head"]
    assert assembly.forbidden_privileged_structure is True
    assert typed.forbidden_privileged_structure is True
    assert assembly.classification == "forbidden-privileged-structure"
    assert typed.classification == "forbidden-privileged-structure"


def test_internally_self_confirming_credit_is_invalid() -> None:
    result = _assessments()["self-confirming-lineage-score"]
    assert result.self_confirmation_risk is True
    assert result.classification == "invalid-self-confirming-mechanism"
    assert result.accepted_as_emergent_field_organization is False


def test_bounded_causal_eligibility_survives_static_rejection_only() -> None:
    result = _assessments()["bounded-causal-eligibility"]
    assert result.transient_causal_eligibility_candidate is True
    assert result.explicit_target_lookup_equivalent is False
    assert result.forbidden_privileged_structure is False
    assert result.self_confirmation_risk is False
    assert result.requires_further_behavioral_equivalence_test is True
    assert result.accepted_as_emergent_field_organization is False
    assert result.classification == "transient-causal-eligibility-candidate"


def test_distributed_trace_is_candidate_not_proof_of_distributed_memory() -> None:
    result = _assessments()["distributed-consequence-trace"]
    assert result.distributed_field_candidate is True
    assert result.explicit_target_lookup_equivalent is False
    assert result.requires_further_behavioral_equivalence_test is True
    assert result.accepted_as_emergent_field_organization is False
    assert result.classification == "distributed-field-candidate"


def test_persistent_local_credit_is_reported_as_explicit_transition_memory() -> None:
    result = _assessments()["persistent-local-credit"]
    assert result.explicit_transition_memory is True
    assert result.explicit_target_lookup_equivalent is False
    assert result.classification == "explicit-transition-memory"
    assert result.requires_further_behavioral_equivalence_test is True
    assert result.accepted_as_emergent_field_organization is False


def test_direct_target_lookup_is_detected_even_without_target_in_the_key() -> None:
    descriptor = MechanismDescriptor(
        mechanism_id="path-to-next-target",
        state_locality=StateLocality.LOCAL_TRANSITION,
        persistent=True,
        expires_or_decays=False,
        key_dimensions=("path_id",),
        value_dimensions=("next_target",),
        update_gate=UpdateGate.EXTERNAL_CAUSAL,
        direct_query_returns_target=True,
    )
    result = audit_table_equivalence(descriptor)
    assert result.explicit_target_lookup_equivalent is True
    assert result.classification == "explicit-target-lookup"


def test_static_audit_never_declares_emergence() -> None:
    for descriptor in canonical_mechanism_descriptors():
        result = audit_table_equivalence(descriptor)
        assert result.accepted_as_emergent_field_organization is False


def test_canonical_descriptors_contain_no_evaluator_answer_field() -> None:
    lowered = str([row.state_dict() for row in canonical_mechanism_descriptors()]).lower()
    for forbidden in (
        "expected_answer",
        "outcome_label",
        "semantic_label",
        "correct_action_value",
    ):
        assert forbidden not in lowered
