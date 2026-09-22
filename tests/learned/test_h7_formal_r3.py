from __future__ import annotations

import json
from pathlib import Path

import pytest

from sparkbrain.learned.h7_formal_r1 import FormalIntegrityError
from sparkbrain.learned.h7_formal_r3 import (
    EVALUATION_EPISODES,
    EVALUATION_EPISODES_PER_WORLD,
    EVALUATION_SPLIT,
    STEPS_PER_EPISODE,
    OpaqueEvaluationCommitment,
    assert_no_public_evaluation_seed_material,
    load_and_assert_r3_contract,
    preidentity_sentinel,
)

CONTRACT = Path("artifacts/formal_h7_r3/contract_design.json")


def test_r3_contract_is_preidentity_and_contains_no_seed_payload_keys() -> None:
    contract = load_and_assert_r3_contract(CONTRACT)
    assert contract["preidentity_only"]["formal_identity_created"] is False
    assert contract["preidentity_only"]["evaluation_seed_revealed"] is False
    assert contract["preidentity_only"]["protected_evaluation_accessed"] is False
    assert contract["evaluation_commitment_interface"]["commitment_created_preidentity"] is False


def test_public_seed_material_is_rejected() -> None:
    with pytest.raises(FormalIntegrityError, match="forbidden evaluation-seed material"):
        assert_no_public_evaluation_seed_material({"evaluation_seeds": [1, 2, 3]})


def test_opaque_commitment_descriptor_contains_only_public_binding_metadata() -> None:
    descriptor = OpaqueEvaluationCommitment(
        commitment_sha256="1" * 64,
        ciphertext_sha256="2" * 64,
        payload_size_bytes=4096,
        seed_count=EVALUATION_EPISODES,
        world_count=4,
        episodes_per_world=EVALUATION_EPISODES_PER_WORLD,
        split=EVALUATION_SPLIT,
        steps_per_episode=STEPS_PER_EPISODE,
        created_after_final_binding=True,
        plaintext_accessible_to_claim_capable=False,
        collision_audit_passed=True,
    ).public_descriptor()
    serialized = json.dumps(descriptor, sort_keys=True)
    assert "evaluation_seeds" not in serialized
    assert "plaintext_seeds" not in serialized
    assert descriptor["seed_count"] == 256


def test_opaque_commitment_rejects_claim_capable_plaintext_access() -> None:
    descriptor = OpaqueEvaluationCommitment(
        commitment_sha256="1" * 64,
        ciphertext_sha256="2" * 64,
        payload_size_bytes=4096,
        seed_count=EVALUATION_EPISODES,
        world_count=4,
        episodes_per_world=EVALUATION_EPISODES_PER_WORLD,
        split=EVALUATION_SPLIT,
        steps_per_episode=STEPS_PER_EPISODE,
        created_after_final_binding=True,
        plaintext_accessible_to_claim_capable=True,
        collision_audit_passed=True,
    )
    with pytest.raises(FormalIntegrityError, match="may not access plaintext"):
        descriptor.assert_valid()


def test_preidentity_sentinel_cannot_claim_scientific_result() -> None:
    contract = load_and_assert_r3_contract(CONTRACT)
    sentinel = preidentity_sentinel(contract)
    assert sentinel["evaluation_commitment_created"] is False
    assert sentinel["evaluation_seed_revealed"] is False
    assert sentinel["scientific_result"] is None
