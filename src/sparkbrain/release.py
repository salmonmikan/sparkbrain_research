from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import subprocess
import tomllib
import zipfile
from collections.abc import Iterable
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any, Literal

MANIFEST_SCHEMA_VERSION = "3"
MANIFEST_PATH = "PACKAGE_MANIFEST.json"
RELEASE_METADATA_SCHEMA_VERSION = "1"
RELEASE_METADATA_PATH = "RELEASE_METADATA.json"
EXCLUDED_PREFIXES = (
    ".git/",
    ".mypy_cache/",
    ".pytest_cache/",
    ".ruff_cache/",
    ".venv/",
    "data/external/",
)
EXCLUDED_PATHS = {
    MANIFEST_PATH,
    # This file binds the manifest hash without creating a self-hash cycle.
    RELEASE_METADATA_PATH,
    # Rewritten by validate_bundle.py on every local run; it is not release evidence.
    "artifacts/validation_manifest.json",
}
REQUIRED_PREPARATION_FILES = (
    "PACKAGE_MANIFEST.json",
    "RELEASE_METADATA.json",
    "requirements-release.lock",
    "requirements-release-provenance.json",
    "scripts/reproduce_release.py",
    "scripts/generate_release_artifacts.py",
    "scripts/build_release_archive.py",
    "docs/ARTIFACT_EVALUATION_GUIDE.md",
    "docs/CLEAN_ROOM_REPRODUCTION.md",
    "docs/MODEL_CARD.md",
    "docs/NEGATIVE_RESULTS_APPENDIX.md",
    "docs/PLATFORM_MATRIX.md",
    "docs/SECURITY_PRIVACY_REVIEW.md",
    "docs/SYSTEM_CARD.md",
    "docs/TECHNICAL_REPORT_v0.2.1.html",
    "docs/TECHNICAL_REPORT_v0.2.1.md",
    "docs/THIRD_PARTY_NOTICES.md",
    "artifacts/release/evidence_map.json",
    "artifacts/release/primary_subset.json",
    "artifacts/release/provenance.json",
    "artifacts/release/claim_audit.json",
    "artifacts/release/sbom.spdx.json",
)
V03_REQUIRED_PREPARATION_FILES = (
    "PACKAGE_MANIFEST.json",
    "RELEASE_METADATA.json",
    "PACKAGE_CONTENTS.md",
    "requirements-release.lock",
    "requirements-release-provenance.json",
    "scripts/build_v03_private_review_bundle.py",
    "scripts/generate_v03_release_artifacts.py",
    "scripts/generate_v03_root_manifest.py",
    "scripts/reproduce_release.py",
    "docs/CLEAN_ROOM_REPRODUCTION.md",
    "docs/NEGATIVE_RESULTS_APPENDIX.md",
    "docs/V03_CLAIM_BOUNDARIES_AND_RISKS.md",
    "docs/V03_MIGRATION_AND_COMPATIBILITY.md",
    "artifacts/release/v0.3/evidence_map.json",
    "artifacts/release/v0.3/release_report.md",
    "artifacts/release/v0.3/release_figure.svg",
    "artifacts/release/v0.3/claim_boundary_figure.svg",
    "artifacts/release/v0.3/sbom.spdx.json",
    "artifacts/release/v0.3/source_license_inventory.json",
    "artifacts/release/v0.3/primary_subset.json",
    "artifacts/release/v0.3/source_manifest.json",
    "artifacts/release/v0.3/reproduction_manifest.json",
    "artifacts/release/v0.3/release_metadata.json",
)
V031_REQUIRED_PREPARATION_FILES = tuple(
    path.replace("artifacts/release/v0.3/", "artifacts/release/v0.3.1/")
    for path in V03_REQUIRED_PREPARATION_FILES
)
REQUIRED_PUBLIC_FILES = ("LICENSE",)
OWNER_LICENSE_BLOCKER = "project license has not been selected by the repository owner"
# Backward-compatible name used by the initial C10 tests.
REQUIRED_RELEASE_FILES = (*REQUIRED_PUBLIC_FILES, *REQUIRED_PREPARATION_FILES)


def _is_v03_package(root: Path) -> bool:
    try:
        return package_version(root) in {"0.3.0", "0.3.1"}
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError, KeyError, ValueError):
        return False


def _v03_release_version(root: Path) -> str | None:
    try:
        value = package_version(root)
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError, KeyError, ValueError):
        return None
    return value if value in {"0.3.0", "0.3.1"} else None


def _v03_release_relative(root: Path) -> str:
    v031 = root / "artifacts/release/v0.3.1/evidence_map.json"
    if _v03_release_version(root) == "0.3.1" and v031.is_file():
        return "artifacts/release/v0.3.1"
    return "artifacts/release/v0.3"


def required_preparation_files(root: Path) -> tuple[str, ...]:
    """Select the release contract from package metadata, not Git history."""

    if _v03_release_relative(root) == "artifacts/release/v0.3.1":
        return V031_REQUIRED_PREPARATION_FILES
    return V03_REQUIRED_PREPARATION_FILES if _is_v03_package(root) else REQUIRED_PREPARATION_FILES


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def _safe_relative_path(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"unsafe release path: {value!r}")
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
        raise ValueError(f"unsafe release path: {value!r}")
    return path.as_posix()


def _is_release_path(path: str) -> bool:
    return path not in EXCLUDED_PATHS and not path.startswith(EXCLUDED_PREFIXES)


def release_mode(root: Path) -> Literal["repository", "archive"]:
    """Select the validation contract from the package root, not an ancestor repo."""

    return "repository" if (root / ".git").exists() else "archive"


def tracked_release_paths(root: Path) -> list[str]:
    if release_mode(root) == "archive":
        metadata_problems = validate_release_metadata(root)
        if metadata_problems:
            raise ValueError(
                "archive release metadata is invalid: " + "; ".join(metadata_problems)
            )
        manifest, problems = _read_json_object(
            root / MANIFEST_PATH, label="release manifest"
        )
        if manifest is None:
            raise ValueError("archive release manifest is invalid: " + "; ".join(problems))
        rows = manifest.get("files")
        if not isinstance(rows, list):
            raise ValueError("archive release manifest files must be an array")
        paths: list[str] = []
        for index, row in enumerate(rows):
            if not isinstance(row, dict) or not isinstance(row.get("path"), str):
                raise ValueError(f"archive release manifest files[{index}] has no path")
            relative = _safe_relative_path(row["path"])
            if not _is_release_path(relative):
                raise ValueError(f"archive release manifest contains excluded path: {relative}")
            paths.append(relative)
        if len(paths) != len(set(paths)):
            raise ValueError("archive release manifest paths must be unique")
        return sorted(paths)
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    paths = [
        _safe_relative_path(item)
        for item in result.stdout.decode("utf-8").split("\0")
        if item
    ]
    return sorted(path for path in paths if _is_release_path(path))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def artifact_class(path: str) -> str:
    if path.startswith("artifacts/release/"):
        return "generated-release-evidence"
    if path.startswith("artifacts/"):
        return "research-artifact"
    if path.startswith("configs/") or path.startswith("schemas/"):
        return "configuration-or-schema"
    if path.startswith("docs/") or path.endswith(".md"):
        return "documentation"
    if path.startswith("scripts/"):
        return "reproduction-tooling"
    if path.startswith("src/") or path.startswith("tests/"):
        return "software"
    return "package-metadata"


def build_release_manifest(
    root: Path,
    *,
    generated_at: str,
    source_revision: str,
    paths: Iterable[str] | None = None,
    platform_record: dict[str, str] | None = None,
) -> dict[str, Any]:
    selected = tracked_release_paths(root) if paths is None else sorted(
        _safe_relative_path(path) for path in paths if _is_release_path(path)
    )
    if len(selected) != len(set(selected)):
        raise ValueError("release manifest paths must be unique")

    files: list[dict[str, Any]] = []
    total_bytes = 0
    for relative in selected:
        absolute = root / Path(relative)
        if absolute.is_symlink():
            raise ValueError(f"release manifest does not allow symlinks: {relative}")
        if not absolute.is_file():
            raise FileNotFoundError(f"tracked release file is missing: {relative}")
        size = absolute.stat().st_size
        total_bytes += size
        files.append(
            {
                "path": relative,
                "size": size,
                "sha256": sha256_file(absolute),
                "artifact_class": artifact_class(relative),
            }
        )

    return {
        "manifest_schema_version": MANIFEST_SCHEMA_VERSION,
        "generated_at": generated_at,
        "source_revision": source_revision,
        "platform": platform_record
        or {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python": platform.python_version(),
        },
        "manifest_excludes": sorted(EXCLUDED_PATHS),
        "file_count": len(files),
        "uncompressed_bytes_excluding_manifest": total_bytes,
        "files": files,
    }


def write_release_manifest(path: Path, manifest: dict[str, Any]) -> None:
    path.write_text(_canonical_json(manifest), encoding="utf-8", newline="\n")


def package_version(root: Path) -> str:
    try:
        metadata = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        raise ValueError(f"project metadata is unreadable: {exc}") from exc
    value = metadata.get("project", {}).get("version")
    if not isinstance(value, str) or not value.strip():
        raise ValueError("pyproject project.version must be a non-empty string")
    return value.strip()


def build_release_metadata(root: Path, manifest_path: Path) -> dict[str, Any]:
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"release manifest is unreadable for metadata generation: {exc}") from exc
    return {
        "release_metadata_schema_version": RELEASE_METADATA_SCHEMA_VERSION,
        "source_revision": manifest.get("source_revision"),
        "generated_at": manifest.get("generated_at"),
        "package_version": package_version(root),
        "manifest_sha256": sha256_file(manifest_path),
        "file_count": manifest.get("file_count"),
    }


def write_release_metadata(path: Path, metadata: dict[str, Any]) -> None:
    path.write_text(_canonical_json(metadata), encoding="utf-8", newline="\n")


def _read_json_object(path: Path, *, label: str) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return None, [f"{label} is unreadable: {exc}"]
    if not isinstance(value, dict):
        return None, [f"{label} must be a JSON object"]
    return value, []


def validate_release_metadata(root: Path) -> list[str]:
    metadata_path = root / RELEASE_METADATA_PATH
    manifest_path = root / MANIFEST_PATH
    metadata, problems = _read_json_object(metadata_path, label="release metadata")
    manifest, manifest_problems = _read_json_object(manifest_path, label="release manifest")
    problems.extend(manifest_problems)
    if metadata is None or manifest is None:
        return problems

    expected_fields = {
        "release_metadata_schema_version",
        "source_revision",
        "generated_at",
        "package_version",
        "manifest_sha256",
        "file_count",
    }
    if set(metadata) != expected_fields:
        problems.append("release metadata fields do not match the fixed schema")
    if metadata.get("release_metadata_schema_version") != RELEASE_METADATA_SCHEMA_VERSION:
        problems.append("unsupported release metadata schema version")
    revision = metadata.get("source_revision")
    if not isinstance(revision, str) or re.fullmatch(r"[0-9a-f]{40}", revision) is None:
        problems.append("release metadata source_revision must be a full lowercase Git SHA")
    generated_at = metadata.get("generated_at")
    if not isinstance(generated_at, str) or not generated_at.strip():
        problems.append("release metadata generated_at must be a non-empty string")
    manifest_hash = metadata.get("manifest_sha256")
    if not isinstance(manifest_hash, str) or re.fullmatch(r"[0-9a-f]{64}", manifest_hash) is None:
        problems.append("release metadata manifest_sha256 must be a lowercase SHA-256")
    elif manifest_hash != sha256_file(manifest_path):
        problems.append("release metadata manifest_sha256 does not match PACKAGE_MANIFEST.json")
    if metadata.get("file_count") != manifest.get("file_count"):
        problems.append("release metadata file_count does not match PACKAGE_MANIFEST.json")
    if metadata.get("source_revision") != manifest.get("source_revision"):
        problems.append("release metadata source_revision does not match PACKAGE_MANIFEST.json")
    if metadata.get("generated_at") != manifest.get("generated_at"):
        problems.append("release metadata generated_at does not match PACKAGE_MANIFEST.json")
    try:
        expected_version = package_version(root)
    except ValueError as exc:
        problems.append(str(exc))
    else:
        if metadata.get("package_version") != expected_version:
            problems.append("release metadata package_version does not match pyproject.toml")
    return problems


def source_revision(root: Path) -> str:
    if release_mode(root) == "archive":
        metadata, problems = _read_json_object(
            root / RELEASE_METADATA_PATH, label="release metadata"
        )
        if metadata is None:
            raise RuntimeError("archive source revision unavailable: " + "; ".join(problems))
        revision = metadata.get("source_revision")
        if not isinstance(revision, str) or re.fullmatch(r"[0-9a-f]{40}", revision) is None:
            raise RuntimeError(
                "archive source revision unavailable: release metadata source_revision "
                "must be a full lowercase Git SHA"
            )
        return revision

    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        raise RuntimeError(f"repository source revision unavailable: {exc}") from exc
    revision = result.stdout.strip()
    if result.returncode or re.fullmatch(r"[0-9a-f]{40}", revision) is None:
        detail = result.stderr.strip() or "git rev-parse HEAD failed"
        raise RuntimeError(f"repository source revision unavailable: {detail}")
    return revision


def _archive_tree_paths(root: Path) -> tuple[set[str], list[str]]:
    paths: set[str] = set()
    problems: list[str] = []
    for directory, dirnames, filenames in os.walk(root, followlinks=False):
        base = Path(directory)
        for name in [*dirnames, *filenames]:
            absolute = base / name
            relative = absolute.relative_to(root).as_posix()
            if absolute.is_symlink():
                problems.append(f"archive tree contains symlink: {relative}")
                continue
            if absolute.is_dir() and _forbidden_archive_path(relative):
                problems.append(f"archive tree contains forbidden directory: {relative}")
            if absolute.is_file():
                paths.add(relative)
    return paths, problems


def _forbidden_archive_path(path: str) -> bool:
    parts = PurePosixPath(path).parts
    cache_names = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".venv"}
    return (
        any(part in cache_names for part in parts)
        or path == "data/external"
        or path.startswith("data/external/")
    )


def verify_release_manifest(
    root: Path,
    manifest: dict[str, Any],
    *,
    require_complete_tracked_tree: bool = False,
) -> list[str]:
    problems: list[str] = []
    if manifest.get("manifest_schema_version") != MANIFEST_SCHEMA_VERSION:
        problems.append("unsupported release manifest schema version")
    rows = manifest.get("files")
    if not isinstance(rows, list):
        return [*problems, "release manifest files must be an array"]

    seen: set[str] = set()
    total_bytes = 0
    for index, row in enumerate(rows):
        required = {"path", "size", "sha256", "artifact_class"}
        if not isinstance(row, dict) or set(row) != required:
            problems.append(
                f"files[{index}] must contain only path, size, sha256, and artifact_class"
            )
            continue
        try:
            relative = _safe_relative_path(row["path"])
        except (TypeError, ValueError) as exc:
            problems.append(f"files[{index}] has invalid path: {exc}")
            continue
        if not _is_release_path(relative):
            problems.append(f"files[{index}] is excluded from release: {relative}")
            continue
        if relative in seen:
            problems.append(f"duplicate release path: {relative}")
            continue
        seen.add(relative)
        absolute = root / Path(relative)
        if absolute.is_symlink() or not absolute.is_file():
            problems.append(f"missing or non-regular release file: {relative}")
            continue
        actual_size = absolute.stat().st_size
        if row["size"] != actual_size:
            problems.append(f"size mismatch: {relative}")
        actual_hash = sha256_file(absolute)
        if row["sha256"] != actual_hash:
            problems.append(f"sha256 mismatch: {relative}")
        if row["artifact_class"] != artifact_class(relative):
            problems.append(f"artifact class mismatch: {relative}")
        total_bytes += actual_size

    if manifest.get("file_count") != len(rows):
        problems.append("release manifest file_count mismatch")
    if manifest.get("uncompressed_bytes_excluding_manifest") != total_bytes:
        problems.append("release manifest total byte count mismatch")
    if require_complete_tracked_tree:
        if release_mode(root) == "repository":
            try:
                tracked = set(tracked_release_paths(root))
            except (OSError, subprocess.SubprocessError, UnicodeDecodeError) as exc:
                problems.append(f"repository release completeness check failed: {exc}")
            else:
                missing = sorted(tracked - seen)
                unexpected = sorted(seen - tracked)
                if missing:
                    problems.append(f"release manifest omits tracked files: {missing}")
                if unexpected:
                    problems.append(f"release manifest contains untracked files: {unexpected}")
        else:
            problems.extend(validate_release_metadata(root))
            bound_manifest, bound_problems = _read_json_object(
                root / MANIFEST_PATH, label="release manifest"
            )
            problems.extend(bound_problems)
            if bound_manifest is not None and isinstance(bound_manifest.get("files"), list):
                bound_paths = {
                    row.get("path")
                    for row in bound_manifest["files"]
                    if isinstance(row, dict) and isinstance(row.get("path"), str)
                }
                omitted = sorted(bound_paths - seen)
                if omitted:
                    problems.append(f"release manifest omits archive files: {omitted}")
            actual, tree_problems = _archive_tree_paths(root)
            problems.extend(tree_problems)
            forbidden = sorted(path for path in actual if _forbidden_archive_path(path))
            if forbidden:
                problems.append(f"archive tree contains forbidden paths: {forbidden}")
            expected = {*seen, MANIFEST_PATH, RELEASE_METADATA_PATH}
            missing = sorted(expected - actual)
            unexpected = sorted(actual - expected)
            if missing:
                problems.append(f"archive tree is missing manifest files: {missing}")
            if unexpected:
                problems.append(f"archive tree contains unexpected files: {unexpected}")
    return problems


def declared_project_license(root: Path) -> str | None:
    pyproject = root / "pyproject.toml"
    try:
        metadata = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError):
        return None
    value = metadata.get("project", {}).get("license")
    if not isinstance(value, str):
        return None
    value = value.strip()
    if not value or value.upper() == "NOASSERTION":
        return None
    return value


def project_license_selected(root: Path) -> bool:
    license_path = root / "LICENSE"
    if (root / "LICENSE_NOT_SELECTED.md").exists() or not license_path.is_file():
        return False
    try:
        license_text = license_path.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeDecodeError):
        return False
    return bool(license_text) and declared_project_license(root) is not None


def validate_project_license_metadata(root: Path) -> list[str]:
    declared = declared_project_license(root)
    if declared is None:
        return ["pyproject project.license must contain the selected SPDX expression"]
    try:
        sbom = json.loads(
            (
                root
                / (
                    f"{_v03_release_relative(root)}/sbom.spdx.json"
                    if _is_v03_package(root)
                    else "artifacts/release/sbom.spdx.json"
                )
            ).read_text(encoding="utf-8")
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return [f"release SBOM is unreadable for license validation: {exc}"]
    packages = sbom.get("packages")
    if not isinstance(packages, list):
        return ["release SBOM packages must be an array for license validation"]
    project_rows = [
        row
        for row in packages
        if isinstance(row, dict) and row.get("name") == "sparkbrain-research"
    ]
    if len(project_rows) != 1:
        return ["release SBOM must contain exactly one sparkbrain-research package"]
    project = project_rows[0]
    problems = []
    for field in ("licenseDeclared", "licenseConcluded"):
        if project.get(field) != declared:
            problems.append(f"release SBOM {field} does not match pyproject project.license")
    if "owner-blocked" in str(project.get("comment", "")):
        problems.append("release SBOM still marks the project license as owner-blocked")
    return problems


def validate_evidence_map(root: Path, evidence_map: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if evidence_map.get("schema_version") != "c10-evidence-map-v1":
        problems.append("unsupported evidence-map schema version")
    entries = evidence_map.get("entries")
    if not isinstance(entries, list):
        return [*problems, "evidence-map entries must be an array"]
    claim_text = (root / "docs/CLAIMS_REGISTER.md").read_text(encoding="utf-8")
    seen: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            problems.append(f"evidence-map entries[{index}] must be an object")
            continue
        entry_id = entry.get("id")
        if not isinstance(entry_id, str) or not entry_id:
            problems.append(f"evidence-map entries[{index}] has no id")
            continue
        if entry_id in seen:
            problems.append(f"duplicate evidence-map id: {entry_id}")
        seen.add(entry_id)
        status = entry.get("status")
        if status not in {"accepted", "pending", "negative"}:
            problems.append(f"invalid evidence status for {entry_id}: {status!r}")
        claim_ids = entry.get("claim_ids")
        if not isinstance(claim_ids, list) or not claim_ids:
            problems.append(f"evidence entry {entry_id} has no claim_ids")
        else:
            for claim_id in claim_ids:
                if not isinstance(claim_id, str) or claim_id not in claim_text:
                    problems.append(f"unknown claim id in {entry_id}: {claim_id!r}")
        paths = entry.get("artifacts", [])
        if not isinstance(paths, list):
            problems.append(f"artifacts for {entry_id} must be an array")
            continue
        for relative in paths:
            try:
                safe = _safe_relative_path(relative)
            except (TypeError, ValueError) as exc:
                problems.append(f"unsafe evidence path in {entry_id}: {exc}")
                continue
            if not (root / safe).is_file():
                problems.append(f"missing evidence artifact for {entry_id}: {safe}")
    return problems


def validate_source_revision(root: Path, payload: dict[str, Any], *, label: str) -> list[str]:
    revision = payload.get("source_revision")
    if not isinstance(revision, str) or re.fullmatch(r"[0-9a-f]{40}", revision) is None:
        return [f"{label} source_revision must be a full lowercase Git SHA"]
    if release_mode(root) == "archive":
        metadata, problems = _read_json_object(
            root / RELEASE_METADATA_PATH, label="release metadata"
        )
        if metadata is None:
            return problems
        if revision != metadata.get("source_revision"):
            return [f"{label} source_revision does not match release metadata"]
        return []
    try:
        result = subprocess.run(
            ["git", "merge-base", "--is-ancestor", revision, "HEAD"],
            cwd=root,
            capture_output=True,
            check=False,
        )
    except OSError as exc:
        return [f"{label} source_revision ancestry check failed: {exc}"]
    if result.returncode != 0:
        return [f"{label} source_revision is not an ancestor of HEAD"]
    return []


def validate_release_revision_consistency(root: Path) -> list[str]:
    payloads: dict[str, dict[str, Any]] = {}
    evidence_path = (
        root / f"{_v03_release_relative(root)}/evidence_map.json"
        if _is_v03_package(root)
        else root / "artifacts/release/evidence_map.json"
    )
    paths = {
        "package manifest": root / MANIFEST_PATH,
        "release evidence map": evidence_path,
    }
    if not _is_v03_package(root):
        paths["release provenance"] = root / "artifacts/release/provenance.json"
    if (root / RELEASE_METADATA_PATH).is_file() or release_mode(root) == "archive":
        paths["release metadata"] = root / RELEASE_METADATA_PATH
    problems: list[str] = []
    for label, path in paths.items():
        payload, read_problems = _read_json_object(path, label=label)
        problems.extend(read_problems)
        if payload is not None:
            payloads[label] = payload
    revisions: dict[str, str] = {}
    for label, payload in payloads.items():
        revision = payload.get("source_revision")
        if not isinstance(revision, str) or re.fullmatch(r"[0-9a-f]{40}", revision) is None:
            problems.append(f"{label} source_revision must be a full lowercase Git SHA")
        else:
            revisions[label] = revision
    if len(set(revisions.values())) > 1:
        detail = ", ".join(f"{label}={revision}" for label, revision in revisions.items())
        problems.append(f"release source_revision values do not match: {detail}")
    return problems


def validate_generated_release_evidence(root: Path) -> list[str]:
    if _is_v03_package(root):
        return validate_v03_generated_release_evidence(root)
    problems: list[str] = []
    release_dir = root / "artifacts/release"
    try:
        subset = json.loads((release_dir / "primary_subset.json").read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return [f"primary subset is unreadable: {exc}"]
    if subset.get("schema_version") != "c10-primary-subset-v1":
        problems.append("unsupported primary-subset schema version")
    if subset.get("full_evaluation") is not False:
        problems.append("primary subset must state that it is not the full evaluation")
    for section in ("inputs", "outputs"):
        rows = subset.get(section)
        if not isinstance(rows, dict) or not rows:
            problems.append(f"primary subset {section} must be a non-empty object")
            continue
        for relative, expected in rows.items():
            try:
                safe = _safe_relative_path(relative)
            except (TypeError, ValueError) as exc:
                problems.append(f"unsafe primary subset path: {exc}")
                continue
            path = root / safe
            if not path.is_file():
                problems.append(f"missing primary subset {section[:-1]}: {safe}")
            elif expected != sha256_file(path):
                problems.append(f"primary subset {section[:-1]} hash mismatch: {safe}")

    try:
        provenance = json.loads((release_dir / "provenance.json").read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        problems.append(f"release provenance is unreadable: {exc}")
    else:
        if provenance.get("schema_version") != "c10-provenance-v1":
            problems.append("unsupported release-provenance schema version")
        problems.extend(validate_source_revision(root, provenance, label="release provenance"))
        products = provenance.get("products")
        if not isinstance(products, dict) or not products:
            problems.append("release provenance products must be a non-empty object")
        else:
            for product, inputs in products.items():
                if not (root / _safe_relative_path(product)).is_file():
                    problems.append(f"missing provenance product: {product}")
                if not isinstance(inputs, list) or not inputs:
                    problems.append(f"provenance product has no inputs: {product}")
                    continue
                for relative in inputs:
                    if not (root / _safe_relative_path(relative)).is_file():
                        problems.append(f"missing provenance input for {product}: {relative}")

    try:
        audit = json.loads((release_dir / "claim_audit.json").read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        problems.append(f"claim audit is unreadable: {exc}")
    else:
        if audit.get("schema_version") != "c10-claim-audit-v1":
            problems.append("unsupported claim-audit schema version")
        if audit.get("status") not in {"pass", "pass-with-pending-evidence"}:
            problems.append("claim audit has unresolved prohibited wording findings")
        if audit.get("prohibited_wording_findings") != []:
            problems.append("claim audit prohibited-wording findings must be empty")

    try:
        sbom = json.loads((release_dir / "sbom.spdx.json").read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        problems.append(f"SBOM is unreadable: {exc}")
    else:
        if sbom.get("spdxVersion") != "SPDX-2.3":
            problems.append("SBOM must declare SPDX-2.3")
        package_names = {
            row.get("name") for row in sbom.get("packages", []) if isinstance(row, dict)
        }
        if "sparkbrain-research" not in package_names:
            problems.append("SBOM does not identify the SparkBrain package")

    c04_manifest = root / "artifacts/phase2/learned-routing-v1/main/manifest-evidence.json"
    if c04_manifest.is_file():
        evidence = json.loads(c04_manifest.read_text(encoding="utf-8"))
        for split in ("dev", "test"):
            relative = evidence.get("paths", {}).get(split)
            expected = evidence.get("sha256_after", {}).get(split)
            if not isinstance(relative, str) or not isinstance(expected, str):
                problems.append(f"C04 immutable {split} manifest evidence is incomplete")
                continue
            normalized = relative.replace("\\", "/")
            if not (root / normalized).is_file() or sha256_file(root / normalized) != expected:
                problems.append(f"C04 immutable {split} manifest hash mismatch")
    return problems


def validate_v03_generated_release_evidence(
    root: Path, *, release_version: str | None = None
) -> list[str]:
    """Validate generated C20 artifacts without reclassifying their evidence."""

    from sparkbrain import release_v03_artifacts

    selected_version = release_version or (
        "0.3.1" if _v03_release_relative(root) == "artifacts/release/v0.3.1" else "0.3.0"
    )
    if selected_version not in {"0.3.0", "0.3.1"}:
        return ["unsupported v0.3 release evidence package version"]
    release_relative = release_v03_artifacts.release_relative_for_version(selected_version)
    release_dir = root / release_relative
    try:
        evidence = json.loads((release_dir / "evidence_map.json").read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return [f"v0.3 evidence map is unreadable: {exc}"]
    problems = release_v03_artifacts.validate_v03_evidence_map(
        root, evidence, release_version=selected_version
    )
    problems.extend(validate_source_revision(root, evidence, label="v0.3 evidence map"))
    revision = evidence.get("source_revision")
    if not isinstance(revision, str):
        return _unique_problems(problems)

    expected_text = {
        "release_report.md": release_v03_artifacts._render_results_table(evidence),
        "release_figure.svg": release_v03_artifacts._render_results_figure(evidence),
        "claim_boundary_figure.svg": release_v03_artifacts._render_claim_boundary_figure(
            evidence
        ),
        "sbom.spdx.json": release_v03_artifacts._canonical_json(
            release_v03_artifacts.build_v03_sbom(
                root, source_revision=revision, release_version=selected_version
            )
        ),
        "primary_subset.json": release_v03_artifacts._canonical_json(
            release_v03_artifacts.build_v03_primary_subset(evidence)
        ),
        "source_license_inventory.json": release_v03_artifacts._canonical_json(
            release_v03_artifacts.build_v03_source_license_inventory(
                root, source_revision=revision, release_version=selected_version
            )
        ),
    }
    for name, expected in expected_text.items():
        path = release_dir / name
        try:
            actual = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            problems.append(f"v0.3 generated artifact is unreadable: {name}: {exc}")
        else:
            if actual != expected:
                problems.append(f"v0.3 generated artifact does not match evidence map: {name}")

    try:
        source_manifest = json.loads(
            (release_dir / "source_manifest.json").read_text(encoding="utf-8")
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        problems.append(f"v0.3 source manifest is unreadable: {exc}")
        return _unique_problems(problems)
    expected_files = {
        f"{release_relative}/{name}"
        for name in ("evidence_map.json", *expected_text)
    }
    if (
        not isinstance(source_manifest, dict)
        or source_manifest.get("schema_version")
        != release_v03_artifacts._release_contract(selected_version)["source_manifest_schema"]
        or source_manifest.get("package_version") != selected_version
        or source_manifest.get("source_revision") != revision
        or not isinstance(source_manifest.get("files"), list)
    ):
        problems.append("v0.3 source manifest does not match fixed schema")
        return _unique_problems(problems)
    rows = source_manifest["files"]
    paths = [row.get("path") for row in rows if isinstance(row, dict)]
    if paths != sorted(expected_files) or len(rows) != len(expected_files):
        problems.append("v0.3 source manifest files do not match generated artifacts")
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"path", "sha256"}:
            problems.append("v0.3 source manifest row does not match fixed schema")
            continue
        relative = row["path"]
        if not isinstance(relative, str) or relative not in expected_files:
            problems.append("v0.3 source manifest contains an unexpected path")
            continue
        if row["sha256"] != sha256_file(root / relative):
            problems.append(f"v0.3 source manifest hash mismatch: {relative}")
    expected_linked = {
        "reproduction_manifest.json": release_v03_artifacts._canonical_json(
            release_v03_artifacts.build_v03_reproduction_manifest(source_manifest)
        ),
        "release_metadata.json": release_v03_artifacts._canonical_json(
            release_v03_artifacts.build_v03_release_metadata(source_manifest)
        ),
    }
    for name, expected in expected_linked.items():
        try:
            actual = (release_dir / name).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            problems.append(f"v0.3 generated artifact is unreadable: {name}: {exc}")
        else:
            if actual != expected:
                problems.append(f"v0.3 generated artifact does not match source manifest: {name}")
    return _unique_problems(problems)


def _unique_problems(problems: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(problems))


def preparation_problems(root: Path) -> list[str]:
    required = required_preparation_files(root)
    problems = [
        f"missing required release artifact: {relative}"
        for relative in required
        if not (root / relative).is_file()
    ]
    evidence_path = (
        root / f"{_v03_release_relative(root)}/evidence_map.json"
        if _is_v03_package(root)
        else root / "artifacts/release/evidence_map.json"
    )
    if evidence_path.is_file():
        try:
            evidence_map = json.loads(evidence_path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            problems.append(f"evidence map is not valid UTF-8 JSON: {exc}")
        else:
            if _is_v03_package(root):
                from sparkbrain.release_v03_artifacts import validate_v03_evidence_map

                problems.extend(validate_v03_evidence_map(root, evidence_map))
            else:
                problems.extend(validate_evidence_map(root, evidence_map))
            problems.extend(validate_source_revision(root, evidence_map, label="evidence map"))
    if all((root / relative).is_file() for relative in required):
        problems.extend(validate_generated_release_evidence(root))
    return _unique_problems(problems)


def integrity_problems(root: Path) -> list[str]:
    problems: list[str] = []
    if (root / RELEASE_METADATA_PATH).is_file() or release_mode(root) == "archive":
        problems.extend(validate_release_metadata(root))
    problems.extend(validate_release_revision_consistency(root))

    manifest_path = root / MANIFEST_PATH
    if not manifest_path.is_file():
        problems.append(f"missing required release artifact: {MANIFEST_PATH}")
        return _unique_problems(problems)
    manifest, read_problems = _read_json_object(manifest_path, label="release manifest")
    problems.extend(read_problems)
    if manifest is not None:
        problems.extend(
            verify_release_manifest(root, manifest, require_complete_tracked_tree=True)
        )
        manifest_paths = {
            row.get("path") for row in manifest.get("files", []) if isinstance(row, dict)
        }
        leaked = sorted(
            path
            for path in manifest_paths
            if isinstance(path, str) and path.startswith("data/external/")
        )
        if leaked:
            problems.append(f"external dataset cache is included in release: {leaked}")
    return _unique_problems(problems)


def owner_blockers(root: Path) -> list[str]:
    return [] if project_license_selected(root) else [OWNER_LICENSE_BLOCKER]


def evidence_blockers(root: Path) -> list[str]:
    evidence_path = (
        root / f"{_v03_release_relative(root)}/evidence_map.json"
        if _is_v03_package(root)
        else root / "artifacts/release/evidence_map.json"
    )
    if not evidence_path.is_file():
        return []
    evidence, read_problems = _read_json_object(evidence_path, label="evidence map")
    if read_problems or evidence is None:
        return []
    return [
        f"pending release evidence gate: {entry['id']}"
        for entry in evidence.get("entries", [])
        if isinstance(entry, dict) and entry.get("status") == "pending"
    ]


def release_validation(
    root: Path, *, require_public: bool = True
) -> dict[str, list[str]]:
    integrity = integrity_problems(root)
    preparation = preparation_problems(root)
    owners = owner_blockers(root)
    evidence = evidence_blockers(root) if require_public else []
    if require_public and not owners:
        integrity.extend(
            f"missing required release artifact: {relative}"
            for relative in REQUIRED_PUBLIC_FILES
            if not (root / relative).is_file()
        )
        integrity.extend(validate_project_license_metadata(root))
    return {
        "integrity_problems": _unique_problems(integrity),
        "preparation_problems": _unique_problems(preparation),
        "owner_blockers": _unique_problems(owners),
        "evidence_blockers": _unique_problems(evidence),
    }


def non_public_integrity_problems(root: Path) -> list[str]:
    validation = release_validation(root, require_public=False)
    return _unique_problems(
        [
            *validation["integrity_problems"],
            *validation["preparation_problems"],
            *validation["evidence_blockers"],
        ]
    )


def validate_release_tree(root: Path, *, require_public: bool = True) -> list[str]:
    validation = release_validation(root, require_public=require_public)
    return _unique_problems(
        [
            *validation["integrity_problems"],
            *validation["preparation_problems"],
            *validation["owner_blockers"],
            *validation["evidence_blockers"],
        ]
    )


def build_release_archive(root: Path, output: Path, *, source_date_epoch: int) -> dict[str, Any]:
    if not project_license_selected(root):
        raise PermissionError("public archive blocked: project license is not selected")
    problems = validate_release_tree(root, require_public=True)
    if problems:
        raise ValueError("release tree is not ready: " + "; ".join(problems))
    metadata_problems = validate_release_metadata(root)
    if metadata_problems:
        raise ValueError("release metadata is not ready: " + "; ".join(metadata_problems))
    manifest = json.loads((root / MANIFEST_PATH).read_text(encoding="utf-8"))
    paths = [row["path"] for row in manifest["files"]]
    # ZIP cannot represent dates before 1980. The caller supplies the frozen release epoch.
    import datetime

    date = datetime.datetime.fromtimestamp(max(source_date_epoch, 315532800), tz=datetime.UTC)
    timestamp = (date.year, date.month, date.day, date.hour, date.minute, date.second)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for relative in sorted([*paths, MANIFEST_PATH, RELEASE_METADATA_PATH]):
            info = zipfile.ZipInfo(relative, date_time=timestamp)
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, (root / relative).read_bytes())
    checksum = sha256_file(output)
    checksum_path = output.with_suffix(output.suffix + ".sha256")
    checksum_path.write_text(f"{checksum}  {output.name}\n", encoding="ascii", newline="\n")
    return {"archive": str(output), "sha256": checksum, "checksum_file": str(checksum_path)}
