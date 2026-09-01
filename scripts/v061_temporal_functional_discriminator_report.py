from __future__ import annotations

import argparse
import json
from pathlib import Path

from sparkbrain.evaluation.v061_temporal_functional_discriminators import (
    build_discriminator_report,
)


def _markdown(report: dict[str, object]) -> str:
    lag = report["lag_assignment_permutation"]
    consequence = report["consequence_permutation"]
    cross = report["storage_expression_cross"]
    ambiguity = report["ambiguity"]
    assert isinstance(lag, dict)
    assert isinstance(consequence, dict)
    assert isinstance(cross, dict)
    assert isinstance(ambiguity, dict)
    return "\n".join(
        (
            "# v0.6.1 D8 — Temporal–Functional Causal Discriminators",
            "",
            "## Scope",
            "",
            "These are observer-only development counterfactuals. Candidate-003 is not "
            "re-executed and the Primary runtime is unchanged.",
            "",
            "## D8-A — Lag-profile ownership permutation",
            "",
            "The total lag multiset, exposure counts, branch identities, and anonymous "
            "world-consistency winner are preserved. Only lag ownership is permuted.",
            "",
            "```text",
            f"assignment A G1 winner: {lag['assignment_a']['selected_by_g1']}",
            f"assignment B G1 winner: {lag['assignment_b']['selected_by_g1']}",
            f"selection flipped:       {lag['g1_selection_flipped']}",
            "```",
            "",
            "This supports a causal role for lag-profile assignment in current G1 branch "
            "selection, independently of world consistency.",
            "",
            "## D8-B — Consequence permutation after fixed local evidence",
            "",
            "```text",
            f"local evidence identical:       {consequence['local_transition_evidence_identical']}",
            f"world-consistency winner changed:{consequence['world_consistency_winner_changed']}",
            f"G1 selection unchanged:          {consequence['g1_selection_unchanged']}",
            "```",
            "",
            "The current G1 selector cannot respond to a changed anonymous world relation "
            "because that evidence is not part of its state update or competition rule.",
            "",
            "## D8-C — Relation storage / Field-expression cross",
            "",
            "The relation link and reliability are held fixed while only the Field "
            "expression demand changes.",
            "",
            "```text",
            f"stored state identical:       {cross['stored_state_identical']}",
            f"dominant relation identical:  {cross['dominant_relation_identical']}",
            f"expression changed:            {cross['expression_changed']}",
            f"expression bottleneck shown:   {cross['expression_bottleneck_demonstrated']}",
            "```",
            "",
            "This demonstrates that correct relation storage is neither identical to nor "
            "sufficient for later Field expression.",
            "",
            "## D8-D — Equal-evidence ambiguity",
            "",
            "```text",
            f"co-maximal branches: {ambiguity['co_maximal_branches']}",
            f"exact confidence tie:{ambiguity['exact_confidence_tie']}",
            "```",
            "",
            "The local evidence defines a genuine tie. A singleton named by reporting order "
            "must not be mistaken for an internally justified winner. Future SparkBrain "
            "experiments must distinguish bounded coexistence from arbitrary ID tie-breaking.",
            "",
            "## Combined conclusion",
            "",
            "The current failure is best represented as a missing causal circulation:",
            "",
            "```text",
            "local temporal evidence",
            "    -> G1 trajectory competition",
            "    -> Field / boundary / world",
            "    -> anonymous relation evidence",
            "    -X-> future G1 trajectory competition",
            "```",
            "",
            "The crossed arrow is the current architectural gap. Threshold tuning can alter "
            "whether stored relations are expressed, but it cannot create anonymous causal "
            "credit from world interaction back to the earlier trajectory competition.",
            "",
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path)
    parser.add_argument("--markdown", type=Path)
    args = parser.parse_args()
    report = build_discriminator_report()
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
