from __future__ import annotations

import json
from pathlib import Path

import pytest
from test_capability_staging_development_fixture import (
    DevelopmentCapabilityWorld,
)
from test_capability_staging_development_fixture import (
    _run as run_development_condition,
)

from sparkbrain.evaluation.v06_confirmatory import ConfirmatoryCondition, EvidenceDomain
from sparkbrain.evaluation.v06_confirmatory_artifacts import (
    ARTIFACT_CONTRACT_VERSION,
    AtomicRawRunWriter,
    ExecutionIdentity,
    artifact_contract_hash,
    deterministic_execution_id,
    verify_execution_bundle,
    verify_raw_run,
)
from sparkbrain.evaluation.v06_confirmatory_resource_accounting import (
    measure_condition_execution,
)

_SOURCE_SHA = "a" * 40
_MANIFEST_HASH = "b" * 64
_GENERATION = "development-only-artifact-test"


def _measured():
    world = DevelopmentCapabilityWorld()
    return world, measure_condition_execution(
        lambda: run_development_condition(world, ConfirmatoryCondition.PRIMARY)
    )


def _identity(world: DevelopmentCapabilityWorld) -> ExecutionIdentity:
    execution_id = deterministic_execution_id(
        world_generation_id=_GENERATION,
        family_id=world.family_id,
        seed=world.seed,
        condition=ConfirmatoryCondition.PRIMARY,
        source_code_sha=_SOURCE_SHA,
        manifest_hash=_MANIFEST_HASH,
    )
    return ExecutionIdentity(
        artifact_contract_version=ARTIFACT_CONTRACT_VERSION,
        world_generation_id=_GENERATION,
        family_id=world.family_id,
        seed=world.seed,
        condition=ConfirmatoryCondition.PRIMARY,
        source_code_sha=_SOURCE_SHA,
        manifest_hash=_MANIFEST_HASH,
        execution_id=execution_id,
    )


def test_execution_identity_is_deterministic_and_binds_frozen_inputs() -> None:
    world = DevelopmentCapabilityWorld()
    first = _identity(world)
    second = _identity(world)
    assert first == second
    first.validate()
    assert len(first.execution_id) == len("execution-") + 40
    assert first.execution_id != deterministic_execution_id(
        world_generation_id=_GENERATION,
        family_id=world.family_id,
        seed=world.seed,
        condition=ConfirmatoryCondition.PRIMARY,
        source_code_sha="c" * 40,
        manifest_hash=_MANIFEST_HASH,
    )
    assert len(artifact_contract_hash()) == 64


def test_one_execution_and_raw_run_commit_atomically(tmp_path: Path) -> None:
    world, measured = _measured()
    writer = AtomicRawRunWriter(
        tmp_path,
        run_id="development-raw-run",
        expected_execution_count=1,
        expected_result_record_count=len(EvidenceDomain),
    )
    bundle = writer.add(_identity(world), measured)
    verification = verify_execution_bundle(bundle)
    assert verification.valid is True
    assert verification.result_record_count == len(EvidenceDomain)
    receipt = writer.finalize()
    assert receipt.execution_count == 1
    assert receipt.result_record_count == len(EvidenceDomain)
    assert receipt.raw_resource_count == 1
    assert receipt.normalized_resource_count == 1
    assert receipt.immutable_permissions_applied is True
    verified = verify_raw_run(Path(receipt.final_directory))
    assert verified.raw_manifest_hash == receipt.raw_manifest_hash
    assert verified.run_checksums_hash == receipt.run_checksums_hash


def test_duplicate_execution_id_is_rejected_without_overwrite(tmp_path: Path) -> None:
    world, measured = _measured()
    writer = AtomicRawRunWriter(
        tmp_path,
        run_id="duplicate-test",
        expected_execution_count=1,
        expected_result_record_count=len(EvidenceDomain),
    )
    identity = _identity(world)
    writer.add(identity, measured)
    with pytest.raises(FileExistsError, match="duplicate execution"):
        writer.add(identity, measured)


def test_partial_transaction_is_not_counted_as_an_execution(tmp_path: Path) -> None:
    world, measured = _measured()
    writer = AtomicRawRunWriter(
        tmp_path,
        run_id="partial-transaction-test",
        expected_execution_count=1,
        expected_result_record_count=len(EvidenceDomain),
    )
    writer.add(_identity(world), measured)
    partial = writer.run_staging_directory / ".transactions" / "crashed.tmp"
    partial.mkdir(parents=True)
    partial.joinpath("results.jsonl").write_text("partial\n", encoding="utf-8")
    receipt = writer.finalize()
    assert receipt.execution_count == 1
    assert not Path(receipt.final_directory).joinpath(".transactions", "crashed.tmp").is_file()


def test_missing_resource_file_blocks_run_finalization(tmp_path: Path) -> None:
    world, measured = _measured()
    writer = AtomicRawRunWriter(
        tmp_path,
        run_id="missing-resource-test",
        expected_execution_count=1,
        expected_result_record_count=len(EvidenceDomain),
    )
    bundle = writer.add(_identity(world), measured)
    bundle.joinpath("raw_resource.json").unlink()
    assert verify_execution_bundle(bundle).valid is False
    with pytest.raises(RuntimeError, match="invalid execution bundle"):
        writer.finalize()


def test_checksum_tampering_is_detected_before_raw_lock(tmp_path: Path) -> None:
    world, measured = _measured()
    writer = AtomicRawRunWriter(
        tmp_path,
        run_id="tamper-test",
        expected_execution_count=1,
        expected_result_record_count=len(EvidenceDomain),
    )
    bundle = writer.add(_identity(world), measured)
    resource_path = bundle / "normalized_resource.json"
    value = json.loads(resource_path.read_text("utf-8"))
    value["adapter_generated_event_proxy"] += 1
    resource_path.write_text(json.dumps(value), encoding="utf-8")
    verification = verify_execution_bundle(bundle)
    assert verification.checksum_match is False
    assert verification.valid is False
    with pytest.raises(RuntimeError, match="invalid execution bundle"):
        writer.finalize()


def test_artifact_layer_does_not_import_or_call_scoring() -> None:
    source = Path(
        "src/sparkbrain/evaluation/v06_confirmatory_artifacts.py"
    ).read_text(encoding="utf-8")
    assert "v06_confirmatory_scoring" not in source
    assert "score_confirmatory_results" not in source
    assert "score_strict_confirmatory_results" not in source
