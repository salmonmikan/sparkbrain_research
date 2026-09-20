# SparkBrain Research Orchestrator SUB — 2026-09-20 22:46 JST

## Generation / authority

- schema_version: `2`
- generation_id: `SUB-20260920T224620+0900-THEORY-ELIGHIST-8D4C71A2`
- produced_at: `2026-09-20T22:46:20+09:00`
- producer_run_id: `SUB-RUN-20260920T224620+0900-ELIGHIST-8D4C71A2`
- authority_scope: `SUB_BOUNDED_NON_EVIDENTIARY_THEORY_BACKWARD_MECHANISM_DISCOVERY_AND_CONTROL_PLANE_PERSISTENCE`
- supersedes_generation_id: `SUB-20260920T214600+0900-THEORY-PREDERR-5C8A2F17`
- Evidence Analyst: `EVA-20260920T215718+0900-R21-4F8C2A71@f85692e6e207ae622282116779b559108085ede8`
- MAIN: `MAIN-20260920T221704+0900-PRIMARY-FUNNEL21-HOLD-R21-9C2A7E41`; lane `LOWER_FUNNEL_MAIN_HOLD_NO_COHERENT_CENTRAL_OBJECT`; active scientific object `NONE`
- Control Brain: `CTRL-20260920T205000+0900-R16-5E9A71C3@016a248143dc71380fca28128d564d74aeb4c3f3`
- previous SUB: `SUB-20260920T214600+0900-THEORY-PREDERR-5C8A2F17`
- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`

## Decision

- mode: `discovery`
- discovery_mode: `THEORY_BACKWARD_MECHANISM_DISCOVERY`
- target: `V05_ELIGIBILITY_HISTORY_SPECIFICITY_DISCOVERY_CYCLE1`
- proposed candidate: `CAND-V05-ELIGIBILITY-HISTORY-SPECIFICITY-01` (`SUB_PROPOSED_NOT_YET_ANALYST_CANONICAL`)
- exploration_cycle: `1/3`
- evidentiary_status: `NON_EVIDENTIARY`
- proposed claim_ceiling: `MECHANISM`
- proposed preformal_eligible: `false`
- recommendation: `REJECT`

Analyst R21 authorizes bounded SUB Discovery while MAIN is intentionally idle. The current object is a fresh native-v0.5 local plasticity discriminator and does not reopen or execute held `CAND-H7-RESP-01` or any terminal current object.

## Theory-backward accounting

Before selection: Assembly cluster order=`SYSTEM`, delayed action responsibility=`MECHANISM`, endogenous prediction-error modulation=`MECHANISM` (`2/3`). After selection: delayed action responsibility=`MECHANISM`, endogenous prediction-error modulation=`MECHANISM`, eligibility-history specificity=`MECHANISM` (`3/3`). `theory_backward_exception=null`.

## Question / prospective semantics

Question: with identical current `+1 ms` causal activity, does stored per-edge eligibility history create reward-credit differences that exceed an ordinary decaying eligibility trace?

Hypothesis: richer responsibility-sensitive credit would produce a target-edge difference not exactly reproduced by the fixed recurrence `e_t = decay*e_(t-1)+delta_t`, `delta_w = learning_rate*reward_trace*e_t`.

Falsifier/reduction: if both target-edge eligibilities and weight changes match that recurrence exactly under the common reward and clipping contract, the current mechanism object is reduced.

Prospective contract: `e466bd89cfd4ab80dc970173a183638af815fe8b` on `research/exploratory-sub-eligibility-history-specificity-20260920`.

## Implementation / observations

A deterministic pair of disjoint interior plastic edges was selected from the default synthetic v0.5 field. With weight/delay learning disabled, only A was primed by one `+1 ms` causal pair, creating stored eligibility `≈0.94595947`; B remained unprimed. Weight learning was then enabled without changing trace state. Under one common `reward_trace=-2.0`, A and B each received one new `+1 ms` causal pair in the same plasticity step.

The fixed comparator predicted A post-step eligibility `≈1.79732299`, B `≈0.94595947`, A weight delta `≈-0.00359465`, and B `≈-0.00189192`. Native v0.5 matched both target-edge eligibility values and both weight changes exactly within the prospectively fixed numerical comparator. Stored local history is functionally expressed, but its entire effect reduces to the ordinary per-edge eligibility recurrence plus the common scalar reward.

Observed terminal: `ORDINARY_PER_EDGE_ELIGIBILITY_TRACE_REDUCTION`.

Outcome-bearing diagnostic head `bd071d9023058d01f58d6f7ddacf35e820de51b6` had CI `35514176121` success. Final research head `6ddcb7fec39dd017fbfe172885a994a98b503021` has exact-head CI `35514340688` completed success on Python 3.11/3.13 with lint, local readiness, full tests, and bundle validation green.

No cycle-2 rescue is warranted. Any richer responsibility-sensitive credit claim requires a fresh candidate ID and fresh prospective comparator/intervention contract.

## Funnel v2.1 proposal

- proposed claim_ceiling: `MECHANISM`
- proposed preformal_eligible: `false`
- preliminary readiness status: `NOT_READY`
- claim_type: `mechanism`
- supported_reachability: `PARTIAL_SYNTHETIC_DEV_ONLY`
- functional_consequence: `DIFFERENTIAL_HISTORY_SENSITIVE_WEIGHT_UPDATE_PRESENT_BUT_EXACTLY_REDUCED`
- ordinary reductions specified/controlled: `PER_EDGE_DECAYING_ELIGIBILITY_TRACE_WITH_COMMON_REWARD_SCALAR`
- ordinary reductions unresolved: `[]`
- comparator status: `COMPLETE_AND_EXACT_FOR_BOTH_MATCHED_CURRENT_ACTIVITY_TARGET_EDGES`
- support breadth: `one deterministic two-edge matched-current-activity DEV intervention`
- falsifier: `exact match to fixed per-edge eligibility recurrence for both target edges`
- open scientific choices: `[]`
- formal claim ceiling: `NONE_FOR_CURRENT_REDUCED_RESULT`
- proposed hold_class: `null`
- proposed hold_reason: `null`
- proposed terminal_state: `TERMINAL_FOR_CURRENT_OBJECT`
- proposed queue_state: `NOT_QUEUED`
- candidate next research layer: `NONE`
- recommendation: `REJECT`

## Completion

Independent reconciliation confirmed Analyst R21 remained current before mutation and persistence, MAIN had no active scientific object, stable main remained unchanged, and exactly five `evidence/*` tags remained present. No FORMAL/TEST/scoring, consumed/frozen identity, preserve/control/evidence ref, stable-main mutation, research merge, or novelty claim occurred.

Utility request: none. Consumed identities: none. New FORMAL results: zero. Blocker: fresh Evidence Analyst classification/closure only.

Completion target `ACHIEVED_ONE_THEORY_BACKWARD_ELIGIBILITY_HISTORY_SPECIFICITY_DISCOVERY_CYCLE_AND_REDUCED_TO_ORDINARY_PER_EDGE_ELIGIBILITY_TRACE` — achieved.
