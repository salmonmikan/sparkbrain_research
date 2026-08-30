from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import pytest

from sparkbrain.evaluation.v06_confirmatory_environment import (
    ENVIRONMENT_LOCK_VERSION,
    RNG_CONTRACT,
    ConfirmatoryEnvironmentLock,
)
from sparkbrain.evaluation.v06_confirmatory_execution_seal import (
    validate_execution_seal,
)
from sparkbrain.evaluation.v06_confirmatory_freeze_candidate import (
    build_freeze_candidate,
    freeze_candidate_from_state,
    independently_verify_freeze_candidate,
    issue_execution_seal,
    read_freeze_candidate,
    write_approved_control_package,
    write_freeze_candidate,
)
from sparkbrain.evaluation.v06_confirmatory_launch_gate import GitWorkspaceState
from sparkbrain.v06.foundation import digest

_SOURCE_SHA = "a" * 40


def _repository_root() -> Path:
    return Path(__file__).parents[2]


def _workspace(*, clean: bool = True, source_sha: str = _SOURCE_SHA) -> GitWorkspaceState:
    return GitWorkspaceState(
        head_sha=source_sha,
        status_porcelain="" if clean else " M changed.py\n",
        symbolic_ref="v06-freeze-candidate-test",
        detached_head=False,
    )


def _environment() -> ConfirmatoryEnvironmentLock:
    distributions = (
        "pip==24.0",
        "sparkbrain-research==0.3.2.dev0",
    )
    return ConfirmatoryEnvironmentLock(
        version=ENVIRONMENT_LOCK_VERSION,
        python_implementation="CPython",
        python_version="3.11.9",
        python_executable_sha256="b" * 64,
        platform_system="Linux",
        platform_release="6.8.0-freeze-candidate-test",
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


def _candidate():
    return build_freeze_candidate(
        repository_root=_repository_root(),
        source_code_sha=_SOURCE_SHA,
        environment_lock=_environment(),
        builder_id="builder-1",
        workspace=_workspace(),
    )


def test_freeze_candidate_is_unsigned_and_non_executable() -> None:
    candidate = _candidate()
    candidate.validate_shape()
    assert candidate.source_code_sha == _SOURCE_SHA
    assert candidate.builder_id == "builder-1"
    assert candidate.unsigned_freeze_record_state["approval_id"] == ""
    assert len(candidate.candidate_hash()) == 64
    assert candidate.manifest_state["code_ref"] == _SOURCE_SHA


def test_freeze_candidate_requires_a_clean_matching_source_checkout() -> None:
    with pytest.raises(RuntimeError, match="not clean"):
        build_freeze_candidate(
            repository_root=_repository_root(),
            source_code_sha=_SOURCE_SHA,
            environment_lock=_environment(),
            builder_id="builder-1",
            workspace=_workspace(clean=False),
        )
    with pytest.raises(RuntimeError, match="does not match"):
        build_freeze_candidate(
            repository_root=_repository_root(),
            source_code_sha=_SOURCE_SHA,
            environment_lock=_environment(),
            builder_id="builder-1",
            workspace=_workspace(source_sha="c" * 40),
        )


def test_same_builder_cannot_independently_approve() -> None:
    verification = independently_verify_freeze_candidate(
        _candidate(),
        repository_root=_repository_root(),
        reviewer_id="builder-1",
        workspace=_workspace(),
        observed_environment=_environment(),
    )
    assert verification.reviewer_is_independent is False
    assert verification.ready_for_approval is False
    with pytest.raises(RuntimeError, match="independent verification"):
        issue_execution_seal(
            _candidate(),
            repository_root=_repository_root(),
            reviewer_id="builder-1",
            workspace=_workspace(),
            observed_environment=_environment(),
        )


def test_independent_verification_rebuilds_every_frozen_component() -> None:
    verification = independently_verify_freeze_candidate(
        _candidate(),
        repository_root=_repository_root(),
        reviewer_id="reviewer-2",
        workspace=_workspace(),
        observed_environment=_environment(),
    )
    assert verification.reviewer_is_independent is True
    assert verification.source_workspace_clean is True
    assert verification.source_workspace_sha_matches is True
    assert verification.source_manifest_state_matches is True
    assert verification.source_manifest_hash_matches is True
    assert verification.environment_lock_state_matches is True
    assert verification.environment_lock_hash_matches is True
    assert verification.unsigned_freeze_record_matches is True
    assert verification.unsigned_seal_hash_matches is True
    assert verification.all_unsigned_seal_components_match is True
    assert verification.unsigned_approval_absent is True
    assert verification.ready_for_approval is True
    assert len(verification.verification_hash()) == 64


def test_independent_reviewer_issues_executable_external_seal() -> None:
    package = issue_execution_seal(
        _candidate(),
        repository_root=_repository_root(),
        reviewer_id="reviewer-2",
        workspace=_workspace(),
        observed_environment=_environment(),
    )
    package.validate()
    assert package.approved_freeze_record.approval_id.startswith(
        "APPROVED:reviewer-2:"
    )
    assert len(package.package_hash()) == 64
    from sparkbrain.evaluation.v06_confirmatory_candidate_manifest import (
        build_candidate_manifest,
    )

    manifest = build_candidate_manifest(source_code_sha=_SOURCE_SHA)
    report = validate_execution_seal(
        manifest,
        package.approved_freeze_record,
        repository_root=_repository_root(),
        environment_lock=_environment(),
    )
    assert report.approval_present is True
    assert report.execution_allowed is True


def test_candidate_round_trip_and_external_control_package_are_atomic(
    tmp_path: Path,
) -> None:
    candidate = _candidate()
    candidate_path = tmp_path / "freeze_candidate.json"
    write_freeze_candidate(candidate_path, candidate)
    serialized_state = json.loads(candidate_path.read_text("utf-8"))
    loaded = read_freeze_candidate(candidate_path)
    assert loaded.state_dict() == serialized_state
    assert loaded.candidate_hash() == candidate.candidate_hash()
    assert freeze_candidate_from_state(serialized_state) == loaded
    with pytest.raises(FileExistsError):
        write_freeze_candidate(candidate_path, candidate)

    package = issue_execution_seal(
        candidate,
        repository_root=_repository_root(),
        reviewer_id="reviewer-2",
        workspace=_workspace(),
        observed_environment=_environment(),
    )
    control = tmp_path / "control"
    write_approved_control_package(control, package)
    assert {
        "environment_lock.json",
        "freeze_record.json",
        "freeze_verification.json",
    } == {row.name for row in control.iterdir()}
    with pytest.raises(FileExistsError):
        write_approved_control_package(control, package)


def test_tampered_candidate_fails_independent_verification() -> None:
    candidate = _candidate()
    tampered = replace(candidate, manifest_hash="0" * 64)
    verification = independently_verify_freeze_candidate(
        tampered,
        repository_root=_repository_root(),
        reviewer_id="reviewer-2",
        workspace=_workspace(),
        observed_environment=_environment(),
    )
    assert verification.source_manifest_hash_matches is False
    assert verification.ready_for_approval is False
