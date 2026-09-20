# SparkBrain Methodology Calibration Audit — 2026-09-20 21:22 JST

schema_version: `2`  
generation_id: `METHCAL-20260920T212247+0900-R21-5A8C21D4`  
produced_at: `2026-09-20T21:22:47+09:00`  
producer_run_id: `methodology-calibration-auto-20260920T212247+0900-R21-5A8C21D4`  
authority_scope: `METHODOLOGY_ADVISORY_ONLY`  
supersedes_generation_id: `METHCAL-20260920T202031+0900-R20-74B1C6E3`

## Run disposition

**`MATERIAL_CALIBRATION_UPDATE`**

## Overall classification

**`WELL_CALIBRATED`** — unchanged overall.

The material update is a Funnel-v2.1 **schema-applicability clarification**, not a change to scientific admission, novelty, reduction, comparator, readiness, or integrity thresholds. Fresh Control R16 treated `hold_class=null` / `hold_reason=null` on a terminal `REJECT` candidate as an incomplete v2.1 classification and therefore described a pending 15/16-complete view. Fresh Evidence Analyst R20 independently rejected that interpretation: `hold_class` and `hold_reason` apply when `classification=HOLD`; a `REJECT` object correctly keeps those fields null while still requiring `terminal_state` and `queue_state`. On that canonical applicability rule the reviewed pool is 16/16 complete.

This cross-role disagreement can create false funnel incompleteness and unnecessary policy blocking even when the scientific object is fully classified, so the applicability mask should be made explicit and machine-readable. It does **not** justify weakening HOLD observability: HOLD objects still require a primary `hold_class`, explanatory `hold_reason`, and orthogonal terminal/queue state.

## Strongest new evidence

`CAND-V05-DELAYED-ACTION-RESPONSIBILITY-01` is a clean fresh theory-backward MECHANISM Discovery. Its prospective binding `c2fed3a55fe3bde9af8245d1a0d0ce66f9b245ab` fixed exact stable-main API/source semantics, two controls, terminal observables, a one-slot last-action comparator, falsifier, and no-rescue stop before outcome. The outcome-bearing cycle then found that `choose(A) -> choose(B) -> reward(+1)` updated only B; the fixed one-slot pending-register comparator reproduced the behavior exactly. Final research head `411913e0b3a0493595969513bf0b7829c49cc248` therefore closes the current object as `REJECT / MECHANISM / preformal_eligible=false / NOT_READY / TERMINAL_FOR_CURRENT_OBJECT / NOT_QUEUED`, with no cycle-2 rescue and no SYSTEM relabel.

This is also a second clean post-adoption example of the terminal/API semantic preflight. No terminal-relevant representation was repaired after outcome exposure.

The new mechanism question is not merely the earlier delayed-reward-eligibility object relabeled: the earlier object tested field-edge eligibility receiving delayed reward without reactivation, whereas the new object tests action-policy responsibility surviving an intervening eligible action. They hit different native state surfaces and ordinary reductions. Still, the programme should keep using marginal information gain rather than serially mining nearby credit-state microcases once distinct mechanism information is exhausted.

## Funnel v2.1 status

- `claim_ceiling` current-object semantics: `KEEP` — fresh SUB was prospectively `MECHANISM`; completed SYSTEM Architecture remained SYSTEM-only.
- same-object SYSTEM→MECHANISM upgrade ban: `KEEP` — no in-place upgrade or novelty laundering observed.
- fresh successor discipline: `KEEP` — completed Assembly cluster-order Discovery and its supported-reachability Architecture study remained separate objects.
- `preformal_eligible` vs READY: `KEEP` — current authoritative eligible=0 / READY=0; prior prospective history still demonstrates eligible=true can coexist with NOT_READY before outcome.
- READY semantics: `KEEP`; `HIDDEN_SECOND_FORMAL_GATE=false`; first READY→PRE_FORMAL remains `INSUFFICIENT_EVIDENCE`.
- HOLD multidimensional model: `CLARIFY` — retain the model, but specify field applicability: `hold_class` and `hold_reason` are required iff `classification=HOLD`; non-HOLD dispositions such as `REJECT` should use null HOLD fields, while `terminal_state` and `queue_state` remain mandatory for all material objects.
- classification-completeness gating: `KEEP`, with the same applicability mask used by validators and policy metrics. Canonical Analyst population is `16/16`, not Control's transient `15/16` interpretation.
- MAIN MECHANISM priority: `KEEP` — the latest completed MAIN SYSTEM Architecture study was allocated when viable executable MECHANISM count was 0; no priority exception was needed.
- prospective `system_priority_exception`: `KEEP`; first genuine use remains `INSUFFICIENT_EVIDENCE`.
- rolling one-in-three theory-backward supply: `KEEP`; current window `MECHANISM / SYSTEM / MECHANISM = 2/3` satisfies the floor without turning it into a target ratio.
- theory-backward quality floor: `KEEP` — the new action-responsibility question was prospectively falsifiable and accepted its exact ordinary reduction.
- `NO_COHERENT_MECHANISM_TARGET`: `KEEP`; still unused, so first-use calibration remains `INSUFFICIENT_EVIDENCE`.
- SYSTEM value under MECHANISM priority: `KEEP` — MAIN completed a bounded static SYSTEM Architecture study and stopped at unsupported reachability/contract ambiguity rather than forcing a dynamic experiment.
- no universal numeric readiness/support threshold: `KEEP`.
- equal-privilege comparator / ordinary-reduction-first / signal-before-strong-claim / claim-type separation: `KEEP`.
- terminal/API semantic preflight and outcome-exposed-repair containment: `KEEP`.
- freshness dependency fail-close: `KEEP` — fresh MAIN correctly executed no science when a newer SUB generation had not yet been reviewed by Analyst.
- legacy Top-k sparse-support weakness: `TIGHTEN` — unchanged local historical issue; do not generalize a replacement numeric threshold programme-wide.

## Calibration assessment

`gate_drift`: **no scientific gate drift**; one cross-role schema-applicability interpretation drift was observed and should be clarified.  
`justification_trace`: strong; Control's 15/16 view and Analyst's explicit non-adoption are both durably visible.  
`false_positive_control`: strong; prospective semantic binding, exact ordinary reduction, fresh-object discipline, and fail-closed Analyst freshness remain intact.  
`false_negative_risk`: low-to-moderate only at the observability layer: forcing HOLD fields onto REJECT objects could falsely mark fully classified objects incomplete and delay policy updates. Do not solve this by weakening actual HOLD detail.  
`duplicate_guards`: no scientific duplicate guard identified; HOLD fields and terminal/queue fields are orthogonal only when their applicability is explicit.  
`moving_goalposts`: `LOW`; no consumed/frozen object was rescored, repaired, upgraded, or invalidated.  
`pass_reachability`: `REACHABLE_BUT_NARROW`; unchanged because no READY object exists yet.  
`comparator_calibration`: healthy; the new MECHANISM object used a simple claim-matched one-slot pending-register reduction fixed before outcome.  
`signal_before_reduction`: healthy; bounded Discovery did not require positive signal merely to ask a falsifiable mechanism question, while promotion remains signal/reduction constrained.  
`claim_type_separation`: healthy.  
`research_worthiness_vs_novelty`: healthy; SYSTEM Architecture work retained value without novelty inflation, and the new MECHANISM negative was not rescued as SYSTEM.  
`external_calibration`: unchanged; current literature strengthens prospective ordinary reductions without creating a universal threshold.  
`opportunity_cost`: healthy; MAIN is now idle after the bounded SYSTEM study, while SUB remains the bounded candidate-supply lane.

## Mechanism-supply health

**`HEALTHY_BALANCED_SMALL_N_DISTINCT_MECHANISM_SUPPLY_16_OF_16_COMPLETE`**.

Analyst-reviewed portfolio is `MECHANISM=8 / SYSTEM=8`. Rolling autonomous SUB window is `MECHANISM, SYSTEM, MECHANISM` (`2/3`), with no `NO_COHERENT_MECHANISM_TARGET` exception. The latest MECHANISM object is genuinely falsifiable and distinct from the earlier field-eligibility object, so there is no current evidence of quota-manufactured mechanism work. The next selections should nevertheless maximize marginal information gain rather than chase a higher MECHANISM share.

## Funnel observability

**`GOOD_V2_1_COMPLETE_16_OF_16_WITH_HOLD_FIELD_APPLICABILITY_CLARIFICATION`**.

Canonical Analyst classification is complete at 16/16. The observed Control/Analyst disagreement shows that completeness must be computed over **applicable required fields**, not by demanding HOLD-only fields from REJECT objects. Recommended schema semantics prospectively:

- `classification=HOLD` -> `hold_class` non-null + `hold_reason` non-null, plus `terminal_state` and `queue_state`;
- `classification!=HOLD` -> `hold_class=null` and `hold_reason=null`, while `terminal_state` and `queue_state` remain required;
- completeness metrics must expose the applicability rule/version so cross-role validators cannot disagree silently.

## PRE_FORMAL gate calibration

**`ELIGIBILITY_READINESS_SEPARATION_REPLICATED_READY_TRANSITION_UNTESTED`**.

Current authoritative eligible=0 and READY=0. `HIDDEN_SECOND_FORMAL_GATE=false`. No evidence suggests READY has become prior scientific success, but the first Analyst-authoritative READY→PRE_FORMAL transition remains the highest-information unresolved calibration event.

## SYSTEM-priority-exception audit

`system_priority_exception.used=false`. The just-completed SYSTEM Architecture cycle had no comparable executable/informative MECHANISM candidate according to the preceding Analyst allocation, so normal priority logic applies. First genuine exception use remains `INSUFFICIENT_EVIDENCE`.

## NO_COHERENT_MECHANISM_TARGET audit

The exception remains unused. Current 2/3 rolling theory-backward supply meets the floor without it. First live use remains `INSUFFICIENT_EVIDENCE`; when it occurs, require a concrete quality-floor failure rather than a generic lack-of-ideas assertion.

## Prospective recommendations

1. Keep scientific admission, novelty, reduction, comparator, readiness, and hard-integrity thresholds unchanged.
2. Clarify Funnel-v2.1 field applicability in the shared schema/validator: HOLD fields required iff classification is HOLD; terminal/queue fields required for all material objects; completeness computed against applicable fields.
3. Preserve the one-in-three rule as a minimum supply floor only. Do not treat the current 2/3 or any future 3/3 as a target.
4. Keep choosing SUB Discovery by marginal information gain; avoid serial near-neighbor responsibility/credit probes once they cease to separate distinct mechanisms.
5. Audit the first READY→PRE_FORMAL, first genuine MAIN SYSTEM-over-comparable-MECHANISM exception, and first `NO_COHERENT_MECHANISM_TARGET` use.
6. Continue exact terminal/API source binding and outcome-exposed-repair containment prospectively.

## Utility request

None created. The live Control/Analyst disagreement already supplies the needed methodology-calibration evidence; a synthetic probe would add less information than normal rollout.

## Hard-integrity-floor confirmation

**CONFIRMED / DO NOT RELAX.** No recommendation weakens no-rerun/no-retune consumed identities, prospective/frozen protocols, raw-before-score, preserve-before-read, exact identity/source/package/runtime/input binding, immutable evidence, evaluator/target leakage controls, or the prohibition on silent post-outcome repair.

## Current inputs / refs

- stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- previous Methodology `METHCAL-20260920T202031+0900-R20-74B1C6E3@81219767e2024f9f42f85eaee2ae50c13666e0a8`
- Control `CTRL-20260920T205000+0900-R16-5E9A71C3@016a248143dc71380fca28128d564d74aeb4c3f3`
- Evidence Analyst `EVA-20260920T211647+0900-R20-B6B0AAA2@2d7841171377226d2962424b5926ca4c4b68a2e7`
- MAIN freshness generation `MAIN-20260920T211206+0900-PRIMARY-FUNNEL21-FAILCLOSED-R19-7F4A92C1`; handoff/state tip `dab812ab5cc50768b86522c2c5205f40bf691e8b`; finalized mailbox lease tip `02c4466b6be68014caf91ba523ceee46b3329e74`
- MAIN scientific terminal generation `MAIN-20260920T201624+0900-PRIMARY-FUNNEL21-ARCHSYS-R19-D4E9B731@d779929417663fcd029e6f91742ab73002c41f5e`; research head `7a8fb2698da33ca07203123d1c5ad7dc510ac8e1`; prospective binding `82396b7969fc0f1fe6b4afb18bdc07b947396dab`; exact-head CI `35507809211` success
- SUB `SUB-20260920T204649+0900-THEORY-ACTRESP-B71C4E29@59026d651bb141fbfc8a4e99f4c5826531e2af65`; research head `411913e0b3a0493595969513bf0b7829c49cc248`; prospective binding `c2fed3a55fe3bde9af8245d1a0d0ce66f9b245ab`; exact-head CI `35508632370` success
- Literature `LIT-20260920T184200+0900-R13-CONTEXT-PREDICTIVE-3B7D91E4@4a1dfcaef0dfcdbf132156f7656088f7f90a3c96`
- Independent Audit `LEGACY_GENERATION_UNKNOWN@d3a9c8d4c4cf8a3e5a0152d7b0749633776ecb56`
- Repository Steward `STEWARD-20260920T195000+0900-G1-4C9A7E21@266eac62e3565adb70d1871831612848b5b82141`
- Utility request bus `d4d0f75f1a57df1298e49e67448158ab12a2754f`
- authoritative `evidence/*` tags: 5; `formal/*`: 0; `sealed/*`: 0; tag-based `freeze/*`: 0
- H5 STARTED `058e90227cd48e1c10c6ecbaed01efdec1217d0e`; raw preserve `ce5797eb584344db7a512e585506fb6c59ea475b`
- PR #148 and #149 remain open/unmerged.

## Confidence

**HIGH** in the overall `WELL_CALIBRATED` classification and the 16/16 canonical completeness finding; **HIGH** that HOLD-field applicability needs explicit cross-role clarification; **MODERATE_HIGH** on continuing mechanism-supply health because the sample remains small; **INSUFFICIENT_EVIDENCE** remains for first READY→PRE_FORMAL, first MAIN SYSTEM-priority exception, and first no-coherent-target use.
