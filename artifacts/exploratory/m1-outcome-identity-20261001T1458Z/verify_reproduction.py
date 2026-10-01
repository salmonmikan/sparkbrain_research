"""Compare saved M1 runs with authenticated retained records; execute no runtime."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any


class VerificationError(ValueError):
    """A saved run does not satisfy the portable reproduction contract."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        require(key not in result, f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise VerificationError(f"Non-finite JSON number: {value}")


def parse_json(raw: bytes, label: str) -> Any:
    try:
        return json.loads(raw, object_pairs_hook=unique_object, parse_constant=reject_constant)
    except (ValueError, UnicodeError) as error:
        raise VerificationError(f"Invalid JSON in {label}: {error}") from error


def object_json(raw: bytes, label: str) -> dict[str, Any]:
    value = parse_json(raw, label)
    require(isinstance(value, dict), f"Expected JSON object: {label}")
    return value


def canonical(value: Any) -> str:
    # Comparing serialized values also distinguishes booleans from numbers and 1 from 1.0.
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def inventory(root: Path) -> dict[str, Path]:
    require(root.is_dir() and not root.is_symlink(), f"Not a regular run directory: {root}")
    files = {}
    for path in root.rglob("*"):
        require(not path.is_symlink(), f"Symlink is not a retained run file: {path}")
        if path.is_dir():
            continue
        require(path.is_file(), f"Not a regular run file: {path}")
        files[path.relative_to(root).as_posix()] = path
    return files


def require_inventory(actual: dict, expected: dict, label: str) -> None:
    missing = sorted(expected.keys() - actual.keys())
    extra = sorted(actual.keys() - expected.keys())
    require(
        not missing and not extra,
        f"Inventory mismatch in {label}: missing={missing}, extra={extra}",
    )


def manifest_runs(artifact: Path) -> tuple[dict[str, dict[str, str]], str]:
    metadata = object_json((artifact / "BUNDLE.json").read_bytes(), "BUNDLE.json")
    raw = (artifact / "review/ARTIFACT_MANIFEST.json").read_bytes()
    digest = sha256(raw)
    require(
        digest == metadata.get("artifact_manifest_sha256"), "Artifact manifest SHA-256 mismatch"
    )
    manifest = object_json(raw, "review/ARTIFACT_MANIFEST.json")
    files = manifest.get("files")
    require(isinstance(files, dict), "Artifact manifest must declare files")
    runs: dict[str, dict[str, str]] = {"r2-run1": {}, "r2-run37": {}}
    for relative, file_digest in files.items():
        path = PurePosixPath(relative)
        require(
            bool(path.parts)
            and not path.is_absolute()
            and ".." not in path.parts
            and path.as_posix() == relative,
            f"Invalid manifest path: {relative}",
        )
        require(
            isinstance(file_digest, str) and re.fullmatch(r"[0-9a-f]{64}", file_digest) is not None,
            f"Invalid manifest SHA-256: {relative}",
        )
        if path.parts[0] in runs:
            require(len(path.parts) > 1, f"Invalid run file path: {relative}")
            runs[path.parts[0]][path.relative_to(path.parts[0]).as_posix()] = file_digest
    for run, declared in runs.items():
        require(
            {"calls.jsonl", "COMPLETED.json", "environment.json", "summary.json"}
            <= declared.keys(),
            f"Missing required run files in manifest: {run}",
        )
    require_inventory(runs["r2-run1"], runs["r2-run37"], "declared retained runs")
    return runs, digest


def without_traceback(value: Any, label: str) -> Any:
    if value is None:
        return None
    require(isinstance(value, dict), f"Expected exception object or null: {label}")
    require(
        set(value) == {"type", "message", "traceback"}
        and all(isinstance(value[key], str) for key in ("type", "message", "traceback")),
        f"Expected exception type/message/traceback string fields: {label}",
    )
    return {key: item for key, item in value.items() if key != "traceback"}


def normalize_record(record: Any, label: str) -> dict[str, Any]:
    require(isinstance(record, dict) and "exception" in record, f"Invalid call record: {label}")
    return {**record, "exception": without_traceback(record["exception"], f"{label}.exception")}


def normalize_case(case: Any, label: str) -> dict[str, Any]:
    require(isinstance(case, dict), f"Expected case summary object: {label}")
    result = dict(case)
    for key in ("probe_exception", "redelivery_exception", "fourth_exception"):
        require(key in result, f"Missing {key}: {label}")
        result[key] = without_traceback(result[key], f"{label}.{key}")
    return result


def normalized_json(relative: str, raw: bytes, label: str) -> Any:
    if relative == "calls.jsonl":
        return [
            normalize_record(parse_json(line, f"{label}:{index}"), f"{label}:{index}")
            for index, line in enumerate(raw.splitlines(), 1)
        ]
    value = object_json(raw, label)
    if relative == "COMPLETED.json":
        # The raw calls digest is checked independently for every run before comparison.
        return {key: item for key, item in value.items() if key != "calls_sha256"}
    if relative == "summary.json":
        require(isinstance(value.get("cases"), list), f"Expected aggregate cases: {label}")
        return {
            **value,
            "cases": [
                normalize_case(case, f"{label}.cases[{i}]") for i, case in enumerate(value["cases"])
            ],
        }
    if relative.endswith("/record.json"):
        return normalize_record(value, label)
    return normalize_case(value, label)


def semantic_json_path(relative: str) -> bool:
    parts = PurePosixPath(relative).parts
    return (
        relative in {"calls.jsonl", "COMPLETED.json", "summary.json"}
        or (len(parts) == 2 and parts[1] == "summary.json")
        or (
            len(parts) == 3
            and re.fullmatch(r"call-[0-9]{2}", parts[1]) is not None
            and parts[2] == "record.json"
        )
    )


def validate_calls_digest(files: dict[str, bytes], label: str) -> str:
    completed = object_json(files["COMPLETED.json"], f"{label}/COMPLETED.json")
    digest = sha256(files["calls.jsonl"])
    require(
        completed.get("calls_sha256") == digest, f"Invalid calls_sha256 in {label}/COMPLETED.json"
    )
    return digest


def validate_verification(path: Path) -> None:
    final = object_json(path.read_bytes(), str(path))
    for run in ("run1", "run37"):
        result = final.get(run)
        require(isinstance(result, dict), f"Missing frozen-verifier result: {run}")
        require(
            result.get("all_expected_checks_pass") is True, f"Frozen-verifier checks failed: {run}"
        )
        checks = result.get("checks")
        require(
            isinstance(checks, dict)
            and len(checks) == 29
            and all(v is True for v in checks.values()),
            f"Expected 29 passing frozen-verifier checks: {run}",
        )
    reproduction = final.get("reproducibility")
    require(
        isinstance(reproduction, dict)
        and reproduction.get("reproducible_all_runtime_records_and_checkpoints") is True,
        "Frozen-verifier primary/replica reproduction check failed",
    )


def verify(
    verification: Path, primary: Path, replica: Path, retained_root: Path, artifact: Path
) -> dict[str, Any]:
    """Authenticate retained files, then compare complete saved semantics and state."""
    declared_runs, manifest_digest = manifest_runs(artifact)
    validate_verification(verification)
    results = {}
    for run, fresh_root in (("r2-run1", primary), ("r2-run37", replica)):
        declared = declared_runs[run]
        retained_paths = inventory(retained_root / run)
        fresh_paths = inventory(fresh_root)
        require_inventory(retained_paths, declared, f"retained {run}")
        require_inventory(fresh_paths, declared, f"fresh {run}")
        retained = {name: path.read_bytes() for name, path in retained_paths.items()}
        fresh = {name: path.read_bytes() for name, path in fresh_paths.items()}
        for name, digest in declared.items():
            require(
                sha256(retained[name]) == digest,
                f"Retained manifest SHA-256 mismatch: {run}/{name}",
            )
        retained_digest = validate_calls_digest(retained, f"retained {run}")
        fresh_digest = validate_calls_digest(fresh, f"fresh {run}")
        provenance_differences = []
        byte_exact_count = 0
        semantic_count = 0
        for name in sorted(declared):
            label = f"{run}/{name}"
            if name == "environment.json":
                continue
            if semantic_json_path(name):
                expected = normalized_json(name, retained[name], f"retained {label}")
                actual = normalized_json(name, fresh[name], f"fresh {label}")
                require(
                    canonical(actual) == canonical(expected), f"Semantic/state mismatch: {label}"
                )
                semantic_count += 1
                if retained[name] != fresh[name]:
                    provenance_differences.append(name)
            else:
                require(fresh[name] == retained[name], f"Physical file byte mismatch: {label}")
                byte_exact_count += 1
        retained_environment = object_json(
            retained["environment.json"], f"retained {run}/environment.json"
        )
        fresh_environment = object_json(fresh["environment.json"], f"fresh {run}/environment.json")
        results[run] = {
            "files_verified": len(declared),
            "byte_exact_physical_files": byte_exact_count,
            "semantic_json_files": semantic_count,
            "declared_provenance_or_json_encoding_differences": provenance_differences,
            "calls_sha256": {"retained": retained_digest, "fresh": fresh_digest},
            "environment": {"retained": retained_environment, "fresh": fresh_environment},
            "environment_changed": retained["environment.json"] != fresh["environment.json"],
        }
    return {
        "comparison": "portable semantic/state reproduction",
        "artifact_manifest_sha256": manifest_digest,
        "runs": results,
        "scientific_credit": 0,
        "runtime_executed_by_verifier": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verification", type=Path, required=True)
    parser.add_argument("--primary", type=Path, required=True)
    parser.add_argument("--replica", type=Path, required=True)
    parser.add_argument("--retained-root", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = verify(
            args.verification,
            args.primary,
            args.replica,
            args.retained_root,
            Path(__file__).resolve().parent,
        )
    except (OSError, ValueError) as error:
        print(f"Reproduction verification failed: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
