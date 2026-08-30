from __future__ import annotations

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
from sparkbrain.evaluation.v06_confirmatory_external_freeze import (
    ExternalArtifactLayout,
)
from sparkbrain.evaluation.v06_confirmatory_external_verification_v2 import (
    independently_verify_external_bundle_v2,
    load_external_freeze_bundle_v2,
)
from sparkbrain.evaluation.v06_confirmatory_freeze_bundle_v2 import (
    build_external_freeze_bundle_v2,
    write_external_freeze_bundle_v2,
)

_FAKE_SHA = "a" * 40


def _environment_or_skip():
    if platform.python_implementation() != "CPython" or sys.version_info[:2] != (3, 11):
        pytest.skip("independent freeze verification is locked to CPython 3.11")
    if os.environ.get("PYTHONHASHSEED") != "0" or os.environ.get("TZ") != "UTC":
        pytest.skip("focused freeze workflow supplies deterministic environment variables")
    return capture_environment_lock_v2()


def _unsigned_bundle(tmp_path: Path):
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
    bundle = build_external_freeze_bundle_v2(
        manifest,
        source_root=source_root,
        source_git_sha=_FAKE_SHA,
        artifact_layout=layout,
        environment_lock=environment,
        builder="builder-a",
    )
    return source_root, environment, bundle


def test_unsigned_bundle_round_trip_preserves_tuple_contracts(tmp_path: Path) -> None:
    _, _, bundle = _unsigned_bundle(tmp_path)
    path = tmp_path / "control" / "unsigned_freeze_bundle.json"
    write_external_freeze_bundle_v2(
        bundle,
        path=path,
        require_execution_ready=False,
    )
    loaded = load_external_freeze_bundle_v2(path)
    assert loaded == bundle
    assert isinstance(loaded.heldout_seeds, tuple)
    assert all(
        isinstance(value, tuple)
        for value in loaded.privilege_inventory.values()
    )
    assert all(
        isinstance(value, tuple)
        for value in loaded.world_field_read_inventory.values()
    )


def test_independent_rebuild_can_verify_but_not_approve_unready_manifest(
    tmp_path: Path,
) -> None:
    source_root, environment, bundle = _unsigned_bundle(tmp_path)
    approved, report = independently_verify_external_bundle_v2(
        bundle,
        source_root=source_root,
        environment_lock=environment,
        reviewer="reviewer-b",
        issue_approval=False,
    )
    assert approved is None
    assert report.verification_passed is True
    assert report.unsigned_bundle_matches is True
    assert report.environment_matches is True
    assert report.candidate_execution_counter_zero is True
    assert report.manifest_execution_ready is False
    assert report.approval_issued is False

    with pytest.raises(ValueError, match="approval is prohibited"):
        independently_verify_external_bundle_v2(
            bundle,
            source_root=source_root,
            environment_lock=environment,
            reviewer="reviewer-b",
            issue_approval=True,
        )


def test_builder_cannot_act_as_independent_reviewer(tmp_path: Path) -> None:
    source_root, environment, bundle = _unsigned_bundle(tmp_path)
    with pytest.raises(ValueError, match="reviewer must differ"):
        independently_verify_external_bundle_v2(
            bundle,
            source_root=source_root,
            environment_lock=environment,
            reviewer="builder-a",
            issue_approval=False,
        )


def test_any_unsigned_bundle_change_is_detected(tmp_path: Path) -> None:
    source_root, environment, bundle = _unsigned_bundle(tmp_path)
    changed = replace(bundle, training_schedule_hash="0" * 64)
    with pytest.raises(ValueError, match="hash"):
        changed.validate_structure()

    changed = replace(
        bundle,
        adapter_inventory=tuple(reversed(bundle.adapter_inventory)),
        adapter_inventory_hash=bundle.adapter_inventory_hash,
    )
    with pytest.raises(ValueError, match="adapter inventory hash"):
        changed.validate_structure()

    different_environment = replace(environment, machine="different-machine")
    approved, report = independently_verify_external_bundle_v2(
        bundle,
        source_root=source_root,
        environment_lock=different_environment,
        reviewer="reviewer-b",
        issue_approval=False,
    )
    assert approved is None
    assert report.environment_matches is False
    assert report.verification_passed is False
