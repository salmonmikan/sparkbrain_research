from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .candidate import CandidateSpec, candidate_grid_hash, declaration_bundle_hash
from .freeze import ExecutionSeal, FreezeManifest, require_execution_seal


@dataclass(frozen=True, slots=True)
class OneWayControlMarker:
    candidate_spec_hash: str
    candidate_grid_hash: str
    declaration_bundle_hash: str
    manifest_hash: str
    source_git_sha: str
    execution_policy: str = "one-way-no-rerun"
    state: str = "STARTED"

    def validate(self) -> None:
        for name in (
            "candidate_spec_hash",
            "candidate_grid_hash",
            "declaration_bundle_hash",
            "manifest_hash",
        ):
            value = str(getattr(self, name))
            if len(value) != 64 or any(char not in "0123456789abcdef" for char in value.lower()):
                raise ValueError(f"{name} must be SHA-256")
        if len(self.source_git_sha) != 40 or any(
            char not in "0123456789abcdef" for char in self.source_git_sha.lower()
        ):
            raise ValueError("source_git_sha must be a Git SHA")
        if self.execution_policy != "one-way-no-rerun":
            raise ValueError("control marker must use one-way-no-rerun policy")
        if self.state != "STARTED":
            raise ValueError("control marker must be STARTED")

    def state_dict(self) -> dict[str, Any]:
        self.validate()
        return asdict(self)

    @classmethod
    def from_state_dict(cls, state: dict[str, Any]) -> OneWayControlMarker:
        marker = cls(
            candidate_spec_hash=str(state["candidate_spec_hash"]),
            candidate_grid_hash=str(state["candidate_grid_hash"]),
            declaration_bundle_hash=str(state["declaration_bundle_hash"]),
            manifest_hash=str(state["manifest_hash"]),
            source_git_sha=str(state["source_git_sha"]),
            execution_policy=str(state.get("execution_policy", "")),
            state=str(state.get("state", "")),
        )
        marker.validate()
        return marker


def build_control_marker(
    candidate: CandidateSpec,
    manifest: FreezeManifest,
    seal: ExecutionSeal,
    *,
    current_source_git_sha: str,
) -> OneWayControlMarker:
    """Bind a formal candidate to its sealed source without executing capability."""

    require_execution_seal(
        manifest,
        seal,
        current_source_git_sha=current_source_git_sha,
    )
    candidate.require_formal()
    if candidate.specification_hash() != manifest.candidate_spec_hash:
        raise RuntimeError("candidate specification does not match frozen manifest")
    grid_hash = candidate_grid_hash(candidate)
    if grid_hash != manifest.candidate_grid_hash:
        raise RuntimeError("candidate world grid does not match frozen manifest")
    declarations_hash = declaration_bundle_hash(candidate)
    if declarations_hash != manifest.declaration_bundle_hash:
        raise RuntimeError("candidate declarations do not match frozen manifest")
    marker = OneWayControlMarker(
        candidate_spec_hash=candidate.specification_hash(),
        candidate_grid_hash=grid_hash,
        declaration_bundle_hash=declarations_hash,
        manifest_hash=manifest.manifest_hash(),
        source_git_sha=current_source_git_sha,
    )
    marker.validate()
    return marker


def require_control_marker(
    marker: OneWayControlMarker,
    candidate: CandidateSpec,
    manifest: FreezeManifest,
    *,
    current_source_git_sha: str,
) -> None:
    marker.validate()
    candidate.require_formal()
    manifest.validate()
    expected = {
        "candidate_spec_hash": candidate.specification_hash(),
        "candidate_grid_hash": candidate_grid_hash(candidate),
        "declaration_bundle_hash": declaration_bundle_hash(candidate),
        "manifest_hash": manifest.manifest_hash(),
        "source_git_sha": current_source_git_sha,
    }
    observed = marker.state_dict()
    for name, value in expected.items():
        if observed[name] != value:
            raise RuntimeError(f"control marker mismatch: {name}")


def write_control_marker(
    output_path: Path,
    candidate: CandidateSpec,
    manifest: FreezeManifest,
    seal: ExecutionSeal,
    *,
    current_source_git_sha: str,
) -> Path:
    marker = build_control_marker(
        candidate,
        manifest,
        seal,
        current_source_git_sha=current_source_git_sha,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with output_path.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(marker.state_dict(), handle, indent=2, sort_keys=True)
            handle.write("\n")
    except FileExistsError as exc:
        raise RuntimeError("control marker already exists; candidate is already consumed") from exc
    output_path.chmod(0o444)
    return output_path


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
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    from .candidate import CandidateSpec
    from .freeze import ExecutionSeal, FreezeManifest

    candidate = CandidateSpec.from_state_dict(_read_json(args.candidate))
    manifest = FreezeManifest.from_state_dict(_read_json(args.manifest))
    seal = ExecutionSeal.from_state_dict(_read_json(args.seal))
    print(
        write_control_marker(
            args.output,
            candidate,
            manifest,
            seal,
            current_source_git_sha=args.source_sha,
        )
    )


if __name__ == "__main__":
    main()
