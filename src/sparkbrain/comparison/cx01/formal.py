from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from .artifacts import write_run_atomic
from .candidate import (
    CX01_COMPARATOR_INVENTORY,
    CandidateSpec,
    candidate_grid_hash,
    declaration_bundle_hash,
)
from .development import run_development_execution
from .freeze import ExecutionSeal, FreezeManifest, require_execution_seal


def _run_id(manifest: FreezeManifest, candidate: CandidateSpec) -> str:
    payload = (
        f"{manifest.manifest_hash()}|{candidate.specification_hash()}|"
        f"{manifest.source_git_sha}"
    ).encode("utf-8")
    return f"cx01-formal-{hashlib.sha256(payload).hexdigest()[:24]}"


def _validate_formal_binding(
    candidate: CandidateSpec,
    manifest: FreezeManifest,
) -> None:
    candidate.validate()
    manifest.validate()
    if candidate.specification_hash() != manifest.candidate_spec_hash:
        raise RuntimeError("candidate specification does not match frozen manifest")
    if candidate_grid_hash(candidate) != manifest.candidate_grid_hash:
        raise RuntimeError("candidate world grid does not match frozen manifest")
    if declaration_bundle_hash(candidate) != manifest.declaration_bundle_hash:
        raise RuntimeError("candidate declarations do not match frozen manifest")
    expected_inventory = tuple(kind.value for kind in CX01_COMPARATOR_INVENTORY)
    if manifest.comparator_inventory != expected_inventory:
        raise RuntimeError("comparator inventory does not match frozen CX01 inventory")


def execute_formal_candidate(
    candidate: CandidateSpec,
    manifest: FreezeManifest,
    seal: ExecutionSeal,
    *,
    current_source_git_sha: str,
    artifact_root: Path,
) -> Path:
    """Execute one fully sealed CX01 comparator candidate exactly once.

    This function is intentionally unusable without a valid frozen manifest and
    independently approved execution seal. The deterministic run directory is a
    one-way marker: an existing directory makes same-candidate rerun fail closed.
    """

    _validate_formal_binding(candidate, manifest)
    require_execution_seal(
        manifest,
        seal,
        current_source_git_sha=current_source_git_sha,
    )
    run_id = _run_id(manifest, candidate)
    target = artifact_root / run_id
    if target.exists():
        raise RuntimeError("formal CX01 candidate has already been executed")

    rows: list[dict[str, Any]] = []
    from .candidate import build_candidate_grid

    for world in build_candidate_grid(candidate):
        for kind in CX01_COMPARATOR_INVENTORY:
            execution = run_development_execution(kind, world)
            rows.append(execution.state_dict())

    expected = len(candidate.seeds) * 6 * len(CX01_COMPARATOR_INVENTORY)
    if len(rows) != expected:
        raise RuntimeError("formal CX01 execution matrix is incomplete")

    return write_run_atomic(
        artifact_root,
        run_id=run_id,
        manifest=manifest,
        seal=seal,
        rows=rows,
    )
