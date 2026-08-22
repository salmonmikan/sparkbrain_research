from __future__ import annotations

import hashlib
import itertools
import json
import platform
import socket
import sys
from collections import Counter
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from statistics import mean
from typing import Any

from ..baselines.neural import configure_determinism
from ..tasks import Episode
from .adapters import (
    INTERNAL_LABELS,
    ChanceAdapter,
    ExternalStreamingAdapter,
    load_frozen_adapter_manifest,
    load_model_adapters,
    reject_test_fit,
    require_official_test_only,
)
from .belief_r import load_belief_r_episodes, load_belief_r_spec, verify_belief_r_cache
from .metrics import categorize_errors
from .schema import PredictionStep, RevisionTarget
from .symbolic import generate_symbolic_episode, template_group_splits
from .transforms import (
    TransformResult,
    correlated_source_variants,
    delay_decisive_correction,
    duplicate_same_id,
    inject_irrelevant_distractor,
    permute_order,
    restate_observation,
)

ROOT = Path(__file__).resolve().parents[3]
TRACK_C_TRANSFORMS = (
    "premise_permutation",
    "delayed_decisive_correction",
    "same_id_duplicate",
    "deterministic_restatement",
    "correlated_source",
    "irrelevant_distractor",
)


@contextmanager
def network_blocked() -> Iterator[None]:
    """Fail closed if an offline evaluation path attempts a network connection."""

    original_connect = socket.socket.connect
    original_connect_ex = socket.socket.connect_ex

    def blocked_connect(self: socket.socket, address: object) -> None:
        del self, address
        raise RuntimeError("network access is blocked during external evaluation")

    def blocked_connect_ex(self: socket.socket, address: object) -> int:
        del self, address
        raise RuntimeError("network access is blocked during external evaluation")

    socket.socket.connect = blocked_connect
    socket.socket.connect_ex = blocked_connect_ex
    try:
        yield
    finally:
        socket.socket.connect = original_connect
        socket.socket.connect_ex = original_connect_ex


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
        newline="\n",
    )


def _target(episode: Episode, index: int) -> RevisionTarget:
    step = episode.steps[index]
    object_id = sorted(step.target.belief_truth_by_object)[0]
    return RevisionTarget(
        truth=step.target.belief_truth_by_object[object_id],
        update_required=step.target.update_required,
        decision_justified=step.target.decision_justified_by_object[object_id],
        scenario_tags=step.target.scenario_tags,
        object_id=object_id,
    )


def _ece(rows: list[dict[str, Any]], *, bins: int = 10) -> float | None:
    decided = [row for row in rows if row["prediction"] is not None]
    if not decided:
        return None
    total = len(decided)
    value = 0.0
    for bin_index in range(bins):
        lower = bin_index / bins
        upper = (bin_index + 1) / bins
        bucket = [
            row
            for row in decided
            if lower <= row["confidence"] < upper
            or (bin_index == bins - 1 and row["confidence"] == 1.0)
        ]
        if bucket:
            accuracy = mean(float(row["correct"]) for row in bucket)
            confidence = mean(float(row["confidence"]) for row in bucket)
            value += len(bucket) / total * abs(accuracy - confidence)
    return value


def _brier(rows: list[dict[str, Any]], labels: tuple[str, ...]) -> float:
    return mean(
        sum(
            (float(row["probabilities"].get(label, 0.0)) - float(label == row["truth"])) ** 2
            for label in labels
        )
        for row in rows
    )


def _belief_r_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    initial = [row for row in rows if row["step_index"] == 0]
    final = [row for row in rows if row["step_index"] == 1]
    updates = [row for row in final if row["update_required"]]
    maintains = [row for row in final if not row["update_required"]]
    by_pair = {row["episode_id"]: row for row in initial}
    changes = [
        row
        for row in final
        if row["prediction"] != by_pair[row["episode_id"]]["prediction"]
    ]
    initially_correct = [row for row in final if by_pair[row["episode_id"]]["correct"]]
    correct_changes = sum(row["correct"] for row in changes)
    retained_correct = sum(
        row["correct"]
        and row["prediction"] == by_pair[row["episode_id"]]["prediction"]
        for row in maintains
    )
    bu = mean(float(row["correct"]) for row in updates) if updates else None
    bm = mean(float(row["correct"]) for row in maintains) if maintains else None
    decided = [row for row in rows if row["prediction"] is not None]
    final_decided = [row for row in final if row["prediction"] is not None]
    return {
        "episodes": len(final),
        "basic_t_accuracy": mean(float(row["correct"]) for row in initial),
        "bu_accuracy": bu,
        "bm_accuracy": bm,
        "breu": (bu + bm) / 2.0 if bu is not None and bm is not None else None,
        "final_accuracy": mean(float(row["correct"]) for row in final),
        "accuracy_when_decided": mean(float(row["correct"]) for row in decided)
        if decided
        else None,
        "coverage_all_steps": len(decided) / len(rows),
        "coverage_final": len(final_decided) / len(final),
        "unconditional_revision_rate": len(changes) / len(final),
        "revision_precision": correct_changes / len(changes) if changes else None,
        "revision_recall": bu,
        "no_update_retention_accuracy": retained_correct / len(maintains)
        if maintains
        else None,
        "false_revision_rate": sum(
            row["prediction"] != by_pair[row["episode_id"]]["prediction"]
            for row in maintains
        )
        / len(maintains)
        if maintains
        else None,
        "mean_switch_latency_steps": 0.0
        if any(row["correct"] for row in updates)
        else None,
        "conditional_revision_rate_update": sum(
            row["prediction"] != by_pair[row["episode_id"]]["prediction"] for row in updates
        )
        / len(updates)
        if updates
        else None,
        "conditional_revision_rate_maintain": sum(
            row["prediction"] != by_pair[row["episode_id"]]["prediction"] for row in maintains
        )
        / len(maintains)
        if maintains
        else None,
        "final_accuracy_given_initially_correct": mean(
            float(row["correct"]) for row in initially_correct
        )
        if initially_correct
        else None,
        "brier_score": _brier(rows, ("a", "b", "c")),
        "ece_10_bin": _ece(rows),
        "attribution_fidelity": None,
        "attribution_status": "not_available",
    }


def _evaluate_belief_r_condition(
    condition: str,
    adapter: ExternalStreamingAdapter | None,
    episodes: list[Episode],
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, int]]:
    rows: list[dict[str, Any]] = []
    errors: Counter[str] = Counter()
    for episode in episodes:
        predictions: list[PredictionStep] = []
        targets: list[RevisionTarget] = []
        if adapter is not None:
            adapter.reset()
        for index, step in enumerate(episode.steps):
            target = _target(episode, index)
            if adapter is None:
                prediction = PredictionStep(target.truth, 1.0, (), object_id=target.object_id)
                probabilities = {
                    label: float(label == target.truth) for label in ("a", "b", "c")
                }
            else:
                prediction = adapter.step(step.observation)
                probabilities = adapter.probabilities()
            predictions.append(prediction)
            targets.append(target)
            rows.append(
                {
                    "condition": condition,
                    "episode_id": episode.episode_id,
                    "step_index": index,
                    "target_choice_id": target.truth,
                    "prediction": prediction.prediction,
                    "confidence": prediction.confidence,
                    "probabilities": probabilities,
                    "update_required": target.update_required,
                    "correct": prediction.prediction == target.truth,
                    "attribution_available": False,
                    "cited_evidence_ids": [],
                }
            )
        for labels in categorize_errors(tuple(predictions), tuple(targets)):
            errors.update(labels)
    metric_rows = [
        {
            **row,
            "truth": row["target_choice_id"],
        }
        for row in rows
    ]
    return rows, _belief_r_summary(metric_rows), dict(sorted(errors.items()))


def _track_b_episodes(config: dict[str, Any]) -> dict[str, list[Episode]]:
    split_seed = int(config["split_seed"])
    groups = template_group_splits(seed=split_seed)
    result: dict[str, list[Episode]] = {}
    for split in ("train", "dev", "test"):
        episodes: list[Episode] = []
        start = int(config[f"{split}_seed_start"])
        count = int(config["episodes_per_group"])
        for group in groups[split]:
            for offset in range(count):
                episodes.append(
                    generate_symbolic_episode(
                        group, seed=start + offset, split=split, split_seed=split_seed
                    )
                )
        result[split] = episodes
    return result


def _select_track_b_map(
    adapter: ExternalStreamingAdapter, dev: list[Episode]
) -> dict[str, str]:
    reject_test_fit(dev, purpose="Track B output-map selection")
    raw: list[tuple[str | None, str]] = []
    for episode in dev:
        adapter.reset()
        for index, step in enumerate(episode.steps):
            prediction = adapter.step(step.observation)
            raw.append((prediction.prediction, _target(episode, index).truth))
    candidates = []
    for permutation in itertools.permutations(("true", "false", "unknown")):
        mapping = dict(zip(INTERNAL_LABELS, permutation, strict=True))
        correct = sum(mapping.get(prediction) == truth for prediction, truth in raw)
        candidates.append((correct, permutation, mapping))
    return max(candidates, key=lambda row: (row[0], tuple(reversed(row[1]))))[2]


def _evaluate_track_b(
    manifest_path: Path,
    *,
    root: Path,
    config: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    episodes = _track_b_episodes(config)
    reject_test_fit(episodes["train"], purpose="Track B train materialization")
    reject_test_fit(episodes["dev"], purpose="Track B output-map selection")
    identity = dict(zip(INTERNAL_LABELS, INTERNAL_LABELS, strict=True))
    adapters = load_model_adapters(manifest_path, root=root, output_map=identity)
    mappings: dict[str, dict[str, str]] = {}
    for condition, adapter in adapters.items():
        mapping = _select_track_b_map(adapter, episodes["dev"])
        adapter.output_map = mapping  # type: ignore[attr-defined]
        mappings[condition] = mapping
    adapters["chance"] = ChanceAdapter(("true", "false", "unknown"))
    rows: list[dict[str, Any]] = []
    summaries: dict[str, Any] = {}
    for condition in ("direct", "explicit", "spark", "chance", "oracle"):
        adapter = adapters.get(condition)
        condition_rows: list[dict[str, Any]] = []
        for episode in episodes["test"]:
            if adapter is not None:
                adapter.reset()
            for index, step in enumerate(episode.steps):
                target = _target(episode, index)
                prediction = (
                    PredictionStep(target.truth, 1.0, (), object_id=target.object_id)
                    if adapter is None
                    else adapter.step(step.observation)
                )
                row = {
                    "condition": condition,
                    "episode_id": episode.episode_id,
                    "template_group": step.observation.metadata["template_group"],
                    "pattern": target.scenario_tags[1],
                    "step_index": index,
                    "truth_state_id": target.truth,
                    "prediction": prediction.prediction,
                    "confidence": prediction.confidence,
                    "update_required": target.update_required,
                    "correct": prediction.prediction == target.truth,
                }
                rows.append(row)
                condition_rows.append(row)
        decided = [row for row in condition_rows if row["prediction"] is not None]
        contradiction = [row for row in condition_rows if row["pattern"] == "contradiction"]
        summaries[condition] = {
            "steps": len(condition_rows),
            "accuracy": mean(float(row["correct"]) for row in condition_rows),
            "coverage": len(decided) / len(condition_rows),
            "unsupported_both_steps": sum(
                row["truth_state_id"] == "both" for row in condition_rows
            ),
            "contradiction_sensitivity": mean(
                float(row["correct"]) for row in contradiction
            )
            if contradiction
            else None,
            "output_map_selected_on_dev": mappings.get(condition),
            "attribution_fidelity": None,
            "attribution_status": "not_available",
        }
    split_groups = template_group_splits(seed=int(config["split_seed"]))
    split_manifest = {
        "split_seed": int(config["split_seed"]),
        "episodes_per_group": int(config["episodes_per_group"]),
        "groups": split_groups,
        "episode_ids": {
            split: [episode.episode_id for episode in values]
            for split, values in episodes.items()
        },
        "episode_hashes": {
            split: hashlib.sha256(
                "\n".join(episode.canonical_json() for episode in values).encode()
            ).hexdigest()
            for split, values in episodes.items()
        },
        "train_usage": "materialized and disjoint; pretrained C04/C05 weights are not refit",
        "dev_usage": "output label permutation only; no official Belief-R examples",
        "test_usage": "metrics only",
    }
    return {"split_manifest": split_manifest, "conditions": summaries}, rows


def _track_c_transform(name: str, episode: Episode) -> TransformResult:
    observations = tuple(step.observation for step in episode.steps)
    if name == "premise_permutation":
        return permute_order(observations, seed=episode.seed)
    if name == "delayed_decisive_correction":
        return delay_decisive_correction(observations, source_index=1, delay_steps=3)
    if name == "same_id_duplicate":
        return duplicate_same_id(observations, source_index=1)
    if name == "deterministic_restatement":
        return restate_observation(observations, source_index=1)
    if name == "correlated_source":
        return correlated_source_variants(observations, source_index=1, count=2)
    if name == "irrelevant_distractor":
        return inject_irrelevant_distractor(observations, after_index=0, seed=episode.seed)
    raise ValueError(f"Unknown Track C transform: {name}")


def _final_prediction(
    adapter: ExternalStreamingAdapter | None,
    observations: tuple[Any, ...],
    *,
    oracle_truth: str,
) -> str | None:
    if adapter is None:
        return oracle_truth
    adapter.reset()
    prediction: str | None = None
    for observation in observations:
        prediction = adapter.step(observation).prediction
    return prediction


def _evaluate_track_c_and_interventions(
    manifest_path: Path,
    *,
    root: Path,
    episodes: list[Episode],
    original_rows: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    output_map = {"cat": "a", "dog": "b", "toy": "c"}
    adapters = load_model_adapters(manifest_path, root=root, output_map=output_map)
    adapters["chance"] = ChanceAdapter(("a", "b", "c"))
    original = {
        (row["condition"], row["episode_id"]): row["prediction"]
        for row in original_rows
        if row["step_index"] == 1
    }
    track_c: dict[str, Any] = {}
    interventions: dict[str, Any] = {}
    for condition in ("direct", "explicit", "spark", "chance", "oracle"):
        adapter = adapters.get(condition)
        per_transform: dict[str, Any] = {}
        original_accuracy = mean(
            float(row["correct"])
            for row in original_rows
            if row["condition"] == condition and row["step_index"] == 1
        )
        for transform_name in TRACK_C_TRANSFORMS:
            predictions = []
            for episode in episodes:
                truth = _target(episode, 1).truth
                transformed = _track_c_transform(transform_name, episode)
                prediction = _final_prediction(
                    adapter, transformed.observations, oracle_truth=truth
                )
                predictions.append((episode.episode_id, prediction, truth))
            transformed_accuracy = mean(
                float(prediction == truth) for _, prediction, truth in predictions
            )
            per_transform[transform_name] = {
                "episodes": len(predictions),
                "final_accuracy": transformed_accuracy,
                "final_accuracy_delta_from_original": original_accuracy
                - transformed_accuracy,
                "context_length_degradation": original_accuracy - transformed_accuracy
                if transform_name
                in {"same_id_duplicate", "correlated_source", "irrelevant_distractor"}
                else None,
                "coverage": mean(float(prediction is not None) for _, prediction, _ in predictions),
                "prediction_change_from_original": mean(
                    float(prediction != original[(condition, episode_id)])
                    for episode_id, prediction, _ in predictions
                ),
            }
        track_c[condition] = per_transform

        causal_delta = []
        remove_delta = []
        duplicate_delta = []
        irrelevant_delta = []
        for episode in episodes:
            observations = tuple(step.observation for step in episode.steps)
            truth = _target(episode, 1).truth
            base = original[(condition, episode.episode_id)]
            initial = _final_prediction(
                adapter,
                observations[:1],
                oracle_truth=_target(episode, 0).truth,
            )
            removed = _final_prediction(adapter, observations[:1], oracle_truth=truth)
            duplicated = _final_prediction(
                adapter,
                duplicate_same_id(observations, source_index=1).observations,
                oracle_truth=truth,
            )
            irrelevant = _final_prediction(
                adapter,
                inject_irrelevant_distractor(
                    observations, after_index=0, seed=episode.seed
                ).observations,
                oracle_truth=truth,
            )
            causal_delta.append(base != initial)
            remove_delta.append(base != removed)
            duplicate_delta.append(base != duplicated)
            irrelevant_delta.append(base != irrelevant)
        interventions[condition] = {
            "episodes": len(episodes),
            "causal_delta_t_to_t1": mean(map(float, causal_delta)),
            "remove_decisive_change_rate": mean(map(float, remove_delta)),
            "same_id_duplicate_change_rate": mean(map(float, duplicate_delta)),
            "irrelevant_distractor_change_rate": mean(map(float, irrelevant_delta)),
            "entity_cross_talk_rate": mean(map(float, irrelevant_delta)),
            "attribution_fidelity": None,
            "attribution_status": "not_available",
        }
    return track_c, interventions


def _leakage_audit(episodes: list[Episode], adapter_manifest: dict[str, Any]) -> dict[str, Any]:
    official_hashes = {
        hashlib.sha256(step.observation.evidence_label.encode()).hexdigest()
        for episode in episodes
        for step in episode.steps
    }
    c02_labels = {
        token.removeprefix("evidence:")
        for token in adapter_manifest["c05"]["encoder"]["ordered_vocabulary"]
        if token.startswith("evidence:")
    }
    c02_hashes = {hashlib.sha256(label.encode()).hexdigest() for label in c02_labels}
    overlap = sorted(official_hashes & c02_hashes)
    return {
        "method": "exact SHA-256 comparison after frozen adapters were selected",
        "official_observation_count": sum(len(episode.steps) for episode in episodes),
        "official_unique_observation_hashes": len(official_hashes),
        "c02_dev_fitted_evidence_label_hashes": len(c02_hashes),
        "exact_overlap_count": len(overlap),
        "exact_overlap_sha256": overlap,
        "selection_effect": "none; audit is evaluator-side after adapter freeze",
        "scope_limit": (
            "Exact string overlap only; it does not establish semantic independence or "
            "absence from unrelated pretraining corpora"
        ),
    }


def run_external_evaluation(
    config_path: Path,
    *,
    output_override: Path | None = None,
    root: Path = ROOT,
) -> dict[str, Any]:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if config.get("schema_version") != "0.2" or config.get("offline_required") is not True:
        raise ValueError("C06 evaluation requires schema 0.2 and offline_required=true")
    if tuple(config.get("track_c", {}).get("transforms", ())) != TRACK_C_TRANSFORMS:
        raise ValueError("C06 final config must declare the frozen six-transform Track C matrix")
    output = output_override or root / config["output_dir"]
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"Output directory is not empty: {output}")
    output.mkdir(parents=True, exist_ok=True)
    spec_path = root / config["belief_r_spec"]
    cache_path = root / config["belief_r_cache"]
    adapter_manifest_path = root / config["adapter_manifest"]

    with network_blocked():
        determinism = configure_determinism(101, threads=1)
        spec = load_belief_r_spec(spec_path)
        verification = verify_belief_r_cache(cache_path, spec)
        manifest = load_frozen_adapter_manifest(adapter_manifest_path, root=root)
        episodes = list(load_belief_r_episodes(cache_path, spec))
        require_official_test_only(episodes, revision=spec.revision)
        output_map = dict(manifest["fixed_output_maps"]["belief_r"])
        adapters = load_model_adapters(adapter_manifest_path, root=root, output_map=output_map)
        adapters["chance"] = ChanceAdapter(("a", "b", "c"))
        all_rows: list[dict[str, Any]] = []
        summaries: dict[str, Any] = {}
        error_counts: dict[str, Any] = {}
        for condition in ("direct", "explicit", "spark", "chance", "oracle"):
            rows, summary, errors = _evaluate_belief_r_condition(
                condition, adapters.get(condition), episodes
            )
            all_rows.extend(rows)
            summaries[condition] = summary
            error_counts[condition] = errors
        track_b, track_b_rows = _evaluate_track_b(
            adapter_manifest_path,
            root=root,
            config=dict(config["track_b"]),
        )
        track_c, interventions = _evaluate_track_c_and_interventions(
            adapter_manifest_path,
            root=root,
            episodes=episodes,
            original_rows=all_rows,
        )
        leakage_audit = _leakage_audit(episodes, manifest)

    run_manifest = {
        "schema_version": "0.2",
        "run_id": config["run_id"],
        "config": str(config_path.relative_to(root)).replace("\\", "/")
        if config_path.is_relative_to(root)
        else str(config_path),
        "config_sha256": _sha256(config_path),
        "completed": True,
        "offline_network_blocked": True,
        "belief_r_role": "official_test_only_zero_shot",
        "belief_r_fit_or_tuning": False,
        "belief_r_revision": spec.revision,
        "belief_r_cache_sha256": verification.sha256,
        "belief_r_rows": verification.row_count,
        "belief_r_pairs": verification.pair_count,
        "adapter_manifest": config["adapter_manifest"],
        "adapter_manifest_sha256": _sha256(adapter_manifest_path),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "determinism": determinism,
        "information_conditions": {
            "direct": "C05 causal Transformer; observation-only; frozen seed 101",
            "explicit": "C05 explicit-state memory; observation-only; frozen seed 101",
            "spark": "C04 learned sparse-rate checkpoint; observation-only; frozen seed 41",
            "chance": "uniform three-choice bound; no target or semantic features",
            "oracle": (
                "evaluator-only target-visible upper bound; excluded from matched conclusions"
            ),
        },
        "fairness": {
            "same_official_examples": True,
            "same_observation_objects_at_adapter_api": True,
            "same_effective_features": False,
            "same_context_steps_track_a": 2,
            "same_example_budget": True,
            "tokenizer_matched": False,
            "parameter_matched": False,
            "compute_matched": False,
            "reason": (
                "C04 hashes raw evidence text while C05 uses its frozen dev-fitted feature "
                "vocabulary and maps unseen external categorical tokens to UNK while retaining "
                "strength/timing; C05's reduced run also failed scientific compute matching"
            ),
        },
        "artifact_content_policy": (
            "IDs, hashes, metrics, probabilities, and predictions only; no official text"
        ),
    }
    _write_json(output / "run_manifest.json", run_manifest)
    _write_json(output / "belief_r_metrics.json", summaries)
    _write_json(output / "error_counts.json", error_counts)
    _write_json(output / "track_b.json", track_b)
    _write_json(output / "track_c.json", track_c)
    _write_json(output / "interventions.json", interventions)
    _write_json(output / "leakage_audit.json", leakage_audit)
    _write_jsonl(output / "belief_r_predictions.jsonl", all_rows)
    _write_jsonl(output / "track_b_predictions.jsonl", track_b_rows)
    return {
        "run_manifest": run_manifest,
        "belief_r_metrics": summaries,
        "error_counts": error_counts,
        "track_b": track_b,
        "track_c": track_c,
        "interventions": interventions,
        "leakage_audit": leakage_audit,
    }
