#!/usr/bin/env python3
"""Repackage retained compatibility data deterministically; never run the model."""
from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import io
import json
import subprocess
import tarfile
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ANCHOR_STATUS = (
    "post-execution integrity binding of unchanged first/only diagnostic output; "
    "no rerun or independent scientific replicate"
)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def formatted(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def read_raw(root: Path) -> dict[str, bytes]:
    if not root.is_dir() or root.is_symlink():
        raise ValueError("raw input must be an ordinary directory")
    files = {}
    for path in root.rglob("*"):
        if path.is_symlink() or not (path.is_file() or path.is_dir()):
            raise ValueError("raw input contains a non-regular entry")
        if path.is_file():
            files[path.relative_to(root).as_posix()] = path.read_bytes()
    return files


def verifier() -> Any:
    source = ROOT / "scripts/verify_m1_checkpoint_compatibility_artifacts.py"
    spec = importlib.util.spec_from_file_location("compatibility_transport_reader", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("data-only transport reader is unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_published(root: Path) -> dict[str, bytes]:
    return verifier().read_bundle(root)


def git_bytes(root: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=root)


def validate_source(files: dict[str, bytes], git_root: Path | None) -> dict[str, Any]:
    # This command republishes one exhausted allocation, never arbitrary new data.
    # The verifier pins the external anchor digest independently of raw inventory.
    anchor = verifier().anchors()
    if {name: sha(raw) for name, raw in files.items()} != anchor["raw_files_sha256"]:
        raise ValueError("raw files do not match the frozen external evidence anchor")
    if {name: sha(raw) for name, raw in files.items() if name != "inventory.json"} != json.loads(
            files["inventory.json"]):
        raise ValueError("raw inventory mismatch")
    started = json.loads(files["STARTED.json"])
    source = started["source_commit"]
    if (not isinstance(source, str) or len(source) != 40
            or any(char not in "0123456789abcdef" for char in source)):
        raise ValueError("source commit must be an exact lowercase Git SHA")
    if git_root is None:
        return started
    tree = git_bytes(git_root, "rev-parse", source + "^{tree}").decode().strip()
    if tree != started["source_tree"]:
        raise ValueError("source tree does not match retained provenance")
    for prefix, key in (("src/sparkbrain", "runtime_source_files_sha256"),
                        ("schemas", "schema_assets_sha256")):
        listing = git_bytes(git_root, "ls-tree", "-r", "--name-only", source, prefix)
        names = listing.decode().splitlines()
        expected = {name: sha(git_bytes(git_root, "show", f"{source}:{name}")) for name in names}
        if expected != started[key]:
            raise ValueError(f"complete pinned Git source manifest mismatch: {prefix}")
    bindings = (
        ("scripts/m1_checkpoint_compatibility_diagnostic.py", "runner_sha256", None),
        ("protocols/m1_checkpoint_compatibility_v1.json", "protocol_sha256", "protocol.json"),
        ("protocols/m1_checkpoint_compatibility_inputs_v1.json", "inputs_sha256", "inputs.json"),
    )
    for path, key, retained in bindings:
        raw = git_bytes(git_root, "show", f"{source}:{path}")
        if sha(raw) != started[key] or (retained is not None and raw != files[retained]):
            raise ValueError(f"pinned execution input/source mismatch: {path}")
    return started


def build_package(files: dict[str, bytes], git_root: Path | None = None) -> dict[str, bytes]:
    started = validate_source(files, git_root)
    output = io.BytesIO()
    with tarfile.open(fileobj=output, mode="w:xz", format=tarfile.PAX_FORMAT) as archive:
        # The original generator sorted Path objects, hence component-wise order.
        # Plain string order differs for e.g. setup/... versus setup.stderr.
        for name in sorted(files, key=lambda value: PurePosixPath(value).parts):
            path = PurePosixPath(name)
            if path.is_absolute() or ".." in path.parts or path.as_posix() != name:
                raise ValueError("unsafe/noncanonical archive member path")
            raw = files[name]
            info = tarfile.TarInfo(name)
            info.size, info.mtime, info.mode = len(raw), 0, 0o644
            info.uid, info.gid, info.uname, info.gname = 0, 0, "", ""
            archive.addfile(info, io.BytesIO(raw))
    payload = output.getvalue()
    result = {"run.tar.xz": payload}
    parts = []
    for index, offset in enumerate(range(0, len(payload), 49152)):
        name = f"part-{index:03d}.b64"
        raw = base64.b64encode(payload[offset:offset + 49152]) + b"\n"
        result["run.parts/" + name] = raw
        parts.append({"path": name, "sha256": sha(raw)})
    result["run.parts/manifest.json"] = formatted({
        "archive_bytes": len(payload), "archive_sha256": sha(payload), "parts": parts})
    result["anchors.json"] = formatted({
        "schema_version": 1, "archive_sha256": sha(payload), "archive_bytes": len(payload),
        "raw_files_sha256": {name: sha(raw) for name, raw in files.items()},
        "execution_provenance": {key: value for key, value in started.items() if key != "command"},
        "classification": "EXPLORATORY_NONCANONICAL_NON_EVIDENTIARY",
        "scientific_credit": 0, "anchor_status": ANCHOR_STATUS,
    })
    return result


def write_package(
    files: dict[str, bytes], output: Path, git_root: Path | None = None,
) -> dict[str, Any]:
    if output.exists() or output.is_symlink():
        raise FileExistsError("packaging output must be absent; no clobber")
    # Write the checked canonical path: mkdir on an unresolved a/new/../ spelling
    # can create the intermediate directory even when the final destination is elsewhere.
    output = output.resolve()
    if output.exists():
        raise FileExistsError("packaging output must be absent; no clobber")
    package = build_package(files, git_root)
    output.mkdir(parents=True, exist_ok=False)
    for name, raw in package.items():
        path = output / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as stream:
            stream.write(raw)
    return {"archive_bytes": len(package["run.tar.xz"]),
            "archive_sha256": sha(package["run.tar.xz"]),
            "anchors_sha256": sha(package["anchors.json"]),
            "raw_files": len(files), "model_executed": False}


def require_disjoint_paths(input_root: Path, output: Path) -> None:
    source = input_root.resolve()
    destination = output.resolve()
    if destination.is_relative_to(source) or source.is_relative_to(destination):
        raise ValueError("packaging input and output must not overlap")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument("--raw", type=Path, help="existing raw output; never generated here")
    inputs.add_argument("--published", type=Path, help="existing committed artifact directory")
    parser.add_argument("--git-root", type=Path,
                        help="optional additional source-object audit in a full-history checkout")
    parser.add_argument("--output", type=Path, required=True, help="new absent packaging directory")
    args = parser.parse_args()
    require_disjoint_paths(args.raw if args.raw else args.published, args.output)
    if args.output.exists() or args.output.is_symlink():
        raise FileExistsError("packaging output must be absent; no clobber")
    files = read_raw(args.raw) if args.raw else read_published(args.published)
    print(json.dumps(write_package(files, args.output, args.git_root), sort_keys=True))


if __name__ == "__main__":
    main()
