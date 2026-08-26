from __future__ import annotations

import argparse
import hashlib
import json
import math
import multiprocessing
import os
import random
import shutil
import subprocess
import sys
import tempfile
import time
from collections.abc import Iterable, Mapping, Sequence
from multiprocessing.connection import Connection
from multiprocessing.process import BaseProcess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_RELATIVE = "artifacts/v03/c15_revision/protocol.json"
DEFAULT_PROTOCOL = ROOT / PROTOCOL_RELATIVE
BASE_PROTOCOL_COMMIT = "cd241a898cc20b6b5696baea14147051ef126ad3"
EXPECTED_FILES = {
    "calibration_by_input_track.json",
    "confusion_matrices.json",
    "loss_ablation_metrics.json",
    "objective_config.json",
    "pareto_frontier.json",
    "per_transition_predictions.jsonl",
    "protocol.json",
    "report.md",
}


def _canonical(value: object) -> str:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _write_json(path: Path, value: object) -> None:
    path.write_text(_canonical(value) + "\n", encoding="utf-8", newline="\n")


def _write_jsonl(path: Path, rows: Iterable[Mapping[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(_canonical(row) + "\n")


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-c", f"safe.directory={root.as_posix()}", *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _git_bytes(root: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", "-c", f"safe.directory={root.as_posix()}", *args],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return result.stdout


def _require_exact_keys(value: object, fields: Sequence[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != set(fields):
        raise RuntimeError(f"{label} has missing or unknown keys")
    return value


def _require_list(value: object, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise RuntimeError(f"{label} must be a list")
    return value


def _require_int(value: object, label: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise RuntimeError(f"{label} must be an integer >= {minimum}")
    return value


def _require_number(value: object, label: str, *, nullable: bool = False) -> float | None:
    if value is None and nullable:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise RuntimeError(f"{label} must be a finite number")
    return float(value)


def _require_probability(value: object, label: str, *, nullable: bool = False) -> float | None:
    number = _require_number(value, label, nullable=nullable)
    if number is not None and not 0.0 <= number <= 1.0:
        raise RuntimeError(f"{label} must be in [0, 1]")
    return number


def _require_hash(value: object, label: str, *, length: int = 64) -> str:
    if (
        not isinstance(value, str)
        or len(value) != length
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise RuntimeError(f"{label} must be a lowercase hexadecimal hash of length {length}")
    return value


def _require_finite_json(value: object, label: str) -> None:
    try:
        json.dumps(value, allow_nan=False, ensure_ascii=False)
    except (TypeError, ValueError) as exc:
        raise RuntimeError(f"{label} must contain only finite JSON data") from exc


def _require_sorted_unique_strings(value: object, label: str) -> list[str]:
    rows = _require_list(value, label)
    if any(not isinstance(item, str) or not item for item in rows):
        raise RuntimeError(f"{label} must contain non-empty strings")
    if rows != sorted(set(rows)):
        raise RuntimeError(f"{label} must be sorted and unique")
    return rows


def _validate_failed_seeds(
    value: object, protocol: dict[str, Any], label: str = "failed_seeds"
) -> list[dict[str, Any]]:
    rows = _require_list(value, label)
    fields = protocol["failure_contract"]["failed_seed_fields"]
    phase_order = list(protocol["failure_contract"]["phase_order"])
    allowed_seeds = set(protocol["seeds"]["model"])
    conditions = set(protocol["conditions"]["order"])
    seen: set[int] = set()
    for index, raw in enumerate(rows):
        row = _require_exact_keys(raw, fields, f"{label}[{index}]")
        seed = _require_int(row["model_seed"], f"{label}[{index}].model_seed")
        if seed not in allowed_seeds or seed in seen:
            raise RuntimeError(f"{label} contains an invalid or duplicate model seed")
        seen.add(seed)
        if row["phase"] not in phase_order or row["condition_id"] not in conditions:
            raise RuntimeError(f"{label}[{index}] phase/condition is invalid")
        if not isinstance(row["error_type"], str) or not row["error_type"]:
            raise RuntimeError(f"{label}[{index}].error_type must be non-empty")
        _require_hash(row["error_hash"], f"{label}[{index}].error_hash")
        expected_hash = _sha256_bytes(
            _canonical([row["phase"], row["condition_id"], row["error_type"]]).encode()
        )
        if row["error_hash"] != expected_hash:
            raise RuntimeError(f"{label}[{index}].error_hash is invalid")
    if [row["model_seed"] for row in rows] != sorted(seen):
        raise RuntimeError(f"{label} order is not canonical")
    return rows


def _successful_model_seeds(
    protocol: dict[str, Any], failed_seeds: Sequence[Mapping[str, object]]
) -> list[int]:
    failed = {int(row["model_seed"]) for row in failed_seeds}
    return [int(seed) for seed in protocol["seeds"]["model"] if int(seed) not in failed]


def _failure_scientific_support(protocol: dict[str, Any]) -> dict[str, object]:
    thresholds = protocol["acceptance"]["scientific_support_gates"]
    maxima = {
        "distractor_change": thresholds["distractor_prediction_change_rate_max"],
        "same_id_change": thresholds["same_id_duplicate_prediction_change_rate_max"],
        "correlated_copy_change": thresholds[
            "correlated_copy_prediction_change_rate_max"
        ],
    }
    margins = thresholds["weighted_ce_noninferiority_margins"]
    margin_specs = {
        "unnecessary_revision_rate": (
            margins["unnecessary_revision_rate_max_increase"],
            "max_increase",
        ),
        "missed_revision_rate": (margins["missed_revision_rate_max_increase"], "max_increase"),
        "recovery_rate": (margins["recovery_rate_max_decrease"], "max_decrease"),
        "no_ignition_f1": (margins["no_ignition_f1_max_decrease"], "max_decrease"),
        "ece": (margins["ece_max_increase"], "max_increase"),
    }
    comparisons = protocol["determinism"]["bootstrap_algorithm"]["comparison_order"]
    return {
        "status": protocol["failure_contract"]["failed_scientific_status"],
        "variant_gates": {
            name: {
                "changed_pairs": 0,
                "denominator": 0,
                "rate": None,
                "maximum": maximum,
                "passed": False,
            }
            for name, maximum in maxima.items()
        },
        "residual_gate": {
            "full_recovery_rate": None,
            "no_residual_recovery_rate": None,
            "passed": False,
        },
        "weighted_ce_noninferiority": {
            name: {
                "effect_full_minus_weighted_ce": None,
                "margin": margin,
                "direction": direction,
                "passed": False,
            }
            for name, (margin, direction) in margin_specs.items()
        },
        "strict_improvement": {
            "effects": {name: None for name in margin_specs},
            "minimum": thresholds[
                "weighted_ce_strict_improvement_required_on_at_least_one_dimension"
            ],
            "passed": False,
        },
        "all_gates_passed": False,
        "bootstrap_intervals": {
            comparison: {
                "effect": None,
                "lower": None,
                "upper": None,
                "resamples": protocol["determinism"]["bootstrap_resamples"],
                "bootstrap_seed": protocol["determinism"]["bootstrap_seed"],
                "defined_resamples": None,
                "undefined_resamples": None,
            }
            for comparison in comparisons
        },
    }


def _validate_protocol_amendment(
    current_protocol: dict[str, Any], base_protocol: dict[str, Any]
) -> None:
    normalized = json.loads(_canonical(current_protocol))
    dependencies = normalized["dependencies"]
    for name in ("c15_protocol_base_commit", "c15_protocol_base_sha256"):
        dependencies.pop(name)
    dependencies["c15_source_pin"] = base_protocol["dependencies"]["c15_source_pin"]
    dependencies["runner_execution_allowed"] = base_protocol["dependencies"][
        "runner_execution_allowed"
    ]
    if normalized != base_protocol:
        raise RuntimeError("C15 protocol amendment changes fields beyond the authorized pin")


def _reject_belief_r_argument(*paths: Path) -> None:
    for path in paths:
        normalized = path.as_posix().casefold().replace("-", "_")
        if "belief_r" in normalized or "beliefr" in normalized:
            raise RuntimeError("official Belief-R paths are forbidden for C15")


def _validate_source_scope(
    *, root: Path, protocol: dict[str, Any], source_commit: str, base_commit: str
) -> None:
    control = protocol["source_control"]
    authorized = tuple(str(path) for path in control["c15_authorized_paths_before_pin"])
    changed = tuple(
        line
        for line in _git(root, "diff", "--name-only", base_commit, source_commit).splitlines()
        if line
    )
    if not changed:
        raise RuntimeError("C15 source diff must be non-empty")
    unexpected = sorted(set(changed) - set(authorized))
    if unexpected:
        raise RuntimeError(f"C15 source diff contains unauthorized paths: {unexpected}")
    denied = tuple(str(path).rstrip("/") for path in control["v02_deny_paths"])
    if any(
        path == prefix or path.startswith(prefix + "/") for path in changed for prefix in denied
    ):
        raise RuntimeError("C15 source diff changes a frozen v0.2 path")

    _git(root, "merge-base", "--is-ancestor", source_commit, "HEAD")
    after_pin = tuple(
        line
        for line in _git(root, "diff", "--name-only", source_commit, "HEAD").splitlines()
        if line
    )
    permitted_after_pin = {
        PROTOCOL_RELATIVE,
        "docs/DECISION_LOG.md",
        "docs/EXPERIMENT_PROTOCOL.md",
        "docs/PROJECT_STATUS.md",
        "docs/RESULTS_LEDGER.md",
    }
    permitted_after_pin.update(
        f"artifacts/v03/c15_revision/{name}" for name in EXPECTED_FILES - {"protocol.json"}
    )
    changed_authorized = sorted(set(after_pin) & set(authorized))
    if changed_authorized:
        raise RuntimeError(f"C15 source changed after its pin: {changed_authorized}")
    unexpected_after_pin = sorted(set(after_pin) - permitted_after_pin)
    if unexpected_after_pin:
        raise RuntimeError(
            f"C15 post-pin history contains unauthorized paths: {unexpected_after_pin}"
        )

    for relative in authorized:
        path = root / relative
        try:
            pinned_bytes = _git_bytes(root, "show", f"{source_commit}:{relative}")
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(f"C15 pinned source path is missing: {relative}") from exc
        if not path.is_file() or path.read_bytes() != pinned_bytes:
            raise RuntimeError(f"C15 working source differs from its pin: {relative}")

    c14_source = str(protocol["dependencies"]["c14_source"])
    c14_paths = tuple(str(path) for path in control["c14_protected_source_paths"])
    c14_changed = _git(root, "diff", "--name-only", c14_source, "HEAD", "--", *c14_paths)
    if c14_changed:
        raise RuntimeError("C14 protected source differs from the accepted source pin")

    for prefix in protocol["release_freeze"]["deny_changed_prefixes"]:
        frozen_changed = _git(root, "diff", "--name-only", base_commit, "HEAD", "--", str(prefix))
        if frozen_changed:
            raise RuntimeError(f"C15 changes frozen release/schema prefix: {prefix}")


def _validate_protected_hashes(root: Path, protocol: dict[str, Any]) -> dict[str, str]:
    protected = dict(protocol["protected_files"])
    if len(protected) != 28:
        raise RuntimeError("C15 protected inventory must contain exactly 28 files")
    actual: dict[str, str] = {}
    for relative, expected in protected.items():
        path = root / relative
        if not path.is_file():
            raise RuntimeError(f"protected file is missing: {relative}")
        digest = _sha256_file(path)
        if digest != expected:
            raise RuntimeError(f"protected file hash changed: {relative}")
        actual[relative] = digest
    return actual


def _validate_fixture_hashes(protocol: dict[str, Any]) -> dict[str, dict[str, str]]:
    from sparkbrain.v03_seed.revision_worlds import (
        full_fixture_sha256,
        split_manifest_sha256,
    )

    expected_full = protocol["seeds"]["full_fixture_sha256"]
    expected_manifest = protocol["seeds"]["split_manifest_sha256"]
    actual = {"full_fixture_sha256": {}, "split_manifest_sha256": {}}
    for split in ("train", "dev", "test"):
        full_hash = full_fixture_sha256(split)
        manifest_hash = split_manifest_sha256(split)
        if full_hash != expected_full[split]:
            raise RuntimeError(f"C15 full fixture hash mismatch for {split}")
        if manifest_hash != expected_manifest[split]:
            raise RuntimeError(f"C15 split manifest hash mismatch for {split}")
        actual["full_fixture_sha256"][split] = full_hash
        actual["split_manifest_sha256"][split] = manifest_hash
    return actual


def _preflight(
    *, root: Path, protocol_path: Path, output: Path, source_commit: str
) -> tuple[dict[str, Any], bytes, dict[str, str], dict[str, dict[str, str]]]:
    expected_protocol_path = (root / PROTOCOL_RELATIVE).resolve()
    if protocol_path.resolve() != expected_protocol_path:
        raise RuntimeError("C15 protocol must use the repository-fixed canonical path")
    _reject_belief_r_argument(root, protocol_path, output)
    protocol_bytes = protocol_path.read_bytes()
    protocol = json.loads(protocol_bytes.decode("utf-8"))
    dependencies = protocol["dependencies"]
    if dependencies.get("runner_execution_allowed") is not True:
        raise RuntimeError("C15 runner execution is disabled until the source-pin amendment")
    if dependencies.get("c15_source_pin") != source_commit:
        raise RuntimeError("C15 source commit does not match the preregistered pin")

    head_protocol = _git_bytes(root, "show", f"HEAD:{PROTOCOL_RELATIVE}")
    if protocol_bytes != head_protocol:
        raise RuntimeError("working C15 protocol bytes differ from the HEAD blob")
    base_commit = str(dependencies["c15_protocol_base_commit"])
    base_sha256 = str(dependencies["c15_protocol_base_sha256"])
    if base_commit != BASE_PROTOCOL_COMMIT:
        raise RuntimeError("C15 protocol base commit is not the frozen preregistration commit")
    _git(root, "merge-base", "--is-ancestor", base_commit, "HEAD")
    base_bytes = _git_bytes(root, "show", f"{base_commit}:{PROTOCOL_RELATIVE}")
    if _sha256_bytes(base_bytes) != base_sha256:
        raise RuntimeError("C15 preregistration base protocol blob hash mismatch")
    base_protocol = json.loads(base_bytes.decode("utf-8"))
    _validate_protocol_amendment(protocol, base_protocol)

    for name in (
        "c12_merge",
        "c13_merge",
        "c13_source",
        "c14_artifact_commit",
        "c14_merge",
        "c14_source",
        "c14_status_ledger_correction",
    ):
        commit = str(dependencies[name])
        _git(root, "cat-file", "-e", f"{commit}^{{commit}}")
        _git(root, "merge-base", "--is-ancestor", commit, "HEAD")
    _git(root, "cat-file", "-e", f"{source_commit}^{{commit}}")
    _validate_source_scope(
        root=root,
        protocol=protocol,
        source_commit=source_commit,
        base_commit=base_commit,
    )
    protected = _validate_protected_hashes(root, protocol)
    fixture_hashes = _validate_fixture_hashes(protocol)
    return protocol, protocol_bytes, protected, fixture_hashes


def _safe_ratio(numerator: int | float, denominator: int) -> float | None:
    return float(numerator) / denominator if denominator else None


def _mean_or_none(values: Sequence[float]) -> float | None:
    return sum(values) / len(values) if values else None


def _ovr_counts(rows: Sequence[Mapping[str, object]], label: str) -> dict[str, int]:
    tn = fp = fn = tp = 0
    for row in rows:
        target = row["transition_target"] == label
        predicted = row["predicted_transition"] == label
        if target and predicted:
            tp += 1
        elif target:
            fn += 1
        elif predicted:
            fp += 1
        else:
            tn += 1
    return {"fn": fn, "fp": fp, "tn": tn, "tp": tp}


def _confusion_row(
    rows: Sequence[Mapping[str, object]],
    *,
    protocol: dict[str, Any],
    identity: Mapping[str, object],
) -> dict[str, object]:
    labels = list(protocol["transition_contract"]["labels"])
    confusion = {target: {predicted: 0 for predicted in labels} for target in labels}
    for row in rows:
        confusion[str(row["transition_target"])][str(row["predicted_transition"])] += 1

    positive = set(protocol["metrics"]["revision_positive_labels"])
    revision_tp = sum(
        row["transition_target"] in positive and row["predicted_transition"] in positive
        for row in rows
    )
    revision_fp = sum(
        row["transition_target"] not in positive and row["predicted_transition"] in positive
        for row in rows
    )
    revision_fn = sum(
        row["transition_target"] in positive and row["predicted_transition"] not in positive
        for row in rows
    )
    maintain = [row for row in rows if row["transition_target"] == "maintain"]
    revisions = [row for row in rows if row["transition_target"] in positive]
    unnecessary = sum(row["predicted_transition"] in positive for row in maintain)
    missed = sum(row["predicted_transition"] not in positive for row in revisions)
    recovery = [row for row in rows if row["transition_target"] == "recover"]
    successes = [
        row
        for row in recovery
        if row["predicted_belief"] == row["truth_belief"]
        and row["predicted_transition"] == "recover"
        and row["checkpoint_restored"] is False
    ]
    observed_latency = [float(row["recovery_latency_steps"]) for row in successes]
    censored_latency = [
        float(row["recovery_latency_steps"]) if row in successes else 3.0 for row in recovery
    ]
    target_no_ignition = [row["transition_target"] == "insufficient_information" for row in rows]
    predicted_no_ignition = [not bool(row["ignited"]) for row in rows]
    no_tp = sum(
        target and predicted
        for target, predicted in zip(
            target_no_ignition, predicted_no_ignition, strict=True
        )
    )
    no_fp = sum(
        not target and predicted
        for target, predicted in zip(
            target_no_ignition, predicted_no_ignition, strict=True
        )
    )
    no_fn = sum(
        target and not predicted
        for target, predicted in zip(
            target_no_ignition, predicted_no_ignition, strict=True
        )
    )
    no_precision = _safe_ratio(no_tp, no_tp + no_fp)
    no_recall = _safe_ratio(no_tp, no_tp + no_fn)
    no_f1 = (
        2.0 * no_precision * no_recall / (no_precision + no_recall)
        if no_precision is not None and no_recall is not None and no_precision + no_recall
        else None
    )
    decided = sum(bool(row["ignited"]) for row in rows)
    correct = sum(row["predicted_belief"] == row["truth_belief"] for row in rows)
    return {
        **identity,
        "row_count": len(rows),
        "transition_confusion": confusion,
        "maintain_ovr": _ovr_counts(rows, "maintain"),
        "update_ovr": _ovr_counts(rows, "update"),
        "unnecessary_revision_count": unnecessary,
        "unnecessary_revision_denominator": len(maintain),
        "unnecessary_revision_rate": _safe_ratio(unnecessary, len(maintain)),
        "missed_revision_count": missed,
        "missed_revision_denominator": len(revisions),
        "missed_revision_rate": _safe_ratio(missed, len(revisions)),
        "revision_tp": revision_tp,
        "revision_fp": revision_fp,
        "revision_fn": revision_fn,
        "revision_precision": _safe_ratio(revision_tp, revision_tp + revision_fp),
        "revision_recall": _safe_ratio(revision_tp, revision_tp + revision_fn),
        "recovery_opportunities": len(recovery),
        "recovery_successes": len(successes),
        "recovery_rate": _safe_ratio(len(successes), len(recovery)),
        "recovery_latency_observed_mean": _mean_or_none(observed_latency),
        "recovery_latency_censored_mean": _mean_or_none(censored_latency),
        "recovery_censored": len(recovery) - len(successes),
        "no_ignition_tp": no_tp,
        "no_ignition_fp": no_fp,
        "no_ignition_fn": no_fn,
        "no_ignition_precision": no_precision,
        "no_ignition_recall": no_recall,
        "no_ignition_f1": no_f1,
        "accuracy": _safe_ratio(correct, len(rows)),
        "coverage": _safe_ratio(decided, len(rows)),
    }


def _ece_bins(rows: Sequence[Mapping[str, object]]) -> tuple[list[dict[str, object]], float | None]:
    decided = [row for row in rows if row["ignited"]]
    bins: list[dict[str, object]] = []
    weighted = 0.0
    for index in range(10):
        lower = index / 10.0
        upper = (index + 1) / 10.0
        include_upper = index == 9
        selected: list[tuple[float, bool]] = []
        for row in decided:
            probabilities = row["belief_probabilities"]
            assert isinstance(probabilities, Mapping)
            confidence = max(float(value) for value in probabilities.values())
            if lower <= confidence < upper or (include_upper and confidence == upper):
                selected.append((confidence, row["predicted_belief"] == row["truth_belief"]))
        mean_confidence = _mean_or_none([item[0] for item in selected])
        accuracy = _mean_or_none([float(item[1]) for item in selected])
        bins.append(
            {
                "lower_inclusive": lower,
                "upper_exclusive": upper,
                "include_upper": include_upper,
                "count": len(selected),
                "mean_confidence": mean_confidence,
                "accuracy": accuracy,
            }
        )
        if selected:
            assert mean_confidence is not None and accuracy is not None
            weighted += len(selected) * abs(accuracy - mean_confidence)
    return bins, _safe_ratio(weighted, len(decided))


def _calibration_row(
    rows: Sequence[Mapping[str, object]], *, identity: Mapping[str, object]
) -> dict[str, object]:
    multiclass_brier = 0.0
    nll = 0.0
    abstention_brier = 0.0
    for row in rows:
        p_abstain = float(row["no_ignition_probability"])
        belief_probabilities = row["belief_probabilities"]
        assert isinstance(belief_probabilities, Mapping)
        probabilities = {
            label: (1.0 - p_abstain) * float(belief_probabilities[label])
            for label in ("alpha", "beta", "gamma")
        }
        probabilities["NO_IGNITION"] = p_abstain
        target = (
            "NO_IGNITION"
            if row["transition_target"] == "insufficient_information"
            else str(row["truth_belief"])
        )
        multiclass_brier += sum(
            (probability - float(label == target)) ** 2
            for label, probability in probabilities.items()
        )
        nll += -math.log(max(probabilities[target], 1e-12))
        abstention_brier += (p_abstain - float(target == "NO_IGNITION")) ** 2
    bins, ece = _ece_bins(rows)
    decided = sum(bool(row["ignited"]) for row in rows)
    return {
        **identity,
        "row_count": len(rows),
        "decided_count": decided,
        "coverage": _safe_ratio(decided, len(rows)),
        "multiclass_brier": _safe_ratio(multiclass_brier, len(rows)),
        "nll": _safe_ratio(nll, len(rows)),
        "abstention_brier": _safe_ratio(abstention_brier, len(rows)),
        "ece": ece,
        "ece_bins": bins,
    }


def _raw_strata(
    rows: Sequence[Mapping[str, object]], *, include_seed: bool
) -> list[tuple[dict[str, object], list[Mapping[str, object]]]]:
    keys = ["split", "condition_id", "input_track", "entity_condition"]
    if include_seed:
        keys.append("model_seed")
    grouped: dict[tuple[object, ...], list[Mapping[str, object]]] = {}
    for row in rows:
        identity = tuple(row[key] for key in keys)
        grouped.setdefault(identity, []).append(row)
    return [
        (dict(zip(keys, identity, strict=True)), grouped[identity])
        for identity in sorted(grouped)
    ]


def _confusion_artifact(
    rows: list[dict[str, object]],
    *,
    protocol: dict[str, Any],
    source_commit: str,
    failed_seeds: Sequence[Mapping[str, object]] = (),
) -> dict[str, object]:
    seed_rows = [
        _confusion_row(selected, protocol=protocol, identity=identity)
        for identity, selected in _raw_strata(rows, include_seed=True)
    ]
    aggregate_rows = [
        _confusion_row(selected, protocol=protocol, identity=identity)
        for identity, selected in _raw_strata(rows, include_seed=False)
    ]
    return {
        "schema_version": "0.3",
        "protocol_id": protocol["protocol_id"],
        "source_commit": source_commit,
        "seed_rows": seed_rows,
        "aggregate_rows": aggregate_rows,
        "failed_seeds": list(failed_seeds),
    }


def _calibration_artifact(
    rows: list[dict[str, object]],
    *,
    protocol: dict[str, Any],
    source_commit: str,
    failed_seeds: Sequence[Mapping[str, object]] = (),
) -> dict[str, object]:
    return {
        "schema_version": "0.3",
        "protocol_id": protocol["protocol_id"],
        "source_commit": source_commit,
        "seed_rows": [
            _calibration_row(selected, identity=identity)
            for identity, selected in _raw_strata(rows, include_seed=True)
        ],
        "aggregate_rows": [
            _calibration_row(selected, identity=identity)
            for identity, selected in _raw_strata(rows, include_seed=False)
        ],
        "failed_seeds": list(failed_seeds),
    }


def _primary_base_rows(
    rows: Sequence[Mapping[str, object]], condition_id: str
) -> list[Mapping[str, object]]:
    return [
        row
        for row in rows
        if row["split"] == "test"
        and row["condition_id"] == condition_id
        and row["input_track"] == "I1_local_compositional"
        and row["entity_condition"] == "E1_oracle_entity"
        and row["variant_id"] == "base"
    ]


def _pareto_metrics(
    rows: Sequence[Mapping[str, object]], *, protocol: dict[str, Any]
) -> dict[str, float | None]:
    confusion = _confusion_row(rows, protocol=protocol, identity={})
    calibration = _calibration_row(rows, identity={})
    return {
        "unnecessary_revision_rate": confusion["unnecessary_revision_rate"],
        "missed_revision_rate": confusion["missed_revision_rate"],
        "recovery_latency_censored_mean": confusion["recovery_latency_censored_mean"],
        "ece": calibration["ece"],
        "recovery_rate": confusion["recovery_rate"],
        "no_ignition_f1": confusion["no_ignition_f1"],
    }


def _dominates(
    left: Mapping[str, float | None],
    right: Mapping[str, float | None],
    dimensions: Sequence[Mapping[str, str]],
) -> bool:
    epsilon = 1e-12
    if any(left[row["metric"]] is None or right[row["metric"]] is None for row in dimensions):
        return False
    no_worse = True
    strictly_better = False
    for dimension in dimensions:
        metric = dimension["metric"]
        left_value = float(left[metric])  # type: ignore[arg-type]
        right_value = float(right[metric])  # type: ignore[arg-type]
        if dimension["direction"] == "minimize":
            no_worse &= left_value <= right_value + epsilon
            strictly_better |= left_value < right_value - epsilon
        else:
            no_worse &= left_value + epsilon >= right_value
            strictly_better |= left_value > right_value + epsilon
    return no_worse and strictly_better


def _variant_change(
    rows: Sequence[Mapping[str, object]], variant_id: str
) -> tuple[int, int, float]:
    selected = [
        row
        for row in rows
        if row["split"] == "test"
        and row["condition_id"] == "full_separated"
        and row["input_track"] == "I1_local_compositional"
        and row["entity_condition"] == "E1_oracle_entity"
        and row["variant_id"] in {"base", variant_id}
    ]
    by_key: dict[tuple[object, object, object], list[Mapping[str, object]]] = {}
    for row in selected:
        by_key.setdefault((row["model_seed"], row["episode_id"], row["variant_id"]), []).append(row)
    pairs: list[tuple[object, object, int]] = []
    for seed, episode_id in sorted({(row["model_seed"], row["episode_id"]) for row in selected}):
        base_count = len(by_key[(seed, episode_id, "base")])
        variant_count = len(by_key[(seed, episode_id, variant_id)])
        if base_count != variant_count:
            raise RuntimeError("variant pairing cardinality mismatch")
        pairs.extend((seed, episode_id, occurrence) for occurrence in range(base_count))
    changed = 0
    for seed, episode_id, occurrence in pairs:
        base = by_key[(seed, episode_id, "base")][occurrence]
        variant = by_key[(seed, episode_id, variant_id)][occurrence]
        left = (base["predicted_belief"], base["predicted_transition"], base["ignited"])
        right = (
            variant["predicted_belief"],
            variant["predicted_transition"],
            variant["ignited"],
        )
        changed += int(left != right)
    return changed, len(pairs), changed / len(pairs)


def _nullable_difference(left: float | None, right: float | None) -> float | None:
    return None if left is None or right is None else float(left) - float(right)


def _comparison_effect(
    comparison: str,
    rows: Sequence[Mapping[str, object]],
    *,
    protocol: dict[str, Any],
) -> float | None:
    if comparison.endswith("_change"):
        variant = {
            "distractor_change": "irrelevant_distractor",
            "same_id_change": "same_id_duplicate",
            "correlated_copy_change": "correlated_copy",
        }[comparison]
        return _variant_change(rows, variant)[2]
    full = _pareto_metrics(_primary_base_rows(rows, "full_separated"), protocol=protocol)
    if comparison == "recovery_full_minus_no_residual":
        other = _pareto_metrics(_primary_base_rows(rows, "no_residual"), protocol=protocol)
        return _nullable_difference(full["recovery_rate"], other["recovery_rate"])
    other = _pareto_metrics(_primary_base_rows(rows, "one_weighted_ce"), protocol=protocol)
    metric = {
        "full_minus_weighted_ce_unnecessary": "unnecessary_revision_rate",
        "full_minus_weighted_ce_missed": "missed_revision_rate",
        "full_minus_weighted_ce_recovery": "recovery_rate",
        "full_minus_weighted_ce_no_ignition_f1": "no_ignition_f1",
        "full_minus_weighted_ce_ece": "ece",
    }[comparison]
    return _nullable_difference(full[metric], other[metric])


def _percentile(values: Sequence[float], probability: float) -> float:
    ordered = sorted(values)
    rank = (len(ordered) - 1) * probability
    lower = math.floor(rank)
    upper = math.ceil(rank)
    if lower == upper:
        return ordered[lower]
    fraction = rank - lower
    return ordered[lower] + fraction * (ordered[upper] - ordered[lower])


def _bootstrap_intervals(
    rows: list[dict[str, object]], *, protocol: dict[str, Any]
) -> dict[str, dict[str, object]]:
    algorithm = protocol["determinism"]["bootstrap_algorithm"]
    comparisons = list(algorithm["comparison_order"])
    seeds = [int(seed) for seed in protocol["seeds"]["model"]]
    worlds = list(protocol["splits"]["world_order"])
    eligible = [
        row
        for row in rows
        if row["split"] == "test"
        and row["input_track"] == "I1_local_compositional"
        and row["entity_condition"] == "E1_oracle_entity"
    ]
    episode_order: dict[tuple[int, str], list[str]] = {}
    for seed in seeds:
        for world in worlds:
            episode_order[(seed, world)] = sorted(
                {
                    str(row["episode_id"])
                    for row in eligible
                    if row["model_seed"] == seed and row["world"] == world
                },
                key=lambda episode_id: next(
                    int(row["episode_seed"])
                    for row in eligible
                    if row["model_seed"] == seed and row["episode_id"] == episode_id
                ),
            )
            if len(episode_order[(seed, world)]) != 8:
                raise RuntimeError("C15 bootstrap requires eight test fixtures per seed/world")
    by_block: dict[tuple[int, str], list[dict[str, object]]] = {}
    for row in eligible:
        by_block.setdefault((int(row["model_seed"]), str(row["episode_id"])), []).append(row)

    rng = random.Random(int(protocol["determinism"]["bootstrap_seed"]))
    resamples = int(protocol["determinism"]["bootstrap_resamples"])
    result: dict[str, dict[str, object]] = {}
    for comparison in comparisons:
        effects: list[float] = []
        for _ in range(resamples):
            sampled: list[dict[str, object]] = []
            for _seed_position in seeds:
                seed = seeds[rng.randrange(len(seeds))]
                for world in worlds:
                    ordered = episode_order[(seed, world)]
                    for _fixture_index in range(8):
                        episode_id = ordered[rng.randrange(8)]
                        sampled.extend(by_block[(seed, episode_id)])
            effect = _comparison_effect(comparison, sampled, protocol=protocol)
            if effect is not None:
                effects.append(effect)
        observed = _comparison_effect(comparison, eligible, protocol=protocol)
        undefined = resamples - len(effects)
        # Undefined draws still consume their complete paired sample; no conditional CI.
        bounds_defined = undefined == 0 and observed is not None
        result[comparison] = {
            "effect": observed,
            "lower": _percentile(effects, 0.025) if bounds_defined else None,
            "upper": _percentile(effects, 0.975) if bounds_defined else None,
            "resamples": resamples,
            "bootstrap_seed": int(protocol["determinism"]["bootstrap_seed"]),
            "defined_resamples": len(effects),
            "undefined_resamples": undefined,
        }
    return result


def _scientific_support(
    rows: list[dict[str, object]], *, protocol: dict[str, Any]
) -> dict[str, object]:
    thresholds = protocol["acceptance"]["scientific_support_gates"]
    variant_specs = {
        "distractor_change": (
            "irrelevant_distractor",
            float(thresholds["distractor_prediction_change_rate_max"]),
        ),
        "same_id_change": (
            "same_id_duplicate",
            float(thresholds["same_id_duplicate_prediction_change_rate_max"]),
        ),
        "correlated_copy_change": (
            "correlated_copy",
            float(thresholds["correlated_copy_prediction_change_rate_max"]),
        ),
    }
    variant_gates: dict[str, dict[str, object]] = {}
    for name, (variant, maximum) in variant_specs.items():
        changed, denominator, rate = _variant_change(rows, variant)
        variant_gates[name] = {
            "changed_pairs": changed,
            "denominator": denominator,
            "rate": rate,
            "maximum": maximum,
            "passed": rate <= maximum,
        }
    full = _pareto_metrics(_primary_base_rows(rows, "full_separated"), protocol=protocol)
    no_residual = _pareto_metrics(_primary_base_rows(rows, "no_residual"), protocol=protocol)
    weighted = _pareto_metrics(_primary_base_rows(rows, "one_weighted_ce"), protocol=protocol)
    residual_gate = {
        "full_recovery_rate": full["recovery_rate"],
        "no_residual_recovery_rate": no_residual["recovery_rate"],
        "passed": full["recovery_rate"] is not None
        and no_residual["recovery_rate"] is not None
        and full["recovery_rate"] > no_residual["recovery_rate"],
    }
    margins = thresholds["weighted_ce_noninferiority_margins"]
    checks = {
        "unnecessary_revision_rate": (
            _nullable_difference(
                full["unnecessary_revision_rate"], weighted["unnecessary_revision_rate"]
            ),
            float(margins["unnecessary_revision_rate_max_increase"]),
            "max_increase",
        ),
        "missed_revision_rate": (
            _nullable_difference(full["missed_revision_rate"], weighted["missed_revision_rate"]),
            float(margins["missed_revision_rate_max_increase"]),
            "max_increase",
        ),
        "recovery_rate": (
            _nullable_difference(full["recovery_rate"], weighted["recovery_rate"]),
            float(margins["recovery_rate_max_decrease"]),
            "max_decrease",
        ),
        "no_ignition_f1": (
            _nullable_difference(full["no_ignition_f1"], weighted["no_ignition_f1"]),
            float(margins["no_ignition_f1_max_decrease"]),
            "max_decrease",
        ),
        "ece": (
            _nullable_difference(full["ece"], weighted["ece"]),
            float(margins["ece_max_increase"]),
            "max_increase",
        ),
    }
    noninferiority = {
        name: {
            "effect_full_minus_weighted_ce": effect,
            "margin": margin,
            "direction": direction,
            "passed": effect is not None
            and (effect <= margin if direction == "max_increase" else effect >= -margin),
        }
        for name, (effect, margin, direction) in checks.items()
    }
    improvements = {
        "unnecessary_revision_rate": _nullable_difference(
            weighted["unnecessary_revision_rate"], full["unnecessary_revision_rate"]
        ),
        "missed_revision_rate": _nullable_difference(
            weighted["missed_revision_rate"], full["missed_revision_rate"]
        ),
        "recovery_rate": _nullable_difference(full["recovery_rate"], weighted["recovery_rate"]),
        "no_ignition_f1": _nullable_difference(full["no_ignition_f1"], weighted["no_ignition_f1"]),
        "ece": _nullable_difference(weighted["ece"], full["ece"]),
    }
    required = float(
        thresholds["weighted_ce_strict_improvement_required_on_at_least_one_dimension"]
    )
    strict_improvement = {
        "effects": improvements,
        "minimum": required,
        "passed": any(value is not None and value >= required for value in improvements.values()),
    }
    intervals = _bootstrap_intervals(rows, protocol=protocol)
    all_passed = (
        all(row["passed"] for row in variant_gates.values())
        and residual_gate["passed"]
        and all(row["passed"] for row in noninferiority.values())
        and strict_improvement["passed"]
    )
    return {
        "status": "supported" if all_passed else "not_supported",
        "variant_gates": variant_gates,
        "residual_gate": residual_gate,
        "weighted_ce_noninferiority": noninferiority,
        "strict_improvement": strict_improvement,
        "all_gates_passed": bool(all_passed),
        "bootstrap_intervals": intervals,
    }


def _pareto_artifact(
    rows: list[dict[str, object]],
    *,
    protocol: dict[str, Any],
    source_commit: str,
    failed_seeds: Sequence[Mapping[str, object]] = (),
) -> dict[str, object]:
    conditions = sorted(protocol["conditions"]["order"])
    seeds = _successful_model_seeds(protocol, failed_seeds)
    dimensions = list(protocol["pareto"]["dimensions"])
    seed_points = [
        {
            "condition_id": condition,
            "model_seed": seed,
            "metrics": _pareto_metrics(
                [row for row in _primary_base_rows(rows, condition) if row["model_seed"] == seed],
                protocol=protocol,
            ),
        }
        for condition in conditions
        for seed in seeds
    ]
    aggregate_points = [
        {
            "condition_id": condition,
            "metrics": _pareto_metrics(_primary_base_rows(rows, condition), protocol=protocol),
            "nondominated": False,
        }
        for condition in conditions
        if seeds
    ]
    for point in aggregate_points:
        point["nondominated"] = not any(
            other is not point and _dominates(other["metrics"], point["metrics"], dimensions)  # type: ignore[arg-type]
            for other in aggregate_points
        )
    pairwise: list[dict[str, object]] = []
    for left_index, left in enumerate(aggregate_points):
        for right in aggregate_points[left_index + 1 :]:
            left_dominates = _dominates(
                left["metrics"],
                right["metrics"],
                dimensions,  # type: ignore[arg-type]
            )
            right_dominates = _dominates(
                right["metrics"],
                left["metrics"],
                dimensions,  # type: ignore[arg-type]
            )
            has_null = any(
                left["metrics"][dimension["metric"]] is None  # type: ignore[index]
                or right["metrics"][dimension["metric"]] is None  # type: ignore[index]
                for dimension in dimensions
            )
            pairwise.append(
                {
                    "left_condition": left["condition_id"],
                    "right_condition": right["condition_id"],
                    "left_dominates": left_dominates,
                    "right_dominates": right_dominates,
                    "incomparable_reason": "null_metric" if has_null else None,
                }
            )
    return {
        "schema_version": "0.3",
        "protocol_id": protocol["protocol_id"],
        "source_commit": source_commit,
        "dimensions": dimensions,
        "seed_points": seed_points,
        "aggregate_points": aggregate_points,
        "pairwise_dominance": pairwise,
        "scientific_support": (
            _failure_scientific_support(protocol)
            if failed_seeds
            else _scientific_support(rows, protocol=protocol)
        ),
        "failed_seeds": list(failed_seeds),
    }


def _validate_decision_dict(value: object, label: str) -> dict[str, Any]:
    decision = _require_exact_keys(
        value,
        ("ignited", "belief_key", "object_key", "score", "margin", "reason", "citation_ids"),
        label,
    )
    if not isinstance(decision["ignited"], bool):
        raise RuntimeError(f"{label}.ignited must be bool")
    for name in ("belief_key", "object_key"):
        item = decision[name]
        if item is not None and (not isinstance(item, str) or not item):
            raise RuntimeError(f"{label}.{name} must be null or a non-empty string")
    _require_number(decision["score"], f"{label}.score")
    _require_number(decision["margin"], f"{label}.margin")
    if not isinstance(decision["reason"], str) or not decision["reason"]:
        raise RuntimeError(f"{label}.reason must be a non-empty string")
    _require_sorted_unique_strings(decision["citation_ids"], f"{label}.citation_ids")
    if decision["ignited"] != (decision["belief_key"] is not None):
        raise RuntimeError(f"{label} ignition and belief identity disagree")
    if not decision["ignited"] and decision["object_key"] is not None:
        raise RuntimeError(f"{label} rejected decisions must have null object_key")
    return decision


def _validate_state(value: object, protocol: dict[str, Any], label: str) -> dict[str, Any]:
    nested = protocol["metrics"]["nested_raw_contract"]
    state = _require_exact_keys(value, nested["state_fields"], label)
    activations = _require_exact_keys(
        state["activations"], nested["belief_probability_keys"], f"{label}.activations"
    )
    for belief, activation in activations.items():
        number = _require_number(activation, f"{label}.activations.{belief}")
        if number is not None and number < 0.0:
            raise RuntimeError(f"{label}.activations.{belief} must be nonnegative")
    _require_sorted_unique_strings(state["citations"], f"{label}.citations")
    history = _require_list(state["history"], f"{label}.history")
    beliefs = set(nested["belief_probability_keys"])
    if any(item not in beliefs for item in history):
        raise RuntimeError(f"{label}.history contains an invalid belief")
    if not isinstance(state["entity_key"], str) or not state["entity_key"]:
        raise RuntimeError(f"{label}.entity_key must be non-empty")
    _require_hash(state["state_hash"], f"{label}.state_hash")
    if state["winner"] is not None and state["winner"] not in beliefs:
        raise RuntimeError(f"{label}.winner is invalid")
    return state


def _validate_stage_trace(value: object, protocol: dict[str, Any], label: str) -> None:
    stages = _require_list(value, label)
    if len(stages) not in {2, 3}:
        raise RuntimeError(f"{label} must contain context stages followed by assessment")
    stage_fields = (
        "stage_index",
        "stage_role",
        "delivery_rows",
        "input_hash",
        "gate_passes",
        "proposal",
        "learned_decision",
        "state_before",
        "state_after",
    )
    delivery_fields = (
        "evidence_id",
        "source_id",
        "correlation_group",
        "entity_key",
        "hypothesis_id",
        "polarity",
        "strength",
        "time",
        "redelivery",
    )
    for index, raw_stage in enumerate(stages):
        stage = _require_exact_keys(raw_stage, stage_fields, f"{label}[{index}]")
        expected_stage_index = 2 if index == len(stages) - 1 else index
        if stage["stage_index"] != expected_stage_index:
            raise RuntimeError(f"{label}[{index}].stage_index is not the frozen stage number")
        expected_role = "assessment" if index == len(stages) - 1 else "context"
        if stage["stage_role"] != expected_role:
            raise RuntimeError(f"{label}[{index}].stage_role is invalid")
        _require_hash(stage["input_hash"], f"{label}[{index}].input_hash")
        deliveries = _require_list(stage["delivery_rows"], f"{label}[{index}].delivery_rows")
        if not deliveries:
            raise RuntimeError(f"{label}[{index}] must retain deliveries")
        seen: set[str] = set()
        for delivery_index, raw_delivery in enumerate(deliveries):
            delivery = _require_exact_keys(
                raw_delivery,
                delivery_fields,
                f"{label}[{index}].delivery_rows[{delivery_index}]",
            )
            for name in (
                "evidence_id",
                "source_id",
                "correlation_group",
                "entity_key",
                "hypothesis_id",
                "polarity",
            ):
                if not isinstance(delivery[name], str) or not delivery[name]:
                    raise RuntimeError(f"{label} delivery {name} must be non-empty")
            _require_number(delivery["strength"], f"{label} delivery strength")
            _require_number(delivery["time"], f"{label} delivery time")
            expected_redelivery = delivery["evidence_id"] in seen
            if delivery["redelivery"] is not expected_redelivery:
                raise RuntimeError(f"{label} redelivery marker is inconsistent")
            seen.add(delivery["evidence_id"])
        passes = _require_list(stage["gate_passes"], f"{label}[{index}].gate_passes")
        if len(passes) != 2:
            raise RuntimeError(f"{label}[{index}] must retain two gate passes")
        for pass_index, raw_pass in enumerate(passes, 1):
            gate_pass = _require_exact_keys(
                raw_pass,
                ("pass_index", "proposal"),
                f"{label}[{index}].gate_passes[{pass_index - 1}]",
            )
            if gate_pass["pass_index"] != pass_index:
                raise RuntimeError(f"{label}[{index}] gate pass order is invalid")
            _validate_decision_dict(gate_pass["proposal"], f"{label}[{index}] gate proposal")
        _validate_decision_dict(stage["proposal"], f"{label}[{index}].proposal")
        _validate_decision_dict(stage["learned_decision"], f"{label}[{index}].learned_decision")
        _validate_state(stage["state_before"], protocol, f"{label}[{index}].state_before")
        _validate_state(stage["state_after"], protocol, f"{label}[{index}].state_after")


def _validate_raw_rows(
    rows: list[dict[str, object]],
    protocol: dict[str, Any],
    failed_seeds: Sequence[Mapping[str, object]] = (),
) -> None:
    from sparkbrain.v03_seed.revision_worlds import build_split_manifest

    contract = protocol["artifacts"]
    successful_seeds = _successful_model_seeds(protocol, failed_seeds)
    expected_raw_count = (
        len(successful_seeds)
        * int(protocol["failure_contract"]["successful_seed_cardinality"]["raw_rows_per_seed"])
    )
    if len(rows) != expected_raw_count:
        raise RuntimeError("C15 per-transition raw row cardinality mismatch")
    required = list(contract["required_raw_fields"])
    beliefs = set(protocol["fixture_generator"]["belief_order"])
    transitions = set(protocol["transition_contract"]["labels"])
    variants = set(protocol["variants"]["order"])
    conditions = set(protocol["conditions"]["order"])
    seeds = set(successful_seeds)
    input_tracks = {"I0_whole_hash", "I1_local_compositional", "I2_symbolic_oracle"}
    entity_conditions = {"E0_global", "E1_oracle_entity"}
    sort_fields = list(contract["raw_sort"])
    sort_keys: list[tuple[object, ...]] = []
    actual_keys: set[tuple[object, ...]] = set()
    manifests = {
        split: {row.episode_id: row for row in build_split_manifest(split)}
        for split in ("dev", "test")
    }
    for index, raw in enumerate(rows):
        label = f"per_transition_predictions[{index}]"
        row = _require_exact_keys(raw, required, label)
        _require_finite_json(row, label)
        if row["schema_version"] != "0.3" or row["split"] not in {"dev", "test"}:
            raise RuntimeError(f"{label} schema/split is invalid")
        if row["condition_id"] not in conditions or row["model_seed"] not in seeds:
            raise RuntimeError(f"{label} condition/seed is invalid")
        if (
            row["input_track"] not in input_tracks
            or row["entity_condition"] not in entity_conditions
        ):
            raise RuntimeError(f"{label} diagnostic cell is invalid")
        if (
            row["variant_id"] not in variants
            or row["world"] not in protocol["splits"]["world_order"]
        ):
            raise RuntimeError(f"{label} variant/world is invalid")
        fixture = manifests[str(row["split"])].get(str(row["episode_id"]))
        if fixture is None or (
            row["episode_seed"], row["family_id"], row["world"]
        ) != (fixture.episode_seed, fixture.family_id, fixture.world):
            raise RuntimeError(f"{label} does not match the frozen split fixture")
        _require_int(row["episode_seed"], f"{label}.episode_seed")
        for name in ("episode_id", "family_id", "evaluated_entity_key", "reason"):
            if not isinstance(row[name], str) or not row[name]:
                raise RuntimeError(f"{label}.{name} must be a non-empty string")
        if row["truth_belief"] not in beliefs or row["previous_truth_belief"] not in beliefs:
            raise RuntimeError(f"{label} evaluator beliefs are invalid")
        if (
            row["predicted_belief"] is not None
            and row["predicted_belief"] not in beliefs
        ) or row["transition_target"] not in transitions:
            raise RuntimeError(f"{label} prediction/target is invalid")
        if row["predicted_transition"] not in transitions:
            raise RuntimeError(f"{label}.predicted_transition is invalid")
        for name in (
            "sufficient_information",
            "recovery_opportunity",
            "ignited",
            "checkpoint_restored",
            "protocol_compliant",
        ):
            if not isinstance(row[name], bool):
                raise RuntimeError(f"{label}.{name} must be bool")
        if row["checkpoint_restored"] or not row["protocol_compliant"]:
            raise RuntimeError(f"{label} violates checkpoint/protocol flags")
        _require_probability(row["no_ignition_probability"], f"{label}.no_ignition_probability")
        belief_probabilities = _require_exact_keys(
            row["belief_probabilities"],
            protocol["metrics"]["nested_raw_contract"]["belief_probability_keys"],
            f"{label}.belief_probabilities",
        )
        transition_probabilities = _require_exact_keys(
            row["transition_probabilities"],
            protocol["metrics"]["nested_raw_contract"]["transition_probability_keys"],
            f"{label}.transition_probabilities",
        )
        for name, probabilities in (
            ("belief", belief_probabilities),
            ("transition", transition_probabilities),
        ):
            values = [
                _require_probability(value, f"{label}.{name}_probabilities.{key}")
                for key, value in probabilities.items()
            ]
            if not math.isclose(
                sum(float(value) for value in values),
                1.0,
                rel_tol=0.0,
                abs_tol=1e-12,
            ):
                raise RuntimeError(f"{label}.{name}_probabilities do not sum to one")
        _require_sorted_unique_strings(row["cited_evidence_ids"], f"{label}.cited_evidence_ids")
        _require_sorted_unique_strings(row["attribution_targets"], f"{label}.attribution_targets")
        attribution = _require_list(
            row["attribution_probabilities"], f"{label}.attribution_probabilities"
        )
        if len(attribution) != 5:
            raise RuntimeError(f"{label} must retain exactly five attribution slots")
        item_fields = protocol["metrics"]["nested_raw_contract"][
            "attribution_probability_item_fields"
        ]
        for item_index, raw_item in enumerate(attribution):
            item = _require_exact_keys(
                raw_item, item_fields, f"{label}.attribution_probabilities[{item_index}]"
            )
            if item["evidence_id"] is None:
                if item["probability"] is not None:
                    raise RuntimeError(f"{label} padding attribution must be null")
            else:
                if not isinstance(item["evidence_id"], str) or not item["evidence_id"]:
                    raise RuntimeError(f"{label} attribution evidence ID is invalid")
                _require_probability(item["probability"], f"{label} attribution probability")
        before = _validate_state(row["state_before"], protocol, f"{label}.state_before")
        after = _validate_state(row["state_after"], protocol, f"{label}.state_after")
        if (
            before["entity_key"] != row["evaluated_entity_key"]
            or after["entity_key"] != row["evaluated_entity_key"]
        ):
            raise RuntimeError(f"{label} state entity does not match evaluated entity")
        _validate_stage_trace(row["stage_trace"], protocol, f"{label}.stage_trace")
        _require_hash(row["state_lineage_hash"], f"{label}.state_lineage_hash")
        _require_hash(row["input_hash"], f"{label}.input_hash")
        _require_hash(row["target_hash"], f"{label}.target_hash")
        if row["recovery_latency_steps"] is not None:
            latency = _require_int(
                row["recovery_latency_steps"], f"{label}.recovery_latency_steps", minimum=1
            )
            if latency not in {1, 2}:
                raise RuntimeError(f"{label}.recovery_latency_steps must be 1, 2, or null")
        composite_key = tuple(row[name] for name in sort_fields)
        if composite_key in actual_keys:
            raise RuntimeError("C15 raw rows contain a duplicate canonical composite key")
        actual_keys.add(composite_key)
        sort_keys.append(composite_key)
    if sort_keys != sorted(sort_keys):
        raise RuntimeError("C15 raw rows are not in the frozen canonical order")

    primary = protocol["conditions"]["primary_cell"]
    expected_cells = {
        (condition, primary["input_track"], primary["entity_condition"])
        for condition in protocol["conditions"]["order"]
    }
    expected_cells.update(
        ("full_separated", input_track, entity_condition)
        for input_track, entity_condition in protocol["conditions"][
            "diagnostic_full_only_cells"
        ]
    )
    expected_keys = {
        (split, condition, input_track, entity_condition, seed, episode_id, variant)
        for split, manifest in manifests.items()
        for condition, input_track, entity_condition in expected_cells
        for seed in successful_seeds
        for episode_id in manifest
        for variant in protocol["variants"]["order"]
    }
    if actual_keys != expected_keys:
        missing = len(expected_keys - actual_keys)
        unexpected = len(actual_keys - expected_keys)
        raise RuntimeError(
            "C15 raw canonical composite set mismatch "
            f"(missing={missing}, unexpected={unexpected})"
        )


def _validate_tabular_artifact(
    value: object,
    *,
    protocol: dict[str, Any],
    artifact_name: str,
) -> None:
    contract = protocol["artifacts"]["derived_contracts"][artifact_name]
    artifact = _require_exact_keys(value, contract["exact_top_level_fields"], artifact_name)
    _require_finite_json(artifact, artifact_name)
    failed_seeds = _validate_failed_seeds(
        artifact["failed_seeds"], protocol, f"{artifact_name}.failed_seeds"
    )
    successful_count = len(_successful_model_seeds(protocol, failed_seeds))
    cardinality = protocol["failure_contract"]["successful_seed_cardinality"]
    seed_per_name = {
        "confusion_matrices.json": "confusion_seed_rows_per_seed",
        "calibration_by_input_track.json": "calibration_seed_rows_per_seed",
    }
    for container_name, row_fields_name in (
        ("seed_rows", "seed_row_fields"),
        ("aggregate_rows", "aggregate_row_fields"),
    ):
        rows = _require_list(artifact[container_name], f"{artifact_name}.{container_name}")
        expected_count = (
            successful_count * int(cardinality[seed_per_name[artifact_name]])
            if container_name == "seed_rows"
            else int(cardinality["aggregate_rows_when_any_seed_succeeds"])
            if successful_count
            else 0
        )
        if len(rows) != expected_count:
            raise RuntimeError(f"{artifact_name}.{container_name} has invalid cardinality")
        sort_keys: list[tuple[object, ...]] = []
        for index, row in enumerate(rows):
            item = _require_exact_keys(
                row,
                contract[row_fields_name],
                f"{artifact_name}.{container_name}[{index}]",
            )
            label = f"{artifact_name}.{container_name}[{index}]"
            _require_int(item["row_count"], f"{label}.row_count")
            if artifact_name == "confusion_matrices.json":
                labels = list(protocol["transition_contract"]["labels"])
                confusion = _require_exact_keys(
                    item["transition_confusion"], labels, f"{label}.transition_confusion"
                )
                for target, raw_counts in confusion.items():
                    counts = _require_exact_keys(
                        raw_counts, labels, f"{label}.transition_confusion.{target}"
                    )
                    for predicted, count in counts.items():
                        _require_int(count, f"{label}.transition_confusion.{target}.{predicted}")
                for name in ("maintain_ovr", "update_ovr"):
                    counts = _require_exact_keys(
                        item[name], ("tn", "fp", "fn", "tp"), f"{label}.{name}"
                    )
                    for key, count in counts.items():
                        _require_int(count, f"{label}.{name}.{key}")
                for name in (
                    "unnecessary_revision_count",
                    "unnecessary_revision_denominator",
                    "missed_revision_count",
                    "missed_revision_denominator",
                    "revision_tp",
                    "revision_fp",
                    "revision_fn",
                    "recovery_opportunities",
                    "recovery_successes",
                    "recovery_censored",
                    "no_ignition_tp",
                    "no_ignition_fp",
                    "no_ignition_fn",
                ):
                    _require_int(item[name], f"{label}.{name}")
                for name in (
                    "unnecessary_revision_rate",
                    "missed_revision_rate",
                    "revision_precision",
                    "revision_recall",
                    "recovery_rate",
                    "recovery_latency_observed_mean",
                    "recovery_latency_censored_mean",
                    "no_ignition_precision",
                    "no_ignition_recall",
                    "no_ignition_f1",
                    "accuracy",
                    "coverage",
                ):
                    _require_number(item[name], f"{label}.{name}", nullable=True)
            else:
                _require_int(item["decided_count"], f"{label}.decided_count")
                for name in (
                    "coverage",
                    "multiclass_brier",
                    "nll",
                    "abstention_brier",
                    "ece",
                ):
                    _require_number(item[name], f"{label}.{name}", nullable=True)
                bins = _require_list(item["ece_bins"], f"{label}.ece_bins")
                if len(bins) != 10:
                    raise RuntimeError(f"{label}.ece_bins must contain ten bins")
                for bin_index, raw_bin in enumerate(bins):
                    bin_label = f"{label}.ece_bins[{bin_index}]"
                    bin_row = _require_exact_keys(
                        raw_bin, contract["ece_bin_fields"], bin_label
                    )
                    for name in ("lower_inclusive", "upper_exclusive"):
                        _require_number(bin_row[name], f"{bin_label}.{name}")
                    if not isinstance(bin_row["include_upper"], bool):
                        raise RuntimeError(f"{bin_label}.include_upper must be bool")
                    _require_int(bin_row["count"], f"{bin_label}.count")
                    for name in ("mean_confidence", "accuracy"):
                        _require_number(bin_row[name], f"{bin_label}.{name}", nullable=True)
            sort_fields = [
                name for name in contract["sort"] if name in contract[row_fields_name]
            ]
            sort_keys.append(tuple(item[name] for name in sort_fields))
        if sort_keys != sorted(sort_keys) or len(sort_keys) != len(set(sort_keys)):
            raise RuntimeError(f"{artifact_name}.{container_name} order is not canonical")


def _visible_feature_row(
    evidence: object,
    *,
    input_track: str,
    first_correlation_group: str,
    truth_belief: str,
    sufficient_information: bool,
) -> list[float]:
    from sparkbrain.v03_seed.revision_worlds import BELIEF_ORDER

    row = evidence
    if input_track == "I0_whole_hash":
        payload = {
            "correlation_group": row.correlation_group,
            "entity_key": row.entity_key,
            "evidence_id": row.evidence_id,
            "hypothesis_id": row.hypothesis_id,
            "polarity": row.polarity,
            "source_id": row.source_id,
            "strength": row.strength,
            "time": row.time,
        }
        features = [0.0] * 12
        index = int.from_bytes(hashlib.sha256(_canonical(payload).encode()).digest()[:8], "big") % 8
        features[index] = 1.0
        features[11] = 1.0
        return features
    if input_track == "I2_symbolic_oracle":
        features = [0.0] * 12
        features[BELIEF_ORDER.index(truth_belief)] = 1.0
        features[3] = float(sufficient_information)
        features[11] = 1.0
        return features
    if input_track != "I1_local_compositional":
        raise ValueError("C15 input track is invalid")
    features = [0.0] * 12
    features[BELIEF_ORDER.index(row.hypothesis_id)] = 1.0
    features[3] = float(row.polarity == "support")
    features[4] = float(row.polarity == "contradict")
    features[5] = float(row.strength)
    features[6] = min(max(float(row.time) / 25.0, 0.0), 1.0)
    bucket = int.from_bytes(hashlib.sha256(row.source_id.encode()).digest()[:8], "big") % 3
    features[7 + bucket] = 1.0
    features[10] = float(row.correlation_group == first_correlation_group)
    features[11] = 1.0
    return features


def _stage_model_call(
    deliveries: Sequence[object],
    *,
    input_track: str,
    entity_condition: str,
    truth_belief: str,
    sufficient_information: bool,
) -> dict[str, object]:
    from sparkbrain.v03_seed.revision_worlds import (
        adapt_fixture_entity_key,
        fixture_evidence_to_record,
    )

    if not deliveries:
        raise ValueError("C15 stages require visible evidence")
    unique: list[object] = []
    seen: set[str] = set()
    for evidence in deliveries:
        record = fixture_evidence_to_record(evidence, entity_condition=entity_condition)
        if record.evidence_id not in seen:
            seen.add(record.evidence_id)
            unique.append(record)
    if len(unique) > 5:
        raise ValueError("C15 stage exceeds five unique candidate slots")
    first_group = str(unique[0].correlation_group)
    features = [
        _visible_feature_row(
            record,
            input_track=input_track,
            first_correlation_group=first_group,
            truth_belief=truth_belief,
            sufficient_information=sufficient_information,
        )
        for record in unique
    ]
    evidence_ids: list[str | None] = [record.evidence_id for record in unique]
    padding_mask = [True] * len(unique)
    while len(features) < 5:
        features.append([0.0] * 12)
        evidence_ids.append(None)
        padding_mask.append(False)
    return {
        "entity_key": adapt_fixture_entity_key(
            deliveries[0].entity_key, entity_condition=entity_condition
        ),
        "features": features,
        "evidence_ids": evidence_ids,
        "padding_mask": padding_mask,
    }


def _episode_envelope(
    fixture: object,
    *,
    variant_id: str,
    input_track: str,
    entity_condition: str,
    condition_id: str,
) -> dict[str, object]:
    from sparkbrain.v03_seed.revision_worlds import BELIEF_ORDER, map_attribution_target_ids

    variant = next(row for row in fixture.variants if row.variant_id == variant_id)
    stages = [*fixture.context_stages, variant.assessment_deliveries]
    model_calls = [
        _stage_model_call(
            stage,
            input_track=input_track,
            entity_condition=entity_condition,
            truth_belief=fixture.target_truth,
            sufficient_information=fixture.sufficient_information,
        )
        for stage in stages
    ]
    if condition_id == "one_weighted_ce":
        target: dict[str, object] = {
            "belief_index": BELIEF_ORDER.index(fixture.target_truth),
            "sufficient_information": fixture.sufficient_information,
        }
    else:
        target = {
            "belief_index": BELIEF_ORDER.index(fixture.target_truth),
            "previous_belief_index": BELIEF_ORDER.index(fixture.previous_truth),
            "transition_target": fixture.transition_target,
            "sufficient_information": fixture.sufficient_information,
            "attribution_target_ids": list(
                map_attribution_target_ids(
                    variant.attribution_targets,
                    entity_condition=entity_condition,
                )
            ),
        }
    return {
        "episode_id": fixture.episode_id,
        "variant_id": variant_id,
        "input_track": input_track,
        "entity_condition": entity_condition,
        "model_calls": model_calls,
        "assessment_index": len(fixture.context_stages),
        "target": target,
    }


def _head_output(model_output: object, *, temperature: float) -> object:
    from sparkbrain.v03_seed.revision import RevisionHeadOutput
    from sparkbrain.v03_seed.revision_worlds import BELIEF_ORDER

    beliefs = model_output.conditional_belief_probabilities(temperature=temperature)
    values = _normalized_probabilities(beliefs.detach().cpu().tolist())
    return RevisionHeadOutput(
        belief_probabilities={
            belief: float(values[index]) for index, belief in enumerate(BELIEF_ORDER)
        },
        maintain_probability=float(model_output.maintain_logit.sigmoid().detach().cpu()),
        update_probability=float(model_output.update_logit.sigmoid().detach().cpu()),
        recovery_probability=float(model_output.recovery_logit.sigmoid().detach().cpu()),
        abstention_probability=float(model_output.abstention_logit.sigmoid().detach().cpu()),
    )


def _normalized_probabilities(values: object) -> list[float]:
    probabilities = [float(value) for value in values]  # type: ignore[union-attr]
    if not probabilities or any(not math.isfinite(value) or value < 0.0 for value in probabilities):
        raise RuntimeError("C15 model probabilities must be finite and nonnegative")
    total = sum(probabilities)
    if total <= 0.0:
        raise RuntimeError("C15 model probabilities must have positive mass")
    normalized = [value / total for value in probabilities]
    normalized[-1] = 1.0 - sum(normalized[:-1])
    if normalized[-1] < 0.0:
        raise RuntimeError("C15 probability normalization produced negative mass")
    return normalized


def _controller_for_condition(condition_id: str, *, abstention_threshold: float) -> object:
    from sparkbrain.v03_seed.revision import RevisionBeliefField, RevisionController

    belief_field = RevisionBeliefField(
        decay=0.88,
        loser_retention=0.0 if condition_id == "no_residual" else 0.92,
    )
    return RevisionController(
        belief_field=belief_field,
        abstention_threshold=abstention_threshold,
    )


def _replay_context_activation(
    fixture: object,
    outputs: object,
    *,
    condition_id: str,
    entity_condition: str,
) -> float:
    from sparkbrain.v03_seed.revision import RevisionObservation
    from sparkbrain.v03_seed.revision_worlds import adapt_fixture_entity_key

    controller = _controller_for_condition(condition_id, abstention_threshold=0.5)
    for stage_index, deliveries in enumerate(fixture.context_stages):
        observation = RevisionObservation(
            entity_key=fixture.entity_key,
            entity_condition=entity_condition,
            time=float(stage_index * 10 + 5),
            evidence=tuple(deliveries),
            heads=_head_output(outputs.outputs[stage_index], temperature=1.0),
        )
        controller.process_stage(observation)
    evaluated = adapt_fixture_entity_key(fixture.entity_key, entity_condition=entity_condition)
    snapshot = controller.belief_field.snapshot(evaluated)
    return float(snapshot.activations[fixture.target_truth])


def _target_builder(
    fixtures_by_id: Mapping[str, object],
    *,
    condition_id: str,
):
    from sparkbrain.v03_learned.training import objective_target_with_state

    def build(episode: object, outputs: object) -> object:
        fixture = fixtures_by_id[episode.episode_id]
        activation = _replay_context_activation(
            fixture,
            outputs,
            condition_id=condition_id,
            entity_condition=episode.entity_condition,
        )
        return objective_target_with_state(
            episode,
            outputs,
            restored_prior_activation=activation,
        )

    return build


def _proposal_citations(proposal: object) -> list[str]:
    for coalition in proposal.coalitions:
        if (
            coalition.belief_key == proposal.belief_key
            and coalition.object_key == proposal.object_key
        ):
            return sorted(set(coalition.support_ids))
    return []


def _ignition_dict(proposal: object) -> dict[str, object]:
    return {
        "ignited": bool(proposal.ignited),
        "belief_key": proposal.belief_key,
        "object_key": proposal.object_key,
        "score": float(proposal.score),
        "margin": float(proposal.margin),
        "reason": str(proposal.reason),
        "citation_ids": _proposal_citations(proposal),
    }


def _revision_decision_dict(decision: object) -> dict[str, object]:
    return {
        "ignited": bool(decision.ignited),
        "belief_key": decision.belief_key,
        "object_key": decision.object_key,
        "score": float(decision.score),
        "margin": float(decision.margin),
        "reason": str(decision.reason),
        "citation_ids": sorted(set(decision.citation_ids)),
    }


def _delivery_rows(
    deliveries: Sequence[object], *, entity_condition: str
) -> list[dict[str, object]]:
    from sparkbrain.v03_seed.revision_worlds import fixture_evidence_to_record

    rows: list[dict[str, object]] = []
    seen: set[str] = set()
    for evidence in deliveries:
        record = fixture_evidence_to_record(evidence, entity_condition=entity_condition)
        rows.append(
            {
                "evidence_id": record.evidence_id,
                "source_id": record.source_id,
                "correlation_group": record.correlation_group,
                "entity_key": record.entity_key,
                "hypothesis_id": record.hypothesis_id,
                "polarity": record.polarity,
                "strength": record.strength,
                "time": record.time,
                "redelivery": record.evidence_id in seen,
            }
        )
        seen.add(record.evidence_id)
    return rows


def _checkpoint_scores(
    training_result: object,
    episodes: Sequence[object],
    fixtures_by_id: Mapping[str, object],
    *,
    condition_id: str,
) -> list[object]:
    from sparkbrain.v03_learned.objectives import ObjectiveWeights, compute_objective_losses
    from sparkbrain.v03_learned.training import (
        CheckpointScore,
        run_visible_episode,
    )

    target_builder = _target_builder(fixtures_by_id, condition_id=condition_id)
    scores: list[object] = []
    for epoch in (2, 4, 6):
        snapshot = training_result.checkpoints[epoch]
        training_result.model.load_state_dict(snapshot.state_dict)
        values: list[float] = []
        for episode in episodes:
            outputs = run_visible_episode(training_result.model, episode)
            target = (
                episode.target
                if condition_id == "one_weighted_ce"
                else target_builder(episode, outputs)
            )
            bundle = compute_objective_losses(
                model=training_result.model,
                assessment=outputs.assessment,
                episode_outputs=outputs.outputs,
                target=target,
                weights=ObjectiveWeights.for_condition(condition_id),
                one_weighted_ce=condition_id == "one_weighted_ce",
            )
            values.append(float(bundle.total_loss.detach().cpu()))
        scores.append(
            CheckpointScore(epoch=epoch, weighted_objective_total=sum(values) / len(values))
        )
    return scores


def _calibration_scores(model: object, episodes: Sequence[object]) -> list[object]:
    from sparkbrain.v03_learned.training import (
        ABSTENTION_THRESHOLD_GRID,
        TEMPERATURE_GRID,
        CalibrationScore,
        run_visible_episode,
    )

    cached = [(episode, run_visible_episode(model, episode)) for episode in episodes]
    scores: list[object] = []
    for temperature in TEMPERATURE_GRID:
        belief_brier = 0.0
        abstention_brier = 0.0
        for episode, outputs in cached:
            beliefs = (
                outputs.assessment.conditional_belief_probabilities(temperature=temperature)
                .detach()
                .cpu()
                .tolist()
            )
            belief_brier += sum(
                (float(probability) - float(index == episode.target.belief_index)) ** 2
                for index, probability in enumerate(beliefs)
            )
            abstention = float(outputs.assessment.abstention_logit.sigmoid().detach().cpu())
            abstention_brier += (abstention - float(not episode.target.sufficient_information)) ** 2
        for threshold in ABSTENTION_THRESHOLD_GRID:
            scores.append(
                CalibrationScore(
                    temperature=temperature,
                    abstention_threshold=threshold,
                    belief_brier=belief_brier / len(cached),
                    abstention_brier=abstention_brier / len(cached),
                )
            )
    return scores


def _evaluation_target(fixture: object) -> object:
    from sparkbrain.v03_seed.revision import RevisionTarget

    truth_history = (
        (fixture.target_truth, fixture.previous_truth)
        if fixture.world == "recover"
        else (fixture.previous_truth,)
    )
    variant = next(row for row in fixture.variants if row.variant_id == "base")
    causal = [
        row
        for row in variant.assessment_deliveries
        if row.hypothesis_id == fixture.target_truth and row.polarity == "support"
    ]
    target = RevisionTarget.from_truth_history(
        truth_history,
        truth_belief=fixture.target_truth,
        causal_source_count=len({row.source_id for row in causal}),
        causal_group_count=len({row.correlation_group for row in causal}),
    )
    if (
        target.transition.value != fixture.transition_target
        or target.sufficient_information != fixture.sufficient_information
    ):
        raise RuntimeError("C15 evaluator target disagrees with frozen fixture")
    return target


def _evaluate_episode(
    model: object,
    fixture: object,
    *,
    split: str,
    variant_id: str,
    input_track: str,
    entity_condition: str,
    condition_id: str,
    model_seed: int,
    temperature: float,
    abstention_threshold: float,
) -> dict[str, object]:
    from sparkbrain.v03_seed.revision import RevisionObservation
    from sparkbrain.v03_seed.revision_worlds import (
        adapt_fixture_entity_key,
        map_attribution_target_ids,
    )

    envelope = _episode_envelope(
        fixture,
        variant_id=variant_id,
        input_track=input_track,
        entity_condition=entity_condition,
        condition_id=condition_id,
    )
    model.reset_runtime()
    model_outputs = tuple(model.forward_fixture(call) for call in envelope["model_calls"])
    assessment_output = model_outputs[int(envelope["assessment_index"])]
    controller = _controller_for_condition(
        condition_id,
        abstention_threshold=abstention_threshold,
    )
    variant = next(row for row in fixture.variants if row.variant_id == variant_id)
    stages = [
        *[
            (stage_index, "context", deliveries, stage_index)
            for stage_index, deliveries in enumerate(fixture.context_stages)
        ],
        (2, "assessment", variant.assessment_deliveries, len(fixture.context_stages)),
    ]
    trace: list[dict[str, object]] = []
    decisions: list[object] = []
    for stage_index, stage_role, deliveries, model_output_index in stages:
        observation = RevisionObservation(
            entity_key=fixture.entity_key,
            entity_condition=entity_condition,
            time=float(stage_index * 10 + 5),
            evidence=tuple(deliveries),
            heads=_head_output(model_outputs[model_output_index], temperature=temperature),
        )
        decision = controller.process_stage(observation)
        decisions.append(decision)
        trace.append(
            {
                "stage_index": stage_index,
                "stage_role": stage_role,
                "delivery_rows": _delivery_rows(deliveries, entity_condition=entity_condition),
                "input_hash": decision.input_hash,
                "gate_passes": [
                    {"pass_index": index, "proposal": _ignition_dict(proposal)}
                    for index, proposal in enumerate(decision.gate_passes, 1)
                ],
                "proposal": _ignition_dict(decision.proposal),
                "learned_decision": _revision_decision_dict(decision),
                "state_before": decision.state_before.to_dict(),
                "state_after": decision.state_after.to_dict(),
            }
        )
    final = decisions[-1]
    target = _evaluation_target(fixture)
    belief_values = _normalized_probabilities(
        assessment_output.conditional_belief_probabilities(temperature=temperature)
        .detach()
        .cpu()
        .tolist()
    )
    transition_values = _normalized_probabilities(
        assessment_output.transition_probabilities().detach().cpu().tolist()
    )
    belief_probabilities = {
        belief: float(belief_values[index])
        for index, belief in enumerate(("alpha", "beta", "gamma"))
    }
    transition_probabilities = {
        transition: float(transition_values[index])
        for index, transition in enumerate(
            ("insufficient_information", "maintain", "recover", "update")
        )
    }
    attribution_values = assessment_output.attribution_logits.sigmoid().detach().cpu().tolist()
    attribution_probabilities = [
        {
            "evidence_id": evidence_id,
            "probability": float(attribution_values[index]) if evidence_id is not None else None,
        }
        for index, evidence_id in enumerate(assessment_output.evidence_ids)
    ]
    evaluated_entity_key = adapt_fixture_entity_key(
        fixture.entity_key, entity_condition=entity_condition
    )
    predicted_belief = final.state_after.winner
    recovery_success = (
        fixture.transition_target == "recover"
        and final.predicted_transition.value == "recover"
        and predicted_belief == fixture.target_truth
    )
    input_hash = _sha256_bytes(
        _canonical(
            {
                "assessment_index": envelope["assessment_index"],
                "entity_condition": entity_condition,
                "input_track": input_track,
                "model_calls": envelope["model_calls"],
            }
        ).encode()
    )
    target_hash = _sha256_bytes(target.to_canonical_json().encode())
    state_lineage_hash = _sha256_bytes(
        _canonical(
            [
                [stage["state_before"]["state_hash"], stage["state_after"]["state_hash"]]
                for stage in trace
            ]
        ).encode()
    )
    return {
        "schema_version": "0.3",
        "split": split,
        "condition_id": condition_id,
        "input_track": input_track,
        "entity_condition": entity_condition,
        "model_seed": model_seed,
        "episode_id": fixture.episode_id,
        "episode_seed": fixture.episode_seed,
        "family_id": fixture.family_id,
        "world": fixture.world,
        "variant_id": variant_id,
        "evaluated_entity_key": evaluated_entity_key,
        "truth_belief": fixture.target_truth,
        "previous_truth_belief": fixture.previous_truth,
        "transition_target": fixture.transition_target,
        "sufficient_information": fixture.sufficient_information,
        "recovery_opportunity": fixture.transition_target == "recover",
        "predicted_belief": predicted_belief,
        "predicted_transition": final.predicted_transition.value,
        "ignited": bool(final.ignited),
        "no_ignition_probability": float(
            assessment_output.abstention_logit.sigmoid().detach().cpu()
        ),
        "belief_probabilities": belief_probabilities,
        "transition_probabilities": transition_probabilities,
        "reason": final.reason,
        "cited_evidence_ids": sorted(set(final.citation_ids)),
        "attribution_targets": sorted(
            set(
            map_attribution_target_ids(
                variant.attribution_targets,
                entity_condition=entity_condition,
            )
            )
        ),
        "attribution_probabilities": attribution_probabilities,
        "state_before": final.state_before.to_dict(),
        "state_after": final.state_after.to_dict(),
        "stage_trace": trace,
        "state_lineage_hash": state_lineage_hash,
        "checkpoint_restored": False,
        "recovery_latency_steps": 2 if recovery_success else None,
        "input_hash": input_hash,
        "target_hash": target_hash,
        "protocol_compliant": True,
    }


def _training_input_hash(episodes: Sequence[object]) -> str:
    return _sha256_bytes(
        _canonical(
            [
                {
                    "assessment_index": episode.assessment_index,
                    "entity_condition": episode.entity_condition,
                    "episode_id": episode.episode_id,
                    "input_track": episode.input_track,
                    "model_calls": list(episode.model_calls),
                    "variant_id": episode.variant_id,
                }
                for episode in episodes
            ]
        ).encode()
    )


def _objective_rows(
    training_rows: list[dict[str, object]],
    *,
    protocol: dict[str, Any],
    successful_seeds: Sequence[int] | None = None,
) -> list[dict[str, object]]:
    objective_order = list(
        protocol["artifacts"]["derived_contracts"]["loss_ablation_metrics.json"][
            "training_step_objective_keys"
        ]
    )
    result: list[dict[str, object]] = []
    seeds = (
        list(successful_seeds)
        if successful_seeds is not None
        else sorted({int(row["model_seed"]) for row in training_rows})
    )
    for condition in protocol["conditions"]["order"]:
        for seed in seeds:
            selected = [
                row
                for row in training_rows
                if row["condition_id"] == condition and row["model_seed"] == seed
            ]
            expected_steps = int(protocol["objective_config"]["optimizer_steps"])
            if len(selected) != expected_steps:
                raise RuntimeError(
                    f"C15 objective aggregation requires {expected_steps} optimizer rows"
                )
            for objective_id in objective_order:
                values = [row["objectives"][objective_id] for row in selected]
                weight_values = {float(value["weight"]) for value in values}
                if len(weight_values) != 1:
                    raise RuntimeError("C15 objective weight changed within a run")
                weight = weight_values.pop()
                result.append(
                    {
                        "condition_id": condition,
                        "model_seed": seed,
                        "objective_id": objective_id,
                        "eligible_count": sum(int(value["eligible_count"]) for value in values),
                        "mean_raw_loss": sum(float(value["raw_loss"]) for value in values)
                        / len(values),
                        "weight": weight,
                        "mean_weighted_contribution": sum(
                            float(value["weighted_contribution"]) for value in values
                        )
                        / len(values),
                        "mean_unweighted_gradient_l2": sum(
                            float(value["unweighted_gradient_l2"]) for value in values
                        )
                        / len(values),
                        "mean_weighted_gradient_l2": sum(
                            float(value["weighted_gradient_l2"]) for value in values
                        )
                        / len(values),
                        "ablated": weight == 0.0,
                    }
                )
    result.sort(key=lambda row: (row["condition_id"], row["model_seed"], row["objective_id"]))
    return result


def _engineering_gates(
    raw: list[dict[str, object]],
    training_rows: list[dict[str, object]],
    objective_rows: list[dict[str, object]],
    *,
    protocol: dict[str, Any],
    failed_seeds: Sequence[Mapping[str, object]] = (),
) -> list[dict[str, object]]:
    seeds = list(protocol["seeds"]["model"])
    recovery_by_seed: dict[int, bool] = {}
    for seed in seeds:
        selected = [
            row
            for row in _primary_base_rows(raw, "full_separated")
            if row["model_seed"] == seed and row["transition_target"] == "recover"
        ]
        recovery_by_seed[int(seed)] = bool(selected) and all(
            row["predicted_belief"] == row["truth_belief"]
            and row["predicted_transition"] == "recover"
            and not row["checkpoint_restored"]
            for row in selected
        )
    zero_ablation = bool(objective_rows) and all(
        not row["ablated"]
        or (
            row["weight"] == 0.0
            and row["mean_weighted_contribution"] == 0.0
            and row["mean_weighted_gradient_l2"] == 0.0
        )
        for row in objective_rows
    )
    target_ids = {target for row in raw for target in row["attribution_targets"]}
    visible_ids = {
        item["evidence_id"]
        for row in raw
        for item in row["attribution_probabilities"]
        if item["evidence_id"] is not None
    }
    citation_ids = {citation for row in raw for citation in row["cited_evidence_ids"]}
    lineage_ids = {
        delivery["evidence_id"]
        for row in raw
        for stage in row["stage_trace"]
        for delivery in stage["delivery_rows"]
    }
    has_raw = bool(raw)
    gates = [
        (
            "raw_row_count",
            len(raw),
            int(protocol["artifacts"]["raw_row_count"]),
            len(raw) == int(protocol["artifacts"]["raw_row_count"]),
        ),
        ("training_step_count", len(training_rows), 23040, len(training_rows) == 23040),
        (
            "continuous_recovery_all_seeds",
            recovery_by_seed,
            {int(seed): True for seed in seeds},
            not failed_seeds and all(recovery_by_seed.values()),
        ),
        (
            "checkpoint_restore_zero",
            sum(row["checkpoint_restored"] for row in raw) if has_raw else None,
            0,
            has_raw and not any(row["checkpoint_restored"] for row in raw),
        ),
        (
            "explicit_no_ignition",
            sum(not row["ignited"] for row in raw) if has_raw else None,
            1,
            has_raw and any(not row["ignited"] for row in raw),
        ),
        ("objective_ablation_exact_zero", zero_ablation, True, zero_ablation),
        (
            "attribution_target_coverage",
            len(target_ids & visible_ids) / len(target_ids) if target_ids else None,
            1.0,
            bool(target_ids) and target_ids <= visible_ids,
        ),
        (
            "citation_resolvability",
            len(citation_ids & lineage_ids) / len(citation_ids)
            if citation_ids
            else None
            if failed_seeds
            else 1.0,
            1.0,
            citation_ids <= lineage_ids if citation_ids else not failed_seeds,
        ),
    ]
    return [
        {"gate_id": gate_id, "observed": observed, "threshold": threshold, "passed": bool(passed)}
        for gate_id, observed, threshold, passed in gates
    ]


def _objective_config_artifact(
    condition_seed_rows: list[dict[str, object]],
    *,
    protocol: dict[str, Any],
    source_commit: str,
    failed_seeds: Sequence[Mapping[str, object]] = (),
) -> dict[str, object]:
    from sparkbrain.v03_learned.objectives import ObjectiveWeights

    by_condition = {
        condition: [row for row in condition_seed_rows if row["condition_id"] == condition]
        for condition in sorted(protocol["conditions"]["order"])
    }
    conditions = []
    for condition in sorted(protocol["conditions"]["order"]):
        rows = by_condition[condition]
        parameter_counts = {int(row["parameter_count"]) for row in rows}
        if len(parameter_counts) > 1:
            raise RuntimeError("C15 parameter count changed across seeds")
        conditions.append(
            {
                "condition_id": condition,
                "objective_weights": ObjectiveWeights.for_condition(condition).as_dict(),
                "residual_retention": 0.0 if condition == "no_residual" else 0.92,
                "baseline_kind": "one_weighted_ce"
                if condition == "one_weighted_ce"
                else "separated_objectives",
                "parameter_count": parameter_counts.pop() if parameter_counts else 3132,
                "optimizer_steps": int(protocol["objective_config"]["optimizer_steps"]),
            }
        )
    config = protocol["objective_config"]
    return {
        "schema_version": "0.3",
        "protocol_id": protocol["protocol_id"],
        "source_commit": source_commit,
        "model": {
            "active_k": config["active_k"],
            "belief_order": list(protocol["fixture_generator"]["belief_order"]),
            "candidate_slots": 5,
            "hidden_dim": config["hidden_dim"],
            "module_count": config["module_count"],
        },
        "training": {
            "epochs": config["epochs"],
            "learning_rate": config["learning_rate"],
            "optimizer": config["optimizer"],
            "batch_size_episodes": 1,
            "shuffle": False,
            "drop_last": False,
            "training_cell": list(config["training_cell"]),
            "training_variants": ["base"],
        },
        "selection": {
            "checkpoint_epochs": list(config["checkpoint_epochs"]),
            "checkpoint_dev_indices": [0, 1, 2, 3],
            "calibration_dev_indices": [4, 5, 6, 7],
            "temperature_grid": list(protocol["selection"]["calibration_grid"]["temperature"]),
            "abstention_threshold_grid": list(
                protocol["selection"]["calibration_grid"]["abstention_thresholds"]
            ),
            "test_evaluations": 1,
        },
        "conditions": conditions,
        "failed_seeds": list(failed_seeds),
    }


def _run_training_and_evaluation(
    *, protocol: dict[str, Any], source_commit: str
) -> tuple[
    list[dict[str, object]],
    dict[str, object],
    dict[str, object],
    list[dict[str, object]],
]:
    from sparkbrain.v03_learned.training import (
        TrainingEpisode,
        select_calibration,
        select_checkpoint,
        train_condition,
    )
    from sparkbrain.v03_seed.revision_worlds import build_full_fixture

    train_fixtures = list(build_full_fixture("train"))
    dev_fixtures = list(build_full_fixture("dev"))
    test_fixtures = list(build_full_fixture("test"))
    train_by_id = {fixture.episode_id: fixture for fixture in train_fixtures}
    dev_by_id = {fixture.episode_id: fixture for fixture in dev_fixtures}
    selection_fixtures = [
        fixture
        for world in protocol["splits"]["world_order"]
        for fixture in [row for row in dev_fixtures if row.world == world][:4]
    ]
    calibration_fixtures = [
        fixture
        for world in protocol["splits"]["world_order"]
        for fixture in [row for row in dev_fixtures if row.world == world][4:8]
    ]
    training_rows: list[dict[str, object]] = []
    condition_seed_rows: list[dict[str, object]] = []
    raw: list[dict[str, object]] = []
    failed_seeds: list[dict[str, object]] = []
    primary_cell = protocol["conditions"]["primary_cell"]
    primary = [(primary_cell["input_track"], primary_cell["entity_condition"])]
    diagnostics = [tuple(row) for row in protocol["conditions"]["diagnostic_full_only_cells"]]
    for seed in protocol["seeds"]["model"]:
        seed_training: list[dict[str, object]] = []
        seed_conditions: list[dict[str, object]] = []
        seed_raw: list[dict[str, object]] = []
        phase = "training"
        condition = str(protocol["conditions"]["order"][0])
        try:
            for condition in protocol["conditions"]["order"]:
                phase = "training"
                training_episodes = [
                    TrainingEpisode.from_fixture(
                        _episode_envelope(
                            fixture,
                            variant_id="base",
                            input_track="I1_local_compositional",
                            entity_condition="E1_oracle_entity",
                            condition_id=condition,
                        )
                    )
                    for fixture in train_fixtures
                ]
                selection_episodes = [
                    TrainingEpisode.from_fixture(
                        _episode_envelope(
                            fixture,
                            variant_id="base",
                            input_track="I1_local_compositional",
                            entity_condition="E1_oracle_entity",
                            condition_id=condition,
                        )
                    )
                    for fixture in selection_fixtures
                ]
                calibration_episodes = [
                    TrainingEpisode.from_fixture(
                        _episode_envelope(
                            fixture,
                            variant_id="base",
                            input_track="I1_local_compositional",
                            entity_condition="E1_oracle_entity",
                            condition_id=condition,
                        )
                    )
                    for fixture in calibration_fixtures
                ]
                training_hash = _training_input_hash(training_episodes)
                cells = primary + (diagnostics if condition == "full_separated" else [])
                result = train_condition(
                    training_episodes,
                    condition_id=condition,
                    model_seed=int(seed),
                    target_builder=_target_builder(train_by_id, condition_id=condition),
                )
                seed_training.extend(
                    row.as_artifact_row() for row in result.training_step_rows
                )
                phase = "checkpoint_selection"
                checkpoint = select_checkpoint(
                    _checkpoint_scores(
                        result,
                        selection_episodes,
                        dev_by_id,
                        condition_id=condition,
                    )
                )
                snapshot = result.checkpoints[checkpoint.epoch]
                result.model.load_state_dict(snapshot.state_dict)
                result.model.eval()
                phase = "calibration"
                calibration = select_calibration(
                    _calibration_scores(result.model, calibration_episodes)
                )
                seed_conditions.append(
                    {
                        "condition_id": condition,
                        "model_seed": seed,
                        "selected_epoch": checkpoint.epoch,
                        "temperature": calibration.temperature,
                        "abstention_threshold": calibration.abstention_threshold,
                        "optimizer_steps": int(
                            protocol["objective_config"]["optimizer_steps"]
                        ),
                        "parameter_count": result.parameter_count,
                        "training_input_hash": training_hash,
                        "checkpoint_hash": snapshot.sha256,
                        "protocol_compliant": True,
                    }
                )
                for split, fixtures in (("dev", dev_fixtures), ("test", test_fixtures)):
                    phase = f"{split}_evaluation"
                    for input_track, entity_condition in cells:
                        for fixture in fixtures:
                            for variant in protocol["variants"]["order"]:
                                seed_raw.append(
                                    _evaluate_episode(
                                        result.model,
                                        fixture,
                                        split=split,
                                        variant_id=variant,
                                        input_track=input_track,
                                        entity_condition=entity_condition,
                                        condition_id=condition,
                                        model_seed=int(seed),
                                        temperature=calibration.temperature,
                                        abstention_threshold=calibration.abstention_threshold,
                                    )
                                )
        except Exception as exc:  # noqa: BLE001 - frozen seed failure boundary
            error_type = type(exc).__name__
            failed_seeds.append(
                {
                    "model_seed": int(seed),
                    "phase": phase,
                    "condition_id": condition,
                    "error_type": error_type,
                    "error_hash": _sha256_bytes(
                        _canonical([phase, condition, error_type]).encode()
                    ),
                }
            )
            continue
        training_rows.extend(seed_training)
        condition_seed_rows.extend(seed_conditions)
        raw.extend(seed_raw)
    raw.sort(key=lambda row: tuple(row[name] for name in protocol["artifacts"]["raw_sort"]))
    training_rows.sort(
        key=lambda row: (
            row["condition_id"],
            row["model_seed"],
            row["optimizer_step"],
        )
    )
    condition_seed_rows.sort(key=lambda row: (row["condition_id"], row["model_seed"]))
    successful_seeds = sorted({int(row["model_seed"]) for row in condition_seed_rows})
    objective_rows = _objective_rows(
        training_rows, protocol=protocol, successful_seeds=successful_seeds
    )
    gates = _engineering_gates(
        raw,
        training_rows,
        objective_rows,
        protocol=protocol,
        failed_seeds=failed_seeds,
    )
    from sparkbrain.v03_learned.objectives import OBJECTIVE_ORDER

    loss_metrics = {
        "schema_version": "0.3",
        "protocol_id": protocol["protocol_id"],
        "source_commit": source_commit,
        "objective_order": list(OBJECTIVE_ORDER),
        "training_step_rows": training_rows,
        "condition_seed_rows": condition_seed_rows,
        "objective_rows": objective_rows,
        "engineering_gates": gates,
        "scientific_gates": {},
        "failed_seeds": failed_seeds,
    }
    objective_config = _objective_config_artifact(
        condition_seed_rows,
        protocol=protocol,
        source_commit=source_commit,
        failed_seeds=failed_seeds,
    )
    return raw, objective_config, loss_metrics, failed_seeds


def _validate_objective_config(value: object, protocol: dict[str, Any]) -> None:
    contract = protocol["artifacts"]["derived_contracts"]["objective_config.json"]
    artifact = _require_exact_keys(
        value, contract["exact_top_level_fields"], "objective_config.json"
    )
    _require_finite_json(artifact, "objective_config.json")
    _validate_failed_seeds(artifact["failed_seeds"], protocol, "objective_config.failed_seeds")
    model = _require_exact_keys(
        artifact["model"], contract["model_fields"], "objective_config.model"
    )
    training = _require_exact_keys(
        artifact["training"], contract["training_fields"], "objective_config.training"
    )
    selection = _require_exact_keys(
        artifact["selection"], contract["selection_fields"], "objective_config.selection"
    )
    for name in ("active_k", "candidate_slots", "hidden_dim", "module_count"):
        _require_int(model[name], f"objective_config.model.{name}", minimum=1)
    _require_sorted_unique_strings(model["belief_order"], "objective_config.model.belief_order")
    _require_int(training["epochs"], "objective_config.training.epochs", minimum=1)
    _require_number(training["learning_rate"], "objective_config.training.learning_rate")
    _require_int(
        training["batch_size_episodes"],
        "objective_config.training.batch_size_episodes",
        minimum=1,
    )
    for name in ("shuffle", "drop_last"):
        if not isinstance(training[name], bool):
            raise RuntimeError(f"objective_config.training.{name} must be bool")
    _require_sorted_unique_strings(
        training["training_variants"], "objective_config.training.training_variants"
    )
    for name in ("checkpoint_epochs", "checkpoint_dev_indices", "calibration_dev_indices"):
        values = _require_list(selection[name], f"objective_config.selection.{name}")
        if any(isinstance(item, bool) or not isinstance(item, int) for item in values):
            raise RuntimeError(f"objective_config.selection.{name} must contain integers")
    for name in ("temperature_grid", "abstention_threshold_grid"):
        values = _require_list(selection[name], f"objective_config.selection.{name}")
        for index, item in enumerate(values):
            _require_number(item, f"objective_config.selection.{name}[{index}]")
    _require_int(
        selection["test_evaluations"],
        "objective_config.selection.test_evaluations",
        minimum=1,
    )
    rows = _require_list(artifact["conditions"], "objective_config.conditions")
    if len(rows) != int(contract["condition_rows"]):
        raise RuntimeError("objective_config condition cardinality mismatch")
    for index, row in enumerate(rows):
        item = _require_exact_keys(
            row,
            contract["condition_row_fields"],
            f"objective_config.conditions[{index}]",
        )
        weights = _require_exact_keys(
            item["objective_weights"],
            protocol["artifacts"]["derived_contracts"]["loss_ablation_metrics.json"][
                "training_step_objective_keys"
            ],
            f"objective_config.conditions[{index}].objective_weights",
        )
        for objective, weight in weights.items():
            _require_number(
                weight, f"objective_config.conditions[{index}].objective_weights.{objective}"
            )
        _require_number(
            item["residual_retention"],
            f"objective_config.conditions[{index}].residual_retention",
        )
        for name in ("parameter_count", "optimizer_steps"):
            _require_int(
                item[name], f"objective_config.conditions[{index}].{name}", minimum=1
            )
    if [row["condition_id"] for row in rows] != sorted(protocol["conditions"]["order"]):
        raise RuntimeError("objective_config condition order is not canonical")


def _validate_loss_metrics(value: object, protocol: dict[str, Any]) -> None:
    contract = protocol["artifacts"]["derived_contracts"]["loss_ablation_metrics.json"]
    artifact = _require_exact_keys(
        value, contract["exact_top_level_fields"], "loss_ablation_metrics.json"
    )
    _require_finite_json(artifact, "loss_ablation_metrics.json")
    failed_seeds = _validate_failed_seeds(
        artifact["failed_seeds"], protocol, "loss.failed_seeds"
    )
    successful_seeds = _successful_model_seeds(protocol, failed_seeds)
    cardinality = protocol["failure_contract"]["successful_seed_cardinality"]
    if artifact["objective_order"] != contract["training_step_objective_keys"]:
        raise RuntimeError("loss objective order differs from protocol")
    step_rows = _require_list(artifact["training_step_rows"], "loss.training_step_rows")
    if len(step_rows) != len(successful_seeds) * int(
        cardinality["training_step_rows_per_seed"]
    ):
        raise RuntimeError("training step row cardinality mismatch")
    step_sort: list[tuple[object, ...]] = []
    for index, row in enumerate(step_rows):
        item = _require_exact_keys(
            row, contract["training_step_row_fields"], f"training_step_rows[{index}]"
        )
        if item["condition_id"] not in protocol["conditions"]["order"]:
            raise RuntimeError("training step condition is invalid")
        if item["model_seed"] not in protocol["seeds"]["model"]:
            raise RuntimeError("training step model seed is invalid")
        _require_int(item["epoch"], "training step epoch", minimum=1)
        _require_int(item["optimizer_step"], "training step optimizer_step", minimum=1)
        if not isinstance(item["episode_id"], str) or not item["episode_id"]:
            raise RuntimeError("training step episode_id must be non-empty")
        for name in (
            "total_loss",
            "pre_clip_total_gradient_l2",
            "post_clip_total_gradient_l2",
        ):
            _require_number(item[name], f"training step {name}")
        objectives = _require_exact_keys(
            item["objectives"],
            contract["training_step_objective_keys"],
            f"training_step_rows[{index}].objectives",
        )
        for objective_id, objective in objectives.items():
            term = _require_exact_keys(
                objective,
                contract["training_step_objective_fields"],
                f"training_step_rows[{index}].objectives.{objective_id}",
            )
            _require_int(term["eligible_count"], f"objective {objective_id} eligible_count")
            for name in (
                "raw_loss",
                "weight",
                "weighted_contribution",
                "unweighted_gradient_l2",
                "weighted_gradient_l2",
            ):
                _require_number(term[name], f"objective {objective_id} {name}")
            if term["weight"] == 0.0 and (
                term["weighted_contribution"] != 0.0 or term["weighted_gradient_l2"] != 0.0
            ):
                raise RuntimeError("zero-weight objective has nonzero weighted contribution")
        step_sort.append(tuple(item[name] for name in contract["training_step_sort"]))
    if step_sort != sorted(step_sort):
        raise RuntimeError("training step rows are not sorted")
    if len(step_sort) != len(set(step_sort)):
        raise RuntimeError("training step rows contain duplicate optimizer steps")
    expected_steps = {
        (condition, seed, optimizer_step)
        for condition in protocol["conditions"]["order"]
        for seed in successful_seeds
        for optimizer_step in range(1, int(protocol["objective_config"]["optimizer_steps"]) + 1)
    }
    if set(step_sort) != expected_steps:
        raise RuntimeError("training step rows do not cover the frozen optimizer-step grid")
    for container, per_seed, fields in (
        (
            "condition_seed_rows",
            "condition_seed_rows_per_seed",
            "condition_seed_row_fields",
        ),
        ("objective_rows", "objective_rows_per_seed", "objective_row_fields"),
    ):
        rows = _require_list(artifact[container], f"loss.{container}")
        if len(rows) != len(successful_seeds) * int(cardinality[per_seed]):
            raise RuntimeError(f"loss {container} cardinality mismatch")
        sort_keys: list[tuple[object, ...]] = []
        for index, row in enumerate(rows):
            item = _require_exact_keys(row, contract[fields], f"loss.{container}[{index}]")
            label = f"loss.{container}[{index}]"
            if container == "condition_seed_rows":
                _require_int(item["model_seed"], f"{label}.model_seed")
                _require_int(item["selected_epoch"], f"{label}.selected_epoch", minimum=1)
                for name in ("temperature", "abstention_threshold"):
                    _require_number(item[name], f"{label}.{name}")
                for name in ("optimizer_steps", "parameter_count"):
                    _require_int(item[name], f"{label}.{name}", minimum=1)
                for name in ("training_input_hash", "checkpoint_hash"):
                    _require_hash(item[name], f"{label}.{name}")
                if item["protocol_compliant"] is not True:
                    raise RuntimeError(f"{label}.protocol_compliant must be true")
                sort_keys.append((item["condition_id"], item["model_seed"]))
            else:
                _require_int(item["model_seed"], f"{label}.model_seed")
                _require_int(item["eligible_count"], f"{label}.eligible_count")
                for name in (
                    "mean_raw_loss",
                    "weight",
                    "mean_weighted_contribution",
                    "mean_unweighted_gradient_l2",
                    "mean_weighted_gradient_l2",
                ):
                    _require_number(item[name], f"{label}.{name}")
                if not isinstance(item["ablated"], bool):
                    raise RuntimeError(f"{label}.ablated must be bool")
                sort_keys.append(
                    (item["condition_id"], item["model_seed"], item["objective_id"])
                )
        if sort_keys != sorted(sort_keys) or len(sort_keys) != len(set(sort_keys)):
            raise RuntimeError(f"loss {container} order is not canonical")

    condition_seed_rows = artifact["condition_seed_rows"]
    objective_rows = artifact["objective_rows"]
    expected_condition_seeds = {
        (condition, seed)
        for condition in protocol["conditions"]["order"]
        for seed in successful_seeds
    }
    if {
        (row["condition_id"], row["model_seed"]) for row in condition_seed_rows
    } != expected_condition_seeds:
        raise RuntimeError("loss condition_seed_rows do not cover the frozen grid")
    expected_objectives = {
        (condition, seed, objective)
        for condition, seed in expected_condition_seeds
        for objective in contract["training_step_objective_keys"]
    }
    if {
        (row["condition_id"], row["model_seed"], row["objective_id"])
        for row in objective_rows
    } != expected_objectives:
        raise RuntimeError("loss objective_rows do not cover the frozen grid")
    if not isinstance(artifact["engineering_gates"], list):
        raise RuntimeError("engineering_gates must be a list")
    if not isinstance(artifact["scientific_gates"], dict):
        raise RuntimeError("scientific_gates must be an object")


def _validate_pareto(value: object, protocol: dict[str, Any]) -> None:
    contract = protocol["artifacts"]["derived_contracts"]["pareto_frontier.json"]
    artifact = _require_exact_keys(
        value, contract["exact_top_level_fields"], "pareto_frontier.json"
    )
    _require_finite_json(artifact, "pareto_frontier.json")
    failed_seeds = _validate_failed_seeds(
        artifact["failed_seeds"], protocol, "pareto.failed_seeds"
    )
    successful_seeds = _successful_model_seeds(protocol, failed_seeds)
    cardinality = protocol["failure_contract"]["successful_seed_cardinality"]
    if artifact["dimensions"] != protocol["pareto"]["dimensions"]:
        raise RuntimeError("Pareto dimensions differ from the frozen protocol")
    containers: dict[str, list[Any]] = {}
    for container, expected_count, fields in (
        (
            "seed_points",
            len(successful_seeds) * int(cardinality["pareto_seed_points_per_seed"]),
            "seed_point_fields",
        ),
        (
            "aggregate_points",
            int(cardinality["aggregate_points_when_any_seed_succeeds"])
            if successful_seeds
            else 0,
            "aggregate_point_fields",
        ),
        (
            "pairwise_dominance",
            int(cardinality["pairwise_rows_when_any_seed_succeeds"])
            if successful_seeds
            else 0,
            "pairwise_dominance_fields",
        ),
    ):
        rows = _require_list(artifact[container], f"pareto.{container}")
        containers[container] = rows
        if len(rows) != expected_count:
            raise RuntimeError(f"pareto {container} cardinality mismatch")
        for index, row in enumerate(rows):
            item = _require_exact_keys(
                row, contract[fields], f"pareto.{container}[{index}]"
            )
            if container in {"seed_points", "aggregate_points"}:
                metrics = _require_exact_keys(
                    item["metrics"],
                    contract["metrics_fields"],
                    f"pareto.{container}[{index}].metrics",
                )
                for metric, metric_value in metrics.items():
                    _require_number(
                        metric_value,
                        f"pareto.{container}[{index}].metrics.{metric}",
                        nullable=True,
                    )
                if container == "aggregate_points" and not isinstance(
                    item["nondominated"], bool
                ):
                    raise RuntimeError("Pareto nondominated flag must be bool")
            else:
                for name in ("left_dominates", "right_dominates"):
                    if not isinstance(item[name], bool):
                        raise RuntimeError(f"pareto pairwise {name} must be bool")
                if item["incomparable_reason"] not in {None, "null_metric"}:
                    raise RuntimeError("Pareto incomparable_reason is invalid")
    conditions = sorted(protocol["conditions"]["order"])
    seeds = successful_seeds
    expected_seed_order = [(condition, seed) for condition in conditions for seed in seeds]
    actual_seed_order = [
        (row["condition_id"], row["model_seed"]) for row in containers["seed_points"]
    ]
    if actual_seed_order != expected_seed_order:
        raise RuntimeError("Pareto seed point order is not canonical")
    expected_aggregate_order = conditions if seeds else []
    if [
        row["condition_id"] for row in containers["aggregate_points"]
    ] != expected_aggregate_order:
        raise RuntimeError("Pareto aggregate point order is not canonical")
    expected_pairs = [
        (left, right)
        for left_index, left in enumerate(conditions)
        for right in conditions[left_index + 1 :]
    ] if seeds else []
    actual_pairs = [
        (row["left_condition"], row["right_condition"])
        for row in containers["pairwise_dominance"]
    ]
    if actual_pairs != expected_pairs:
        raise RuntimeError("Pareto pairwise order is not canonical")
    dimensions = list(protocol["pareto"]["dimensions"])
    for point in containers["aggregate_points"]:
        expected_nondominated = not any(
            other is not point
            and _dominates(other["metrics"], point["metrics"], dimensions)
            for other in containers["aggregate_points"]
        )
        if point["nondominated"] is not expected_nondominated:
            raise RuntimeError("Pareto nondominated flag does not recalculate")
    by_condition = {
        row["condition_id"]: row["metrics"] for row in containers["aggregate_points"]
    }
    for pair in containers["pairwise_dominance"]:
        left = by_condition[pair["left_condition"]]
        right = by_condition[pair["right_condition"]]
        if pair["left_dominates"] is not _dominates(left, right, dimensions) or pair[
            "right_dominates"
        ] is not _dominates(right, left, dimensions):
            raise RuntimeError("Pareto pairwise dominance does not recalculate")
    support = _require_exact_keys(
        artifact["scientific_support"],
        contract["scientific_support_fields"],
        "pareto.scientific_support",
    )
    if failed_seeds and support != _failure_scientific_support(protocol):
        raise RuntimeError("Pareto failure scientific support differs from protocol")
    _require_exact_keys(
        support["variant_gates"],
        ("distractor_change", "same_id_change", "correlated_copy_change"),
        "pareto.variant_gates",
    )
    for name, raw_gate in support["variant_gates"].items():
        gate = _require_exact_keys(
            raw_gate,
            ("changed_pairs", "denominator", "rate", "maximum", "passed"),
            f"pareto.variant_gates.{name}",
        )
        _require_int(gate["changed_pairs"], f"pareto.variant_gates.{name}.changed_pairs")
        _require_int(gate["denominator"], f"pareto.variant_gates.{name}.denominator")
        _require_number(
            gate["rate"], f"pareto.variant_gates.{name}.rate", nullable=bool(failed_seeds)
        )
        _require_number(gate["maximum"], f"pareto.variant_gates.{name}.maximum")
        if not isinstance(gate["passed"], bool):
            raise RuntimeError(f"pareto.variant_gates.{name}.passed must be bool")
    residual = _require_exact_keys(
        support["residual_gate"],
        ("full_recovery_rate", "no_residual_recovery_rate", "passed"),
        "pareto.residual_gate",
    )
    for name in ("full_recovery_rate", "no_residual_recovery_rate"):
        _require_number(
            residual[name], f"pareto.residual_gate.{name}", nullable=True
        )
    if not isinstance(residual["passed"], bool):
        raise RuntimeError("pareto.residual_gate.passed must be bool")
    expected_residual = (
        residual["full_recovery_rate"] is not None
        and residual["no_residual_recovery_rate"] is not None
        and residual["full_recovery_rate"] > residual["no_residual_recovery_rate"]
    )
    if residual["passed"] is not expected_residual:
        raise RuntimeError("pareto residual gate does not recalculate")
    noninferiority = _require_exact_keys(
        support["weighted_ce_noninferiority"],
        (
            "unnecessary_revision_rate",
            "missed_revision_rate",
            "recovery_rate",
            "no_ignition_f1",
            "ece",
        ),
        "pareto.weighted_ce_noninferiority",
    )
    for name, raw_check in noninferiority.items():
        check = _require_exact_keys(
            raw_check,
            ("effect_full_minus_weighted_ce", "margin", "direction", "passed"),
            f"pareto.weighted_ce_noninferiority.{name}",
        )
        _require_number(
            check["effect_full_minus_weighted_ce"],
            f"pareto noninferiority {name} effect",
            nullable=True,
        )
        _require_number(check["margin"], f"pareto noninferiority {name} margin")
        if check["direction"] not in {"max_increase", "max_decrease"} or not isinstance(
            check["passed"], bool
        ):
            raise RuntimeError(f"pareto noninferiority {name} decision is invalid")
        effect = check["effect_full_minus_weighted_ce"]
        expected_pass = effect is not None and (
            effect <= check["margin"]
            if check["direction"] == "max_increase"
            else effect >= -check["margin"]
        )
        if check["passed"] is not expected_pass:
            raise RuntimeError(f"pareto noninferiority {name} does not recalculate")
    strict = _require_exact_keys(
        support["strict_improvement"],
        ("effects", "minimum", "passed"),
        "pareto.strict_improvement",
    )
    effects = _require_exact_keys(
        strict["effects"], tuple(noninferiority), "pareto.strict_improvement.effects"
    )
    for name, effect in effects.items():
        _require_number(
            effect,
            f"pareto.strict_improvement.effects.{name}",
            nullable=True,
        )
    _require_number(strict["minimum"], "pareto.strict_improvement.minimum")
    if not isinstance(strict["passed"], bool) or not isinstance(
        support["all_gates_passed"], bool
    ):
        raise RuntimeError("Pareto support pass flags must be bool")
    if strict["passed"] is not any(
        effect is not None and effect >= strict["minimum"] for effect in effects.values()
    ):
        raise RuntimeError("Pareto strict improvement does not recalculate")
    expected_all = (
        all(gate["passed"] for gate in support["variant_gates"].values())
        and residual["passed"]
        and all(check["passed"] for check in noninferiority.values())
        and strict["passed"]
    )
    if support["all_gates_passed"] is not expected_all:
        raise RuntimeError("Pareto all-gates decision does not recalculate")
    if support["status"] not in {
        "supported",
        "not_supported",
        protocol["failure_contract"]["failed_scientific_status"],
    }:
        raise RuntimeError("Pareto scientific support status is invalid")
    if not failed_seeds and support["status"] != (
        "supported" if expected_all else "not_supported"
    ):
        raise RuntimeError("Pareto scientific support status does not recalculate")
    _validate_bootstrap_intervals(
        support["bootstrap_intervals"], protocol=protocol, failed=bool(failed_seeds)
    )


def _validate_bootstrap_intervals(
    value: object, *, protocol: dict[str, Any], failed: bool
) -> None:
    expected_comparisons = protocol["determinism"]["bootstrap_algorithm"]["comparison_order"]
    intervals = _require_exact_keys(value, expected_comparisons, "pareto.bootstrap_intervals")
    for comparison, interval in intervals.items():
        item = _require_exact_keys(
            interval,
            (
                "effect", "lower", "upper", "resamples", "bootstrap_seed",
                "defined_resamples", "undefined_resamples",
            ),
            f"pareto.bootstrap_intervals.{comparison}",
        )
        for name in ("effect", "lower", "upper"):
            _require_number(item[name], f"pareto interval {comparison}.{name}", nullable=True)
        _require_int(item["resamples"], f"pareto interval {comparison}.resamples", minimum=1)
        _require_int(item["bootstrap_seed"], f"pareto interval {comparison}.bootstrap_seed")
        if item["resamples"] != protocol["determinism"]["bootstrap_resamples"] or item[
            "bootstrap_seed"
        ] != protocol["determinism"]["bootstrap_seed"]:
            raise RuntimeError(f"pareto interval {comparison} parameters differ from protocol")
        if failed:
            if any(item[name] is not None for name in (
                "effect", "lower", "upper", "defined_resamples", "undefined_resamples"
            )):
                raise RuntimeError(f"pareto interval {comparison} failure fields must be null")
            continue
        for name in ("defined_resamples", "undefined_resamples"):
            _require_int(item[name], f"pareto interval {comparison}.{name}")
        if item["defined_resamples"] + item["undefined_resamples"] != item["resamples"]:
            raise RuntimeError(f"pareto interval {comparison} counts do not sum to resamples")
        bounds_defined = item["undefined_resamples"] == 0 and item["effect"] is not None
        if bounds_defined:
            if item["lower"] is None or item["upper"] is None or item["lower"] > item["upper"]:
                raise RuntimeError(f"pareto interval {comparison} requires ordered finite bounds")
        elif item["lower"] is not None or item["upper"] is not None:
            raise RuntimeError(
                f"pareto interval {comparison} undefined effects require null bounds"
            )


def _validate_generated_artifacts(
    *,
    protocol: dict[str, Any],
    raw: list[dict[str, object]],
    objective_config: dict[str, object],
    confusion: dict[str, object],
    calibration: dict[str, object],
    loss_metrics: dict[str, object],
    pareto: dict[str, object],
) -> None:
    failed_seeds = _validate_failed_seeds(
        loss_metrics["failed_seeds"], protocol, "generated.failed_seeds"
    )
    successful_count = len(_successful_model_seeds(protocol, failed_seeds))
    cardinality = protocol["failure_contract"]["successful_seed_cardinality"]
    _validate_raw_rows(raw, protocol, failed_seeds)
    _validate_objective_config(objective_config, protocol)
    _validate_tabular_artifact(
        confusion, protocol=protocol, artifact_name="confusion_matrices.json"
    )
    _validate_tabular_artifact(
        calibration,
        protocol=protocol,
        artifact_name="calibration_by_input_track.json",
    )
    _validate_loss_metrics(loss_metrics, protocol)
    _validate_pareto(pareto, protocol)
    expected_seed_rows = successful_count * int(cardinality["confusion_seed_rows_per_seed"])
    expected_aggregate_rows = (
        int(cardinality["aggregate_rows_when_any_seed_succeeds"])
        if successful_count
        else 0
    )
    if (
        len(confusion["seed_rows"]) != expected_seed_rows
        or len(confusion["aggregate_rows"]) != expected_aggregate_rows
    ):
        raise RuntimeError("confusion strata are incomplete")
    if (
        len(calibration["seed_rows"]) != expected_seed_rows
        or len(calibration["aggregate_rows"]) != expected_aggregate_rows
    ):
        raise RuntimeError("calibration strata are incomplete")
    source_commit = str(objective_config["source_commit"])
    for artifact_name, artifact in (
        ("objective_config", objective_config),
        ("confusion", confusion),
        ("calibration", calibration),
        ("loss", loss_metrics),
        ("pareto", pareto),
    ):
        if artifact["schema_version"] != "0.3":
            raise RuntimeError(f"{artifact_name} schema_version is invalid")
        if artifact["protocol_id"] != protocol["protocol_id"]:
            raise RuntimeError(f"{artifact_name} protocol_id is invalid")
        if artifact["source_commit"] != source_commit:
            raise RuntimeError(f"{artifact_name} source_commit is inconsistent")
        if artifact["failed_seeds"] != failed_seeds:
            raise RuntimeError(f"{artifact_name} failed_seeds is inconsistent")

    expected_objective_config = _objective_config_artifact(
        loss_metrics["condition_seed_rows"],
        protocol=protocol,
        source_commit=source_commit,
        failed_seeds=failed_seeds,
    )
    if objective_config != expected_objective_config:
        raise RuntimeError("objective_config does not recalculate from retained condition rows")

    expected_confusion = _confusion_artifact(
        raw,
        protocol=protocol,
        source_commit=source_commit,
        failed_seeds=failed_seeds,
    )
    if confusion != expected_confusion:
        raise RuntimeError("confusion artifact does not exactly recalculate from raw rows")
    expected_calibration = _calibration_artifact(
        raw,
        protocol=protocol,
        source_commit=source_commit,
        failed_seeds=failed_seeds,
    )
    if calibration != expected_calibration:
        raise RuntimeError("calibration artifact does not exactly recalculate from raw rows")
    expected_objective_rows = _objective_rows(
        loss_metrics["training_step_rows"],
        protocol=protocol,
        successful_seeds=_successful_model_seeds(protocol, failed_seeds),
    )
    if loss_metrics["objective_rows"] != expected_objective_rows:
        raise RuntimeError("objective aggregates do not recalculate from training rows")
    expected_engineering_gates = _engineering_gates(
        raw,
        loss_metrics["training_step_rows"],
        expected_objective_rows,
        protocol=protocol,
        failed_seeds=failed_seeds,
    )
    if loss_metrics["engineering_gates"] != expected_engineering_gates:
        raise RuntimeError("engineering gates do not recalculate from retained raw rows")
    expected_pareto = _pareto_artifact(
        raw,
        protocol=protocol,
        source_commit=source_commit,
        failed_seeds=failed_seeds,
    )
    if pareto != expected_pareto:
        raise RuntimeError("Pareto artifact does not exactly recalculate from raw rows")
    if loss_metrics["scientific_gates"] != expected_pareto["scientific_support"]:
        raise RuntimeError("scientific gates do not recalculate from retained raw rows")


def _report_text(
    *,
    protocol: dict[str, Any],
    source_commit: str,
    engineering_status: str,
    scientific: str,
    failed_seeds: Sequence[Mapping[str, object]],
) -> str:
    return f"""# C15 Persistent revision objectives

Protocol: `{protocol["protocol_id"]}`
Run: `{protocol["run_id"]}`
Source commit: `{source_commit}`

## Engineering status

`{engineering_status}`

Failed seeds: `{_canonical(list(failed_seeds))}`

## Scientific status

`{scientific}`

## Methods

CPU-only frozen synthetic train/dev/test evaluation with separated objectives, checkpoint
selection before disjoint calibration, and one official test evaluation.

## Transition metrics

Exact maintain/update/recover/insufficient confusions and revision rates are retained in the
machine-readable artifacts.

## Calibration

Calibration remains grouped by input track and entity condition with explicit coverage.

## Objective ablations

All nine single-objective ablations and the matched one-weighted-CE baseline are retained.

## Pareto trade-offs

The frozen six-dimensional Pareto comparison and descriptive paired intervals are retained.

## Negative findings

Failed scientific gates remain visible and do not invalidate a separately passing engineering run.

## Claim boundary

This synthetic CPU result does not establish external generalization, autonomous entity discovery,
semantic understanding, biological fidelity, energy efficiency, or a higher scientific claim grade.

## Reproduction

Re-run the canonical source-pinned runner with a distinct `PYTHONHASHSEED` and require all eight
files to match byte-for-byte.
"""


def _generate(
    *,
    output: Path,
    protocol: dict[str, Any],
    protocol_bytes: bytes,
    source_commit: str,
) -> dict[str, object]:
    raw, objective_config, loss_metrics, failed_seeds = _run_training_and_evaluation(
        protocol=protocol,
        source_commit=source_commit,
    )
    confusion = _confusion_artifact(
        raw,
        protocol=protocol,
        source_commit=source_commit,
        failed_seeds=failed_seeds,
    )
    calibration = _calibration_artifact(
        raw,
        protocol=protocol,
        source_commit=source_commit,
        failed_seeds=failed_seeds,
    )
    pareto = _pareto_artifact(
        raw,
        protocol=protocol,
        source_commit=source_commit,
        failed_seeds=failed_seeds,
    )
    loss_metrics["scientific_gates"] = pareto["scientific_support"]
    _validate_generated_artifacts(
        protocol=protocol,
        raw=raw,
        objective_config=objective_config,
        confusion=confusion,
        calibration=calibration,
        loss_metrics=loss_metrics,
        pareto=pareto,
    )
    engineering_passed = not failed_seeds and all(
        row["passed"] for row in loss_metrics["engineering_gates"]
    )
    engineering_status = "pass" if engineering_passed else (
        "implementation_failure" if failed_seeds else "fail"
    )
    scientific = str(pareto["scientific_support"]["status"])
    output.mkdir(parents=True, exist_ok=True)
    (output / "protocol.json").write_bytes(protocol_bytes)
    _write_json(output / "objective_config.json", objective_config)
    _write_jsonl(output / "per_transition_predictions.jsonl", raw)
    _write_json(output / "confusion_matrices.json", confusion)
    _write_json(output / "calibration_by_input_track.json", calibration)
    _write_json(output / "loss_ablation_metrics.json", loss_metrics)
    _write_json(output / "pareto_frontier.json", pareto)
    (output / "report.md").write_text(
        _report_text(
            protocol=protocol,
            source_commit=source_commit,
            engineering_status=engineering_status,
            scientific=scientific,
            failed_seeds=failed_seeds,
        ),
        encoding="utf-8",
        newline="\n",
    )
    return {
        "engineering_passed": engineering_passed,
        "engineering_status": engineering_status,
        "scientific_status": scientific,
        "failed_seeds": failed_seeds,
    }


class C15WorkerError(RuntimeError):
    """Global worker failure; live workers keep their staging directory quarantined."""

    def __init__(self, message: str, *, worker_alive: bool = False) -> None:
        super().__init__(message)
        self.worker_alive = worker_alive


class C15RunTimeoutError(C15WorkerError):
    """The parent did not confirm worker exit within the preregistered budget."""


def _worker_alive(worker: BaseProcess) -> bool:
    try:
        return worker.is_alive()
    except (OSError, ValueError):
        # Failed process inspection is not evidence of termination.
        return True


def _stop_worker(worker: BaseProcess, *, grace_seconds: float) -> None:
    for stop in (worker.terminate, worker.kill):
        if not _worker_alive(worker):
            return
        try:
            stop()
        except (OSError, ValueError):
            pass
        try:
            worker.join(grace_seconds)
        except (OSError, ValueError):
            pass


def _wait_for_worker(
    worker: BaseProcess, *, deadline: float, grace_seconds: float
) -> None:
    try:
        worker.join(max(0.0, deadline - time.monotonic()))
    except (OSError, ValueError) as exc:
        _stop_worker(worker, grace_seconds=grace_seconds)
        raise C15WorkerError(
            "C15 worker exit could not be inspected", worker_alive=_worker_alive(worker)
        ) from exc
    confirmed_at = time.monotonic()
    if worker.exitcode is not None and confirmed_at <= deadline:
        return
    # A normal exit observed only after the deadline cannot authorize publication.
    _stop_worker(worker, grace_seconds=grace_seconds)
    raise C15RunTimeoutError(
        "C15RunTimeoutError: worker exit was not confirmed by the deadline",
        worker_alive=_worker_alive(worker),
    )


def _generation_worker(connection: Connection, arguments: dict[str, Any]) -> None:
    try:
        connection.send(_generate(**arguments))
    finally:
        connection.close()


def _generate_isolated(
    *, output: Path, protocol: dict[str, Any], protocol_bytes: bytes, source_commit: str
) -> dict[str, object]:
    context = multiprocessing.get_context("spawn")
    receiver, sender = context.Pipe(duplex=False)
    worker = context.Process(
        target=_generation_worker,
        args=(sender, {
            "output": output,
            "protocol": protocol,
            "protocol_bytes": protocol_bytes,
            "source_commit": source_commit,
        }),
        daemon=True,
    )
    grace = float(protocol["determinism"]["timeout_contract"]["termination_grace_seconds"])
    started = False
    timed_out = False
    try:
        deadline = time.monotonic() + float(
            protocol["determinism"]["official_run_timeout_seconds"]
        )
        worker.start()
        started = True
        sender.close()
        try:
            _wait_for_worker(worker, deadline=deadline, grace_seconds=grace)
        except C15RunTimeoutError:
            timed_out = True
            raise
        if worker.exitcode != 0:
            raise C15WorkerError(f"C15 worker failed with exit code {worker.exitcode}")
        if not receiver.poll():
            raise C15WorkerError("C15 worker exited without a result")
        try:
            result = receiver.recv()
        except EOFError as exc:
            raise C15WorkerError("C15 worker exited without a result") from exc
        if not isinstance(result, dict):
            raise C15WorkerError("C15 worker returned an invalid result")
        return result
    finally:
        sender.close()
        receiver.close()
        if started and _worker_alive(worker) and not timed_out:
            _stop_worker(worker, grace_seconds=grace)
        if started and _worker_alive(worker):
            # Do not let run() remove files a surviving worker can still write.
            error_type = C15RunTimeoutError if timed_out else C15WorkerError
            raise error_type(
                f"{error_type.__name__}: quarantined staging retained at {output.resolve()}",
                worker_alive=True,
            )
        worker.close()


def run(*, root: Path, protocol_path: Path, output: Path, source_commit: str) -> dict[str, object]:
    protocol, protocol_bytes, _protected, _fixture_hashes = _preflight(
        root=root,
        protocol_path=protocol_path,
        output=output,
        source_commit=source_commit,
    )
    if output.exists() and any(output.iterdir()):
        raise RuntimeError("output directory must be new or empty")
    output.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{output.name}.staging-", dir=output.parent))
    cleanup_allowed = True
    try:
        result = _generate_isolated(
            output=staging,
            protocol=protocol,
            protocol_bytes=protocol_bytes,
            source_commit=source_commit,
        )
        if (
            {path.name for path in staging.iterdir()} != EXPECTED_FILES
            or any(not path.is_file() for path in staging.iterdir())
        ):
            raise RuntimeError("C15 staging output is incomplete or contains extra files")
        if output.exists():
            output.rmdir()
        staging.replace(output)
        return result
    except C15WorkerError as exc:
        cleanup_allowed = not exc.worker_alive
        if exc.worker_alive:
            print(f"Quarantined C15 staging: {staging.resolve()}", file=sys.stderr)
        raise
    finally:
        if cleanup_allowed and staging.exists():
            shutil.rmtree(staging, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the frozen C15 revision evaluation")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    try:
        result = run(
            root=args.root.resolve(),
            protocol_path=args.protocol.resolve(),
            output=args.output.resolve(),
            source_commit=args.source_commit,
        )
    except C15RunTimeoutError as exc:
        print(str(exc), file=sys.stderr)
        if exc.worker_alive:
            # multiprocessing's atexit hook otherwise joins surviving children indefinitely.
            sys.stderr.flush()
            os._exit(124)
        return 124
    except C15WorkerError as exc:
        print(str(exc), file=sys.stderr)
        if exc.worker_alive:
            sys.stderr.flush()
            os._exit(1)
        return 1
    print(_canonical(result))
    return 0 if result["engineering_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
