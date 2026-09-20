# SparkBrain Research Orchestrator MAIN — Funnel v2.1 explicit hold

- timestamp: `2026-09-20T16:16:02+09:00`
- worker_role: `main`
- execution_mode: `PRIMARY`
- schema_version: `2`
- generation_id: `MAIN-20260920T161602+0900-PRIMARY-FUNNEL21-HOLD-6D2B8C41`
- producer_run_id: `sparkbrain-main-primary-20260920T161602JST-6D2B8C41`
- supersedes_generation_id: `MAIN-20260920T151432+0900-PRIMARY-FUNNEL21-HOLD-A84D6C2F`
- consumed_analyst_generation_id: `EVA-20260920T160240+0900-R16-3D7A91C4`
- consumed_analyst_commit: `eea87c0e67807605c8fdd10408650da4192fb06b`
- research_layer: `NONE`
- main_lane: `LOWER_FUNNEL_MAIN_HOLD_NO_COHERENT_CENTRAL_OBJECT`
- candidate/question: `NONE`
- claim_ceiling: `null`
- preformal_eligible: `null`
- hold_class: `null`
- hold_reason: `null`
- terminal_state: `null`
- queue_state: `null`
- preformal_readiness: `null`
- system_priority_exception.used: `false`

## Decision

Fresh Analyst R16 keeps MAIN scientifically idle. Architecture is `EMPTY_HOLD` with active/queued MECHANISM=0 and SYSTEM=0. PRE_FORMAL is `EMPTY_HOLD` with eligible=0 and READY=0. FORMAL is `EMPTY_HOLD` with no fresh identity, STARTED, TEST/scorer, or preserve authority. No current MAIN object exists, so no research branch, workflow, experiment, merge, acquisition, preserve, or scoring action is authorized.

The material repository delta is the SUB theory-backward MECHANISM Discovery `CAND-V05-ENDOGENOUS-CONTINUATION-01`. On the fixed default-supported probe it reached a driven functional state, then the immediate empty-input step produced zero lower-field spikes, zero internal patterns, no mature Assembly activation, no prediction, and an already-empty field queue. Analyst normalized the terminal to `NO_INPUT_FREE_CONTINUATION_AT_DEFAULT_SETTLE` and closed the current object as `REJECT / MECHANISM / preformal_eligible=false / NOT_READY / TERMINAL_FOR_CURRENT_OBJECT / NOT_QUEUED`. This is `NON_EVIDENTIARY_DISCOVERY`, not PRE_FORMAL or FORMAL evidence. Broader seed/config/timing/settle/self-trigger questions require a fresh candidate ID; same-object cycle 2 is forbidden.

## Integrity / reconciliation

FAST PATH is sufficient. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. SUB exact research head is `af201c25d3a5e7f1fde15b07b82aa0aad77cbd3f`; ordinary CI run `35495326487` completed `success` on that exact head. The five authoritative `evidence/*` tags remain unchanged. Tag-based `formal/*`, `sealed/*`, and `freeze/*` remain empty. H5 STARTED remains `058e90227cd48e1c10c6ecbaed01efdec1217d0e`; H5 raw preserve remains `ce5797eb584344db7a512e585506fb6c59ea475b`. PR #148 and PR #149 remain open/unmerged. No collision, allocation ambiguity, or ref disagreement was found.

## Funnel snapshot

Material portfolio is MECHANISM=5 / SYSTEM=6. Terminal current objects=10; nonterminal holds=1. PRE_FORMAL eligible=0 and READY=0. Viable executable MECHANISM candidates=0. `CAND-H7-RESP-01` remains `HOLD_MECHANISM_UNRESOLVED / NONTERMINAL_HOLD / NOT_QUEUED`, with no native executable responsibility-sensitive object, supported reachability, fixed equal-privilege comparator, or fixed falsifier.

This run created no new FORMAL scientific evidence, PRE_FORMAL development evidence, MECHANISM Architecture observation, or SYSTEM Architecture observation. No consumed identity was touched and no Utility request was created.

## Stop / next action

- stop_reason: `ANALYST_STOP_NO_CURRENT_MAIN_OBJECT_NO_COHERENT_CENTRAL_OBJECT`
- lease target: `COMPLETED`
- next MAIN action: remain scientifically idle until a fresh Analyst generation allocates a fresh coherent executable MECHANISM object or an independently high-information integrity-protecting SYSTEM object. Before any scientific mutation, re-read current claim ceiling, readiness, hold dimensions, system-priority exception, Analyst generation, and exact refs.

Persistence for this generation uses MAIN-owned `latest.md`, `state.json`, `lease.json`, and append-only `reports/orchestrator/history/2026-09-20/1616-main.md` only.
