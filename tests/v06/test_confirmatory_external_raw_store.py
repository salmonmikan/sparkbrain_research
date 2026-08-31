from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from sparkbrain.evaluation.v06_confirmatory_external_freeze import (
    ExternalArtifactLayout,
)
from sparkbrain.evaluation.v06_confirmatory_external_raw_store import (
    ExternalAtomicRawRunWriter,
    RawExecutionMetadata,
)

_SOURCE_SHA = "a" * 40
_ENVELOPE_HASH = "b" * 64
_MANIFEST_HASH = "c" * 64
_WORLD_GRID_HASH = "d" * 64
_WORLD_HASH = "e" * 64


def _layout(tmp_path: Path) -> ExternalArtifactLayout:
    source = tmp_path / "source"
    source.mkdir()
    layout = ExternalArtifactLayout(
        control_root=str((tmp_path / "control").resolve()),
        raw_root=str((tmp_path / "raw").resolve()),
        analysis_root=str((tmp_path / "analysis").resolve()),
    )
    layout.validate(source_checkout=source)
    return layout


def _metadata(index: int, *, record_count: int = 2) -> RawExecutionMetadata:
    execution_id = f"{index + 1:064x}"
    return RawExecutionMetadata(
        execution_id=execution_id,
        envelope_hash=_ENVELOPE_HASH,
        source_git_sha=_SOURCE_SHA,
        manifest_hash=_MANIFEST_HASH,
        world_generation_id="candidate-test",
        world_grid_hash=_WORLD_GRID_HASH,
        family_id="family-test",
        seed=1000 + index,
        condition=f"condition-{index}",
        world_specification_hash=_WORLD_HASH,
        record_count=record_count,
        resource_record_count=1,
    )


def _writer(tmp_path: Path, *, run_id: str = "run-test") -> ExternalAtomicRawRunWriter:
    return ExternalAtomicRawRunWriter(
        _layout(tmp_path),
        run_id=run_id,
        envelope_hash=_ENVELOPE_HASH,
        source_git_sha=_SOURCE_SHA,
        expected_execution_count=2,
        expected_evidence_record_count=4,
    )


def _write_pair(writer: ExternalAtomicRawRunWriter) -> None:
    for index in range(2):
        writer.write_execution(
            _metadata(index),
            result_rows=(
                {"domain": "a", "passed": True},
                {"domain": "b", "passed": False},
            ),
            resource_row={"condition": f"condition-{index}", "wall_clock_ns": index},
        )


def test_two_level_atomic_commit_excludes_transaction_namespace(tmp_path: Path) -> None:
    writer = _writer(tmp_path)
    writer.begin()
    _write_pair(writer)
    commit = writer.finalize()
    final = writer.final_root
    assert commit.execution_count == 2
    assert commit.evidence_record_count == 4
    assert commit.resource_record_count == 2
    assert final.is_dir()
    assert (final / "RAW_COMPLETE").is_file()
    assert (final / "raw_manifest.json").is_file()
    assert (final / "results.jsonl").is_file()
    assert (final / "resources.jsonl").is_file()
    assert not (final / ".transactions").exists()
    assert len(tuple((final / "executions").iterdir())) == 2
    assert final.stat().st_mode & 0o222 == 0
    assert all(path.stat().st_mode & 0o222 == 0 for path in final.rglob("*"))
    manifest = json.loads((final / "raw_manifest.json").read_text(encoding="utf-8"))
    assert manifest["execution_count"] == 2
    assert manifest["evidence_record_count"] == 4


def test_orphan_transaction_blocks_final_commit_and_never_enters_final(tmp_path: Path) -> None:
    writer = _writer(tmp_path)
    writer.begin()
    _write_pair(writer)
    orphan = writer.transactions / "orphan.tmp"
    orphan.mkdir()
    (orphan / "partial.json").write_text("{}\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="orphan execution transactions"):
        writer.finalize()
    assert not writer.final_root.exists()
    assert orphan.exists()
    failed = writer.abort(preserve_partial=True)
    assert failed is not None
    assert failed.name.endswith(".FAILED")
    assert (failed / "FAILED").is_file()
    assert failed.stat().st_mode & 0o222 == 0


def test_duplicate_execution_identity_fails_before_overwrite(tmp_path: Path) -> None:
    writer = _writer(tmp_path)
    writer.begin()
    metadata = _metadata(0)
    rows = (
        {"domain": "a", "passed": True},
        {"domain": "b", "passed": False},
    )
    resource = {"condition": "condition-0", "wall_clock_ns": 1}
    writer.write_execution(metadata, result_rows=rows, resource_row=resource)
    with pytest.raises(FileExistsError, match="duplicate execution identity"):
        writer.write_execution(metadata, result_rows=rows, resource_row=resource)


def test_checksum_tamper_blocks_run_finalization(tmp_path: Path) -> None:
    writer = _writer(tmp_path)
    writer.begin()
    _write_pair(writer)
    execution = writer.executions / _metadata(0).execution_id
    (execution / "results.jsonl").write_text("tampered\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="checksum mismatch"):
        writer.finalize()
    assert not writer.final_root.exists()


def test_raw_run_identity_and_existing_output_fail_closed(tmp_path: Path) -> None:
    layout = _layout(tmp_path)
    with pytest.raises(ValueError, match="safe"):
        ExternalAtomicRawRunWriter(
            layout,
            run_id="../unsafe",
            envelope_hash=_ENVELOPE_HASH,
            source_git_sha=_SOURCE_SHA,
            expected_execution_count=1,
            expected_evidence_record_count=1,
        )
    writer = ExternalAtomicRawRunWriter(
        layout,
        run_id="existing",
        envelope_hash=_ENVELOPE_HASH,
        source_git_sha=_SOURCE_SHA,
        expected_execution_count=1,
        expected_evidence_record_count=1,
    )
    writer.begin()
    with pytest.raises(FileExistsError, match="already exists"):
        writer.begin()
    writer.abort(preserve_partial=False)


def test_execution_metadata_rejects_wrong_hash_and_record_counts() -> None:
    with pytest.raises(ValueError, match="wrong hash length"):
        _metadata(0).__class__(
            **{
                **_metadata(0).state_dict(),
                "source_git_sha": "short",
            }
        ).validate()
    with pytest.raises(ValueError, match="record counts"):
        _metadata(0, record_count=0).validate()


def test_exclusive_execution_files_are_not_overwritten(tmp_path: Path) -> None:
    writer = _writer(tmp_path)
    writer.begin()
    metadata = _metadata(0)
    transaction = writer.transactions / f"{metadata.execution_id}.tmp"
    transaction.mkdir()
    existing = transaction / "metadata.json"
    existing.write_text("existing\n", encoding="utf-8")
    with pytest.raises(FileExistsError):
        writer.write_execution(
            metadata,
            result_rows=(
                {"domain": "a", "passed": True},
                {"domain": "b", "passed": False},
            ),
            resource_row={"condition": "condition-0"},
        )
    assert existing.read_text(encoding="utf-8") == "existing\n"
    os.chmod(writer.run_staging, 0o755)
