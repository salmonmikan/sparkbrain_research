from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from sparkbrain.evaluation.v061_state_factorization_diagnostics import (
    run_state_factorization_diagnosis,
)


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def build_markdown(result: dict[str, Any]) -> str:
    assessment = result["assessment"]
    lines = [
        "# SparkBrain v0.6.1 D7 State-Factorization Diagnosis",
        "",
        "## Scope",
        "",
        (
            "This is a development-only 2x2 transplant diagnosis. Candidate-003 "
            "is not rerun or rescored."
        ),
        "",
        "## Crossed state matrix",
        "",
        "| G1 transition state | Consistency state | Trajectory | Relation re-entry |",
        "|---|---|---|---|",
    ]
    for row in result["cells"]:
        lines.append(
            "| "
            f"{row['transition_label']} | {row['consistency_label']} | "
            f"{row['trajectory_units']} | {row['relation_reentry_units']} |"
        )
    lines.extend(
        [
            "",
            "## Assessment",
            "",
            "```text",
            (
                "transition changes trajectory: "
                f"{assessment['transition_changes_trajectory']}"
            ),
            (
                "consistency changes relation expression: "
                f"{assessment['consistency_changes_relation_expression']}"
            ),
            (
                "trajectory invariant under consistency swap: "
                f"{assessment['trajectory_invariant_under_consistency_swap']}"
            ),
            (
                "relation expression invariant under transition swap: "
                f"{assessment['relation_expression_invariant_under_transition_swap']}"
            ),
            (
                "full Cartesian factorization: "
                f"{assessment['full_cartesian_factorization']}"
            ),
            (
                "missing consistency-to-trajectory edge supported: "
                f"{assessment['missing_consistency_to_trajectory_edge_supported']}"
            ),
            "candidate-003 executions: 0",
            "```",
            "",
            "## Interpretation",
            "",
            assessment["interpretation"],
            "",
            (
                "The result does not say that G1 or consistency is semantically typed. "
                "Both remain anonymous. It says that the current Primary stores branch "
                "organization and external-relation organization in two separable explicit "
                "state systems. Their outputs meet again in the Field, but external "
                "consistency does not currently revise which G1 trajectory wins."
            ),
            "",
            (
                "This identifies the missing SparkBrain loop more precisely than a generic "
                "memory deficit: world interaction can change later relation-driven Sparks, "
                "but it cannot yet reorganize the earlier anonymous trajectory competition "
                "that determines which internal path reaches the world."
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
    result = run_state_factorization_diagnosis()
    _write_json(args.output_dir / "d7_state_factorization.json", result)
    report = build_markdown(result)
    (args.output_dir / "D7_STATE_FACTORIZATION.md").write_text(
        report,
        encoding="utf-8",
    )
    print(report)


if __name__ == "__main__":
    main()
