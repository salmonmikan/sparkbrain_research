from __future__ import annotations

import hashlib
import json
import os
import shutil
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from .freeze import ExecutionSeal, FreezeManifest


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_run_atomic(
    root: Path,
    *,
    run_id: str,
    manifest: FreezeManifest,
    seal: ExecutionSeal,
    rows: Iterable[dict[str, Any]],
) -> Path:
    """Publish a complete CX01 run or publish nothing.

    Existing run directories are never replaced. Successful files are made
    read-only before the temporary directory is atomically renamed.
    """

    if not run_id or "/" in run_id or "\\" in run_id:
        raise ValueError("run_id must be a simple non-empty path component")
    manifest.validate()
    seal.validate()
    root.mkdir(parents=True, exist_ok=True)
    target = root / run_id
    temporary = root / f".{run_id}.tmp"
    if target.exists() or temporary.exists():
        raise FileExistsError("CX01 run identity already exists")
    temporary.mkdir()
    try:
        (temporary / "manifest.json").write_bytes(_canonical_bytes(manifest.state_dict()) + b"\n")
        (temporary / "seal.json").write_bytes(_canonical_bytes(seal.state_dict()) + b"\n")
        with (temporary / "results.jsonl").open("wb") as handle:
            for row in rows:
                handle.write(_canonical_bytes(row) + b"\n")
        checksums = {
            name: _sha256(temporary / name)
            for name in ("manifest.json", "seal.json", "results.jsonl")
        }
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
