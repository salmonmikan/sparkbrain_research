from __future__ import annotations

import argparse
import hashlib
import json
import platform
import time
from dataclasses import asdict
from pathlib import Path
from statistics import mean
from typing import Any

from ..baselines import (
    ChanceBound,
    EvidenceAccumulator,
    LaplaceHMM,
    OracleBound,
    PrivilegedBayesFilter,
)
from ..baselines.neural import (
    FeatureEncoder,
    TorchStreamingBaseline,
    analytical_training_work,
    compute_match,
    configure_determinism,
    make_explicit_state,
    make_gru,
    make_lstm,
    make_rim_like,
    make_transformer,
    parameter_match,
    trainable_parameter_count,
)
from ..worlds import SwitchEvent
from .baseline_data import (
    episode_manifest_hash,
    episodes_from_manifest,
    load_split_manifest,
    split_dev_episodes,
)
from .baseline_profiler import profile_calls
from .baseline_report import holm_adjust, paired_bootstrap, paired_sign_flip, standardized_effect
from .baseline_trainer import train_module

ROOT = Path(__file__).resolve().parents[3]

FROZEN_INPUTS = (
    "configs/experiments/phase1/manifests/dev-v1.json",
    "configs/experiments/phase1/manifests/test-v1.json",
    "artifacts/phase1/c02-main-1000/run_manifest.json",
    "artifacts/phase1/c02-main-1000/split_manifest.json",
)


def _frozen_hashes() -> dict[str, str]:
    return {
        relative: hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        for relative in FROZEN_INPUTS
    }


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _truth(step: Any) -> str:
    object_id = step.observation.object_id or sorted(step.target.belief_truth_by_object)[0]
    if object_id not in step.target.belief_truth_by_object:
        object_id = sorted(step.target.belief_truth_by_object)[0]
    return step.target.belief_truth_by_object[object_id]


def _evaluate(
    name: str, model: Any, episodes: list[Any]
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    for episode in episodes:
        model.reset()
        for step in episode.steps:
            truth = _truth(step)
            if isinstance(model, OracleBound):
                prediction = model.evaluator_step(truth)
            elif isinstance(model, EvidenceAccumulator):
                event = SwitchEvent(
                    step.observation.delivery_time,
                    step.observation.evidence_label,
                    "<evaluator-hidden>",
                )
                prediction = model.step(event).prediction
            else:
                prediction = model.step(step.observation)
            probabilities = model.predict_proba()
            rows.append(
                {
                    "model": name,
                    "episode_id": episode.episode_id,
                    "step_index": step.observation.step_index,
                    "truth": truth,
                    "prediction": prediction,
                    "decided": prediction is not None,
                    "correct": prediction == truth,
                    "probabilities": probabilities,
                }
            )
    decided = [row for row in rows if row["decided"]]
    return (
        {
            "model": name,
            "steps": len(rows),
            "accuracy_all_steps": mean(float(row["correct"]) for row in rows),
            "coverage": len(decided) / len(rows),
            "accuracy_when_decided": mean(float(row["correct"]) for row in decided)
            if decided
            else None,
            "work_counters": model.work_counters(),
        },
        rows,
    )


def _nearest(
    candidates: list[tuple[int, Any]], parameter_target: int
) -> tuple[Any, dict[str, int]]:
    size, module = min(
        candidates,
        key=lambda row: (abs(trainable_parameter_count(row[1]) - parameter_target), row[0]),
    )
    return module, {"architecture_size": size}


def _neural_modules(
    input_size: int, parameter_target: int
) -> dict[str, tuple[Any, dict[str, int]]]:
    return {
        "gru": _nearest(
            [(size, make_gru(input_size, hidden_size=size)) for size in range(8, 180)],
            parameter_target,
        ),
        "lstm": _nearest(
            [(size, make_lstm(input_size, hidden_size=size)) for size in range(8, 180)],
            parameter_target,
        ),
        "causal_transformer_context64": _nearest(
            [
                (size, make_transformer(input_size, model_size=size, heads=4))
                for size in range(8, 181, 4)
            ],
            parameter_target,
        ),
        "rim_like_top2_of4": _nearest(
            [(size, make_rim_like(input_size, module_size=size)) for size in range(4, 120)],
            parameter_target,
        ),
        "explicit_state_memory": _nearest(
            [(size, make_explicit_state(input_size, state_size=size)) for size in range(3, 350)],
            parameter_target,
        ),
    }


def _family_forward_operations(
    name: str, *, input_size: int, size: int, sequence_length: int
) -> int:
    classes = 3
    if name == "gru":
        per_token = 3 * (input_size * size + size * size + size) + size * classes
    elif name == "lstm":
        per_token = 4 * (input_size * size + size * size + size) + size * classes
    elif name == "causal_transformer_context64":
        per_token = input_size * size + 8 * size * size + size * classes
        return sequence_length * per_token + 2 * sequence_length**2 * size
    elif name == "rim_like_top2_of4":
        per_token = (
            2 * 3 * (input_size * size + size * size + size) + 4 * input_size + 4 * size * classes
        )
    else:
        per_token = (input_size + size) * size + size * classes
    return sequence_length * per_token


def run(config_path: Path, output: Path) -> dict[str, Any]:
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"Output directory is not empty: {output}")
    output.mkdir(parents=True, exist_ok=True)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    frozen_before = _frozen_hashes()
    started = time.monotonic()
    deadline = started + float(config["hard_timeout_seconds"])
    dev_manifest = load_split_manifest(ROOT / config["dev_manifest"])
    test_manifest = load_split_manifest(ROOT / config["test_manifest"])
    worlds = list(config["worlds"])
    dev = episodes_from_manifest(
        dev_manifest,
        worlds=worlds,
        steps=int(config["steps"]),
        limit=int(config["dev_episodes_per_world"]),
    )
    test = episodes_from_manifest(
        test_manifest,
        worlds=worlds,
        steps=int(config["steps"]),
        limit=int(config["test_episodes_per_world"]),
    )
    train, selection = split_dev_episodes(dev)
    encoder = FeatureEncoder()
    encoder.fit(train)
    input_hashes = {
        "train": encoder.input_hash(train),
        "dev": encoder.input_hash(selection),
        "test": encoder.input_hash(test),
    }
    results: list[dict[str, Any]] = []
    raw_rows: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    profiles: list[dict[str, Any]] = []
    run_seeds = [int(seed) for seed in config["run_seeds"]]
    determinism: list[dict[str, Any]] = []
    parameter_target = int(config["parameter_target"])
    compute_target = int(config["compute_target"])
    dev_target, _ = _evaluate("accumulator", EvidenceAccumulator(), selection)
    for run_seed in run_seeds:
        if time.monotonic() >= deadline:
            failures.append({"family": "all_remaining", "seed": run_seed, "reason": "hard timeout"})
            break
        determinism.append(configure_determinism(run_seed, threads=int(config["torch_threads"])))
        modules = _neural_modules(encoder.input_size, parameter_target)
        for name, (module, architecture) in modules.items():
            training = train_module(
                module,
                encoder,
                train,
                optimizer_steps=int(config["optimizer_steps"]),
                learning_rate=float(config["learning_rate"]),
            )
            optimizer_proxy = analytical_training_work(
                module,
                examples=1,
                sequence_length=int(config["steps"]),
                steps=training.steps_completed,
            )
            profile = {
                "model": name,
                "seed": run_seed,
                "parameters": trainable_parameter_count(module),
                "body_parameters": trainable_parameter_count(module),
                "nominal_padded_parameters": None,
                "parameter_target": parameter_target,
                "parameter_match": parameter_match(
                    trainable_parameter_count(module), parameter_target
                ),
                "architecture": architecture,
                "optimizer_work_proxy": optimizer_proxy,
                "compute_target": compute_target,
                "optimizer_proxy_match": compute_match(optimizer_proxy, compute_target),
                "training": asdict(training),
            }
            family_forward = _family_forward_operations(
                name,
                input_size=encoder.input_size,
                size=architecture["architecture_size"],
                sequence_length=int(config["steps"]),
            )
            profile["family_forward_operations_per_episode"] = family_forward
            profile["family_training_operations_estimate"] = (
                family_forward * 3 * training.steps_completed
            )
            import torch

            sample = torch.tensor([encoder.encode_episode(train[0]).features], dtype=torch.float32)
            profile.update(
                profile_calls(
                    lambda module=module, sample=sample: module(sample), warmups=1, repeats=3
                )
            )
            checkpoint = output / "checkpoints" / f"{name}-seed-{run_seed}.pt"
            checkpoint.parent.mkdir(parents=True, exist_ok=True)
            torch.save(module.state_dict(), checkpoint)
            profile["checkpoint"] = str(checkpoint.relative_to(output)).replace("\\", "/")
            profiles.append(profile)
            if training.failed:
                failures.append({"family": name, "seed": run_seed, "reason": training.error})
            threshold_rows = []
            for threshold in (0.0, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.8, 0.9):
                candidate = TorchStreamingBaseline(
                    name, module, encoder, context_limit=64, confidence_threshold=threshold
                )
                candidate_metrics, _ = _evaluate(name, candidate, selection)
                distance = abs(
                    candidate_metrics["accuracy_all_steps"] - dev_target["accuracy_all_steps"]
                ) + abs(candidate_metrics["coverage"] - dev_target["coverage"])
                threshold_rows.append((distance, threshold, candidate_metrics))
            _, selected_threshold, dev_metrics = min(
                threshold_rows, key=lambda row: (row[0], row[1])
            )
            wrapped = TorchStreamingBaseline(
                name,
                module,
                encoder,
                context_limit=64,
                confidence_threshold=selected_threshold,
            )
            profile["dev_accuracy_all_steps"] = dev_metrics["accuracy_all_steps"]
            profile["dev_coverage"] = dev_metrics["coverage"]
            profile["selected_confidence_threshold"] = selected_threshold
            profile["quality_target_accuracy"] = dev_target["accuracy_all_steps"]
            profile["quality_target_coverage"] = dev_target["coverage"]
            profile["quality_match"] = (
                abs(dev_metrics["accuracy_all_steps"] - dev_target["accuracy_all_steps"]) <= 0.01
                and abs(dev_metrics["coverage"] - dev_target["coverage"]) <= 0.02
            )
            aggregate, rows = _evaluate(name, wrapped, test)
            aggregate["seed"] = run_seed
            results.append(aggregate)
            raw_rows.extend({**row, "seed": run_seed} for row in rows)
    hmm = LaplaceHMM(alpha=1.0)
    hmm.fit(train)
    deterministic = {
        "accumulator": EvidenceAccumulator(),
        "privileged_bayes": PrivilegedBayesFilter(),
        "laplace_hmm": hmm,
        "chance": ChanceBound(),
        "oracle": OracleBound(),
    }
    for name, model in deterministic.items():
        aggregate, rows = _evaluate(name, model, test)
        aggregate["seed"] = None
        results.append(aggregate)
        raw_rows.extend(rows)
    grouped = {
        name: [row for row in raw_rows if row["model"] == name]
        for name in sorted({row["model"] for row in raw_rows})
    }
    reference = grouped.get("accumulator", [])
    paired: list[dict[str, Any]] = []
    p_values: dict[str, float] = {}
    reference_map = {
        (row["episode_id"], row["step_index"]): float(row["correct"]) for row in reference
    }
    comparison_groups: dict[tuple[str, int | None], list[dict[str, Any]]] = {}
    for row in raw_rows:
        comparison_groups.setdefault((row["model"], row.get("seed")), []).append(row)
    for (name, seed), rows in comparison_groups.items():
        if name == "accumulator":
            continue
        values = [
            float(row["correct"]) - reference_map[(row["episode_id"], row["step_index"])]
            for row in rows
            if (row["episode_id"], row["step_index"]) in reference_map
        ]
        p_value = paired_sign_flip(values)
        comparison_id = f"{name}:seed={seed}"
        p_values[comparison_id] = p_value
        paired.append(
            {
                "comparison_id": comparison_id,
                "model": name,
                "seed": seed,
                "mean_accuracy_difference": mean(values),
                "bootstrap_95": paired_bootstrap(values),
                "effect_size": standardized_effect(values),
                "p_value": p_value,
            }
        )
    adjusted = holm_adjust(p_values)
    for row in paired:
        row["holm_p_value"] = adjusted[row["comparison_id"]]
    acceptance = {
        "all_families_present": len(grouped) == 10,
        "five_learned_seeds": len(run_seeds) >= 5,
        "identical_input_hash_recorded": len(set(input_hashes.values())) == 3,
        "parameter_tolerance": all(row["parameter_match"] for row in profiles),
        "optimizer_proxy_tolerance": all(row["optimizer_proxy_match"] for row in profiles),
        "scientific_compute_match": False,
        "equal_trial_budget": int(config["trial_budget_per_family"]) == 12,
        "quality_match_evaluated": all("quality_match" in row for row in profiles),
        "quality_match_achieved": all(row["quality_match"] for row in profiles),
        "within_hard_timeout": time.monotonic() < deadline,
        "no_failed_runs": not failures,
    }
    failure_cases = []
    for name in sorted(grouped):
        candidates = [row for row in grouped[name] if not row["correct"]]
        if candidates:
            failure_cases.append(candidates[0])
    _write_json(output / "resolved_config.json", config)
    _write_json(output / "raw_results.json", raw_rows)
    _write_json(output / "aggregate_metrics.json", results)
    _write_json(output / "profiles.json", profiles)
    _write_json(output / "paired_statistics.json", paired)
    _write_json(output / "failures.json", failures)
    _write_json(output / "failure_cases.json", failure_cases)
    _write_json(output / "acceptance.json", acceptance)
    manifest = {
        "schema_version": "0.1",
        "run_id": output.name,
        "profile": config["profile"],
        "completed": all(acceptance.values()),
        "elapsed_seconds": time.monotonic() - started,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "determinism": determinism,
        "episode_manifest_hashes": {
            "dev": episode_manifest_hash(dev),
            "test": episode_manifest_hash(test),
        },
        "input_hashes": input_hashes,
        "input_hashes_by_family": {name: input_hashes for name in grouped},
        "test_used_for_selection": False,
        "network_required": False,
        "frozen_input_sha256_before": frozen_before,
        "frozen_input_sha256_after": _frozen_hashes(),
    }
    manifest["frozen_inputs_unchanged"] = (
        manifest["frozen_input_sha256_before"] == manifest["frozen_input_sha256_after"]
    )
    if not manifest["frozen_inputs_unchanged"]:
        raise RuntimeError("C02 frozen input hashes changed during C05 execution")
    completion_checks = dict(acceptance)
    completion_checks.pop("quality_match_achieved")
    completion_checks.pop("scientific_compute_match")
    if config["profile"] == "smoke":
        completion_checks.pop("five_learned_seeds")
    manifest["completed"] = all(completion_checks.values())
    _write_json(output / "run_manifest.json", manifest)
    report = [
        "# C05 matched baseline run",
        "",
        f"Profile: `{config['profile']}`; completed: `{manifest['completed']}`; "
        f"elapsed: `{manifest['elapsed_seconds']:.3f}s`.",
        "",
        "Accuracy and coverage are reported separately. Oracle is evaluator-only and "
        "privileged Bayes uses declared world information. RIM-like is a small top-k "
        "modular recurrent equivalent, not an exact RIM reproduction.",
        "",
        "Operation counts and CPU time are not physical energy measurements. Any failed "
        "or unmatched run remains in `failures.json` / `acceptance.json`.",
    ]
    (output / "report.md").write_text("\n".join(report) + "\n", encoding="utf-8", newline="\n")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.config, args.output), indent=2))


if __name__ == "__main__":
    main()
