from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from sparkbrain.evaluation.v061_field_expression_diagnostics import (
    run_field_expression_diagnosis,
)


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def build_markdown(result: dict[str, Any]) -> str:
    assessment = result["assessment"]
    lines = [
        "# SparkBrain v0.6.1 D8 Field-Expression Role Diagnosis",
        "",
        "## Scope",
        "",
        (
            "This development-only diagnosis keeps learned anonymous G1 or "
            "consistency state fixed and changes only the Field expression "
            "conditions. Candidate-003 is not rerun or rescored."
        ),
        "",
        "## Fixed G1 state under different Field conditions",
        "",
        (
            "| Condition | Threshold | Proposals | Generated Spark units | "
            "Trajectory class |"
        ),
        "|---|---:|---|---|---|",
    ]
    for row in result["transition_conditions"]:
        lines.append(
            "| "
            f"{row['condition']} | {row['field_threshold']:.3f} | "
            f"{tuple(row['proposal_targets'])} | "
            f"{tuple(row['generated_units'])} | "
            f"{row['trajectory_class']} |"
        )
    lines.extend(
        [
            "",
            "## Fixed consistency state under different Field conditions",
            "",
            "| Condition | Threshold | Proposal targets | Endogenous output |",
            "|---|---:|---|---|",
        ]
    )
    for row in result["relation_conditions"]:
        lines.append(
            "| "
            f"{row['condition']} | {row['field_threshold']:.3f} | "
            f"{tuple(row['proposal_targets'])} | "
            f"{tuple(row['endogenous_output_units'])} |"
        )
    lines.extend(
        [
            "",
            "## Assessment",
            "",
            "```text",
            (
                "proposal identity invariant: "
                f"{assessment['proposal_identity_invariant_across_field_conditions']}"
            ),
            (
                "readout without Spark: "
                f"{assessment['readout_without_reinjection_has_no_endogenous_spark']}"
            ),
            (
                "threshold changes trajectory expression: "
                f"{assessment['threshold_changes_trajectory_expression']}"
            ),
            (
                "residual state rescues branch: "
                f"{assessment['residual_state_rescues_subthreshold_branch']}"
            ),
            (
                "refractory state suppresses branch: "
                f"{assessment['refractory_state_suppresses_selected_branch']}"
            ),
            (
                "Field active expression substrate: "
                f"{assessment['field_active_expression_substrate_supported']}"
            ),
            (
                "Field learned organizer: "
                f"{assessment['field_learned_organizer_supported']}"
            ),
            (
                "distributed Field memory: "
                f"{assessment['distributed_field_memory_supported']}"
            ),
            "candidate-003 executions: 0",
            "```",
            "",
            "## Interpretation",
            "",
            assessment["interpretation"],
            "",
            (
                "The diagnosis rejects both extreme descriptions. The Field is "
                "not merely a visualization layer because its ordinary threshold, "
                "residual potential, and refractory state determine which proposed "
                "events become real Sparks. But it is also not presently the learned "
                "organizer: branch identity and external-relation identity remain in "
                "separable explicit anonymous state systems."
            ),
            "",
            (
                "The current architecture is therefore better described as an "
                "active excitable expression medium driven by explicit anonymous "
                "learned organizers. The unresolved SparkBrain question is whether "
                "those organizers can become endogenous consequences of Field/world "
                "Dynamics rather than permanent hand-separated state tables."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    result = run_field_expression_diagnosis()
    _write_json(args.output_dir / "d8_field_expression.json", result)
    report = build_markdown(result)
    (args.output_dir / "D8_FIELD_EXPRESSION.md").write_text(
        report,
        encoding="utf-8",
    )
    print(report)


if __name__ == "__main__":
    main()
