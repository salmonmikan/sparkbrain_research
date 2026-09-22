from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

from .h7_formal_r1 import (
    COMPARATORS,
    EVALUATOR_ID,
    EXPECTED_EVALUATOR_SHA256,
    INTERVENTION_ID,
    FormalIntegrityError,
    assert_contract_design,
)

CONTRACT_ID: Final = "H7-FORMAL-R2-INPUT-SPLIT-BINDING-V1"
BASE_CONTRACT_ID: Final = "H7-FORMAL-R1-DYNAMIC-TOP1-CONFIRMATORY-CONTRACT-DESIGN-V1"
BASE_CONTRACT_BLOB: Final = "af26de3067263afcff0e727321fa173ea14de659"
R2_CONTRACT_BLOB: Final = "a4965eb49528e5b7e6da70f28e076de89d822f93"
R2_INPUT_SURFACE_SHA256: Final = "b1ec2861017642954fc7b510f0131d13500397aa5d991d4a3d30fe75fd3bafcc"
WORLDS: Final = (
    "switchworld",
    "contradiction_world",
    "goal_conflict_world",
    "multi_object_world",
)
STEPS_PER_EPISODE: Final = 24
FIT_SEEDS: Final = range(8_166_520, 8_166_712)
CALIBRATION_SEEDS: Final = range(8_350_164, 8_350_228)
EVALUATION_SEEDS: Final = range(8_846_030, 8_846_286)
FIT_SPLIT: Final = "train"
CALIBRATION_SPLIT: Final = "dev"
EVALUATION_SPLIT: Final = "test"
NATIVE_TRAINING_SEED: Final = 9_339_631
DENSE_TRAINING_SEED: Final = 9_428_927
ELIGIBILITY_HEAD_SEED: Final = 9_107_020


def canonical_json_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def expected_input_surface() -> dict[str, Any]:
    return {
        "worlds": list(WORLDS),
        "steps_per_episode": STEPS_PER_EPISODE,
        "fit_seed_range_inclusive": [FIT_SEEDS.start, FIT_SEEDS.stop - 1],
        "calibration_seed_range_inclusive": [
            CALIBRATION_SEEDS.start,
            CALIBRATION_SEEDS.stop - 1,
        ],
        "formal_evaluation_seed_range_inclusive": [
            EVALUATION_SEEDS.start,
            EVALUATION_SEEDS.stop - 1,
        ],
        "world_assignment": "seed-list index modulo 4 in listed world order",
        "fit_split": FIT_SPLIT,
        "calibration_split": CALIBRATION_SPLIT,
        "formal_evaluation_split": EVALUATION_SPLIT,
        "smoke_result_bearing_forbidden": True,
        "native_training_seed": NATIVE_TRAINING_SEED,
        "dense_training_seed": DENSE_TRAINING_SEED,
        "eligibility_head_seed": ELIGIBILITY_HEAD_SEED,
    }


def assert_r2_contract(r2: Mapping[str, Any], r1: Mapping[str, Any]) -> None:
    assert_contract_design(r1)
    if r2.get("schema_version") != 2 or r2.get("contract_id") != CONTRACT_ID:
        raise FormalIntegrityError("H7 FORMAL-R2 contract identity drift")
    base = r2.get("base_contract", {})
    if base.get("contract_id") != BASE_CONTRACT_ID or base.get("blob") != BASE_CONTRACT_BLOB:
        raise FormalIntegrityError("H7 FORMAL-R2 base contract binding drift")
    if base.get("preserved_unchanged") is not True:
        raise FormalIntegrityError("H7 FORMAL-R1 base must remain preserved unchanged")
    delta = r2.get("science_affecting_delta", {})
    expected_delta = {
        "field": "Episode.split",
        "fit_split": FIT_SPLIT,
        "calibration_split": CALIBRATION_SPLIT,
        "formal_evaluation_split": EVALUATION_SPLIT,
        "smoke_result_bearing_forbidden": True,
        "outcome_dependence": False,
        "all_other_r1_scientific_fields_preserved": True,
    }
    observed_delta = {key: delta.get(key) for key in expected_delta}
    if observed_delta != expected_delta:
        raise FormalIntegrityError("H7 FORMAL-R2 science-affecting delta drift")
    surface = r2.get("r2_input_surface", {})
    if surface != expected_input_surface():
        raise FormalIntegrityError("H7 FORMAL-R2 input surface drift")
    if canonical_json_sha256(surface) != R2_INPUT_SURFACE_SHA256:
        raise FormalIntegrityError("H7 FORMAL-R2 input surface digest drift")
    if r2.get("r2_input_surface_sha256") != R2_INPUT_SURFACE_SHA256:
        raise FormalIntegrityError("H7 FORMAL-R2 recorded input digest drift")
    guard = r2.get("preidentity_only", {})
    forbidden_true = (
        "formal_identity_created",
        "started_created",
        "protected_evaluation_accessed",
        "result_bearing_workflow_dispatched",
        "official_scoring_performed",
        "scientific_preserve_or_evidence_ref_created",
    )
    if any(guard.get(key) is not False for key in forbidden_true):
        raise FormalIntegrityError("H7 FORMAL-R2 preidentity hard-stop drift")
    if guard.get("result_bearing_smoke_forbidden") is not True:
        raise FormalIntegrityError("H7 FORMAL-R2 smoke guard drift")


def load_and_assert_r2_contract(
    r2_path: Path, r1_path: Path
) -> tuple[dict[str, Any], dict[str, Any]]:
    r2 = json.loads(r2_path.read_text(encoding="utf-8"))
    r1 = json.loads(r1_path.read_text(encoding="utf-8"))
    assert_r2_contract(r2, r1)
    return r2, r1


def episode_plan(role: str) -> tuple[tuple[str, int, str], ...]:
    roles = {
        "fit": (FIT_SEEDS, FIT_SPLIT),
        "calibration": (CALIBRATION_SEEDS, CALIBRATION_SPLIT),
        "evaluation": (EVALUATION_SEEDS, EVALUATION_SPLIT),
    }
    try:
        seeds, split = roles[role]
    except KeyError as exc:
        raise ValueError(f"unknown H7 FORMAL-R2 role: {role!r}") from exc
    return tuple((WORLDS[index % len(WORLDS)], seed, split) for index, seed in enumerate(seeds))


@dataclass(frozen=True)
class FutureIdentityBindingR2:
    identity_id: str
    final_source_sha: str
    contract_blob: str
    runner_blob: str
    scorer_blob: str
    preserver_blob: str
    package_manifest_sha256: str
    runtime_manifest_sha256: str
    input_surface_sha256: str
    evaluator_spec_sha256: str
    intervention_id: str
    comparators: tuple[str, ...]

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> FutureIdentityBindingR2:
        return cls(
            identity_id=str(value["identity_id"]),
            final_source_sha=str(value["final_source_sha"]),
            contract_blob=str(value["contract_blob"]),
            runner_blob=str(value["runner_blob"]),
            scorer_blob=str(value["scorer_blob"]),
            preserver_blob=str(value["preserver_blob"]),
            package_manifest_sha256=str(value["package_manifest_sha256"]),
            runtime_manifest_sha256=str(value["runtime_manifest_sha256"]),
            input_surface_sha256=str(value["input_surface_sha256"]),
            evaluator_spec_sha256=str(value["evaluator_spec_sha256"]),
            intervention_id=str(value["intervention_id"]),
            comparators=tuple(str(item) for item in value["comparators"]),
        )

    def assert_frozen_semantics(self) -> None:
        if len(self.final_source_sha) != 40:
            raise FormalIntegrityError("final source SHA must be an exact Git SHA")
        if self.contract_blob != R2_CONTRACT_BLOB:
            raise FormalIntegrityError("H7 FORMAL-R2 contract blob mismatch")
        if self.input_surface_sha256 != R2_INPUT_SURFACE_SHA256:
            raise FormalIntegrityError("H7 FORMAL-R2 input surface mismatch")
        if self.evaluator_spec_sha256 != EXPECTED_EVALUATOR_SHA256:
            raise FormalIntegrityError("H7 FORMAL evaluator mismatch")
        if self.intervention_id != INTERVENTION_ID:
            raise FormalIntegrityError("H7 FORMAL intervention mismatch")
        if self.comparators != COMPARATORS:
            raise FormalIntegrityError("H7 FORMAL ordinary comparator panel mismatch")
        required_digests = (
            self.runner_blob,
            self.scorer_blob,
            self.preserver_blob,
            self.package_manifest_sha256,
            self.runtime_manifest_sha256,
        )
        if any(len(value) < 40 for value in required_digests):
            raise FormalIntegrityError("incomplete H7 FORMAL-R2 implementation/runtime binding")

    def assert_same_final_sha(self, actual_sha: str) -> None:
        if actual_sha != self.final_source_sha:
            raise FormalIntegrityError(
                f"same-final-SHA gate failed: expected {self.final_source_sha}, got {actual_sha}"
            )


def preidentity_sentinel(r2: Mapping[str, Any], r1: Mapping[str, Any]) -> dict[str, Any]:
    assert_r2_contract(r2, r1)
    return {
        "contract_id": CONTRACT_ID,
        "base_contract_id": BASE_CONTRACT_ID,
        "evaluator_id": EVALUATOR_ID,
        "r2_input_surface_sha256": R2_INPUT_SURFACE_SHA256,
        "fit_split": FIT_SPLIT,
        "calibration_split": CALIBRATION_SPLIT,
        "formal_evaluation_split": EVALUATION_SPLIT,
        "result_bearing_smoke_forbidden": True,
        "no_identity_created": True,
        "no_started_created": True,
        "no_protected_evaluation_access": True,
        "no_result_bearing_execution": True,
        "no_scoring_performed": True,
        "scientific_result": None,
    }
