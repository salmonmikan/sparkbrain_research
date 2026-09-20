# SparkBrain Evidence Analyst — 2026-09-21 06:58 JST

- schema_version: `2`
- generation_id: `EVA-20260921T065846+0900-R29-7B2C91E4`
- produced_at: `2026-09-21T06:58:46+09:00`
- producer_run_id: `evidence-analyst-auto-20260921T065846+0900-R29-7B2C91E4`
- authority_scope: `EVIDENCE_ANALYST_ALLOCATION_AND_SCIENTIFIC_STRATEGY_READ_ONLY_EXECUTION`
- supersedes_generation_id: `EVA-20260921T055830+0900-R28-4D7A91C2`

## Material update

Fresh SUB has completed a genuine `THEORY_BACKWARD_MECHANISM_DISCOVERY` after the R28 qualitative search-space reframe. Candidate `CAND-V05-ASSEMBLY-UNIT-CAUSAL-SELECTIVITY-01` was prospectively bound before intervention outcome and produced `SELECTIVE_TARGETED_FUNCTION_LOSS` on one bounded non-held-out DEV probe: suppressing selected Assembly-member units removed the mature Assembly activation and changed prediction `outcome-0 -> null`, while the prospectively fixed equal-cardinality nearest baseline-spike-participation nonmember lesion retained the prediction and Assembly activation.

This is a meaningful positive lower-funnel signal, but it is **not PRE_FORMAL-ready and not Formal evidence**. The fixed comparator was imperfect: each targeted unit had one baseline probe spike, while each selected comparator unit had zero because no exact one-spike nonmember match existed. Graph-centrality/topological-load and stronger sham/random lesion reductions also remain unresolved. Stable theory already requires targeted impairment to be interpreted against matched random/sham intervention. Therefore the current Discovery object is closed at `HOLD / MECHANISM / HOLD_MECHANISM_UNRESOLVED / TERMINAL_FOR_CURRENT_OBJECT / NOT_QUEUED`. It is not allowed to receive an outcome-driven cycle-2 comparator redesign.

A fresh successor is created: `CAND-V05-ASSEMBLY-UNIT-CAUSAL-SELECTIVITY-MATCHED-LOAD-01`. This is a new current object, `MECHANISM`, `preformal_eligible=true`, `ARCHITECTURE_STUDY`, ACTIVE. Its next authorized MAIN step is **comparator-feasibility and prospective contract definition only**. No new suppression/intervention outcome is authorized in that same run. Exact activity-load, topology-load, sham/random lesion and selection-privilege controls must be made outcome-independent before any outcome-bearing continuation.

No new FORMAL evidence exists. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; authoritative annotated `evidence/*` tags remain five; tag-based `formal/*`, `sealed/*`, and `freeze/*` remain zero.

## Fresh SUB result and canonical Discovery review

SUB generation: `SUB-20260921T064900+0900-THEORY-ASMCAUSAL-7A4C91E2`.

Prospective contract: `eb5ae27f3ef7f8cca2bcc521e2c3f027a5ab6c42`.
Outcome-bearing commit: `1a571db21ff82001407f01cb2c5449f253bfd4e5`.
Final research head: `0c857a73cf34b58b737f686fd9af60769de3d306`.
Bounded DEV workflow: `35539567864`, completed/success.
Exact-head CI: `35539682655`, completed/success.

Observed fixed probe:
- selected Assembly: `assembly-0001`, training motif-X=`10`, motif-Y=`0`;
- baseline prediction=`outcome-0`, strongest similarity=`0.9433062621147579`, lower spikes=`9`;
- targeted prototype units `[45,56,63]`, baseline spikes=`1` each;
- prospectively fixed nearest nonmember comparators `[16,17,18]`, baseline spikes=`0` each;
- targeted suppression: prediction=`null`, no strongest mature Assembly activation, spikes=`6`;
- comparator suppression: prediction=`outcome-0`, same selected Assembly/similarity, spikes=`9`;
- prospective terminal=`SELECTIVE_TARGETED_FUNCTION_LOSS`.

Canonical current-object disposition:
- classification=`HOLD`
- claim_ceiling=`MECHANISM`
- preformal_eligible=`false`
- hold_class=`HOLD_MECHANISM_UNRESOLVED`
- hold_reason=`SELECTIVE_TARGETED_FUNCTION_LOSS_ON_FIXED_DEV_PROBE`, `ACTIVITY_MATCH_IMPERFECT_TARGET_1_SPIKE_COMPARATOR_0`, `GRAPH_CENTRALITY_TOPOLOGY_LOAD_UNCONTROLLED`, `FRESH_SUCCESSOR_REQUIRED_FOR_STRONGER_DISCRIMINATOR`
- terminal_state=`TERMINAL_FOR_CURRENT_OBJECT`
- queue_state=`NOT_QUEUED`
- preformal_readiness.status=`NOT_READY`

SUB's proposed `HOLD_MECHANISM_UNRESOLVED_REDUCTION` is not a valid Funnel-v2.1 enum and is normalized to `HOLD_MECHANISM_UNRESOLVED`.

## Fresh successor

`CAND-V05-ASSEMBLY-UNIT-CAUSAL-SELECTIVITY-MATCHED-LOAD-01`

- target layer: `ARCHITECTURE_STUDY`
- classification: `ARCHITECTURE_STUDY`
- claim_ceiling: `MECHANISM`
- preformal_eligible: `true`
- terminal_state: `ACTIVE`
- queue_state: `ACTIVE`
- readiness: `NOT_READY`
- supported_reachability: `PARTIAL`
- functional_consequence: `PARTIAL` from predecessor DEV signal only
- matched_comparator_status: `NOT_READY`
- unresolved reductions: exact activity-load, graph-centrality/topological-load, sham/random lesion equivalence, selection privilege
- formal claim ceiling: Assembly-member causal selectivity beyond prospectively matched ordinary lesion load; no broader novelty claim

This is not a post-outcome upgrade of the completed Discovery object. It is a fresh candidate ID and fresh question motivated independently by stable Gate-E causal-intervention semantics plus the predecessor's bounded development signal.

## Four-layer funnel

- DISCOVERY: `OPEN`, SUB-owned independent candidate supply.
- ARCHITECTURE_STUDY: `ACTIVE`; active MECHANISM=`1`, SYSTEM=`0`; queued=`0/0`.
- PRE_FORMAL: `EMPTY_HOLD`; eligible=`1`, READY=`0`.
- FORMAL: `EMPTY_HOLD`; no fresh one-way identity/STARTED/TEST/scorer/preserve authority.

Canonical portfolio: material candidates=`24`, MECHANISM=`12`, SYSTEM=`12`.
Classification completeness=`24/24`.
Terminal states: ACTIVE=`1`, NONTERMINAL_HOLD=`1`, TERMINAL_FOR_CURRENT_OBJECT=`22`.
Viable executable MECHANISM candidates=`1`.

## Candidate lifecycle snapshot

1. `CAND-ASSEMBLY-MATURE-CAPACITY-LIFECYCLE-01` — HOLD / SYSTEM / false / N/A / HOLD_SYSTEM_TERMINAL / terminal.
2. `CAND-V05-ASSEMBLY-FEEDBACK-CAUSALITY-01` — REJECT / MECHANISM / false / NOT_READY / terminal.
3. `CAND-V05-RECEPTOR-SIMULTANEITY-ORDERING-01` — HOLD / SYSTEM / false / N/A / HOLD_SYSTEM_TERMINAL / terminal.
4. `CAND-V05-CHECKPOINT-CONTINUATION-EQUIVALENCE-01` — REJECT / SYSTEM / false / N/A / terminal.
5. `CAND-V05-HOMEOSTASIS-POPULATION-SEMANTICS-01` — HOLD / SYSTEM / false / N/A / HOLD_SYSTEM_TERMINAL / terminal.
6. `CAND-V05-UNIT-SUPPRESSION-TRANSIENT-SEMANTICS-01` — HOLD / SYSTEM / false / N/A / HOLD_METHOD_LIMITED / terminal.
7. `CAND-H7-RESP-01` — HOLD / MECHANISM / false / NOT_READY / HOLD_MECHANISM_UNRESOLVED / NONTERMINAL_HOLD.
8. `CAND-V05-ASSEMBLY-PARTIAL-COMPLETION-FUNCTION-01` — REJECT / MECHANISM / false / NOT_READY / terminal.
9. `CAND-V05-DELAYED-REWARD-ELIGIBILITY-01` — REJECT / MECHANISM / false / NOT_READY / terminal.
10. `CAND-V05-NONLEARNING-EVAL-ORDER-DEPENDENCE-01` — REJECT / SYSTEM / false / N/A / terminal.
11. `CAND-V05-ENDOGENOUS-CONTINUATION-01` — REJECT / MECHANISM / false / NOT_READY / terminal.
12. `CAND-V05-PRESEMANTIC-FUNCTION-TRANSFER-01` — HOLD / MECHANISM / false / NOT_READY / HOLD_METHOD_LIMITED / terminal.
13. `CAND-V05-CONTEXT-CONDITIONED-PREDICTION-01` — REJECT / MECHANISM / false / NOT_READY / terminal.
14. `CAND-V05-ASSEMBLY-CLUSTER-ORDER-DEPENDENCE-01` — HOLD / SYSTEM / false / N/A / HOLD_SYSTEM_TERMINAL / terminal.
15. `CAND-V05-ASSEMBLY-CLUSTER-ORDER-SUPPORTED-REACHABILITY-01` — HOLD / SYSTEM / false / N/A / HOLD_SYSTEM_TERMINAL / terminal.
16. `CAND-V05-DELAYED-ACTION-RESPONSIBILITY-01` — REJECT / MECHANISM / false / NOT_READY / terminal.
17. `CAND-V05-ENDOGENOUS-PREDICTION-ERROR-MODULATION-01` — REJECT / MECHANISM / false / NOT_READY / terminal.
18. `CAND-V05-ELIGIBILITY-HISTORY-SPECIFICITY-01` — REJECT / MECHANISM / false / NOT_READY / terminal.
19. `CAND-V05-STEP-STATE-HASH-SEMANTICS-01` — REJECT / SYSTEM / false / N/A / terminal.
20. `CAND-V05-ELIGIBILITY-TIMEBASE-CONTRACT-01` — HOLD / SYSTEM / false / N/A / HOLD_CONTRACT_AMBIGUITY / terminal.
21. `CAND-V05-NONLEARNING-ACTION-VISIT-CARRYOVER-01` — HOLD / SYSTEM / false / N/A / HOLD_SYSTEM_TERMINAL / terminal.
22. `CAND-V05-ELIGIBILITY-TIMEBASE-PARTITION-INVARIANCE-01` — HOLD / SYSTEM / false / N/A / HOLD_SYSTEM_TERMINAL / terminal.
23. `CAND-V05-ASSEMBLY-UNIT-CAUSAL-SELECTIVITY-01` — HOLD / MECHANISM / false / NOT_READY / HOLD_MECHANISM_UNRESOLVED / terminal.
24. `CAND-V05-ASSEMBLY-UNIT-CAUSAL-SELECTIVITY-MATCHED-LOAD-01` — ARCHITECTURE_STUDY / MECHANISM / true / NOT_READY / ACTIVE.

All material candidates carry the mandatory Funnel-v2.1 fields in `state.json`; all twelve MECHANISM objects carry full `preformal_readiness`.

## Funnel metrics and theory-backward accounting

Recent actual scientific Discovery dispositions: REJECT=`1`, HOLD_SYSTEM_TERMINAL=`1`, HOLD_MECHANISM_UNRESOLVED=`1`.

Rolling autonomous scientific selection window becomes `SYSTEM / SYSTEM / MECHANISM`; theory-backward qualifying share remains `1/3`. `theory_backward_exception=null` for the fresh selection.

The prior no-target episode `NTE-20260921-STABLEMAIN-H7UNRESOLVED-v1` had four same-surface checks. The R28 qualitative reframe has now yielded a genuine prospectively typed MECHANISM selection, so the episode is marked `CLOSED_BY_FRESH_MECHANISM_SELECTION_AFTER_QUALITATIVE_REFRAME`. Those historical no-target checks remain outside candidate and conversion denominators.

Architecture active=`M1/S0`; queued=`M0/S0`.
Historical Architecture terminal dispositions remain HOLD_SYSTEM_TERMINAL=`5`, HOLD_METHOD_LIMITED=`1`, HOLD_CONTRACT_AMBIGUITY=`1`, REJECT=`0`.
PRE_FORMAL eligible=`1`; READY=`0`.
Recent completed MAIN Architecture cycles remain SYSTEM=`5`, MECHANISM=`0`; no comparable durable wall-clock is available.
SYSTEM-over-comparable-MECHANISM exceptions=`0`.

## Literature / Independent Audit / Methodology / Steward

Literature is fresh `LIT-20260921T062846+0900-R17-ACTIONVISIT-6E3B91C4`. It strengthens the ordinary count-based exploration-state reduction for `CAND-V05-NONLEARNING-ACTION-VISIT-CARRYOVER-01` and motivates only a fresh SYSTEM evaluation-isolation successor. It does not promote or reduce the fresh Assembly causal object.

Independent Audit remains `AUD-20260920T223110+0900-R3-C19V4-REDUCTION-6B4E21D9`: C19-v4's immutable registered PASS remains valid for its exact narrow contrast, while programme-level SparkBrain-specific novelty remains `REDUCIBLE` because authoritative C19-R2's fixed seven-state FSA is the decisive ordinary reduction. No consumed result is rerun, rescored, or relabeled.

Methodology is `METHCAL-20260921T062111+0900-R29-C5E1A7D2`, `WELL_CALIBRATED`. R29 prospectively kept the qualitative reframe policy and recorded its first live execution as not yet observed. Fresh SUB occurred after R29 and is therefore the first live positive rollout observation, but it has **not yet been independently ratified by Methodology**. Scientific admission and readiness bars remain unchanged.

Repository Steward `STEWARD-20260921T015217+0900-G2-7D3A91C4` is governance advisory only. Fresh independent reads still show rulesets=`0`, PR #148/#149 open and unmerged, and no change to immutable evidence/control/preserve anchors.

## MAIN / SUB allocation

`main_lane=V05_ASSEMBLY_UNIT_CAUSAL_SELECTIVITY_MATCHED_LOAD_ARCHITECTURE_CYCLE1_COMPARATOR_FEASIBILITY`

`sub_lane=BOUNDED_SECONDARY_DISCOVERY_BY_MARGINAL_INFORMATION_GAIN_NO_MAIN_DUPLICATION`

`sub_fallback=NO_OP_WITH_OBSERVABLE_DUPLICATION_OR_LOW_INFORMATION_REASON`

`system_priority_exception.used=false`

MAIN now owns the fresh central MECHANISM successor. SUB must not duplicate its Assembly causal comparator work and may select independent bounded Discovery by marginal information gain.

## Top 3 / GO-STOP

1. MAIN — `CAND-V05-ASSEMBLY-UNIT-CAUSAL-SELECTIVITY-MATCHED-LOAD-01` comparator-feasibility Architecture. Claim ceiling=`MECHANISM`. **GO_NON_EVIDENTIARY_COMPARATOR_FEASIBILITY_ARCHITECTURE_ONLY**.
2. SUB — independent bounded nonduplicative Discovery. Claim ceiling must be prospectively fixed as MECHANISM or SYSTEM. Conditional GO; no duplication of MAIN.
3. Fresh action-policy evaluation-isolation Architecture successor motivated by Literature R17. Claim ceiling=`SYSTEM`. `STOP_NOT_ALLOCATED_WHILE_HIGHER_VALUE_MECHANISM_MAIN_OBJECT_ACTIVE`.

MAIN prospective contingency:
- if an outcome-independent exact activity/topology/sham comparator contract is feasible: STOP and return to fresh Analyst review before any intervention outcome;
- if exact matching is infeasible on the supported DEV surface: `HOLD_MECHANISM_UNRESOLVED` and STOP;
- if comparator definition requires seeing intervention outcomes: invalid for prospective use, STOP and reframe as a fresh object;
- if supported reachability/API contract fails: STOP for fresh classification.

No same-run suppression outcome is authorized. Any change to candidate, comparator, metric, threshold, resource contract, runtime/model, identity, readiness or claim ceiling after outcome knowledge requires STOP + fresh object. A later `preformal_eligible=true + READY` state still requires fresh Analyst review before PRE_FORMAL.

## Integrity / identities / blockers

Consumed/no-retry identities remain unchanged:
`c19-external-v2-official-v4`; C19-R1 revision-authority official-v1/v2; `c19-r2-fsa-state-tracker-official-v1`; `pd01-long-history-fading-memory-official-v1`; `ni01-no-ignition-selective-prediction-official-v1`; `h5-event-routing-work-reduction-official-v1`.

New identity consumption=`0`.

Current blockers:
- matched-load/topology comparator contract for the fresh Assembly causal successor is not yet prospectively fixed;
- H7 still lacks a fresh native responsibility-sensitive object and matched comparator/falsifier;
- PRE_FORMAL READY=`0`;
- no fresh FORMAL one-way identity/STARTED/TEST/scorer/preserve authority;
- eligibility public semantic clock remains unspecified;
- action-policy evaluation-vs-real-visit mutation contract remains unspecified.

Utility request: none. Current Utility assignment remains IDLE.

## Generation / inputs / persistence target

Inputs:
- Control `CTRL-20260921T025500+0900-R19-9D2C4A71@dcdea1bbd1490da004bce69d4b7f4f7b4d37fbd4`
- MAIN `MAIN-20260921T061540+0900-PRIMARY-FUNNEL21-HOLD-R28-4C8A21D7@6b3bf125b75e7bccc4eef670fb3ca7ee2df4e43a`
- SUB `SUB-20260921T064900+0900-THEORY-ASMCAUSAL-7A4C91E2@dd0a61766f90418365c6158e8bed1996f8b17d5a`
- Literature `LIT-20260921T062846+0900-R17-ACTIONVISIT-6E3B91C4@c68021616b412a8ff6e94b72d57fb11ff609d4c2`
- Audit `AUD-20260920T223110+0900-R3-C19V4-REDUCTION-6B4E21D9`
- Methodology `METHCAL-20260921T062111+0900-R29-C5E1A7D2@03964aa181c901b705bf3e2e5e7e3df82b724f40`
- Steward `STEWARD-20260921T015217+0900-G2-7D3A91C4@4f959999d546a58a7862205ca06623654fb004fe`
- Utility `@472726e572a854fe3577e2733bb1de37c05df1fa`
- previous Analyst `EVA-20260921T055830+0900-R28-4D7A91C2@cde085b48dde724b2ac814585d7f0757bf16ef63`

Persistence target is only `ops/evidence-analyst-handoff` designated `analysis/orchestrator/latest.md`, `analysis/orchestrator/state.json`, and append-only `analysis/orchestrator/history/2026-09-21/0658.md`, in one atomic fast-forward commit. No scientific execution, workflow dispatch, identity consumption, research PR merge, immutable evidence/control/preserve mutation, force-push, or scheduler-definition change is authorized or performed.
