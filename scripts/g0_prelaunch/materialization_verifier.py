#!/usr/bin/env python3
"""Independent, model-free materialization checker; never launches or authorizes G0.

Use a separately trusted Python with -I -S -B, outside the candidate tree.
The CLI emits observations, never an approval or the legacy v1 attestation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import stat
import sys
from pathlib import Path
from typing import Any

VERSION = "g0-external-materialization-verifier-3.0.1"
BASELINE_COMMIT = "16dba8f28a88134c57603d4f0c90d2edc39e4e49"
BASELINE_TREE = "cbb897ed74a1f0b9f40c77e534c794dc82c7a962"
BASELINE_FILES = 1323
# Filled from the reviewed, source-only inventory shipped with this implementation.
BASELINE_INVENTORY_SHA256 = "1dbe162e7b015193c9de9f8c25b1363b889feb9e1fb6d7f5b5e28f9289ee343f"
MAX_JSON_BYTES = 64 * 1024 * 1024
MAX_FILES = 200_000
MAX_BYTES = 4 * 1024 * 1024 * 1024
MAX_FILE_BYTES = 512 * 1024 * 1024
MAX_DEPTH = 64
MAX_DYNAMIC_BYTES = 64 * 1024
MODULE = "scripts.launch_g0_v3_eligibility"
IDENTITY = "assembly-m1-g0-v3-20261003"
APPROVAL_RELATIVE = (
    "artifacts/research/assembly_m1_g0_v3_20261003/independent-execution-approval.json"
)
SLOTS = {
    "approval_raw_sha256": "--approval-sha256",
    "approval_canonical_sha256": "--approval-object-sha256",
}
ENV_KEYS = frozenset({"LANG", "LC_ALL", "TZ", "PYTHONPATH", "PYTHONDONTWRITEBYTECODE"})
FILE_KEYS = frozenset({"path", "mode", "size", "sha256", "git_blob_sha1"})


class Rejected(ValueError):
    """The proposed source/environment does not meet the closed contract."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Rejected(message)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
    ).encode("ascii")


def target_approval_canonical(value: Any) -> bytes:
    """Published support.canonical contract is sorted compact ASCII JSON plus LF."""
    return canonical(value) + b"\n"


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def hex_digest(value: Any, width: int, label: str) -> str:
    require(
        type(value) is str and re.fullmatch(f"[0-9a-f]{{{width}}}", value) is not None,
        f"invalid {label}",
    )
    return value


def exact_keys(value: Any, keys: set[str] | frozenset[str], label: str) -> None:
    require(type(value) is dict and set(value) == keys, f"invalid {label} fields")


def relative(value: Any) -> str:
    require(type(value) is str and bool(value) and len(value) <= 4096, "invalid relative path")
    parts = value.split("/")
    require(
        not value.startswith("/")
        and "\\" not in value
        and all(p not in {"", ".", ".."} for p in parts)
        and all(ord(c) >= 32 and ord(c) != 127 for c in value)
        and len(parts) <= MAX_DEPTH,
        "noncanonical relative path",
    )
    return value


def absolute(value: Any) -> Path:
    require(
        type(value) is str and value.startswith("/") and value != "/" and len(value) <= 4096,
        "absolute canonical path required",
    )
    require(
        value == os.path.normpath(value)
        and "\\" not in value
        and all(ord(c) >= 32 and ord(c) != 127 for c in value),
        "noncanonical absolute path",
    )
    # lstat every component, including ancestors: resolve() alone would hide aliases.
    path = Path(value)
    for item in reversed((path, *path.parents)):
        require(not stat.S_ISLNK(item.lstat().st_mode), f"symlink path: {item}")
    return path


def regular(path: Path, *, private_data: bool = False) -> os.stat_result:
    info = path.lstat()
    require(stat.S_ISREG(info.st_mode), f"not a regular file: {path}")
    require(info.st_nlink == 1, f"hardlink/alias file: {path}")
    allowed_modes = {0o600, 0o644} if private_data else {0o644, 0o755}
    require(stat.S_IMODE(info.st_mode) in allowed_modes, f"unsafe file mode: {path}")
    require(info.st_size <= MAX_FILE_BYTES, f"file too large: {path}")
    return info


def no_duplicate_pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        require(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def finite_float(value: str) -> float:
    result = float(value)
    require(math.isfinite(result), "nonfinite JSON float")
    return result


def decode_json(raw: bytes) -> Any:
    require(len(raw) <= MAX_JSON_BYTES, "JSON input too large")
    try:
        return json.loads(
            raw,
            object_pairs_hook=no_duplicate_pairs,
            parse_float=finite_float,
            parse_constant=lambda _: (_ for _ in ()).throw(Rejected("nonfinite JSON")),
        )
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise Rejected(f"invalid JSON: {exc}") from exc


def read_json(path: Path, expected_sha256: str | None = None) -> Any:
    absolute(str(path))
    info = regular(path, private_data=True)
    require(info.st_size <= MAX_JSON_BYTES, "JSON input too large")
    raw = path.read_bytes()
    if expected_sha256 is not None:
        hex_digest(expected_sha256, 64, "externally supplied binding digest")
        require(sha256(raw) == expected_sha256, "raw binding digest mismatch")
    return decode_json(raw)


def file_record(path: Path, name: str) -> dict[str, Any]:
    info = regular(path)
    digest = hashlib.sha256()
    blob = hashlib.sha1(b"blob " + str(info.st_size).encode("ascii") + b"\0")
    count = 0
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            count += len(chunk)
            require(count <= MAX_FILE_BYTES, "file grew beyond bound")
            digest.update(chunk)
            blob.update(chunk)
    require(count == info.st_size, "file changed while scanning")
    return {
        "path": name,
        "mode": "100755" if stat.S_IMODE(info.st_mode) == 0o755 else "100644",
        "size": count,
        "sha256": digest.hexdigest(),
        "git_blob_sha1": blob.hexdigest(),
    }


def validate_inventory(records: Any) -> dict[str, dict[str, Any]]:
    require(type(records) is list and 0 < len(records) <= MAX_FILES, "invalid file inventory")
    result: dict[str, dict[str, Any]] = {}
    total = 0
    for record in records:
        exact_keys(record, FILE_KEYS, "file inventory")
        path = relative(record["path"])
        require(path not in result, "duplicate inventory path")
        require(record["mode"] in {"100644", "100755"}, "unsupported Git mode")
        require(
            type(record["size"]) is int and 0 <= record["size"] <= MAX_FILE_BYTES,
            "invalid inventory file size",
        )
        hex_digest(record["sha256"], 64, "file sha256")
        hex_digest(record["git_blob_sha1"], 40, "Git blob SHA-1")
        total += record["size"]
        require(total <= MAX_BYTES, "inventory exceeds byte bound")
        result[path] = record
    # Reject file/directory conflicts, including an implicit namespace path.
    for path in result:
        require(
            not any(str(p) in result for p in Path(path).parents if str(p) != "."),
            "inventory file/directory collision",
        )
    return result


def git_tree_sha1(records: list[dict[str, Any]]) -> str:
    table = validate_inventory(records)
    tree: dict[str, Any] = {}
    for name, record in table.items():
        node = tree
        parts = name.split("/")
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = (record["mode"], record["git_blob_sha1"])

    def hash_tree(node: dict[str, Any]) -> str:
        payload = bytearray()
        # Git compares tree names as if a slash followed the directory name.
        for name, child in sorted(
            node.items(), key=lambda p: p[0].encode("utf-8") + (b"/" if type(p[1]) is dict else b"")
        ):
            mode, oid = ("40000", hash_tree(child)) if type(child) is dict else child
            payload.extend(
                mode.encode("ascii") + b" " + name.encode("utf-8") + b"\0" + bytes.fromhex(oid)
            )
        return hashlib.sha1(
            b"tree " + str(len(payload)).encode("ascii") + b"\0" + payload
        ).hexdigest()

    return hash_tree(tree)


def expected_directories(names: set[str]) -> set[str]:
    return {str(parent) for name in names for parent in Path(name).parents if str(parent) != "."}


def dynamic_specs(value: Any, published: set[str]) -> dict[str, dict[str, Any]]:
    require(type(value) is list and len(value) <= 1, "invalid dynamic data exceptions")
    result: dict[str, dict[str, Any]] = {}
    dirs = expected_directories(published)
    for item in value:
        exact_keys(item, {"path", "purpose", "maximum_bytes"}, "dynamic data exception")
        name = relative(item["path"])
        require(
            name not in published
            and name not in result
            and name == APPROVAL_RELATIVE
            and item["purpose"] == "independently-pinned-approval-data"
            and type(item["maximum_bytes"]) is int
            and 0 < item["maximum_bytes"] <= MAX_DYNAMIC_BYTES,
            "invalid dynamic approval-data exception",
        )
        parent = str(Path(name).parent)
        require(parent == "." or parent in dirs, "dynamic data cannot create namespace directories")
        result[name] = item
    return result


def verify_directory(
    root: Path,
    records: list[dict[str, Any]],
    exceptions: list[dict[str, Any]] | None = None,
    *,
    excluded_subtrees: list[str] | None = None,
) -> dict[str, Any]:
    absolute(str(root))
    require(root.is_dir(), "inventory root is not a directory")
    expected = validate_inventory(records)
    dynamic = dynamic_specs(exceptions or [], set(expected))
    excluded = excluded_subtrees or []
    require(
        type(excluded) is list
        and len(excluded) <= 2
        and all(item in {"site-packages", "dist-packages"} for item in excluded)
        and len(set(excluded)) == len(excluded),
        "invalid inactive stdlib exclusions",
    )
    require(
        not any(
            name == item or name.startswith(item + "/") for name in expected for item in excluded
        ),
        "excluded subtree cannot also be inventoried",
    )
    if excluded:
        require(
            {"site.py", "runpy.py"} <= set(expected),
            "only a stdlib inventory may exclude inactive packages",
        )
    dirs = expected_directories(set(expected))
    found: set[str] = set()
    found_dirs: set[str] = set()
    nodes, total = 0, 0
    stack = [(root, 0)]
    seen_inodes: set[tuple[int, int]] = set()
    while stack:
        current, depth = stack.pop()
        require(depth <= MAX_DEPTH, "scan depth exceeded")
        info = current.lstat()
        require(stat.S_ISDIR(info.st_mode), f"non-directory in scan: {current}")
        require(not (stat.S_IMODE(info.st_mode) & 0o022), f"writable shared directory: {current}")
        key = (info.st_dev, info.st_ino)
        require(key not in seen_inodes, "directory inode alias")
        seen_inodes.add(key)
        with os.scandir(current) as entries:
            for entry in entries:
                nodes += 1
                require(nodes <= MAX_FILES * 2, "scan node bound exceeded")
                path = Path(entry.path)
                name = relative(path.relative_to(root).as_posix())
                info = entry.stat(follow_symlinks=False)
                require(not stat.S_ISLNK(info.st_mode), f"symlink in inventory: {name}")
                if name in excluded:
                    require(
                        stat.S_ISDIR(info.st_mode) and not (stat.S_IMODE(info.st_mode) & 0o022),
                        "inactive stdlib exclusion must be a non-writable real directory",
                    )
                    continue
                if stat.S_ISDIR(info.st_mode):
                    require(name in dirs, f"undeclared directory/namespace: {name}")
                    found_dirs.add(name)
                    stack.append((path, depth + 1))
                elif name in dynamic:
                    regular(path, private_data=True)
                    require(
                        stat.S_IMODE(info.st_mode) in {0o600, 0o644}, "dynamic data is executable"
                    )
                    require(
                        info.st_size <= dynamic[name]["maximum_bytes"],
                        "dynamic approval data too large",
                    )
                    require(
                        type(read_json(path)) is dict, "dynamic approval data must be a JSON object"
                    )
                else:
                    require(name in expected, f"undeclared file/importable: {name}")
                    require(
                        file_record(path, name) == expected[name],
                        f"file content/mode differs: {name}",
                    )
                    found.add(name)
                    total += info.st_size
                    require(total <= MAX_BYTES, "scan byte bound exceeded")
    require(found == set(expected), f"missing published files: {sorted(set(expected) - found)[:5]}")
    require(found_dirs == dirs, "directory inventory differs")
    return {
        "files": len(found),
        "bytes": total,
        "inventory_sha256": sha256(canonical(records)),
        "dynamic_data_exceptions": sorted(dynamic),
    }


def verify_venv_configuration(raw: bytes, path: Path) -> None:
    """Validate the same hashed configuration buffer, without running its Python."""
    require(len(raw) <= MAX_DYNAMIC_BYTES, "venv configuration too large")
    try:
        text = raw.decode("utf-8")
    except UnicodeError as exc:
        raise Rejected("venv configuration is not UTF-8") from exc
    values: dict[str, str] = {}
    for line in text.splitlines():
        if not line.strip():
            continue
        require("=" in line, "malformed pyvenv configuration")
        key, value = (part.strip() for part in line.split("=", 1))
        key = key.lower()
        require(key not in values, "duplicate pyvenv configuration key")
        values[key] = value
    require(
        values.get("include-system-site-packages", "").lower() == "false",
        "venv system-site-packages must be explicitly disabled",
    )
    require("home" in values and absolute(values["home"]).is_dir(), "venv home must be canonical")
    require(path.name == "pyvenv.cfg", "unexpected venv configuration basename")


def reject_startup_hooks(
    root: Path, records: list[dict[str, Any]], *, allow_runtime_bytecode: bool = False
) -> None:
    for record in records:
        path = record["path"]
        parts = path.split("/")
        name = parts[-1]
        require(
            not name.endswith((".pth", "._pth", ".egg-link"))
            and name != "pyvenv.cfg"
            and not any(p.split(".")[0] in {"sitecustomize", "usercustomize"} for p in parts),
            f"startup hook/config not permitted in import tree: {root}/{path}",
        )
        require(
            not name.endswith(".pyo")
            and (
                allow_runtime_bytecode
                or (not any(p == "__pycache__" for p in parts) and not name.endswith(".pyc"))
            ),
            f"bytecode not permitted: {root}/{path}",
        )


def import_names(
    root: Path,
    records: list[dict[str, Any]],
    relative_root: str = "",
    *,
    runtime_caches: bool = False,
) -> set[str]:
    prefix = relative_root + "/" if relative_root else ""
    result: set[str] = set()
    for record in records:
        name = record["path"]
        if not name.startswith(prefix):
            continue
        remainder = name[len(prefix) :]
        first = remainder.split("/")[0]
        if runtime_caches and first == "__pycache__":
            require(remainder.endswith(".pyc"), "runtime cache directory contains non-bytecode")
            continue
        if "/" in remainder:
            candidate = first  # no __init__ requirement: namespace directories count
        elif first.endswith((".py", ".pyc", ".pyo", ".so", ".pyd")):
            candidate = first.split(".")[0]  # includes ABI-tagged extension modules
        else:
            continue
        if candidate.isidentifier():
            result.add(candidate)
    return result


def verify_source_binding(source: Any) -> tuple[Path, list[dict[str, Any]]]:
    exact_keys(
        source,
        {
            "root",
            "published_commit",
            "published_tree",
            "publication_reference",
            "files",
            "dynamic_data_exceptions",
        },
        "source binding",
    )
    root = absolute(source["root"])
    hex_digest(source["published_commit"], 40, "published commit")
    hex_digest(source["published_tree"], 40, "published tree")
    require(
        type(source["publication_reference"]) is str
        and source["publication_reference"].startswith("https://"),
        "independent publication reference required",
    )
    records = source["files"]
    require(git_tree_sha1(records) == source["published_tree"], "reconstructed Git tree mismatch")
    verify_directory(root, records, source["dynamic_data_exceptions"])
    reject_startup_hooks(root, records)
    return root, records


def expected_arguments(binding: dict[str, Any]) -> list[Any]:
    return [
        "--run-reviewed",
        "--root",
        binding["source"]["root"],
        "--approval-sha256",
        {"slot": "approval_raw_sha256"},
        "--approval-object-sha256",
        {"slot": "approval_canonical_sha256"},
        "--published-commit",
        binding["source"]["published_commit"],
        "--source-inventory-sha256",
        binding["bindings"]["source_inventory_sha256"],
    ]


def make_launch_request(
    binding: dict[str, Any], overlay: dict[str, str] | None = None
) -> dict[str, Any]:
    """Pure typed command template, or exact digest-slot substitution; never exec."""
    runtime, source = binding["runtime"], binding["source"]
    arguments = binding["target_arguments"]
    if overlay is not None:
        exact_keys(overlay, set(SLOTS), "approval digest overlay")
        for key, value in overlay.items():
            hex_digest(value, 64, key)
        arguments = [overlay[arg["slot"]] if type(arg) is dict else arg for arg in arguments]
    # Preserve the published -B -s -m profile and venv/site semantics.
    # Before overlay argv contains typed objects and cannot be executed.
    command = [
        runtime["timeout_executable"],
        "--signal=KILL",
        "900s",
        runtime["interpreter"],
        "-B",
        "-s",
        "-m",
        MODULE,
        *arguments,
    ]
    return {
        "argv" if overlay is not None else "argv_template": command,
        "cwd": source["root"],
        "env": runtime["environment"],
    }


def verify_final(
    binding_path: Path, externally_trusted_sha256: str, request: Any
) -> dict[str, Any]:
    """Check an externally pinned proposal. Caller must supply trust and sequencing.

    A digest calculated by the same untrusted requester is NOT a trust anchor.
    The independent authority must authenticate it out-of-band and guarantee
    source/environment quiescence until termination. This function never execs.
    """
    binding = read_json(binding_path, externally_trusted_sha256)
    exact_keys(binding, {"schema", "source", "runtime", "target_arguments", "bindings"}, "binding")
    require(binding["schema"] == "g0-external-prelaunch-binding-v3", "binding schema differs")
    pins = binding["bindings"]
    exact_keys(
        pins,
        {
            "execution_object_sha256",
            "source_inventory_sha256",
            "environment_freeze_sha256",
            "runtime_origin_commit",
        },
        "execution bindings",
    )
    for key, value in pins.items():
        hex_digest(value, 40 if key.endswith("commit") else 64, key)
    root, source_records = verify_source_binding(binding["source"])
    runtime = binding["runtime"]
    exact_keys(
        runtime,
        {
            "interpreter",
            "timeout_executable",
            "import_roots",
            "repository_import_roots",
            "trusted_files",
            "startup_absent_paths",
            "absent_import_archives",
            "startup_search_path",
            "native_closure_review",
            "environment",
        },
        "runtime binding",
    )
    require(
        type(runtime["import_roots"]) is list and 0 < len(runtime["import_roots"]) <= 16,
        "invalid trusted import roots",
    )
    require(runtime["repository_import_roots"] == ["", "src"], "repository import paths differ")
    require(
        type(runtime["environment"]) is dict
        and set(runtime["environment"]) <= ENV_KEYS
        and all(type(v) is str and "\0" not in v for v in runtime["environment"].values()),
        "target environment must be an exact replacement without unbound Python/loader injection",
    )
    require(
        runtime["environment"].get("PYTHONPATH") == "src"
        and runtime["environment"].get("PYTHONDONTWRITEBYTECODE") == "1",
        "fixed startup environment differs",
    )
    require(
        canonical(binding["target_arguments"]) == canonical(expected_arguments(binding)),
        "fixed arguments/typed approval slots differ",
    )
    source_names = {record["path"] for record in source_records}
    require("scripts/launch_g0_v3_eligibility.py" in source_names, "fixed v3 wrapper missing")
    all_lists = [source_records]
    for entry in runtime["import_roots"]:
        exact_keys(entry, {"path", "files", "excluded_subtrees"}, "runtime import root")
        validate_inventory(entry["files"])
        all_lists.append(entry["files"])
    require(
        sum(len(rows) for rows in all_lists) <= MAX_FILES
        and sum(row["size"] for rows in all_lists for row in rows) <= MAX_BYTES,
        "aggregate inventory bound exceeded before runtime scan",
    )
    roots: list[Path] = []
    names: dict[str, str] = {
        name: "trusted-built-in" for name in {"sys", "builtins", "_imp", "_io", "marshal"}
    }
    total_files = len(source_records)
    total_bytes = sum(record["size"] for record in source_records)
    for entry in runtime["import_roots"]:
        exact_keys(entry, {"path", "files", "excluded_subtrees"}, "runtime import root")
        directory = absolute(entry["path"])
        require(
            directory != root and root not in directory.parents and directory not in root.parents,
            "runtime/source import roots overlap",
        )
        for previous in roots:
            require(previous != directory, "duplicate import root")
        # A stdlib/lib-dynload nested root is allowed only when it is also exactly
        # covered by the enclosing inventory. Duplicate import names still reject.
        verify_directory(directory, entry["files"], excluded_subtrees=entry["excluded_subtrees"])
        reject_startup_hooks(directory, entry["files"], allow_runtime_bytecode=True)
        total_files += len(entry["files"])
        total_bytes += sum(record["size"] for record in entry["files"])
        roots.append(directory)
        for name in import_names(directory, entry["files"], runtime_caches=True):
            require(name not in names, f"import shadow/namespace collision: {name}")
            names[name] = str(directory)
    require("runpy" in names, "trusted runpy missing")
    for relative_root in runtime["repository_import_roots"]:
        directory = root / relative_root if relative_root else root
        absolute(str(directory))
        require(directory.is_dir(), "repository import root missing")
        for name in import_names(root, source_records, relative_root):
            require(name not in names, f"repository import shadow/namespace collision: {name}")
            names[name] = str(directory)
    require(
        type(runtime["trusted_files"]) is list and 0 < len(runtime["trusted_files"]) <= 4096,
        "invalid trusted native/startup file inventory",
    )
    trusted: set[str] = set()
    venv_configurations: set[str] = set()
    for entry in runtime["trusted_files"]:
        exact_keys(entry, {"path", "file", "role"}, "trusted runtime file")
        path = absolute(entry["path"])
        require(entry["path"] not in trusted, "duplicate trusted file")
        require(
            entry["role"]
            in {
                "interpreter",
                "timeout",
                "native-library",
                "loader-configuration",
                "startup-configuration",
            },
            "invalid runtime file role",
        )
        validate_inventory([entry["file"]])
        require(
            total_files + 1 <= MAX_FILES and total_bytes + entry["file"]["size"] <= MAX_BYTES,
            "aggregate inventory bound exceeded before trusted-file read",
        )
        require(entry["file"]["path"] == path.name, "trusted file basename mismatch")
        # Small startup configuration is read once, then both hashed and parsed.
        if path.name == "pyvenv.cfg":
            require(entry["role"] == "startup-configuration", "venv config role differs")
            info = regular(path)
            require(info.st_size <= MAX_DYNAMIC_BYTES, "venv configuration too large")
            raw = path.read_bytes()
            observed = {
                "path": path.name,
                "mode": "100644" if stat.S_IMODE(info.st_mode) == 0o644 else "100755",
                "size": len(raw),
                "sha256": sha256(raw),
                "git_blob_sha1": hashlib.sha1(
                    b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw
                ).hexdigest(),
            }
            require(observed == entry["file"], f"trusted file differs: {path}")
            verify_venv_configuration(raw, path)
            venv_configurations.add(str(path))
        else:
            require(file_record(path, path.name) == entry["file"], f"trusted file differs: {path}")
        if entry["role"] == "interpreter":
            require(
                str(path) == runtime["interpreter"] and entry["file"]["mode"] == "100755",
                "interpreter identity/mode differs",
            )
        if entry["role"] == "timeout":
            require(
                str(path) == runtime["timeout_executable"] and entry["file"]["mode"] == "100755",
                "timeout identity/mode differs",
            )
        trusted.add(str(path))
        total_files += 1
        total_bytes += entry["file"]["size"]
    require(
        runtime["interpreter"] in trusted
        and sum(item["role"] == "interpreter" for item in runtime["trusted_files"]) == 1,
        "exact interpreter must be inventoried",
    )
    require(
        runtime["timeout_executable"] in trusted
        and sum(item["role"] == "timeout" for item in runtime["trusted_files"]) == 1,
        "exact timeout must be inventoried",
    )
    require(total_files <= MAX_FILES and total_bytes <= MAX_BYTES, "aggregate scan bound exceeded")
    for entry in runtime["import_roots"]:
        if entry["excluded_subtrees"]:
            require(
                str(Path(runtime["interpreter"]).parent.parent / "pyvenv.cfg")
                in venv_configurations,
                "inactive stdlib exclusions require the target's pinned venv configuration",
            )
        for excluded in entry["excluded_subtrees"]:
            inactive = Path(entry["path"]) / excluded
            require(
                not any(item == inactive or inactive in item.parents for item in roots),
                "inactive subtree is also an active import root",
            )
    absent = runtime["startup_absent_paths"]
    require(
        type(absent) is list
        and len(absent) <= 256
        and all(type(name) is str for name in absent)
        and len(set(absent)) == len(absent),
        "invalid absent startup paths",
    )
    executable = Path(runtime["interpreter"])
    mandatory_absent = {str(executable.with_suffix("._pth")), "/etc/ld.so.preload"}
    for config in (executable.parent / "pyvenv.cfg", executable.parent.parent / "pyvenv.cfg"):
        if str(config) not in trusted:
            mandatory_absent.add(str(config))
    require(mandatory_absent <= set(absent), "startup absence checks incomplete")
    archives = runtime["absent_import_archives"]
    require(
        type(archives) is list
        and len(archives) <= 8
        and all(type(name) is str and name.endswith(".zip") for name in archives)
        and len(set(archives)) == len(archives),
        "only explicitly absent startup zip archives are supported",
    )
    startup = runtime["startup_search_path"]
    require(
        type(startup) is list
        and len(startup) <= 26
        and all(type(name) is str for name in startup)
        and len(set(startup)) == len(startup),
        "invalid startup path precedence",
    )
    require(
        [name for name in startup if name not in archives]
        == [str(root), str(root / "src"), *[str(item) for item in roots]]
        and set(archives) <= set(startup),
        "startup path precedence differs",
    )
    for value in [*absent, *archives]:
        require(
            type(value) is str and value == os.path.normpath(value) and value.startswith("/"),
            "invalid absent path",
        )
        path = Path(value)
        absolute(str(path.parent))
        require(not os.path.lexists(path), f"unexpected startup file: {path}")
    review = runtime["native_closure_review"]
    exact_keys(review, {"sha256", "reference", "assertion"}, "native closure review")
    hex_digest(review["sha256"], 64, "native closure review digest")
    require(
        type(review["reference"]) is str
        and bool(review["reference"].strip())
        and review["assertion"] == "independently-reviewed-complete-loader-and-startup-closure",
        "independent native/startup closure review required",
    )
    exact_keys(request, {"argv_template", "cwd", "env"}, "fixed launch template")
    require(
        canonical(request) == canonical(make_launch_request(binding)),
        "fixed launch template differs",
    )
    return _observation_record(binding, externally_trusted_sha256, request)


def _observation_record(
    binding: dict[str, Any], binding_sha256: str, template: dict[str, Any]
) -> dict[str, Any]:
    """Pure projection shared by full verification and detached association checks."""
    return {
        "schema": "g0-prelaunch-observation-v3",
        "verifier_version": VERSION,
        "status": "checked-not-authorized",
        "authority_binding_sha256": binding_sha256,
        "published_commit": binding["source"]["published_commit"],
        "published_tree": binding["source"]["published_tree"],
        "source_root": binding["source"]["root"],
        "full_tree_inventory_sha256": sha256(canonical(binding["source"]["files"])),
        "launch_template_sha256": sha256(canonical(template)),
        "bindings": binding["bindings"],
        "identity": IDENTITY,
        "requires_external_prestart_sequencing": True,
        "requires_quiescent_source_environment": True,
        "native_closure_review": binding["runtime"]["native_closure_review"],
        "dynamic_data_exceptions": binding["source"]["dynamic_data_exceptions"],
        "execution_authorized": False,
    }


def verify_approval_overlay(
    observation: dict[str, Any],
    template: dict[str, Any],
    binding_raw: bytes,
    approval_path: Path,
    externally_trusted_raw_sha256: str,
    externally_trusted_canonical_sha256: str,
    *,
    externally_trusted_binding_sha256: str,
) -> dict[str, Any]:
    """Detached, non-authorizing receipt. Does not certify approval semantics.

    Authenticate/hash/parse the SAME raw binding buffer and require the complete
    observation projection, not merely matching argv. The supervisor separately
    authenticates both the binding digest and the prior observation's provenance.
    This check does not rescan target/source files or rerun the target.

    Independent authority must bind the canonical observation digest in the approval;
    this overlay then references both, without feeding its digest back into either.
    Read/hash/parse the SAME approval byte buffer; never hash then reopen.
    """
    require(type(binding_raw) is bytes, "overlay requires raw binding bytes")
    require(len(binding_raw) <= MAX_JSON_BYTES, "JSON input too large")
    hex_digest(externally_trusted_binding_sha256, 64, "externally trusted binding digest")
    require(
        sha256(binding_raw) == externally_trusted_binding_sha256,
        "overlay raw binding digest differs",
    )
    require(
        type(observation) is dict
        and observation.get("authority_binding_sha256") == externally_trusted_binding_sha256,
        "observation authority binding differs",
    )
    binding = decode_json(binding_raw)
    try:
        exact_keys(
            binding, {"schema", "source", "runtime", "target_arguments", "bindings"}, "binding"
        )
        require(binding["schema"] == "g0-external-prelaunch-binding-v3", "binding schema differs")
        exact_keys(template, {"argv_template", "cwd", "env"}, "fixed launch template")
        require(
            canonical(template) == canonical(make_launch_request(binding)),
            "overlay template differs",
        )
        expected = _observation_record(binding, externally_trusted_binding_sha256, template)
        exact_keys(observation, set(expected), "closure observation")
        require(
            canonical(observation) == canonical(expected),
            "observation content differs from authenticated binding",
        )
    except (KeyError, TypeError, ValueError, RecursionError) as exc:
        raise Rejected(f"invalid overlay association: {exc}") from exc
    absolute(str(approval_path))
    info = regular(approval_path, private_data=True)
    require(info.st_size <= MAX_DYNAMIC_BYTES, "approval overlay exceeds byte bound")
    raw = approval_path.read_bytes()
    hex_digest(externally_trusted_raw_sha256, 64, "raw approval pin")
    hex_digest(externally_trusted_canonical_sha256, 64, "canonical approval pin")
    require(sha256(raw) == externally_trusted_raw_sha256, "raw approval overlay differs")
    approval = decode_json(raw)
    require(
        type(approval) is dict
        and sha256(target_approval_canonical(approval)) == externally_trusted_canonical_sha256,
        "canonical approval overlay differs",
    )
    overlay = {
        "approval_raw_sha256": externally_trusted_raw_sha256,
        "approval_canonical_sha256": externally_trusted_canonical_sha256,
    }
    actual = make_launch_request(binding, overlay)
    return {
        "schema": "g0-prelaunch-overlay-observation-v3",
        "execution_authorized": False,
        "closure_observation_sha256": sha256(canonical(observation)),
        "authority_binding_sha256": externally_trusted_binding_sha256,
        "approval_overlay": overlay,
        "actual_launch_request": actual,
        "actual_launch_request_sha256": sha256(canonical(actual)),
        "approval_semantics_verified": False,
        "target_started": False,
    }


def check_published_baseline(root: Path) -> dict[str, Any]:
    inventory_path = Path(__file__).absolute().with_name("published_baseline_inventory.json")
    inventory = read_json(inventory_path, BASELINE_INVENTORY_SHA256)
    exact_keys(
        inventory, {"schema", "published_commit", "published_tree", "files"}, "baseline inventory"
    )
    require(
        inventory["schema"] == "g0-published-source-inventory-v1"
        and inventory["published_commit"] == BASELINE_COMMIT
        and inventory["published_tree"] == BASELINE_TREE
        and len(inventory["files"]) == BASELINE_FILES,
        "fixed published baseline differs",
    )
    require(git_tree_sha1(inventory["files"]) == BASELINE_TREE, "fixed Git tree mismatch")
    result = verify_directory(root, inventory["files"])
    return {
        "schema": "g0-source-only-check-v3",
        "status": "source-only-checked",
        "published_commit": BASELINE_COMMIT,
        "published_tree": BASELINE_TREE,
        **result,
        "execution_authorized": False,
        "environment_verified": False,
    }


def main() -> int:
    require(
        sys.flags.isolated == 1 and sys.flags.no_site == 1 and sys.dont_write_bytecode,
        "run verifier with a separately trusted Python -I -S -B",
    )
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    source = commands.add_parser(
        "check-source", help="fixed PR195 baseline only; no proof issuance"
    )
    source.add_argument("--root", required=True)
    final = commands.add_parser("check-final", help="check an independently pinned future proposal")
    final.add_argument("--binding", required=True)
    final.add_argument(
        "--binding-sha256",
        required=True,
        help="raw-file digest authenticated by independent authority, never self-derived",
    )
    final.add_argument("--launch-request", required=True)
    args = parser.parse_args()
    if args.command == "check-source":
        result = check_published_baseline(absolute(args.root))
    else:
        request = read_json(absolute(args.launch_request))
        result = verify_final(absolute(args.binding), args.binding_sha256, request)
    print(canonical(result).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Rejected, OSError, KeyError, TypeError, RecursionError) as error:
        print(f"REJECTED: {error}", file=sys.stderr)
        raise SystemExit(2) from None
