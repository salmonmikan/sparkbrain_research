from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from .v06_confirmatory_external_freeze import ExternalArtifactLayout

_RAW_STORE_VERSION = "v06-external-raw-store-1"
_REQUIRED_EXECUTION_FILES = (
    "metadata.json",
    "results.jsonl",
    "resource.json",
    "checksums.json",
    "COMPLETE",
)


def _canonical_json(value: object) -> str:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_file(path: Path, payload: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        with os.fdopen(descriptor, "wb", closefd=False) as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        os.close(descriptor)


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _json_bytes(value: object) -> bytes:
    return (_canonical_json(value) + "\n").encode("utf-8")


def _jsonl_bytes(rows: Iterable[object]) -> bytes:
    return b"".join(_json_bytes(row) for row in rows)


def _make_read_only(root: Path) -> None:
    for path in sorted(root.rglob("*"), reverse=True):
        mode = path.stat().st_mode
        if path.is_dir():
            path.chmod(mode & ~stat.S_IWUSR & ~stat.S_IWGRP & ~stat.S_IWOTH)
        else:
            path.chmod(mode & ~stat.S_IWUSR & ~stat.S_IWGRP & ~stat.S_IWOTH)
    root.chmod(root.stat().st_mode & ~stat.S_IWUSR & ~stat.S_IWGRP & ~stat.S_IWOTH)


@dataclass(frozen=True, slots=True)
class RawExecutionMetadata:
    execution_id: str
    envelope_hash: str
    source_git_sha: str
    manifest_hash: str
    world_generation_id: str
    world_grid_hash: str
    family_id: str
    seed: int
    condition: str
    world_specification_hash: str
    record_count: int
    resource_record_count: int

    def validate(self) -> None:
        if not self.execution_id or len(self.execution_id) != 64:
            raise ValueError("execution_id must be a deterministic SHA-256 identifier")
        for name in (
            "envelope_hash",
            "source_git_sha",
            "manifest_hash",
            "world_grid_hash",
            "world_specification_hash",
        ):
            value = str(getattr(self, name))
            expected = 40 if name == "source_git_sha" else 64
            if len(value) != expected:
                raise ValueError(f"{name} has the wrong hash length")
        if not self.world_generation_id or not self.family_id or not self.condition:
            raise ValueError("execution metadata identities must be non-empty")
        if self.record_count < 1 or self.resource_record_count != 1:
            raise ValueError("execution metadata record counts are invalid")

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class RawRunCommit:
    raw_store_version: str
    run_id: str
    envelope_hash: str
    source_git_sha: str
    execution_count: int
    evidence_record_count: int
    resource_record_count: int
    execution_ids: tuple[str, ...]
    execution_checksums: dict[str, str]

    def state_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "execution_ids": list(self.execution_ids),
        }

    def commit_hash(self) -> str:
        return _sha256_bytes(_json_bytes(self.state_dict()))


class ExternalAtomicRawRunWriter:
    """Raw-only two-level atomic writer outside the source checkout.

    Each execution is committed from ``.transactions/<id>.tmp`` to
    ``executions/<id>``. The run itself is committed from ``.<run>.tmp`` to the
    final immutable raw directory only after every execution has a COMPLETE
    marker and verified checksums. Orphan transactions block finalization and
    are never moved into the immutable final directory.
    """

    def __init__(
        self,
        layout: ExternalArtifactLayout,
        *,
        run_id: str,
        envelope_hash: str,
        source_git_sha: str,
        expected_execution_count: int,
        expected_evidence_record_count: int,
    ) -> None:
        if not run_id or "/" in run_id or "\\" in run_id:
            raise ValueError("run_id must be a safe non-empty directory name")
        if len(envelope_hash) != 64 or len(source_git_sha) != 40:
            raise ValueError("raw writer requires frozen envelope and source hashes")
        if expected_execution_count < 1 or expected_evidence_record_count < 1:
            raise ValueError("raw writer expected counts must be positive")
        self.layout = layout
        self.run_id = run_id
        self.envelope_hash = envelope_hash
        self.source_git_sha = source_git_sha
        self.expected_execution_count = expected_execution_count
        self.expected_evidence_record_count = expected_evidence_record_count
        _, raw_root, _ = layout.resolved()
        self.raw_root = raw_root
        self.run_staging = raw_root / f".{run_id}.tmp"
        self.final_root = raw_root / run_id
        self.transactions = self.run_staging / ".transactions"
        self.executions = self.run_staging / "executions"

    def begin(self) -> None:
        self.raw_root.mkdir(parents=True, exist_ok=True)
        if self.final_root.exists() or self.run_staging.exists():
            raise FileExistsError("raw run identity already exists")
        self.run_staging.mkdir()
        self.transactions.mkdir()
        self.executions.mkdir()
        _fsync_directory(self.raw_root)

    def write_execution(
        self,
        metadata: RawExecutionMetadata,
        *,
        result_rows: tuple[dict[str, Any], ...],
        resource_row: dict[str, Any],
    ) -> Path:
        metadata.validate()
        if metadata.envelope_hash != self.envelope_hash:
            raise ValueError("execution envelope hash differs from raw run")
        if metadata.source_git_sha != self.source_git_sha:
            raise ValueError("execution source SHA differs from raw run")
        if metadata.record_count != len(result_rows):
            raise ValueError("metadata and result-row count differ")
        transaction = self.transactions / f"{metadata.execution_id}.tmp"
        destination = self.executions / metadata.execution_id
        if transaction.exists() or destination.exists():
            raise FileExistsError("duplicate execution identity")
        transaction.mkdir()
        payloads = {
            "metadata.json": _json_bytes(metadata.state_dict()),
            "results.jsonl": _jsonl_bytes(result_rows),
            "resource.json": _json_bytes(resource_row),
        }
        for name, payload in payloads.items():
            _write_file(transaction / name, payload)
        checksums = {
            name: _sha256_file(transaction / name) for name in sorted(payloads)
        }
        _write_file(transaction / "checksums.json", _json_bytes(checksums))
        _write_file(
            transaction / "COMPLETE",
            _json_bytes(
                {
                    "execution_id": metadata.execution_id,
                    "state": "COMPLETE",
                }
            ),
        )
        _fsync_directory(transaction)
        os.replace(transaction, destination)
        _fsync_directory(self.transactions)
        _fsync_directory(self.executions)
        return destination

    def _verify_execution(self, path: Path) -> tuple[RawExecutionMetadata, str]:
        names = tuple(sorted(row.name for row in path.iterdir()))
        if names != tuple(sorted(_REQUIRED_EXECUTION_FILES)):
            raise RuntimeError(f"incomplete execution directory: {path.name}")
        metadata = RawExecutionMetadata(
            **json.loads((path / "metadata.json").read_text(encoding="utf-8"))
        )
        metadata.validate()
        if metadata.execution_id != path.name:
            raise RuntimeError("execution directory name and metadata ID differ")
        checksums = json.loads((path / "checksums.json").read_text(encoding="utf-8"))
        for name in ("metadata.json", "results.jsonl", "resource.json"):
            if checksums.get(name) != _sha256_file(path / name):
                raise RuntimeError(f"execution checksum mismatch: {path.name}/{name}")
        return metadata, _sha256_file(path / "checksums.json")

    def finalize(self) -> RawRunCommit:
        if any(self.transactions.iterdir()):
            raise RuntimeError("orphan execution transactions block raw commit")
        execution_paths = tuple(
            sorted(row for row in self.executions.iterdir() if row.is_dir())
        )
        if len(execution_paths) != self.expected_execution_count:
            raise RuntimeError("raw execution count differs from frozen expectation")
        metadata_rows: list[RawExecutionMetadata] = []
        execution_checksums: dict[str, str] = {}
        result_chunks: list[bytes] = []
        resource_rows: list[dict[str, Any]] = []
        for path in execution_paths:
            metadata, checksum = self._verify_execution(path)
            metadata_rows.append(metadata)
            execution_checksums[metadata.execution_id] = checksum
            result_chunks.append((path / "results.jsonl").read_bytes())
            resource_rows.append(
                json.loads((path / "resource.json").read_text(encoding="utf-8"))
            )
        evidence_record_count = sum(row.record_count for row in metadata_rows)
        if evidence_record_count != self.expected_evidence_record_count:
            raise RuntimeError("raw evidence-record count differs from frozen expectation")
        resource_record_count = sum(row.resource_record_count for row in metadata_rows)
        if resource_record_count != self.expected_execution_count:
            raise RuntimeError("raw resource-record count differs from frozen expectation")

        # The transaction namespace is working state and must never enter the
        # immutable raw evidence directory, even when it is empty.
        self.transactions.rmdir()
        _write_file(self.run_staging / "results.jsonl", b"".join(result_chunks))
        _write_file(self.run_staging / "resources.jsonl", _jsonl_bytes(resource_rows))
        commit = RawRunCommit(
            raw_store_version=_RAW_STORE_VERSION,
            run_id=self.run_id,
            envelope_hash=self.envelope_hash,
            source_git_sha=self.source_git_sha,
            execution_count=len(metadata_rows),
            evidence_record_count=evidence_record_count,
            resource_record_count=resource_record_count,
            execution_ids=tuple(row.execution_id for row in metadata_rows),
            execution_checksums=execution_checksums,
        )
        _write_file(self.run_staging / "raw_manifest.json", _json_bytes(commit.state_dict()))
        top_checksums = {
            name: _sha256_file(self.run_staging / name)
            for name in ("raw_manifest.json", "resources.jsonl", "results.jsonl")
        }
        _write_file(self.run_staging / "checksums.json", _json_bytes(top_checksums))
        _write_file(
            self.run_staging / "RAW_COMPLETE",
            _json_bytes(
                {
                    "commit_hash": commit.commit_hash(),
                    "run_id": self.run_id,
                    "state": "RAW_COMPLETE",
                }
            ),
        )
        _fsync_directory(self.run_staging)
        os.replace(self.run_staging, self.final_root)
        _fsync_directory(self.raw_root)
        _make_read_only(self.final_root)
        return commit

    def abort(self, *, preserve_partial: bool = True) -> Path | None:
        if not self.run_staging.exists():
            return None
        if not preserve_partial:
            shutil.rmtree(self.run_staging)
            return None
        failure_root = self.raw_root / f"{self.run_id}.FAILED"
        if failure_root.exists():
            raise FileExistsError("raw failure directory already exists")
        _write_file(
            self.run_staging / "FAILED",
            _json_bytes({"run_id": self.run_id, "state": "FAILED"}),
        )
        os.replace(self.run_staging, failure_root)
        _fsync_directory(self.raw_root)
        _make_read_only(failure_root)
        return failure_root
