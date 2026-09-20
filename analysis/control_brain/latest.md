# SparkBrain Control Brain — 2026-09-21 00:50 JST

- schema_version: `2`
- generation_id: `CTRL-20260921T005250+0900-R18-6B4D2F91`
- produced_at: `2026-09-21T00:52:50+09:00`
- producer_run_id: `control-brain-auto-20260921T005250+0900-R18-6B4D2F91`
- authority_scope: `CONTROL_BRAIN_STRATEGIC_GOVERNANCE_AND_ALLOCATION_ONLY_NO_SCIENTIFIC_EXECUTION`
- supersedes_generation_id: `CTRL-20260920T225013+0900-R17-3F8C61A2`
- programme_position: `FORMAL_HOLD_WITH_ACTIVE_LOWER_FUNNEL`
- fleet_status: `YELLOW`
- scheduler_controller_action: `NO_CHANGE`
- utility_action: `ACCEPT_ONE_BOUNDED_NON_EVIDENTIARY_ELIGIBILITY_TIMEBASE_DIAGNOSTIC`

## Control conclusion

FORMAL remains correctly on hold. Evidence Analyst R22 remains authoritative at PRE_FORMAL eligible=`0`, READY=`0`, viable executable MECHANISM=`0`, Architecture active/queued=`0/0`, and no fresh one-way FORMAL authority. MAIN should remain intentionally idle.

Fresh SUB completed one prospectively bound SYSTEM Discovery, `CAND-V05-STEP-STATE-HASH-SEMANTICS-01`. The returned `V05StepResult.state_hash` differs from the immediate post-return brain hash, but the difference is reproduced exactly by removing only the just-appended trace entry and decrementing `episode_index` by one. The current object therefore reduces to deterministic pre-return bookkeeping/API semantics, not scientific-state divergence. SUB proposes terminal `REJECT / SYSTEM / preformal_eligible=false / N/A_FOR_SYSTEM_OBJECT / TERMINAL_FOR_CURRENT_OBJECT / NOT_QUEUED`; Control leaves canonical closure to fresh Analyst review.

A fresh Literature finding separately identifies a high-information reproducibility question: stable v0.5 eligibility decay is applied once per `V05PlasticityController.apply()` call without an elapsed-time parameter. Control ACCEPTED the resulting Utility request and assigned one bounded, non-evidentiary timebase/partition-invariance diagnostic. This is not a candidate, not a novelty claim, not a MAIN dependency, and may not reopen the terminal eligibility-history object. No Utility scheduler reconfiguration was needed.

## Human Directive review

No directive is new or materially changed.

- `HUMAN-20260918-001`: `ACCEPT / UNCHANGED` — reusable assets require independent review before main promotion; no promotion directed.
- `HUMAN-20260919-002`: `ACCEPT / UNCHANGED` — repository protection/rulesets remain deferred absent a materially changed concrete integrity risk.
- `HUMAN-20260919-003`: `ACCEPT / UNCHANGED` — preserve strict FORMAL integrity while preferring meaningful lower-funnel information over low-value governance cleanup or manufactured activity.

## Fresh SUB — state-hash semantics

SUB generation `SUB-20260921T004300+0900-SYSTEM-STATEHASH-2E7C91A4` used prospective contract `fcfb04d540a437378126d86c3ad66600714fbf99` before outcome. The fixed question, reduction and terminal mapping were bound before the diagnostic.

- outcome-bearing commit: `8e1bfa42471295b2cc7898f9fc6ce72092c18222`
- outcome CI: `35520053053`, success
- final research head: `83d11ba6e0e8aca3f6cda9e4ab9592c851cc0306`
- exact final-head CI: `35520275001`, success
- terminal: `PRE_RETURN_BOOKKEEPING_HASH_SEMANTICS`
- proposed disposition: `REJECT`
- claim ceiling: `SYSTEM`
- preformal eligible: `false`
- readiness: `N/A_FOR_SYSTEM_OBJECT`
- hold fields: `null`, correctly so for REJECT
- terminal state: `TERMINAL_FOR_CURRENT_OBJECT`
- queue state: `NOT_QUEUED`

The final post-outcome commit only narrowed operational interpretation after a stable-main usage search; it did not alter the diagnostic or terminal predicate. No v0.5 consumer was found that relies on equality between the returned hash and immediate post-return brain hash; the existing v0.5 test only requires the result hash to be non-empty. Same-object cycle 2 remains stopped. Any hash timing/content redesign or mechanism question requires a fresh object and prospective contract.

Rolling safe autonomous SUB selection is now `MECHANISM, MECHANISM, SYSTEM = 2/3` qualifying theory-backward work. The one-in-three minimum is satisfied and remains a floor, not a target.

## Funnel v2.1 metrics

Canonical Evidence Analyst R22:
- material candidates=`18`; MECHANISM=`10`; SYSTEM=`8`
- classification completeness=`18/18` with HOLD-only fields required iff `classification=HOLD`
- terminal states: ACTIVE=`0`; NONTERMINAL_HOLD=`1`; TERMINAL_FOR_CURRENT_OBJECT=`17`
- Architecture active/queued: MECHANISM=`0/0`; SYSTEM=`0/0`
- terminal HOLD distribution: `HOLD_SYSTEM_TERMINAL=4`, `HOLD_METHOD_LIMITED=1`
- PRE_FORMAL eligible=`0`; READY=`0`; viable executable MECHANISM=`0`
- recent completed MAIN Architecture cycles: SYSTEM=`3`; MECHANISM=`0`
- SYSTEM-over-comparable-MECHANISM exceptions=`0`

Pending fresh SUB view without pre-empting Analyst authority:
- material candidates=`19`; MECHANISM=`10`; SYSTEM=`9`
- fresh candidate-local mandatory fields are applicability-complete
- if terminal is confirmed: TERMINAL_FOR_CURRENT_OBJECT=`18`, NONTERMINAL_HOLD=`1`
- PRE_FORMAL eligible=`0`; READY=`0`; viable executable MECHANISM=`0`

No same-object SYSTEM->MECHANISM upgrade, `SYSTEM_QUEUE_STARVING_MECHANISM`, hidden second Formal gate, post-hoc priority-exception gaming, or theory-backward quota gaming is observed. The first Analyst-authoritative `eligible=true + READY -> PRE_FORMAL` transition remains unobserved.

## Literature / Utility request disposition

Literature generation `LIT-20260921T003000+0900-R15-ELIGIBILITY-TIMEBASE-5A7C2E91` reports that stable v0.5 multiplies stored eligibility by `0.90` once per `apply()` call, while no elapsed/current-time argument participates. Because `IntegratedV05Brain` calls plasticity apply once per learning episode, episode/apply count may be the effective clock unless that is explicitly intended.

Utility request `LIT-20260921-0030-ELIGIBILITY-TIMEBASE-INVARIANCE`: `ACCEPT`.

Control published:
- decision: `CTRL-DEC-20260921-0050-ELIGIBILITY-TIMEBASE-INVARIANCE`, commit `8660a825e2ac86f31f04e5439e9bc95242f16df9`
- assignment_id: `CTRL-20260921-0050-ELIGIBILITY-TIMEBASE-INVARIANCE`
- assignment_generation_id: `UASSIGN-20260921T005250+0900-ELIGTIME-7D4A2C91`
- assignment commit: `48c1bf1a7ed0474cff599cee4efadf3a319de011`
- max_runs=`1`
- evidentiary status=`NON_EVIDENTIARY_ARCHITECTURE_REPRODUCIBILITY_DIAGNOSTIC`
- scientific authority=`NONE`
- main critical-path dependency=`false`

Utility must first determine from stable source/docs/tests whether episode/apply count is explicitly the intended clock. If not, it may persist one prospective isolated diagnostic contract and run at most one DEV diagnostic holding semantic event-time/reward history and elapsed model time fixed while varying only non-semantic partition count. Terminal is restricted to `PARTITION_INVARIANT`, `EXPLICIT_EPISODE_TIME_SEMANTICS`, `CALL_COUNT_DEPENDENT`, or `INVALID_DIAGNOSTIC`.

Utility may not reopen `CAND-V05-ELIGIBILITY-HISTORY-SPECIFICITY-01`, patch production semantics, create/promote/classify a scientific candidate, alter claim ceiling/readiness/HOLD dimensions/theory accounting, touch consumed/formal/evidence/preserve refs, use active MAIN/SUB/Relay branches as fixtures, retune after outcome, or change any scheduler. Unhandled Utility requests after this decision=`0`.

## MAIN / Relay

MAIN primary `MAIN-20260921T001507+0900-PRIMARY-FUNNEL21-HOLD-R22-4B7C91E2` completed intentional idle with zero FORMAL, PRE_FORMAL, MECHANISM Architecture, or SYSTEM Architecture execution.

Relay `MAIN-20260921T004800+0900-RELAY-FUNNEL21-FAILCLOSED-R22-5A2E8C71` observed the fresh SUB generation and correctly stopped at `FAIL_CLOSED_ANALYST_DEPENDENCY_ADVANCED_UNREVIEWED_SUB_GENERATION`. It created no candidate or identity and executed no science. This is healthy dependency-aware behavior.

## Methodology / Audit / Steward

Methodology `METHCAL-20260921T002430+0900-R23-A7D24C91` remains `WELL_CALIBRATED / NO_MATERIAL_CALIBRATION_CHANGE`. Canonical v2.1 completeness is `18/18`; `HIDDEN_SECOND_FORMAL_GATE=false`; first READY->PRE_FORMAL transition, first genuine SYSTEM-priority exception, and first explicit `NO_COHERENT_MECHANISM_TARGET` use remain unobserved. The opportunity-cost guidance remains to prefer domain diversification when comparably informative rather than serial near-neighbor credit probes.

Independent Audit remains `AUD-20260920T223110+0900-R3-C19V4-REDUCTION-6B4E21D9`: immutable C19-v4 PASS is preserved for its exact registered contrast while programme-level SparkBrain-specific novelty support is `REDUCIBLE` after C19-R2's fixed seven-state FSA. C19-R1 revision-authority remains separate and unresolved.

Repository Steward remains governance-only at `STEWARD-20260920T195000+0900-G1-4C9A7E21`; no new immutable-ref incident is observed. Protection/rulesets remain read-only/deferred.

## Repository / authoritative refs

Fresh reconciliation confirms:
- `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- authoritative annotated `evidence/*` tags=`5`
- `formal/*`=`0`; `sealed/*`=`0`; tag-based `freeze/*`=`0`
- legacy `freeze/*` branches=`13`
- H5 STARTED=`058e90227cd48e1c10c6ecbaed01efdec1217d0e`
- H5 raw preserve=`ce5797eb584344db7a512e585506fb6c59ea475b`
- NI01 STARTED=`d3e4a5d6349e7e69f21ffc3554998aa72f1f9d3d`
- NI01 raw preserve=`8a39cf70e397bb7588f948910f01ec58672ac814`
- PR #148 open/unmerged at `14ba187bb13705bc306baabe310d5364cf1b60fb`
- PR #149 open/unmerged at `01ef8c3a54ff20403aba2fab9996dbda5552dd4d`

## Fleet health

`fleet_status: YELLOW`.

- Evidence Analyst: `HEALTHY` — fresh SUB/Literature/Utility deltas await the next dependency-aware review.
- MAIN: `NO_OP_BY_DESIGN` — no coherent central object.
- Relay: `NO_OP_BY_DESIGN` — correctly fail-closed pending fresh Analyst after SUB advanced.
- SUB: `EXPLORATORY_PRODUCTIVE` — prospectively bound, bounded SYSTEM Discovery; exact reduction and green exact-head CI.
- Literature: `HEALTHY` — fresh high-information reproducibility request.
- Independent Audit: `HEALTHY` — prior consequential reduction remains current.
- Methodology: `HEALTHY` — fresh R23; newer Literature/SUB deltas await its normal next poll.
- Repository Steward: `HEALTHY` — schema-v2 governance state.
- Utility: `HEALTHY` — one bounded Control-approved assignment active; result pending.

Critical FORMAL/immutable integrity failures=`0`; role collisions=`0`; relevant fresh SUB CI failures=`0`; scheduler failures requiring intervention=`0`. YELLOW reflects expected dependency deltas and one active bounded Utility diagnostic, not cadence failure. `scheduler_controller_action=NO_CHANGE`.

## Direction to Evidence Analyst

1. Independently verify `CAND-V05-STEP-STATE-HASH-SEMANTICS-01` against contract `fcfb04d...`, outcome `8e1bfa...`, final head `83d11b...`, outcome CI `35520053053`, and final CI `35520275001`; confirm the final post-outcome change is interpretation-only. If confirmed, close as `REJECT / SYSTEM / preformal_eligible=false / N/A_FOR_SYSTEM_OBJECT / TERMINAL_FOR_CURRENT_OBJECT / NOT_QUEUED`, HOLD-only fields null, terminal `PRE_RETURN_BOOKKEEPING_HASH_SEMANTICS`.
2. Do not upgrade the current SYSTEM object post-outcome. Any hash redesign or mechanism claim requires a fresh candidate ID and prospective contract.
3. Keep MAIN idle absent a coherent central object. Relay remains fail-closed until the fresh SUB generation is consumed.
4. When Utility returns the eligibility-timebase diagnostic, treat it only as NON_EVIDENTIARY Architecture/reproducibility information. It must not reopen eligibility-history, satisfy theory-backward quota, or create PRE_FORMAL/FORMAL authority.
5. Preserve `preformal_eligible` versus READY semantics and audit the first real READY->PRE_FORMAL transition as development/test readiness rather than prior comparator victory.
6. Treat current theory-backward `2/3` as the supply floor being satisfied, not as a target ratio.

## Generation / freshness map

- previous Control: `CTRL-20260920T225013+0900-R17-3F8C61A2@90c088f5fc3f6064f883d308ba5e1af9fd076441`
- Human Directives: `LEGACY_GENERATION_UNKNOWN`, unchanged
- Evidence Analyst: `EVA-20260921T000400+0900-R22-7C4E91A2@b4a2d1625f0b2f2a5cffffd7fe015b6ad60c797e`
- MAIN: `MAIN-20260921T001507+0900-PRIMARY-FUNNEL21-HOLD-R22-4B7C91E2@105737eaa5a6cf7ef731d7250e6e6fc2778d6fba`
- Relay: `MAIN-20260921T004800+0900-RELAY-FUNNEL21-FAILCLOSED-R22-5A2E8C71@751d525825a7297da0a54715a5820ae9bd983897`
- SUB: `SUB-20260921T004300+0900-SYSTEM-STATEHASH-2E7C91A4`, mailbox/state commit `12f2999994d465e4b1c49c38f6bd73f2620d09db`, research head `83d11ba6e0e8aca3f6cda9e4ab9592c851cc0306`
- Literature: `LIT-20260921T003000+0900-R15-ELIGIBILITY-TIMEBASE-5A7C2E91@31f6705c56489e0c7907b8f8b3eecb80c4355982`
- Independent Audit: `AUD-20260920T223110+0900-R3-C19V4-REDUCTION-6B4E21D9@2edf544763d699ccfe81dd52044f776e5425a90d`
- Methodology: `METHCAL-20260921T002430+0900-R23-A7D24C91@087fbab8af304b7703dec575b6f9230446024506`
- Repository Steward: `STEWARD-20260920T195000+0900-G1-4C9A7E21@266eac62e3565adb70d1871831612848b5b82141`
- Utility request: `LIT-20260921-0030-ELIGIBILITY-TIMEBASE-INVARIANCE`
- Utility decision: `CTRL-DEC-20260921-0050-ELIGIBILITY-TIMEBASE-INVARIANCE@8660a825e2ac86f31f04e5439e9bc95242f16df9`
- Utility assignment: `UASSIGN-20260921T005250+0900-ELIGTIME-7D4A2C91@48c1bf1a7ed0474cff599cee4efadf3a319de011`

## Integrity actions

experiments_executed=`0`; scientific_workflows_dispatched=`0`; identities_consumed=`0`; research_prs_merged=`0`; immutable_refs_mutated=`0`; formal_refs_mutated=`0`; evidence_refs_mutated=`0`; utility_assignments_changed=`1`; utility_live_scheduler_reconfigurations=`0`; schedulers_changed=`0`.
