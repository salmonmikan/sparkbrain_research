#!/usr/bin/env python3
"""Run the single authorized RD006 v4 bounded D0 matrix."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import subprocess
from pathlib import Path

from sparkbrain.research.rv02_rd006_external_learning_reachability_v4_d0 import (
    OBJECT_ID,
    PARENT_PREFLIGHT_HEAD,
    PARENT_PREFLIGHT_TREE,
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


def _append_progress(path: Path, value: object) -> None:
    encoded = (
        json.dumps(value, allow_nan=False, ensure_ascii=False, sort_keys=True)
        + "\n"
    ).encode("utf-8")
    with path.open("ab") as handle:
        handle.write(encoded)
        handle.flush()
        os.fsync(handle.fileno())


def _verify_exact_head(source_git_sha: str) -> str:
    observed_head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True
    ).strip()
    observed_tree = subprocess.check_output(
        ["git", "rev-parse", "HEAD^{tree}"], text=True
    ).strip()
    if observed_head != source_git_sha:
        raise ValueError(
            f"source_git_sha {source_git_sha} does not match exact HEAD {observed_head}"
        )
    subprocess.run(
        ["git", "merge-base", "--is-ancestor", PARENT_PREFLIGHT_HEAD, observed_head],
        check=True,
    )
    parent_tree = subprocess.check_output(
        ["git", "rev-parse", f"{PARENT_PREFLIGHT_HEAD}^{{tree}}"], text=True
    ).strip()
    if parent_tree != PARENT_PREFLIGHT_TREE:
        raise ValueError("parent preflight tree does not match frozen contract")
    return observed_tree


def main() -> int:
    args = parse_args()
    source_git_tree = _verify_exact_head(args.source_git_sha)
    args.output.mkdir(parents=True, exist_ok=False)
    manifest_path = args.output / "manifest.json"
    progress_path = args.output / "progress.jsonl"
    manifest = {
        "object_id": OBJECT_ID,
        "protocol_id": PROTOCOL_ID,
        "parent_preflight_head": PARENT_PREFLIGHT_HEAD,
        "parent_preflight_tree": PARENT_PREFLIGHT_TREE,
        "source_git_sha": args.source_git_sha,
        "source_git_tree": source_git_tree,
        "artifact_path": "artifact.json.gz",
        "progress_path": "progress.jsonl",
        "status": "STARTED",
        "formal_execution": False,
        "capability_scoring": False,
        "held_out_access": False,
    }
    _write_json(manifest_path, manifest)
    progress_path.touch(exist_ok=False)
    _append_progress(
        progress_path,
        {
            "event": "MATRIX_STARTED",
            "object_id": OBJECT_ID,
            "protocol_id": PROTOCOL_ID,
            "source_git_sha": args.source_git_sha,
            "source_git_tree": source_git_tree,
        },
    )
    try:
        artifact = run_matrix(
            args.source_git_sha,
            progress_hook=lambda value: _append_progress(progress_path, value),
        )
    except Exception as exc:
        _write_json(
            manifest_path,
            {
                **manifest,
                "status": "FAILED_INCOMPLETE",
                "error_class": type(exc).__name__,
                "error": str(exc),
                "progress_file_sha256": hashlib.sha256(
                    progress_path.read_bytes()
                ).hexdigest(),
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
            **manifest,
            "artifact_sha256": artifact["artifact_sha256"],
            "artifact_file_sha256": hashlib.sha256(compressed).hexdigest(),
            "artifact_uncompressed_sha256": hashlib.sha256(encoded).hexdigest(),
            "matrix_status": artifact["matrix_status"],
            "execution_cell_count": artifact["execution_cell_count"],
            "complete_cell_count": len(artifact["complete_cell_ids"]),
            "bounded_cell_count": len(artifact["bounded_cell_ids"]),
            "gate_open_cell_count": len(artifact["gate_open_cell_ids"]),
            "prohibited_update_count": artifact["prohibited_update_count"],
            "new_edge_count": artifact["new_edge_count"],
            "progress_file_sha256": hashlib.sha256(
                progress_path.read_bytes()
            ).hexdigest(),
            "status": "COMPLETED",
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
