from __future__ import annotations

import hashlib
import json
import os
import shutil
from pathlib import Path
from typing import Any


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_path(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


class FormalRawStore:
    """Append-only formal raw-evidence store with atomic execution cells."""

    def __init__(self, artifact_root: Path, run_id: str) -> None:
        if not run_id or "/" in run_id or "\\" in run_id:
            raise ValueError("run_id must be a simple non-empty path component")
        self.artifact_root = artifact_root
        self.run_id = run_id
        self.root = artifact_root / f"{run_id}.RAW"

    def initialize(self) -> None:
        self.artifact_root.mkdir(parents=True, exist_ok=True)
        if self.root.exists():
            raise RuntimeError("formal raw store already exists")
        self.root.mkdir()
        (self.root / "STATE.json").write_bytes(
            _canonical_bytes({"run_id": self.run_id, "state": "OPEN"}) + b"\n"
        )

    def _cell(self, index: int) -> Path:
        if index < 0:
            raise ValueError("formal execution index must be non-negative")
        return self.root / f"execution-{index:06d}"

    def write_execution(self, index: int, row: dict[str, Any]) -> Path:
        if not self.root.exists():
            raise RuntimeError("formal raw store is not initialized")
        if (self.root / "RAW_COMPLETE.json").exists() or (self.root / "RUN_FAILED.json").exists():
            raise RuntimeError("formal raw store is already closed")
        target = self._cell(index)
        temporary = self.root / f".{target.name}.tmp"
        if target.exists() or temporary.exists():
            raise FileExistsError("formal raw execution identity already exists")
        temporary.mkdir()
        try:
            result_bytes = _canonical_bytes(row) + b"\n"
            (temporary / "result.json").write_bytes(result_bytes)
            checksums = {"result.json": _sha256_bytes(result_bytes)}
            (temporary / "checksums.json").write_bytes(_canonical_bytes(checksums) + b"\n")
            (temporary / "COMPLETE").write_text("complete\n", encoding="utf-8")
            for path in temporary.iterdir():
                if path.is_file():
                    path.chmod(0o444)
            os.replace(temporary, target)
        except Exception:
            shutil.rmtree(temporary, ignore_errors=True)
            raise
        return target

    def completed_indices(self) -> tuple[int, ...]:
        if not self.root.exists():
            return ()
        indices: list[int] = []
        for path in self.root.glob("execution-*"):
            if not path.is_dir():
                continue
            try:
                indices.append(int(path.name.removeprefix("execution-")))
            except ValueError:
                continue
        return tuple(sorted(indices))

    def _verify_cell(self, index: int) -> dict[str, Any]:
        cell = self._cell(index)
        if not cell.is_dir() or not (cell / "COMPLETE").is_file():
            raise RuntimeError(f"formal raw execution {index} is incomplete")
        result_path = cell / "result.json"
        checksum_path = cell / "checksums.json"
        if not result_path.is_file() or not checksum_path.is_file():
            raise RuntimeError(f"formal raw execution {index} is missing files")
        checksums = json.loads(checksum_path.read_text(encoding="utf-8"))
        if checksums.get("result.json") != _sha256_path(result_path):
            raise RuntimeError(f"formal raw execution {index} checksum mismatch")
        row = json.loads(result_path.read_text(encoding="utf-8"))
        if not isinstance(row, dict):
            raise RuntimeError(f"formal raw execution {index} result must be an object")
        return row

    def finalize(self, expected_count: int) -> tuple[dict[str, Any], ...]:
        if expected_count < 1:
            raise ValueError("formal raw expected count must be positive")
        observed = self.completed_indices()
        expected = tuple(range(expected_count))
        if observed != expected:
            raise RuntimeError(
                f"formal raw matrix incomplete: observed={len(observed)} expected={expected_count}"
            )
        rows = tuple(self._verify_cell(index) for index in expected)
        aggregate_hash = _sha256_bytes(b"".join(_canonical_bytes(row) + b"\n" for row in rows))
        marker = {
            "aggregate_hash": aggregate_hash,
            "execution_count": expected_count,
            "run_id": self.run_id,
            "state": "RAW_COMPLETE",
        }
        complete_path = self.root / "RAW_COMPLETE.json"
        try:
            with complete_path.open("xb") as handle:
                handle.write(_canonical_bytes(marker) + b"\n")
        except FileExistsError as exc:
            raise RuntimeError("formal raw store was already finalized") from exc
        complete_path.chmod(0o444)
        (self.root / "STATE.json").chmod(0o444)
        self.root.chmod(0o555)
        return rows

    def mark_failed(self, exc: BaseException) -> Path:
        if not self.root.exists():
            raise RuntimeError("formal raw store is not initialized")
        marker = self.root / "RUN_FAILED.json"
        payload = {
            "completed_execution_count": len(self.completed_indices()),
            "error_message": str(exc),
            "error_type": type(exc).__name__,
            "run_id": self.run_id,
            "state": "FAILED",
        }
        try:
            with marker.open("xb") as handle:
                handle.write(_canonical_bytes(payload) + b"\n")
        except FileExistsError as marker_exc:
            raise RuntimeError("formal raw store already has a failure marker") from marker_exc
        marker.chmod(0o444)
        (self.root / "STATE.json").chmod(0o444)
        self.root.chmod(0o555)
        return marker
