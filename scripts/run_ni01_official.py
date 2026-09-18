#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import socket
from collections import defaultdict
from pathlib import Path
from typing import Any

from sparkbrain.evaluation.ni01 import (
    ScoredStep,
    comparator_decision,
    coverage_matched_threshold,
    selective_decision_loss,
    summarize_effect,
)
from sparkbrain.evaluation.runner import _probabilities
from sparkbrain.model import BrainConfig
from sparkbrain.tasks.worlds import generate_episode
from sparkbrain.worlds import LABELS, build_reference_brain

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "configs/experiments/ni01/preformal_contract.json"
AUTHORITY_PATH = ROOT / "configs/experiments/ni01/execution_authority.json"

EXPECTED_ANALYST = "d3626617c3b054afd726e468682aaa02d613bca0"
EXPECTED_IDENTITY = "ni01-no-ignition-selective-prediction-official-v1"
EXPECTED_PROTOCOL = "ni01-no-ignition-selective-prediction-protocol-v1"
FORBIDDEN_RAW_KEYS = {
    "truth",
    "decision_justified",
    "target",
    "scenario_tags_from_target",
}


def _disable_network() -> None:
    def blocked(*_args: object, **_kwargs: object) -> None:
        raise RuntimeError("NI01 formal Python network access is disabled")

    socket.socket = blocked  # type: ignore[assignment]
    socket.create_connection = blocked  # type: ignore[assignment]


def _load(analyst_commit: str) -> tuple[dict[str, Any], dict[str, Any]]:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    authority = json.loads(AUTHORITY_PATH.read_text(encoding="utf-8"))
    if analyst_commit != EXPECTED_ANALYST:
        raise SystemExit("NI01 analyst commit mismatch")
    if authority["evidence_analyst_commit"] != EXPECTED_ANALYST:
        raise SystemExit("NI01 authority drift")
    if authority["formal_identity"] != EXPECTED_IDENTITY:
        raise SystemExit("NI01 identity authority drift")
    if contract["formal_identity_plan"]["identity"] != EXPECTED_IDENTITY:
        raise SystemExit("NI01 scientific identity drift")
    if contract["protocol_id"] != EXPECTED_PROTOCOL:
        raise SystemExit("NI01 protocol drift")
    return contract, authority


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _target_blind_steps(world: str, seed: int, split: str) -> list[dict[str, Any]]:
    episode = generate_episode(world, seed=seed, split=split, steps=30)
    brain = build_reference_brain(BrainConfig(random_seed=seed))
    rows: list[dict[str, Any]] = []
    for item in episode.steps:
        obs = item.observation
        sensory_id = f"sensory:{obs.evidence_label}"
        brain.inject_stimulus(
            target=sensory_id,
            label=obs.evidence_label,
            time=max(brain.time, obs.delivery_time),
            strength=obs.strength,
            source=obs.source_id,
            evidence_id=obs.evidence_id,
            metadata={"sensor": obs.source_id, "object_id": obs.object_id},
        )
        brain.run()
        probabilities = _probabilities(brain)
        rows.append(
            {
                "world": world,
                "seed": seed,
                "step_index": obs.step_index,
                "candidate_prediction": brain.prediction,
                "probabilities": [probabilities[label] for label in LABELS],
                "confidence": max(probabilities.values()),
            }
        )
    return rows


def _derive_thresholds(contract: dict[str, Any]) -> dict[str, float]:
    thresholds: dict[str, float] = {}
    dev = contract["inputs"]["dev"]
    for world in contract["inputs"]["worlds"]:
        native_decided: list[bool] = []
        confidences: list[float] = []
        for seed in range(dev["seed_start"], dev["seed_end_inclusive"] + 1):
            rows = _target_blind_steps(world, seed, "dev")
            native_decided.extend(
                row["candidate_prediction"] is not None for row in rows
            )
            confidences.extend(float(row["confidence"]) for row in rows)
        thresholds[world] = coverage_matched_threshold(native_decided, confidences)
    return thresholds


def _assert_raw_row(row: dict[str, Any]) -> None:
    if FORBIDDEN_RAW_KEYS.intersection(row):
        raise SystemExit("NI01 raw target leakage")
    if set(row) != {
        "world",
        "seed",
        "step_index",
        "candidate_prediction",
        "comparator_prediction",
        "probabilities",
        "confidence",
        "threshold",
    }:
        raise SystemExit(f"NI01 unexpected raw schema: {sorted(row)}")
    probabilities = row["probabilities"]
    if len(probabilities) != len(LABELS):
        raise SystemExit("NI01 probability vector cardinality changed")


def prestart_smoke(args: argparse.Namespace) -> None:
    contract, _ = _load(args.analyst_commit)
    worlds = contract["inputs"]["worlds"]
    first_seed = contract["inputs"]["dev"]["seed_start"]
    for world in worlds:
        candidate_rows: list[dict[str, Any]] = []
        for seed in (first_seed, first_seed + 1):
            candidate_rows.extend(_target_blind_steps(world, seed, "dev"))
        threshold = coverage_matched_threshold(
            [row["candidate_prediction"] is not None for row in candidate_rows],
            [float(row["confidence"]) for row in candidate_rows],
        )
        for base in candidate_rows[:3]:
            probabilities = [float(value) for value in base["probabilities"]]
            raw = dict(base)
            raw["comparator_prediction"] = comparator_decision(
                probabilities, LABELS, threshold
            )
            raw["threshold"] = threshold
            _assert_raw_row(raw)
    print("NI01 target-free pre-START smoke: PASS")


def acquire_raw(args: argparse.Namespace) -> None:
    contract, authority = _load(args.analyst_commit)
    thresholds = _derive_thresholds(contract)
    raw_rows: list[dict[str, Any]] = []
    inventory: list[dict[str, Any]] = []
    test = contract["inputs"]["test"]
    for world in contract["inputs"]["worlds"]:
        threshold = thresholds[world]
        for seed in range(test["seed_start"], test["seed_end_inclusive"] + 1):
            episode_rows = _target_blind_steps(world, seed, "test")
            if len(episode_rows) != contract["inputs"]["steps_per_episode"]:
                raise SystemExit("NI01 TEST episode length mismatch")
            for base in episode_rows:
                probabilities = [float(value) for value in base["probabilities"]]
                raw = dict(base)
                raw["comparator_prediction"] = comparator_decision(
                    probabilities, LABELS, threshold
                )
                raw["threshold"] = threshold
                _assert_raw_row(raw)
                raw_rows.append(raw)
            inventory.append({"world": world, "seed": seed, "steps": len(episode_rows)})

    expected = contract["raw_contract"]["expected_test_step_count"]
    if len(raw_rows) != expected:
        detail = f"NI01 raw cardinality mismatch: {len(raw_rows)} != {expected}"
        raise SystemExit(detail)
    keys = {
        (row["world"], int(row["seed"]), int(row["step_index"])) for row in raw_rows
    }
    if len(keys) != expected:
        raise SystemExit("NI01 raw join keys are not unique")

    args.raw.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in raw_rows),
        encoding="utf-8",
    )
    args.inventory.write_text(
        json.dumps(inventory, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    manifest = {
        "schema_version": 1,
        "protocol_id": EXPECTED_PROTOCOL,
        "run_identity": EXPECTED_IDENTITY,
        "evidence_analyst_commit": EXPECTED_ANALYST,
        "exact_package_commit": args.package_commit,
        "started_ref": args.started_ref,
        "worlds": contract["inputs"]["worlds"],
        "test_episode_count": contract["raw_contract"]["expected_test_episode_count"],
        "test_step_count": expected,
        "thresholds_by_world": thresholds,
        "threshold_source": "target-free DEV native-coverage matching only",
        "targets_materialized": False,
        "raw_forbidden_keys": sorted(FORBIDDEN_RAW_KEYS),
        "source_binding": contract["source_binding"],
        "authority_contract_blob": authority["formal_contract_git_blob"],
    }
    args.manifest.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _load_raw(path: Path) -> list[dict[str, Any]]:
    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    for row in rows:
        _assert_raw_row(row)
    return rows


def score_preserved(args: argparse.Namespace) -> None:
    contract, authority = _load(args.analyst_commit)
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    inventory = json.loads(args.inventory.read_text(encoding="utf-8"))
    if manifest["targets_materialized"] is not False:
        raise SystemExit("NI01 preserved manifest indicates target leakage")
    if manifest["run_identity"] != EXPECTED_IDENTITY:
        raise SystemExit("NI01 preserved identity mismatch")
    raw_rows = _load_raw(args.raw)
    expected = contract["raw_contract"]["expected_test_step_count"]
    if len(raw_rows) != expected:
        raise SystemExit("NI01 preserved raw cardinality mismatch")
    if len(inventory) != contract["raw_contract"]["expected_test_episode_count"]:
        raise SystemExit("NI01 preserved inventory cardinality mismatch")

    raw_map: dict[tuple[str, int, int], dict[str, Any]] = {}
    for row in raw_rows:
        key = (row["world"], int(row["seed"]), int(row["step_index"]))
        if key in raw_map:
            raise SystemExit("NI01 duplicate preserved raw join key")
        raw_map[key] = row

    target_map: dict[tuple[str, int, int], tuple[str, bool]] = {}
    test = contract["inputs"]["test"]
    for world in contract["inputs"]["worlds"]:
        for seed in range(test["seed_start"], test["seed_end_inclusive"] + 1):
            episode = generate_episode(world, seed=seed, split="test", steps=30)
            for item in episode.steps:
                key = (world, seed, item.observation.step_index)
                target = item.target
                if key in target_map:
                    raise SystemExit("NI01 duplicate target join key")
                target_map[key] = (
                    target.belief_truth_by_object["object"],
                    bool(target.decision_justified_by_object["object"]),
                )
    if set(raw_map) != set(target_map):
        missing = len(set(target_map) - set(raw_map))
        extra = len(set(raw_map) - set(target_map))
        detail = f"NI01 raw/target join mismatch missing={missing} extra={extra}"
        raise SystemExit(detail)

    scored: list[ScoredStep] = []
    coverage: dict[str, dict[str, int]] = defaultdict(
        lambda: {"candidate_decisions": 0, "comparator_decisions": 0, "steps": 0}
    )
    for key in sorted(raw_map):
        row = raw_map[key]
        truth, justified = target_map[key]
        candidate = row["candidate_prediction"]
        comparator = row["comparator_prediction"]
        candidate_loss = selective_decision_loss(
            candidate, truth=truth, decision_justified=justified
        )
        comparator_loss = selective_decision_loss(
            comparator, truth=truth, decision_justified=justified
        )
        world, seed, _ = key
        scored.append(
            ScoredStep(
                world=world,
                episode_id=f"{world}:{seed}",
                candidate_loss=candidate_loss,
                comparator_loss=comparator_loss,
            )
        )
        coverage[world]["steps"] += 1
        coverage[world]["candidate_decisions"] += int(candidate is not None)
        coverage[world]["comparator_decisions"] += int(comparator is not None)

    summary = summarize_effect(
        scored,
        worlds=contract["inputs"]["worlds"],
        episodes_per_world=test["episodes_per_world"],
        steps_per_episode=contract["inputs"]["steps_per_episode"],
        resamples=contract["statistics"]["resamples"],
        seed=contract["statistics"]["bootstrap_seed"],
    )
    coverage_report: dict[str, dict[str, float]] = {}
    guard = True
    for world in contract["inputs"]["worlds"]:
        counts = coverage[world]
        candidate_cov = counts["candidate_decisions"] / counts["steps"]
        comparator_cov = counts["comparator_decisions"] / counts["steps"]
        difference = abs(candidate_cov - comparator_cov)
        coverage_report[world] = {
            "candidate": candidate_cov,
            "comparator": comparator_cov,
            "absolute_difference": difference,
        }
        guard = guard and difference <= 0.03

    if (
        guard
        and summary.ci95_lower >= 0.02
        and all(value > 0.0 for value in summary.world_effects.values())
    ):
        result_class = "PASS_NATIVE_NO_IGNITION_ADDS_SELECTIVE_VALUE"
    elif guard and summary.ci95_upper <= 0.005:
        result_class = "FAIL_REDUCED_BY_CONFIDENCE_ABSTENTION"
    else:
        result_class = "INCONCLUSIVE"

    args.output.mkdir(parents=True, exist_ok=False)
    report = {
        "schema_version": 1,
        "protocol_id": EXPECTED_PROTOCOL,
        "run_identity": EXPECTED_IDENTITY,
        "result_class": result_class,
        "candidate_overall_loss": summary.candidate_loss,
        "comparator_overall_loss": summary.comparator_loss,
        "effect": summary.effect,
        "effect_ci95": [summary.ci95_lower, summary.ci95_upper],
        "world_effects": summary.world_effects,
        "coverage_guard_pass": guard,
        "coverage_by_world": coverage_report,
        "test_target_count": len(target_map),
        "joined_step_count": len(scored),
    }
    (args.output / "report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    binding = {
        "raw_sha256": _sha256(args.raw),
        "manifest_sha256": _sha256(args.manifest),
        "inventory_sha256": _sha256(args.inventory),
        "preservation_commit": args.preservation_commit,
        "exact_package_commit": args.package_commit,
        "evidence_analyst_commit": EXPECTED_ANALYST,
        "formal_contract_git_blob": authority["formal_contract_git_blob"],
        "ni01_scorer_git_blob": authority["ni01_scorer_git_blob"],
        "source_binding": contract["source_binding"],
    }
    (args.output / "binding.json").write_text(
        json.dumps(binding, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser()
    sub = value.add_subparsers(dest="command", required=True)

    smoke = sub.add_parser("prestart-smoke")
    smoke.add_argument("--analyst-commit", required=True)
    smoke.set_defaults(func=prestart_smoke)

    acquire = sub.add_parser("acquire-raw")
    acquire.add_argument("--raw", required=True, type=Path)
    acquire.add_argument("--manifest", required=True, type=Path)
    acquire.add_argument("--inventory", required=True, type=Path)
    acquire.add_argument("--analyst-commit", required=True)
    acquire.add_argument("--package-commit", required=True)
    acquire.add_argument("--started-ref", required=True)
    acquire.set_defaults(func=acquire_raw)

    score = sub.add_parser("score-preserved")
    score.add_argument("--raw", required=True, type=Path)
    score.add_argument("--manifest", required=True, type=Path)
    score.add_argument("--inventory", required=True, type=Path)
    score.add_argument("--output", required=True, type=Path)
    score.add_argument("--analyst-commit", required=True)
    score.add_argument("--package-commit", required=True)
    score.add_argument("--preservation-commit", required=True)
    score.set_defaults(func=score_preserved)
    return value


def main() -> int:
    _disable_network()
    args = parser().parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
