from __future__ import annotations

import copy

from sparkbrain.equivalence_certificate import (
    Verdict,
    canonical_sha256,
    verify_equivalence_certificate,
)


def _certificate() -> dict[str, object]:
    bindings = {
        "source": {"id": "source-commit", "sha256": "1" * 64},
        "protocol": {"id": "protocol-v1", "sha256": "2" * 64},
        "package": {"id": "package-v1", "sha256": "3" * 64},
        "input": {"id": "fixture-set-v1", "sha256": "4" * 64},
        "evaluator": {"id": "evaluator-v1", "sha256": "5" * 64},
    }
    privilege = {"observations": ["local"], "held_out_access": False}
    resources = {"cpu_count": 2, "wall_clock_seconds": 30}
    common = {
        "bindings_sha256": canonical_sha256(bindings),
        "privilege_envelope_sha256": canonical_sha256(privilege),
        "resource_envelope_sha256": canonical_sha256(resources),
        "ordered_trajectory_sha256": "6" * 64,
        "checkpoint_sequence_sha256": "7" * 64,
    }
    return {
        "schema_version": 1,
        "certificate_type": "equivalence-certificate-v0.1",
        "bindings": bindings,
        "privilege_envelope": privilege,
        "resource_envelope": resources,
        "members": [
            {
                **common,
                "producer_id": "producer-a",
                "process_id": "process-a",
                "challenge_nonce": "a" * 32,
                "os_pid": 1001,
            },
            {
                **common,
                "producer_id": "producer-b",
                "process_id": "process-b",
                "challenge_nonce": "b" * 32,
                "os_pid": 1002,
            },
        ],
    }


def test_exact_match_is_valid_equivalent() -> None:
    result = verify_equivalence_certificate(_certificate())
    assert result.verdict == Verdict.VALID_EQUIVALENT
    assert result.reason == "EXACT_SEMANTIC_DIGEST_MATCH"


def test_semantic_digest_difference_is_valid_not_equivalent() -> None:
    value = _certificate()
    value["members"][1]["checkpoint_sequence_sha256"] = "8" * 64
    result = verify_equivalence_certificate(value)
    assert result.verdict == Verdict.VALID_NOT_EQUIVALENT


def test_binding_attestation_mismatch_fails_closed() -> None:
    value = _certificate()
    value["members"][0]["bindings_sha256"] = "f" * 64
    result = verify_equivalence_certificate(value)
    assert result.verdict == Verdict.INVALID_CONTRACT
    assert result.reason == "BINDINGS_ATTESTATION_MISMATCH:0"


def test_privilege_or_resource_drift_fails_closed() -> None:
    value = _certificate()
    value["privilege_envelope"]["held_out_access"] = True
    result = verify_equivalence_certificate(value)
    assert result.verdict == Verdict.INVALID_CONTRACT
    assert result.reason == "PRIVILEGE_ATTESTATION_MISMATCH:0"


def test_non_independent_producers_fail_closed() -> None:
    value = _certificate()
    value["members"][1]["challenge_nonce"] = value["members"][0]["challenge_nonce"]
    result = verify_equivalence_certificate(value)
    assert result.verdict == Verdict.INVALID_CONTRACT
    assert result.reason == "PRODUCERS_NOT_INDEPENDENT:challenge_nonce"


def test_extra_fields_fail_closed() -> None:
    value = _certificate()
    value["scientific_claim"] = "should never be accepted here"
    result = verify_equivalence_certificate(value)
    assert result.verdict == Verdict.INVALID_CONTRACT
    assert result.reason == "TOP_LEVEL_SCHEMA_MISMATCH"


def test_nan_in_envelope_fails_closed() -> None:
    value = _certificate()
    value["resource_envelope"] = copy.deepcopy(value["resource_envelope"])
    value["resource_envelope"]["weight"] = float("nan")
    result = verify_equivalence_certificate(value)
    assert result.verdict == Verdict.INVALID_CONTRACT
    assert result.reason == "NON_CANONICAL_CONTRACT_VALUE"
