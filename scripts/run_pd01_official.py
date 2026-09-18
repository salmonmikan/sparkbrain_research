#!/usr/bin/env python3
"""One-way PD0.1 formal acquisition and deterministic scoring."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from sparkbrain.external_validation.fading_memory import (
    PD01ScoreRow,
    PD01WorldConfig,
    build_pd01_inputs,
    build_pd01_targets,
    classify_pd01_terminal,
    fit_ridge_readout,
    pd01_primary_statistics,
    predict_ridge,
    run_reservoir_probe_features,
    run_v04_probe_features,
)

ROOT = Path(__file__).resolve().parents[1]
AUTHORITY_PATH = ROOT / "research" / "pd01" / "execution_authority.json"
CONTRACT_PATH = ROOT / "research" / "pd01" / "formal_contract.json"
EXPECTED_ANALYST = "91a05bad6d130f89975e776960a1d25d764fba32"
EXPECTED_IDENTITY = "pd01-long-history-fading-memory-official-v1"
MODEL_CANDIDATE = "sparkbrain_v04"
MODEL_COMPARATOR = "fixed_contractive_reservoir"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _json_digest(value: Any) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


def _load_authority(analyst_commit: str) -> tuple[dict[str, Any], dict[str, Any]]:
    authority = json.loads(AUTHORITY_PATH.read_text(encoding="utf-8"))
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    if analyst_commit != EXPECTED_ANALYST or authority["evidence_analyst_commit"] != EXPECTED_ANALYST:
        raise SystemExit("PD01 analyst authority mismatch")
    if authority["formal_identity"] != EXPECTED_IDENTITY or authority["no_retry"] is not True:
        raise SystemExit("PD01 identity/one-way authority mismatch")
    if contract["formal_identity_proposed"] != EXPECTED_IDENTITY:
        raise SystemExit("PD01 scientific contract identity mismatch")
    return authority, contract


def _fit_dev_readouts() -> tuple[tuple[float, ...], tuple[float, ...]]:
    world = PD01WorldConfig()
    histories = build_pd01_inputs("DEV", world)
    targets = {row.history_id: row.target for row in build_pd01_targets("DEV", world)}
    ids = [row.history_id for row in histories]
    if len(ids) != 512 or set(ids) != set(targets):
        raise SystemExit("PD01 DEV inventory mismatch")
    labels = [targets[history_id] for history_id in ids]
    candidate_features = [run_v04_probe_features(row.observations) for row in histories]
    comparator_features = [run_reservoir_probe_features(row.observations) for row in histories]
    return (
        fit_ridge_readout(candidate_features, labels),
        fit_ridge_readout(comparator_features, labels),
    )


def prestart_smoke(args: argparse.Namespace) -> None:
    _, contract = _load_authority(args.analyst_commit)
    world = PD01WorldConfig()
    dev = build_pd01_inputs("DEV", world)
    if len(dev) != contract["inventory"]["dev_histories"]:
        raise SystemExit("PD01 DEV input inventory mismatch")
    probe = dev[0]
    if len(run_v04_probe_features(probe.observations)) != 64:
        raise SystemExit("PD01 candidate feature width mismatch")
    if len(run_reservoir_probe_features(probe.observations)) != 64:
        raise SystemExit("PD01 comparator feature width mismatch")
    print("PD01 prestart smoke: PASS")


def acquire_raw(args: argparse.Namespace) -> None:
    authority, contract = _load_authority(args.analyst_commit)
    candidate_weights, comparator_weights = _fit_dev_readouts()
    test_inputs = build_pd01_inputs("TEST", PD01WorldConfig())
    if len(test_inputs) != contract["inventory"]["test_histories"]:
        raise SystemExit("PD01 TEST input inventory mismatch")

    inventory_rows: list[dict[str, Any]] = []
    raw_rows: list[dict[str, Any]] = []
    for row in test_inputs:
        obs = [[float(a), float(b)] for a, b in row.observations]
        inventory_rows.append(
            {
                "history_id": row.history_id,
                "base_world_id": row.base_world_id,
                "lag": row.lag,
                "observations_sha256": _json_digest(obs),
                "observation_count": len(obs),
            }
        )
        candidate_feature = run_v04_probe_features(row.observations)
        comparator_feature = run_reservoir_probe_features(row.observations)
        raw_rows.extend(
            [
                {
                    "history_id": row.history_id,
                    "base_world_id": row.base_world_id,
                    "lag": row.lag,
                    "model_id": MODEL_CANDIDATE,
                    "score": predict_ridge(candidate_feature, candidate_weights),
                },
                {
                    "history_id": row.history_id,
                    "base_world_id": row.base_world_id,
                    "lag": row.lag,
                    "model_id": MODEL_COMPARATOR,
                    "score": predict_ridge(comparator_feature, comparator_weights),
                },
            ]
        )

    if len(raw_rows) != contract["inventory"]["test_raw_prediction_rows"]:
        raise SystemExit("PD01 raw cardinality mismatch")
    args.raw.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in raw_rows), encoding="utf-8")
    args.inventory.write_text(json.dumps(inventory_rows, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest = {
        "schema_version": 1,
        "run_identity": EXPECTED_IDENTITY,
        "protocol_id": authority["protocol_id"],
        "evidence_analyst_commit": args.analyst_commit,
        "exact_package_commit": args.package_commit,
        "started_ref": args.started_ref,
        "raw_row_count": len(raw_rows),
        "history_count": len(test_inputs),
        "raw_sha256": _sha256(args.raw),
        "input_inventory_sha256": _sha256(args.inventory),
        "candidate_readout_sha256": _json_digest(candidate_weights),
        "comparator_readout_sha256": _json_digest(comparator_weights),
        "models": [MODEL_CANDIDATE, MODEL_COMPARATOR],
        "targets_materialized": False,
    }
    args.manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def score_preserved(args: argparse.Namespace) -> None:
    authority, contract = _load_authority(args.analyst_commit)
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if manifest["raw_sha256"] != _sha256(args.raw):
        raise SystemExit("PD01 preserved raw digest mismatch")
    if manifest["input_inventory_sha256"] != _sha256(args.inventory):
        raise SystemExit("PD01 preserved inventory digest mismatch")
    if manifest["raw_row_count"] != 2048 or manifest["history_count"] != 1024:
        raise SystemExit("PD01 preserved cardinality mismatch")
    if manifest["targets_materialized"] is not False:
        raise SystemExit("PD01 pre-target manifest leakage")
    raw_rows = [json.loads(line) for line in args.raw.read_text(encoding="utf-8").splitlines() if line]
    if len(raw_rows) != 2048:
        raise SystemExit("PD01 raw row count mismatch")
    by_history: dict[str, dict[str, dict[str, Any]]] = {}
    for row in raw_rows:
        model = str(row["model_id"])
        if model not in {MODEL_CANDIDATE, MODEL_COMPARATOR}:
            raise SystemExit("PD01 unknown model row")
        bucket = by_history.setdefault(str(row["history_id"]), {})
        if model in bucket:
            raise SystemExit("PD01 duplicate model/history row")
        bucket[model] = row
    targets = build_pd01_targets("TEST", PD01WorldConfig())
    target_map = {row.history_id: row.target for row in targets}
    if len(target_map) != 1024 or set(target_map) != set(by_history):
        raise SystemExit("PD01 target/raw history join mismatch")
    score_rows: list[PD01ScoreRow] = []
    for history_id in sorted(target_map):
        bucket = by_history[history_id]
        if set(bucket) != {MODEL_CANDIDATE, MODEL_COMPARATOR}:
            raise SystemExit("PD01 incomplete model/history join")
        candidate = bucket[MODEL_CANDIDATE]
        comparator = bucket[MODEL_COMPARATOR]
        if candidate["base_world_id"] != comparator["base_world_id"] or candidate["lag"] != comparator["lag"]:
            raise SystemExit("PD01 paired metadata mismatch")
        score_rows.append(
            PD01ScoreRow(
                base_world_id=int(candidate["base_world_id"]),
                lag=int(candidate["lag"]),
                candidate_score=float(candidate["score"]),
                comparator_score=float(comparator["score"]),
                target=int(target_map[history_id]),
            )
        )
    stats = pd01_primary_statistics(score_rows, resamples=10_000, seed=19_901)
    result_class = classify_pd01_terminal(stats)
    args.output.mkdir(parents=True, exist_ok=False)
    report = {
        "schema_version": 1,
        "run_identity": EXPECTED_IDENTITY,
        "result_class": result_class,
        "primary_statistics": stats,
        "interpretation_cap": authority["pass_interpretation_cap"],
        "raw_preservation_commit": args.preservation_commit,
        "exact_package_commit": args.package_commit,
        "evidence_analyst_commit": args.analyst_commit,
        "test_target_count": len(target_map),
        "joined_history_count": len(score_rows),
    }
    (args.output / "report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    binding = {
        "raw_sha256": _sha256(args.raw),
        "manifest_sha256": _sha256(args.manifest),
        "input_inventory_sha256": _sha256(args.inventory),
        "target_sha256": _json_digest(sorted(target_map.items())),
        "protocol_id": authority["protocol_id"],
        "formal_contract_git_blob": authority["formal_contract_git_blob"],
        "implementation_git_blob": authority["implementation_git_blob"],
    }
    (args.output / "binding.json").write_text(json.dumps(binding, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser()
    commands = root.add_subparsers(dest="command", required=True)
    smoke = commands.add_parser("prestart-smoke")
    smoke.add_argument("--analyst-commit", required=True)
    smoke.set_defaults(func=prestart_smoke)
    acquire = commands.add_parser("acquire-raw")
    acquire.add_argument("--raw", type=Path, required=True)
    acquire.add_argument("--manifest", type=Path, required=True)
    acquire.add_argument("--inventory", type=Path, required=True)
    acquire.add_argument("--analyst-commit", required=True)
    acquire.add_argument("--package-commit", required=True)
    acquire.add_argument("--started-ref", required=True)
    acquire.set_defaults(func=acquire_raw)
    score = commands.add_parser("score-preserved")
    score.add_argument("--raw", type=Path, required=True)
    score.add_argument("--manifest", type=Path, required=True)
    score.add_argument("--inventory", type=Path, required=True)
    score.add_argument("--output", type=Path, required=True)
    score.add_argument("--analyst-commit", required=True)
    score.add_argument("--package-commit", required=True)
    score.add_argument("--preservation-commit", required=True)
    score.set_defaults(func=score_preserved)
    return root


def main() -> None:
    args = parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
