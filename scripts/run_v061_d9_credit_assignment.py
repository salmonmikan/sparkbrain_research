from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from sparkbrain.evaluation.v061_credit_assignment_diagnostics import (
    run_credit_assignment_diagnosis,
)


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def build_markdown(result: dict[str, Any]) -> str:
    assessment = result["assessment"]
    lineage = result["runtime_lineage"]
    probe = result["direct_g2_probe"]
    lines = [
        "# SparkBrain v0.6.1 D9 Anonymous Credit-Continuity Audit",
        "",
        "## Scope",
        "",
        (
            "This development-only audit follows one anonymous internal trajectory "
            "through an actual Field Spark, outbound boundary event, world return, "
            "and consistency resolution. Candidate-003 is not rerun or rescored."
        ),
        "",
        "## Runtime causal chain",
        "",
        "```text",
        f"terminal Spark:       {lineage['terminal_spark_id']}",
        f"terminal proposals:   {tuple(lineage['terminal_proposal_ids'])}",
        f"proposal ancestry:    {tuple(lineage['proposal_ancestry'])}",
        f"anonymous local paths:{tuple(lineage['local_path_ids'])}",
        (
            "boundary event:      "
            f"{lineage['boundary_event']['event_id']}"
        ),
        f"world external:      {lineage['world_external']['event_id']}",
        (
            "consistency link:   "
            f"{lineage['consistency_resolution']['link_id']}"
        ),
        "```",
        "",
        "The complete route is reconstructible while runtime and audit objects coexist:",
        "",
        "```text",
        "local path",
        "  -> proposal",
        "  -> actual endogenous Spark",
        "  -> boundary event",
        "  -> raw external event",
        "  -> anonymous consistency resolution",
        "```",
        "",
        "## Persistence boundary",
        "",
        "```text",
        (
            "world pulse directly carries local path IDs: "
            f"{assessment['world_pulse_carries_local_path_ids_directly']}"
        ),
        (
            "learned consistency retains proposal IDs: "
            f"{assessment['learned_consistency_retains_proposal_ids']}"
        ),
        (
            "learned consistency retains local path IDs: "
            f"{assessment['learned_consistency_retains_local_path_ids']}"
        ),
        (
            "G2 terminal eligibility exists: "
            f"{assessment['g2_eligibility_exists_for_terminal_path']}"
        ),
        (
            "world consequence commits that eligibility: "
            f"{assessment['g2_eligibility_committed_by_world_consequence']}"
        ),
        (
            "world consequence updates G2 path: "
            f"{assessment['g2_path_adaptation_updated_by_world_consequence']}"
        ),
        (
            "automatic world-to-G2 resolution: "
            f"{assessment['automatic_world_to_g2_resolution_present']}"
        ),
        "```",
        "",
        "## Direct G2 semantic mismatch",
        "",
        "```text",
        f"local proposal target: {probe['proposal_target']}",
        f"world return target:    {probe['external_target']}",
        f"direct G2 matched:      {probe['matched']}",
        f"confidence before:      {probe['confidence_before']}",
        f"confidence after:       {probe['confidence_after']}",
        "```",
        "",
        (
            "G2 is designed to validate a local predicted target against a later "
            "external event with the same target. A downstream world consequence "
            "is structurally caused by the chain but is not the same local target; "
            "feeding it directly into G2 therefore produces contradiction rather "
            "than anonymous distal credit."
        ),
        "",
        "## Assessment",
        "",
        "```text",
        (
            "transient credit information available: "
            f"{assessment['anonymous_credit_information_available_transiently']}"
        ),
        (
            "credit loop closed in learning: "
            f"{assessment['anonymous_credit_loop_closed_in_learning']}"
        ),
        "candidate-003 executions: 0",
        "```",
        "",
        "## Interpretation",
        "",
        assessment["interpretation"],
        "",
        (
            "The missing SparkBrain mechanism is therefore not the complete absence "
            "of causal provenance. Enough anonymous provenance exists to identify "
            "which internal path produced which world interaction. The break occurs "
            "when persistent consistency learning discards that path identity and "
            "no external-return operation commits the still-local G2 eligibility."
        ),
        "",
        (
            "A future hypothesis can remain pre-semantic: it may preserve a bounded "
            "anonymous lineage eligibility from local trajectory to boundary return. "
            "But adding such a mechanism would be new SparkBrain model work, not a "
            "reinterpretation or repair of candidate-003."
        ),
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    result = run_credit_assignment_diagnosis()
    _write_json(args.output_dir / "d9_credit_assignment.json", result)
    report = build_markdown(result)
    (args.output_dir / "D9_CREDIT_ASSIGNMENT.md").write_text(
        report,
        encoding="utf-8",
    )
    print(report)


if __name__ == "__main__":
    main()
