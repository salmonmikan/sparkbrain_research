from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .v06_confirmatory import (
    ConfirmatoryCondition,
    ConfirmatoryManifest,
    ConfirmatoryResultRecord,
    EvidenceDomain,
    assess_result_coverage,
)
from .v06_confirmatory_artifacts import (
    ExecutionIdentity,
    RawRunReceipt,
    deterministic_execution_id,
    verify_execution_bundle,
    verify_raw_run,
)
from .v06_confirmatory_execution_seal import ConfirmatoryFreezeRecord
from .v06_confirmatory_heldout_spec import heldout_world_parameters
from .v06_confirmatory_resource_accounting import (
    NormalizedConditionResourceRecord,
    ResourceDecisionUse,
    assess_normalized_resource_matrix,
)
from .v06_confirmatory_resources import (
    ConditionResourceRecord,
    PrivilegedInformation,
    assess_resource_matrix,
)

WorldHashResolver = Callable[[str, int], str]


@dataclass(frozen=True, slots=True)
class VerifiedRawEvidence:
    run_id: str
    raw_directory: str
    freeze_seal_hash: str
    source_code_sha: str
    manifest_hash: str
    world_generation_id: str
    receipt: RawRunReceipt
    results: tuple[ConfirmatoryResultRecord, ...]
    raw_resources: tuple[ConditionResourceRecord, ...]
    normalized_resources: tuple[NormalizedConditionResourceRecord, ...]
    execution_ids: tuple[str, ...]
    world_specification_hashes: tuple[tuple[str, str], ...]
    immutable_and_complete: bool

    def validate(self, manifest: ConfirmatoryManifest) -> None:
        if not self.run_id or not self.immutable_and_complete:
            raise ValueError("raw evidence is not complete and immutable")
        if self.source_code_sha != manifest.code_ref:
            raise ValueError("raw evidence source SHA does not match manifest")
        if self.manifest_hash != manifest.manifest_hash():
            raise ValueError("raw evidence manifest hash does not match")
        coverage = assess_result_coverage(manifest, self.results)
        raw_coverage = assess_resource_matrix(manifest, self.raw_resources)
        normalized_coverage = assess_normalized_resource_matrix(
            manifest,
            self.normalized_resources,
        )
        if not coverage.complete:
            raise ValueError("raw result matrix is incomplete")
        if not raw_coverage.complete:
            raise ValueError("raw resource matrix is incomplete")
        if not normalized_coverage.complete:
            raise ValueError("normalized resource matrix is incomplete")
        expected_executions = (
            len(manifest.world_families)
            * len(manifest.seeds)
            * len(manifest.conditions)
        )
        expected_results = expected_executions * len(manifest.evidence_domains)
        if self.receipt.execution_count != expected_executions:
            raise ValueError("raw receipt execution count does not match manifest")
        if self.receipt.result_record_count != expected_results:
            raise ValueError("raw receipt result count does not match manifest")
        if len(self.execution_ids) != expected_executions:
            raise ValueError("raw evidence execution identity count is incomplete")
        if len(set(self.execution_ids)) != len(self.execution_ids):
            raise ValueError("raw evidence contains duplicate execution identities")

    def state_dict(self) -> dict[str, Any]:
        return {
            "execution_count": len(self.execution_ids),
            "freeze_seal_hash": self.freeze_seal_hash,
            "immutable_and_complete": self.immutable_and_complete,
            "manifest_hash": self.manifest_hash,
            "normalized_resource_count": len(self.normalized_resources),
            "raw_directory": self.raw_directory,
            "raw_resource_count": len(self.raw_resources),
            "receipt": self.receipt.state_dict(),
            "result_record_count": len(self.results),
            "run_id": self.run_id,
            "source_code_sha": self.source_code_sha,
            "world_generation_id": self.world_generation_id,
            "world_specification_hashes": dict(
                self.world_specification_hashes
            ),
        }


def result_record_from_state(state: dict[str, Any]) -> ConfirmatoryResultRecord:
    metrics_state = state.get("metrics", {})
    if not isinstance(metrics_state, dict):
        raise ValueError("result metrics must be a JSON object")
    record = ConfirmatoryResultRecord(
        family_id=str(state["family_id"]),
        seed=int(state["seed"]),
        condition=ConfirmatoryCondition(str(state["condition"])),
        evidence_domain=EvidenceDomain(str(state["evidence_domain"])),
        passed=bool(state["passed"]),
        metrics=tuple(
            sorted((str(key), float(value)) for key, value in metrics_state.items())
        ),
    )
    expected_keys = {
        "condition",
        "evidence_domain",
        "family_id",
        "metrics",
        "passed",
        "seed",
    }
    if set(state) != expected_keys:
        raise ValueError("result record contains missing or unexpected fields")
    return record


def raw_resource_from_state(state: dict[str, Any]) -> ConditionResourceRecord:
    record = ConditionResourceRecord(
        family_id=str(state["family_id"]),
        seed=int(state["seed"]),
        condition=ConfirmatoryCondition(str(state["condition"])),
        observed_training_events=int(state["observed_training_events"]),
        generated_internal_events=int(state["generated_internal_events"]),
        persistent_state_entries=int(state["persistent_state_entries"]),
        intervention_count=int(state["intervention_count"]),
        parameter_count=int(state["parameter_count"]),
        wall_clock_ms=float(state["wall_clock_ms"]),
        normal_field_threshold_present=bool(
            state["normal_field_threshold_present"]
        ),
        normal_field_threshold_crossings=int(
            state["normal_field_threshold_crossings"]
        ),
        threshold_bypassed=bool(state["threshold_bypassed"]),
        explicit_assembly_entries=int(state["explicit_assembly_entries"]),
        typed_head_count=int(state["typed_head_count"]),
        scalar_reward_observations=int(state["scalar_reward_observations"]),
        privileged_information=tuple(
            PrivilegedInformation(str(value))
            for value in state["privileged_information"]
        ),
    )
    if set(record.state_dict()) != set(state):
        raise ValueError("raw resource contains missing or unexpected fields")
    record.validate()
    return record


def normalized_resource_from_state(
    state: dict[str, Any],
) -> NormalizedConditionResourceRecord:
    record = NormalizedConditionResourceRecord(
        family_id=str(state["family_id"]),
        seed=int(state["seed"]),
        condition=ConfirmatoryCondition(str(state["condition"])),
        accounting_version=str(state["accounting_version"]),
        decision_use=ResourceDecisionUse(str(state["decision_use"])),
        adapter_observed_training_event_proxy=int(
            state["adapter_observed_training_event_proxy"]
        ),
        adapter_generated_event_proxy=int(
            state["adapter_generated_event_proxy"]
        ),
        adapter_intervention_event_proxy=int(
            state["adapter_intervention_event_proxy"]
        ),
        adapter_mutable_state_scalar_proxy=int(
            state["adapter_mutable_state_scalar_proxy"]
        ),
        adapter_persistent_state_entry_proxy=int(
            state["adapter_persistent_state_entry_proxy"]
        ),
        adapter_logical_operation_proxy_units=int(
            state["adapter_logical_operation_proxy_units"]
        ),
        wall_clock_ns=int(state["wall_clock_ns"]),
        process_cpu_ns=int(state["process_cpu_ns"]),
        peak_traced_memory_bytes=int(state["peak_traced_memory_bytes"]),
        canonical_output_bytes=int(state["canonical_output_bytes"]),
        normal_field_threshold_present=bool(
            state["normal_field_threshold_present"]
        ),
        normal_field_threshold_crossings=int(
            state["normal_field_threshold_crossings"]
        ),
        threshold_bypassed=bool(state["threshold_bypassed"]),
        explicit_assembly_entries=int(state["explicit_assembly_entries"]),
        typed_head_count=int(state["typed_head_count"]),
        scalar_reward_observations=int(state["scalar_reward_observations"]),
        privileged_information_count=int(state["privileged_information_count"]),
    )
    if set(record.state_dict()) != set(state):
        raise ValueError("normalized resource contains missing or unexpected fields")
    record.validate()
    return record


def execution_identity_from_state(state: dict[str, Any]) -> ExecutionIdentity:
    identity = ExecutionIdentity(
        artifact_contract_version=str(state["artifact_contract_version"]),
        world_generation_id=str(state["world_generation_id"]),
        family_id=str(state["family_id"]),
        seed=int(state["seed"]),
        condition=ConfirmatoryCondition(str(state["condition"])),
        source_code_sha=str(state["source_code_sha"]),
        manifest_hash=str(state["manifest_hash"]),
        execution_id=str(state["execution_id"]),
    )
    if set(identity.state_dict()) != set(state):
        raise ValueError("execution identity contains missing or unexpected fields")
    identity.validate()
    return identity


def _candidate_world_hash(family_id: str, seed: int) -> str:
    return heldout_world_parameters(family_id, seed).specification_hash()


def load_verified_raw_evidence(
    raw_directory: Path,
    *,
    manifest: ConfirmatoryManifest,
    freeze_record: ConfirmatoryFreezeRecord,
    world_hash_resolver: WorldHashResolver | None = None,
) -> VerifiedRawEvidence:
    """Verify and load raw artifacts without calculating any aggregate score."""

    raw_directory = raw_directory.resolve()
    receipt = verify_raw_run(raw_directory)
    expected_run_id = f"confirmatory-{freeze_record.seal_hash()[:32]}"
    if receipt.run_id != expected_run_id or raw_directory.name != expected_run_id:
        raise RuntimeError("raw run identity does not match the execution seal")
    resolver = world_hash_resolver or _candidate_world_hash
    executions_directory = raw_directory / "executions"
    results: list[ConfirmatoryResultRecord] = []
    raw_resources: list[ConditionResourceRecord] = []
    normalized_resources: list[NormalizedConditionResourceRecord] = []
    execution_ids: list[str] = []
    world_hashes: dict[str, str] = {}

    for execution_directory in sorted(
        row for row in executions_directory.iterdir() if row.is_dir()
    ):
        verification = verify_execution_bundle(execution_directory)
        if not verification.valid:
            raise RuntimeError(
                f"invalid raw execution bundle: {execution_directory.name}"
            )
        metadata = json.loads(
            execution_directory.joinpath("metadata.json").read_text("utf-8")
        )
        identity = execution_identity_from_state(
            dict(metadata["execution_identity"])
        )
        if identity.execution_id != execution_directory.name:
            raise RuntimeError("execution directory and identity disagree")
        if identity.source_code_sha != freeze_record.source_code_sha:
            raise RuntimeError("execution source SHA differs from seal")
        if identity.manifest_hash != freeze_record.manifest_hash:
            raise RuntimeError("execution manifest hash differs from seal")
        if identity.world_generation_id != freeze_record.world_generation_id:
            raise RuntimeError("execution world generation differs from seal")
        expected_execution_id = deterministic_execution_id(
            world_generation_id=freeze_record.world_generation_id,
            family_id=identity.family_id,
            seed=identity.seed,
            condition=identity.condition,
            source_code_sha=freeze_record.source_code_sha,
            manifest_hash=freeze_record.manifest_hash,
        )
        if identity.execution_id != expected_execution_id:
            raise RuntimeError("execution ID does not match frozen inputs")
        expected_world_hash = resolver(identity.family_id, identity.seed)
        observed_world_hash = str(metadata["world_specification_hash"])
        if observed_world_hash != expected_world_hash:
            raise RuntimeError("execution world hash differs from frozen world")
        world_key = f"{identity.family_id}|{identity.seed}"
        existing_world_hash = world_hashes.setdefault(
            world_key,
            observed_world_hash,
        )
        if existing_world_hash != observed_world_hash:
            raise RuntimeError("conditions disagree on one world specification")

        result_rows = tuple(
            result_record_from_state(json.loads(line))
            for line in execution_directory.joinpath("results.jsonl")
            .read_text("utf-8")
            .splitlines()
            if line.strip()
        )
        if len(result_rows) != len(EvidenceDomain):
            raise RuntimeError("execution result-domain coverage is incomplete")
        if any(
            row.family_id != identity.family_id
            or row.seed != identity.seed
            or row.condition is not identity.condition
            for row in result_rows
        ):
            raise RuntimeError("execution result identity differs from metadata")
        raw_resource = raw_resource_from_state(
            json.loads(
                execution_directory.joinpath("raw_resource.json").read_text(
                    "utf-8"
                )
            )
        )
        normalized_resource = normalized_resource_from_state(
            json.loads(
                execution_directory.joinpath("normalized_resource.json").read_text(
                    "utf-8"
                )
            )
        )
        if raw_resource.key != identity.key:
            raise RuntimeError("raw resource identity differs from metadata")
        if normalized_resource.key != identity.key:
            raise RuntimeError("normalized resource identity differs from metadata")
        results.extend(result_rows)
        raw_resources.append(raw_resource)
        normalized_resources.append(normalized_resource)
        execution_ids.append(identity.execution_id)

    evidence = VerifiedRawEvidence(
        run_id=receipt.run_id,
        raw_directory=str(raw_directory),
        freeze_seal_hash=freeze_record.seal_hash(),
        source_code_sha=freeze_record.source_code_sha,
        manifest_hash=freeze_record.manifest_hash,
        world_generation_id=freeze_record.world_generation_id,
        receipt=receipt,
        results=tuple(results),
        raw_resources=tuple(raw_resources),
        normalized_resources=tuple(normalized_resources),
        execution_ids=tuple(execution_ids),
        world_specification_hashes=tuple(sorted(world_hashes.items())),
        immutable_and_complete=receipt.immutable_permissions_applied,
    )
    evidence.validate(manifest)
    return evidence
