from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
import warnings
from pathlib import Path
from typing import Any

from sparkbrain.v05.brain import IntegratedV05Brain, V05BrainConfig

CONTRACT_PATH = Path(
    "analysis/architecture/v05_topology_config_contract_cycle1_contract_20260920.json"
)
EXPECTED_MAIN = "ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d"
EXPLICIT_CONTRACT_PHRASES = (
    "fixed topology",
    "fixed geometry",
    "non-operative",
    "nonoperative",
    "compatibility metadata",
    "metadata-only",
    "metadata only",
    "intentionally ignored",
    "not used for topology",
    "does not control topology",
    "does not affect topology",
)
GEOMETRY_FIELD_NAMES = ("width", "height", "receptor_rows")


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git_output(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def git_blob_sha(path: Path) -> str:
    return git_output("hash-object", str(path))


def current_git_head() -> str:
    return os.environ.get("GITHUB_SHA") or git_output("rev-parse", "HEAD")


def load_contract() -> tuple[dict[str, Any], str]:
    raw = CONTRACT_PATH.read_bytes()
    return json.loads(raw), sha256_bytes(raw)


def verify_binding(contract: dict[str, Any]) -> dict[str, str]:
    if contract["source_binding"]["main"] != EXPECTED_MAIN:
        raise RuntimeError("contract main binding mismatch")
    if contract["topology_seed"] != 41:
        raise RuntimeError("unexpected topology seed")

    expected_matrix = [
        (8, 8, 1),
        (12, 8, 1),
        (8, 10, 1),
        (8, 8, 2),
        (12, 10, 2),
    ]
    actual_matrix = [
        (row["width"], row["height"], row["receptor_rows"])
        for row in contract["config_matrix"]
    ]
    if actual_matrix != expected_matrix:
        raise RuntimeError("prospective config matrix mismatch")

    observed_blobs: dict[str, str] = {}
    for path_text, expected in contract["source_binding"].items():
        if path_text == "main":
            continue
        observed = git_blob_sha(Path(path_text))
        observed_blobs[path_text] = observed
        if observed != expected:
            message = f"source blob mismatch for {path_text}: {observed} != {expected}"
            raise RuntimeError(message)
    return observed_blobs


def coordinate_extents(
    rows: list[tuple[float, float]],
) -> dict[str, float | None]:
    if not rows:
        return {"min_x": None, "max_x": None, "min_y": None, "max_y": None}
    xs = [row[0] for row in rows]
    ys = [row[1] for row in rows]
    return {
        "min_x": min(xs),
        "max_x": max(xs),
        "min_y": min(ys),
        "max_y": max(ys),
    }


def topology_metadata(brain: IntegratedV05Brain) -> dict[str, Any]:
    field = brain.base.field
    all_ids = tuple(sorted(field.units))
    receptor_ids = tuple(sorted(int(value) for value in field.receptor_ids))
    receptor_set = set(receptor_ids)
    reservoir_ids = tuple(unit_id for unit_id in all_ids if unit_id not in receptor_set)
    all_coords = [(float(field.units[i].x), float(field.units[i].y)) for i in all_ids]
    reservoir_coords = [
        (float(field.units[i].x), float(field.units[i].y)) for i in reservoir_ids
    ]
    return {
        "total_unit_count": len(all_ids),
        "unit_ids": list(all_ids),
        "receptor_count": len(receptor_ids),
        "receptor_ids": list(receptor_ids),
        "reservoir_count": len(reservoir_ids),
        "reservoir_ids": list(reservoir_ids),
        "coordinate_extents_all": coordinate_extents(all_coords),
        "coordinate_extents_reservoir": coordinate_extents(reservoir_coords),
        "connection_count": len(field.connections),
        "connection_keys": [list(key) for key in sorted(field.connections)],
    }


def field_state_metadata(field_state: dict[str, Any]) -> dict[str, Any]:
    units = list(field_state["units"])
    receptor_ids = sorted(int(value) for value in field_state["receptor_ids"])
    receptor_set = set(receptor_ids)
    reservoir = [row for row in units if int(row["unit_id"]) not in receptor_set]
    all_coords = [(float(row["x"]), float(row["y"])) for row in units]
    reservoir_coords = [(float(row["x"]), float(row["y"])) for row in reservoir]
    return {
        "total_unit_count": len(units),
        "receptor_count": len(receptor_ids),
        "receptor_ids": receptor_ids,
        "reservoir_count": len(reservoir),
        "coordinate_extents_all": coordinate_extents(all_coords),
        "coordinate_extents_reservoir": coordinate_extents(reservoir_coords),
        "connection_count": len(field_state["connections"]),
    }


def topology_signature(metadata: dict[str, Any]) -> str:
    stable = {
        "total_unit_count": metadata["total_unit_count"],
        "unit_ids": metadata.get("unit_ids"),
        "receptor_count": metadata["receptor_count"],
        "receptor_ids": metadata["receptor_ids"],
        "reservoir_count": metadata["reservoir_count"],
        "reservoir_ids": metadata.get("reservoir_ids"),
        "coordinate_extents_all": metadata["coordinate_extents_all"],
        "coordinate_extents_reservoir": metadata["coordinate_extents_reservoir"],
        "connection_count": metadata["connection_count"],
        "connection_keys": metadata.get("connection_keys"),
    }
    return sha256_bytes(canonical_json(stable).encode())


def audit_explicit_contract(contract: dict[str, Any]) -> list[dict[str, Any]]:
    root = Path.cwd()
    candidate_paths: set[Path] = set()
    for pattern in contract["contract_audit_scope"]:
        if "*" in pattern:
            candidate_paths.update(path for path in root.glob(pattern) if path.is_file())
        else:
            path = root / pattern
            if path.is_file():
                candidate_paths.add(path)

    hits: list[dict[str, Any]] = []
    for path in sorted(candidate_paths):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            lowered = line.lower()
            if not any(field in lowered for field in GEOMETRY_FIELD_NAMES):
                continue
            matched = [phrase for phrase in EXPLICIT_CONTRACT_PHRASES if phrase in lowered]
            if not matched:
                continue
            hits.append(
                {
                    "path": str(path.relative_to(root)),
                    "line": line_number,
                    "text": line.strip(),
                    "matched_phrases": matched,
                }
            )
    return hits


def inspect_config(row: dict[str, Any], temp_dir: Path) -> dict[str, Any]:
    config = V05BrainConfig(
        width=int(row["width"]),
        height=int(row["height"]),
        receptor_rows=int(row["receptor_rows"]),
        topology_seed=41,
    )
    construction_error: str | None = None
    brain: IntegratedV05Brain | None = None
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            brain = IntegratedV05Brain(config)
        except Exception as exc:
            construction_error = f"{type(exc).__name__}: {exc}"
        construction_warnings = [
            f"{item.category.__name__}: {item.message}" for item in caught
        ]

    declared_tuple = [config.width, config.height, config.receptor_rows]
    if brain is None:
        return {
            "label": row["label"],
            "declared_v05_config_tuple": declared_tuple,
            "construction_error": construction_error,
            "construction_warnings": construction_warnings,
        }

    nested = brain.base.config
    pre_metadata = topology_metadata(brain)
    pre_signature = topology_signature(pre_metadata)
    checkpoint_path = temp_dir / f"{row['label']}.json"
    brain.save_checkpoint(checkpoint_path)
    checkpoint_wrapper = json.loads(checkpoint_path.read_text(encoding="utf-8"))
    payload = checkpoint_wrapper["payload"]
    checkpoint_field = payload["base"]["payload"]["field"]
    checkpoint_metadata = field_state_metadata(checkpoint_field)

    restored = IntegratedV05Brain.load_checkpoint(checkpoint_path)
    restored_metadata = topology_metadata(restored)
    restored_signature = topology_signature(restored_metadata)
    restored_config = restored.config
    roundtrip_tuple = [
        restored_config.width,
        restored_config.height,
        restored_config.receptor_rows,
    ]
    return {
        "label": row["label"],
        "declared_v05_config_tuple": declared_tuple,
        "nested_v04_config_tuple": [nested.width, nested.height, nested.receptor_rows],
        "construction_error": construction_error,
        "construction_warnings": construction_warnings,
        "realized_topology": pre_metadata,
        "realized_topology_signature": pre_signature,
        "checkpoint_payload_config": payload["config"],
        "checkpoint_nested_field_topology_metadata": checkpoint_metadata,
        "roundtrip_declared_config_tuple": roundtrip_tuple,
        "roundtrip_realized_topology": restored_metadata,
        "roundtrip_realized_topology_signature": restored_signature,
        "roundtrip_declared_config_preserved": roundtrip_tuple == declared_tuple,
        "roundtrip_realized_topology_preserved": restored_signature == pre_signature,
    }


def map_outcome(rows: list[dict[str, Any]], contract_hits: list[dict[str, Any]]) -> str:
    if len(rows) != 5 or any(row.get("construction_error") for row in rows):
        return "INVALID_DIAGNOSTIC"

    baseline_signature = rows[0]["realized_topology_signature"]
    signatures = [row["realized_topology_signature"] for row in rows]
    all_realized_fixed = all(signature == baseline_signature for signature in signatures)
    declared_preserved = all(row["roundtrip_declared_config_preserved"] for row in rows)
    realized_preserved = all(row["roundtrip_realized_topology_preserved"] for row in rows)
    nested_matches_declared = all(
        row["nested_v04_config_tuple"] == row["declared_v05_config_tuple"]
        for row in rows
    )
    no_nondefault_warning = all(not row["construction_warnings"] for row in rows[1:])

    if all_realized_fixed and declared_preserved and realized_preserved:
        if not nested_matches_declared:
            return "PARTIAL_BINDING_OR_INCONSISTENT_ROUNDTRIP"
        if contract_hits:
            return "INTENTIONAL_FIXED_TOPOLOGY_EXPLICIT_CONTRACT"
        if no_nondefault_warning:
            return "SILENT_DECLARED_REALIZED_GEOMETRY_DIVERGENCE"
        return "AMBIGUOUS_CONTRACT"
    return "PARTIAL_BINDING_OR_INCONSISTENT_ROUNDTRIP"


def write_raw(path: Path, records: list[dict[str, Any]]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        for record in records:
            handle.write(canonical_json(record) + "\n")
        handle.flush()
        os.fsync(handle.fileno())

    raw = path.read_bytes()
    parsed = [
        json.loads(line)
        for line in raw.decode().splitlines()
        if line.strip()
    ]
    if parsed != records:
        raise RuntimeError("raw artifact readback mismatch")
    return sha256_bytes(raw)


def run(output_dir: Path) -> None:
    contract, contract_sha256 = load_contract()
    observed_blobs = verify_binding(contract)
    with tempfile.TemporaryDirectory(prefix="sparkbrain-v05-config-contract-") as name:
        temp_dir = Path(name)
        rows = [inspect_config(row, temp_dir) for row in contract["config_matrix"]]

    contract_hits = audit_explicit_contract(contract)
    raw_records: list[dict[str, Any]] = [
        {
            "record_type": "metadata",
            "candidate_id": contract["candidate_id"],
            "analyst_authority": contract["analyst_authority"],
            "git_head": current_git_head(),
            "workflow_run_id": os.environ.get("GITHUB_RUN_ID"),
            "contract_sha256": contract_sha256,
            "source_blobs": observed_blobs,
            "evidentiary_status": contract["evidentiary_status"],
        }
    ]
    raw_records.extend(
        {"record_type": "config_observation", **row} for row in rows
    )
    raw_records.append(
        {
            "record_type": "explicit_contract_audit",
            "hits": contract_hits,
            "scope": contract["contract_audit_scope"],
            "requirement": contract["explicit_contract_requirement"],
        }
    )

    raw_path = output_dir / "raw.jsonl"
    raw_sha256 = write_raw(raw_path, raw_records)
    outcome = map_outcome(rows, contract_hits)
    unique_signatures = sorted(
        {
            row["realized_topology_signature"]
            for row in rows
            if "realized_topology_signature" in row
        }
    )
    summary = {
        "schema": "sparkbrain-architecture-study-summary-v1",
        "candidate_id": contract["candidate_id"],
        "lane": contract["lane"],
        "evidentiary_status": contract["evidentiary_status"],
        "analyst_authority": contract["analyst_authority"],
        "git_head": raw_records[0]["git_head"],
        "workflow_run_id": raw_records[0]["workflow_run_id"],
        "contract_sha256": contract_sha256,
        "raw_sha256": raw_sha256,
        "mapped_outcome": outcome,
        "config_count": len(rows),
        "construction_error_count": sum(
            bool(row.get("construction_error")) for row in rows
        ),
        "nondefault_warning_count": sum(
            len(row.get("construction_warnings", [])) for row in rows[1:]
        ),
        "unique_realized_topology_signatures": unique_signatures,
        "all_roundtrip_declared_config_preserved": all(
            row.get("roundtrip_declared_config_preserved", False) for row in rows
        ),
        "all_roundtrip_realized_topology_preserved": all(
            row.get("roundtrip_realized_topology_preserved", False) for row in rows
        ),
        "explicit_contract_hit_count": len(contract_hits),
        "explicit_contract_hits": contract_hits,
        "stop_condition": contract["stop_condition"],
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = output_dir / "summary.json"
    summary_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    metadata = {
        "contract_path": str(CONTRACT_PATH),
        "contract_sha256": contract_sha256,
        "raw_path": str(raw_path),
        "raw_sha256": raw_sha256,
        "summary_path": str(summary_path),
        "mapped_outcome": outcome,
        "test_manifest_opened": False,
        "formal_identity_created": False,
        "started_created": False,
    }
    (output_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    contract, contract_sha256 = load_contract()
    observed_blobs = verify_binding(contract)
    if args.preflight_only:
        print(
            json.dumps(
                {
                    "status": "PREFLIGHT_OK",
                    "contract_sha256": contract_sha256,
                    "source_blobs": observed_blobs,
                    "config_count": len(contract["config_matrix"]),
                    "topology_seed": contract["topology_seed"],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return

    if args.output_dir is None:
        parser.error("--output-dir is required unless --preflight-only is used")
    run(args.output_dir)


if __name__ == "__main__":
    main()
