from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from pathlib import Path
from typing import Any

from .candidate import (
    CandidatePurpose,
    CandidateSpec,
    build_candidate_grid,
    build_outcome_blind_declarations,
)
from .formal_identifiability import audit_formal_grid_identifiability
from .formal_worlds import audit_formal_grid_structure
from .freeze import FreezeManifest, build_freeze_manifest
from .structural_components import audit_formal_grid_components

PACKAGE_SCHEMA_VERSION = "cx01-outcome-blind-package-v2"
PACKAGE_STATUS = "OUTCOME_BLIND_UNSIGNED_PRESTART"


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _write_jsonl(path: Path, rows: tuple[dict[str, Any], ...]) -> None:
    with path.open("wb") as handle:
        for row in rows:
            handle.write(_canonical_bytes(row) + b"\n")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _payload_manifest(
    root: Path,
    *,
    declaration_count: int,
    world_count: int,
) -> dict[str, dict[str, Any]]:
    counts = {
        "declarations.jsonl": declaration_count,
        "world_grid.json": world_count,
    }
    return {
        path.name: {
            "record_count": counts.get(path.name),
            "sha256": _sha256(path),
            "size_bytes": path.stat().st_size,
        }
        for path in sorted(root.iterdir(), key=lambda item: item.name)
        if path.is_file() and path.name != "package_checksums.json"
    }


def _build_package_status(
    *,
    candidate: CandidateSpec,
    manifest: FreezeManifest,
    declaration_count: int,
    world_count: int,
) -> dict[str, Any]:
    return {
        "candidate_consumed": False,
        "candidate_generation_id": candidate.generation_id,
        "candidate_spec_hash": manifest.candidate_spec_hash,
        "declaration_bundle_hash": manifest.declaration_bundle_hash,
        "declaration_count": declaration_count,
        "execution_seal_status": "NOT_ISSUED",
        "formal_capability_executed": False,
        "formal_score_present": False,
        "formal_status": "NOT_STARTED",
        "independent_review_status": "PENDING",
        "package_schema_version": PACKAGE_SCHEMA_VERSION,
        "package_status": PACKAGE_STATUS,
        "source_git_sha": manifest.source_git_sha,
        "structural_review_required": True,
        "world_count": world_count,
        "world_grid_hash": manifest.candidate_grid_hash,
    }


def prepare_outcome_blind_bundle(
    *,
    generation_id: str,
    seeds: tuple[int, ...],
    purpose: CandidatePurpose,
    source_git_sha: str,
    builder: str,
    execution_command: str,
    artifact_root: str,
    output_dir: Path,
) -> tuple[Path, Path, Path]:
    """Create a complete, unsigned, outcome-blind pre-start package.

    The package contains the candidate, all world specifications, all unscored
    declarations, the three structural/identifiability audits, the unsigned
    freeze manifest, and byte-level checksums. It never creates a comparator
    model, capability result, resource measurement, execution seal, or STARTED
    marker.
    """

    candidate = CandidateSpec(
        generation_id=generation_id,
        seeds=seeds,
        purpose=purpose,
    )
    candidate.validate()
    worlds = build_candidate_grid(candidate)
    declarations = build_outcome_blind_declarations(candidate)
    declaration_rows = tuple(row.state_dict() for row in declarations)
    world_rows = tuple(world.state_dict() for world in worlds)
    audits = {
        "canonical_structure": audit_formal_grid_structure(worlds),
        "component_structure": audit_formal_grid_components(worlds),
        "family_identifiability": audit_formal_grid_identifiability(worlds),
    }
    if not all(bool(row.get("passed")) for row in audits.values()):
        raise RuntimeError("candidate structural audits must pass before packaging")

    manifest = build_freeze_manifest(
        source_git_sha=source_git_sha,
        builder=builder,
        candidate=candidate,
        execution_command=execution_command,
        artifact_root=artifact_root,
    )

    if output_dir.exists():
        raise FileExistsError(f"outcome-blind package already exists: {output_dir}")
    temporary = output_dir.with_name(f".{output_dir.name}.tmp")
    if temporary.exists():
        raise FileExistsError(f"temporary package path already exists: {temporary}")
    temporary.mkdir(parents=True)
    try:
        candidate_path = temporary / "candidate.json"
        worlds_path = temporary / "world_grid.json"
        declarations_path = temporary / "declarations.jsonl"
        audits_path = temporary / "structural_novelty_audit.json"
        manifest_path = temporary / "freeze_manifest.json"
        status_path = temporary / "package_status.json"
        checksums_path = temporary / "package_checksums.json"
        marker_path = temporary / "OUTCOME_BLIND"

        _write_json(candidate_path, candidate.state_dict())
        _write_json(
            worlds_path,
            {
                "generation_id": candidate.generation_id,
                "world_count": len(world_rows),
                "worlds": world_rows,
            },
        )
        _write_jsonl(declarations_path, declaration_rows)
        _write_json(audits_path, audits)
        _write_json(manifest_path, manifest.state_dict())
        _write_json(
            status_path,
            _build_package_status(
                candidate=candidate,
                manifest=manifest,
                declaration_count=len(declaration_rows),
                world_count=len(world_rows),
            ),
        )
        marker_path.write_text(
            "outcome-blind unsigned pre-start package\n",
            encoding="utf-8",
            newline="\n",
        )
        _write_json(
            checksums_path,
            {
                "files": _payload_manifest(
                    temporary,
                    declaration_count=len(declaration_rows),
                    world_count=len(world_rows),
                ),
                "package_schema_version": PACKAGE_SCHEMA_VERSION,
            },
        )
        os.replace(temporary, output_dir)
    except Exception:
        shutil.rmtree(temporary, ignore_errors=True)
        raise

    verify_outcome_blind_bundle(output_dir)
    return (
        output_dir / "candidate.json",
        output_dir / "declarations.jsonl",
        output_dir / "freeze_manifest.json",
    )


def verify_outcome_blind_bundle(output_dir: Path) -> dict[str, Any]:
    required = {
        "OUTCOME_BLIND",
        "candidate.json",
        "declarations.jsonl",
        "freeze_manifest.json",
        "package_checksums.json",
        "package_status.json",
        "structural_novelty_audit.json",
        "world_grid.json",
    }
    names = {path.name for path in output_dir.iterdir() if path.is_file()}
    missing = required.difference(names)
    if missing:
        raise RuntimeError(f"outcome-blind package is incomplete: {sorted(missing)}")
    forbidden = {"execution_seal.json", "STARTED", "results.jsonl"}
    present_forbidden = forbidden.intersection(names)
    if present_forbidden:
        raise RuntimeError(
            "pre-start package contains forbidden execution material: "
            f"{sorted(present_forbidden)}"
        )

    checksums = json.loads(
        (output_dir / "package_checksums.json").read_text(encoding="utf-8")
    )
    if checksums["package_schema_version"] != PACKAGE_SCHEMA_VERSION:
        raise RuntimeError("package checksum schema version mismatch")
    for name, metadata in checksums["files"].items():
        path = output_dir / name
        if not path.is_file():
            raise RuntimeError(f"checksummed package file is missing: {name}")
        if _sha256(path) != metadata["sha256"]:
            raise RuntimeError(f"package checksum mismatch: {name}")
        if path.stat().st_size != metadata["size_bytes"]:
            raise RuntimeError(f"package size mismatch: {name}")

    candidate_state = json.loads(
        (output_dir / "candidate.json").read_text(encoding="utf-8")
    )
    candidate = CandidateSpec.from_state_dict(candidate_state)
    declaration_rows = tuple(
        json.loads(line)
        for line in (output_dir / "declarations.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
        if line
    )
    if not declaration_rows:
        raise RuntimeError("outcome-blind declaration archive is empty")
    if any(row["status"] != "unscored" for row in declaration_rows):
        raise RuntimeError("declaration archive contains scored state")
    if any(row["capability_result_present"] for row in declaration_rows):
        raise RuntimeError("declaration archive contains capability results")
    if any(row["measurements_present"] for row in declaration_rows):
        raise RuntimeError("declaration archive contains measurements")

    world_state = json.loads(
        (output_dir / "world_grid.json").read_text(encoding="utf-8")
    )
    status = json.loads(
        (output_dir / "package_status.json").read_text(encoding="utf-8")
    )
    audits = json.loads(
        (output_dir / "structural_novelty_audit.json").read_text(
            encoding="utf-8"
        )
    )
    manifest = FreezeManifest.from_state_dict(
        json.loads(
            (output_dir / "freeze_manifest.json").read_text(encoding="utf-8")
        )
    )
    expected_declarations = (
        len(world_state["worlds"]) * len(manifest.comparator_inventory)
    )
    if len(declaration_rows) != expected_declarations:
        raise RuntimeError("declaration archive cardinality mismatch")
    if world_state["world_count"] != len(world_state["worlds"]):
        raise RuntimeError("world-grid cardinality mismatch")
    if status["world_count"] != world_state["world_count"]:
        raise RuntimeError("package status world count mismatch")
    if status["declaration_count"] != len(declaration_rows):
        raise RuntimeError("package status declaration count mismatch")
    if status["formal_status"] != "NOT_STARTED":
        raise RuntimeError("pre-start package cannot be STARTED")
    if status["execution_seal_status"] != "NOT_ISSUED":
        raise RuntimeError("pre-start package cannot contain an execution seal")
    if status["source_git_sha"] != manifest.source_git_sha:
        raise RuntimeError("package status source SHA mismatch")
    if candidate.specification_hash() != manifest.candidate_spec_hash:
        raise RuntimeError("candidate specification does not match freeze manifest")
    if not all(bool(row.get("passed")) for row in audits.values()):
        raise RuntimeError("packaged structural audit does not pass")

    return {
        "candidate_generation_id": candidate.generation_id,
        "declaration_count": len(declaration_rows),
        "execution_seal_status": status["execution_seal_status"],
        "formal_status": status["formal_status"],
        "source_git_sha": manifest.source_git_sha,
        "verified": True,
        "world_count": world_state["world_count"],
    }


def _parse_seeds(value: str) -> tuple[int, ...]:
    try:
        return tuple(int(row.strip()) for row in value.split(",") if row.strip())
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "seeds must be comma-separated integers"
        ) from exc


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generation-id", required=True)
    parser.add_argument("--seeds", type=_parse_seeds, required=True)
    parser.add_argument(
        "--purpose",
        choices=tuple(row.value for row in CandidatePurpose),
        default=CandidatePurpose.FORMAL.value,
    )
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--builder", required=True)
    parser.add_argument("--execution-command", required=True)
    parser.add_argument("--artifact-root", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    prepare_outcome_blind_bundle(
        generation_id=args.generation_id,
        seeds=args.seeds,
        purpose=CandidatePurpose(args.purpose),
        source_git_sha=args.source_sha,
        builder=args.builder,
        execution_command=args.execution_command,
        artifact_root=args.artifact_root,
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    main()
