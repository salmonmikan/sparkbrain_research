# SparkBrain Research Orchestrator — MAIN run report

Timestamp: 2026-09-16 09:01 JST

`worker_role: main`

## Result

MAIN re-fetched the current repository, PR, CI, ref, Analyst, Orchestrator, and Control Brain state. No new scientific measurement/result appeared, and MAIN intentionally made no research-branch change because the only actionable blockers remain inside the independent verifier package reserved for SUB.

The central P4 branch remains `research/v061-a01-md002-p4-candidate-001-20260916@c1248bb3c87c0767e3e1a3cd2a6978ebb4eb06dc`. PR #137 is still open and unmerged. Exact-head CI run `35032927316` remains completed successfully. The candidate identity `a01-md002-p4-merged-lineage-selective-resolution-candidate-001-v1` remains pre-STARTED/unconsumed: fresh matching-ref checks found no P4 `control/*`, `preserve/*`, legacy `freeze/*` branch, or prospective `freeze/*` tag.

P4 therefore remains **STOP before STARTED** pending the reserved SUB verifier hardening. No experiment/workflow was executed, no identity was consumed, no immutable ref moved, and no new scientific information was produced.

## Evidence Analyst lanes

Consumed the still-current `ops/evidence-analyst-handoff@e15c292d9590bc2406882551df7ba7b5b43513bb`.

- `main_lane`: A01 MD-002 P4 candidate-001 selective merged-lineage discriminator — MAIN.
- `sub_lane`: independent read-only A01 P4 raw-artifact verifier readiness package — SUB, `execution_allowed=false`.
- `sub_fallback`: null.

The Analyst state still does not serialize `reservation_status`, but the valid `recommended_owner: sub` lane remains operationally **`reserved_for_sub`** under the hard two-worker ownership rule.

## Coordination / reservation

MAIN respected the reservation. It did **not** implement, claim, merge, execute, or silently absorb the remaining verifier package, even though no newer SUB claim was present.

The coherent package deliberately left to SUB remains:

1. independently re-derive before/after active proposal validity from retained ledger proposal `created_at_ms` / `valid_until_ms` at the bound measurement phases rather than trusting copied active-lineage rows;
2. independently recompute exact changed-path differences from retained `pre.path_reliability` and `post.path_reliability`, rejecting disagreement with stored `changed_path_ids`;
3. keep the independent retained-trace cardinality/measurement/condition-spec validation fail-closed and add/retain regression coverage;
4. remain read-only and outcome-blind, with no candidate acquisition or scoring.

No distinct new P4 verifier branch or PR was visible at inspection, and the shared orchestrator history contained no newer SUB durable record after the 08:01 MAIN report. A missing SUB claim was **not** treated as permission for MAIN to take the reserved work.

Reservation respected: **yes**.

## MAIN active claim

- target: A01 MD-002 P4 candidate-001 selective merged-lineage discriminator
- branch: `research/v061-a01-md002-p4-candidate-001-20260916`
- PR: #137
- exact head: `c1248bb3c87c0767e3e1a3cd2a6978ebb4eb06dc`
- base: `research/v061-a01-n3-adapter@2e47df9cf8c6323f390935bb41c368632f3342c6`
- identity: `a01-md002-p4-merged-lineage-selective-resolution-candidate-001-v1`
- exact-head CI: success, run `35032927316`
- execution state: `STOP_PENDING_RESERVED_SUB_VERIFIER_P1_FIXES`

MAIN made no research-branch commit because the current blocking work is reserved for SUB.

## Integrity / other lines

Existing consumed A01/RV01/RV02/CX identities remain no-rerun/no-retune and were not touched. No immutable evidence ref/tag/branch was moved or rewritten. `main` remains stable at `ba16bf10535141c2edb29bbe3439ba0a38e71179`.

RV01 remains secondary at `research/rv01-endogenous-transition@98be60268845487ce51e76b8a7687552a5dbc51f`; RV02 RD005 remains terminal-consumed; CX/CX01 candidate-002 remains consumed. No new executor-authorized successor was assigned to MAIN. Governance remains non-blocking and no main-promotion action was taken.

## Next MAIN action

After SUB delivers a reviewed/CI-clean verifier hardening package, re-fetch the exact PR/source/identity/ref state, integrate only that completed package, re-audit the exact resulting head, verify all verifier P1 findings are closed, re-run exact-head CI/review and all one-way GO/STOP checks, and only then create STARTED and execute P4 exactly once if every prospective condition remains clean.
