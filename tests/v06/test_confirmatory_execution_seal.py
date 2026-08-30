from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from sparkbrain.evaluation.v06_confirmatory import PerturbationSeedSpec
from sparkbrain.evaluation.v06_confirmatory_analysis_contract import SCORING_COMMAND
from sparkbrain.evaluation.v06_confirmatory_candidate_manifest import (
    build_candidate_manifest,
)
from sparkbrain.evaluation.v06_confirmatory_environment import (
    ENVIRONMENT_LOCK_VERSION,
    RNG_CONTRACT,
    ConfirmatoryEnvironmentLock,
)
from sparkbrain.evaluation.v06_confirmatory_execution_seal import (
    ARTIFACT_PATH_TEMPLATES,
    EXECUTION_COMMAND,
    SEAL_STORAGE_MODE,
    build_freeze_record,
    freeze_record_from_state,
    require_execution_seal,
    validate_execution_seal,
)
from sparkbrain.evaluation.v06_confirmatory_heldout_spec import (
    HELDOUT_SEEDS,
    QUARANTINED_HELDOUT_SEEDS,
    WORLD_GENERATION_ID,
)
from sparkbrain.v06.foundation import digest

_FAKE_SOURCE_SHA = "a" * 40
_APPROVAL_ID = "APPROVED:unit-test:0123456789abcdef"


def _repository_root() -> Path:
    return Path(__file__).parents[2]


def _environment_lock() -> ConfirmatoryEnvironmentLock:
    distributions = ("sparkbrain-research==0.3.2.dev0",)
    return ConfirmatoryEnvironmentLock(
        version=ENVIRONMENT_LOCK_VERSION,
        python_implementation="CPython",
        python_version="3.11.9",
        python_executable_sha256="b" * 64,
        platform_system="Linux",
        platform_release="6.8.0-freeze-test",
        platform_machine="x86_64",
        os_release=(("ID", "ubuntu"), ("VERSION_ID", "24.04")),
        runner_os="Linux",
        runner_arch="X64",
        runner_image_os="ubuntu24",
        runner_image_version="20260825.1.0",
        python_hash_seed="0",
        timezone="UTC",
        locale_name="C.UTF-8",
        installed_distributions=distributions,
        installed_distributions_hash=digest(list(distributions)),
        rng_contract_hash=RNG_CONTRACT.contract_hash(),
    )


def _manifest():
    return build_candidate_manifest(source_code_sha=_FAKE_SOURCE_SHA)


def _record():
    return build_freeze_record(
        _manifest(),
        source_code_sha=_FAKE_SOURCE_SHA,
        repository_root=_repository_root(),
        environment_lock=_environment_lock(),
        approval_id=_APPROVAL_ID,
    )


def _validate(record=None, manifest=None):
    return validate_execution_seal(
        manifest or _manifest(),
        record or _record(),
        repository_root=_repository_root(),
        environment_lock=_environment_lock(),
    )


def test_complete_freeze_record_binds_every_protocol_component() -> None:
    report = _validate()
    assert report.manifest_ready is True
    assert report.source_code_sha_matches is True
    assert report.manifest_hash_matches is True
    assert report.world_generation_matches is True
    assert report.world_grid_matches is True
    assert report.seeds_fresh_and_exact is True
    assert report.training_schedule_matches is True
    assert report.thresholds_match is True
    assert report.exclusions_match is True
    assert report.result_schema_matches is True
    assert report.raw_resource_schema_matches is True
    assert report.normalized_resource_schema_matches is True
    assert report.resource_policy_matches is True
    assert report.adapter_registration_matches is True
    assert report.adapter_source_inventory_matches is True
    assert report.privilege_inventory_matches is True
    assert report.threshold_mode_matches is True
    assert report.artifact_contract_matches is True
    assert report.analysis_contract_matches is True
    assert report.execution_command_matches is True
    assert report.scoring_command_matches is True
    assert report.artifact_paths_match is True
    assert report.environment_lock_matches is True
    assert report.rng_contract_matches is True
    assert report.storage_mode_matches is True
    assert report.approval_present is True
    assert report.execution_allowed is True
    assert len(report.seal_hash) == 64


def test_seal_solves_self_reference_by_pointing_to_detached_source_sha() -> None:
    record = _record()
    assert record.source_code_sha == _FAKE_SOURCE_SHA
    assert record.seal_storage_mode == SEAL_STORAGE_MODE
    assert "detached-source-checkout" in record.seal_storage_mode
    assert "seal_commit_sha" not in record.state_dict()
    assert _manifest().code_ref == record.source_code_sha


def test_freeze_record_round_trips_exactly() -> None:
    record = _record()
    assert freeze_record_from_state(record.state_dict()) == record
    with pytest.raises(ValueError, match="missing or unexpected"):
        freeze_record_from_state({**record.state_dict(), "unexpected": True})


def test_approval_must_have_structured_independent_format() -> None:
    for invalid in (
        "",
        "approved",
        "APPROVED",
        "APPROVED:reviewer",
        "APPROVED:reviewer:not-a-hash",
        "PENDING:reviewer:0123456789abcdef",
    ):
        report = _validate(replace(_record(), approval_id=invalid))
        assert report.approval_present is False
        assert report.execution_allowed is False


def test_any_frozen_hash_change_fails_closed() -> None:
    record = _record()
    mutations = (
        replace(record, manifest_hash="0" * 64),
        replace(record, world_grid_hash="0" * 64),
        replace(record, training_schedule_grid_hash="0" * 64),
        replace(record, thresholds_hash="0" * 64),
        replace(record, exclusions_hash="0" * 64),
        replace(record, result_schema_hash="0" * 64),
        replace(record, raw_resource_schema_hash="0" * 64),
        replace(record, normalized_resource_schema_hash="0" * 64),
        replace(record, resource_policy_hash="0" * 64),
        replace(record, adapter_registration_hash="0" * 64),
        replace(record, adapter_source_inventory_hash="0" * 64),
        replace(record, privilege_inventory_hash="0" * 64),
        replace(record, threshold_mode_hash="0" * 64),
        replace(record, artifact_contract_hash="0" * 64),
        replace(record, analysis_contract_hash="0" * 64),
        replace(record, execution_command_hash="0" * 64),
        replace(record, scoring_command_hash="0" * 64),
        replace(record, artifact_path_hash="0" * 64),
        replace(record, environment_lock_hash="0" * 64),
        replace(record, rng_contract_hash="0" * 64),
        replace(record, world_generation_id="wrong-generation"),
        replace(record, source_code_sha="c" * 40),
        replace(record, approval_id=""),
    )
    for changed in mutations:
        report = _validate(changed)
        assert report.execution_allowed is False
        with pytest.raises(RuntimeError, match="remains prohibited"):
            require_execution_seal(
                _manifest(),
                changed,
                repository_root=_repository_root(),
                environment_lock=_environment_lock(),
            )


def test_environment_change_invalidates_the_seal() -> None:
    changed_environment = replace(
        _environment_lock(),
        python_version="3.11.10",
    )
    report = validate_execution_seal(
        _manifest(),
        _record(),
        repository_root=_repository_root(),
        environment_lock=changed_environment,
    )
    assert report.environment_lock_matches is False
    assert report.execution_allowed is False


def test_quarantined_seed_set_can_never_validate_as_fresh() -> None:
    manifest = _manifest()
    contaminated = replace(
        manifest,
        seeds=tuple(
            PerturbationSeedSpec(
                seed=seed,
                structural_token=f"quarantined:{seed}",
            )
            for seed in QUARANTINED_HELDOUT_SEEDS
        ),
    )
    record = build_freeze_record(
        contaminated,
        source_code_sha=_FAKE_SOURCE_SHA,
        repository_root=_repository_root(),
        environment_lock=_environment_lock(),
        approval_id=_APPROVAL_ID,
    )
    report = validate_execution_seal(
        contaminated,
        record,
        repository_root=_repository_root(),
        environment_lock=_environment_lock(),
    )
    assert report.seeds_fresh_and_exact is False
    assert report.execution_allowed is False


def test_freeze_contract_names_commands_and_raw_then_analysis_paths() -> None:
    assert HELDOUT_SEEDS == tuple(range(1000, 1010))
    assert WORLD_GENERATION_ID == "v06-confirmatory-candidate-002"
    assert EXECUTION_COMMAND.startswith("python -m ")
    assert "--freeze-record" in EXECUTION_COMMAND
    assert "--environment-lock" in EXECUTION_COMMAND
    assert SCORING_COMMAND.startswith("python -m ")
    assert "--raw-directory" in SCORING_COMMAND
    assert len(set(ARTIFACT_PATH_TEMPLATES)) == len(ARTIFACT_PATH_TEMPLATES)
    assert any(path.startswith("raw/") for path in ARTIFACT_PATH_TEMPLATES)
    assert any(path.startswith("analysis/") for path in ARTIFACT_PATH_TEMPLATES)
