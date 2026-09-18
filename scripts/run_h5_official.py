#!/usr/bin/env python3
"""Execute the prospectively fixed H5 formal chain without changing science."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from sparkbrain.h5_work import (
    canonical_raw_json,
    dev_validate,
    quality_pass,
    run_cell,
    score_rows,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "configs/experiments/h5/formal_contract.json"
AUTHORITY_PATH = ROOT / "configs/experiments/h5/execution_authority.json"

EXPECTED_COUNTER_FIELDS = {
    "scheduler_writes",
    "scheduler_reads",
    "target_state_accesses",
    "state_materializations",
    "state_decay_evaluations",
    "threshold_relax_evaluations",
    "eligibility_edge_touches",
    "eligibility_multiplications",
    "route_edge_checks",
    "message_traversals",
    "activation_additions",
    "eligibility_additions",
    "threshold_additions",
    "residual_multiplications",
    "fanout_index_lookups",
}


def _read_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"expected JSON object: {path}")
    return value


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _git_blob(path: str) -> str:
    result = subprocess.run(
        ["git", "hash-object", path],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _git_head() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _load_bound_package() -> tuple[dict[str, Any], dict[str, Any]]:
    contract = _read_object(CONTRACT_PATH)
    authority = _read_object(AUTHORITY_PATH)
    if authority["formal_contract_git_blob"] != _git_blob(
        "configs/experiments/h5/formal_contract.json"
    ):
        raise SystemExit("H5 formal contract blob drift")
    if authority["h5_module_git_blob"] != _git_blob("src/sparkbrain/h5_work.py"):
        raise SystemExit("H5 work module blob drift")
    if authority["official_runner_git_blob"] != _git_blob(
        "scripts/run_h5_official.py"
    ):
        raise SystemExit("H5 official runner blob drift")
    if authority["preserver_git_blob"] != _git_blob(
        "scripts/preserve_h5_boundary.py"
    ):
        raise SystemExit("H5 preserver blob drift")
    if authority["one_way_workflow_git_blob"] != _git_blob(
        ".github/workflows/h5-formal-one-way.yml"
    ):
        raise SystemExit("H5 one-way workflow blob drift")
    if contract["schema"] != authority["protocol_id"]:
        raise SystemExit("H5 protocol/contract schema drift")
    if contract["phase"] != "H5_REVISED_DENSE_COMPARATOR_READY_FOR_ANALYST_REVIEW":
        raise SystemExit("H5 frozen scientific phase drift")
    if contract["execution_authorized"] is not False:
        raise SystemExit("H5 scientific contract was rewritten for execution")
    if contract["formal_identity"] is not None:
        raise SystemExit("H5 frozen scientific contract identity changed")
    return contract, authority


def _validate_rows(
    rows: list[dict[str, Any]],
    contract: dict[str, Any],
) -> tuple[int, int]:
    sparse_expected = int(
        contract["formal_test_workloads"]["sparse_primary"]["cell_count"]
    )
    dense_expected = int(
        contract["formal_test_workloads"]["dense_control"]["cell_count"]
    )
    if len(rows) != sparse_expected + dense_expected:
        raise SystemExit("H5 formal raw total cardinality mismatch")
    sparse_rows = [row for row in rows if not row.get("dense_control", False)]
    dense_rows = [row for row in rows if row.get("dense_control", False)]
    if len(sparse_rows) != sparse_expected:
        raise SystemExit("H5 sparse raw cardinality mismatch")
    if len(dense_rows) != dense_expected:
        raise SystemExit("H5 dense-control raw cardinality mismatch")

    keys: set[tuple[str, int, float, int, int, bool]] = set()
    for row in rows:
        key = (
            str(row["family"]),
            int(row["size"]),
            float(row["activity_fraction"]),
            int(row["horizon"]),
            int(row["seed"]),
            bool(row.get("dense_control", False)),
        )
        if key in keys:
            raise SystemExit("H5 duplicate formal raw cell")
        keys.add(key)
        for side in ("candidate", "dense"):
            counters = row[f"{side}_counters"]
            if set(counters) != EXPECTED_COUNTER_FIELDS:
                raise SystemExit(f"H5 {side} counter schema mismatch")
            if any(
                not isinstance(value, int)
                or isinstance(value, bool)
                or value < 0
                for value in counters.values()
            ):
                raise SystemExit(f"H5 {side} counter value invalid")
            if sum(counters.values()) != int(row[f"{side}_work"]):
                raise SystemExit(f"H5 {side} total-work invariant failed")
        if row["dense_algorithm"] != "standalone_dense_eager_calendar":
            raise SystemExit("H5 dense algorithm identity drift")
        forbidden = {
            "classification",
            "primary_mean_work_reduction",
            "primary_ci95",
            "activity_mean_reductions",
            "work_reduction",
        }
        if forbidden.intersection(row):
            raise SystemExit("H5 raw contains forbidden pre-preserve score fields")
    return len(sparse_rows), len(dense_rows)


def _formal_rows(contract: dict[str, Any]) -> list[dict[str, Any]]:
    workloads = contract["formal_test_workloads"]
    rows: list[dict[str, Any]] = []
    sparse = workloads["sparse_primary"]
    for family in sparse["families"]:
        for size in sparse["sizes"]:
            for activity in sparse["activity_fractions"]:
                for seed in sparse["seeds"]:
                    row = run_cell(
                        family=str(family),
                        size=int(size),
                        activity_fraction=float(activity),
                        horizon=int(sparse["horizon"]),
                        seed=int(seed),
                    )
                    row["dense_control"] = False
                    rows.append(row)
    dense = workloads["dense_control"]
    for family in dense["families"]:
        for size in dense["sizes"]:
            for activity in dense["activity_fractions"]:
                for seed in dense["seeds"]:
                    row = run_cell(
                        family=str(family),
                        size=int(size),
                        activity_fraction=float(activity),
                        horizon=int(dense["horizon"]),
                        seed=int(seed),
                    )
                    row["dense_control"] = True
                    rows.append(row)
    _validate_rows(rows, contract)
    return rows


def _prestart_smoke(args: argparse.Namespace) -> None:
    contract, authority = _load_bound_package()
    if args.analyst_commit != authority["evidence_analyst_commit"]:
        raise SystemExit("H5 analyst authority argument mismatch")
    rows = dev_validate()
    expected = len(contract["dev_only_validation"]["families"])
    if len(rows) != expected or not all(quality_pass(row) for row in rows):
        raise SystemExit("H5 DEV-only pre-START smoke failed")
    print("H5 formal pre-START smoke: PASS")


def _acquire_raw(args: argparse.Namespace) -> None:
    contract, authority = _load_bound_package()
    if args.analyst_commit != authority["evidence_analyst_commit"]:
        raise SystemExit("H5 analyst authority argument mismatch")
    if args.package_commit != _git_head():
        raise SystemExit("H5 exact package commit mismatch")
    if args.package_commit == authority["reviewed_scientific_head"]:
        raise SystemExit("H5 execution package must include authority mechanics")
    if args.started_ref != authority["control_ref"]:
        raise SystemExit("H5 STARTED ref mismatch")

    rows = _formal_rows(contract)
    sparse_count, dense_count = _validate_rows(rows, contract)
    args.raw.write_text(canonical_raw_json(rows), encoding="utf-8")

    inventory = {
        "schema_version": 1,
        "state": "FORMAL_INPUT_INVENTORY",
        "protocol_id": authority["protocol_id"],
        "formal_identity": authority["formal_identity"],
        "sparse_primary": contract["formal_test_workloads"]["sparse_primary"],
        "dense_control": contract["formal_test_workloads"]["dense_control"],
        "graph": contract["graph"],
        "runtime_binding": contract["runtime_binding"],
        "expected_sparse_rows": sparse_count,
        "expected_dense_control_rows": dense_count,
        "expected_total_rows": sparse_count + dense_count,
    }
    args.inventory.write_text(
        json.dumps(inventory, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    manifest = {
        "schema_version": 1,
        "state": "RAW_UNSCORED",
        "protocol_id": authority["protocol_id"],
        "formal_identity": authority["formal_identity"],
        "evidence_analyst_commit": authority["evidence_analyst_commit"],
        "evidence_analyst_mailbox_tip": authority[
            "evidence_analyst_mailbox_tip"
        ],
        "exact_package_commit": args.package_commit,
        "started_ref": args.started_ref,
        "formal_contract_git_blob": authority["formal_contract_git_blob"],
        "h5_module_git_blob": authority["h5_module_git_blob"],
        "official_runner_git_blob": authority["official_runner_git_blob"],
        "preserver_git_blob": authority["preserver_git_blob"],
        "one_way_workflow_git_blob": authority["one_way_workflow_git_blob"],
        "raw_sha256": _sha256(args.raw),
        "inventory_sha256": _sha256(args.inventory),
        "row_count": sparse_count + dense_count,
        "sparse_row_count": sparse_count,
        "dense_control_row_count": dense_count,
        "contains_formal_classification": False,
    }
    args.manifest.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _score_preserved(args: argparse.Namespace) -> None:
    contract, authority = _load_bound_package()
    if args.analyst_commit != authority["evidence_analyst_commit"]:
        raise SystemExit("H5 analyst authority argument mismatch")
    if args.package_commit != _git_head():
        raise SystemExit("H5 scoring package commit mismatch")

    rows_value = json.loads(args.raw.read_text(encoding="utf-8"))
    if not isinstance(rows_value, list) or not all(
        isinstance(row, dict) for row in rows_value
    ):
        raise SystemExit("H5 preserved raw must be a JSON list of objects")
    rows = [dict(row) for row in rows_value]
    sparse_count, dense_count = _validate_rows(rows, contract)
    manifest = _read_object(args.manifest)
    inventory = _read_object(args.inventory)

    if manifest["state"] != "RAW_UNSCORED":
        raise SystemExit("H5 preserved manifest state mismatch")
    if manifest["formal_identity"] != authority["formal_identity"]:
        raise SystemExit("H5 preserved identity mismatch")
    if manifest["evidence_analyst_commit"] != authority[
        "evidence_analyst_commit"
    ]:
        raise SystemExit("H5 preserved analyst authority mismatch")
    if manifest["exact_package_commit"] != args.package_commit:
        raise SystemExit("H5 preserved package commit mismatch")
    if manifest["raw_sha256"] != _sha256(args.raw):
        raise SystemExit("H5 preserved raw digest mismatch")
    if manifest["inventory_sha256"] != _sha256(args.inventory):
        raise SystemExit("H5 preserved inventory digest mismatch")
    if manifest["contains_formal_classification"] is not False:
        raise SystemExit("H5 raw manifest crossed scoring boundary early")
    if int(manifest["row_count"]) != sparse_count + dense_count:
        raise SystemExit("H5 preserved total row count mismatch")
    if int(manifest["sparse_row_count"]) != sparse_count:
        raise SystemExit("H5 preserved sparse row count mismatch")
    if int(manifest["dense_control_row_count"]) != dense_count:
        raise SystemExit("H5 preserved dense row count mismatch")
    if int(inventory["expected_total_rows"]) != sparse_count + dense_count:
        raise SystemExit("H5 preserved inventory cardinality mismatch")

    score = score_rows(
        rows,
        bootstrap_seed=int(
            contract["primary_statistic"]["bootstrap"]["seed"]
        ),
        bootstrap_replicates=int(
            contract["primary_statistic"]["bootstrap"]["replicates"]
        ),
    )
    result_class = str(score["classification"])
    allowed = {
        "PASS_WORK_REDUCTION",
        "FAIL_NO_USEFUL_WORK_REDUCTION",
        "INCONCLUSIVE",
        "INVALID_QUALITY_GUARD",
    }
    if result_class not in allowed:
        raise SystemExit("H5 scorer emitted unknown terminal class")

    args.output.mkdir(parents=True, exist_ok=False)
    report = {
        "schema_version": 1,
        "state": "TERMINAL_CLASSIFICATION",
        "protocol_id": authority["protocol_id"],
        "formal_identity": authority["formal_identity"],
        "evidence_analyst_commit": authority["evidence_analyst_commit"],
        "exact_package_commit": args.package_commit,
        "raw_preservation_commit": args.preservation_commit,
        "raw_sha256": manifest["raw_sha256"],
        "row_count": sparse_count + dense_count,
        "sparse_row_count": sparse_count,
        "dense_control_row_count": dense_count,
        "result_class": result_class,
        "score": score,
    }
    (args.output / "report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    bindings = {
        "formal_contract_git_blob": authority["formal_contract_git_blob"],
        "h5_module_git_blob": authority["h5_module_git_blob"],
        "official_runner_git_blob": authority["official_runner_git_blob"],
        "preserver_git_blob": authority["preserver_git_blob"],
        "one_way_workflow_git_blob": authority["one_way_workflow_git_blob"],
        "engine_blob": contract["source_binding"]["engine_blob"],
        "model_blob": contract["source_binding"]["model_blob"],
        "package_blob": contract["source_binding"]["package_blob"],
        "runtime": contract["runtime_binding"]["python"],
        "candidate": contract["candidate"]["implementation"],
        "comparator": contract["comparator"]["implementation"],
        "scorer": contract["scorer_binding"]["function"],
        "preserver": contract["raw_preservation_contract"]["preserver"],
    }
    (args.output / "bindings.json").write_text(
        json.dumps(bindings, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    raw_reference = {
        "preserve_ref": authority["preserve_ref"],
        "preservation_commit": args.preservation_commit,
        "raw_sha256": manifest["raw_sha256"],
        "inventory_sha256": manifest["inventory_sha256"],
        "row_count": manifest["row_count"],
    }
    (args.output / "raw_reference.json").write_text(
        json.dumps(raw_reference, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    smoke = subparsers.add_parser("prestart-smoke")
    smoke.add_argument("--analyst-commit", required=True)
    smoke.set_defaults(func=_prestart_smoke)

    acquire = subparsers.add_parser("acquire-raw")
    acquire.add_argument("--raw", required=True, type=Path)
    acquire.add_argument("--manifest", required=True, type=Path)
    acquire.add_argument("--inventory", required=True, type=Path)
    acquire.add_argument("--analyst-commit", required=True)
    acquire.add_argument("--package-commit", required=True)
    acquire.add_argument("--started-ref", required=True)
    acquire.set_defaults(func=_acquire_raw)

    score = subparsers.add_parser("score-preserved")
    score.add_argument("--raw", required=True, type=Path)
    score.add_argument("--manifest", required=True, type=Path)
    score.add_argument("--inventory", required=True, type=Path)
    score.add_argument("--output", required=True, type=Path)
    score.add_argument("--analyst-commit", required=True)
    score.add_argument("--package-commit", required=True)
    score.add_argument("--preservation-commit", required=True)
    score.set_defaults(func=_score_preserved)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
