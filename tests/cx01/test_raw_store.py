from __future__ import annotations

import json
from pathlib import Path

import pytest

from sparkbrain.comparison.cx01.raw_store import FormalRawStore


def test_raw_store_retains_atomic_cells_and_locks_complete(tmp_path: Path) -> None:
    store = FormalRawStore(tmp_path, "formal-fixture")
    store.initialize()
    store.write_execution(0, {"value": 1})
    store.write_execution(1, {"value": 2})
    with pytest.raises(FileExistsError):
        store.write_execution(1, {"value": 3})
    rows = store.finalize(2)
    assert rows == ({"value": 1}, {"value": 2})
    assert store.read_finalized(2) == rows
    assert store.root.stat().st_mode & 0o222 == 0
    assert (store.root / "execution-000000").stat().st_mode & 0o222 == 0


def test_raw_store_detects_checksum_tamper(tmp_path: Path) -> None:
    store = FormalRawStore(tmp_path, "tamper-fixture")
    store.initialize()
    cell = store.write_execution(0, {"value": 1})
    result = cell / "result.json"
    result.chmod(0o644)
    result.write_text(json.dumps({"value": 999}) + "\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="checksum mismatch"):
        store.finalize(1)


def test_failure_marker_preserves_completed_count_and_closes_store(tmp_path: Path) -> None:
    store = FormalRawStore(tmp_path, "failure-fixture")
    store.initialize()
    store.write_execution(0, {"value": 1})
    marker = store.mark_failed(RuntimeError("forced failure"))
    payload = json.loads(marker.read_text(encoding="utf-8"))
    assert payload["completed_execution_count"] == 1
    assert payload["error_type"] == "RuntimeError"
    assert store.root.stat().st_mode & 0o222 == 0
    with pytest.raises(RuntimeError, match="closed"):
        store.write_execution(1, {"value": 2})
