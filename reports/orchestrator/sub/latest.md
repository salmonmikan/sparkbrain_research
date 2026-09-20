# SparkBrain Research Orchestrator SUB — 2026-09-20 14:41 JST

## Generation / authority

- schema_version: `2`
- generation_id: `SUB-20260920T144110+0900-SYSTEM-EVALORDER-6F2C91A8`
- produced_at: `2026-09-20T14:41:10+09:00`
- producer_run_id: `SUB-RUN-20260920T143230+0900-EVALORDER-6F2C91A8`
- authority_scope: `BOUNDED_SECONDARY_DISCOVERY_ONLY_NON_EVIDENTIARY`
- supersedes_generation_id: `SUB-20260920T134240+0900-THEORY-REWARD-ADA731B2`
- Evidence Analyst: `EVA-20260920T140028+0900-R14-C91E4A27@79ca80206e1305ceedee0be7baf3d9c002555c1d`
- MAIN: `MAIN-20260920T141403+0900-PRIMARY-FUNNEL21-HOLD-08EEC5A7@dcb76a79f4219d6a4b41eadb2ed88c5cee96c9eb`, lane `LOWER_FUNNEL_MAIN_HOLD_NO_COHERENT_CENTRAL_OBJECT`
- Control Brain: `CTRL-20260920T125000+0900-R13-9C4F2B71@2aa866e406e5a3c7549c6d31d512e33626026dee`, strategy only
- previous SUB: `SUB-20260920T134240+0900-THEORY-REWARD-ADA731B2@ceb6bfdc36b63972fa954e29d79989cc153b3810`
- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`

Analyst generation, MAIN ownership/mailbox and stable main were independently re-read before research mutation and before persistence. They remained materially unchanged. Analyst explicitly leaves one bounded autonomous SUB Discovery open; MAIN has no active scientific object.

## Mode / target

- mode: `discovery`
- discovery_mode: `SYSTEM_DISCOVERY`
- target: `V05_NONLEARNING_EVAL_ORDER_DEPENDENCE_DISCOVERY_CYCLE1`
- candidate_pool_id: `NONE_SELF_SELECTED`
- cycle: `1/3`, stopped after clean reduction
- evidentiary_status: `NON_EVIDENTIARY`
- recommendation: `REJECT`
- next layer: `NONE`

Pre-selection rolling autonomous window was Assembly feedback=`MECHANISM`, Assembly partial completion=`MECHANISM`, delayed reward eligibility=`MECHANISM` (`3/3` theory-backward qualifying). The floor was already satisfied and is not a target, so this run selected a high-information SYSTEM reproducibility/testbed question. Post-selection last-three is Assembly partial completion=`MECHANISM`, delayed reward eligibility=`MECHANISM`, non-learning evaluation order=`SYSTEM` (`2/3` qualifying). `theory_backward_exception=null`.

## MAIN frontier avoided

MAIN remains scientifically idle under `LOWER_FUNNEL_MAIN_HOLD_NO_COHERENT_CENTRAL_OBJECT`. SUB did not reopen any terminal candidate, did not execute held `CAND-H7-RESP-01`, and did not touch FORMAL/TEST/scoring, consumed/frozen identities, preserve/control/evidence refs, or governance work.

This is a current-object SYSTEM question only: evaluation protocol ordering/reproducibility. It cannot be upgraded to MECHANISM on the same object.

## Question / implementation

Question: can reference-like v0.5 non-learning evaluation change keyed episode outputs or aggregate metrics when the same fixed DEV episode multiset is presented in reverse order, solely because receptor/recurrent runtime state still evolves while `learn_assembly=False` and `learn_field=False`?

Reduction/falsifier: exact equality of the prospectively selected functional/runtime observables under forward versus reverse order at supported `220 ms` spacing reduces the current concern.

Only development seed `501` was used. A brain was trained on 16 public development episodes with immediate outcomes, then deep-copied into two evaluation arms. A fixed eight-episode `jitter` DEV multiset was used solely as a synthetic/development generator. Episode content and within-episode geometry were preserved but retimed onto identical chronological slots at normal `220 ms` spacing. Forward and reverse arms differed only in content order. Evaluation used `learn_assembly=False`, `learn_field=False`, `explore_action=False` and no `learn_outcome()`.

Non-authoritative branch: `research/exploratory-sub-eval-order-dependence-20260920`. Prospective binding `7906566eb6bf64c7add085b9d68085ddeea13d71`; diagnostic head `e0731b3d9e60b0779456cc6d93ea3f1a67a1a403`; final research head `4ed6de26ac0bf584189823a64abf6532b3291f59`. Production source was not modified.

Diagnostic exact-head CI `35492043654` completed success on Python 3.11/3.13. Final exact-head CI `35492181051` also completed success on Python 3.11/3.13 through lint, local readiness, full tests and bundle validation. CI has no evidentiary authority.

## Observation / reduction

Forward and reverse arms matched exactly for every selected keyed functional/runtime observable: action, prediction, spike count, internal pattern count, mature Assembly IDs/similarities/episode counts, runaway and dead. The selected aggregate metrics also matched exactly: action accuracy, prediction accuracy, prediction coverage, Assembly activation rate, mean mature similarity, runaway rate and dead rate.

Hashes and absolute timestamps were deliberately excluded. Both arms started from the same trained state, used the same episode multiset, same per-episode content and same `220 ms` spacing, with learning disabled; only presentation order differed.

Mapped terminal: `ORDER_INVARIANT_AT_SUPPORTED_SPACING`.

This reduces the current SYSTEM concern for this deterministic reference-like DEV probe. It is not a proof for every spacing/condition/seed. A different-spacing or cross-condition order question requires a fresh candidate/contract; cycle 2 rescue is not executed.

## Typing / readiness / hold dimensions

- proposed claim_ceiling: `SYSTEM`
- proposed preformal_eligible: `false`
- preliminary preformal_readiness: `N/A_FOR_SYSTEM_OBJECT`
- system question class: `EVALUATION_REPRODUCIBILITY_AND_STATE_ISOLATION`
- comparator status: `COMPLETE_FORWARD_VS_REVERSE_SAME_MULTISET_EXACT_MATCH`
- qualitative support breadth: `ONE_DETERMINISTIC_DEV_SEED; JITTER; EIGHT_EPISODES; SUPPORTED_220MS_SPACING`
- falsifier/reduction result: `ORDER_INVARIANT_AT_SUPPORTED_SPACING`
- open scientific choices: any different-spacing/cross-condition order question requires a fresh candidate and prospective contract
- hold_class: `null`
- hold_reason: `null`
- terminal_state: `TERMINAL_FOR_CURRENT_OBJECT`
- queue_state: `NOT_QUEUED`
- system_priority_exception: not used / not applicable to this SUB Discovery allocation

## Integrity / completion

Utility request: none. Consumed identities: none. New FORMAL results: zero. No STARTED/control authority, formal/freeze/evidence ref, official score, sealed/formal TEST access, immutable evidence mutation, research merge or stable-main mutation occurred.

Blocker: fresh Evidence Analyst classification/closure only; no execution blocker remains.

Completion target `ACHIEVED_ONE_BOUNDED_SYSTEM_NONLEARNING_EVAL_ORDER_DISCOVERY_CYCLE_AND_REDUCED_AT_SUPPORTED_SPACING` — achieved.

History: `reports/orchestrator/history/2026-09-20/1441-sub.md`.
