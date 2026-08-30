from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import pytest

from sparkbrain.evaluation.v06_confirmatory import ConfirmatoryPhase
from sparkbrain.evaluation.v06_confirmatory_candidate_manifest import (
    build_candidate_manifest,
)
from sparkbrain.evaluation.v06_confirmatory_current_manifest import (
    build_current_confirmatory_manifest,
)
from sparkbrain.evaluation.v06_confirmatory_environment_lock_v2 import (
    capture_environment_lock_v2,
    environment_locks_equal,
)
from sparkbrain.evaluation.v06_confirmatory_external_freeze import (
    ExternalArtifactLayout,
)
from sparkbrain.evaluation.v06_confirmatory_freeze_bundle_v2 import (
    build_external_freeze_bundle_v2,
    combined_training_schedule_hash,
    verify_independent_rebuild,
    write_external_freeze_bundle_v2,
)
from sparkbrain.evaluation.v06_confirmatory_heldout_spec import (
    HELDOUT_SEEDS,
    QUARANTINED_HELDOUT_SEEDS,
    WORLD_GENERATION_ID,
)

_FAKE_SHA = "a" * 40


def _source_root() -> Path:
    return Path(__file__).parents[2].resolve()


def _layout(tmp_path: Path) -> ExternalArtifactLayout:
    return ExternalArtifactLayout(
        control_root=str((tmp_path / "control").resolve()),
        raw_root=str((tmp_path / "raw").resolve()),
        analysis_root=str((tmp_path / "analysis").resolve()),
    )


def _environment_or_skip():
    if platform.python_implementation() != "CPython" or sys.version_info[:2] != (3, 11):
        pytest.skip("freeze environment is intentionally locked to CPython 3.11")
    if os.environ.get("PYTHONHASHSEED") != "0" or os.environ.get("TZ") != "UTC":
        pytest.skip("freeze environment variables are set by the focused workflow")
    return capture_environment_lock_v2()


def _candidate(tmp_path: Path, *, ready: bool, builder: str = "builder-a"):
    environment = _environment_or_skip()
    manifest = (
        build_candidate_manifest(source_code_sha=_FAKE_SHA)
        if ready
        else build_current_confirmatory_manifest(ConfirmatoryPhase.CONFIRMATORY)
    )
    return build_external_freeze_bundle_v2(
        manifest,
        source_root=_source_root(),
        source_git_sha=_FAKE_SHA,
        artifact_layout=_layout(tmp_path),
        environment_lock=environment,
        builder=builder,
    )


def test_environment_lock_captures_exact_dependency_and_rng_contract() -> None:
    lock = _environment_or_skip()
    lock.validate()
    assert lock.python_implementation == "CPython"
    assert lock.python_version.startswith("3.11.")
    assert lock.operating_system == "Linux"
    assert lock.timezone == "UTC"
    assert lock.python_hash_seed == "0"
    assert lock.installed_distributions
    assert len(lock.installed_distributions_hash) == 64
    assert lock.rng_contract.python_generator == "random.Random/MT19937"
    assert lock.rng_contract.numpy_rng_allowed is False
    assert environment_locks_equal(lock, capture_environment_lock_v2()) is True


def test_unsigned_current_candidate_cannot_be_approved_for_execution(
    tmp_path: Path,
) -> None:
    bundle = _candidate(tmp_path, ready=False)
    bundle.validate_structure()
    assert bundle.manifest_execution_ready is False
    assert bundle.reviewer is None
    assert bundle.approval is None
    with pytest.raises(ValueError, match="manifest is not execution-ready"):
        bundle.validate_for_execution()
    target = tmp_path / "control" / "unsigned_freeze_candidate.json"
    file_hash = write_external_freeze_bundle_v2(
        bundle,
        path=target,
        require_execution_ready=False,
    )
    assert target.is_file()
    assert len(file_hash) == 64
    assert target.stat().st_mode & 0o222 == 0


def test_bundle_binds_full_world_schedule_adapter_environment_and_paths(
    tmp_path: Path,
) -> None:
    bundle = _candidate(tmp_path, ready=True)
    assert bundle.world_generation_id == WORLD_GENERATION_ID
    assert bundle.heldout_seeds == HELDOUT_SEEDS
    assert bundle.quarantined_seeds == QUARANTINED_HELDOUT_SEEDS
    assert set(bundle.heldout_seeds).isdisjoint(bundle.quarantined_seeds)
    assert bundle.training_schedule_hash == combined_training_schedule_hash()
    assert len(bundle.adapter_inventory) == 8
    assert len(bundle.adapter_source_hashes) == 9
    assert bundle.world_field_read_inventory
    assert bundle.privilege_inventory["g4-assembly-conditioned"] == (
        "explicit-assembly-state",
    )
    assert "scalar-reward" in bundle.privilege_inventory[
        "g5-typed-functional-heads"
    ]
    assert bundle.threshold_mode_inventory["g3-recurrent"] == (
        "field-threshold-bypassed"
    )
    assert bundle.normalized_resource_contract_hash
    assert bundle.execution_command[0] == bundle.environment_lock["python_executable"]
    assert bundle.execution_command[1:3] == (
        "-m",
        "sparkbrain.evaluation.v06_confirmatory_execute_external_v2",
    )
    assert bundle.scoring_command[0] == bundle.environment_lock["python_executable"]
    assert bundle.scoring_command[1:3] == (
        "-m",
        "sparkbrain.evaluation.v06_confirmatory_score_external_v2",
    )
    source = _source_root()
    for path in bundle.artifact_layout.values():
        assert not Path(path).is_relative_to(source)


def test_independent_rebuild_issues_approval_bound_to_unsigned_hash(
    tmp_path: Path,
) -> None:
    first = _candidate(tmp_path, ready=True, builder="builder-a")
    second = _candidate(tmp_path, ready=True, builder="builder-a")
    assert first.unsigned_state_dict() == second.unsigned_state_dict()
    approved = verify_independent_rebuild(first, second, reviewer="reviewer-b")
    approved.validate_for_execution()
    assert approved.reviewer == "reviewer-b"
    assert approved.approval == (
        f"APPROVED:reviewer-b:{approved.unsigned_hash()[:16]}"
    )
    target = tmp_path / "control" / "freeze_bundle.json"
    write_external_freeze_bundle_v2(
        approved,
        path=target,
        require_execution_ready=True,
    )
    state = json.loads(target.read_text(encoding="utf-8"))
    assert state["source_git_sha"] == _FAKE_SHA
    assert state["approval"] == approved.approval


def test_builder_cannot_self_approve_and_any_bound_hash_change_fails(
    tmp_path: Path,
) -> None:
    first = _candidate(tmp_path, ready=True, builder="builder-a")
    second = _candidate(tmp_path, ready=True, builder="builder-a")
    with pytest.raises(ValueError, match="reviewer must differ"):
        verify_independent_rebuild(first, second, reviewer="builder-a")
    changed = replace(second, training_schedule_hash="0" * 64)
    with pytest.raises(
        ValueError,
        match="training schedule hash mismatch|independent freeze bundle rebuild differs",
    ):
        verify_independent_rebuild(first, changed, reviewer="reviewer-b")


def test_source_inventory_changes_when_a_bound_source_changes(tmp_path: Path) -> None:
    bundle = _candidate(tmp_path, ready=True)
    source_hashes = dict(bundle.adapter_source_hashes)
    path = _source_root() / next(iter(source_hashes))
    assert source_hashes[str(path.relative_to(_source_root()))]
    completed = subprocess.run(
        ("git", "-C", str(_source_root()), "status", "--porcelain"),
        check=True,
        capture_output=True,
        text=True,
    )
    assert completed.stdout.strip() == ""
