from __future__ import annotations

from pathlib import Path

import pytest

from sparkbrain.comparison.cx01.candidate import CandidatePurpose, CandidateSpec
from sparkbrain.comparison.cx01.control import (
    OneWayControlMarker,
    require_control_marker,
    write_control_marker,
)
from sparkbrain.comparison.cx01.freeze import (
    build_freeze_manifest,
    issue_execution_seal,
)


def _fixture() -> CandidateSpec:
    return CandidateSpec(
        generation_id="cx01-fixture-control-001",
        seeds=tuple(range(5000, 5010)),
        purpose=CandidatePurpose.STRUCTURE_FIXTURE,
    )


def _manifest(candidate: CandidateSpec):
    return build_freeze_manifest(
        source_git_sha="a" * 40,
        builder="builder-a",
        candidate=candidate,
        execution_command="formal-fixture",
        artifact_root="artifacts/cx01/formal",
    )


def _seal(manifest):
    return issue_execution_seal(
        manifest,
        reviewer="reviewer-b",
        approval_digest="b" * 64,
        approved=True,
    )


def test_marker_schema_rejects_wrong_policy() -> None:
    marker = OneWayControlMarker(
        candidate_spec_hash="a" * 64,
        candidate_grid_hash="b" * 64,
        declaration_bundle_hash="c" * 64,
        manifest_hash="d" * 64,
        source_git_sha="e" * 40,
        execution_policy="rerunnable",
    )
    with pytest.raises(ValueError, match="one-way-no-rerun"):
        marker.validate()


def test_structure_fixture_cannot_be_consumed_as_formal_marker(tmp_path: Path) -> None:
    candidate = _fixture()
    manifest = _manifest(candidate)
    seal = _seal(manifest)
    output = tmp_path / "STARTED.json"
    with pytest.raises(RuntimeError, match="structure fixture"):
        write_control_marker(
            output,
            candidate,
            manifest,
            seal,
            current_source_git_sha=manifest.source_git_sha,
        )
    assert not output.exists()


def test_require_marker_rejects_structure_fixture_before_capability() -> None:
    candidate = _fixture()
    manifest = _manifest(candidate)
    marker = OneWayControlMarker(
        candidate_spec_hash=candidate.specification_hash(),
        candidate_grid_hash=manifest.candidate_grid_hash,
        declaration_bundle_hash=manifest.declaration_bundle_hash,
        manifest_hash=manifest.manifest_hash(),
        source_git_sha=manifest.source_git_sha,
    )
    with pytest.raises(RuntimeError, match="structure fixture"):
        require_control_marker(
            marker,
            candidate,
            manifest,
            current_source_git_sha=manifest.source_git_sha,
        )
