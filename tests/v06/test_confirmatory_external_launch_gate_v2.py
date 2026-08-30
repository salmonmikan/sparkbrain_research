from __future__ import annotations

import os
import platform
import subprocess
import sys
from pathlib import Path

import pytest

from sparkbrain.evaluation.v06_confirmatory_candidate_manifest import (
    build_candidate_manifest,
)
from sparkbrain.evaluation.v06_confirmatory_environment_lock_v2 import (
    capture_environment_lock_v2,
)
from sparkbrain.evaluation.v06_confirmatory_external_control_package_v2 import (
    write_external_control_package_v2,
)
from sparkbrain.evaluation.v06_confirmatory_external_freeze import (
    ExternalArtifactLayout,
)
from sparkbrain.evaluation.v06_confirmatory_external_launch_gate_v2 import (
    claim_external_one_way_execution_v2,
    require_external_launch_gate_v2,
    validate_external_launch_gate_v2,
)
from sparkbrain.evaluation.v06_confirmatory_external_verification_v2 import (
    IndependentFreezeVerificationV2,
)
from sparkbrain.evaluation.v06_confirmatory_freeze_bundle_v2 import (
    build_external_freeze_bundle_v2,
    verify_independent_rebuild,
)


def _git(path: Path, *arguments: str, check: bool = True) -> str:
    return subprocess.run(
        ("git", "-C", str(path), *arguments),
        check=check,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _environment_or_skip():
    if platform.python_implementation() != "CPython" or sys.version_info[:2] != (3, 11):
        pytest.skip("external launch gate is frozen to CPython 3.11")
    if os.environ.get("PYTHONHASHSEED") != "0" or os.environ.get("TZ") != "UTC":
        pytest.skip("focused workflow supplies deterministic environment variables")
    return capture_environment_lock_v2()


def _detached_clone(tmp_path: Path) -> tuple[Path, str]:
    repository = Path(__file__).parents[2].resolve()
    source = tmp_path / "detached-source"
    clone_environment = os.environ.copy()
    clone_environment["GIT_LFS_SKIP_SMUDGE"] = "1"
    subprocess.run(
        ("git", "clone", "--no-local", "--quiet", str(repository), str(source)),
        check=True,
        env=clone_environment,
    )
    sha = _git(source, "rev-parse", "HEAD")
    _git(source, "checkout", "--quiet", "--detach", sha)
    assert _git(source, "status", "--porcelain") == ""
    return source, sha


def _sealed_package(tmp_path: Path):
    environment = _environment_or_skip()
    source, sha = _detached_clone(tmp_path)
    manifest = build_candidate_manifest(source_code_sha=sha)
    layout = ExternalArtifactLayout(
        control_root=str((tmp_path / "control").resolve()),
        raw_root=str((tmp_path / "raw").resolve()),
        analysis_root=str((tmp_path / "analysis").resolve()),
    )
    first = build_external_freeze_bundle_v2(
        manifest,
        source_root=source,
        source_git_sha=sha,
        artifact_layout=layout,
        environment_lock=environment,
        builder="builder-a",
    )
    second = build_external_freeze_bundle_v2(
        manifest,
        source_root=source,
        source_git_sha=sha,
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
    write_external_control_package_v2(approved, environment, verification)
    return source, approved


def test_exact_detached_clean_package_opens_machine_gate(tmp_path: Path) -> None:
    source, bundle = _sealed_package(tmp_path)
    report = require_external_launch_gate_v2(bundle)
    assert report.execution_allowed is True
    assert report.bundle_execution_ready is True
    assert report.source_checkout_exists is True
    assert report.source_checkout_clean is True
    assert report.source_sha_matches is True
    assert report.source_is_detached is True
    assert report.independent_rebuild_matches is True
    assert report.environment_matches is True
    assert report.control_package_exact is True
    assert report.candidate_counter_zero is True
    assert report.raw_root_empty is True
    assert report.analysis_root_empty is True
    assert _git(source, "status", "--porcelain") == ""


def test_one_way_claim_consumes_fresh_execution_state(tmp_path: Path) -> None:
    _, bundle = _sealed_package(tmp_path)
    report = require_external_launch_gate_v2(bundle)
    marker, counter = claim_external_one_way_execution_v2(bundle, report)
    assert marker.name == "STARTED.json"
    assert counter.name == "candidate_execution_counter.1.json"
    assert marker.stat().st_mode & 0o222 == 0
    assert counter.stat().st_mode & 0o222 == 0
    after = validate_external_launch_gate_v2(bundle)
    assert after.started_marker_absent is False
    assert after.started_counter_absent is False
    assert after.control_package_exact is False
    assert after.execution_allowed is False
    with pytest.raises(FileExistsError):
        claim_external_one_way_execution_v2(bundle, report)


def test_dirty_attached_or_wrong_source_closes_gate(tmp_path: Path) -> None:
    source, bundle = _sealed_package(tmp_path)
    (source / "dirty.txt").write_text("dirty\n", encoding="utf-8")
    dirty = validate_external_launch_gate_v2(bundle)
    assert dirty.source_checkout_clean is False
    assert dirty.execution_allowed is False
    source.joinpath("dirty.txt").unlink()

    branch = _git(source, "branch", "--format=%(refname:short)").splitlines()[0]
    _git(source, "checkout", "--quiet", branch)
    attached = validate_external_launch_gate_v2(bundle)
    assert attached.source_is_detached is False
    assert attached.execution_allowed is False


def test_extra_control_file_or_nonempty_output_closes_gate(tmp_path: Path) -> None:
    _, bundle = _sealed_package(tmp_path)
    control = Path(bundle.artifact_layout["control_root"])
    (control / "unexpected.json").write_text("{}\n", encoding="utf-8")
    extra = validate_external_launch_gate_v2(bundle)
    assert extra.control_package_exact is False
    assert extra.execution_allowed is False
    control.joinpath("unexpected.json").unlink()

    raw = Path(bundle.artifact_layout["raw_root"])
    raw.mkdir(parents=True)
    (raw / "unexpected").write_text("x\n", encoding="utf-8")
    nonempty_raw = validate_external_launch_gate_v2(bundle)
    assert nonempty_raw.raw_root_empty is False
    assert nonempty_raw.execution_allowed is False
    raw.joinpath("unexpected").unlink()

    analysis = Path(bundle.artifact_layout["analysis_root"])
    analysis.mkdir(parents=True)
    (analysis / "unexpected").write_text("x\n", encoding="utf-8")
    nonempty_analysis = validate_external_launch_gate_v2(bundle)
    assert nonempty_analysis.analysis_root_empty is False
    assert nonempty_analysis.execution_allowed is False
