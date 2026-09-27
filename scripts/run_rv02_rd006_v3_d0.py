#!/usr/bin/env python3
"""Run the single authorized RD006 v3 bounded D0 matrix."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import subprocess
from pathlib import Path

from sparkbrain.research.rv02_rd006_external_learning_reachability_v3_d0 import (
    OBJECT_ID,
    PARENT_STATIC_PREFLIGHT_HEAD,
    PROTOCOL_ID,
    run_matrix,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-git-sha", required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def _write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _verify_exact_head(source_git_sha: str) -> None:
    observed = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True
    ).strip()
    if observed != source_git_sha:
        raise ValueError(
            f"source_git_sha {source_git_sha} does not match exact HEAD {observed}"
        )
    subprocess.run(
        ["git", "merge-base", "--is-ancestor", PARENT_STATIC_PREFLIGHT_HEAD, observed],
        check=True,
    )


def main() -> int:
    args = parse_args()
    _verify_exact_head(args.source_git_sha)
    args.output.mkdir(parents=True, exist_ok=False)
    manifest_path = args.output / "manifest.json"
    manifest = {
        "object_id": OBJECT_ID,
        "protocol_id": PROTOCOL_ID,
        "parent_static_preflight_head": PARENT_STATIC_PREFLIGHT_HEAD,
        "source_git_sha": args.source_git_sha,
        "artifact_path": "artifact.json.gz",
        "status": "STARTED",
        "formal_execution": False,
        "capability_scoring": False,
    }
    _write_json(manifest_path, manifest)
    try:
        artifact = run_matrix(args.source_git_sha)
    except Exception as exc:
        _write_json(
            manifest_path,
            {
                **manifest,
                "status": "FAILED_INCOMPLETE",
                "error_class": type(exc).__name__,
                "error": str(exc),
            },
        )
        raise
    encoded = (
        json.dumps(artifact, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    compressed = gzip.compress(encoded, compresslevel=9, mtime=0)
    temporary_path = args.output / "artifact.json.gz.tmp"
    with temporary_path.open("xb") as handle:
        handle.write(compressed)
        handle.flush()
        os.fsync(handle.fileno())
    artifact_path = args.output / "artifact.json.gz"
    temporary_path.replace(artifact_path)
    _write_json(
        manifest_path,
        {
            "object_id": artifact["object_id"],
            "protocol_id": artifact["protocol_id"],
            "parent_static_preflight_head": PARENT_STATIC_PREFLIGHT_HEAD,
            "source_git_sha": artifact["source_git_sha"],
            "artifact_path": "artifact.json.gz",
            "artifact_sha256": artifact["artifact_sha256"],
            "artifact_file_sha256": hashlib.sha256(compressed).hexdigest(),
            "artifact_uncompressed_sha256": hashlib.sha256(encoded).hexdigest(),
            "matrix_status": artifact["matrix_status"],
            "execution_cell_count": artifact["execution_cell_count"],
            "complete_cell_count": len(artifact["complete_cell_ids"]),
            "bounded_cell_count": len(artifact["bounded_cell_ids"]),
            "gate_open_cell_count": len(artifact["gate_open_cell_ids"]),
            "status": "COMPLETED",
            "formal_execution": False,
            "capability_scoring": False,
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
