"""Fail-closed source-only candidate/review release primitives for C20 integration.

Each publication is a unique directory atomically renamed from validated staging. The group
directory contains both ZIP/checksum pairs and its binding manifest; no external pointer is
published. A process kill before/within rename is not recoverable and must not be reported as a
successful release.
"""

from __future__ import annotations

import ast
import hashlib
import io
import json
import shutil
import stat
import subprocess
import tempfile
import time
import zipfile
from collections import Counter
from collections.abc import Iterable
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from sparkbrain.release_atomic import atomic_publish_directory_noreplace

CANDIDATE_MANIFEST_NAME = "CANDIDATE_RELEASE_MANIFEST.json"
REVIEW_MANIFEST_NAME = "REVIEW_BUNDLE_MANIFEST.json"
RELEASE_GROUP_MANIFEST_NAME = "RELEASE_GROUP_MANIFEST.json"
PRIVATE_REVIEW_NOTICE_NAME = "PRIVATE_REVIEW_NOTICE.txt"
CANDIDATE_MANIFEST_SCHEMA = "sparkbrain-candidate-release-v1"
REVIEW_MANIFEST_SCHEMA = "sparkbrain-review-bundle-v2"
RELEASE_GROUP_SCHEMA = "sparkbrain-release-group-v1"
NETWORK_PREFIXES = {"aiohttp", "http", "httpx", "requests", "socket", "urllib", "urllib3"}
FORBIDDEN_DYNAMIC_RESOLVER_MODULES = {
    "importlib",
    "pkg_resources",
    "pkgutil",
    "pydoc",
    "runpy",
    "zipimport",
}
FORBIDDEN_DYNAMIC_RESOLVER_CALLS = {
    "exec_module",
    "find_spec",
    "load_entry_point",
    "locate",
    "module_from_spec",
    "resolve_name",
    "run_module",
    "run_path",
    "zipimporter",
}
STATIC_NETWORK_IMPORT_ALLOWLIST = {
    "src/sparkbrain/external_validation/belief_r.py": {"urllib"},
    "src/sparkbrain/external_validation/evaluation.py": {"socket"},
}
GROUP_PAYLOAD_NAMES = {
    "candidate.zip",
    "candidate.zip.sha256",
    "review.zip",
    "review.zip.sha256",
}
PRIVATE_REVIEW_NOTICE = (
    b"PRIVATE CHATGPT REVIEW BUNDLE\n"
    b"This archive is for private review, not a public release.\n"
    b"The project license remains an owner decision.\n"
    b"REVIEW_BUNDLE_MANIFEST.json is the content authority for this archive.\n"
)


def _json(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=2) + "\n").encode()


def _plain_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _valid_sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _path(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError("unsafe candidate path")
    normalized = value.replace("\\", "/")
    path = PurePosixPath(normalized)
    windows_path = PureWindowsPath(value)
    if (
        path.is_absolute()
        or windows_path.is_absolute()
        or bool(windows_path.drive)
        or ".." in path.parts
        or normalized in {"", "."}
    ):
        raise ValueError("unsafe candidate path")
    return path.as_posix()


def _revision(value: Any) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 40
        or any(c not in "0123456789abcdef" for c in value)
    ):
        raise ValueError("source_revision must be a full lowercase Git SHA")
    return value


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=False)
    if result.returncode:
        raise ValueError(
            "repository revision validation failed: " + (result.stderr.strip() or "git failed")
        )
    return result.stdout.strip()


def _bound_revision(root: Path, revision: str, base: str | None) -> None:
    _git(root, "cat-file", "-e", f"{revision}^{{commit}}")
    target = base or _git(root, "rev-parse", "HEAD")
    _git(root, "cat-file", "-e", f"{_revision(target)}^{{commit}}")
    _git(root, "merge-base", "--is-ancestor", revision, target)


def _git_blob(root: Path, revision: str, relative: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{revision}:{relative}"], cwd=root, capture_output=True, check=False
    )
    if result.returncode:
        raise ValueError(f"payload path is not bound to source_revision: {relative}")
    return result.stdout


def _bound_payload(root: Path, revision: str, paths: Iterable[str]) -> None:
    for relative in paths:
        clean = _git(root, "hash-object", "--path", relative, "--", relative)
        expected = _git(root, "rev-parse", f"{revision}:{relative}")
        if clean != expected:
            raise ValueError(f"payload content is not bound to source_revision: {relative}")


def build_canonical_reproduction_manifest(
    root: Path, *, source_revision: str, paths: Iterable[str], revision_base: str | None = None
) -> dict[str, Any]:
    revision = _revision(source_revision)
    selected = sorted(_path(path) for path in paths)
    if len(selected) != len(set(selected)):
        raise ValueError("candidate manifest paths must be unique")
    _bound_revision(root, revision, revision_base)
    _bound_payload(root, revision, selected)
    files = []
    for relative in selected:
        source = root / relative
        if source.is_symlink() or not source.is_file():
            raise ValueError(f"candidate input is not a regular file: {relative}")
        blob = _git_blob(root, revision, relative)
        files.append(
            {"path": relative, "size": len(blob), "sha256": hashlib.sha256(blob).hexdigest()}
        )
    return {
        "schema_version": CANDIDATE_MANIFEST_SCHEMA,
        "source_revision": revision,
        "files": files,
        "file_count": len(files),
        "total_bytes": sum(row["size"] for row in files),
    }


def validate_canonical_reproduction_manifest(
    root: Path, manifest: Any, *, revision_base: str | None = None
) -> list[str]:
    if not isinstance(manifest, dict):
        return ["candidate manifest must be a JSON object"]
    expected = {"schema_version", "source_revision", "files", "file_count", "total_bytes"}
    problems: list[str] = []
    if set(manifest) != expected:
        problems.append("candidate manifest fields do not match fixed schema")
    if manifest.get("schema_version") != CANDIDATE_MANIFEST_SCHEMA:
        problems.append("unsupported candidate manifest schema version")
    revision: str | None = None
    try:
        revision = _revision(manifest.get("source_revision"))
        _bound_revision(root, revision, revision_base)
    except ValueError as exc:
        problems.append(str(exc))
    rows = manifest.get("files")
    if not isinstance(rows, list):
        return [*problems, "candidate manifest files must be an array"]
    paths: list[str] = []
    total = 0
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != {"path", "size", "sha256"}:
            problems.append(f"candidate manifest files[{index}] has invalid fields")
            continue
        try:
            canonical_path = _path(row["path"])
            paths.append(canonical_path)
        except ValueError:
            problems.append(f"candidate manifest files[{index}] has unsafe path")
            continue
        if canonical_path != row["path"]:
            problems.append(f"candidate manifest files[{index}] path is not canonical")
        if not _plain_int(row["size"]) or row["size"] < 0:
            problems.append(
                f"candidate manifest files[{index}] size must be a non-negative integer"
            )
        else:
            total += row["size"]
        if not _valid_sha256(row["sha256"]):
            problems.append(f"candidate manifest files[{index}] sha256 must be lowercase SHA-256")
        if revision is not None:
            try:
                blob = _git_blob(root, revision, paths[-1])
            except ValueError as exc:
                problems.append(str(exc))
            else:
                if _plain_int(row["size"]) and row["size"] != len(blob):
                    problems.append(
                        f"candidate manifest files[{index}] size does not match Git blob"
                    )
                if _valid_sha256(row["sha256"]) and row["sha256"] != _sha256_bytes(blob):
                    problems.append(
                        f"candidate manifest files[{index}] sha256 does not match Git blob"
                    )
    if paths != sorted(paths):
        problems.append("candidate manifest file paths must be sorted")
    if len(paths) != len(set(paths)):
        problems.append("candidate manifest file paths must be unique")
    if not _plain_int(manifest.get("file_count")) or manifest["file_count"] != len(rows):
        problems.append("candidate manifest file_count mismatch")
    if not _plain_int(manifest.get("total_bytes")) or manifest["total_bytes"] != total:
        problems.append("candidate manifest total_bytes mismatch")
    if revision is not None and len(paths) == len(rows):
        try:
            _bound_payload(root, revision, paths)
        except ValueError as exc:
            problems.append(str(exc))
    return problems


def _subscript_key(node: ast.Subscript) -> str | None:
    if isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, str):
        return node.slice.value
    return None


def _dynamic_import_aliases(tree: ast.AST) -> tuple[set[str], set[str], set[str]]:
    importlib_names = {"importlib"}
    builtins_names = {"builtins"}
    direct_names = {"__import__"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "importlib":
                    importlib_names.add(alias.asname or alias.name)
                elif alias.name == "builtins":
                    builtins_names.add(alias.asname or alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module == "importlib":
            for alias in node.names:
                if alias.name == "import_module":
                    direct_names.add(alias.asname or alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module == "builtins":
            for alias in node.names:
                if alias.name == "__import__":
                    direct_names.add(alias.asname or alias.name)
    return importlib_names, builtins_names, direct_names


def _sys_module_aliases(tree: ast.AST) -> tuple[set[str], set[str]]:
    sys_names = {"sys"}
    module_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "sys":
                    sys_names.add(alias.asname or alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module == "sys":
            for alias in node.names:
                if alias.name == "modules":
                    module_names.add(alias.asname or alias.name)
    return sys_names, module_names


def _shadowed_import_aliases(tree: ast.AST, tracked: set[str]) -> set[str]:
    shadowed: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store) and node.id in tracked:
            shadowed.add(node.id)
        elif isinstance(node, ast.arg) and node.arg in tracked:
            shadowed.add(node.arg)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.name in tracked:
                shadowed.add(node.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                bound = alias.asname or alias.name.split(".")[0]
                if bound in tracked and alias.name not in {"importlib", "builtins"}:
                    shadowed.add(bound)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                bound = alias.asname or alias.name
                allowed = (node.module, alias.name) in {
                    ("importlib", "import_module"),
                    ("builtins", "__import__"),
                }
                if bound in tracked and not allowed:
                    shadowed.add(bound)
        elif isinstance(node, ast.ExceptHandler) and node.name in tracked:
            shadowed.add(node.name)
    return shadowed


def _dynamic_import_primitive_kind(
    node: ast.AST,
    *,
    importlib_names: set[str],
    builtins_names: set[str],
    direct_names: set[str],
    shadowed: set[str],
) -> str | None:
    if isinstance(node, ast.Name) and node.id in direct_names:
        return "ambiguous" if node.id in shadowed else "proven"
    if isinstance(node, ast.Attribute) and node.attr in {"import_module", "__import__"}:
        owner = node.value.id if isinstance(node.value, ast.Name) else None
        expected = importlib_names if node.attr == "import_module" else builtins_names
        return "proven" if owner in expected and owner not in shadowed else "ambiguous"
    return None


def _name_in(node: ast.AST, names: set[str]) -> bool:
    return any(isinstance(child, ast.Name) and child.id in names for child in ast.walk(node))


def _folded_string(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = _folded_string(node.left)
        right = _folded_string(node.right)
        if left is not None and right is not None:
            return left + right
    return None


def _is_forbidden_reflection(
    node: ast.AST,
    *,
    parent: ast.AST | None,
    importlib_names: set[str],
    builtins_names: set[str],
    sys_names: set[str],
    sys_module_names: set[str],
) -> bool:
    module_names = {*importlib_names, *builtins_names, "__builtins__"}
    dynamic_names = {"import_module", "__import__", "__builtins__"}
    if (
        isinstance(node, ast.Name)
        and isinstance(node.ctx, ast.Load)
        and (node.id in module_names or node.id in sys_module_names)
    ):
        return True
    if (
        _folded_string(node) in dynamic_names
        and isinstance(parent, (ast.Call, ast.Subscript))
    ):
        return True
    if (
        isinstance(node, ast.Name)
        and isinstance(node.ctx, ast.Load)
        and node.id in sys_names
        and not (
            isinstance(parent, ast.Attribute)
            and parent.value is node
            and parent.attr != "modules"
        )
    ):
        return True
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id in {
            "eval",
            "exec",
            "compile",
            "globals",
            "locals",
            "vars",
        }:
            return True
        if isinstance(node.func, ast.Name) and node.func.id == "getattr":
            attribute = (
                node.args[1].value
                if len(node.args) >= 2
                and isinstance(node.args[1], ast.Constant)
                and isinstance(node.args[1].value, str)
                else None
            )
            return bool(
                node.args
                and (
                    _name_in(node.args[0], module_names)
                    or _name_in(node.args[0], sys_names)
                    and attribute in {None, "modules", "__dict__", "__getattribute__"}
                    or attribute in {"__dict__", "__getattribute__", *dynamic_names}
                )
            )
        if isinstance(node.func, ast.Attribute) and node.func.attr == "__getattribute__":
            return _name_in(node.func.value, module_names) or any(
                isinstance(argument, ast.Constant) and argument.value in dynamic_names
                for argument in node.args
            )
    if isinstance(node, ast.Attribute) and node.attr in {"__dict__", "__getattribute__"}:
        return _name_in(node.value, module_names) or _name_in(node.value, sys_names)
    if (
        isinstance(node, ast.Attribute)
        and node.attr == "modules"
        and _name_in(node.value, sys_names)
    ):
        return True
    if isinstance(node, ast.Subscript):
        return (
            _subscript_key(node) in dynamic_names
            or _name_in(node.value, module_names)
            and (
                isinstance(node.value, ast.Name)
                or isinstance(node.value, ast.Attribute)
                and node.value.attr in {"__dict__", "__getattribute__"}
            )
        )
    return False


def _is_forbidden_dynamic_resolver(node: ast.AST) -> bool:
    if isinstance(node, ast.Import):
        return any(
            alias.name.split(".")[0] in FORBIDDEN_DYNAMIC_RESOLVER_MODULES
            for alias in node.names
        )
    if isinstance(node, ast.ImportFrom) and node.module:
        return node.module.split(".")[0] in FORBIDDEN_DYNAMIC_RESOLVER_MODULES
    if not isinstance(node, ast.Call):
        return False
    if isinstance(node.func, ast.Attribute):
        return node.func.attr in FORBIDDEN_DYNAMIC_RESOLVER_CALLS
    return isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_DYNAMIC_RESOLVER_CALLS


def validate_network_client_boundary(root: Path) -> list[str]:
    package = root / "src" / "sparkbrain"
    if not package.is_dir():
        raise ValueError("network boundary requires src/sparkbrain package root")
    sources = sorted(package.rglob("*.py"))
    if not sources:
        raise ValueError("network boundary found no package Python sources")
    problems: list[str] = []
    for path in sources:
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (OSError, UnicodeDecodeError, SyntaxError) as exc:
            problems.append(f"network boundary could not parse {path}: {exc}")
            continue
        relative = path.relative_to(root).as_posix()
        allowed_static = STATIC_NETWORK_IMPORT_ALLOWLIST.get(relative, set())
        importlib_names, builtins_names, direct_names = _dynamic_import_aliases(tree)
        sys_names, sys_module_names = _sys_module_aliases(tree)
        tracked = {*importlib_names, *builtins_names, *direct_names, "__builtins__", "getattr"}
        shadowed = _shadowed_import_aliases(tree, tracked)
        parents = {
            child: parent
            for parent in ast.walk(tree)
            for child in ast.iter_child_nodes(parent)
        }
        for node in ast.walk(tree):
            names = (
                [a.name for a in node.names]
                if isinstance(node, ast.Import)
                else [node.module]
                if isinstance(node, ast.ImportFrom) and node.module
                else []
            )
            imported_network = {
                name.split(".")[0]
                for name in names
                if name.split(".")[0] in NETWORK_PREFIXES
            }
            if imported_network - allowed_static:
                problems.append(f"network client import is forbidden: {path}")
            primitive_kind = _dynamic_import_primitive_kind(
                node,
                importlib_names=importlib_names,
                builtins_names=builtins_names,
                direct_names=direct_names,
                shadowed=shadowed,
            )
            if primitive_kind is not None:
                problems.append(f"unproven or network dynamic import is forbidden: {path}")
            if _is_forbidden_reflection(
                node,
                parent=parents.get(node),
                importlib_names=importlib_names,
                builtins_names=builtins_names,
                sys_names=sys_names,
                sys_module_names=sys_module_names,
            ):
                problems.append(f"dynamic import reflection is forbidden: {path}")
            if _is_forbidden_dynamic_resolver(node):
                problems.append(f"dynamic resolver or loader is forbidden: {path}")
    return sorted(set(problems))


def _archive_layout(archive: zipfile.ZipFile) -> tuple[list[str], list[str]]:
    problems: list[str] = []
    infos = archive.infolist()
    names = [info.filename for info in infos]
    duplicates = sorted(name for name, count in Counter(names).items() if count > 1)
    if duplicates:
        problems.append(f"duplicate ZIP entries: {duplicates}")
    for info in infos:
        try:
            canonical = _path(info.filename)
        except ValueError:
            problems.append(f"unsafe ZIP entry path: {info.filename}")
            continue
        if canonical != info.filename:
            problems.append(f"non-canonical ZIP entry path: {info.filename}")
        if info.is_dir():
            problems.append(f"ZIP directory entry is not allowed: {info.filename}")
        if stat.S_ISLNK(info.external_attr >> 16):
            problems.append(f"ZIP symlink is not allowed: {info.filename}")
    try:
        damaged = archive.testzip()
    except (OSError, RuntimeError, zipfile.BadZipFile) as exc:
        problems.append(f"ZIP CRC validation failed: {exc}")
    else:
        if damaged is not None:
            problems.append(f"ZIP CRC validation failed: {damaged}")
    return problems, names


def _inspect_candidate_archive_bytes(
    root: Path, data: bytes, *, revision_base: str | None = None
) -> tuple[list[str], dict[str, Any] | None, bytes | None]:
    problems: list[str] = []
    try:
        archive = zipfile.ZipFile(io.BytesIO(data))
    except (OSError, zipfile.BadZipFile) as exc:
        return [f"candidate ZIP is unreadable: {exc}"], None, None
    with archive:
        layout_problems, names = _archive_layout(archive)
        problems.extend(layout_problems)
        if names.count(CANDIDATE_MANIFEST_NAME) != 1:
            problems.append("candidate manifest must appear exactly once")
            return problems, None, None
        try:
            manifest_bytes = archive.read(CANDIDATE_MANIFEST_NAME)
            manifest = json.loads(manifest_bytes.decode("utf-8"))
        except (
            KeyError,
            RuntimeError,
            UnicodeDecodeError,
            json.JSONDecodeError,
            zipfile.BadZipFile,
        ) as exc:
            problems.append(f"candidate manifest is unreadable: {exc}")
            return problems, None, None
        if manifest_bytes != _json(manifest):
            problems.append("candidate manifest is not canonical JSON")
        problems.extend(
            validate_canonical_reproduction_manifest(
                root, manifest, revision_base=revision_base
            )
        )
        rows = manifest.get("files") if isinstance(manifest, dict) else None
        expected_names = {CANDIDATE_MANIFEST_NAME}
        if isinstance(rows, list):
            for row in rows:
                if not isinstance(row, dict) or not isinstance(row.get("path"), str):
                    continue
                try:
                    relative = _path(row["path"])
                except ValueError:
                    continue
                expected_names.add(relative)
                if names.count(relative) != 1:
                    problems.append(f"candidate ZIP entry must appear exactly once: {relative}")
                    continue
                try:
                    content = archive.read(relative)
                except (KeyError, RuntimeError, zipfile.BadZipFile) as exc:
                    problems.append(f"candidate ZIP entry is unreadable: {relative}: {exc}")
                    continue
                if _plain_int(row.get("size")) and row["size"] != len(content):
                    problems.append(f"candidate ZIP size mismatch: {relative}")
                if _valid_sha256(row.get("sha256")) and row["sha256"] != _sha256_bytes(content):
                    problems.append(f"candidate ZIP sha256 mismatch: {relative}")
        if set(names) != expected_names:
            problems.append("candidate manifest does not exactly match ZIP contents")
    return sorted(set(problems)), manifest if isinstance(manifest, dict) else None, manifest_bytes


def validate_candidate_archive(
    root: Path, path: Path, *, revision_base: str | None = None
) -> list[str]:
    if path.is_symlink() or not path.is_file():
        return ["candidate archive must be a regular file"]
    try:
        data = path.read_bytes()
    except OSError as exc:
        return [f"candidate ZIP is unreadable: {exc}"]
    problems, _, _ = _inspect_candidate_archive_bytes(
        root, data, revision_base=revision_base
    )
    return problems


def _review_manifest_fields() -> set[str]:
    return {
        "schema_version",
        "bundle_type",
        "candidate_zip",
        "candidate_sha256",
        "candidate_checksum",
        "candidate_checksum_sha256",
        "candidate_manifest",
        "candidate_manifest_sha256",
        "source_revision",
        "private_notice",
        "private_notice_sha256",
        "license_status",
    }


def _inspect_review_archive_bytes(
    root: Path, data: bytes, *, revision_base: str | None = None
) -> tuple[list[str], dict[str, Any] | None, bytes | None]:
    problems: list[str] = []
    try:
        archive = zipfile.ZipFile(io.BytesIO(data))
    except (OSError, zipfile.BadZipFile) as exc:
        return [f"review ZIP is unreadable: {exc}"], None, None
    with archive:
        layout_problems, names = _archive_layout(archive)
        problems.extend(layout_problems)
        expected_names = {
            "candidate.zip",
            "candidate.zip.sha256",
            PRIVATE_REVIEW_NOTICE_NAME,
            REVIEW_MANIFEST_NAME,
        }
        if set(names) != expected_names or len(names) != len(expected_names):
            problems.append("review manifest does not exactly match ZIP contents")
        if names.count(REVIEW_MANIFEST_NAME) != 1:
            problems.append("review manifest must appear exactly once")
            return sorted(set(problems)), None, None
        try:
            manifest_bytes = archive.read(REVIEW_MANIFEST_NAME)
            manifest = json.loads(manifest_bytes.decode("utf-8"))
        except (
            KeyError,
            RuntimeError,
            UnicodeDecodeError,
            json.JSONDecodeError,
            zipfile.BadZipFile,
        ) as exc:
            problems.append(f"review manifest is unreadable: {exc}")
            return sorted(set(problems)), None, None
        if manifest_bytes != _json(manifest):
            problems.append("review manifest is not canonical JSON")
        if not isinstance(manifest, dict) or set(manifest) != _review_manifest_fields():
            problems.append("review manifest fields do not match fixed schema")
            return sorted(set(problems)), None, manifest_bytes
        expected_values = {
            "schema_version": REVIEW_MANIFEST_SCHEMA,
            "bundle_type": "private-review",
            "candidate_zip": "candidate.zip",
            "candidate_checksum": "candidate.zip.sha256",
            "candidate_manifest": CANDIDATE_MANIFEST_NAME,
            "private_notice": PRIVATE_REVIEW_NOTICE_NAME,
            "license_status": "owner-decision-pending",
        }
        for field, expected in expected_values.items():
            if manifest[field] != expected:
                problems.append(f"review manifest {field} mismatch")
        for field in (
            "candidate_sha256",
            "candidate_checksum_sha256",
            "candidate_manifest_sha256",
            "private_notice_sha256",
        ):
            if not _valid_sha256(manifest[field]):
                problems.append(f"review manifest {field} must be lowercase SHA-256")
        try:
            candidate_bytes = archive.read("candidate.zip")
            checksum_bytes = archive.read("candidate.zip.sha256")
            notice_bytes = archive.read(PRIVATE_REVIEW_NOTICE_NAME)
        except (KeyError, RuntimeError, zipfile.BadZipFile) as exc:
            problems.append(f"review payload is unreadable: {exc}")
            return sorted(set(problems)), manifest, manifest_bytes
        candidate_sha256 = _sha256_bytes(candidate_bytes)
        if manifest["candidate_sha256"] != candidate_sha256:
            problems.append("review candidate hash mismatch")
        expected_checksum = f"{candidate_sha256}  candidate.zip\n".encode("ascii")
        if checksum_bytes != expected_checksum:
            problems.append("review candidate checksum content mismatch")
        if manifest["candidate_checksum_sha256"] != _sha256_bytes(checksum_bytes):
            problems.append("review candidate checksum hash mismatch")
        if notice_bytes != PRIVATE_REVIEW_NOTICE:
            problems.append("review private notice content mismatch")
        if manifest["private_notice_sha256"] != _sha256_bytes(notice_bytes):
            problems.append("review private notice hash mismatch")
        candidate_problems, candidate_manifest, candidate_manifest_bytes = (
            _inspect_candidate_archive_bytes(
                root, candidate_bytes, revision_base=revision_base
            )
        )
        problems.extend(candidate_problems)
        if candidate_manifest_bytes is None:
            problems.append("review candidate manifest is unavailable")
        elif manifest["candidate_manifest_sha256"] != _sha256_bytes(candidate_manifest_bytes):
            problems.append("review candidate manifest hash mismatch")
        if candidate_manifest is None:
            problems.append("review candidate source revision is unavailable")
        elif manifest["source_revision"] != candidate_manifest.get("source_revision"):
            problems.append("review candidate source revision mismatch")
    return sorted(set(problems)), manifest, manifest_bytes


def validate_review_bundle(
    root: Path, path: Path, *, revision_base: str | None = None
) -> list[str]:
    if path.is_symlink() or not path.is_file():
        return ["review archive must be a regular file"]
    try:
        data = path.read_bytes()
    except OSError as exc:
        return [f"review ZIP is unreadable: {exc}"]
    problems, _, _ = _inspect_review_archive_bytes(root, data, revision_base=revision_base)
    return problems


def validate_release_group(
    root: Path, directory: Path, *, revision_base: str | None = None
) -> list[str]:
    if directory.is_symlink() or not directory.is_dir():
        return ["release group must be a regular directory"]
    problems: list[str] = []
    expected_names = {*GROUP_PAYLOAD_NAMES, RELEASE_GROUP_MANIFEST_NAME}
    actual_names = {path.name for path in directory.iterdir()}
    if actual_names != expected_names:
        problems.append("release group contents do not match fixed schema")
    group_path = directory / RELEASE_GROUP_MANIFEST_NAME
    try:
        group_bytes = group_path.read_bytes()
        group = json.loads(group_bytes.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return [*problems, f"release group manifest is unreadable: {exc}"]
    if group_bytes != _json(group):
        problems.append("release group manifest is not canonical JSON")
    if not isinstance(group, dict) or set(group) != {"schema_version", "files"}:
        return [*problems, "release group manifest fields do not match fixed schema"]
    if group["schema_version"] != RELEASE_GROUP_SCHEMA:
        problems.append("unsupported release group manifest schema version")
    files = group["files"]
    if not isinstance(files, dict) or set(files) != GROUP_PAYLOAD_NAMES:
        problems.append("release group file bindings do not match fixed schema")
    else:
        for name in sorted(GROUP_PAYLOAD_NAMES):
            path = directory / name
            if path.is_symlink() or not path.is_file():
                problems.append(f"release group payload is not a regular file: {name}")
                continue
            if not _valid_sha256(files[name]):
                problems.append(f"release group hash must be lowercase SHA-256: {name}")
            elif files[name] != sha256_file(path):
                problems.append(f"release group hash mismatch: {name}")
    candidate = directory / "candidate.zip"
    review = directory / "review.zip"
    if candidate.is_file() and not candidate.is_symlink():
        problems.extend(
            validate_candidate_archive(root, candidate, revision_base=revision_base)
        )
        candidate_sha256 = sha256_file(candidate)
        try:
            candidate_checksum = (directory / "candidate.zip.sha256").read_bytes()
        except OSError as exc:
            problems.append(f"candidate checksum is unreadable: {exc}")
        else:
            expected = f"{candidate_sha256}  candidate.zip\n".encode("ascii")
            if candidate_checksum != expected:
                problems.append("candidate checksum binding mismatch")
    if review.is_file() and not review.is_symlink():
        problems.extend(validate_review_bundle(root, review, revision_base=revision_base))
        review_sha256 = sha256_file(review)
        try:
            review_checksum = (directory / "review.zip.sha256").read_bytes()
        except OSError as exc:
            problems.append(f"review checksum is unreadable: {exc}")
        else:
            expected = f"{review_sha256}  review.zip\n".encode("ascii")
            if review_checksum != expected:
                problems.append("review checksum binding mismatch")
        try:
            with zipfile.ZipFile(review) as archive:
                nested_candidate = archive.read("candidate.zip")
        except (OSError, KeyError, RuntimeError, zipfile.BadZipFile) as exc:
            problems.append(f"review candidate cross-binding is unreadable: {exc}")
        else:
            try:
                external_candidate = candidate.read_bytes()
            except OSError as exc:
                problems.append(f"candidate cross-binding is unreadable: {exc}")
            else:
                if nested_candidate != external_candidate:
                    problems.append("review and release group candidate bytes differ")
    return sorted(set(problems))


def _zip(archive: zipfile.ZipFile, name: str, data: bytes, epoch: int) -> None:
    info = zipfile.ZipInfo(name)
    info.date_time = tuple(time.gmtime(max(epoch, 315532800))[:6])
    info.create_system = 3
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    archive.writestr(info, data, compresslevel=9)


def build_candidate_and_review_archives(
    root: Path,
    *,
    source_revision: str,
    paths: Iterable[str],
    release_directory: Path,
    source_date_epoch: int,
    revision_base: str | None = None,
) -> dict[str, str]:
    if not _plain_int(source_date_epoch):
        raise ValueError("source_date_epoch must be an integer")
    if release_directory.exists() or release_directory.is_symlink():
        raise ValueError("candidate release directory already exists")
    network = validate_network_client_boundary(root)
    if network:
        raise ValueError("network boundary failed: " + "; ".join(network))
    manifest = build_canonical_reproduction_manifest(
        root, source_revision=source_revision, paths=paths, revision_base=revision_base
    )
    release_directory.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(
        tempfile.mkdtemp(prefix=".candidate-release-staging-", dir=release_directory.parent)
    )
    try:
        candidate = staging / "candidate.zip"
        with zipfile.ZipFile(candidate, "w") as archive:
            for row in manifest["files"]:
                _zip(
                    archive,
                    row["path"],
                    _git_blob(root, manifest["source_revision"], row["path"]),
                    source_date_epoch,
                )
            _zip(archive, CANDIDATE_MANIFEST_NAME, _json(manifest), source_date_epoch)
        candidate_problems = validate_candidate_archive(
            root, candidate, revision_base=revision_base
        )
        if candidate_problems:
            raise ValueError(
                "candidate archive validation failed: " + "; ".join(candidate_problems)
            )
        candidate_hash = f"{sha256_file(candidate)}  {candidate.name}\n".encode()
        (staging / "candidate.zip.sha256").write_bytes(candidate_hash)
        review = staging / "review.zip"
        candidate_manifest_bytes = _json(manifest)
        review_manifest = {
            "schema_version": REVIEW_MANIFEST_SCHEMA,
            "bundle_type": "private-review",
            "candidate_zip": candidate.name,
            "candidate_sha256": sha256_file(candidate),
            "candidate_checksum": "candidate.zip.sha256",
            "candidate_checksum_sha256": _sha256_bytes(candidate_hash),
            "candidate_manifest": CANDIDATE_MANIFEST_NAME,
            "candidate_manifest_sha256": _sha256_bytes(candidate_manifest_bytes),
            "source_revision": manifest["source_revision"],
            "private_notice": PRIVATE_REVIEW_NOTICE_NAME,
            "private_notice_sha256": _sha256_bytes(PRIVATE_REVIEW_NOTICE),
            "license_status": "owner-decision-pending",
        }
        with zipfile.ZipFile(review, "w") as archive:
            _zip(archive, candidate.name, candidate.read_bytes(), source_date_epoch)
            _zip(archive, "candidate.zip.sha256", candidate_hash, source_date_epoch)
            _zip(
                archive,
                PRIVATE_REVIEW_NOTICE_NAME,
                PRIVATE_REVIEW_NOTICE,
                source_date_epoch,
            )
            _zip(archive, REVIEW_MANIFEST_NAME, _json(review_manifest), source_date_epoch)
        review_problems = validate_review_bundle(root, review, revision_base=revision_base)
        if review_problems:
            raise ValueError("review archive validation failed: " + "; ".join(review_problems))
        (staging / "review.zip.sha256").write_bytes(
            f"{sha256_file(review)}  {review.name}\n".encode()
        )
        group = {
            "schema_version": RELEASE_GROUP_SCHEMA,
            "files": {p.name: sha256_file(p) for p in sorted(staging.iterdir())},
        }
        (staging / RELEASE_GROUP_MANIFEST_NAME).write_bytes(_json(group))
        group_problems = validate_release_group(root, staging, revision_base=revision_base)
        if group_problems:
            raise ValueError("release group validation failed: " + "; ".join(group_problems))
        final_problems = validate_release_group(root, staging, revision_base=revision_base)
        if final_problems:
            raise ValueError(
                "release group pre-publish validation failed: " + "; ".join(final_problems)
            )
        atomic_publish_directory_noreplace(staging, release_directory)
        published_problems = validate_release_group(
            root, release_directory, revision_base=revision_base
        )
        if published_problems:
            raise ValueError(
                "published release group validation failed: " + "; ".join(published_problems)
            )
    except BaseException:
        # Once published, leave a failed post-publish validation directory in
        # place. Removing by path could delete a competitor that replaced it
        # after publication; failed output is never returned as a release.
        if staging.exists():
            shutil.rmtree(staging, ignore_errors=True)
        raise
    return {
        "release_directory": str(release_directory),
        "candidate": str(release_directory / "candidate.zip"),
        "review": str(release_directory / "review.zip"),
    }
