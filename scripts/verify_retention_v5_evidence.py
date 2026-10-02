#!/usr/bin/env python3
"""Verify/extract pinned retention v5 bytes; no model import or study replay."""
from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import tarfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "artifacts/research/plasticity_retention_results_20261002"
ARCHIVE_SHA = "75bee0d8ce010af13049f684651623a3257a00359966852ea6f0517516bce55d"
INVENTORY_SHA = "898d222300213136ca590d8acc1c28f5bd79a6d7e453cd587ef572def6bc65a7"
FREEZE_SHA = "272ed83bd0a520d8fc80a6e54b6145eaae76333f8866cba0d780bae76746a0b9"
TERMINAL_SHA = "5b62860e7c17241c2136817c8f8915cf7099b2422507589277c2e1218d7c7a67"
AUTHORITY_PINS = {
    "review": "3a6c848a0d91bbccd9af96453a1b440ae1e463b247e8d387eb218c09d3899789",
    "publication": "49b7b54c1151366dbf992bd4b52f4357d731ac1227540a15e251a8b8845d8a6c",
    "approval": "7af778f61a311ad3ef405c64e267d2d4a99c997edf8524218276b5bc29347b3b",
}


def require(value: bool, message: str) -> None:
    if not value:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verified_members(
    package: Path = PACKAGE, *, check_current_sources: bool = False
) -> dict[str, bytes]:
    transport = json.loads((package / "transport_manifest.json").read_bytes())
    bindings = {
        "schema": "retention-v5-preservation-transport-1",
        "archive_format": "canonical normalized tar.xz",
        "archive_sha256": ARCHIVE_SHA,
        "archive_bytes": 1150200,
        "archive_files": 521,
        "raw_run_files": 315,
        "preservation_manifest_sha256": INVENTORY_SHA,
        "source_commit": "81088ae386cbc611fb9e6366d8ade1c2ea74b6b7",
        "execution_manifest_sha256": FREEZE_SHA,
        "terminal_sha256": TERMINAL_SHA,
        "scientific_credit": 0,
    }
    require(set(transport) == {*bindings, "parts"}, "transport metadata inventory")
    for key, value in bindings.items():
        require(
            type(transport[key]) is type(value) and transport[key] == value,
            "independent transport binding: " + key,
        )
    expected_parts = [f"evidence-{i:03d}.b64" for i in range(24)]
    require([p["path"] for p in transport["parts"]] == expected_parts, "part inventory")
    require(transport["archive_sha256"] == ARCHIVE_SHA, "independent archive pin")
    chunks = []
    for part in transport["parts"]:
        path = package / part["path"]
        require(not path.is_symlink(), "transport symlink")
        raw = path.read_bytes()
        require(sha(raw) == part["sha256"], "transport part hash")
        decoded = base64.b64decode(raw.strip(), validate=True)
        require(len(decoded) == part["decoded_bytes"], "transport part size")
        chunks.append(decoded)
    archive = b"".join(chunks)
    require(len(archive) == transport["archive_bytes"] == 1150200, "archive size")
    require(sha(archive) == ARCHIVE_SHA, "archive content hash")
    members = {}
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:xz") as tar:
        for member in tar:
            path = PurePosixPath(member.name)
            require(
                member.isfile() and not path.is_absolute() and ".." not in path.parts
                and path.as_posix() == member.name and member.name not in members,
                "unsafe or duplicate member",
            )
            stream = tar.extractfile(member)
            require(stream is not None, "missing member stream")
            members[member.name] = stream.read()
    require(len(members) == transport["archive_files"] == 521, "archive member count")
    inventory_raw = members["preservation-manifest.json"]
    require(sha(inventory_raw) == INVENTORY_SHA, "independent preservation inventory pin")
    inventory = json.loads(inventory_raw)
    require(set(inventory) == set(members) - {"preservation-manifest.json"}, "member inventory")
    require(all(sha(members[n]) == digest for n, digest in inventory.items()), "member hash")
    require(sha(members["freeze/manifest.json"]) == FREEZE_SHA, "execution freeze pin")
    require(sha(members["run/result.json"]) == TERMINAL_SHA, "terminal pin")
    frozen = json.loads(members["freeze/manifest.json"])
    for name, digest in frozen["sources"].items():
        require(sha(members["frozen-sources/" + name]) == digest, "frozen source hash")
        if check_current_sources:
            require(
                (ROOT / name).is_file() and sha((ROOT / name).read_bytes()) == digest,
                "current audit source mismatch",
            )
    require(len(frozen["sources"]) == 198, "source inventory size")
    for name, digest in frozen["generated"].items():
        require(sha(members["freeze/" + name]) == digest, "dependency file pin")
    for kind, pin in AUTHORITY_PINS.items():
        original = members["original-authority-records/" + kind + ".json"]
        require(sha(original) == pin, "independent original authority pin")
        require(original == members["run/authority-records/" + kind + ".json"], "authority copy")
    require(
        json.loads(members["original-authority-records/original-record-pins.json"])
        == AUTHORITY_PINS, "original authority pin inventory",
    )
    return members


def verify(
    package: Path = PACKAGE, extract: Path | None = None, *, check_current_sources: bool = False
) -> dict:
    members = verified_members(package, check_current_sources=check_current_sources)
    if extract is not None:
        require(not extract.exists() and not extract.is_symlink(), "extraction no clobber")
        extract.mkdir(parents=True, exist_ok=False)
        for name, raw in members.items():
            path = extract / name
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("xb") as stream:
                stream.write(raw)
    return {
        "status": "verified_preserved_bytes",
        "archive_sha256": ARCHIVE_SHA,
        "archive_files": len(members),
        "run_files": sum(n.startswith("run/") for n in members),
        "frozen_source_files": 198,
        "current_source_files_verified": 198 if check_current_sources else 0,
        "terminal_sha256": TERMINAL_SHA,
        "runtime_model_method_calls": 0,
        "scope": "byte/source preservation only; full retained-data audit is a separate command",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--extract", type=Path)
    parser.add_argument("--check-current-sources", action="store_true")
    args = parser.parse_args()
    result = verify(extract=args.extract, check_current_sources=args.check_current_sources)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
