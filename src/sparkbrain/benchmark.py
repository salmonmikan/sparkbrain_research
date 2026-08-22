from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path
from statistics import mean
from typing import Callable

from .baselines import EvidenceAccumulator, HardWinnerTakeAll, InstantClassifier, run_baseline
from .metrics import SequencePoint, evaluate_sequence
from .model import BrainConfig
from .worlds import SwitchEvent, SwitchWorld, build_reference_brain, run_scenario


MetricRow = dict[str, float | int | str | None]


def _truth_at(events: list[SwitchEvent], time: float) -> str:
    applicable = [event.truth for event in events if event.time <= time + 1e-9]
    return applicable[-1] if applicable else events[0].truth


def run_sfa_episode(
    events: list[SwitchEvent],
    *,
    config: BrainConfig | None = None,
    ablation: str = "none",
) -> MetricRow:
    brain = build_reference_brain(config)
    if ablation == "no_residual":
        for spark in brain.sparks.values():
            if spark.kind.value == "hypothesis":
                spark.metadata["post_fire_residual"] = 0.02
    elif ablation == "single_spark_ignition":
        brain.config.min_support_sources = 1
        brain.config.stability_evaluations = 1
        brain.config.diversity_bonus = 0.0
    elif ablation != "none":
        raise ValueError(f"Unknown SFA ablation: {ablation}")

    brain, frames = run_scenario(events, brain=brain)
    points = [
        SequencePoint(
            time=frame.time,
            truth=frame.truth or "",
            prediction=frame.prediction,
            note=event.note,
        )
        for frame, event in zip(frames, events, strict=True)
    ]
    metrics = evaluate_sequence(points).to_dict()
    wrong_ignitions = sum(
        ignition.label != _truth_at(events, ignition.time)
        for ignition in brain.ignitions
    )
    metrics.update(
        {
            "model": "sparkbrain" if ablation == "none" else f"sparkbrain_{ablation}",
            "events_processed": brain.stats.events_processed,
            "spark_updates": brain.stats.spark_updates,
            "edge_evaluations": brain.stats.edge_evaluations,
            "fires": brain.stats.fires,
            "ignitions": brain.stats.ignitions,
            "false_ignition_rate": (
                wrong_ignitions / brain.stats.ignitions
                if brain.stats.ignitions
                else 0.0
            ),
            "active_spark_fraction": sum(
                float(frame.stats.get("active_spark_fraction", 0.0)) for frame in frames
            ) / max(1, len(frames)),
            "spark_update_equivalent_ratio": brain.stats.spark_updates
            / max(1, len(brain.sparks) * len(events)),
        }
    )
    return metrics


def run_baseline_episode(
    events: list[SwitchEvent],
    factory: Callable[[], EvidenceAccumulator],
) -> MetricRow:
    model = factory()
    steps = run_baseline(model, events)
    points = [
        SequencePoint(
            time=step.time,
            truth=step.truth,
            prediction=step.prediction,
            note=event.note,
        )
        for step, event in zip(steps, events, strict=True)
    ]
    metrics = evaluate_sequence(points).to_dict()
    metrics.update(
        {
            "model": model.name,
            # Dense baseline evaluates all labels per external event.
            "events_processed": len(events),
            "spark_updates": len(events) * 3,
            "edge_evaluations": len(events) * 3,
            "fires": 0,
            "ignitions": 0,
            "false_ignition_rate": None,
            "active_spark_fraction": 1.0,
            "spark_update_equivalent_ratio": 1.0,
        }
    )
    return metrics


def run_benchmark(
    *,
    episodes: int = 50,
    steps: int = 30,
    seed_start: int = 100,
) -> tuple[list[MetricRow], list[MetricRow]]:
    episode_rows: list[MetricRow] = []
    factories: list[tuple[str, Callable[[list[SwitchEvent]], MetricRow]]] = [
        ("sparkbrain", lambda events: run_sfa_episode(events)),
        (
            "sparkbrain_no_residual",
            lambda events: run_sfa_episode(events, ablation="no_residual"),
        ),
        (
            "sparkbrain_single_spark_ignition",
            lambda events: run_sfa_episode(events, ablation="single_spark_ignition"),
        ),
        (
            "accumulator",
            lambda events: run_baseline_episode(events, EvidenceAccumulator),
        ),
        (
            "hard_wta",
            lambda events: run_baseline_episode(events, HardWinnerTakeAll),
        ),
        (
            "instant",
            lambda events: run_baseline_episode(events, InstantClassifier),
        ),
    ]

    for episode in range(episodes):
        events = SwitchWorld.random_episode(seed=seed_start + episode, steps=steps)
        for model_name, runner in factories:
            row = runner(events)
            row["episode"] = episode
            row["model"] = model_name
            episode_rows.append(row)

    aggregate_rows: list[MetricRow] = []
    numeric_keys = [
        "coverage",
        "accuracy_all_steps",
        "accuracy_when_decided",
        "truth_changes",
        "prediction_changes",
        "unnecessary_revisions",
        "revision_precision",
        "revision_recall",
        "mean_switch_latency",
        "unresolved_switches",
        "recovery_rate",
        "noise_induced_wrong_switches",
        "events_processed",
        "spark_updates",
        "edge_evaluations",
        "fires",
        "ignitions",
        "false_ignition_rate",
        "active_spark_fraction",
        "spark_update_equivalent_ratio",
    ]

    for model_name, _ in factories:
        rows = [row for row in episode_rows if row["model"] == model_name]
        aggregate: MetricRow = {"model": model_name, "episodes": len(rows)}
        for key in numeric_keys:
            values = [
                float(row[key])
                for row in rows
                if row.get(key) is not None
            ]
            aggregate[key] = mean(values) if values else None
        aggregate_rows.append(aggregate)

    return episode_rows, aggregate_rows


def write_benchmark_outputs(
    output_dir: str | Path,
    *,
    episodes: int = 50,
    steps: int = 30,
) -> tuple[Path, Path, Path]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    episodes_rows, aggregate_rows = run_benchmark(episodes=episodes, steps=steps)

    json_path = output / "benchmark_results.json"
    json_path.write_text(
        json.dumps(
            {"episodes": episodes_rows, "aggregate": aggregate_rows},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    csv_path = output / "benchmark_aggregate.csv"
    fieldnames = list(aggregate_rows[0].keys())
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(aggregate_rows)

    md_path = output / "benchmark_report.md"
    metric_columns = [
        "model",
        "accuracy_all_steps",
        "coverage",
        "revision_recall",
        "revision_precision",
        "mean_switch_latency",
        "unnecessary_revisions",
        "recovery_rate",
        "active_spark_fraction",
        "spark_update_equivalent_ratio",
    ]
    lines = [
        "# SwitchWorld Phase-0 Benchmark",
        "",
        "> This is a deterministic hand-authored evidence-routing experiment. It is a software validation result, not evidence of general intelligence or biological equivalence.",
        "",
        f"Episodes: {episodes}; steps per episode: {steps}",
        "",
        "| " + " | ".join(metric_columns) + " |",
        "|" + "|".join(["---"] * len(metric_columns)) + "|",
    ]
    for row in aggregate_rows:
        values: list[str] = []
        for key in metric_columns:
            value = row.get(key)
            if isinstance(value, float):
                values.append(f"{value:.4f}")
            else:
                values.append(str(value))
        lines.append("| " + " | ".join(values) + " |")
    lines.extend(
        [
            "",
            "## Interpretation limits",
            "",
            "- All models receive the same hand-authored evidence weights.",
            "- No representation learning or end-to-end learning is evaluated.",
            "- `active_spark_fraction` is an algorithmic activity metric, not a hardware energy measurement.",
            "- `spark_update_equivalent_ratio` may exceed 1 because one external event can trigger several recurrent/event-driven updates.",
            "- The decisive research comparison requires learned routing and matched-parameter GRU/Transformer/RIM baselines.",
        ]
    )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, csv_path, md_path
