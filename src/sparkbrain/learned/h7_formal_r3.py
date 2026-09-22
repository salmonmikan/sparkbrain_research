from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import platform
import re
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

import torch

from .h7_formal_r1 import FormalIntegrityError

CONTRACT_ID: Final = "H7-FORMAL-R3-UNEXPOSED-EVALUATION-COMMITMENT-V1"
BASE_R2_CONTRACT_ID: Final = "H7-FORMAL-R2-INPUT-SPLIT-BINDING-V1"
BASE_R2_CONTRACT_BLOB: Final = "a4965eb49528e5b7e6da70f28e076de89d822f93"
BASE_R2_HEAD: Final = "80b88cd49fa5b9f5535feba27a75ebd3d4912406"
WORLDS: Final = (
    "switchworld",
    "contradiction_world",
    "goal_conflict_world",
    "multi_object_world",
)
STEPS_PER_EPISODE: Final = 24
EVALUATION_EPISODES: Final = 256
EVALUATION_EPISODES_PER_WORLD: Final = 64
EVALUATION_SPLIT: Final = "test"
COMMITMENT_SCHEME: Final = "SHA256-CANONICAL-OPAQUE-SEED-PAYLOAD-V1"
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

_FORBIDDEN_PUBLIC_SEED_KEYS = {
    "formal_evaluation_seed_range_inclusive",
    "evaluation_seed_range",
    "evaluation_seeds",
    "seed_list",
    "plaintext_seeds",
    "seed_payload",
    "seed_entropy",
}


def canonical_json_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _walk_keys(value: Any) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, Mapping):
        for key, child in value.items():
            keys.add(str(key))
            keys.update(_walk_keys(child))
    elif isinstance(value, list | tuple):
        for child in value:
            keys.update(_walk_keys(child))
    return keys


def assert_no_public_evaluation_seed_material(value: Mapping[str, Any]) -> None:
    leaked_keys = sorted(_walk_keys(value) & _FORBIDDEN_PUBLIC_SEED_KEYS)
    if leaked_keys:
        raise FormalIntegrityError(
            "R3 public contract contains forbidden evaluation-seed material: "
            + ", ".join(leaked_keys)
        )


@dataclass(frozen=True)
class OpaqueEvaluationCommitment:
    commitment_sha256: str
    ciphertext_sha256: str
    payload_size_bytes: int
    seed_count: int
    world_count: int
    episodes_per_world: int
    split: str
    steps_per_episode: int
    created_after_final_binding: bool
    plaintext_accessible_to_claim_capable: bool
    collision_audit_passed: bool
    commitment_scheme: str = COMMITMENT_SCHEME

    def assert_valid(self) -> None:
        if not _SHA256_RE.fullmatch(self.commitment_sha256):
            raise FormalIntegrityError("invalid opaque evaluation commitment digest")
        if not _SHA256_RE.fullmatch(self.ciphertext_sha256):
            raise FormalIntegrityError("invalid encrypted evaluation payload digest")
        if self.commitment_sha256 == self.ciphertext_sha256:
            raise FormalIntegrityError(
                "commitment and ciphertext digests must bind distinct objects"
            )
        if self.payload_size_bytes <= 0:
            raise FormalIntegrityError("opaque evaluation payload must be non-empty")
        if self.seed_count != EVALUATION_EPISODES:
            raise FormalIntegrityError("R3 evaluation episode count drift")
        if self.world_count != len(WORLDS):
            raise FormalIntegrityError("R3 evaluation world count drift")
        if self.episodes_per_world != EVALUATION_EPISODES_PER_WORLD:
            raise FormalIntegrityError("R3 per-world evaluation count drift")
        if self.split != EVALUATION_SPLIT:
            raise FormalIntegrityError("R3 evaluation split drift")
        if self.steps_per_episode != STEPS_PER_EPISODE:
            raise FormalIntegrityError("R3 recurrent-step count drift")
        if not self.created_after_final_binding:
            raise FormalIntegrityError(
                "evaluation commitment must follow final source/contract/runtime binding"
            )
        if self.plaintext_accessible_to_claim_capable:
            raise FormalIntegrityError(
                "claim-capable code may not access plaintext evaluation seeds"
            )
        if not self.collision_audit_passed:
            raise FormalIntegrityError("fresh evaluation seed collision audit is mandatory")
        if self.commitment_scheme != COMMITMENT_SCHEME:
            raise FormalIntegrityError("evaluation commitment scheme drift")

    def public_descriptor(self) -> dict[str, Any]:
        self.assert_valid()
        return {
            "commitment_sha256": self.commitment_sha256,
            "ciphertext_sha256": self.ciphertext_sha256,
            "payload_size_bytes": self.payload_size_bytes,
            "seed_count": self.seed_count,
            "world_count": self.world_count,
            "episodes_per_world": self.episodes_per_world,
            "split": self.split,
            "steps_per_episode": self.steps_per_episode,
            "created_after_final_binding": self.created_after_final_binding,
            "plaintext_accessible_to_claim_capable": self.plaintext_accessible_to_claim_capable,
            "collision_audit_passed": self.collision_audit_passed,
            "commitment_scheme": self.commitment_scheme,
        }


def _distribution_record_sha256(distribution_name: str) -> str:
    distribution = importlib.metadata.distribution(distribution_name)
    record_text = distribution.read_text("RECORD")
    if not record_text:
        raise FormalIntegrityError(f"{distribution_name} installation RECORD is unavailable")
    return hashlib.sha256(record_text.encode("utf-8")).hexdigest()


def exact_runtime_observation(pip_freeze_text: str) -> dict[str, Any]:
    freeze_lines = sorted(line.strip() for line in pip_freeze_text.splitlines() if line.strip())
    if not freeze_lines:
        raise FormalIntegrityError("pip-freeze inventory must not be empty")
    freeze_bytes = ("\n".join(freeze_lines) + "\n").encode("utf-8")
    observation = {
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "python_executable": sys.executable,
        "platform_system": platform.system(),
        "platform_release": platform.release(),
        "platform_machine": platform.machine(),
        "runner_image_os": os.environ.get("ImageOS", ""),
        "runner_image_version": os.environ.get("ImageVersion", ""),
        "runner_arch": os.environ.get("RUNNER_ARCH", ""),
        "torch_distribution_version": importlib.metadata.version("torch"),
        "torch_module_version": str(torch.__version__),
        "torch_git_version": str(getattr(torch.version, "git_version", "")),
        "torch_cuda_build_version": str(getattr(torch.version, "cuda", "")),
        "torch_distribution_record_sha256": _distribution_record_sha256("torch"),
        "pip_freeze_sha256": hashlib.sha256(freeze_bytes).hexdigest(),
        "device_contract": "cpu",
        "python_hash_seed": os.environ.get("PYTHONHASHSEED", ""),
        "omp_num_threads": os.environ.get("OMP_NUM_THREADS", ""),
        "mkl_num_threads": os.environ.get("MKL_NUM_THREADS", ""),
        "torch_deterministic_algorithms_enabled": torch.are_deterministic_algorithms_enabled(),
    }
    observation["runtime_observation_sha256"] = canonical_json_sha256(observation)
    return observation


def assert_r3_contract(r3: Mapping[str, Any]) -> None:
    if r3.get("schema_version") != 2 or r3.get("contract_id") != CONTRACT_ID:
        raise FormalIntegrityError("H7 FORMAL-R3 contract identity drift")
    base = r3.get("base_r2", {})
    expected_base = {
        "contract_id": BASE_R2_CONTRACT_ID,
        "contract_blob": BASE_R2_CONTRACT_BLOB,
        "head": BASE_R2_HEAD,
        "preserved_unchanged": True,
        "formal_evidence_surface_allowed": False,
    }
    if {key: base.get(key) for key in expected_base} != expected_base:
        raise FormalIntegrityError("H7 FORMAL-R3 base-R2 disposition drift")

    delta = r3.get("science_affecting_delta", {})
    expected_delta = {
        "field": "formal_evaluation_identity_exposure",
        "evaluation_episode_count": EVALUATION_EPISODES,
        "evaluation_episodes_per_world": EVALUATION_EPISODES_PER_WORLD,
        "formal_evaluation_split": EVALUATION_SPLIT,
        "steps_per_episode": STEPS_PER_EPISODE,
        "exact_seed_values_public_before_raw_preserve": False,
        "fresh_unexposed_seed_values_required": True,
        "all_other_r1_r2_scientific_fields_preserved": True,
    }
    if {key: delta.get(key) for key in expected_delta} != expected_delta:
        raise FormalIntegrityError("H7 FORMAL-R3 evaluation-exposure delta drift")

    commitment = r3.get("evaluation_commitment_interface", {})
    if commitment.get("scheme") != COMMITMENT_SCHEME:
        raise FormalIntegrityError("H7 FORMAL-R3 commitment scheme drift")
    if commitment.get("commitment_created_preidentity") is not False:
        raise FormalIntegrityError("R3 cycle 9 must not create an evaluation commitment")
    if commitment.get("plaintext_seed_access_before_raw_immutable_preserve") is not False:
        raise FormalIntegrityError("R3 plaintext evaluation seed access guard drift")
    if commitment.get("controller_owned_protected_payload") is not True:
        raise FormalIntegrityError("R3 evaluation payload must remain controller-owned")

    runtime = r3.get("runtime_binding", {})
    if runtime.get("raw_exact_values_required") is not True:
        raise FormalIntegrityError("R3 exact runtime values must not be normalized")
    if runtime.get("normalization_or_prefix_acceptance_forbidden") is not True:
        raise FormalIntegrityError("R3 runtime normalization guard drift")
    if runtime.get("binding_created_preidentity") is not False:
        raise FormalIntegrityError("R3 cycle 9 may diagnose runtime but not create one-way binding")

    guard = r3.get("preidentity_only", {})
    forbidden_true = (
        "formal_identity_created",
        "started_created",
        "evaluation_seed_revealed",
        "protected_evaluation_accessed",
        "result_bearing_workflow_dispatched",
        "official_scoring_performed",
        "scientific_preserve_or_evidence_ref_created",
    )
    if any(guard.get(key) is not False for key in forbidden_true):
        raise FormalIntegrityError("H7 FORMAL-R3 preidentity hard-stop drift")
    assert_no_public_evaluation_seed_material(r3)


def load_and_assert_r3_contract(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert_r3_contract(value)
    return value


def preidentity_sentinel(r3: Mapping[str, Any]) -> dict[str, Any]:
    assert_r3_contract(r3)
    return {
        "contract_id": CONTRACT_ID,
        "base_r2_contract_id": BASE_R2_CONTRACT_ID,
        "evaluation_episode_count": EVALUATION_EPISODES,
        "evaluation_episodes_per_world": EVALUATION_EPISODES_PER_WORLD,
        "formal_evaluation_split": EVALUATION_SPLIT,
        "steps_per_episode": STEPS_PER_EPISODE,
        "commitment_scheme": COMMITMENT_SCHEME,
        "evaluation_commitment_created": False,
        "evaluation_seed_revealed": False,
        "no_identity_created": True,
        "no_started_created": True,
        "no_protected_evaluation_access": True,
        "no_result_bearing_execution": True,
        "no_scoring_performed": True,
        "scientific_result": None,
    }
