from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from sparkbrain.evaluation.v061_lag_diagnostics import run_lag_diagnostic_suite
from sparkbrain.evaluation.v061_relation_diagnostics import (
    run_relation_diagnostic_suite,
)


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _candidate_row(world: dict[str, Any], branch: str) -> dict[str, Any] | None:
    return next(
        (row for row in world["root_candidates"] if row["branch"] == branch),
        None,
    )


def _lag_markdown(lag: dict[str, Any]) -> list[str]:
    lines = [
        "## D2 — Lag trajectory autopsy",
        "",
        "```text",
        f"development worlds: {lag['world_count']}",
        f"shared-root worlds: {lag['shared_root_world_count']}",
        "candidate-003 executions: 0",
        (
            "root-threshold prediction: "
            f"{lag['root_threshold_prediction_match_count']} / "
            f"{lag['shared_root_world_count']}"
        ),
        f"baseline absent: {lag['baseline_absent_count']}",
        f"baseline superposed: {lag['baseline_superposed_count']}",
        f"selectivity interpretable: {lag['selectivity_interpretable_count']}",
        "```",
        "",
        "| World | Factor | main ratio | alternate ratio | Sham trajectory | Baseline |",
        "|---|---|---:|---:|---|---|",
    ]
    for world in lag["worlds"]:
        main = _candidate_row(world, "main")
        alternate = _candidate_row(world, "alternate")
        lines.append(
            "| "
            f"{world['family_id']} | {world['factor_value']} | "
            f"{main['current_threshold_ratio']:.4f} | "
            f"{alternate['current_threshold_ratio']:.4f} | "
            f"{world['sham']['trajectory_class']} | "
            f"{world['causal_baseline']['baseline_status']} |"
        )
    lines.extend(
        [
            "",
            "The table records mechanism-level expression, not task success. A second "
            "trajectory is retained as superposition rather than silently counted as a "
            "wrong token. Selectivity is interpreted only when the tested main "
            "trajectory exists in the sham run.",
            "",
        ]
    )
    return lines


def _relation_markdown(relation: dict[str, Any]) -> list[str]:
    lines = [
        "## D4 — Relation storage versus Field expression",
        "",
        "```text",
        f"development worlds: {relation['world_count']}",
        f"phases: {relation['phase_count']}",
        f"storage failures: {relation['storage_failure_count']}",
        (
            "expression failures after correct storage: "
            f"{relation['expression_failure_after_correct_storage_count']}"
        ),
        f"abstentions: {relation['abstention_count']}",
        f"superpositions: {relation['superposition_count']}",
        f"exact singleton expressions: {relation['exact_singleton_count']}",
        "candidate-003 executions: 0",
        "```",
        "",
        "| Pattern | Storage match | Exact expression | Contains expected | Storage failures | Expression failures |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for world in relation["worlds"]:
        lines.append(
            "| "
            f"{world['factor_value']} | "
            f"{world['storage_match_fraction']:.3f} | "
            f"{world['exact_expression_fraction']:.3f} | "
            f"{world['contains_expected_fraction']:.3f} | "
            f"{world['storage_failure_count']} | "
            f"{world['expression_failure_after_correct_storage_count']} |"
        )
    lines.extend(
        [
            "",
            "A correct dominant relation followed by abstention or multi-Spark output is "
            "classified as an expression failure. A wrong dominant relation is classified "
            "as storage/update failure before the Field is considered.",
            "",
        ]
    )
    return lines


def build_markdown(lag: dict[str, Any], relation: dict[str, Any]) -> str:
    lines = [
        "# SparkBrain v0.6.1 D2-D4 Failure Diagnostics",
        "",
        "## Scope",
        "",
        "This report uses factor-controlled development-only worlds. It does not rerun, "
        "resume, rescore, or modify candidate-003. No capability threshold is tuned and "
        "no result in this report changes the frozen confirmatory verdict.",
        "",
        "The purpose is to identify where anonymous SparkBrain Dynamics first diverge:",
        "",
        "```text",
        "local temporal evidence",
        "  -> proposal confidence",
        "  -> Field threshold crossing",
        "  -> trajectory expression",
        "  -> causal baseline",
        "  -> anonymous relation storage",
        "  -> relation-to-Field expression",
        "```",
        "",
        *_lag_markdown(lag),
        *_relation_markdown(relation),
        "## Diagnostic boundary",
        "",
        "These experiments may support or reject mechanistic explanations. They do not "
        "promote the Primary architecture, do not make candidate-003 pass, and do not "
        "authorize a new confirmatory candidate. Any future functional-relevance loop is "
        "a new SparkBrain hypothesis and must remain separate from this observational "
        "diagnosis.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    lag = run_lag_diagnostic_suite()
    relation = run_relation_diagnostic_suite()
    _write_json(args.output_dir / "d2_d3_lag_diagnostics.json", lag)
    _write_json(args.output_dir / "d4_relation_diagnostics.json", relation)
    report = build_markdown(lag, relation)
    (args.output_dir / "D2_D4_FAILURE_DIAGNOSTICS.md").write_text(
        report,
        encoding="utf-8",
    )
    print(report)


if __name__ == "__main__":
    main()
