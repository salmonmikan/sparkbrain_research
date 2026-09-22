from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from sparkbrain.learned.h7_formal_r1 import ENDPOINTS, INTERVENTION_ID, FormalIntegrityError
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
from sparkbrain.learned.h7_formal_r3_integrity import (
    PreserveProof,
    assert_paths_available_no_clobber,
    assert_target_sidecar_independence,
    prediction_raw_bytes,
    recompute_correctness_after_preserve,
    validate_prediction_raw_row,
    validate_prior_surface_inventory,
    validate_runtime_binding,
)

CONTRACT = Path("artifacts/formal_h7_r3/contract_design.json")
RUNTIME_BINDING = Path("artifacts/formal_h7_r3/runtime_binding.json")
PRIOR_INVENTORY = Path("artifacts/formal_h7_r3/prior_surface_inventory.json")


def _synthetic_surfaces() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    target_id = hashlib.sha256(b"r3-synthetic-target").hexdigest()
    raw: list[dict[str, object]] = []
    for endpoint in ENDPOINTS:
        row: dict[str, object] = {
            "opaque_target_id": target_id,
            "endpoint": endpoint,
            "intervention_id": INTERVENTION_ID,
            "baseline_prediction": "yes",
            "cut_prediction": "no",
        }
        if endpoint != "FINITE_STATE_ROUTE_HISTORY_V2":
            row["baseline_probabilities"] = [0.8, 0.2]
            row["cut_probabilities"] = [0.3, 0.7]
        raw.append(row)
    targets = [
        {
            "opaque_target_id": target_id,
            "world": "switchworld",
            "episode_seed": 123456789,
            "step_index": 0,
            "truth": "yes",
        }
    ]
    return raw, targets


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


def test_prediction_raw_positive_allowlist_rejects_target_derived_correctness() -> None:
    raw, _ = _synthetic_surfaces()
    invalid = dict(raw[0])
    invalid["baseline_correct"] = 1
    with pytest.raises(FormalIntegrityError, match="prediction raw schema violation"):
        validate_prediction_raw_row(invalid)


def test_prediction_raw_positive_allowlist_rejects_protected_identity_fields() -> None:
    raw, _ = _synthetic_surfaces()
    invalid = dict(raw[0])
    invalid["episode_seed"] = 123
    with pytest.raises(FormalIntegrityError, match="prediction raw schema violation"):
        validate_prediction_raw_row(invalid)


def test_target_sidecar_is_separate_and_complete_for_all_endpoints() -> None:
    raw, targets = _synthetic_surfaces()
    assert_target_sidecar_independence(raw, targets)
    missing = raw[:-1]
    with pytest.raises(FormalIntegrityError, match="coverage mismatch"):
        assert_target_sidecar_independence(missing, targets)


def test_correctness_is_recomputed_only_after_preserve_proof() -> None:
    raw, targets = _synthetic_surfaces()
    payload = prediction_raw_bytes(raw)
    digest = hashlib.sha256(payload).hexdigest()
    rows = recompute_correctness_after_preserve(
        raw_rows=raw,
        target_rows=targets,
        preserve_proof=PreserveProof(
            raw_sha256=digest,
            preserved_raw_sha256=digest,
            preserve_manifest_sha256="a" * 64,
            preserve_before_target_access=True,
        ),
    )
    assert len(rows) == len(ENDPOINTS)
    assert all(row["baseline_correct"] == 1 for row in rows)
    assert all(row["cut_correct"] == 0 for row in rows)
    assert all("truth" not in row for row in rows)


def test_correctness_recompute_fails_if_target_access_preceded_preserve() -> None:
    raw, targets = _synthetic_surfaces()
    payload = prediction_raw_bytes(raw)
    digest = hashlib.sha256(payload).hexdigest()
    with pytest.raises(FormalIntegrityError, match="target access occurred before raw preserve"):
        recompute_correctness_after_preserve(
            raw_rows=raw,
            target_rows=targets,
            preserve_proof=PreserveProof(
                raw_sha256=digest,
                preserved_raw_sha256=digest,
                preserve_manifest_sha256="a" * 64,
                preserve_before_target_access=False,
            ),
        )


def test_no_clobber_preflight_rejects_existing_path(tmp_path: Path) -> None:
    occupied = tmp_path / "STARTED.json"
    occupied.write_text("occupied", encoding="utf-8")
    with pytest.raises(FormalIntegrityError, match="no-clobber path collision"):
        assert_paths_available_no_clobber([occupied])


def test_literal_runtime_binding_is_exact_not_normalized() -> None:
    binding = json.loads(RUNTIME_BINDING.read_text(encoding="utf-8"))
    observation = dict(binding["runtime_observation"])
    validate_runtime_binding(binding, observation)
    observation["runner_image_version"] = "different"
    with pytest.raises(FormalIntegrityError, match="literal exact runtime binding mismatch"):
        validate_runtime_binding(binding, observation)


def test_prior_surface_inventory_is_complete_and_contains_no_future_seed_values() -> None:
    inventory = json.loads(PRIOR_INVENTORY.read_text(encoding="utf-8"))
    validate_prior_surface_inventory(inventory)
    assert inventory["future_r3_evaluation_seed_values_recorded"] is False
