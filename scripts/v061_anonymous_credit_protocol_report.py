from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from sparkbrain.evaluation.v061_anonymous_credit_diagnostic_protocol import (
    CausalCreditObservation,
    EvidenceSource,
    WorldRelationPermutationTrial,
    assess_causal_credit_trial,
    assess_world_relation_permutation,
    build_causal_credit_protocol_matrix,
)


def _current_structure_observation(trial_id: str, source: EvidenceSource):
    return CausalCreditObservation(
        trial_id=trial_id,
        causal_lineage_update=0.0,
        matched_lineage_update=0.0,
        external_observation_count_delta=(
            1
            if source
            in {
                EvidenceSource.EXTERNAL_MATCH,
                EvidenceSource.EXTERNAL_CONTRADICTION,
            }
            else 0
        ),
        positive_commit_count_delta=0,
    )


def _hypothetical_selective_observation(trial_id: str, source: EvidenceSource):
    if source is EvidenceSource.EXTERNAL_MATCH:
        return CausalCreditObservation(
            trial_id=trial_id,
            causal_lineage_update=1.0,
            matched_lineage_update=0.0,
            external_observation_count_delta=1,
            positive_commit_count_delta=1,
        )
    if source is EvidenceSource.EXTERNAL_CONTRADICTION:
        return CausalCreditObservation(
            trial_id=trial_id,
            causal_lineage_update=-1.0,
            matched_lineage_update=0.0,
            external_observation_count_delta=1,
            positive_commit_count_delta=0,
        )
    return CausalCreditObservation(
        trial_id=trial_id,
        causal_lineage_update=0.0,
        matched_lineage_update=0.0,
        external_observation_count_delta=0,
        positive_commit_count_delta=0,
    )


def build_report() -> dict[str, Any]:
    matrix = build_causal_credit_protocol_matrix()
    current = tuple(
        assess_causal_credit_trial(
            trial,
            _current_structure_observation(trial.trial_id, trial.evidence_source),
        )
        for trial in matrix
    )
    hypothetical = tuple(
        assess_causal_credit_trial(
            trial,
            _hypothetical_selective_observation(
                trial.trial_id,
                trial.evidence_source,
            ),
        )
        for trial in matrix
    )
    p2_current = assess_world_relation_permutation(
        WorldRelationPermutationTrial(
            trial_id="fixed-local-current-primary",
            local_state_hash_before="a" * 64,
            local_state_hash_after="a" * 64,
            world_relation_before="external:1",
            world_relation_after="external:2",
            selected_lineage_before="lineage-a",
            selected_lineage_after="lineage-a",
        )
    )
    p2_required = assess_world_relation_permutation(
        WorldRelationPermutationTrial(
            trial_id="fixed-local-required-observation",
            local_state_hash_before="a" * 64,
            local_state_hash_after="a" * 64,
            world_relation_before="external:1",
            world_relation_after="external:2",
            selected_lineage_before="lineage-a",
            selected_lineage_after="lineage-b",
        )
    )
    return {
        "candidate_reexecuted": False,
        "runtime_modified": False,
        "protocol_trials": [row.state_dict() for row in matrix],
        "current_structure_baseline": [row.state_dict() for row in current],
        "hypothetical_selective_reference": [
            row.state_dict() for row in hypothetical
        ],
        "p2_current_structure": p2_current.state_dict(),
        "p2_required_observation": p2_required.state_dict(),
        "interpretation": (
            "The current downstream-only architecture is expected to fail the "
            "positive-match, lineage-swap, contradiction, and fixed-local-state "
            "world-to-transition circulation trials while retaining the external-"
            "absence and internal-only self-confirmation guards."
        ),
    }


def _markdown(report: dict[str, Any]) -> str:
    current = report["current_structure_baseline"]
    hypothetical = report["hypothetical_selective_reference"]
    current_by_id = {row["trial_id"]: row for row in current}
    hypothetical_by_id = {row["trial_id"]: row for row in hypothetical}
    rows = [
        "# v0.6.1 P1–P2 Anonymous Causal-Credit Baseline",
        "",
        "Candidate-003 is not re-executed. This report evaluates the diagnostic "
        "protocol against the current structural expectation and a hypothetical "
        "selective reference observation.",
        "",
        "| Trial | Current structure | Selective reference |",
        "|---|---|---|",
    ]
    for trial_id in current_by_id:
        rows.append(
            "| {trial} | {current} ({current_reason}) | {reference} ({reference_reason}) |".format(
                trial=trial_id,
                current=current_by_id[trial_id]["accepted"],
                current_reason=current_by_id[trial_id]["reason"],
                reference=hypothetical_by_id[trial_id]["accepted"],
                reference_reason=hypothetical_by_id[trial_id]["reason"],
            )
        )
    rows.extend(
        (
            "",
            "## P2 fixed-local-state relation permutation",
            "",
            "```text",
            "current structure circulation observed: "
            f"{report['p2_current_structure']['world_to_transition_circulation_observed']}",
            "required discriminating observation:     "
            f"{report['p2_required_observation']['world_to_transition_circulation_observed']}",
            "```",
            "",
            "The protocol does not prescribe an eligibility trace, Field trace, or "
            "gain rule. It defines what any future anonymous mechanism must demonstrate "
            "and what self-confirming or merely correlated behavior must fail.",
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
