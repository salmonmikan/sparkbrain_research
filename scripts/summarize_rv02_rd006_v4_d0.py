#!/usr/bin/env python3
"""Derive the single fixed summary from a preserved RD006 v4 raw artifact."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any

from sparkbrain.research.rv02_rd006_external_learning_reachability_v4_d0 import (
    PROTOCOL_ID,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def summarize(artifact: dict[str, Any]) -> dict[str, Any]:
    if artifact.get("protocol_id") != PROTOCOL_ID:
        raise ValueError("artifact protocol does not match RD006 v4 D0")
    cells = [
        pair["execution_cells"][arm]
        for pair in artifact["family_pairs"]
        for arm in ("external_learning_off", "external_learning_on")
    ]
    return {
        "schema_version": 1,
        "object_id": artifact["object_id"],
        "protocol_id": artifact["protocol_id"],
        "source_git_sha": artifact["source_git_sha"],
        "raw_artifact_sha256": artifact["artifact_sha256"],
        "matrix_status": artifact["matrix_status"],
        "execution_cell_count": len(cells),
        "complete_cell_count": sum(cell["complete_non_exploded"] for cell in cells),
        "bounded_cell_count": sum(
            cell["bounded_failure"] is not None for cell in cells
        ),
        "gate_open_cell_ids": artifact["gate_open_cell_ids"],
        "gate_open": bool(artifact["gate_open_cell_ids"]),
        "hidden_spike_count_by_arm": {
            arm: sum(
                cell["hidden_spike_count"] for cell in cells if cell["arm"] == arm
            )
            for arm in ("external_learning_off", "external_learning_on")
        },
        "ordinary_updates_by_class": {
            arm: {
                edge_class: sum(
                    cell["ordinary_update_edge_class_counts"][edge_class]
                    for cell in cells
                    if cell["arm"] == arm
                )
                for edge_class in ("PORT_TO_PORT", "PORT_TO_HIDDEN")
            }
            for arm in ("external_learning_off", "external_learning_on")
        },
        "maximum_same_clock_source_count_by_arm": {
            arm: max(
                (
                    cell["maximum_same_clock_source_count"]
                    for cell in cells
                    if cell["arm"] == arm
                ),
                default=0,
            )
            for arm in ("external_learning_off", "external_learning_on")
        },
        "prohibited_update_count": artifact["prohibited_update_count"],
        "new_edge_count": artifact["new_edge_count"],
        "attribution_boundary": (
            "OFF/ON estimates the complete ordinary-learning package effect; "
            "it does not identify incremental PORT-to-hidden contribution."
        ),
        "scientific_credit": 0,
        "next_action": "STOP_FOR_FRESH_EVIDENCE_ANALYST_RECONCILIATION",
    }


def main() -> int:
    args = parse_args()
    if args.output.exists():
        raise FileExistsError(f"refusing to overwrite {args.output}")
    compressed = args.artifact.read_bytes()
    artifact = json.loads(gzip.decompress(compressed).decode("utf-8"))
    summary = summarize(artifact)
    summary["raw_artifact_file_sha256"] = hashlib.sha256(compressed).hexdigest()
    args.output.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
