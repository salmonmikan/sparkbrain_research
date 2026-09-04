from __future__ import annotations

import argparse
import json
from pathlib import Path

from .candidate import (
    CandidatePurpose,
    CandidateSpec,
    build_outcome_blind_declarations,
)
from .freeze import build_freeze_manifest


def _write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


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
    """Create candidate declarations and an unsigned frozen manifest.

    This operation constructs world structure and hashes only. It never creates
    a comparator model, capability result, dynamic resource measurement, or
    execution seal.
    """

    candidate = CandidateSpec(
        generation_id=generation_id,
        seeds=seeds,
        purpose=purpose,
    )
    candidate.validate()
    declarations = build_outcome_blind_declarations(candidate)
    manifest = build_freeze_manifest(
        source_git_sha=source_git_sha,
        builder=builder,
        candidate=candidate,
        execution_command=execution_command,
        artifact_root=artifact_root,
    )

    output_dir.mkdir(parents=True, exist_ok=False)
    candidate_path = output_dir / "candidate.json"
    declarations_path = output_dir / "declarations.jsonl"
    manifest_path = output_dir / "freeze_manifest.json"
    _write_json(candidate_path, candidate.state_dict())
    with declarations_path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in declarations:
            handle.write(json.dumps(row.state_dict(), sort_keys=True))
            handle.write("\n")
    _write_json(manifest_path, manifest.state_dict())
    return candidate_path, declarations_path, manifest_path


def _parse_seeds(value: str) -> tuple[int, ...]:
    try:
        return tuple(int(row.strip()) for row in value.split(",") if row.strip())
    except ValueError as exc:
        raise argparse.ArgumentTypeError("seeds must be comma-separated integers") from exc


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
