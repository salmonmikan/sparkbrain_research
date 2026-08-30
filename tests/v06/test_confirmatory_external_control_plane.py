from __future__ import annotations

import json
import os
import subprocess
from dataclasses import replace
from pathlib import Path

import pytest

from sparkbrain.evaluation.v06_confirmatory import ConfirmatoryPhase
from sparkbrain.evaluation.v06_confirmatory_current_manifest import (
    build_current_confirmatory_manifest,
)
from sparkbrain.evaluation.v06_confirmatory_execution_seal import (
    build_freeze_record,
    frozen_manifest_for_test,
)
from sparkbrain.evaluation.v06_confirmatory_external_freeze import (
    ExternalArtifactLayout,
    build_external_freeze_envelope,
    read_external_freeze_envelope,
    verify_external_envelope_file,
    write_external_freeze_envelope,
)
from sparkbrain.evaluation.v06_confirmatory_external_launch_gate import (
    claim_one_way_execution,
    require_external_launch_gate,
    validate_external_launch_gate,
)

_APPROVAL = "APPROVED:unit-test:0123456789abcdef"


def _git(path: Path, *arguments: str) -> str:
    return subprocess.run(
        ("git", "-C", str(path), *arguments),
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _source_checkout(root: Path, *, detached: bool = True) -> tuple[Path, str]:
    source = root / "source"
    source.mkdir()
    _git(source, "init", "-q")
    _git(source, "config", "user.name", "Freeze Test")
    _git(source, "config", "user.email", "freeze-test@example.invalid")
    (source / "source.txt").write_text("frozen source\n", encoding="utf-8")
    _git(source, "add", "source.txt")
    _git(source, "commit", "-q", "-m", "freeze source")
    sha = _git(source, "rev-parse", "HEAD")
    if detached:
        _git(source, "checkout", "-q", "--detach", sha)
    return source, sha


def _sealed_control_plane(tmp_path: Path):
    source, sha = _source_checkout(tmp_path)
    manifest = frozen_manifest_for_test(
        build_current_confirmatory_manifest(ConfirmatoryPhase.CONFIRMATORY),
        code_ref=sha,
    )
    record = build_freeze_record(manifest, approval=_APPROVAL)
    layout = ExternalArtifactLayout(
        control_root=str((tmp_path / "control").resolve()),
        raw_root=str((tmp_path / "raw").resolve()),
        analysis_root=str((tmp_path / "analysis").resolve()),
    )
    envelope = build_external_freeze_envelope(
        record,
        source_checkout=source,
        artifact_layout=layout,
        created_by="unit-test-builder",
    )
    target = tmp_path / "control" / "freeze_envelope.json"
    file_hash = write_external_freeze_envelope(envelope, path=target)
    return source, manifest, record, envelope, target, file_hash


def test_external_layout_rejects_relative_nested_and_source_internal_paths(
    tmp_path: Path,
) -> None:
    source, _ = _source_checkout(tmp_path)
    with pytest.raises(ValueError, match="absolute"):
        ExternalArtifactLayout(
            control_root="control",
            raw_root=str((tmp_path / "raw").resolve()),
            analysis_root=str((tmp_path / "analysis").resolve()),
        ).validate(source_checkout=source)
    with pytest.raises(ValueError, match="outside source"):
        ExternalArtifactLayout(
            control_root=str((source / "control").resolve()),
            raw_root=str((tmp_path / "raw").resolve()),
            analysis_root=str((tmp_path / "analysis").resolve()),
        ).validate(source_checkout=source)
    with pytest.raises(ValueError, match="cannot be nested"):
        ExternalArtifactLayout(
            control_root=str((tmp_path / "external").resolve()),
            raw_root=str((tmp_path / "external" / "raw").resolve()),
            analysis_root=str((tmp_path / "analysis").resolve()),
        ).validate(source_checkout=source)


def test_external_envelope_solves_source_sha_self_reference(tmp_path: Path) -> None:
    source, manifest, record, envelope, target, expected_file_hash = (
        _sealed_control_plane(tmp_path)
    )
    assert target.is_file()
    assert envelope.source_git_sha == _git(source, "rev-parse", "HEAD")
    assert envelope.freeze_record["code_ref"] == envelope.source_git_sha
    assert manifest.code_ref == envelope.source_git_sha
    assert record.code_ref == envelope.source_git_sha
    loaded, actual_file_hash = verify_external_envelope_file(target)
    assert loaded == envelope
    assert actual_file_hash == expected_file_hash
    assert target.stat().st_mode & 0o222 == 0
    with pytest.raises(FileExistsError):
        write_external_freeze_envelope(envelope, path=target)


def test_detached_clean_source_and_external_empty_outputs_open_gate(
    tmp_path: Path,
) -> None:
    source, manifest, record, envelope, _, _ = _sealed_control_plane(tmp_path)
    report = require_external_launch_gate(
        envelope,
        record,
        manifest=manifest,
    )
    assert report.execution_allowed is True
    assert report.source_checkout_clean is True
    assert report.source_sha_matches is True
    assert report.source_is_detached is True
    assert report.raw_output_empty is True
    assert report.analysis_output_empty is True
    marker = claim_one_way_execution(envelope, report)
    assert marker.name == "STARTED.json"
    assert marker.stat().st_mode & 0o222 == 0
    with pytest.raises(FileExistsError):
        claim_one_way_execution(envelope, report)
    assert _git(source, "status", "--porcelain") == ""


def test_dirty_or_attached_source_closes_gate(tmp_path: Path) -> None:
    source, manifest, record, envelope, _, _ = _sealed_control_plane(tmp_path)
    (source / "dirty.txt").write_text("dirty\n", encoding="utf-8")
    dirty = validate_external_launch_gate(envelope, record, manifest=manifest)
    assert dirty.source_checkout_clean is False
    assert dirty.execution_allowed is False

    attached_root = tmp_path / "attached-case"
    attached_root.mkdir()
    attached_source, attached_sha = _source_checkout(attached_root, detached=False)
    attached_manifest = frozen_manifest_for_test(
        build_current_confirmatory_manifest(ConfirmatoryPhase.CONFIRMATORY),
        code_ref=attached_sha,
    )
    attached_record = build_freeze_record(attached_manifest, approval=_APPROVAL)
    attached_layout = ExternalArtifactLayout(
        control_root=str((attached_root / "control").resolve()),
        raw_root=str((attached_root / "raw").resolve()),
        analysis_root=str((attached_root / "analysis").resolve()),
    )
    attached_envelope = build_external_freeze_envelope(
        attached_record,
        source_checkout=attached_source,
        artifact_layout=attached_layout,
        created_by="unit-test-builder",
    )
    write_external_freeze_envelope(
        attached_envelope,
        path=attached_root / "control" / "freeze_envelope.json",
    )
    attached = validate_external_launch_gate(
        attached_envelope,
        attached_record,
        manifest=attached_manifest,
    )
    assert attached.source_is_detached is False
    assert attached.execution_allowed is False


def test_nonempty_raw_or_analysis_output_closes_gate(tmp_path: Path) -> None:
    _, manifest, record, envelope, _, _ = _sealed_control_plane(tmp_path)
    raw = Path(envelope.artifact_layout["raw_root"])
    raw.mkdir(parents=True)
    (raw / "unexpected.json").write_text("{}\n", encoding="utf-8")
    report = validate_external_launch_gate(envelope, record, manifest=manifest)
    assert report.raw_output_empty is False
    assert report.execution_allowed is False

    raw.joinpath("unexpected.json").unlink()
    analysis = Path(envelope.artifact_layout["analysis_root"])
    analysis.mkdir(parents=True)
    (analysis / "unexpected.json").write_text("{}\n", encoding="utf-8")
    report = validate_external_launch_gate(envelope, record, manifest=manifest)
    assert report.analysis_output_empty is False
    assert report.execution_allowed is False


def test_tampered_external_envelope_is_rejected(tmp_path: Path) -> None:
    _, _, _, envelope, target, _ = _sealed_control_plane(tmp_path)
    os.chmod(target, 0o644)
    state = json.loads(target.read_text(encoding="utf-8"))
    state["source_git_sha"] = "0" * 40
    target.write_text(json.dumps(state), encoding="utf-8")
    with pytest.raises(ValueError, match="detached source SHA"):
        read_external_freeze_envelope(target)

    changed = replace(envelope, execution_counter_initial=1)
    with pytest.raises(ValueError, match="begin at zero"):
        changed.validate()
