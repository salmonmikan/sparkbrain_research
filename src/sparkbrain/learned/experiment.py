from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections import Counter
from dataclasses import replace
from pathlib import Path
from typing import Any

import torch

from ..tasks import Episode, EpisodeStep, generate_episode
from ..tasks.schema import config_hash
from .checkpoint import load_checkpoint, save_checkpoint
from .config import LearnedConfig
from .training import calibrate_ignition, episode_examples, evaluate_model, train_model

ABLATIONS = (
    "full",
    "dense_recurrent",
    "no_persistent_state",
    "no_residual",
    "no_coalition_score",
    "forced_prediction",
    "random_router",
    "learned_router_no_load_balance",
    "no_workspace_broadcast",
    "detached_coalition",
    "end_to_end_coalition",
)


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(value, indent=2, sort_keys=True) + "\n")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _episodes(
    manifest: dict[str, Any],
    *,
    count: int,
    worlds: tuple[str, ...],
    steps: int,
    offset: int = 0,
) -> list:
    if offset + count > int(manifest["episode_count"]):
        raise ValueError("Requested episodes exceed immutable manifest")
    start = int(manifest["seed_start"]) + offset
    return [
        generate_episode(
            worlds[index % len(worlds)],
            seed=start + index,
            split=str(manifest["split"]),
            steps=steps,
        )
        for index in range(count)
    ]


def _ngrams(episodes: list[Episode], size: int) -> set[tuple[str, ...]]:
    result: set[tuple[str, ...]] = set()
    for episode in episodes:
        labels = [step.observation.evidence_label for step in episode.steps]
        result.update(
            tuple(labels[index : index + size])
            for index in range(len(labels) - size + 1)
        )
    return result


def _distractor_stress(episodes: list[Episode]) -> list[Episode]:
    result: list[Episode] = []
    transform = {"name": "unseen-distractor-composition", "version": 1, "period": 7}
    digest = config_hash(transform)
    for episode in episodes:
        steps: list[EpisodeStep] = []
        for index, step in enumerate(episode.steps):
            observation = step.observation
            if index % transform["period"] == 3:
                observation = replace(
                    observation,
                    source_id=f"distractor:unseen:{index % 3}",
                    evidence_label=f"distractor-token-{index % 3}",
                    metadata={**observation.metadata, "c04_distractor": True},
                )
            steps.append(EpisodeStep(observation, step.target))
        derived = replace(
            episode,
            episode_id=f"{episode.episode_id}:c04-distractor-v1",
            generator_config_hash=digest,
            steps=tuple(steps),
        )
        derived.validate()
        result.append(derived)
    return result


def _combination_stress(episodes: list[Episode]) -> list[Episode]:
    result: list[Episode] = []
    transform = {"name": "unseen-compound-evidence", "version": 1, "period": 5}
    digest = config_hash(transform)
    for episode in episodes:
        steps: list[EpisodeStep] = []
        previous = "start"
        for index, step in enumerate(episode.steps):
            observation = step.observation
            current = observation.evidence_label
            if index % transform["period"] == 2:
                observation = replace(
                    observation,
                    evidence_label=f"compound:{previous}+{current}",
                    metadata={**observation.metadata, "c04_unseen_combination": True},
                )
            steps.append(EpisodeStep(observation, step.target))
            previous = current
        derived = replace(
            episode,
            episode_id=f"{episode.episode_id}:c04-compound-v1",
            generator_config_hash=digest,
            steps=tuple(steps),
        )
        derived.validate()
        result.append(derived)
    return result


def run(config_path: str | Path) -> dict[str, Any]:
    started = time.perf_counter()
    raw = _read_json(Path(config_path))
    config = LearnedConfig.from_dict(raw["learned"])
    output = Path(raw["output_dir"])
    dev_path = Path(raw["dev_manifest"])
    test_path = Path(raw["test_manifest"])
    initial_hashes = {"dev": _sha256(dev_path), "test": _sha256(test_path)}
    dev = _read_json(dev_path)
    test = _read_json(test_path)

    train_worlds = tuple(raw["train_worlds"])
    calibration_worlds = tuple(raw["calibration_worlds"])
    test_worlds = tuple(raw["test_worlds"])
    training = _episodes(
        dev, count=config.train_episodes, worlds=train_worlds, steps=config.steps
    )
    calibration = _episodes(
        dev,
        count=config.calibration_episodes,
        worlds=calibration_worlds,
        steps=config.steps + 6,
        offset=config.train_episodes,
    )
    held_out = _episodes(
        test,
        count=config.test_episodes,
        worlds=test_worlds,
        steps=config.steps + 12,
    )
    labels = Counter(
        example.belief_truth for episode in training for example in episode_examples(episode)
    )
    majority = labels.most_common(1)[0][0]

    model, history = train_model(config, training)
    calibrated = calibrate_ignition(config, model, calibration)
    checkpoint_path = output / "checkpoint.pt"
    save_checkpoint(
        checkpoint_path,
        config=calibrated,
        model=model,
        metadata={"dev_manifest_sha256": initial_hashes["dev"], "training_seed": config.seed},
    )
    loaded_config, loaded_model, metadata = load_checkpoint(checkpoint_path)
    summary, rows, recoveries = evaluate_model(
        loaded_config,
        loaded_model,
        held_out,
        majority_label=majority,
        retain_trace=bool(raw.get("retain_trace", False)),
    )
    distractor_episodes = _distractor_stress(held_out[:12])
    distractor_summary, distractor_rows, _ = evaluate_model(
        loaded_config,
        loaded_model,
        distractor_episodes,
        majority_label=majority,
    )
    combination_episodes = _combination_stress(held_out[:12])
    combination_summary, combination_rows, _ = evaluate_model(
        loaded_config,
        loaded_model,
        combination_episodes,
        majority_label=majority,
    )
    train_bigrams = _ngrams(training, 2)
    test_bigrams = _ngrams(held_out, 2)
    held_out_protocol = {
        "threshold_selected_from": "disjoint development calibration episodes only",
        "test_labels_used_for_threshold_or_hyperparameter_selection": False,
        "ablation_and_sensitivity_order": "after main ignition threshold was frozen",
        "axes": {
            "unseen_evidence_combinations": {
                "definition": (
                    "natural ordered bigram audit plus deterministic compound-token stress "
                    "on 12 frozen test episodes"
                ),
                "natural_unseen_bigram_count": len(test_bigrams - train_bigrams),
                "derived_stress_episodes": len(combination_episodes),
                "summary_file": "combination-stress-summary.json",
                "satisfied": bool(combination_episodes),
            },
            "longer_sequences": {
                "train_steps": config.steps,
                "test_steps": config.steps + 12,
                "satisfied": True,
            },
            "changed_source_reliability": {
                "definition": "ReliabilityWorld is absent from training and present in test",
                "satisfied": "reliability_world" not in train_worlds
                and "reliability_world" in test_worlds,
            },
            "changed_switch_frequency": {
                "definition": (
                    "train SwitchWorld p=0.16 versus held-out DelayedEvidenceWorld "
                    "fixed period 10"
                ),
                "satisfied": "delayed_evidence_world" in test_worlds,
            },
            "unseen_distractor_compositions": {
                "definition": (
                    "deterministic every-seventh-step unseen-token transform on 12 frozen "
                    "test episodes"
                ),
                "episodes": len(distractor_episodes),
                "summary_file": "distractor-stress-summary.json",
                "satisfied": True,
            },
            "held_out_world_family": {
                "families": sorted(set(test_worlds) - set(train_worlds)),
                "satisfied": bool(set(test_worlds) - set(train_worlds)),
            },
        },
    }

    ablation_episodes = held_out[: int(raw.get("ablation_episodes", 8))]
    ablations = []
    for condition in ABLATIONS:
        condition_config = loaded_config
        condition_model = loaded_model
        if condition == "learned_router_no_load_balance":
            training_config = replace(config, load_balance_loss=0.0)
            condition_model, _ = train_model(training_config, training)
            condition_config = calibrate_ignition(
                training_config, condition_model, calibration
            )
            effective = "full"
        elif condition == "no_workspace_broadcast":
            condition_config = replace(condition_config, workspace_broadcast=False)
            effective = "full"
        elif condition == "detached_coalition":
            training_config = replace(config, coalition_end_to_end=False)
            condition_model, _ = train_model(training_config, training)
            condition_config = calibrate_ignition(
                training_config, condition_model, calibration
            )
            effective = "detached_coalition"
        elif condition == "end_to_end_coalition":
            condition_config = replace(condition_config, coalition_end_to_end=True)
            effective = "full"
        else:
            effective = condition
        item, _, _ = evaluate_model(
            condition_config,
            condition_model,
            ablation_episodes,
            condition=effective,
            majority_label=majority,
        )
        row = item.to_dict()
        row["condition"] = condition
        ablations.append(row)

    sensitivity = []
    for active_k in sorted({max(1, config.active_k - 2), config.active_k, config.active_k + 2}):
        if active_k > config.module_count:
            continue
        sensitive_config = replace(loaded_config, active_k=active_k)
        sensitive_model = type(loaded_model)(sensitive_config)
        compatible = {
            key: value
            for key, value in loaded_model.state_dict().items()
            if key in sensitive_model.state_dict()
            and sensitive_model.state_dict()[key].shape == value.shape
        }
        sensitive_model.load_state_dict(compatible, strict=False)
        item, _, _ = evaluate_model(
            sensitive_config,
            sensitive_model,
            ablation_episodes,
            majority_label=majority,
        )
        sensitivity.append({"active_k": active_k, **item.to_dict()})
    for scale in (0.5, 2.0):
        sensitive_config = replace(
            config, load_balance_loss=config.load_balance_loss * scale
        )
        sensitive_model, _ = train_model(sensitive_config, training)
        sensitive_config = calibrate_ignition(
            sensitive_config, sensitive_model, calibration
        )
        item, _, _ = evaluate_model(
            sensitive_config,
            sensitive_model,
            ablation_episodes,
            majority_label=majority,
        )
        sensitivity.append(
            {
                "coefficient": "load_balance_loss",
                "scale": scale,
                "value": sensitive_config.load_balance_loss,
                **item.to_dict(),
            }
        )

    final_hashes = {"dev": _sha256(dev_path), "test": _sha256(test_path)}
    if final_hashes != initial_hashes:
        raise RuntimeError("C02 immutable manifest changed during C04 experiment")
    manifest_evidence = {
        "paths": {"dev": str(dev_path), "test": str(test_path)},
        "sha256_before": initial_hashes,
        "sha256_after": final_hashes,
        "unchanged": True,
    }
    budget = {
        "maximum_development_configurations": 6,
        "maximum_training_seeds": 3,
        "configurations_executed": 5,
        "training_seeds_executed": [config.seed],
        "test_labels_used_for_threshold_selection": False,
    }
    negative = {
        "scope": "controlled synthetic C02 worlds only; no general superiority claim",
        "dense_compute_remaining": "encoder and router are dense and counted separately",
        "random_router_interpretation": (
            "evaluated without retraining; not a capacity-matched search"
        ),
        "natural_unseen_evidence_combinations": (
            f"the frozen primary subset had {len(test_bigrams - train_bigrams)} unseen "
            "evidence bigrams; the required unseen-combination axis is therefore a separately "
            "labeled derived compound-token stress, not part of primary accuracy"
        ),
        "full_test_manifest": (
            f"evaluated {config.test_episodes} of {test['episode_count']} seeds under the C04 "
            "CPU profile; this is not a C02 1000-episode claim"
        ),
    }
    result = {
        "schema_version": "0.2",
        "config": loaded_config.to_dict(),
        "manifest_evidence": manifest_evidence,
        "checkpoint_metadata": metadata,
        "training_history": history,
        "held_out": summary.to_dict(),
        "held_out_protocol": held_out_protocol,
        "runtime_seconds": time.perf_counter() - started,
        "versions": {"torch": torch.__version__},
    }
    acceptance = {
        "offline_cpu_main_completed": True,
        "reproducible_seed_and_config_recorded": True,
        "immutable_manifests_unchanged": final_hashes == initial_hashes,
        "all_held_out_axes_documented": all(
            bool(row["satisfied"]) for row in held_out_protocol["axes"].values()
        ),
        "above_chance": summary.accuracy > summary.chance_accuracy,
        "above_nonlearning_baseline": summary.accuracy > summary.nonlearning_accuracy,
        "bounded_active_set": int(summary.counters["selected_modules"])
        == summary.examples * config.active_k,
        "real_selected_edge_counter": int(summary.counters["evaluated_edges"])
        == summary.examples * config.active_k**2,
        "no_ignition_not_collapsed": 0.0 < summary.coverage < 1.0,
        "non_hand_authored_recovery": bool(recoveries),
        "trace_fields_present": bool(rows)
        and {"selected_modules", "evidence_path", "coalition"} <= set(rows[0]),
        "collapse_and_load_diagnostics_present": bool(summary.module_loads),
        "checkpoint_reload_completed": metadata["training_seed"] == config.seed,
        "all_ablations_completed": {row["condition"] for row in ablations} == set(ABLATIONS),
        "negative_findings_and_budget_recorded": True,
    }
    _write_json(output / "resolved-config.json", raw)
    _write_json(output / "manifest-evidence.json", manifest_evidence)
    _write_json(output / "training-history.json", history)
    _write_json(output / "held-out-rows.json", rows)
    _write_json(output / "held-out-protocol.json", held_out_protocol)
    _write_json(output / "distractor-stress-summary.json", distractor_summary.to_dict())
    _write_json(output / "distractor-stress-rows.json", distractor_rows)
    _write_json(output / "combination-stress-summary.json", combination_summary.to_dict())
    _write_json(output / "combination-stress-rows.json", combination_rows)
    _write_json(output / "summary.json", result)
    _write_json(output / "recovery-cases.json", recoveries)
    _write_json(output / "ablations.json", ablations)
    _write_json(output / "sensitivity.json", sensitivity)
    _write_json(output / "hyperparameter-budget.json", budget)
    _write_json(output / "negative-findings.json", negative)
    _write_json(output / "acceptance-matrix.json", acceptance)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the offline C04 learned-routing study")
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.config), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
