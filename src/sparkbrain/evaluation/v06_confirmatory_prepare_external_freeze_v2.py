from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

from .v06_confirmatory import ConfirmatoryPhase
from .v06_confirmatory_current_manifest import build_current_confirmatory_manifest
from .v06_confirmatory_environment_lock_v2 import capture_environment_lock_v2
from .v06_confirmatory_external_freeze import ExternalArtifactLayout
from .v06_confirmatory_freeze_bundle_v2 import (
    build_external_freeze_bundle_v2,
    write_external_freeze_bundle_v2,
)


def _canonical_json(value: object) -> str:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def _write_exclusive(path: Path, value: object) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = (_canonical_json(value) + "\n").encode("utf-8")
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
    try:
        with os.fdopen(descriptor, "wb", closefd=False) as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        os.close(descriptor)
    os.chmod(path, 0o444)
    return hashlib.sha256(payload).hexdigest()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build an unsigned, outcome-blind external freeze bundle candidate.",
    )
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--control-root", type=Path, required=True)
    parser.add_argument("--raw-root", type=Path, required=True)
    parser.add_argument("--analysis-root", type=Path, required=True)
    parser.add_argument("--builder", required=True)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    source_root = args.source_root.expanduser().resolve(strict=True)
    layout = ExternalArtifactLayout(
        control_root=str(args.control_root.expanduser().resolve(strict=False)),
        raw_root=str(args.raw_root.expanduser().resolve(strict=False)),
        analysis_root=str(args.analysis_root.expanduser().resolve(strict=False)),
    )
    environment = capture_environment_lock_v2()
    manifest = build_current_confirmatory_manifest(
        ConfirmatoryPhase.CONFIRMATORY,
        code_ref=args.source_sha,
    )
    bundle = build_external_freeze_bundle_v2(
        manifest,
        source_root=source_root,
        source_git_sha=args.source_sha,
        artifact_layout=layout,
        environment_lock=environment,
        builder=args.builder,
    )
    control_root = Path(layout.state_dict()["control_root"])
    bundle_path = control_root / "unsigned_freeze_bundle.json"
    bundle_file_hash = write_external_freeze_bundle_v2(
        bundle,
        path=bundle_path,
        require_execution_ready=False,
    )
    environment_path = control_root / "environment_lock.json"
    environment_file_hash = _write_exclusive(
        environment_path,
        environment.state_dict(),
    )
    summary = {
        "approval": None,
        "bundle_file": str(bundle_path),
        "bundle_file_sha256": bundle_file_hash,
        "bundle_hash": bundle.bundle_hash(),
        "candidate_execution_counter_initial": (
            bundle.candidate_execution_counter_initial
        ),
        "environment_file": str(environment_path),
        "environment_file_sha256": environment_file_hash,
        "environment_lock_hash": environment.lock_hash(),
        "manifest_execution_ready": bundle.manifest_execution_ready,
        "reviewer": None,
        "source_git_sha": bundle.source_git_sha,
        "state": "UNSIGNED_CANDIDATE",
        "unsigned_hash": bundle.unsigned_hash(),
        "world_generation_id": bundle.world_generation_id,
        "world_grid_hash": bundle.world_grid_hash,
    }
    summary_path = control_root / "unsigned_freeze_summary.json"
    _write_exclusive(summary_path, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
