"""Publication corruption checks; these never import or execute SparkBrain models."""

from __future__ import annotations

import base64
import gzip
import hashlib
import importlib.util
import io
import json
import shutil
import tarfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "artifacts/research/temporal_reuse_loop_20261001"
SPEC = importlib.util.spec_from_file_location(
    "verify_temporal", ROOT / "scripts/verify_temporal_reuse_evidence.py"
)
assert SPEC is not None and SPEC.loader is not None
verifier = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verifier)


def test_complete_transport_and_arithmetic() -> None:
    result = verifier.verify(DATA)
    assert result["archive_files"] == 241
    assert result["measured_suffix_rows"] == 640
    assert result["causal_fork_rows"] == 512


def test_corrupted_encoded_part_is_rejected(tmp_path: Path) -> None:
    shutil.copytree(DATA, tmp_path / "copy")
    part = tmp_path / "copy/evidence.part000.b64"
    original = part.read_bytes()
    part.write_bytes(b"A" + original[1:])
    assert part.read_bytes() != original
    with pytest.raises(ValueError, match="encoded part mismatch"):
        verifier.verify(tmp_path / "copy")


def test_rehashed_false_metric_is_rejected(tmp_path: Path) -> None:
    transport = json.loads((DATA / "transport_manifest.json").read_text())
    archive = b"".join(
        base64.b64decode((DATA / p["path"]).read_bytes()) for p in transport["parts"]
    )
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as tar:
        values = {row.name: tar.extractfile(row).read() for row in tar.getmembers()}
    report = json.loads(values["run/report.json"])
    report["seeds"]["910071"]["arms"]["S"]["return"]["brier"] = 0.0
    changed = (json.dumps(report, sort_keys=True) + "\n").encode()
    values["run/report.json"] = changed
    manifest = json.loads(values["ARCHIVE_MANIFEST.json"])
    manifest["files"]["run/report.json"] = {
        "bytes": len(changed),
        "sha256": hashlib.sha256(changed).hexdigest(),
    }
    values["ARCHIVE_MANIFEST.json"] = json.dumps(manifest).encode()
    output = io.BytesIO()
    with gzip.GzipFile(fileobj=output, mode="wb", mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode="w") as tar:
            for name, value in sorted(values.items()):
                info = tarfile.TarInfo(name)
                info.size = len(value)
                tar.addfile(info, io.BytesIO(value))
    altered = output.getvalue()
    encoded = base64.encodebytes(altered)
    (tmp_path / "one.b64").write_bytes(encoded)
    transport.update(
        archive_bytes=len(altered),
        archive_sha256=hashlib.sha256(altered).hexdigest(),
        parts=[
            {
                "path": "one.b64",
                "bytes": len(altered),
                "sha256": hashlib.sha256(altered).hexdigest(),
                "encoded_sha256": hashlib.sha256(encoded).hexdigest(),
            }
        ],
    )
    (tmp_path / "transport_manifest.json").write_text(json.dumps(transport))
    with pytest.raises(ValueError, match="910071/S/brier"):
        verifier.verify(tmp_path)
