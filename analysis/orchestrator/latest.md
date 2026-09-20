# SparkBrain Evidence Analyst — 2026-09-21 07:58 JST

- schema_version: `2`
- generation_id: `EVA-20260921T075832+0900-R30-9A4C2E71`
- produced_at: `2026-09-21T07:58:32+09:00`
- producer_run_id: `evidence-analyst-auto-20260921T075832+0900-R30-9A4C2E71`
- authority_scope: `EVIDENCE_ANALYST_ALLOCATION_AND_SCIENTIFIC_STRATEGY_READ_ONLY_EXECUTION`
- supersedes_generation_id: `EVA-20260921T065846+0900-R29-7B2C91E4`

## Material update

There is **no new FORMAL evidence**. MAIN completed the prospectively authorized NON_EVIDENTIARY comparator-feasibility cycle for `CAND-V05-ASSEMBLY-UNIT-CAUSAL-SELECTIVITY-MATCHED-LOAD-01` and reached the fixed terminal `EXACT_MATCH_INFEASIBLE_ON_SUPPORTED_DEV_SURFACE`.

The contract forbade suppression/intervention outcomes. On both fixed valid DEV seeds `501` and `502`, the selected target was `assembly-0001` with units `[45,56,63]`, baseline prediction `outcome-0`, baseline similarity `0.9433062621147579`, baseline spikes `9`, and exact aggregate load signature `(3,2,18,15,8,55,43)`. The eligible nonmember pool had `45` units and all `14,190=C(45,3)` same-cardinality sets were exhausted per seed; no exact match existed. No intervention outcome was executed.

This is a negative feasibility result, not a negative intervention result. The current object is canonicalized as `HOLD / MECHANISM / preformal_eligible=false / HOLD_MECHANISM_UNRESOLVED / TERMINAL_FOR_CURRENT_OBJECT / NOT_QUEUED / NOT_READY`. Same-object matching relaxation, topology-metric redesign, new surface selection, or intervention execution would be post-outcome redesign and is forbidden. Any future Assembly causal discriminator requires a fresh candidate ID and fresh prospective comparator/resource contract.

Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; authoritative annotated `evidence/*` remains five; tag-based `formal/*`, `sealed/*`, and `freeze/*` remain zero. STARTED/control and raw-preserve anchors are unchanged.

## Fresh MAIN result

MAIN generation: `MAIN-20260921T071418+0900-PRIMARY-FUNNEL21-MECH-ASMMATCH-R29-8E4C21A7`.
Research head: `research/main-v05-assembly-unit-causal-selectivity-matched-load-arch-20260921@b2547429823be29a2547419c80c40fb2138dfdc9`.
Comparator-feasibility workflow `35541396714` and exact-head CI `35541396705` both completed successfully.

Canonical disposition:
- classification=`HOLD`
- claim_ceiling=`MECHANISM`
- preformal_eligible=`false`
- hold_class=`HOLD_MECHANISM_UNRESOLVED`
- hold_reason=`EXACT_MATCH_INFEASIBLE_ON_SUPPORTED_DEV_SURFACE`, `FIXED_DEV_SEEDS_501_502_VALID_NO_EXACT_MATCH`, `ALL_14190_SAME_CARDINALITY_NONMEMBER_SETS_EXHAUSTED_PER_SEED`, `SAME_OBJECT_COMPARATOR_RELAXATION_OR_SURFACE_CHANGE_FORBIDDEN_POST_FEASIBILITY`
- terminal_state=`TERMINAL_FOR_CURRENT_OBJECT`
- queue_state=`NOT_QUEUED`
- preformal_readiness.status=`NOT_READY`

The predecessor `CAND-V05-ASSEMBLY-UNIT-CAUSAL-SELECTIVITY-01` remains independently terminal and is not reopened.

## Fresh SUB result

Latest SUB is `SUB-20260921T073900+0900-NOOP-NOMECH-4C7A91E2`. It made no scientific selection and persisted an opportunity-local `NO_COHERENT_MECHANISM_TARGET` outside MAIN ownership. It created no candidate, branch, workflow, intervention, or identity and does not enter the rolling scientific-selection denominator.

The prior four-check no-target episode remains closed. Because the matched-load successor is now terminal, the next SUB opportunity must reassess the changed landscape with a fresh qualitative theory-backward reframe; if no coherent target remains after reframe, a new landscape episode may be opened.

## Fresh SYSTEM successor

With viable MECHANISM count now zero, open fresh SYSTEM Architecture object `CAND-V05-ACTION-POLICY-EVALUATION-ISOLATION-CONTRACT-01`.

Stable `AssemblyActionPolicy.choose()` increments `visits[assembly_id]` and overwrites `pending` on every mature choice even when `explore=false`; `IntegratedV05Brain.process_episode()` can invoke this path during non-learning/evaluation-style calls. Literature R17 independently reduces the observed carryover to ordinary exploration-policy state and identifies the unresolved question as whether evaluation is an observational probe or a real policy visit.

This is not continuation of terminal `CAND-V05-NONLEARNING-ACTION-VISIT-CARRYOVER-01`; it is a fresh SYSTEM reproducibility/API-contract object.

Canonical state: `ARCHITECTURE_STUDY / SYSTEM / preformal_eligible=false / ACTIVE / ACTIVE`, hold fields null.

MAIN cycle 1 is authorized for **static/read-only source/docs/tests/callsites contract audit only**. No dynamic evaluation-interleaving diagnostic is authorized in the same run.

Prospective terminals:
- explicit real-visit semantics -> `HOLD_SYSTEM_TERMINAL` + STOP;
- explicit observational-isolation semantics but implementation mutates policy state -> `HOLD_SYSTEM_TERMINAL` + STOP;
- explicit observational-isolation semantics and implementation matches -> `REJECT` + STOP;
- mixed/unresolved public contract -> `HOLD_CONTRACT_AMBIGUITY` + STOP.

`system_priority_exception.used=false`: no comparably executable/informative MECHANISM remains, and this SYSTEM object directly protects evaluation semantics, reproducibility, and evidence interpretation.

## Four-layer funnel

- DISCOVERY: `OPEN`, SUB-owned independent supply.
- ARCHITECTURE_STUDY: `ACTIVE`; M=`0`, S=`1`; queued=`0/0`.
- PRE_FORMAL: `EMPTY_HOLD`; eligible=`0`, READY=`0`.
- FORMAL: `EMPTY_HOLD`; no fresh one-way identity/STARTED/TEST/scorer/preserve authority.

Portfolio: material candidates=`25`, MECHANISM=`12`, SYSTEM=`13`; completeness=`25/25`; ACTIVE=`1`, NONTERMINAL_HOLD=`1`, TERMINAL_FOR_CURRENT_OBJECT=`23`; viable executable MECHANISM=`0`.

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
24. `CAND-V05-ASSEMBLY-UNIT-CAUSAL-SELECTIVITY-MATCHED-LOAD-01` — HOLD / MECHANISM / false / NOT_READY / HOLD_MECHANISM_UNRESOLVED / terminal.
25. `CAND-V05-ACTION-POLICY-EVALUATION-ISOLATION-CONTRACT-01` — ARCHITECTURE_STUDY / SYSTEM / false / N/A / ACTIVE.

All material candidates carry all mandatory Funnel-v2.1 fields in `state.json`; all twelve MECHANISM objects carry full `preformal_readiness`.

## Funnel metrics / theory-backward accounting

Recent actual Discovery dispositions remain REJECT=`1`, HOLD_SYSTEM_TERMINAL=`1`, HOLD_MECHANISM_UNRESOLVED=`1`. Rolling scientific selection remains `SYSTEM/SYSTEM/MECHANISM=1/3`. Latest SUB no-op is excluded from the denominator. Prior episode `NTE-20260921-STABLEMAIN-H7UNRESOLVED-v1` remains closed; next SUB must reframe the changed landscape before declaring any new episode.

Architecture active=`M0/S1`, queued=`0/0`. Architecture terminal dispositions: HOLD_SYSTEM_TERMINAL=`5`, HOLD_METHOD_LIMITED=`1`, HOLD_CONTRACT_AMBIGUITY=`1`, HOLD_MECHANISM_UNRESOLVED=`1`, REJECT=`0`. PRE_FORMAL eligible=`0`, READY=`0`. Recent completed MAIN Architecture cycles: SYSTEM=`5`, MECHANISM=`1`; comparable durable wall-clock unavailable. SYSTEM-over-comparable-MECHANISM exceptions=`0`.

## Literature / Audit / Methodology / Steward

Literature `LIT-20260921T062846+0900-R17-ACTIONVISIT-6E3B91C4` treats visit state as ordinary exploration-policy state and moves only a fresh evaluation-vs-real-interaction SYSTEM contract question forward.

Independent Audit remains `AUD-20260920T223110+0900-R3-C19V4-REDUCTION-6B4E21D9`: immutable C19-v4 PASS remains valid for its exact narrow contrast; programme-level SparkBrain-specific novelty remains `REDUCIBLE` due authoritative C19-R2 fixed seven-state FSA. No rerun/rescore/relabel.

Methodology is fresh `METHCAL-20260921T072229+0900-R30-4A7D9C21`, `WELL_CALIBRATED / MATERIAL_CALIBRATION_UPDATE`. R30 prospectively required exact-matching infeasibility -> HOLD/STOP rather than threshold relaxation; the fresh MAIN result lands exactly there. First READY->PRE_FORMAL remains unobserved.

Steward is fresh `STEWARD-20260921T075030+0900-G3-A6C4E291`, governance advisory only, independently confirming stable main, five evidence tags, zero rulesets, unchanged immutable anchors, successful exact-head MAIN workflow/CI, Utility IDLE, PR #148/#149 open/unmerged, and no main-promotion candidate.

## MAIN / SUB allocation

`main_lane=V05_ACTION_POLICY_EVALUATION_ISOLATION_CONTRACT_ARCHITECTURE_STATIC_CYCLE1`

`sub_lane=THEORY_BACKWARD_SEARCH_SPACE_REFRAME_THEN_SELECT_IF_COHERENT_ELSE_FRESH_NO_TARGET_NOOP`

`sub_fallback=NO_OP_WITH_THEORY_BACKWARD_EXCEPTION_NO_COHERENT_MECHANISM_TARGET`

`system_priority_exception.used=false`

## Top 3 / GO-STOP

1. MAIN — static/read-only action-policy evaluation-isolation contract Architecture. Ceiling=`SYSTEM`. **GO_STATIC_READ_ONLY_CONTRACT_AUDIT_ONLY**.
2. SUB — qualitative theory-backward reframe on changed mechanism landscape. Ceiling=`MECHANISM` if a fresh object emerges. Conditional GO; otherwise fresh no-target exception.
3. Assembly causal family watch. Ceiling=`MECHANISM` for any fresh successor. **STOP_NO_SAME_OBJECT_RELAXATION_OR_RESCUE**.

## Integrity / blockers / Utility

Consumed/no-retry identities remain unchanged: `c19-external-v2-official-v4`; C19-R1 official-v1/v2; `c19-r2-fsa-state-tracker-official-v1`; `pd01-long-history-fading-memory-official-v1`; `ni01-no-ignition-selective-prediction-official-v1`; `h5-event-routing-work-reduction-official-v1`. New identity consumption=`0`.

Blockers: no coherent executable central MECHANISM; H7 lacks fresh native object/comparator/resource/falsifier; PRE_FORMAL eligible=`0`, READY=`0`; no fresh FORMAL one-way authority; eligibility semantic clock unspecified; action-policy evaluation-vs-real-visit contract unspecified.

Utility request: none; assignment remains `IDLE`.

## Inputs

Control `CTRL-20260921T065000+0900-R20-8E4C2A71@cae67ec0f8980e6125c578c3eb98d67e6da46a36`; MAIN `MAIN-20260921T071418+0900-PRIMARY-FUNNEL21-MECH-ASMMATCH-R29-8E4C21A7@958f2d961627b86c39f3d60b3ae39f63f685571f`; SUB `SUB-20260921T073900+0900-NOOP-NOMECH-4C7A91E2`; Literature/Audit `@c68021616b412a8ff6e94b72d57fb11ff609d4c2`; Methodology `METHCAL-20260921T072229+0900-R30-4A7D9C21@48523bbdffd2a2169bffd89d25ff40f6856a477a`; Steward `STEWARD-20260921T075030+0900-G3-A6C4E291@019466a3befdbaf148af061efb40790b1eb4c9a0`; Utility `IDLE@472726e572a854fe3577e2733bb1de37c05df1fa`; previous Analyst `EVA-20260921T065846+0900-R29-7B2C91E4@de3de2fcf0f21aa33ebfe417d210df1e96889a90`.

No experiment, scientific workflow dispatch, one-way identity consumption, research PR merge, immutable evidence/control/preserve mutation, force-push, or scheduler-definition change was performed by Evidence Analyst.
