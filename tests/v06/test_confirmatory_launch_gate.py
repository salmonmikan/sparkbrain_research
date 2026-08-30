from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from sparkbrain.evaluation.v06_confirmatory_candidate_manifest import (
    build_candidate_manifest,
)
from sparkbrain.evaluation.v06_confirmatory_environment import (
    ENVIRONMENT_LOCK_VERSION,
    RNG_CONTRACT,
    ConfirmatoryEnvironmentLock,
)
from sparkbrain.evaluation.v06_confirmatory_execution_seal import (
    build_freeze_record,
)
from sparkbrain.evaluation.v06_confirmatory_launch_gate import (
    GitWorkspaceState,
    claim_one_way_execution,
    inspect_git_workspace,
    validate_launch_gate,
)
from sparkbrain.v06.foundation import digest

_SOURCE_SHA = "a" * 40
_APPROVAL_ID = "APPROVED:launch-reviewer:0123456789abcdef"


def _repository_root() -> Path:
    return Path(__file__).parents[2]


def _environment() -> ConfirmatoryEnvironmentLock:
    distributions = ("sparkbrain-research==0.3.2.dev0",)
    return ConfirmatoryEnvironmentLock(
        version=ENVIRONMENT_LOCK_VERSION,
        python_implementation="CPython",
        python_version="3.11.9",
        python_executable_sha256="b" * 64,
        platform_system="Linux",
        platform_release="6.8.0-launch-test",
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
    return build_candidate_manifest(source_code_sha=_SOURCE_SHA)


def _freeze_record():
    return build_freeze_record(
        _manifest(),
        source_code_sha=_SOURCE_SHA,
        repository_root=_repository_root(),
        environment_lock=_environment(),
        approval_id=_APPROVAL_ID,
    )


def _workspace(**changes) -> GitWorkspaceState:
    value = GitWorkspaceState(
        head_sha=_SOURCE_SHA,
        status_porcelain="",
        symbolic_ref=None,
        detached_head=True,
    )
    return replace(value, **changes)


def _validate(tmp_path: Path, **changes):
    workspace = changes.pop("workspace", _workspace())
    environment = changes.pop("observed_environment", _environment())
    output_root = changes.pop("output_root", tmp_path / "output")
    counter = changes.pop(
        "execution_counter_path",
        output_root / "control" / "execution_state.json",
    )
    marker = changes.pop(
        "start_marker_path",
        output_root / "control" / "STARTED.json",
    )
    assert not changes
    return validate_launch_gate(
        _manifest(),
        _freeze_record(),
        _environment(),
        repository_root=_repository_root(),
        output_root=output_root,
        execution_counter_path=counter,
        start_marker_path=marker,
        workspace=workspace,
        observed_environment=environment,
    )


def test_clean_detached_matching_workspace_passes_every_launch_gate(
    tmp_path: Path,
) -> None:
    report = _validate(tmp_path)
    assert report.seal_report.execution_allowed is True
    assert report.environment_report.exact_match is True
    assert report.workspace_clean is True
    assert report.detached_head is True
    assert report.current_sha_matches_source is True
    assert report.output_directory_empty is True
    assert report.execution_counter_zero is True
    assert report.start_marker_absent is True
    assert report.launch_allowed is True


def test_expected_control_files_are_allowed_before_launch(tmp_path: Path) -> None:
    output = tmp_path / "output"
    control = output / "control"
    control.mkdir(parents=True)
    for file_name in (
        "environment_lock.json",
        "freeze_record.json",
        "freeze_verification.json",
    ):
        control.joinpath(file_name).write_text("{}\n", encoding="utf-8")
    report = _validate(tmp_path, output_root=output)
    assert report.output_directory_empty is True
    assert report.launch_allowed is True


@pytest.mark.parametrize(
    "workspace",
    (
        _workspace(status_porcelain=" M source.py\n"),
        _workspace(detached_head=False, symbolic_ref="v06-freeze"),
        _workspace(head_sha="c" * 40),
    ),
)
def test_workspace_mismatch_fails_closed(
    tmp_path: Path,
    workspace: GitWorkspaceState,
) -> None:
    assert _validate(tmp_path, workspace=workspace).launch_allowed is False


def test_nonempty_payload_or_unknown_control_file_blocks_launch(
    tmp_path: Path,
) -> None:
    output = tmp_path / "output"
    output.mkdir()
    output.joinpath("unexpected.txt").write_text("data", encoding="utf-8")
    assert _validate(tmp_path, output_root=output).launch_allowed is False

    output.joinpath("unexpected.txt").unlink()
    raw = output / "raw"
    raw.mkdir()
    raw.joinpath("old-result.json").write_text("{}\n", encoding="utf-8")
    assert _validate(tmp_path, output_root=output).launch_allowed is False

    raw.joinpath("old-result.json").unlink()
    raw.rmdir()
    control = output / "control"
    control.mkdir()
    control.joinpath("unknown.json").write_text("{}\n", encoding="utf-8")
    assert _validate(tmp_path, output_root=output).launch_allowed is False


def test_previous_execution_counter_blocks_launch(tmp_path: Path) -> None:
    output = tmp_path / "output"
    control = output / "control"
    control.mkdir(parents=True)
    counter = control / "execution_state.json"
    counter.write_text('{"candidate_execution_count":1}\n', encoding="utf-8")
    assert _validate(
        tmp_path,
        output_root=output,
        execution_counter_path=counter,
    ).launch_allowed is False


def test_environment_mismatch_blocks_launch(tmp_path: Path) -> None:
    changed = replace(_environment(), python_version="3.11.10")
    report = _validate(tmp_path, observed_environment=changed)
    assert report.environment_report.exact_match is False
    assert report.launch_allowed is False


def test_execution_claim_is_exclusive_and_one_way(tmp_path: Path) -> None:
    output = tmp_path / "output"
    marker = output / "control" / "STARTED.json"
    report = _validate(
        tmp_path,
        output_root=output,
        start_marker_path=marker,
    )
    claim_one_way_execution(
        marker,
        freeze_record=_freeze_record(),
        launch_report=report,
    )
    assert marker.is_file()
    with pytest.raises(FileExistsError):
        claim_one_way_execution(
            marker,
            freeze_record=_freeze_record(),
            launch_report=report,
        )
    assert _validate(
        tmp_path,
        output_root=output,
        start_marker_path=marker,
    ).launch_allowed is False


def test_current_review_checkout_is_not_the_sealed_source_identity() -> None:
    state = inspect_git_workspace(_repository_root())
    assert len(state.head_sha) == 40
    assert not (
        state.detached_head
        and state.clean
        and state.head_sha == _SOURCE_SHA
    )
