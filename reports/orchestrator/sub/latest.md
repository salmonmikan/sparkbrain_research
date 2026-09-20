# SparkBrain Research Orchestrator SUB — 2026-09-20 13:42 JST

## Generation / authority

- schema_version: `2`
- generation_id: `SUB-20260920T134240+0900-THEORY-REWARD-ADA731B2`
- produced_at: `2026-09-20T13:42:40+09:00`
- producer_run_id: `SUB-RUN-20260920T133307+0900-REWARD-ADA731B2`
- authority_scope: `BOUNDED_SECONDARY_DISCOVERY_ONLY_NON_EVIDENTIARY`
- supersedes_generation_id: `SUB-20260920T124445+0900-THEORY-PARTIAL-4E8A1C73`
- Evidence Analyst: `EVA-20260920T125840+0900-R13-5D7A2C91@c7b46081c2dcc980bd7856b37437012842bcce04`
- MAIN: `MAIN-20260920T131743+0900-PRIMARY-FUNNEL21-HOLD-93C7A1E4`, lane `LOWER_FUNNEL_MAIN_HOLD_NO_COHERENT_CENTRAL_OBJECT`
- Control Brain: `CTRL-20260920T125000+0900-R13-9C4F2B71@2aa866e406e5a3c7549c6d31d512e33626026dee`, strategy only
- previous SUB: `SUB-20260920T124445+0900-THEORY-PARTIAL-4E8A1C73`
- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`

Analyst generation and MAIN ownership were re-read before branch/result/persistence mutations and remained equivalent. Analyst explicitly leaves one bounded autonomous SUB Discovery open; MAIN has no active scientific object.

## Mode / target

- mode: `discovery`
- discovery_mode: `THEORY_BACKWARD_MECHANISM_DISCOVERY`
- target: `V05_DELAYED_REWARD_ELIGIBILITY_DISCOVERY_CYCLE1`
- candidate_pool_id: `NONE_SELF_SELECTED`
- cycle: `1/3`, stopped after clean reduction
- evidentiary_status: `NON_EVIDENTIARY`
- recommendation: `REJECT`
- next layer: `NONE`

Pre-selection rolling autonomous window was checkpoint continuation=`SYSTEM`, Assembly feedback=`MECHANISM`, Assembly partial completion=`MECHANISM` (`2/3` qualifying). This fresh mechanism selection was not quota-forced; it was chosen because the native v0.5 eligibility/reward surface permits a direct high-information discriminator. Post-selection rolling last-three is Assembly feedback=`MECHANISM`, Assembly partial completion=`MECHANISM`, delayed reward eligibility=`MECHANISM` (`3/3`). No theory-backward exception was used.

## MAIN frontier avoided

MAIN remains intentionally idle with no prospective object. SUB did not reopen terminal Assembly objects, did not execute `CAND-H7-RESP-01`, and did not touch MAIN blockers/immediate successors, FORMAL/TEST/scoring, consumed/frozen identities, preserve/control/evidence refs, or governance PRs.

This object is narrower than H7: it asks whether the already-existing v0.5 local eligibility surface can receive delayed reward without same-edge reactivation. It does not claim to resolve the full H7 family.

## Question / implementation

Question: can a causal pre/post event write a local eligibility trace that later receives scalar reward and selectively changes that previously eligible synapse without new causal activity on the edge?

Reduction question: is the implementation instead a global reward scalar that affects an edge only when current pre/post activity puts that edge back into the update loop, with old eligibility merely carried and decayed?

Non-authoritative branch: `research/exploratory-sub-delayed-reward-eligibility-20260920` from stable main. Prospective binding `fff0ddeb8e613a27ef9eac6fc6623addad56f82d`; hardened diagnostic `77bd51d3913c9751ca23cd4a2468d97bebe2983f`; final research head/result `391b8b958e9869d3b10f2ca7c8d784353cc0ff2c`. Production source was not modified.

Synthetic DEV-only procedure selected the lexicographically first plastic field edge, wrote one causal pair at `1/2 ms`, delivered reward `-2.0`, and compared: (a) no-new-activity apply, (b) same-edge reactivation at `11/12 ms` under delayed reward, and (c) identical reactivation under neutral reward. Delay learning was disabled to isolate weight credit. No repository evidence dataset, held-out/formal TEST, official scorer, or consumed identity was used.

## Observation / reduction

The first pair created local eligibility. Delayed reward followed by `apply(field, ())` produced zero plastic updates: the selected weight was unchanged while eligibility decayed by the configured `0.90` factor. The same delayed reward became functionally relevant only after the edge received a second causal pre/post pair; rewarded reactivation drove the selected weight downward while the neutral-reward matched control drove it upward.

Mapped terminal: `REWARD_INERT_UNTIL_EDGE_REACTIVATION`.

This is directly reduced by source control flow: `reward()` only changes the global `reward_trace`; `apply()` decays stored eligibility but skips weight updates for edges without current pre/post activity. The integrated brain also performs `plasticity.apply()` inside `process_episode()` before later `learn_outcome()` can call `plasticity.reward()`. Thus the prospectively tested delayed reward-to-stored-local-eligibility effect is absent without edge reactivation.

Exact diagnostic-head CI `35489566146` succeeded on Python 3.11/3.13. Exact final-head CI `35489706078` also completed `success` on Python 3.11/3.13 through lint, local readiness, full tests and bundle validation. CI has no evidentiary authority.

## Typing / readiness / hold dimensions

- proposed claim_ceiling: `MECHANISM`
- proposed preformal_eligible: `false`
- preliminary readiness status: `NOT_READY`
- claim_type: `NATIVE_DELAYED_LOCAL_RESPONSIBILITY_SENSITIVE_ELIGIBILITY_CREDIT`
- supported_reachability: `STORED_ELIGIBILITY_REACHABLE_SYNTHETIC_DEV_ONLY`
- functional_consequence: `ABSENT_FOR_DELAYED_REWARD_WITHOUT_REACTIVATION`
- ordinary reductions specified/controlled: `GLOBAL_REWARD_STATE_GATING_ONLY_ON_CURRENT_EDGE_ACTIVITY`
- reductions unresolved: `NONE_FOR_CURRENT_OBJECT; REDUCTION_SUCCEEDED`
- comparator status: `COMPLETE_REACTIVATION_VS_NEUTRAL_REWARD_CONTROL`
- qualitative support breadth: `ONE_DETERMINISTIC_SYNTHETIC_EDGE_CAUSAL_REWARD_REACTIVATION_PROBE`
- falsifier: `NO_WEIGHT_CHANGE_FROM_DELAYED_REWARD_WITHOUT_REACTIVATION`
- open scientific choices: a genuinely delayed reward-to-stored-eligibility mechanism requires a fresh candidate and prospective contract; it cannot rescue this object
- formal claim ceiling: `NONE_FOR_CURRENT_REDUCED_RESULT`
- hold_class: `null`
- hold_reason: `null`
- terminal_state: `TERMINAL_FOR_CURRENT_OBJECT`
- queue_state: `NOT_QUEUED`

## Integrity / completion

Utility request: none. Consumed identities: none. New FORMAL results: zero. No STARTED/control authority, formal/freeze/evidence ref, official score, held-out TEST access, immutable evidence mutation, research merge or stable-main mutation occurred.

Blocker: fresh Evidence Analyst classification/closure only; no execution blocker remains.

Completion target `ACHIEVED_ONE_THEORY_BACKWARD_DELAYED_REWARD_ELIGIBILITY_DISCOVERY_CYCLE_AND_REDUCED_TO_REACTIVATION_GATED_GLOBAL_REWARD_STATE` — achieved.

History: `reports/orchestrator/history/2026-09-20/1342-sub.md`.
