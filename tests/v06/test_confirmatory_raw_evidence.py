from __future__ import annotations

import json
import stat
from pathlib import Path

import pytest
from test_capability_staging_development_fixture import (
    DevelopmentCapabilityWorld,
)
from test_capability_staging_development_fixture import (
    _run as run_development_condition,
)

from sparkbrain.evaluation.v06_confirmatory import (
    ConditionRegistration,
    ConfirmatoryCondition,
    ConfirmatoryManifest,
    ConfirmatoryPhase,
    ConfirmatoryThresholds,
    EvidenceDomain,
    PerturbationSeedSpec,
    WorldFamilySpec,
)
from sparkbrain.evaluation.v06_confirmatory_artifacts import (
    ARTIFACT_CONTRACT_VERSION,
    AtomicRawRunWriter,
    ExecutionIdentity,
    deterministic_execution_id,
)
from sparkbrain.evaluation.v06_confirmatory_execution_seal import (
    ConfirmatoryFreezeRecord,
)
from sparkbrain.evaluation.v06_confirmatory_raw_evidence import (
    execution_identity_from_state,
    load_verified_raw_evidence,
    normalized_resource_from_state,
    raw_resource_from_state,
    result_record_from_state,
)
from sparkbrain.evaluation.v06_confirmatory_resource_accounting import (
    measure_condition_execution,
)

_SOURCE_SHA = "a" * 40
_WORLD_GENERATION = "development-only-raw-loader"


def _manifest(world: DevelopmentCapabilityWorld) -> ConfirmatoryManifest:
    return ConfirmatoryManifest(
        protocol_version="development-raw-loader-test",
        phase=ConfirmatoryPhase.QUALIFICATION,
        code_ref=_SOURCE_SHA,
        world_families=(
            WorldFamilySpec(
                family_id=world.family_id,
                held_out=False,
                perturbation_axes=("development-only",),
                description="Development-only raw loader fixture.",
            ),
        ),
        seeds=(
            PerturbationSeedSpec(
                seed=world.seed,
                structural_token=world.structural_token,
            ),
        ),
        conditions=(
            ConditionRegistration(
                condition=ConfirmatoryCondition.PRIMARY,
                adapter_path="development.primary",
                adapter_ready=True,
                isolated_from_primary=True,
                engineering_evidence_available=True,
                notes="Development-only raw loader adapter.",
            ),
        ),
        evidence_domains=tuple(EvidenceDomain),
        thresholds=ConfirmatoryThresholds(),
        exclusions=("Development-only raw loader test.",),
    )


def _freeze_record(manifest: ConfirmatoryManifest) -> ConfirmatoryFreezeRecord:
    return ConfirmatoryFreezeRecord(
        record_version="development-raw-loader-freeze",
        seal_storage_mode="development-only",
        source_code_sha=_SOURCE_SHA,
        manifest_hash=manifest.manifest_hash(),
        world_generation_id=_WORLD_GENERATION,
        world_grid_hash="b" * 64,
        training_schedule_grid_hash="c" * 64,
        thresholds_hash="d" * 64,
        exclusions_hash="e" * 64,
        result_schema_hash="f" * 64,
        raw_resource_schema_hash="1" * 64,
        normalized_resource_schema_hash="2" * 64,
        resource_policy_hash="3" * 64,
        adapter_registration_hash="4" * 64,
        adapter_source_inventory_hash="5" * 64,
        privilege_inventory_hash="6" * 64,
        threshold_mode_hash="7" * 64,
        artifact_contract_hash="8" * 64,
        analysis_contract_hash="9" * 64,
        execution_command_hash="a" * 64,
        scoring_command_hash="b" * 64,
        artifact_path_hash="c" * 64,
        environment_lock_hash="d" * 64,
        rng_contract_hash="e" * 64,
        approval_id="APPROVED:development-test:0123456789abcdef",
    )


def _build_raw_run(tmp_path: Path):
    world = DevelopmentCapabilityWorld()
    manifest = _manifest(world)
    freeze = _freeze_record(manifest)
    measured = measure_condition_execution(
        lambda: run_development_condition(world, ConfirmatoryCondition.PRIMARY)
    )
    run_id = f"confirmatory-{freeze.seal_hash()[:32]}"
    writer = AtomicRawRunWriter(
        tmp_path,
        run_id=run_id,
        expected_execution_count=1,
        expected_result_record_count=len(EvidenceDomain),
    )
    execution_id = deterministic_execution_id(
        world_generation_id=_WORLD_GENERATION,
        family_id=world.family_id,
        seed=world.seed,
        condition=ConfirmatoryCondition.PRIMARY,
        source_code_sha=_SOURCE_SHA,
        manifest_hash=manifest.manifest_hash(),
    )
    writer.add(
        ExecutionIdentity(
            artifact_contract_version=ARTIFACT_CONTRACT_VERSION,
            world_generation_id=_WORLD_GENERATION,
            family_id=world.family_id,
            seed=world.seed,
            condition=ConfirmatoryCondition.PRIMARY,
            source_code_sha=_SOURCE_SHA,
            manifest_hash=manifest.manifest_hash(),
            execution_id=execution_id,
        ),
        measured,
    )
    receipt = writer.finalize()
    return world, manifest, freeze, Path(receipt.final_directory), measured


def test_raw_loader_verifies_results_resources_identity_and_world_hash(
    tmp_path: Path,
) -> None:
    world, manifest, freeze, raw_directory, measured = _build_raw_run(tmp_path)
    evidence = load_verified_raw_evidence(
        raw_directory,
        manifest=manifest,
        freeze_record=freeze,
        world_hash_resolver=lambda family_id, seed: (
            world.specification_hash()
            if (family_id, seed) == (world.family_id, world.seed)
            else "unexpected"
        ),
    )
    assert evidence.immutable_and_complete is True
    assert len(evidence.execution_ids) == 1
    assert len(evidence.results) == len(EvidenceDomain)
    assert evidence.raw_resources == (measured.execution.resource,)
    assert evidence.normalized_resources == (measured.normalized_resource,)
    assert evidence.receipt.execution_count == 1
    assert evidence.receipt.result_record_count == len(EvidenceDomain)


def test_raw_record_parsers_round_trip_exactly(tmp_path: Path) -> None:
    _, _, _, raw_directory, measured = _build_raw_run(tmp_path)
    execution_directory = next(raw_directory.joinpath("executions").iterdir())
    metadata = json.loads(
        execution_directory.joinpath("metadata.json").read_text("utf-8")
    )
    identity = execution_identity_from_state(metadata["execution_identity"])
    assert identity.execution_id == execution_directory.name
    raw = raw_resource_from_state(
        json.loads(execution_directory.joinpath("raw_resource.json").read_text("utf-8"))
    )
    normalized = normalized_resource_from_state(
        json.loads(
            execution_directory.joinpath("normalized_resource.json").read_text("utf-8")
        )
    )
    first_result = result_record_from_state(
        json.loads(
            execution_directory.joinpath("results.jsonl")
            .read_text("utf-8")
            .splitlines()[0]
        )
    )
    assert raw == measured.execution.resource
    assert normalized == measured.normalized_resource
    assert first_result == measured.execution.records[0]


def test_raw_checksum_tampering_is_rejected_before_analysis(tmp_path: Path) -> None:
    world, manifest, freeze, raw_directory, _ = _build_raw_run(tmp_path)
    execution_directory = next(raw_directory.joinpath("executions").iterdir())
    results = execution_directory / "results.jsonl"
    raw_directory.chmod(0o755)
    execution_directory.chmod(0o755)
    results.chmod(stat.S_IRUSR | stat.S_IWUSR)
    results.write_text("{}\n", encoding="utf-8")
    with pytest.raises(RuntimeError):
        load_verified_raw_evidence(
            raw_directory,
            manifest=manifest,
            freeze_record=freeze,
            world_hash_resolver=lambda family_id, seed: (
                world.specification_hash()
            ),
        )


def test_raw_loader_module_contains_no_scoring_dependency() -> None:
    source = Path(
        "src/sparkbrain/evaluation/v06_confirmatory_raw_evidence.py"
    ).read_text(encoding="utf-8")
    assert "v06_confirmatory_scoring" not in source
    assert "score_strict_confirmatory_results" not in source
