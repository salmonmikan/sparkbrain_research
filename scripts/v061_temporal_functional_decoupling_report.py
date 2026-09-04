from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from sparkbrain.evaluation.v061_temporal_functional_decoupling import (
    canonical_relation_counterfactuals,
    canonical_temporal_counterfactuals,
)


def build_report() -> dict[str, Any]:
    temporal = {
        key: value.state_dict()
        for key, value in canonical_temporal_counterfactuals().items()
    }
    relation = {
        key: value.state_dict()
        for key, value in canonical_relation_counterfactuals().items()
    }
    return {
        "candidate_003_reexecuted": False,
        "diagnostic_scope": "observer-only development counterfactuals",
        "runtime_modified": False,
        "temporal_branch_counterfactuals": temporal,
        "relation_expression_counterfactuals": relation,
        "mechanistic_conclusions": {
            "trajectory_selection": (
                "The anonymous G1 selector can prefer a less exposed and "
                "world-inconsistent branch when that branch has lower lag variance."
            ),
            "relation_storage": (
                "A relation can be the dominant stored link while still failing "
                "to generate a normally thresholded Field Spark."
            ),
            "relation_superposition": (
                "More than one sufficiently reliable anonymous relation can be "
                "expressed at once because the current re-entry path has no "
                "competition or convergence stage."
            ),
            "central_gap": (
                "Local temporal stability and later anonymous world consistency "
                "are measured in separate state systems and are not jointly used "
                "to organize future trajectory competition."
            ),
        },
        "claim_boundary": (
            "This report diagnoses the frozen mechanism. It neither rescues the "
            "candidate-003 result nor proposes a pass-oriented threshold change."
        ),
    }


def _markdown(report: dict[str, Any]) -> str:
    temporal = report["temporal_branch_counterfactuals"]
    relation = report["relation_expression_counterfactuals"]
    rows = [
        "# v0.6.1 Temporal–Functional Decoupling Diagnostic",
        "",
        "## Scope",
        "",
        "Observer-only development counterfactuals. Candidate-003 was not re-executed, "
        "and no Primary runtime parameter or decision threshold was changed.",
        "",
        "## Temporal branch counterfactuals",
        "",
        "| Case | G1 selection | Exposure winner | World-consistency winner | Decoupled |",
        "|---|---|---|---|---|",
    ]
    for key, value in temporal.items():
        rows.append(
            "| {case} | {g1} | {exposure} | {world} | {decoupled} |".format(
                case=key,
                g1=value["selected_by_g1"],
                exposure=value["selected_by_exposure"],
                world=value["selected_by_world_consistency"],
                decoupled=value["temporal_functional_decoupling"],
            )
        )
    rows.extend(
        (
            "",
            "The decoupled case keeps the world-consistent and most exposed branch fixed as "
            "`main`, but moves lag variance from `alternate` to `main`. The G1 winner flips "
            "to `alternate`. Equalizing variance returns selection to the frequency winner.",
            "",
            "## Relation storage and expression counterfactuals",
            "",
            (
                "| Case | Stored dominant | Expressed targets | Storage correct | "
                "Abstention | Superposition |"
            ),
            "|---|---|---|---|---|---|",
        )
    )
    for key, value in relation.items():
        rows.append(
            (
                "| {case} | {dominant} | {expressed} | {stored} | {abstention} | "
                "{superposition} |"
            ).format(
                case=key,
                dominant=value["dominant_target"],
                expressed=", ".join(value["expressed_targets"]) or "—",
                stored=value["storage_matches_world"],
                abstention=value["expression_abstention"],
                superposition=value["multi_link_superposition"],
            )
        )
    rows.extend(
        (
            "",
            "## Mechanistic conclusion",
            "",
            (
                "The current Primary has two locally meaningful but disconnected "
                "anonymous state systems:"
            ),
            "",
            "```text",
            "local transition frequency + lag stability",
            "    -> trajectory confidence",
            "",
            "world-return consistency",
            "    -> relation reliability",
            "    -> later relation re-entry",
            "```",
            "",
            "World consistency does not reorganize the earlier shared-root trajectory competition. "
            "Conversely, relation re-entry can abstain or co-express multiple links after storage. "
            "The central failure is therefore not merely a bad threshold: it is a missing "
            "endogenous coordination process between temporal trajectory formation, anonymous "
            "world relation, and subsequent Field expression.",
            "",
            "## Claim boundary",
            "",
            report["claim_boundary"],
            "",
        )
    )
    return "\n".join(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path)
    parser.add_argument("--markdown", type=Path)
    args = parser.parse_args()
    report = build_report()
    if args.json is not None:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(
            json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.markdown is not None:
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text(_markdown(report), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
