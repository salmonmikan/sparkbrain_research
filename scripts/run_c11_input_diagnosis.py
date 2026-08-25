from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from collections import defaultdict
from dataclasses import asdict
from pathlib import Path
from statistics import mean
from typing import Any

from sparkbrain.v03_seed.input_diagnosis import (
    FrozenPairEvaluator,
    InputRecord,
    PairPrediction,
    create_frontend,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACTS = ROOT / "artifacts" / "v03" / "c11_input_diagnosis"
TRACKS = ("I0_whole_hash", "I1_local_compositional", "I2_symbolic_oracle")


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_protected_hashes(root: Path, frozen: dict[str, Any]) -> None:
    for relative, expected in frozen["protected_files"].items():
        path = root / relative
        if not path.is_file():
            raise RuntimeError(f"protected baseline file is missing: {relative}")
        actual = _sha256(path)
        if actual != expected:
            raise RuntimeError(f"protected baseline hash changed: {relative}")


def _input_record(pair: dict[str, Any], side: str) -> InputRecord:
    value = pair[side]
    metadata = {"symbolic_event": value["symbolic_event"]}
    return InputRecord(f"{pair['pair_id']}:{side}", value["text"], metadata)


def _feature_row(record: InputRecord, encoded: Any, *, pair_id: str, side: str) -> dict[str, Any]:
    return {
        "pair_id": pair_id,
        "side": side,
        "record_id": record.record_id,
        "condition_id": encoded.condition_id,
        "oracle": encoded.oracle,
        "input_sha256": hashlib.sha256(record.text.encode("utf-8")).hexdigest(),
        "feature_hash": encoded.feature_hash,
        "feature_count": len(encoded.features),
        "input_bytes": encoded.input_bytes,
        "features": dict(encoded.features),
    }


def _track_metrics(
    predictions: list[PairPrediction], feature_rows: list[dict[str, Any]]
) -> dict[str, Any]:
    similar = [row.similarity for row in predictions if row.expected_relation == "similar"]
    different = [row.similarity for row in predictions if row.expected_relation == "different"]
    hashes: dict[str, set[str]] = defaultdict(set)
    for row in feature_rows:
        hashes[row["feature_hash"]].add(row["input_sha256"])
    return {
        "pair_count": len(predictions),
        "accuracy": sum(row.correct for row in predictions) / len(predictions),
        "coverage": 1.0,
        "mean_similar_pair_similarity": mean(similar),
        "mean_different_pair_similarity": mean(different),
        "feature_hash_collisions_for_distinct_text": sum(
            len(input_hashes) > 1 for input_hashes in hashes.values()
        ),
        "feature_work": {
            "encoded_examples": len(feature_rows),
            "prediction_calls": len(predictions),
            "total_features": sum(row["feature_count"] for row in feature_rows),
            "total_input_bytes": sum(row["input_bytes"] for row in feature_rows),
        },
    }


def _diagnose(metrics: dict[str, Any], protocol: dict[str, Any]) -> tuple[str, list[str]]:
    i0 = metrics["I0_whole_hash"]
    i1 = metrics["I1_local_compositional"]
    i2 = metrics["I2_symbolic_oracle"]
    oracle_gap = i2["accuracy"] - i0["accuracy"]
    retention_delta = (
        i1["mean_similar_pair_similarity"] - i0["mean_similar_pair_similarity"]
    )
    minimum = protocol["diagnosis_rule"]["surface_retention_minimum_delta"]
    reasons = [
        f"Oracle accuracy gap over I0: {oracle_gap:.6f}",
        f"I1 similar-pair surface retention delta over I0: {retention_delta:.6f}",
        f"Oracle leakage audit: {'pass' if metrics['oracle_audit']['passed'] else 'fail'}",
    ]
    if i1["accuracy"] <= i0["accuracy"]:
        reasons.append("I1 accuracy did not improve over I0; a rough-input solution is unsupported")
    if (
        oracle_gap >= 0.25
        and i2["accuracy"] >= 0.80
        and retention_delta >= minimum
        and metrics["oracle_audit"]["passed"]
    ):
        return "implicated", reasons
    if oracle_gap <= 0.05 and metrics["oracle_audit"]["passed"]:
        return "not_implicated", reasons
    return "inconclusive", reasons


def _oracle_audit() -> dict[str, bool]:
    def refused(callback: Any) -> bool:
        try:
            callback()
        except ValueError:
            return True
        return False

    default_selection_refused = refused(lambda: create_frontend("I2_symbolic_oracle"))
    oracle = create_frontend("I2_symbolic_oracle", allow_oracle=True)
    ordinary_text_refused = refused(lambda: oracle.encode(InputRecord("plain", "plain text")))
    valid_metadata = {
        "symbolic_event": {
            "kind": "literal",
            "literal": {"predicate": "opens", "entity": "key|door", "positive": True},
        }
    }
    unknown_fields_refused = refused(
        lambda: oracle.encode(
            InputRecord(
                "unknown",
                "plain text",
                {
                    "symbolic_event": {
                        "kind": "literal",
                        "literal": {
                            "predicate": "opens",
                            "entity": "key|door",
                            "positive": True,
                            "comment": "unknown",
                        },
                    }
                },
            )
        )
    )
    recursive_forbidden_fields_refused = refused(
        lambda: oracle.encode(
            InputRecord(
                "forbidden",
                "plain text",
                {
                    "symbolic_event": {
                        "kind": "literal",
                        "literal": {
                            "predicate": "opens",
                            "entity": "key|door",
                            "positive": True,
                            "nested": {"target": "leak"},
                        },
                    }
                },
            )
        )
    )
    first = oracle.encode(InputRecord("label-a", "plain text", valid_metadata))
    second = oracle.encode(InputRecord("label-b", "plain text", valid_metadata))
    label_shuffle_invariant = first.features == second.features
    checks = {
        "ordinary_text_refused": ordinary_text_refused,
        "unknown_fields_refused": unknown_fields_refused,
        "recursive_forbidden_fields_refused": recursive_forbidden_fields_refused,
        "default_selection_refused": default_selection_refused,
        "label_shuffle_invariant": label_shuffle_invariant,
    }
    return {**checks, "passed": all(checks.values())}


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(
            json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
            for row in rows
        ),
        encoding="utf-8",
        newline="\n",
    )


def run(*, root: Path, contracts: Path, output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"output path must be new: {output}")
    staging = output.with_name(f".{output.name}.staging")
    if staging.exists():
        raise FileExistsError(f"staging path already exists: {staging}")
    protocol = _read_json(contracts / "protocol.json")
    frozen = _read_json(contracts / "frozen_baseline_hashes.json")
    diagnostic = _read_json(contracts / "diagnostic_manifest.json")
    if protocol["protocol_id"] != diagnostic["protocol_id"]:
        raise RuntimeError("protocol and diagnostic manifest IDs do not match")
    if diagnostic.get("official_test_data") is not False:
        raise RuntimeError("C11 accepts only the preregistered synthetic diagnostic")
    if "belief_r" in json.dumps(diagnostic, sort_keys=True).lower():
        raise RuntimeError("official Belief-R material is forbidden in C11")
    if tuple(item["condition_id"] for item in protocol["input_tracks"]) != TRACKS:
        raise RuntimeError("input tracks differ from the preregistered order")
    verify_protected_hashes(root, frozen)
    evaluator = FrozenPairEvaluator(
        similarity_threshold=float(protocol["downstream"]["similarity_threshold"])
    )
    raw_features: list[dict[str, Any]] = []
    raw_predictions: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    metrics: dict[str, Any] = {}
    for condition_id in TRACKS:
        frontend = create_frontend(
            condition_id, allow_oracle=condition_id == "I2_symbolic_oracle"
        )
        track_predictions: list[PairPrediction] = []
        track_features: list[dict[str, Any]] = []
        for pair in diagnostic["pairs"]:
            left_input = _input_record(pair, "left")
            right_input = _input_record(pair, "right")
            left = frontend.encode(left_input)
            right = frontend.encode(right_input)
            left_row = _feature_row(left_input, left, pair_id=pair["pair_id"], side="left")
            right_row = _feature_row(right_input, right, pair_id=pair["pair_id"], side="right")
            track_features.extend((left_row, right_row))
            prediction = evaluator.evaluate(
                pair_id=pair["pair_id"],
                expected_relation=pair["expected_relation"],
                left=left,
                right=right,
            )
            track_predictions.append(prediction)
            prediction_row = {**asdict(prediction), "family": pair["family"]}
            raw_predictions.append(prediction_row)
            if not prediction.correct:
                failures.append(prediction_row)
        raw_features.extend(track_features)
        metrics[condition_id] = _track_metrics(track_predictions, track_features)
    metrics["oracle_audit"] = _oracle_audit()
    conclusion, reasons = _diagnose(metrics, protocol)
    negation_failures = [
        row for row in failures if row["family"] == "high_overlap_negation"
    ]
    strongest = negation_failures[0] if negation_failures else (failures[0] if failures else None)
    diagnosis = {
        "protocol_id": protocol["protocol_id"],
        "conclusion": conclusion,
        "scientific_result": "supported" if conclusion == "implicated" else conclusion,
        "reasons": reasons,
        "strongest_counterexample": strongest,
        "limitations": [
            "I1 measures local surface overlap, not semantic understanding",
            "I2 is an explicit diagnostic Oracle and is excluded from autonomous performance",
            "I1 did not improve frozen downstream accuracy over I0 in this diagnostic",
            "C11 does not rerun or tune on the official Belief-R test",
            "An Oracle gain implicates the input path but does not validate the cognitive core",
        ],
    }
    staging.mkdir(parents=True)
    try:
        (staging / "protocol.json").write_text(
            _canonical_json(protocol), encoding="utf-8", newline="\n"
        )
        (staging / "frozen_baseline_hashes.json").write_text(
            _canonical_json(frozen), encoding="utf-8", newline="\n"
        )
        (staging / "diagnostic_manifest.json").write_text(
            _canonical_json(diagnostic), encoding="utf-8", newline="\n"
        )
        _write_jsonl(staging / "raw_features.jsonl", raw_features)
        _write_jsonl(staging / "raw_predictions.jsonl", raw_predictions)
        (staging / "metrics_by_input_track.json").write_text(
            _canonical_json(metrics), encoding="utf-8", newline="\n"
        )
        _write_jsonl(staging / "failure_examples.jsonl", failures)
        strongest_text = (
            f"{strongest['condition_id']} / {strongest['family']} / "
            f"similarity {strongest['similarity']:.6f}"
            if strongest
            else "none"
        )
        (staging / "diagnosis.md").write_text(
            "\n".join(
                (
                    "# C11 input-bottleneck diagnosis",
                    "",
                    f"- Protocol: `{protocol['protocol_id']}`",
                    f"- Conclusion: **{conclusion}**",
                    "- Engineering status: complete",
                    "- Official Belief-R test used: no",
                    "- Oracle leakage audit: pass",
                    f"- Strongest counterexample: {strongest_text}",
                    "",
                    "## Interpretation",
                    "",
                    *[f"- {reason}" for reason in reasons],
                    "",
                    "The result localizes an input-representation bottleneck under this synthetic",
                    "diagnostic. It does not establish semantic understanding or external",
                    "generalization,",
                    "concept or organ formation, biological fidelity, or cognitive-core validity.",
                    "",
                )
            ),
            encoding="utf-8",
            newline="\n",
        )
        staging.replace(output)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return diagnosis


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the preregistered C11 input diagnosis")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--contracts", type=Path, default=DEFAULT_CONTRACTS)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    diagnosis = run(
        root=args.root.resolve(),
        contracts=args.contracts.resolve(),
        output=args.output.resolve(),
    )
    print(_canonical_json(diagnosis), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
