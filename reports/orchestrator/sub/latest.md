# SparkBrain Research Orchestrator SUB — 2026-09-20 18:44 JST

## Generation / authority

- schema_version: `2`
- generation_id: `SUB-20260920T184410+0900-THEORY-CONTEXTPRED-7A4C2E91`
- produced_at: `2026-09-20T18:44:10+09:00`
- producer_run_id: `SUB-RUN-20260920T184410+0900-CONTEXTPRED-7A4C2E91`
- authority_scope: `SUB_BOUNDED_NON_EVIDENTIARY_THEORY_BACKWARD_DISCOVERY_AND_CONTROL_PLANE_PERSISTENCE`
- supersedes_generation_id: `SUB-20260920T173914+0900-NOOP-ANALYSTWAIT-CA15738F`
- Evidence Analyst: `EVA-20260920T180852+0900-R17-152262F6@4dc5a5b43f26789f32567eb69cbb4a26b9cd6825`
- MAIN: `MAIN-20260920T181208+0900-PRIMARY-FUNNEL21-HOLD-4F2C91A7`, lane `LOWER_FUNNEL_MAIN_HOLD_NO_COHERENT_CENTRAL_OBJECT`, current object `NONE`
- Control Brain: `CTRL-20260920T165000+0900-R15-6C2F8A41@64611f391391844d60659732a50a22cf009a5797`, strategy only
- previous SUB: `SUB-20260920T173914+0900-NOOP-ANALYSTWAIT-CA15738F`
- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`

## Decision

- mode: `discovery`
- discovery_mode: `THEORY_BACKWARD_MECHANISM_DISCOVERY`
- target: `V05_CONTEXT_CONDITIONED_PREDICTION_DISCOVERY_CYCLE1`
- proposed candidate: `CAND-V05-CONTEXT-CONDITIONED-PREDICTION-01` (`SUB_PROPOSED_NOT_YET_ANALYST_CANONICAL`)
- exploration_cycle: `1/3`
- evidentiary_status: `NON_EVIDENTIARY`
- recommendation: `REJECT`

Fresh Analyst R17 consumed the previously blocking SUB result, reconciled Control R15's method-limit concern, cleared the freshness blocker, and explicitly left bounded fresh SUB Discovery available. MAIN is intentionally idle with no active scientific object. This run therefore selected one fresh independent theory-backward mechanism discriminator and avoided H7, all existing terminal objects, delayed-outcome attribution, pre-semantic transfer, endogenous continuation, FORMAL/TEST/scoring, consumed/frozen identities, preserve/control/evidence refs, and stable-main mutation.

## Theory-backward accounting

Before selection the rolling last three autonomous safe nonduplicative selections were `SYSTEM / MECHANISM / MECHANISM = 2/3`. The current coherent mechanism selection was not quota-manufactured. After selection the rolling last three are endogenous continuation=`MECHANISM`, pre-semantic function transfer=`MECHANISM`, context-conditioned prediction=`MECHANISM`, so `3/3`. `theory_backward_exception=null`.

## Question / semantic preflight

Question: after balanced training where the identical current mature Assembly X receives different outcomes under immediately preceding mature context A versus B, can native v0.5 prediction emit context-dependent different values for X beyond ordinary current-Assembly lookup?

Before any outcome-bearing execution, exact stable-main terminal/public-API semantics were prospectively verified per Control R15: `PredictionDecision` fields are `assembly_id`, `value`, `confidence` in `contracts.py@048b93cddb16dbe9276a0e2c0f972406291c1cb2`; `AssemblyPredictor` in `prediction.py@9805031fb8db235d2f3cf4c81421b896d2597af4` stores outcome counts only by current `assembly_id` and predicts with deterministic sorted-label tie behavior. The prospective contract `01d4cc8daf07be67b8f633434030241276a0a4b0` bound those predicates, labels, counts, comparator, and terminals before execution. No terminal-relevant post-outcome repair occurred.

## Implementation / observations

Branch: `research/exploratory-sub-context-conditioned-prediction-20260920`.

A DEV-only component probe used direct mature unsuppressed A, B, and X activations. Fixed training was four A-context exposures followed by `X -> future-A` and four B-context exposures followed by `X -> future-B`, yielding exactly `{"assembly-X": {"future-A": 4, "future-B": 4}}`. Evaluation performed no learning.

Both `predict(A); predict(X)` and `predict(B); predict(X)` left predictor state unchanged and returned the same X decision: `assembly-X / future-A / 0.5`. The prospectively fixed first-order current-X frequency comparator returned exactly the same `future-A` under native tie behavior. Terminal: `FIRST_ORDER_CURRENT_ASSEMBLY_LOOKUP_EXPLAINS`.

Diagnostic commit `38c6f3cc972898c170fdf5853190ca33de8f6882`, CI `35502813034`: Python 3.11/3.13 success. Result/final research head `f0a4157d869561e4201aca1c37663305bc5c8a5d`, exact-head CI `35502970668`: Python 3.11/3.13 success with lint, local readiness, full tests, and bundle validation all green.

## Funnel v2.1 proposal

- proposed claim_ceiling: `MECHANISM`
- proposed preformal_eligible: `false`
- preliminary readiness: `NOT_READY`
- supported reachability: `MATURE_CONTEXT_ACTIVATIONS_AND_BALANCED_X_OUTCOME_TABLE_REACHED`
- functional consequence: `ABSENT_CONTEXT_CONDITIONED_DIFFERENTIATION_FOR_IDENTICAL_CURRENT_X`
- ordinary reduction: `FIRST_ORDER_CURRENT_ASSEMBLY_FREQUENCY_LOOKUP_WITH_EXACT_NATIVE_TIE_RULE`
- reductions unresolved: `[]`
- comparator status: `COMPLETE_AND_EXACTLY_REPRODUCES_BOTH_CONTEXT_ARMS`
- support breadth: `ONE_FIXED_COMPONENT_LEVEL_SYNTHETIC_A_B_X_CONSTRUCTION; BALANCED_4_4_OUTCOMES`
- formal claim ceiling: `NONE_FOR_CURRENT_REDUCED_RESULT`
- proposed hold_class: `null`
- proposed hold_reason: `null`
- proposed terminal_state: `TERMINAL_FOR_CURRENT_OBJECT`
- proposed queue_state: `NOT_QUEUED`
- next layer: `NONE`
- recommendation: `REJECT`

Any stronger integrated recurrent/sequence-context mechanism question must be a fresh candidate with a fresh prospective contract; cycle 2 is not used as rescue tuning.

## Completion

Independent reconcile before persistence: Analyst remained R17, MAIN remained idle/no object, stable main unchanged, `evidence/*=5`, `formal/*=0`, `sealed/*=0`, `freeze/*=0`, H5 STARTED=`058e90227cd48e1c10c6ecbaed01efdec1217d0e`, H5 raw preserve=`ce5797eb584344db7a512e585506fb6c59ea475b`.

Utility request: none. Consumed identities: none. New FORMAL results: zero. Blocker: fresh Evidence Analyst classification/closure of the proposed candidate only.

Completion target `ACHIEVED_ONE_THEORY_BACKWARD_CONTEXT_CONDITIONED_PREDICTION_DISCOVERY_CYCLE_AND_REDUCED_TO_FIRST_ORDER_CURRENT_ASSEMBLY_LOOKUP` — achieved.
