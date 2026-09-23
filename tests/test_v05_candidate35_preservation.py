from __future__ import annotations

import json

import pytest

from sparkbrain.v05.candidate35_architecture import (
    Candidate35ResponseNotAuthorized,
    build_candidate35_brain,
)
from sparkbrain.v05.candidate35_preservation import (
    ANALYST_COMMIT,
    ANALYST_GENERATION,
    CLAIM_CEILING,
    DEVELOPMENT_PHASE,
    PREFORMAL_ELIGIBLE,
    PREFORMAL_READINESS,
    PRESERVE_MODE,
    QUEUE_STATE,
    RESPONSE_PRODUCER,
    SOURCE_BLOB_SHA1,
    SOURCE_HEAD,
    SYSTEM_PRIORITY_EXCEPTION,
    TERMINAL_STATE,
    candidate35_preservation_contract,
    candidate35_preservation_nonresult_preflight,
    execute_candidate35_response_preserve_before_read,
)


def test_preservation_contract_preserves_r99_funnel_and_stop_fields() -> None:
    contract = candidate35_preservation_contract()

    assert contract["claim_ceiling"] == CLAIM_CEILING == "SYSTEM"
    assert contract["development_phase"] == DEVELOPMENT_PHASE == "OPEN_DEVELOPMENT"
    assert contract["preformal_eligible"] is PREFORMAL_ELIGIBLE is False
    assert contract["preformal_readiness"] == PREFORMAL_READINESS == "NOT_APPLICABLE"
    assert contract["terminal_state"] == TERMINAL_STATE == "NONTERMINAL"
    assert contract["queue_state"] == QUEUE_STATE
    assert contract["system_priority_exception"] == SYSTEM_PRIORITY_EXCEPTION
    assert contract["analyst_generation"] == ANALYST_GENERATION
    assert contract["analyst_commit"] == ANALYST_COMMIT
    assert contract["source_head"] == SOURCE_HEAD
    assert contract["source_blob_sha1"] == SOURCE_BLOB_SHA1
    assert contract["response_producer"] == RESPONSE_PRODUCER
    assert contract["preserve_mode"] == PRESERVE_MODE == "EXCLUSIVE_CREATE_BEFORE_RETURN"
    assert contract["raw_before_read"] is True
    assert contract["no_clobber"] is True
    assert contract["candidate_response_execution_allowed"] is False
    assert contract["preformal_execution_allowed"] is False
    assert contract["formal_action_allowed"] is False


def test_nonresult_preservation_preflight_is_deterministic_and_non_result() -> None:
    left = candidate35_preservation_nonresult_preflight()
    right = candidate35_preservation_nonresult_preflight()

    assert left == right
    assert left.source_blob_sha1 == SOURCE_BLOB_SHA1
    assert left.response_producer == RESPONSE_PRODUCER
    assert left.candidate_response_executed is False
    assert left.raw_artifact_created is False
    assert len(left.contract_sha256) == 64
    assert len(left.binding_sha256) == 64
    assert len(left.provenance_sha256) == 64

    provenance = json.loads(left.provenance_json)
    assert provenance["source_head"] == SOURCE_HEAD
    assert provenance["source_blob_sha1"] == SOURCE_BLOB_SHA1
    assert provenance["raw_before_read"] is True
    assert provenance["no_clobber"] is True
    assert provenance["candidate_response_execution_allowed"] is False


def test_response_wrapper_fails_closed_before_output_or_source_mutation(tmp_path) -> None:
    brain = build_candidate35_brain()
    source_hash = brain.state_hash()
    output = tmp_path / "candidate35-raw.json"

    with pytest.raises(Candidate35ResponseNotAuthorized):
        execute_candidate35_response_preserve_before_read(
            brain,
            anchor_time_ms=brain.current_time_ms,
            arm="SHAM_STATE",
            output_path=output,
            response_execution_allowed=False,
        )

    assert not output.exists()
    assert brain.state_hash() == source_hash
    assert brain.current_time_ms == 0.0
    assert brain.base.field.state_dict()["queue"] == []
