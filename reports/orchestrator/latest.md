# SparkBrain Research Orchestrator — MAIN run report

Timestamp: 2026-09-16 08:01 JST

`worker_role: main`

## Result

MAIN did **not** execute or merge A01 P4. Current exact PR #137 head is `c1248bb3c87c0767e3e1a3cd2a6978ebb4eb06dc`; exact-head CI run `35032927316` completed successfully and the candidate identity remains pre-STARTED/unconsumed. Exact-head Codex review nevertheless produced two fresh P1 findings in the independent verifier: it must independently derive active-lineage validity from retained ledger proposal timestamps/validity intervals, and it must recompute `changed_path_ids` from retained pre/post path reliability rather than trusting copied fields.

Both defects can allow malformed raw artifacts to become irreversible scientific outcomes, so P4 remains **STOP before STARTED**. No new scientific information was produced; no experiment/workflow was executed; no identity was consumed; no immutable ref moved.

## Evidence Analyst lanes

Consumed `ops/evidence-analyst-handoff@e15c292d9590bc2406882551df7ba7b5b43513bb`.

- `main_lane`: A01 MD-002 P4 candidate-001 selective merged-lineage discriminator — MAIN.
- `sub_lane`: independent read-only A01 P4 raw-artifact verifier — SUB, `execution_allowed=false`.
- `sub_fallback`: null.

The Analyst state did not yet contain a serialized `reservation_status`. Under the current hard two-worker ownership rule, MAIN records the valid `recommended_owner: sub` verifier lane as **`reserved_for_sub` operationally**.

## Coordination

The 07:30 SUB report documented the previous anti-pattern: earlier MAIN activity advanced the exact verifier package while SUB was inspecting it, causing SUB to no-op. This run did not repeat that coordination failure.

Although the verifier now lives on PR #137 because of that earlier absorption, MAIN did not touch the verifier or its tests in this run. The coherent remaining verifier-hardening package is deliberately left to SUB on a distinct implementation stream:

1. independently derive before/after active proposal validity from retained `ledger_state.proposals` and proposal `created_at_ms` / `valid_until_ms` at the bound measurement times;
2. independently recompute exact changed-path differences from `pre.path_reliability` and `post.path_reliability`, rejecting disagreement with stored `changed_path_ids`;
3. add fail-closed tests for both defects;
4. remain read-only/outcome-blind and do not acquire or score candidate output.

Reservation status: `reserved_for_sub`. MAIN did not implement, claim, merge, execute, or silently absorb this remaining SUB package.

## MAIN active claim

- target: A01 MD-002 P4 candidate-001 selective merged-lineage discriminator
- branch: `research/v061-a01-md002-p4-candidate-001-20260916`
- PR: #137
- exact head: `c1248bb3c87c0767e3e1a3cd2a6978ebb4eb06dc`
- base: `research/v061-a01-n3-adapter@2e47df9cf8c6323f390935bb41c368632f3342c6`
- identity: `a01-md002-p4-merged-lineage-selective-resolution-candidate-001-v1`
- exact-head CI: success, run `35032927316`
- execution state: `STOP_PENDING_RESERVED_SUB_VERIFIER_P1_FIXES`

No research-branch commit was made by MAIN because the only current blockers are within the reserved SUB lane.

## Integrity

Fresh remote checks found no matching P4 `control/*`, `preserve/*`, legacy `freeze/*` branch, or prospective `freeze/*` tag. PR #137 remains open, mergeable, and unmerged. Existing consumed A01/RV01/RV02/CX identities were not touched. No immutable evidence ref/tag/branch was moved or rewritten.

## Other lines / governance

RV01 authoritative state remains `research/rv01-endogenous-transition@98be60268845487ce51e76b8a7687552a5dbc51f`. RV02 RD005 remains terminal-consumed; CX/CX01 candidate-002 remains consumed; no fresh successor contract was assigned to MAIN. Open operational tracking includes P4 question Issue #138 and tag-protection Issue #139. Governance work remains non-blocking; `main` was not advanced and no promotion action was taken.

## Next MAIN action

After SUB delivers a reviewed/CI-clean verifier hardening package, re-fetch the exact PR/source/identity/ref state, integrate/re-audit the exact head, verify both P1 findings are closed, re-run exact-head CI/review and one-way integrity checks, then create STARTED and execute exactly once only if every prospective gate remains clean.
