from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from sparkbrain.comparison.cx01.artifacts import write_run_atomic
from sparkbrain.comparison.cx01.candidate import CandidatePurpose, CandidateSpec
from sparkbrain.comparison.cx01.formal import execute_formal_candidate
from sparkbrain.comparison.cx01.freeze import (
    ExecutionSeal,
    build_freeze_manifest,
    issue_execution_seal,
)


def _candidate() -> CandidateSpec:
    return CandidateSpec(
        generation_id="cx01-fixture-formal-gate-001",
        seeds=tuple(range(5100, 5110)),
        purpose=CandidatePurpose.STRUCTURE_FIXTURE,
    )


def _manifest(source_sha: str = "d" * 40):
    return build_freeze_manifest(
        source_git_sha=source_sha,
        builder="freeze-builder-fixture",
        candidate=_candidate(),
        execution_command="python -m sparkbrain.comparison.cx01.formal",
        artifact_root="artifacts/cx01/formal",
    )


def _seal(manifest):
    return issue_execution_seal(
        manifest,
        reviewer="independent-fixture",
        approval_digest=hashlib.sha256(b"fixture-approval").hexdigest(),
        approved=True,
    )


def test_atomic_writer_refuses_existing_run_identity(tmp_path: Path) -> None:
    manifest = _manifest()
    seal = _seal(manifest)
    first = write_run_atomic(
        tmp_path,
        run_id="fixture-run",
        manifest=manifest,
        seal=seal,
        rows=({"row": 1},),
    )
    assert (first / "COMPLETE").read_text(encoding="utf-8") == "complete\n"
    assert (first / "checksums.json").exists()
    with pytest.raises(FileExistsError):
        write_run_atomic(
            tmp_path,
            run_id="fixture-run",
            manifest=manifest,
            seal=seal,
            rows=({"row": 2},),
        )


def test_formal_execution_fails_before_capability_without_valid_seal(
    tmp_path: Path,
) -> None:
    manifest = _manifest()
    invalid = ExecutionSeal(
        manifest_hash=manifest.manifest_hash(),
        source_git_sha=manifest.source_git_sha,
        reviewer="",
        approval_digest=hashlib.sha256(b"not-approved").hexdigest(),
        approved=False,
    )
    with pytest.raises(ValueError):
        execute_formal_candidate(
            _candidate(),
            manifest,
            invalid,
            current_source_git_sha=manifest.source_git_sha,
            artifact_root=tmp_path,
        )
    assert list(tmp_path.iterdir()) == []


def test_formal_execution_rejects_source_mismatch_before_capability(
    tmp_path: Path,
) -> None:
    manifest = _manifest()
    seal = _seal(manifest)
    with pytest.raises(RuntimeError):
        execute_formal_candidate(
            _candidate(),
            manifest,
            seal,
            current_source_git_sha="e" * 40,
            artifact_root=tmp_path,
        )
    assert list(tmp_path.iterdir()) == []


def test_structure_fixture_cannot_execute_even_with_valid_seal(
    tmp_path: Path,
) -> None:
    manifest = _manifest()
    seal = _seal(manifest)
    with pytest.raises(RuntimeError, match="structure fixture"):
        execute_formal_candidate(
            _candidate(),
            manifest,
            seal,
            current_source_git_sha=manifest.source_git_sha,
            artifact_root=tmp_path,
        )
    assert list(tmp_path.iterdir()) == []
