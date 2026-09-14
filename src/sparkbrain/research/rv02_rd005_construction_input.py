"""Prospective, execution-disabled construction-input binding for RV02 RD005.

This module prepares the exact JSON bytes consumed by the already-bound D1
construction wrapper. It verifies the exact source checkout and reconstructs the
authoritative pre-RD005 collision registry before emitting any file. It does not
construct D1, allocate the D1 output identity, run a learner/probe, score an
outcome, or grant execution authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from .rv02_rd005_development_package import (
    RD005CollisionRegistry,
    RD005DevelopmentPackagePlan,
    RD005SourceManifest,
    RD005SourceManifestEntry,
)
from .rv02_rd005_retained_registry import build_authoritative_rd005_collision_registry
from .rv02_rd005_source_binding import verify_rd005_source_checkout

_SOURCE_MANIFEST_KEYS = frozenset({"source_git_sha", "entries"})
_SOURCE_MANIFEST_ENTRY_KEYS = frozenset({"path", "sha256"})


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


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


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
            f"{label} keys must exactly match {sorted(expected_keys)}; got {sorted(keys)}"
        )
    return value


def _require_hash(value: object, *, label: str, length: int) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{label} must be a string")
    if len(value) != length or any(char not in "0123456789abcdef" for char in value):
        raise ValueError(f"{label} must be a {length}-character lowercase hex digest")
    return value


def load_source_manifest(path: Path) -> RD005SourceManifest:
    """Load an exact RD005 source manifest without granting execution authority."""

    try:
        decoded = json.loads(path.read_bytes())
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("RD005 source manifest must be valid UTF-8 JSON") from exc
    row = _require_object(
        decoded,
        label="source manifest",
        expected_keys=_SOURCE_MANIFEST_KEYS,
    )
    entries_value = row["entries"]
    if not isinstance(entries_value, list):
        raise TypeError("source manifest entries must be a JSON array")

    entries: list[RD005SourceManifestEntry] = []
    for index, value in enumerate(entries_value):
        entry = _require_object(
            value,
            label=f"source manifest entry {index}",
            expected_keys=_SOURCE_MANIFEST_ENTRY_KEYS,
        )
        entry_path = entry["path"]
        if not isinstance(entry_path, str):
            raise TypeError(f"source manifest entry {index} path must be a string")
        entries.append(
            RD005SourceManifestEntry(
                path=entry_path,
                sha256=_require_hash(
                    entry["sha256"],
                    label=f"source manifest entry {index} sha256",
                    length=64,
                ),
            )
        )

    manifest = RD005SourceManifest(
        source_git_sha=_require_hash(
            row["source_git_sha"],
            label="source_git_sha",
            length=40,
        ),
        entries=tuple(entries),
    )
    manifest.validate()
    return manifest


def build_construction_input_payload(
    *,
    source_manifest: RD005SourceManifest,
    collision_registry: RD005CollisionRegistry,
) -> dict[str, object]:
    """Build the runner's exact prospective input schema from validated identities."""

    plan = RD005DevelopmentPackagePlan(
        source_manifest=source_manifest,
        collision_registry=collision_registry,
    )
    plan.validate()
    return {
        "source_git_sha": source_manifest.source_git_sha,
        "source_manifest_sha256": source_manifest.manifest_sha256,
        "source_manifest": source_manifest.state_dict(),
        "collision_registry_sha256": collision_registry.registry_sha256,
        "package_plan_sha256": plan.package_plan_sha256,
        "collision_registry": collision_registry.state_dict(),
    }


def prepare_construction_input_bytes(
    *,
    repo_root: Path,
    source_manifest_path: Path,
) -> tuple[bytes, str]:
    """Verify all prospective identities and return exact D1 input bytes and digest.

    Verification is deliberately completed before any caller is allowed to write
    an input artifact. The function itself performs no writes.
    """

    source_manifest = load_source_manifest(source_manifest_path)
    verify_rd005_source_checkout(repo_root, source_manifest)
    collision_registry = build_authoritative_rd005_collision_registry(repo_root)
    payload = build_construction_input_payload(
        source_manifest=source_manifest,
        collision_registry=collision_registry,
    )
    raw = _canonical_json(payload)
    return raw, _sha256(raw)


def write_construction_input(
    *,
    repo_root: Path,
    source_manifest_path: Path,
    output_path: Path,
) -> str:
    """Write one exact construction-input artifact without clobbering any prior file."""

    if output_path.exists():
        raise FileExistsError(f"RD005 construction input already exists: {output_path}")

    raw, digest = prepare_construction_input_bytes(
        repo_root=repo_root,
        source_manifest_path=source_manifest_path,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("xb") as handle:
        handle.write(raw)
    return digest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Prepare the exact prospective RV02 RD005 D1 construction input. "
            "This command does not execute D1."
        )
    )
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--source-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)

    digest = write_construction_input(
        repo_root=args.repo_root,
        source_manifest_path=args.source_manifest,
        output_path=args.output,
    )
    print(digest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "build_construction_input_payload",
    "load_source_manifest",
    "main",
    "prepare_construction_input_bytes",
    "write_construction_input",
]
