from __future__ import annotations

import json
import os
import platform
import sys
from dataclasses import replace
from pathlib import Path

import pytest

from sparkbrain.evaluation.v06_confirmatory import ConfirmatoryPhase
from sparkbrain.evaluation.v06_confirmatory_current_manifest import (
    build_current_confirmatory_manifest,
)
from sparkbrain.evaluation.v06_confirmatory_environment_lock_v2 import (
    capture_environment_lock_v2,
)
from sparkbrain.evaluation.v06_confirmatory_execution_seal import (
    frozen_manifest_for_test,
)
from sparkbrain.evaluation.v06_confirmatory_external_control_package_v2 import (
    write_external_control_package_v2,
)
from sparkbrain.evaluation.v06_confirmatory_external_freeze import (
    ExternalArtifactLayout,
)
from sparkbrain.evaluation.v06_confirmatory_external_verification_v2 import (
    IndependentFreezeVerificationV2,
)
from sparkbrain.evaluation.v06_confirmatory_freeze_bundle_v2 import (
    build_external_freeze_bundle_v2,
    verify_independent_rebuild,
)

_FAKE_SHA = "a" * 40
_EXPECTED_FILES = {
    "candidate_execution_counter.json",
    "environment_lock.json",
    "environment_lock.sha256",
    "freeze_bundle.json",
    "freeze_bundle.sha256",
    "independent_verification.json",
    "independent_verification.sha256",
}


def _environment_or_skip():
    if platform.python_implementation() != "CPython" or sys.version_info[:2] != (3, 11):
        pytest.skip("external control package is frozen to CPython 3.11")
    if os.environ.get("PYTHONHASHSEED") != "0" or os.environ.get("TZ") != "UTC":
        pytest.skip("focused workflow supplies deterministic environment variables")
    return capture_environment_lock_v2()


def _approved_bundle(tmp_path: Path):
    environment = _environment_or_skip()
    source_root = Path(__file__).parents[2].resolve()
    layout = ExternalArtifactLayout(
        control_root=str((tmp_path / "control").resolve()),
        raw_root=str((tmp_path / "raw").resolve()),
        analysis_root=str((tmp_path / "analysis").resolve()),
    )
    manifest = frozen_manifest_for_test(
        build_current_confirmatory_manifest(ConfirmatoryPhase.CONFIRMATORY),
        code_ref=_FAKE_SHA,
    )
    first = build_external_freeze_bundle_v2(
        manifest,
        source_root=source_root,
        source_git_sha=_FAKE_SHA,
        artifact_layout=layout,
        environment_lock=environment,
        builder="builder-a",
    )
    second = build_external_freeze_bundle_v2(
        manifest,
        source_root=source_root,
        source_git_sha=_FAKE_SHA,
        artifact_layout=layout,
        environment_lock=environment,
        builder="builder-a",
    )
    approved = verify_independent_rebuild(
        first,
        second,
        reviewer="reviewer-b",
    )
    verification = IndependentFreezeVerificationV2(
        source_git_sha_matches=True,
        unsigned_bundle_matches=True,
        environment_matches=True,
        builder_and_reviewer_distinct=True,
        manifest_execution_ready=True,
        candidate_execution_counter_zero=True,
        approval_issued=True,
        reviewer="reviewer-b",
        expected_unsigned_hash=approved.unsigned_hash(),
        observed_unsigned_hash=approved.unsigned_hash(),
        verification_passed=True,
    )
    return environment, approved, verification


def test_exact_seven_file_control_package_is_written_exclusively(tmp_path: Path) -> None:
    environment, bundle, verification = _approved_bundle(tmp_path)
    package = write_external_control_package_v2(
        bundle,
        environment,
        verification,
    )
    control_root = Path(bundle.artifact_layout["control_root"])
    assert {row.name for row in control_root.iterdir()} == _EXPECTED_FILES
    assert set(package.file_hashes) == _EXPECTED_FILES
    assert package.candidate_execution_counter == 0
    assert len(package.package_hash()) == 64
    assert all(path.stat().st_mode & 0o222 == 0 for path in control_root.iterdir())

    counter = json.loads(
        (control_root / "candidate_execution_counter.json").read_text(
            encoding="utf-8"
        )
    )
    assert counter == {"bundle_hash": bundle.bundle_hash(), "count": 0}
    frozen = json.loads(
        (control_root / "freeze_bundle.json").read_text(encoding="utf-8")
    )
    assert frozen["source_git_sha"] == bundle.source_git_sha
    assert frozen["reviewer"] == "reviewer-b"
    assert frozen["approval"] == bundle.approval

    with pytest.raises(FileExistsError, match="control root must be empty"):
        write_external_control_package_v2(bundle, environment, verification)


def test_nonempty_raw_or_analysis_root_blocks_control_package(tmp_path: Path) -> None:
    environment, bundle, verification = _approved_bundle(tmp_path)
    raw_root = Path(bundle.artifact_layout["raw_root"])
    raw_root.mkdir(parents=True)
    (raw_root / "unexpected").write_text("x\n", encoding="utf-8")
    with pytest.raises(FileExistsError, match="raw root must be empty"):
        write_external_control_package_v2(bundle, environment, verification)

    raw_root.joinpath("unexpected").unlink()
    analysis_root = Path(bundle.artifact_layout["analysis_root"])
    analysis_root.mkdir(parents=True)
    (analysis_root / "unexpected").write_text("x\n", encoding="utf-8")
    with pytest.raises(FileExistsError, match="analysis root must be empty"):
        write_external_control_package_v2(bundle, environment, verification)


def test_environment_or_verification_mismatch_fails_closed(tmp_path: Path) -> None:
    environment, bundle, verification = _approved_bundle(tmp_path)
    changed_environment = replace(environment, machine="different-machine")
    with pytest.raises(ValueError, match="environment lock differs"):
        write_external_control_package_v2(
            bundle,
            changed_environment,
            verification,
        )

    failed_verification = replace(verification, verification_passed=False)
    with pytest.raises(ValueError, match="has not issued approval"):
        write_external_control_package_v2(
            bundle,
            environment,
            failed_verification,
        )

    wrong_reviewer = replace(verification, reviewer="reviewer-c")
    with pytest.raises(ValueError, match="reviewer differs"):
        write_external_control_package_v2(
            bundle,
            environment,
            wrong_reviewer,
        )


def test_unsigned_or_unready_bundle_cannot_form_control_package(tmp_path: Path) -> None:
    environment = _environment_or_skip()
    source_root = Path(__file__).parents[2].resolve()
    layout = ExternalArtifactLayout(
        control_root=str((tmp_path / "control").resolve()),
        raw_root=str((tmp_path / "raw").resolve()),
        analysis_root=str((tmp_path / "analysis").resolve()),
    )
    manifest = build_current_confirmatory_manifest(
        ConfirmatoryPhase.CONFIRMATORY,
        code_ref=_FAKE_SHA,
    )
    unsigned = build_external_freeze_bundle_v2(
        manifest,
        source_root=source_root,
        source_git_sha=_FAKE_SHA,
        artifact_layout=layout,
        environment_lock=environment,
        builder="builder-a",
    )
    verification = IndependentFreezeVerificationV2(
        source_git_sha_matches=True,
        unsigned_bundle_matches=True,
        environment_matches=True,
        builder_and_reviewer_distinct=True,
        manifest_execution_ready=False,
        candidate_execution_counter_zero=True,
        approval_issued=False,
        reviewer="reviewer-b",
        expected_unsigned_hash=unsigned.unsigned_hash(),
        observed_unsigned_hash=unsigned.unsigned_hash(),
        verification_passed=True,
    )
    with pytest.raises(ValueError, match="manifest is not execution-ready"):
        write_external_control_package_v2(unsigned, environment, verification)
