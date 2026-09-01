from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from sparkbrain.evaluation.v061_comparator_contrast import (
    run_comparator_contrast,
)
from sparkbrain.evaluation.v061_failure_locus_diagnostics import (
    run_failure_locus_suite,
)


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _locus_section(locus: dict[str, Any]) -> list[str]:
    lines = [
        "## D5 — Failure-state locus",
        "",
        "```text",
        f"transition worlds: {locus['transition_world_count']}",
        (
            "trajectory class transferred with G1: "
            f"{locus['transition_failure_transfers_with_g1_count']}"
        ),
        (
            "G1 reset removed expression: "
            f"{locus['transition_g1_reset_removes_expression_count']}"
        ),
        (
            "carried Field state alone transferred trajectory: "
            f"{locus['transition_field_state_alone_transfer_count']}"
        ),
        f"relation worlds: {locus['relation_world_count']}",
        (
            "relation failure replayed on fresh Field: "
            f"{locus['relation_failure_replays_in_fresh_field_count']}"
        ),
        (
            "consistency reset removed expression: "
            f"{locus['relation_reset_removes_expression_count']}"
        ),
        "candidate-003 executions: 0",
        "```",
        "",
        "### Transition state transfer",
        "",
        "| World | Baseline | G1 transplant | G1 reset | Field-only |",
        "|---|---|---|---|---|",
    ]
    for row in locus["transitions"]:
        lines.append(
            "| "
            f"{row['family_id']} | {row['baseline_trajectory_class']} | "
            f"{row['expectation_transplant_class']} | "
            f"{row['expectation_reset_units']} | "
            f"{row['field_state_only_units']} |"
        )
    lines.extend(
        [
            "",
            "### Relation failure transfer",
            "",
            "| Pattern | First failure | Source output | Fresh Field replay | Reset |",
            "|---|---|---|---|---|",
        ]
    )
    for row in locus["relations"]:
        lines.append(
            "| "
            f"{row['factor_value']} | {row['source_failure_stage']} | "
            f"{row['source_output_units']} | "
            f"{row['fresh_field_replay_output_units']} | "
            f"{row['reset_consistency_output_units']} |"
        )
    lines.extend(
        [
            "",
            "The present failure classes move with explicit anonymous G1 transition "
            "state or anonymous consistency state into fresh Fields. A carried Field "
            "state without those learned components does not recreate the trajectory. "
            "This localizes current learned failure structure outside the Field itself, "
            "while leaving ordinary Field thresholding as the expression mechanism.",
            "",
        ]
    )
    return lines


def _contrast_section(contrast: dict[str, Any]) -> list[str]:
    primary = contrast["primary"]
    lines = [
        "## D6 — Comparator temporal abstraction contrast",
        "",
        "The compared worlds contain identical paths, exposure counts, and the same "
        "multiset of lag profiles. Only the chronological lag-profile order differs.",
        "",
        "```text",
        f"same paths: {contrast['same_paths']}",
        f"same exposure counts: {contrast['same_exposure_counts']}",
        f"same lag-profile multiset: {contrast['same_lag_profile_multiset']}",
        f"same lag-profile order: {contrast['lag_profile_order_equal']}",
        (
            "all comparators quotient lag order: "
            f"{contrast['all_comparators_quotient_lag_order']}"
        ),
        (
            "Primary retains lag order in state/expression: "
            f"{contrast['primary_retains_lag_order_in_state_and_expression']}"
        ),
        "candidate-003 executions: 0",
        "```",
        "",
        "| System | Learned state equal | Output equal | Time values represented |",
        "|---|---:|---:|---:|",
        (
            "| Primary G1 | "
            f"{primary['learned_state_equal']} | {primary['trajectory_equal']} | true |"
        ),
    ]
    for row in contrast["comparators"]:
        lines.append(
            "| "
            f"{row['condition']} | {row['learned_state_equal']} | "
            f"{row['output_equal']} | "
            f"{row['lag_profile_values_represented_in_learned_state']} |"
        )
    lines.extend(
        [
            "",
            "Comparator success in lag-dispersion is therefore not evidence that G3, "
            "G4, or G5 processed the same temporal Dynamics more robustly. Their sequence "
            "wrappers form a time-quotiented problem: chronology is discarded while path "
            "identity and exposure count remain. Primary retains temporal moments and can "
            "therefore both exploit and be destabilized by lag order.",
            "",
        ]
    )
    return lines


def build_markdown(locus: dict[str, Any], contrast: dict[str, Any]) -> str:
    lines = [
        "# SparkBrain v0.6.1 D5-D6 Failure Diagnostics",
        "",
        "## Scope",
        "",
        "These are development-only reset/transplant and abstraction diagnostics. "
        "Candidate-003 is not rerun or rescored, and the frozen negative verdict is "
        "unchanged.",
        "",
        *_locus_section(locus),
        *_contrast_section(contrast),
        "## Current theoretical boundary",
        "",
        "The present evidence does not support distributed learned memory in the Field. "
        "It supports a Dynamic Field that expresses influences carried by explicit, "
        "anonymous G1 transition statistics and anonymous consistency links. The Field "
        "still matters for thresholding, concurrency, residual integration, and actual "
        "Spark formation, but the learned branch and relation organization currently "
        "resides outside the Field state.",
        "",
        "The comparator contrast also prevents a misleading conclusion: comparator-only "
        "formal success does not establish better temporal cognition when comparator "
        "adapters omit the temporal values that destabilize Primary. It establishes that "
        "the frozen tasks remain solvable after time is abstracted away.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    locus = run_failure_locus_suite()
    contrast = run_comparator_contrast()
    _write_json(args.output_dir / "d5_failure_locus.json", locus)
    _write_json(args.output_dir / "d6_comparator_contrast.json", contrast)
    report = build_markdown(locus, contrast)
    (args.output_dir / "D5_D6_FAILURE_DIAGNOSTICS.md").write_text(
        report,
        encoding="utf-8",
    )
    print(report)


if __name__ == "__main__":
    main()
