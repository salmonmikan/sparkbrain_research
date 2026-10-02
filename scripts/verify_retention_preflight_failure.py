#!/usr/bin/env python3
"""Data-only verification/repacking of the preserved pre-model retention failure."""

from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import io
import json
import tarfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/research/plasticity_retention_preflight_failure_20261002"
ARCHIVE_SHA = "407a1d81cf2161e32c93be57c2eecabba54d178a3bcd0fd723606aaf6d2b57b6"
RESULT_SHA = "70a54d6f1c6b23809853e14901561bbda4aede73a885422e55a7ab6964caf223"
FREEZE_SHA = "cc4dffcea78d8d82d3f5a6fc42d5474e97387b0dbcbab0377c9895233cb41834"
SOURCE = "2977aefc06d80291bb65c36b4b3bac0499084d0f"


def require(value: bool, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_archive(files: dict[str, bytes]) -> bytes:
    content = io.BytesIO()
    with tarfile.open(fileobj=content, mode="w", format=tarfile.PAX_FORMAT) as archive:
        for name, raw in sorted(files.items()):
            entry = tarfile.TarInfo(name)
            entry.size, entry.mtime, entry.mode = len(raw), 0, 0o644
            entry.uid = entry.gid = 0
            entry.uname = entry.gname = ""
            archive.addfile(entry, io.BytesIO(raw))
    compressed = io.BytesIO()
    with gzip.GzipFile(
        fileobj=compressed, mode="wb", filename="", mtime=0, compresslevel=9
    ) as stream:
        stream.write(content.getvalue())
    return compressed.getvalue()


def verify(directory: Path) -> dict:
    manifest = json.loads((directory / "transport_manifest.json").read_text())
    require(
        manifest["source_commit"] == SOURCE and manifest["archive_sha256"] == ARCHIVE_SHA,
        "independent source/archive pin",
    )
    chunks = []
    for index, part in enumerate(manifest["parts"]):
        require(part["path"] == f"evidence.part{index:03d}.b64", "part order/name")
        raw = (directory / part["path"]).read_bytes()
        require(
            len(raw) == part["encoded_bytes"] and digest(raw) == part["encoded_sha256"],
            "encoded part binding",
        )
        decoded = base64.b64decode(b"".join(raw.split()), validate=True)
        require(
            len(decoded) == part["decoded_bytes"] and digest(decoded) == part["decoded_sha256"],
            "decoded part binding",
        )
        chunks.append(decoded)
    raw = b"".join(chunks)
    require(
        len(raw) == manifest["archive_bytes"] and digest(raw) == ARCHIVE_SHA,
        "independent archive digest",
    )
    files = {}
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as archive:
        for entry in archive.getmembers():
            path = PurePosixPath(entry.name)
            require(
                entry.isfile()
                and not path.is_absolute()
                and ".." not in path.parts
                and entry.name not in files,
                "archive member inventory",
            )
            stream = archive.extractfile(entry)
            require(stream is not None, "missing archive member")
            files[entry.name] = stream.read()
    require(
        len(files) == manifest["archive_files"] == 204 and set(files) == set(manifest["files"]),
        "full archive inventory",
    )
    for name, data in files.items():
        require(
            manifest["files"][name] == {"sha256": digest(data), "bytes": len(data)},
            "archive member digest",
        )
    require(canonical_archive(files) == raw, "canonical repack differs from retained bytes")
    require(digest(files["run/result.json"]) == RESULT_SHA, "independent terminal pin")
    result = json.loads(files["run/result.json"])
    require(
        result["status"] == "failed"
        and result["reserved_pairs"] == 0
        and result["jobs_completed"] == 0
        and result["job_costs"] == [],
        "failed-admission result",
    )
    freeze_path = "source/artifacts/research/plasticity_retention_execution_20261001/freeze-v3/"
    require(digest(files[freeze_path + "manifest.json"]) == FREEZE_SHA, "original freeze pin")
    frozen = json.loads(files[freeze_path + "manifest.json"])
    require(len(frozen["sources"]) == 193, "original source inventory")
    for name, pin in frozen["sources"].items():
        require(digest(files["source/" + name]) == pin, "frozen source member mismatch")
    for name, pin in frozen["generated"].items():
        require(digest(files[freeze_path + name]) == pin, "frozen generated member mismatch")
    direct = {
        "result.json": "run/result.json",
        "invocation.json": "invocation.json",
        "independent_audit.json": "audit/audit.json",
        "independent_audit.md": "audit/report.md",
        "source_preservation_manifest.json": "preservation-manifest.json",
    }
    for name in ("review", "publication", "approval", "original-record-pins"):
        direct[f"authority-records/{name}.json"] = f"authority-records/{name}.json"
    for name, member in direct.items():
        require((directory / name).read_bytes() == files[member], "direct evidence copy differs")
    expected = {"transport_manifest.json", *direct, *(p["path"] for p in manifest["parts"])}
    actual = {str(p.relative_to(directory)) for p in directory.rglob("*") if p.is_file()}
    require(actual == expected, "publication file inventory")
    return {
        "archive_sha256": ARCHIVE_SHA,
        "archive_files": len(files),
        "archive_bytes": len(raw),
        "source_files_verified": 193,
        "canonical_repack_matches": True,
        "retained_terminal_sha256": RESULT_SHA,
        "runtime_model_method_calls": 0,
        "scope": "byte/preservation audit only; no replay or independent process attestation",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-dir", type=Path, default=ARTIFACT)
    args = parser.parse_args()
    print(json.dumps(verify(args.artifact_dir), sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
