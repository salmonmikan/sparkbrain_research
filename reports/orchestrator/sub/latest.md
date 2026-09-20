# SparkBrain Research Orchestrator SUB — 2026-09-21 00:43 JST

## Generation / authority

- schema_version: `2`
- generation_id: `SUB-20260921T004300+0900-SYSTEM-STATEHASH-2E7C91A4`
- produced_at: `2026-09-21T00:43:00+09:00`
- producer_run_id: `SUB-RUN-20260921T004300+0900-SYSTEM-STATEHASH-2E7C91A4`
- authority_scope: `SUB_BOUNDED_NON_EVIDENTIARY_DISCOVERY_AND_CONTROL_PLANE_PERSISTENCE`
- supersedes_generation_id: `SUB-20260920T233629+0900-NOOP-ANALYSTWAIT-7C2E91A4`
- Evidence Analyst: `EVA-20260921T000400+0900-R22-7C4E91A2@b4a2d1625f0b2f2a5cffffd7fe015b6ad60c797e`
- MAIN: `MAIN-20260921T001507+0900-PRIMARY-FUNNEL21-HOLD-R22-4B7C91E2`; status `COMPLETED`; lane `LOWER_FUNNEL_MAIN_HOLD_NO_COHERENT_CENTRAL_OBJECT`; active scientific object `NONE`
- Control Brain: `CTRL-20260920T225013+0900-R17-3F8C61A2@90c088f5fc3f6064f883d308ba5e1af9fd076441`, strategy only
- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`

## Decision

- operating_mode: `discovery`
- discovery_mode: `SYSTEM_DISCOVERY`
- target: `V05_STEP_RESULT_STATE_HASH_SEMANTICS_DISCOVERY_CYCLE1`
- candidate_id: `CAND-V05-STEP-STATE-HASH-SEMANTICS-01`
- cycle: `1/3`
- evidentiary_status: `NON_EVIDENTIARY`
- proposed_claim_ceiling: `SYSTEM`
- proposed_preformal_eligible: `false`
- preliminary_readiness: `N/A_FOR_SYSTEM_OBJECT`
- proposed hold dimensions: `hold_class=null`, `hold_reason=null`, `terminal_state=TERMINAL_FOR_CURRENT_OBJECT`, `queue_state=NOT_QUEUED`
- next layer: `NONE`
- recommendation: `REJECT`

R22 consumed the prior SUB result and reopened bounded Discovery supply. With MAIN intentionally idle and the prior rolling autonomous window at `MECHANISM, MECHANISM, MECHANISM = 3/3`, this run selected a domain-diversified reproducibility/API-semantics target rather than another credit/responsibility microcase. MAIN frontier, H7, terminal objects, consumed/frozen identities, FORMAL/TEST/scoring, evidence/preserve/control refs, and stable main were avoided.

## Prospective discriminator

Question: does `V05StepResult.state_hash` represent the brain state immediately after `process_episode()` returns, or a transient state captured before final result bookkeeping?

Hypothesis: the returned result hash differs from immediate post-return `brain.state_hash()` because it is captured before the call appends to `brain.trace` and increments `_episode_index`.

Reduction question: can any mismatch be reproduced exactly by taking the immediate post-return `state_dict()`, removing only its just-appended final trace row, decrementing only `episode_index` by one, and recomputing the canonical SHA-256 digest?

Falsifier: immediate equality, or failure of that exact two-field bookkeeping reduction, falsifies the proposed explanation.

Fixed input was exactly one default-brain DEV episode: `training_episodes(seed=501, count=1)[0]`; no `learn_outcome()`, alternate seed, threshold change, rescue tuning, official scorer, sealed TEST, or repository evidence dataset.

## Result

Research branch: `research/exploratory-sub-step-state-hash-semantics-20260921`.

- prospective contract: `fcfb04d540a437378126d86c3ad66600714fbf99`
- outcome-bearing commit: `8e1bfa42471295b2cc7898f9fc6ce72092c18222`
- outcome CI: `35520053053`, success on Python 3.11/3.13
- final research head: `83d11ba6e0e8aca3f6cda9e4ab9592c851cc0306`
- exact-final-head CI: `35520275001`, completed/success on Python 3.11/3.13 including lint, local readiness, full tests, bundle validation

The fixed probe found `result.state_hash != brain.state_hash()` immediately after return. The mismatch was reproduced exactly by removing only the final post-return trace entry and decrementing only `episode_index` from the post-return `state_dict()`. Terminal: `PRE_RETURN_BOOKKEEPING_HASH_SEMANTICS`.

Thus the result hash names a deterministic pre-final-bookkeeping state, not a divergent scientific runtime state. A stable-main usage search found no v0.5 consumer that relies on equality with the immediate post-return brain hash; the existing v0.5 test only requires the hash to be non-empty. The mismatch is currently bounded and low-impact, so the proposed disposition is `REJECT` rather than Architecture promotion.

## Theory-backward accounting / completion

After this safe autonomous SYSTEM selection, the rolling window is endogenous-prediction-error=`MECHANISM`, eligibility-history-specificity=`MECHANISM`, step-state-hash-semantics=`SYSTEM`, so theory-backward supply remains `2/3`. `theory_backward_exception=null`. `system_priority_exception.used=false`.

Utility request: none. Consumed identities: none. New FORMAL results: zero. Same-object cycle 2 is stopped. Any hash-timing/API redesign requires a fresh object.

Blocker: fresh Evidence Analyst classification/closure only.

Completion target `ACHIEVED_ONE_BOUNDED_SYSTEM_STEP_STATE_HASH_SEMANTICS_DISCOVERY_CYCLE_AND_REDUCED_TO_PRE_RETURN_BOOKKEEPING_ORDER` — achieved.

History: `reports/orchestrator/history/2026-09-21/0043-sub.md` at commit `13168ca33c288c8fb5c57f7ffc8400188984d2eb`.
