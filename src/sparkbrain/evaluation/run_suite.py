from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from ..tasks import generate_episode
from .bootstrap import percentile_interval
from .metrics import pareto_rows
from .runner import EpisodeResult, run_episode

SCHEMA_VERSION = "0.2"


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _condition_pairs(config: dict[str, Any]) -> list[tuple[str, str]]:
    if config.get("all_combinations"):
        return [
            (world, condition) for world in config["worlds"] for condition in config["conditions"]
        ]
    return [(str(row["world"]), str(row["condition"])) for row in config["matrix"]]


def _aggregate(results: list[EpisodeResult]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    grouped: dict[tuple[str, str], list[EpisodeResult]] = defaultdict(list)
    for result in results:
        grouped[(result.world, result.condition)].append(result)
    aggregates: list[dict[str, Any]] = []
    intervals: list[dict[str, Any]] = []
    for (world, condition), rows in sorted(grouped.items()):
        numeric_keys = sorted(
            {
                key
                for row in rows
                for key, value in row.metrics.items()
                if isinstance(value, (int, float)) and not isinstance(value, bool)
            }
        )
        aggregate: dict[str, Any] = {"world": world, "condition": condition, "episodes": len(rows)}
        for key in numeric_keys:
            values = [
                float(row.metrics[key])
                for row in rows
                if isinstance(row.metrics.get(key), (int, float))
            ]
            aggregate[key] = mean(values)
            if key in {
                "accuracy_all_steps",
                "coverage",
                "revision_precision",
                "revision_recall",
                "mean_switch_latency",
                "recovery_rate",
                "false_certainty_rate",
                "duplicate_evidence_inflation",
                "object_cross_talk",
                "belief_goal_flip_rate",
                "action_accuracy",
                "source_reliability_sensitivity",
            }:
                interval = percentile_interval(values, seed=1729, samples=400)
                intervals.append(
                    {
                        "world": world,
                        "condition": condition,
                        "metric": key,
                        "low": interval[0],
                        "high": interval[1],
                        "episodes": len(values),
                    }
                )
        aggregates.append(aggregate)
    return aggregates, intervals


def _pareto(aggregates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in aggregates:
        prediction_changes = max(1.0, float(row.get("prediction_changes", 0.0)))
        rows.append(
            {
                "world": row["world"],
                "condition": f"{row['world']}:{row['condition']}",
                "unnecessary_revision_rate": float(row.get("unnecessary_revisions", 0.0))
                / prediction_changes,
                "revision_recall": float(row.get("revision_recall", 0.0)),
                "mean_switch_latency": float(row.get("mean_switch_latency") or 1e9),
            }
        )
    return pareto_rows(rows)


def _write_pareto_svg(path: Path, rows: list[dict[str, Any]]) -> None:
    points = []
    for row in rows:
        x = 40 + min(520, float(row["unnecessary_revision_rate"]) * 500)
        y = 360 - min(320, float(row["revision_recall"]) * 320)
        color = "#b91c1c" if row["dominated"] else "#047857"
        label = row["condition"]
        points.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{color}">'
            f"<title>{label}</title></circle>"
        )
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="400" '
        'viewBox="0 0 640 400"><rect width="100%" height="100%" fill="white"/>'
        '<text x="20" y="20">Revision stability/adaptability Pareto '
        '(green=non-dominated)</text><line x1="40" y1="360" x2="600" y2="360" '
        'stroke="black"/><line x1="40" y1="40" x2="40" y2="360" stroke="black"/>'
        + "".join(points)
        + "</svg>\n"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg, encoding="utf-8", newline="\n")


def _failure_candidates(results: list[EpisodeResult]) -> list[tuple[str, EpisodeResult]]:
    categories = [
        ("confident_wrong", lambda row: float(row.metrics.get("false_certainty_rate", 0.0))),
        (
            "unresolved_or_slow",
            lambda row: (
                float(row.metrics.get("unresolved_switches", 0.0))
                + float(row.metrics.get("mean_switch_latency") or 0.0)
            ),
        ),
        (
            "cross_talk_or_goal_flip",
            lambda row: (
                float(row.metrics.get("object_cross_talk", 0.0))
                + float(row.metrics.get("belief_goal_flip_rate", 0.0))
            ),
        ),
    ]
    selected: list[tuple[str, EpisodeResult]] = []
    used: set[str] = set()
    for category, score in categories:
        candidates = [row for row in results if row.episode_id not in used]
        chosen = max(candidates, key=lambda row: (score(row), row.episode_id))
        used.add(chosen.episode_id)
        selected.append((category, chosen))
    return selected


def run_suite(config_path: Path, output: Path, *, command: str = "") -> dict[str, Any]:
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"Output directory is not empty: {output}")
    output.mkdir(parents=True, exist_ok=True)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    pairs = _condition_pairs(config)
    seeds = [int(config["seed_start"]) + index for index in range(int(config["episode_count"]))]
    split = str(config.get("split", "test"))
    split_manifest = {
        "schema_version": SCHEMA_VERSION,
        "split": split,
        "seeds": seeds,
        "worlds": sorted({world for world, _ in pairs}),
        "frozen": bool(config.get("frozen", False)),
    }
    _write_json(output / "resolved_config.json", config)
    _write_json(output / "split_manifest.json", split_manifest)
    _write_json(
        output / "software_versions.json",
        {"python": platform.python_version(), "platform": platform.platform()},
    )
    results: list[EpisodeResult] = []
    raw_handles: dict[tuple[str, str], Any] = {}
    try:
        for world, condition in pairs:
            raw_path = output / "raw" / world / f"{condition}.jsonl"
            raw_path.parent.mkdir(parents=True, exist_ok=True)
            raw_handles[(world, condition)] = raw_path.open("w", encoding="utf-8", newline="\n")
            for seed in seeds:
                episode = generate_episode(
                    world, seed=seed, split=split, steps=int(config.get("steps", 30))
                )
                result = run_episode(episode, condition=condition)
                results.append(result)
                raw_handles[(world, condition)].write(
                    json.dumps(result.to_dict(), ensure_ascii=False, sort_keys=True) + "\n"
                )
    finally:
        for handle in raw_handles.values():
            handle.close()
    aggregates, intervals = _aggregate(results)
    pareto = _pareto(aggregates)
    _write_json(output / "aggregate" / "metrics.json", aggregates)
    _write_csv(output / "aggregate" / "metrics.csv", aggregates)
    _write_json(output / "aggregate" / "confidence_intervals.json", intervals)
    _write_csv(output / "aggregate" / "confidence_intervals.csv", intervals)
    work_rows = [
        {
            "world": row.world,
            "condition": row.condition,
            "episode_id": row.episode_id,
            **row.counters["spark_update_distribution"],
            "edge_mean": row.counters["edge_evaluation_distribution"]["mean"],
        }
        for row in results
    ]
    _write_json(output / "aggregate" / "work_distributions.json", work_rows)
    _write_csv(output / "aggregate" / "work_distributions.csv", work_rows)
    _write_csv(output / "pareto" / "frontier.csv", pareto)
    _write_pareto_svg(output / "pareto" / "frontier.svg", pareto)
    failure_lines = ["# Deterministically selected Phase-1 failure cases", ""]
    for category, result in _failure_candidates(results):
        directory = output / "failures" / result.episode_id.replace(":", "_")
        _write_json(
            directory / "trace.json",
            {"episode_id": result.episode_id, "category": category, "steps": result.steps},
        )
        explanation = (
            f"# {category}\n\nSelected by the predeclared deterministic worst-case rule. "
            f"World: `{result.world}`; condition: `{result.condition}`. This is an "
            "observed synthetic failure case, not evidence of general behavior.\n"
        )
        (directory / "explanation.md").write_text(explanation, encoding="utf-8", newline="\n")
        html_rows = "".join(
            f"<tr><td>{step['step_index']}</td><td>{step['scenario_tags']}</td><td>{step['truth']}</td><td>{step['prediction']}</td><td>{step['confidence']:.3f}</td></tr>"
            for step in result.steps
        )
        (directory / "visualizer.html").write_text(
            f"<!doctype html><meta charset='utf-8'><title>{category}</title>"
            f"<h1>{category}</h1><table border='1'><tr><th>step</th><th>tags</th>"
            "<th>truth</th><th>prediction</th><th>confidence</th></tr>"
            f"{html_rows}</table>",
            encoding="utf-8",
            newline="\n",
        )
        failure_lines.append(
            f"- [{category}]({result.episode_id.replace(':', '_')}/explanation.md): "
            f"{result.world}/{result.condition}"
        )
    (output / "failures" / "index.md").write_text(
        "\n".join(failure_lines) + "\n", encoding="utf-8", newline="\n"
    )
    report = [
        "# Phase-1 Controlled Synthetic Evaluation",
        "",
        f"Episodes per declared condition: {len(seeds)}",
        "",
        "All intervals are episode-level bootstrap intervals. No physical energy claim is "
        "made. Test-set results were generated from the referenced split manifest.",
        "",
        "## Artifact links",
        "",
        "- [Raw results](raw/)",
        "- [Aggregate metrics](aggregate/metrics.csv)",
        "- [Confidence intervals](aggregate/confidence_intervals.csv)",
        "- [Pareto frontier](pareto/frontier.svg)",
        "- [Failure cases](failures/index.md)",
        "",
    ]
    (output / "report.md").write_text("\n".join(report), encoding="utf-8", newline="\n")
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=config_path.parents[3],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        commit = "unknown"
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "run_id": output.name,
        "git_commit": commit,
        "config_hash": _hash(config),
        "split_hash": _hash(split_manifest),
        "command": command,
        "local_execution": True,
        "completed": True,
        "episode_count": len(results),
        "failed_episode_count": 0,
    }
    _write_json(output / "run_manifest.json", manifest)
    _write_json(
        output / "phase1-results.json",
        {
            "schema_version": SCHEMA_VERSION,
            "aggregate": aggregates,
            "confidence_intervals": intervals,
            "pareto": pareto,
        },
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    command = " ".join(sys.argv)
    manifest = run_suite(args.config, args.output, command=command)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
