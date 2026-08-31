from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from .artifacts import write_run_atomic
from .candidate import (
    CX01_COMPARATOR_INVENTORY,
    CandidateSpec,
    build_candidate_grid,
    candidate_grid_hash,
    declaration_bundle_hash,
)
from .control import OneWayControlMarker, require_control_marker
from .development import run_development_execution
from .freeze import ExecutionSeal, FreezeManifest, require_execution_seal


def _run_id(manifest: FreezeManifest, candidate: CandidateSpec) -> str:
    payload = (
        f"{manifest.manifest_hash()}|{candidate.specification_hash()}|"
        f"{manifest.source_git_sha}"
    ).encode()
    return f"cx01-formal-{hashlib.sha256(payload).hexdigest()[:24]}"


def _validate_formal_binding(
    candidate: CandidateSpec,
    manifest: FreezeManifest,
) -> None:
    candidate.require_formal()
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


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def claim_one_way_execution(
    artifact_root: Path,
    *,
    run_id: str,
    candidate: CandidateSpec,
    manifest: FreezeManifest,
) -> Path:
    """Create the local irreversible STARTED marker before capability calls."""

    artifact_root.mkdir(parents=True, exist_ok=True)
    target = artifact_root / run_id
    marker = artifact_root / f"{run_id}.STARTED.json"
    if target.exists() or marker.exists():
        raise RuntimeError("formal CX01 candidate has already been opened")
    payload = {
        "candidate_spec_hash": candidate.specification_hash(),
        "manifest_hash": manifest.manifest_hash(),
        "run_id": run_id,
        "source_git_sha": manifest.source_git_sha,
        "state": "STARTED",
    }
    try:
        with marker.open("xb") as handle:
            handle.write(_canonical_bytes(payload) + b"\n")
        marker.chmod(0o444)
    except FileExistsError as exc:
        raise RuntimeError("formal CX01 candidate has already been opened") from exc
    return marker


def execute_formal_candidate(
    candidate: CandidateSpec,
    manifest: FreezeManifest,
    seal: ExecutionSeal,
    *,
    current_source_git_sha: str,
    artifact_root: Path,
    control_marker: OneWayControlMarker | None = None,
) -> Path:
    """Execute one fully sealed and persistently consumed candidate exactly once.

    The externally committed control marker is required before capability. A
    second local STARTED marker is then created before model construction so a
    process-level retry also fails closed.
    """

    require_execution_seal(
        manifest,
        seal,
        current_source_git_sha=current_source_git_sha,
    )
    _validate_formal_binding(candidate, manifest)
    if control_marker is None:
        raise RuntimeError("persistent one-way control marker is required")
    require_control_marker(
        control_marker,
        candidate,
        manifest,
        current_source_git_sha=current_source_git_sha,
    )
    if str(artifact_root) != manifest.artifact_root:
        raise RuntimeError("artifact root does not match frozen manifest")

    run_id = _run_id(manifest, candidate)
    claim_one_way_execution(
        artifact_root,
        run_id=run_id,
        candidate=candidate,
        manifest=manifest,
    )

    rows: list[dict[str, Any]] = []
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


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--seal", type=Path, required=True)
    parser.add_argument("--control-marker", type=Path, required=True)
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--artifact-root", type=Path, required=True)
    args = parser.parse_args()

    candidate = CandidateSpec.from_state_dict(_read_json(args.candidate))
    manifest = FreezeManifest.from_state_dict(_read_json(args.manifest))
    seal = ExecutionSeal.from_state_dict(_read_json(args.seal))
    control_marker = OneWayControlMarker.from_state_dict(_read_json(args.control_marker))
    output = execute_formal_candidate(
        candidate,
        manifest,
        seal,
        current_source_git_sha=args.source_sha,
        artifact_root=args.artifact_root,
        control_marker=control_marker,
    )
    print(output)


if __name__ == "__main__":
    main()
