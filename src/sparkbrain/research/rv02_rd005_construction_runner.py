"""Fresh-output construction runner for prospective RV02 RD005 development.

The runner materializes only the preregistered D1 construction artifact and
passes it through the independent construction verifier. It never instantiates
an RD005 capability learner/probe, scores an outcome, opens held-out output, or
grants formal authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path
from typing import Any

from .rv02_rd005_artifact_verifier import verify_rd005_artifact_for_future_capability
from .rv02_rd005_construction_artifact import (
    RD005_FRESH_SEED,
    SeedCollisionRecord,
    build_rd005_construction_artifact,
)
from .rv02_rd005_development_package import (
    RD005_OUTPUT_ROOT,
    RD005CollisionRegistry,
    RD005SourceManifest,
    RD005SourceManifestEntry,
)
from .rv02_rd005_source_binding import verify_rd005_source_checkout

_INPUT_KEYS = frozenset(
    {
        "source_git_sha",
        "source_manifest_sha256",
        "source_manifest",
        "collision_registry_sha256",
        "package_plan_sha256",
        "collision_registry",
    }
)
_REGISTRY_KEYS = frozenset(
    {
        "registry_id",
        "source_paths",
        "consumed_or_reserved_seed_ids",
        "consumed_or_reserved_world_ids",
        "authoritative_complete",
    }
)
_SOURCE_MANIFEST_KEYS = frozenset({"source_git_sha", "entries"})
_SOURCE_MANIFEST_ENTRY_KEYS = frozenset({"path", "sha256"})


def _sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _canonical_json(value: object) -> bytes:
    return (
        json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def _write_json(path: Path, value: object) -> None:
    path.write_bytes(_canonical_json(value))


def _require_hash(value: object, *, label: str, length: int) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{label} must be a string")
    if len(value) != length or any(char not in "0123456789abcdef" for char in value):
        raise ValueError(f"{label} must be a {length}-character lowercase hex digest")
    return value


def _require_object(
    value: object,
    *,
    label: str,
    expected_keys: frozenset[str],
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TypeError(f"{label} must be a JSON object")
    keys = frozenset(value)
    if keys != expected_keys:
        raise ValueError(
            f"{label} keys must exactly match {sorted(expected_keys)}; "
            f"got {sorted(keys)}"
        )
    return value


def _string_tuple(value: object, *, label: str) -> tuple[str, ...]:
    if not isinstance(value, list) or any(not isinstance(row, str) for row in value):
        raise TypeError(f"{label} must be a JSON array of strings")
    return tuple(value)


def _int_tuple(value: object, *, label: str) -> tuple[int, ...]:
    if not isinstance(value, list) or any(type(row) is not int for row in value):
        raise TypeError(f"{label} must be a JSON array of exact non-boolean integers")
    return tuple(value)


def _load_source_manifest(value: object) -> RD005SourceManifest:
    row = _require_object(
        value,
        label="source_manifest",
        expected_keys=_SOURCE_MANIFEST_KEYS,
    )
    entries_value = row["entries"]
    if not isinstance(entries_value, list):
        raise TypeError("source_manifest.entries must be a JSON array")
    entries: list[RD005SourceManifestEntry] = []
    for index, entry_value in enumerate(entries_value):
        entry = _require_object(
            entry_value,
            label=f"source_manifest.entries[{index}]",
            expected_keys=_SOURCE_MANIFEST_ENTRY_KEYS,
        )
        path = entry["path"]
        digest = entry["sha256"]
        if not isinstance(path, str):
            raise TypeError(f"source_manifest.entries[{index}].path must be a string")
        entries.append(
            RD005SourceManifestEntry(
                path=path,
                sha256=_require_hash(
                    digest,
                    label=f"source_manifest.entries[{index}].sha256",
                    length=64,
                ),
            )
        )
    manifest = RD005SourceManifest(
        source_git_sha=_require_hash(
            row["source_git_sha"],
            label="source_manifest.source_git_sha",
            length=40,
        ),
        entries=tuple(entries),
    )
    manifest.validate()
    return manifest


def _load_input(
    raw: bytes,
) -> tuple[dict[str, str], RD005CollisionRegistry, RD005SourceManifest]:
    try:
        decoded = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("RD005 construction input must be valid UTF-8 JSON") from exc
    payload = _require_object(decoded, label="construction input", expected_keys=_INPUT_KEYS)

    source_manifest = _load_source_manifest(payload["source_manifest"])
    expected_source_sha = _require_hash(
        payload["source_git_sha"],
        label="source_git_sha",
        length=40,
    )
    if source_manifest.source_git_sha != expected_source_sha:
        raise ValueError("RD005 source Git SHA does not match retained source manifest")
    expected_manifest_sha = _require_hash(
        payload["source_manifest_sha256"],
        label="source_manifest_sha256",
        length=64,
    )
    if source_manifest.manifest_sha256 != expected_manifest_sha:
        raise ValueError("RD005 source manifest digest does not match retained manifest")

    registry_row = _require_object(
        payload["collision_registry"],
        label="collision_registry",
        expected_keys=_REGISTRY_KEYS,
    )
    registry = RD005CollisionRegistry(
        registry_id=str(registry_row["registry_id"]),
        source_paths=_string_tuple(registry_row["source_paths"], label="source_paths"),
        consumed_or_reserved_seed_ids=_int_tuple(
            registry_row["consumed_or_reserved_seed_ids"],
            label="consumed_or_reserved_seed_ids",
        ),
        consumed_or_reserved_world_ids=_string_tuple(
            registry_row["consumed_or_reserved_world_ids"],
            label="consumed_or_reserved_world_ids",
        ),
        authoritative_complete=registry_row["authoritative_complete"],
    )
    registry.validate()
    expected_registry_sha = _require_hash(
        payload["collision_registry_sha256"],
        label="collision_registry_sha256",
        length=64,
    )
    if registry.registry_sha256 != expected_registry_sha:
        raise ValueError("RD005 collision registry digest does not match retained registry")
    identities = {
        "source_git_sha": expected_source_sha,
        "source_manifest_sha256": expected_manifest_sha,
        "collision_registry_sha256": expected_registry_sha,
        "package_plan_sha256": _require_hash(
            payload["package_plan_sha256"],
            label="package_plan_sha256",
            length=64,
        ),
    }
    return identities, registry, source_manifest


def _output_dir(*, repo_root: Path, input_sha256: str) -> Path:
    """Return the one canonical output identity for an exact input payload."""

    return repo_root / RD005_OUTPUT_ROOT / f"construction-{input_sha256}"


def run_construction_from_bytes(*, raw: bytes, repo_root: Path) -> Path:
    """Construct RD005 D1 once from the exact already-selected input bytes.

    The caller owns the read boundary. Passing bytes instead of a path prevents a
    verified input from being swapped between a prospective preflight and output
    identity consumption.
    """

    # Parse the full prospective identity and verify the exact checkout before
    # consuming any output path. Source/package identity failure therefore does
    # not create a misleading terminal construction artifact.
    input_sha256 = _sha256_bytes(raw)
    identities, registry, source_manifest = _load_input(raw)
    verified_source = verify_rd005_source_checkout(repo_root, source_manifest)

    output_dir = _output_dir(repo_root=repo_root, input_sha256=input_sha256)
    output_dir.mkdir(parents=True, exist_ok=False)
    (output_dir / "construction_input.json").write_bytes(raw)
    _write_json(
        output_dir / "input_identity.json",
        {
            "construction_input_sha256": input_sha256,
            "output_relpath": output_dir.relative_to(repo_root).as_posix(),
            "retry_same_input_identity_allowed": False,
        },
    )

    try:
        runtime = {
            "python_implementation": platform.python_implementation(),
            "python_version": platform.python_version(),
            "python_executable": sys.executable,
            "runner_module": "sparkbrain.research.rv02_rd005_construction_runner",
        }
        _write_json(output_dir / "runtime.json", runtime)
        source_binding = verified_source.state_dict()
        source_binding.update(
            {
                "collision_registry_sha256": identities["collision_registry_sha256"],
                "package_plan_sha256": identities["package_plan_sha256"],
            }
        )
        _write_json(output_dir / "source_binding.json", source_binding)

        collision_search = SeedCollisionRecord(
            seed=RD005_FRESH_SEED,
            searched_seed_ids=registry.consumed_or_reserved_seed_ids,
            searched_world_ids=registry.consumed_or_reserved_world_ids,
        )
        artifact = build_rd005_construction_artifact(
            source_git_sha=identities["source_git_sha"],
            collision_search=collision_search,
        )
        artifact_state = artifact.state_dict()
        _write_json(output_dir / "rd005_construction_artifact.json", artifact_state)
        _write_json(
            output_dir / "artifact_identity.json",
            {"artifact_sha256": artifact.artifact_sha256},
        )

        ready_cell_ids = verify_rd005_artifact_for_future_capability(artifact)
        if artifact.matrix_status != "D1_CONSTRUCTION_READY" or not ready_cell_ids:
            raise RuntimeError(
                "RD005 construction stopped before capability: verified D1 matrix is not ready"
            )
        _write_json(
            output_dir / "verification.json",
            {
                "verification_status": "VERIFIED_CONSTRUCTION_ONLY",
                "verified_ready_cell_ids": list(ready_cell_ids),
                "artifact_sha256": artifact.artifact_sha256,
                "capability_output_opened": False,
                "learner_or_probe_executed": False,
                "formal_execution_allowed": False,
            },
        )
        _write_json(
            output_dir / "COMPLETE.json",
            {
                "status": "D1_CONSTRUCTION_COMPLETE_CAPABILITY_UNOPENED",
                "construction_input_sha256": input_sha256,
                "artifact_sha256": artifact.artifact_sha256,
                "capability_output_opened": False,
                "learner_or_probe_executed": False,
                "formal_execution_allowed": False,
            },
        )
    except Exception as exc:
        _write_json(
            output_dir / "FAILED.json",
            {
                "status": "D1_CONSTRUCTION_FAILED_TERMINAL_FOR_THIS_OUTPUT_IDENTITY",
                "construction_input_sha256": input_sha256,
                "exception_type": type(exc).__name__,
                "message": str(exc),
                "retry_same_output_identity_allowed": False,
            },
        )
        raise

    return output_dir


def run_construction(*, input_path: Path, repo_root: Path) -> Path:
    """Read one input path once, then construct from those exact bytes."""

    return run_construction_from_bytes(raw=input_path.read_bytes(), repo_root=repo_root)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Construct and verify RD005 D1 artifacts without capability execution."
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args(argv)
    run_construction(input_path=args.input, repo_root=args.repo_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["main", "run_construction", "run_construction_from_bytes"]
