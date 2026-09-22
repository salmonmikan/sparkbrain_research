# SparkBrain Evidence Analyst — 2026-09-22 13:09 JST

schema_version: `2`  
generation_id: `EVA-20260922T130900+0900-R62-D4A7C21F`  
produced_at: `2026-09-22T13:09:00+09:00`  
producer_run_id: `evidence-analyst-auto-EVA-20260922T130900+0900-R62-D4A7C21F`  
authority_scope: `EVIDENCE_ANALYST_ALLOCATION_AND_SCIENTIFIC_STRATEGY_READ_ONLY_EXECUTION`  
supersedes_generation_id: `EVA-20260922T124300+0900-R61-C7F421A9`

## Result

`MATERIAL_STRATEGY_UPDATE_H7_CYCLE2_PREFLIGHT_FOUND_SCIENCE_AFFECTING_COMPARATOR_GAPS_VERSIONED_DEV_R2_AUTHORIZED`

H7 DEV-R1 cycle 2 reached the exact integrity stop that R61 required. The implementation-only preflight is now at `research/main-h7-dev-r1-claim-scoped-causal-contract-r60-cycle1@c97af135742a7cd3af94c857f4d5b83d7707075d`, ordinary CI `35685323080` is green, and no fit training, calibration, discriminator access, scientific metric, result-bearing intervention, PRE_FORMAL/FORMAL action, or identity consumption occurred.

The preflight independently exposed two science-affecting specification gaps in the frozen R1 comparator panel:

1. `FINITE_STATE_ROUTE_HISTORY_V1` does not fix fit-time previous-prediction closure or unseen-state prediction.
2. `ELIGIBILITY_ROUTE_LEDGER_V1` does not fix event-encoder provenance, head optimizer/loss/update order, or the calibration operation.

MAIN correctly stopped rather than inventing those semantics after implementation had begun. The one intervening Ruff E402/I001 repair is classified `SCIENCE_INVARIANT_REPAIR`; it changed only the optional-torch test import lint suppression and the exact-head CI is green.

Under HUMAN-20260922-005 and Methodology R58, cycle 3 is a mandatory reassessment rather than an automatic terminal. The reassessment outcome is `REFRAME_VERSION_CONTINUE`: keep candidate `CAND-H7-RESPONSIBILITY` active at `ARCHITECTURE_STUDY / MECHANISM / preformal_eligible=true / NOT_READY`, preserve DEV-R1 and its cycle-2 preflight unchanged, and authorize an explicit versioned development revision `H7-DEV-R2-COMPARATOR-PROTOCOL-CLOSURE`.

## H7 DEV-R2 prospective delta

DEV-R2 inherits the R1 claim scope, native `TOP1_SELECTED_LOCAL_NODE_CUT_V1` intervention family, worlds, fit/calibration/discriminator identities, native/dense model seeds and training budget, primary/secondary metrics, positive-phenomenon floor, `1e-7` numerical no-change tolerance, reduction direction, resource/privilege floor, and falsifier intent. It changes only the science-affecting fields that R1 left underspecified plus the prospective validity checks required by Literature R28. This is a versioned development revision, not a repair of an observed H7 scientific result.

### `FINITE_STATE_ROUTE_HISTORY_V2`

Use a non-self-referential state key `(previous_unperturbed_rank1_route_or_START, current_route_token)` instead of previous predicted label. At episode start the previous token is `START`. For each fit step, add both the baseline row `(previous_unperturbed_rank1, current_unperturbed_rank1)` and the paired cut row `(previous_unperturbed_rank1, CUT)` with the same fit target. Advance the persistent previous token only with the unperturbed baseline rank-1 route because the cut arm is one-step and discarded. Predict by fit-count majority with lexical label tie-break. For an unseen key, use the global fit-split majority label with the same lexical tie-break. Reset at every episode boundary. No calibration/discriminator labels may alter the table.

This replaces `FINITE_STATE_ROUTE_HISTORY_V1` in DEV-R2. The replacement is deliberately a stronger, well-posed route-history state-machine reduction rather than a rescue weakening.

### `ELIGIBILITY_ROUTE_LEDGER_V2`

Use a detached, frozen copy of the fitted native DEV-R2 event encoder as the exact 24-d event encoder. The encoder receives the same current external event fields as native and is not updated by the ledger comparator. Train only the 3-class linear head from seed `7603`, for 4 epochs at lr `0.012`, with Adam default betas/eps and zero weight decay, cross-entropy only, deterministic episode order from generator seed `7603 + epoch`, ledger reset per episode, `zero_grad` per episode, mean episode loss, gradient clip `2.0`, and one optimizer step per episode. Training uses only unperturbed baseline fit trajectories; the cut arm is evaluated by excluding `selected[0]`, forcing that ledger coordinate to zero for the paired current-step prediction, and discarding the cut ledger afterward. Calibration is explicitly `IDENTITY_NO_TUNABLE_CALIBRATION`: the calibration split may be used only for fixed conformance/finite-output diagnostics and cannot tune weights, temperature, thresholds, exclusions, or hyperparameters.

This replaces `ELIGIBILITY_ROUTE_LEDGER_V1` in DEV-R2 and intentionally gives the ordinary reduction a strong representation privilege rather than an artificial raw-input handicap.

### Literature R28 disposition

- Intervention well-posedness becomes an implementation validity contract: deterministic frozen route selection, single-valued finite outputs, unchanged non-target input/parameters/RNG, identical shape/dtype, and no cut-state carryover. Failure is `INVALID_INTERVENTION`, not a scientific negative.
- Abstraction-map complexity is `NOT_APPLICABLE_CURRENT_REVISION`: the object is a native selected route/state and no learned cross-system alignment map is used.
- Regime scope remains the exact four frozen development worlds. No broad regime/generalization claim is added.
- No extra reservoir/iSSM panel member is silently added in DEV-R2. The existing dense recurrent comparator is already intervention-mapped. A materially stronger matched intervention-aware dynamical baseline can motivate a later version only prospectively; it is not a hidden READY gate.

## Cycle-3 authorization

`GO_H7_DEV_R2_VERSIONED_PROTOCOL_CLOSURE_CYCLE3_IMPLEMENTATION_ONLY_STOP_BEFORE_TRAINING_CALIBRATION_DISCRIMINATOR_OR_OTHER_RESULT_BEARING_DEVELOPMENT`

MAIN may first persist the DEV-R2 contract/revision, then implement the exact V2 comparator semantics and intervention-well-posedness/conformance tests. Same-run lint/import/build/path/serialization/logging/hash fixes are allowed as `SCIENCE_INVARIANT_REPAIR`. Do not train native/comparators, read calibration/discriminator surfaces, compute scientific metrics, or change any newly frozen scientific field in this cycle. If exact implementation succeeds, STOP for fresh Analyst review; a later cycle may authorize bounded development fitting/testing and assess whether PRE_FORMAL readiness can become READY. If another science-affecting ambiguity appears, STOP and return it without filling it locally.

## Four-layer state

- DISCOVERY: 0 canonical active; noncanonical Question Formation completed one bounded scan with zero retained questions.
- ARCHITECTURE_STUDY: MECHANISM active `1`, SYSTEM active `0`; H7 is the only active canonical object.
- PRE_FORMAL: eligible `1`, READY `0`.
- FORMAL: fresh one-way authority `0`.

Canonical population remains `32 = MECHANISM 13 / SYSTEM 19`; classification completeness remains `32/32`; lifecycle counts remain `ACTIVE=1 / NONTERMINAL_HOLD=0 / TERMINAL_FOR_CURRENT_OBJECT=31`. Canonical development-phase distribution remains `OPEN_DEVELOPMENT=2 / RESULT_EXPOSED_DEVELOPMENT=30 / CONSUMED_ONE_WAY=0`; the separate consumed-scientific-identity registry remains `CONSUMED_ONE_WAY=7`.

Cycle-3 reassessment count becomes `1`, disposition `H7 -> REFRAME_VERSION_CONTINUE_DEV_R2`. No fresh successor is generated or admitted. All 19 terminal SYSTEM objects retain their explicit successor assessment: fresh SYSTEM successor potential for 16; none for #14/#27/#28; fresh MECHANISM successor potential from those terminal SYSTEM objects remains 0.

## SUB / candidate supply

Fresh SUB `SUB-20260922T125100+0900-QFD-R61-ZERORETAIN-C7F421A9` completed the HUMAN-007 bounded `QUESTION_FORMATION_DISCOVERY` scan and retained zero questions. It correctly rejected duplicate/rescue-like pre-semantic, Assembly completion/endogenous-continuation and learned-delay paths, and did not promote the #32 family because it remains SYSTEM-only and tooling-gated. This scan is noncanonical, NON_EVIDENTIARY, denominator-excluded, and does not change the rolling canonical theory-backward share `1/3`.

Because H7 remains a viable MECHANISM object and this scan just returned zero retainable questions, SUB now stays independent-idle until a materially fresh non-MAIN question-supply surface appears. Do not repeatedly rescan unchanged surfaces merely to create activity. The old no-target episode remains closed at canonical check count 23. Phenomenon-first shadow trigger remains inactive while H7 is active.

## External / audit / methodology / utility

- Literature R28 adds intervention admissibility, alignment-map privilege, regime coverage, and intervention-aware dynamical reduction pressure. These are prospective inputs and cannot silently patch DEV-R1; the claim-relevant portion is incorporated only through DEV-R2 above.
- Independent Audit R6 remains unchanged: PD01's frozen FAIL is protocol-valid and consumed, but its narrative ceiling is `NO_DEMONSTRATED_LONG_LAG_RECOVERY_AND_NO_ADVANTAGE_OVER_THE_FIXED_FADING_MEMORY_RESERVOIR`; null-vs-null is not positive mechanistic reduction evidence.
- Methodology R58 supports HUMAN-005: flexible/versioned development, cycle-3 reassessment, PRE_FORMAL iteration, same-object science-invariant repair, and an unchanged strict one-way FORMAL floor.
- Repository Steward G9 remains stale relative to HUMAN-005/006/007, active H7 development and repaired Utility tooling; governance advice only.
- Utility exact repaired head `9f9d18065b481d8597236b0b682f0574c251b319` is CI-green. Fresh Steward review is still absent; merge/promotion is not authorized and CI does not cure trusted-producer/raw-to-digest semantic trust limits.

## Allocation

- MAIN: `H7_DEV_R2_VERSIONED_COMPARATOR_PROTOCOL_CLOSURE_ARCHITECTURE_CYCLE3_IMPLEMENTATION_ONLY`
- SUB: `INDEPENDENT_IDLE_AFTER_ZERO_RETAINED_QUESTION_FORMATION_UNTIL_FRESH_NON_MAIN_SUPPLY_DELTA`
- SYSTEM priority exception: `used=false`

## Top 3

1. MECHANISM / RESULT_EXPOSED_DEVELOPMENT / VERSIONED REVISION — H7 DEV-R2 comparator-protocol closure and implementation-only conformance. **GO**, then STOP before training or result-bearing development.
2. noncanonical candidate supply — SUB waits for fresh independent material after the zero-retained Question Formation scan. **STOP_CURRENT_SURFACES / GO_ONLY_ON_FRESH_DELTA**.
3. SYSTEM / proposed OPEN development — fresh #32-family successor. **STOP** until a new candidate ID, trusted equivalence chain and fresh resource contract exist; predecessor #32 remains terminal.

## Integrity

No experiment, result-bearing scientific workflow dispatch, one-way identity consumption, research PR merge, immutable evidence/control/preserve mutation, scheduler mutation, or historical PASS/FAIL rewrite was performed by Evidence Analyst. Consumed identities remain C19-v4, C19-R1 official-v1/v2, C19-R2, H5, NI01 and PD01.

Utility request: `none`.
