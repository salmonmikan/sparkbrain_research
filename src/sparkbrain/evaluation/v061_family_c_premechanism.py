from __future__ import annotations

import hashlib
import json

from .v061_p3_p5_diagnostic_protocol import StateLocus
from .v061_premechanism_admission import MechanismFamily, PreMechanismProposal

PROPOSAL_ID = "a01-family-c-joint-return-local-field-gen1-v1"
ANALYST_HANDOFF_SHA = "d295a61d37903f1b7c34fd793c6aa6a6e25c5cb6"
MECHANISM_RULE_SPEC_PATH = "docs/V061_A01_FAMILY_C_JOINT_RETURN_LOCAL_FIELD_GEN1.md"
NULL_LADDER_SPEC_PATH = "docs/V061_A01_FAMILY_C_NULL_LADDER_GEN1.md"

BELIEF_STATE_NULL_ID = "v061-a01-cgen1-explicit-latent-cause-belief-null-v1"
SEPARABLE_JOINT_NULL_ID = "v061-a01-cgen1-separable-address-plus-field-null-v1"

WIDTH = 4
DECAY = 0.5
MAX_PENDING_PLURALITY = 2

FAMILY_C_GEN1_PROPOSAL = PreMechanismProposal(
    proposal_id=PROPOSAL_ID,
    mechanism_family=MechanismFamily.JOINT_RETURN_AND_LOCAL_FIELD_UPDATE,
    lineage_swap_test_declared=True,
    external_confirmation_only_positive=True,
    contradiction_correction_declared=True,
    future_local_competition_effect_declared=True,
    bounded_ambiguity_declared=True,
    uses_forbidden_privilege=False,
    expected_p3_carrier_loci=(StateLocus.FIELD_STATE,),
    explicit_null_declared=True,
    recurrent_null_declared=True,
    negative_stop_observation_declared=True,
    lineage_swap_protocol_id="v061-a01-cgen1-lineage-swap-v1",
    contradiction_protocol_id="v061-a01-cgen1-contradiction-v1",
    future_competition_protocol_id="v061-a01-cgen1-future-local-competition-v1",
    bounded_ambiguity_protocol_id="v061-a01-cgen1-bounded-plurality-v1",
    p3_protocol_id="v061-a01-cgen1-address-at-update-field-carrier-cross-v1",
    explicit_null_id="v061-a01-cgen1-explicit-return-address-eligibility-null-v1",
    recurrent_null_id="v061-a01-cgen1-resource-matched-recurrent-causal-trace-null-v1",
    negative_stop_observation_id=(
        "v061-a01-cgen1-stop-no-selective-plurality-or-null-reduction-v1"
    ),
    protocol_bundle_source_sha=ANALYST_HANDOFF_SHA,
    mechanism_rule_spec_path=MECHANISM_RULE_SPEC_PATH,
    null_ladder_spec_path=NULL_LADDER_SPEC_PATH,
).bind()

EXPECTED_PROPOSAL_SHA256 = "4b574b7053efb50b59a8d7536c94d02a7a25bdfc5b1d7f88575c7b6fc3e614ac"

_EXTENSION_PAYLOAD = {
    "proposal_sha256": EXPECTED_PROPOSAL_SHA256,
    "belief_state_null_id": BELIEF_STATE_NULL_ID,
    "separable_joint_null_id": SEPARABLE_JOINT_NULL_ID,
    "selector_source": "actual-pending-causal-provenance",
    "selector_lifetime": "through-external-pairing-only",
    "post_update_carrier": "field-state",
    "p3_rule": "address-selects-update-field-alone-carries-later-effect",
    "candidate_update_rule": (
        "credit_prime[i]=decay*credit[i]+"
        "(1-decay)*sign*indicator(i==actual_pending_slot)"
    ),
    "later_competition_rule": "dot(credit,activity)",
    "width": WIDTH,
    "decay": DECAY,
    "max_pending_plurality": MAX_PENDING_PLURALITY,
    "resource_rule": (
        "all-nulls-receive-same-event-stream-and-address-capability-"
        "with-no-more-state-or-lookup-privilege"
    ),
}

FAMILY_C_GEN1_EXTENSION_SHA256 = hashlib.sha256(
    json.dumps(
        _EXTENSION_PAYLOAD,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
).hexdigest()

EXPECTED_EXTENSION_SHA256 = "690a62df641d0577e3f7d760354763a6f0ec69e33eedfdacb37e92e7c654dbbc"

if FAMILY_C_GEN1_PROPOSAL.bound_specification_hash != EXPECTED_PROPOSAL_SHA256:
    raise RuntimeError("Family-C Gen1 proposal binding drift")
if FAMILY_C_GEN1_EXTENSION_SHA256 != EXPECTED_EXTENSION_SHA256:
    raise RuntimeError("Family-C Gen1 extension binding drift")
