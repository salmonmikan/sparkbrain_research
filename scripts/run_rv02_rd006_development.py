#!/usr/bin/env python3
"""Run the bounded RV02-RD006 Stage D0 development matrix once."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

from sparkbrain.research.rv02_rd006_external_learning_reachability import run_matrix


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-git-sha", required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    manifest_path = args.output / "manifest.json"
    manifest = {
        "object_id": "RV02-RD006-EXTERNAL-LEARNING-REACHABILITY-A",
        "protocol_id": "rv02-rd006-external-learning-reachability-a-v1",
        "source_git_sha": args.source_git_sha,
        "artifact_path": "artifact.json",
        "status": "STARTED",
        "formal_execution": False,
        "capability_scoring": False,
    }
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    try:
        artifact = run_matrix(args.source_git_sha)
    except Exception as exc:
        failed = {
            **manifest,
            "status": "FAILED_INCOMPLETE",
            "error_class": type(exc).__name__,
            "error": str(exc),
        }
        manifest_path.write_text(
            json.dumps(failed, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        raise
    encoded = (
        json.dumps(artifact, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    temporary_path = args.output / "artifact.json.tmp"
    with temporary_path.open("xb") as handle:
        handle.write(encoded)
        handle.flush()
        os.fsync(handle.fileno())
    artifact_path = args.output / "artifact.json"
    temporary_path.replace(artifact_path)
    artifact_file_sha256 = hashlib.sha256(encoded).hexdigest()
    manifest = {
        "object_id": artifact["object_id"],
        "protocol_id": artifact["protocol_id"],
        "source_git_sha": artifact["source_git_sha"],
        "artifact_path": "artifact.json",
        "artifact_sha256": artifact["artifact_sha256"],
        "artifact_file_sha256": artifact_file_sha256,
        "matrix_status": artifact["matrix_status"],
        "status": "COMPLETED",
        "formal_execution": False,
        "capability_scoring": False,
    }
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
