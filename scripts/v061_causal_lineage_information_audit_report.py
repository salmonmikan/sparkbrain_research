from __future__ import annotations

import argparse
import json
from pathlib import Path

from sparkbrain.evaluation.v061_causal_lineage_information_audit import (
    audit_causal_lineage_information,
)


def _markdown(report: dict[str, object]) -> str:
    boundary = report["boundary_event"]
    consistency = report["consistency_classes"]
    assert isinstance(boundary, dict)
    assert isinstance(consistency, list)
    rows = [
        "# v0.6.1 D10 — Causal Lineage Information-Loss Audit",
        "",
        "## Scope",
        "",
        "Static observer-side source audit. Candidate-003 is not re-executed and the "
        "Primary runtime is not modified.",
        "",
        "## Outbound boundary lineage",
        "",
        "`BoundaryEvent` retains:",
        "",
        "```text",
        *[str(value) for value in boundary["lineage_fields"]],
        "```",
        "",
        "The outbound event therefore has enough information to identify the Spark, "
        "unit, proposal lineage, generation depth, and source state that reached the "
        "world boundary.",
        "",
        "## Consistency compression",
        "",
        "| State class | Stored fields | Proposal/path return address |",
        "|---|---|---|",
    ]
    for item in consistency:
        assert isinstance(item, dict)
        rows.append(
            "| {name} | {fields} | {return_address} |".format(
                name=item["class_name"],
                fields=", ".join(item["fields"]),
                return_address=(", ".join(item["return_address_fields"]) or "—"),
            )
        )
    rows.extend(
        (
            "",
            "## Audit result",
            "",
            "```text",
            f"boundary has causal lineage: {report['boundary_has_causal_lineage']}",
            "consistency retains proposal return address: "
            f"{report['consistency_retains_proposal_return_address']}",
            "register_boundary consumes return address: "
            f"{report['register_boundary_consumes_proposal_return_address']}",
            "re-entry recovers historical return address: "
            f"{report['relation_reentry_recovers_original_return_address']}",
            f"lineage information loss confirmed: {report['lineage_information_loss_confirmed']}",
            f"first loss boundary: {report['first_loss_boundary']}",
            "```",
            "",
            "## Mechanistic interpretation",
            "",
            "The current architecture does not merely lack an update call from anonymous "
            "world consistency to G1. It loses the historical return address needed to "
            "make such an update causally selective.",
            "",
            "```text",
            "endogenous proposal/path lineage",
            "    -> Spark",
            "    -> BoundaryEvent  [lineage still present]",
            "    -> PendingBoundaryExposure / AnonymousLinkState",
            "                     [proposal/path return address discarded]",
            "    -> external consistency reliability",
            "    -> relation re-entry from compressed relation",
            "````",
            "",
            "Relation re-entry may attach a current boundary lineage to a newly generated "
            "proposal. That does not reconstruct the historical local lineage whose prior "
            "world consequence established the relation. The stored relation can therefore "
            "support a target, but it cannot identify which earlier local temporal process "
            "should receive externally evidenced credit or contradiction.",
            "",
            "## Consequence for future SparkBrain hypotheses",
            "",
            "A future anonymous feedback mechanism needs a bounded, expiring causal return "
            "address across the world boundary. Retaining it is not sufficient by itself: "
            "the mechanism must still pass lineage-swap, matched-correlation, contradiction, "
            "self-confirmation, reset/transplant, and explicit-table-equivalence tests.",
            "",
            "The return address must not contain semantic role, reward, correct action, or "
            "an evaluator-selected target. It may identify only anonymous causal lineage.",
            "",
        )
    )
    return "\n".join(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--json", type=Path)
    parser.add_argument("--markdown", type=Path)
    args = parser.parse_args()
    report = audit_causal_lineage_information(args.root).state_dict()
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
