from __future__ import annotations

import argparse
import hashlib
import json
import random
import shutil
import tempfile
from collections.abc import Iterable
from pathlib import Path
from statistics import mean
from typing import Any

from sparkbrain.v03_seed import (
    AdaptiveSensoryField,
    DistractorNoiseWorld,
    GoalTargetWorld,
    HabituationWorld,
    SensorySample,
    SensoryWorldStep,
    StimulusSpecificityWorld,
    UnexpectedChangeWorld,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL = ROOT / "artifacts" / "v03" / "c12_sensory_field" / "protocol.json"
DEFAULT_PROTECTED = (
    ROOT / "artifacts" / "v03" / "c11_input_diagnosis" / "frozen_baseline_hashes.json"
)
CONDITIONS = (
    "full",
    "no_goal",
    "no_habituation",
    "no_prediction_error",
    "no_novelty",
    "no_magnitude",
    "bypass",
)


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _verify_protected_hashes(root: Path, protected_path: Path) -> None:
    frozen = json.loads(protected_path.read_text(encoding="utf-8"))
    for relative, expected in frozen["protected_files"].items():
        path = root / relative
        if not path.is_file() or _sha256(path) != expected:
            raise RuntimeError(f"protected baseline hash changed: {relative}")


def _percentile(values: list[float], probability: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = position - lower
    return ordered[lower] * (1.0 - fraction) + ordered[upper] * fraction


def _paired_interval(values: list[float], protocol: dict[str, Any]) -> dict[str, Any]:
    spec = protocol["statistical_analysis"]
    generator = random.Random(int(spec["bootstrap_seed"]))
    repetitions = int(spec["bootstrap_repetitions"])
    samples = [mean(generator.choice(values) for _ in values) for _ in range(repetitions)]
    return {
        "bootstrap_repetitions": repetitions,
        "bootstrap_seed": int(spec["bootstrap_seed"]),
        "ci_high": _percentile(samples, 0.975),
        "ci_low": _percentile(samples, 0.025),
        "confidence_level": 0.95,
        "effect_size": mean(values),
        "paired_block_count": len(values),
    }


def _condition_options(condition: str) -> tuple[frozenset[str], bool]:
    if condition == "full":
        return frozenset(), False
    if condition == "bypass":
        return frozenset(), True
    return frozenset({condition}), False


def _execute(
    *,
    condition: str,
    seed: int,
    steps: Iterable[SensoryWorldStep],
) -> tuple[list[dict[str, Any]], dict[tuple[str, str], bool]]:
    field = AdaptiveSensoryField()
    ablations, bypass = _condition_options(condition)
    rows: list[dict[str, Any]] = []
    event_emission: dict[tuple[str, str], bool] = {}
    for step_index, step in enumerate(steps):
        result = field.observe_with_trace(
            step.sample,
            goal_bias=step.goal_bias,
            ablations=ablations,
            bypass=bypass,
        )
        target_rows = [
            row for row in result.channel_trace if row.feature_id == step.target_feature_id
        ]
        if len(target_rows) != 1:
            raise RuntimeError(
                f"target trace row missing or duplicated: {step.target_feature_id}"
            )
        event_emission[(step.episode_id, step.event_kind)] = target_rows[0].accepted
        for channel in result.channel_trace:
            rows.append(
                {
                    "condition_id": condition,
                    "seed": seed,
                    "world": step.world,
                    "episode_id": step.episode_id,
                    "step_index": step_index,
                    "event_kind": step.event_kind,
                    "expected_salient": step.expected_salient,
                    "target_feature_id": step.target_feature_id,
                    "target_channel": channel.feature_id == step.target_feature_id,
                    "state_hash_before": result.state_hash_before,
                    "state_hash_after": result.state_hash_after,
                    "work_delta": result.work_delta.as_dict(),
                    "work_total": result.work_total.as_dict(),
                    **channel.as_dict(),
                }
            )
    return rows, event_emission


def _evaluate_condition(
    condition: str,
    seeds: list[int],
    raw_rows: list[dict[str, Any]],
    change_examples: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, list[float]]]:
    repetition_reductions: list[float] = []
    downstream_reductions: list[float] = []
    change_recalls: list[float] = []
    goal_deltas: list[float] = []
    false_deltas: list[float] = []
    specificity: list[float] = []
    for seed in seeds:
        habitation_rows, _ = _execute(
            condition=condition, seed=seed, steps=HabituationWorld(seed).steps()
        )
        raw_rows.extend(habitation_rows)
        step_counts: dict[int, int] = {}
        for row in habitation_rows:
            step_counts.setdefault(int(row["step_index"]), 0)
            step_counts[int(row["step_index"])] += int(row["accepted"])
        first = step_counts[0]
        repeated_mean = mean(step_counts[index] for index in sorted(step_counts)[1:])
        repetition_reductions.append(1.0 - repeated_mean / first if first else 0.0)
        downstream_by_step: dict[int, int] = {}
        for row in habitation_rows:
            downstream_by_step.setdefault(
                int(row["step_index"]),
                int(row["work_delta"]["downstream_active_work"]),
            )
        first_downstream = downstream_by_step[0]
        repeated_downstream = mean(
            downstream_by_step[index] for index in sorted(downstream_by_step)[1:]
        )
        downstream_reductions.append(
            1.0 - repeated_downstream / first_downstream if first_downstream else 0.0
        )

        recovered: list[float] = []
        for episode in UnexpectedChangeWorld(seed).episodes():
            episode_rows, emissions = _execute(condition=condition, seed=seed, steps=episode)
            raw_rows.extend(episode_rows)
            event = episode[-1]
            success = emissions[(event.episode_id, event.event_kind)]
            recovered.append(float(success))
            event_rows = [row for row in episode_rows if row["event_kind"] == event.event_kind]
            change_examples.append(
                {
                    "condition_id": condition,
                    "seed": seed,
                    "event_kind": event.event_kind,
                    "recovered": success,
                    "omission_definition": (
                        "explicit expected-channel absence is scored as zero and committed as the "
                        "latest local value after prediction-error evaluation"
                    ),
                    "channel_rows": event_rows,
                }
            )
        change_recalls.extend(recovered)

        goal_outcomes: list[float] = []
        for with_goal in (False, True):
            goal_rows, goal_emissions = _execute(
                condition=condition,
                seed=seed,
                steps=GoalTargetWorld(seed).steps(with_goal=with_goal),
            )
            raw_rows.extend(goal_rows)
            episode_id = f"{'goal' if with_goal else 'no_goal'}:{seed}"
            goal_outcomes.append(float(goal_emissions[(episode_id, "weak_goal_target")]))
        goal_deltas.append(goal_outcomes[1] - goal_outcomes[0])

        false_rates: list[float] = []
        for with_goal in (False, True):
            noise_rows, _ = _execute(
                condition=condition,
                seed=seed,
                steps=DistractorNoiseWorld(seed).steps(with_goal=with_goal),
            )
            raw_rows.extend(noise_rows)
            probes = [row for row in noise_rows if row["event_kind"] == "noise_probe"]
            false_rates.append(mean(float(row["accepted"]) for row in probes))
        false_deltas.append(100.0 * (false_rates[1] - false_rates[0]))

        specificity_rows, specificity_events = _execute(
            condition=condition,
            seed=seed,
            steps=StimulusSpecificityWorld(seed).steps(),
        )
        raw_rows.extend(specificity_rows)
        specificity.append(
            float(specificity_events[(f"specificity:{seed}", "novel_channel")])
        )

    metrics = {
        "change_or_omission_recall": mean(change_recalls),
        "goal_relevant_recall_delta": mean(goal_deltas),
        "irrelevant_false_activation_increase_percentage_points": mean(false_deltas),
        "predictable_repetition_active_spark_reduction": mean(repetition_reductions),
        "predictable_repetition_downstream_work_reduction": mean(downstream_reductions),
        "stimulus_specificity_recall": mean(specificity),
    }
    paired = {
        "change_or_omission_recall": change_recalls,
        "goal_relevant_recall_delta": goal_deltas,
        "irrelevant_false_activation_increase_percentage_points": false_deltas,
        "predictable_repetition_active_spark_reduction": repetition_reductions,
        "predictable_repetition_downstream_work_reduction": downstream_reductions,
        "stimulus_specificity_recall": specificity,
    }
    return metrics, paired


def _goal_adversarial_audit(protocol: dict[str, Any]) -> dict[str, Any]:
    base = AdaptiveSensoryField()
    base.observe(
        SensorySample("audit:0", 0.0, "audit", "vision", {"weak": 1.0})
    )
    base.observe(
        SensorySample("audit:1", 1.0, "audit", "vision", {"weak": 1.0})
    )
    checks: list[dict[str, Any]] = []

    def record_refusal(
        *,
        check_id: str,
        field: AdaptiveSensoryField,
        sample: SensorySample,
        goal_bias: dict[str, float] | None = None,
    ) -> None:
        before = field.state_hash()
        refused = False
        error = ""
        try:
            field.observe(sample, goal_bias=goal_bias)
        except ValueError as exc:
            refused = True
            error = str(exc)
        after = field.state_hash()
        checks.append(
            {
                "check_id": check_id,
                "error": error,
                "passed": refused and before == after,
                "refused": refused,
                "state_hash_after": after,
                "state_hash_before": before,
                "state_unchanged": before == after,
            }
        )

    forbidden = protocol["goal_policy"]["forbidden_recursive_names"]
    for name in forbidden:
        record_refusal(
            check_id=f"metadata_top:{name}",
            field=AdaptiveSensoryField.from_serialized_state(base.serialize_state()),
            sample=SensorySample(
                f"audit:metadata-top:{name}",
                2.0,
                "audit",
                "vision",
                {"weak": 0.4},
                metadata={name: True},
            ),
        )
        record_refusal(
            check_id=f"metadata_nested:{name}",
            field=AdaptiveSensoryField.from_serialized_state(base.serialize_state()),
            sample=SensorySample(
                f"audit:metadata-nested:{name}",
                2.0,
                "audit",
                "vision",
                {"weak": 0.4},
                metadata={"outer": [{name: True}]},
            ),
        )
        record_refusal(
            check_id=f"goal_key:{name}",
            field=AdaptiveSensoryField.from_serialized_state(base.serialize_state()),
            sample=SensorySample(
                f"audit:goal:{name}", 2.0, "audit", "vision", {"weak": 0.4}
            ),
            goal_bias={name: 0.1},
        )

    for label, value in (("nan", float("nan")), ("positive_inf", float("inf"))):
        record_refusal(
            check_id=f"goal_value:{label}",
            field=AdaptiveSensoryField.from_serialized_state(base.serialize_state()),
            sample=SensorySample(
                f"audit:{label}", 2.0, "audit", "vision", {"weak": 0.4}
            ),
            goal_bias={"vision:weak": value},
        )

    capped_field = AdaptiveSensoryField.from_serialized_state(base.serialize_state())
    before = capped_field.state_hash()
    capped = capped_field.observe_with_trace(
        SensorySample("audit:extreme", 2.0, "audit", "vision", {"weak": 0.4}),
        goal_bias={"vision:weak": 1.0e300},
    ).channel_trace[0]
    checks.append(
        {
            "applied": capped.goal_bias_applied,
            "check_id": "goal_value:finite_extreme_cap",
            "passed": (
                capped.goal_bias_requested == 1.0e300
                and capped.goal_bias_applied == protocol["goal_policy"]["maximum_channel_request"]
            ),
            "requested": capped.goal_bias_requested,
            "state_hash_after": capped_field.state_hash(),
            "state_hash_before": before,
            "state_unchanged": False,
        }
    )
    return {
        "all_checks_passed": all(check["passed"] for check in checks),
        "checks": checks,
        "goal_bias_applied_maximum": protocol["goal_policy"]["maximum_channel_request"],
        "protocol_id": protocol["protocol_id"],
    }


def _acceptance(
    metrics: dict[str, Any],
    protocol: dict[str, Any],
    goal_audit: dict[str, Any],
) -> dict[str, bool]:
    gates = protocol["acceptance"]
    return {
        "change_or_omission_recall": metrics["change_or_omission_recall"]
        >= gates["unexpected_change_or_omission_recall_minimum"],
        "goal_relevant_low_salience_recall": metrics["goal_relevant_recall_delta"] > 0.0,
        "goal_adversarial_audit": goal_audit["all_checks_passed"],
        "irrelevant_false_activation": metrics[
            "irrelevant_false_activation_increase_percentage_points"
        ]
        <= gates["distractor_false_activation_increase_max_percentage_points"],
        "predictable_repetition_active_sparks": metrics[
            "predictable_repetition_active_spark_reduction"
        ]
        >= gates["predictable_repetition_active_spark_reduction_minimum"],
        "predictable_repetition_downstream_work": metrics[
            "predictable_repetition_downstream_work_reduction"
        ]
        >= gates["predictable_repetition_downstream_work_reduction_minimum"],
        "stimulus_specificity": metrics["stimulus_specificity_recall"] > 0.0,
    }


def _run_into(*, root: Path, protocol_path: Path, output: Path) -> dict[str, Any]:
    if output.exists() and any(output.iterdir()):
        raise RuntimeError("output directory must be new or empty")
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    if protocol["protocol_id"] != "c12-sensory-field-v1":
        raise RuntimeError("unexpected C12 protocol")
    seeds = [int(seed) for seed in protocol["seed_list"]]
    if len(seeds) < 5 or len(set(seeds)) != len(seeds):
        raise RuntimeError("C12 primary evaluation requires at least five unique seeds")
    if tuple(protocol["ablations"]) != CONDITIONS:
        raise RuntimeError("C12 conditions do not match the preregistered protocol")
    _verify_protected_hashes(root, DEFAULT_PROTECTED)

    output.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(protocol_path, output / "protocol.json")
    raw_rows: list[dict[str, Any]] = []
    change_examples: list[dict[str, Any]] = []
    by_condition: dict[str, Any] = {}
    for condition in CONDITIONS:
        metrics, paired = _evaluate_condition(condition, seeds, raw_rows, change_examples)
        by_condition[condition] = {
            "metrics": metrics,
            "paired_intervals": {
                name: _paired_interval(values, protocol) for name, values in paired.items()
            },
        }
    goal_audit = _goal_adversarial_audit(protocol)
    full_acceptance = _acceptance(by_condition["full"]["metrics"], protocol, goal_audit)
    acceptance_passed = all(full_acceptance.values())
    aggregate = {
        "acceptance": full_acceptance,
        "acceptance_passed": acceptance_passed,
        "conditions": by_condition,
        "protocol_id": protocol["protocol_id"],
        "run_id": protocol["run_id"],
        "seed_list": seeds,
        "work_interpretation": (
            "channels_inspected/features_scored/state_updates are dense sensory work; only "
            "sparks_emitted/downstream_active_work are active downstream work"
        ),
    }
    raw_rows.sort(
        key=lambda row: (
            CONDITIONS.index(row["condition_id"]),
            row["seed"],
            row["world"],
            row["episode_id"],
            row["step_index"],
            row["feature_id"],
        )
    )
    change_examples.sort(
        key=lambda row: (CONDITIONS.index(row["condition_id"]), row["seed"], row["event_kind"])
    )
    _write_jsonl(output / "raw_trace.jsonl", raw_rows)
    (output / "ablation_metrics.json").write_text(
        _canonical_json(aggregate), encoding="utf-8", newline="\n"
    )
    _write_jsonl(output / "change_recovery_examples.jsonl", change_examples)
    goal_adversarial = {
        **goal_audit,
        "acceptance_passed": full_acceptance["goal_adversarial_audit"],
        "irrelevant_false_activation_increase_percentage_points": by_condition["full"][
            "metrics"
        ]["irrelevant_false_activation_increase_percentage_points"],
        "note": (
            "An exact noise-channel request is capped and does not force every noise probe "
            "to emit."
        ),
        "protocol_id": protocol["protocol_id"],
    }
    (output / "goal_bias_adversarial.json").write_text(
        _canonical_json(goal_adversarial), encoding="utf-8", newline="\n"
    )
    full = by_condition["full"]["metrics"]
    repetition = full["predictable_repetition_active_spark_reduction"]
    downstream = full["predictable_repetition_downstream_work_reduction"]
    false_increase = full["irrelevant_false_activation_increase_percentage_points"]
    report = f"""# C12 computational sensory-gate report

Protocol: `{protocol['protocol_id']}`  
Run: `{protocol['run_id']}`  
Seeds: {', '.join(str(seed) for seed in seeds)}

## Result

- G04 acceptance: **{'pass' if acceptance_passed else 'fail'}**
- predictable-repetition active-Spark reduction: {repetition:.6f}
- predictable-repetition downstream-active-work reduction: {downstream:.6f}
- change / explicit-omission recall: {full['change_or_omission_recall']:.6f}
- bounded-goal low-salience recall delta: {full['goal_relevant_recall_delta']:.6f}
- irrelevant false-activation increase: {false_increase:.6f} percentage points
- stimulus-specificity recall: {full['stimulus_specificity_recall']:.6f}

## Omission and work definitions

An omission is an explicit adapter observation that a previously expected channel is absent.
It is scored as value zero against the local prediction, then value zero is committed as the
latest local observation. It is not inferred from an absent key and is not evaluator truth.
The checked raw change/omission rows demonstrate recovery under this definition.

Every channel is inspected and scored. Repetition reduces emitted Sparks and downstream active
work; it does **not** reduce dense channel inspection/scoring in this implementation. These
counters are computational observations, not energy measurements.

## Claim boundary

This is a deterministic local computational sensory gate. It is not a biological sensory-system
reproduction, semantic understanding result, hardware-efficiency result, or change to C06/C08
negative findings or scientific claim grades. Failed ablations and adversarial rows are retained.
"""
    (output / "report.md").write_text(report, encoding="utf-8", newline="\n")
    return aggregate


def run(*, root: Path, protocol_path: Path, output: Path) -> dict[str, Any]:
    if output.exists() and any(output.iterdir()):
        raise RuntimeError("output directory must be new or empty")
    output.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(
        tempfile.mkdtemp(prefix=f".{output.name}.staging-", dir=output.parent)
    )
    try:
        result = _run_into(root=root, protocol_path=protocol_path, output=staging)
        expected = {
            "ablation_metrics.json",
            "change_recovery_examples.jsonl",
            "goal_bias_adversarial.json",
            "protocol.json",
            "raw_trace.jsonl",
            "report.md",
        }
        if {path.name for path in staging.iterdir()} != expected:
            raise RuntimeError("C12 staging output is incomplete or contains extra files")
        json.loads((staging / "ablation_metrics.json").read_text(encoding="utf-8"))
        goal_audit = json.loads(
            (staging / "goal_bias_adversarial.json").read_text(encoding="utf-8")
        )
        if not goal_audit["all_checks_passed"]:
            raise RuntimeError("C12 goal adversarial audit failed")
        if not (staging / "raw_trace.jsonl").read_text(encoding="utf-8").strip():
            raise RuntimeError("C12 raw trace is empty")
        if output.exists():
            output.rmdir()
        staging.replace(output)
        return result
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the preregistered C12 sensory evaluation")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(
        root=args.root.resolve(),
        protocol_path=args.protocol.resolve(),
        output=args.output,
    )
    print(json.dumps({"acceptance_passed": result["acceptance_passed"]}, sort_keys=True))
    return 0 if result["acceptance_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
