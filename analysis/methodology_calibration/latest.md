# SparkBrain Methodology Calibration Audit — 2026-09-20 19:24 JST

schema_version: `2`  
generation_id: `METHCAL-20260920T192400+0900-R19-3E7B5C91`  
produced_at: `2026-09-20T19:24:00+09:00`  
producer_run_id: `methodology-calibration-auto-20260920T192400+0900-R19-3E7B5C91`  
authority_scope: `METHODOLOGY_ADVISORY_ONLY`  
supersedes_generation_id: `METHCAL-20260920T182012+0900-R18-6B2F9C41`

## Run disposition

**`MATERIAL_CALIBRATION_UPDATE`**

## Overall classification

**`WELL_CALIBRATED`** — upgraded from `SLIGHTLY_TOO_PERMISSIVE`.

The specific unresolved process condition that justified the prior slightly-permissive classification has now been satisfied prospectively. A fresh outcome-bearing Discovery object started after Control R15, `CAND-V05-CONTEXT-CONDITIONED-PREDICTION-01`, bound terminal/public-API semantics to exact stable-main source blobs before outcome exposure, executed from that binding without terminal-relevant post-outcome repair, completed exact-head CI on attempt 1, and was then independently consumed by Evidence Analyst. The current rule therefore has both downstream containment evidence and one clean live producer-side prevention example.

This upgrade does **not** erase the two historical pre-adoption method defects and does not rescore them. It says the **current** methodology is now calibrated at that boundary. Requiring an unannounced multi-run success count before clearing the exact blocker that prior Methodology generations explicitly defined as “the first fresh post-Control-R15 outcome-bearing object” would itself move the calibration goalpost. Operational durability should still be watched prospectively.

## Material change since R18

### First clean post-adoption producer-side semantic preflight

Research branch `research/exploratory-sub-context-conditioned-prediction-20260920` was prospectively bound at `01d4cc8daf07be67b8f633434030241276a0a4b0`, directly from stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. Before any outcome-bearing execution, the contract verified exact stable-main source semantics:

- `PredictionDecision` fields `assembly_id`, `value`, `confidence` against `contracts.py` blob `048b93cddb16dbe9276a0e2c0f972406291c1cb2`;
- `AssemblyPredictor` count-state and deterministic prediction/tie semantics against `prediction.py` blob `9805031fb8db235d2f3cf4c81421b896d2597af4`;
- terminal predicates were explicitly bound to those public fields and state representation;
- any post-outcome terminal-semantic mismatch was prospectively mapped to method-limit STOP with no repaired same-object scientific closure.

The diagnostic commit `38c6f3cc972898c170fdf5853190ca33de8f6882` is a direct child of that binding and uses the bound `assembly_id`, `value`, `confidence`, and count-state semantics. The final research head is `f0a4157d869561e4201aca1c37663305bc5c8a5d`; exact-head CI run `35502970668` completed `success`, attempt 1. No terminal-relevant repair/rerun occurred.

This is exactly the live implementation check that remained unresolved in R18. Accordingly:

- `prospective_terminal_semantic_binding`: `TIGHTEN -> KEEP`;
- `producer_terminal_api_source_conformance_preflight`: `TIGHTEN -> KEEP`.

The change is evidence-driven: two pre-adoption outcome-exposed representation repairs justified the tightening; the first prospectively governed post-adoption outcome-bearing object demonstrates the tightened rule can be applied without making the research path impracticable.

### Independent downstream review remains conservative without adding a second gate

Evidence Analyst generation `EVA-20260920T190536+0900-R18-AC1DB49E@fec9320a8e8c868f4df91dafb1af75c640ae995a` independently consumed the new object and confirmed the clean preflight lineage. It classified the current object `REJECT / MECHANISM / preformal_eligible=false / NOT_READY / TERMINAL_FOR_CURRENT_OBJECT / NOT_QUEUED`, with no cycle-2 rescue, SYSTEM relabel, PRE_FORMAL promotion, or same-object redesign. The object had prospectively occupied `preformal_eligible=true` before outcome while still not being READY, preserving eligibility/readiness separation.

MAIN generation `MAIN-20260920T191546+0900-PRIMARY-FUNNEL21-HOLD-R18-8C2F41D7` consumed that fresh Analyst generation, created no object, used no SYSTEM-priority exception, and ended intentionally idle. Final durable run-report branch tip is `9d2bb49356d4ad3c009ce7a049f3a2285035a5e4`.

## Funnel v2.1 gate audit

| Gate / behavior | Classification | Finding |
| --- | --- | --- |
| hard one-way integrity floor | `KEEP` | Do not relax. |
| prospective terminal semantic binding | `KEEP` | Tightening is now prospectively adopted and cleanly live-demonstrated. |
| producer terminal API/source conformance preflight | `KEEP` | First post-adoption outcome-bearing object completed the intended preflight before outcome exposure. |
| Control/Analyst outcome-exposed repair containment | `KEEP` | Historical method-limited cases remain contained without retroactive rewrite. |
| repaired same-object clean closure/promotion/readiness ban | `KEEP` | Necessary integrity boundary; no relaxation. |
| repair lineage / outcome-exposure observability | `KEEP` | Historical defects remain reconstructable. |
| freshness/dependency fail-closed reconciliation | `KEEP` | MAIN waited for Analyst review of fresh SUB result before adopting Funnel fields. |
| current-object `claim_ceiling` | `KEEP` | Fresh object was prospectively typed MECHANISM; no permanent-topic/prestige use observed. |
| same-object SYSTEM→MECHANISM upgrade ban | `KEEP` | No violation. |
| fresh MECHANISM successor from SYSTEM | `KEEP` | Rule remains appropriate; no same-object laundering. |
| `preformal_eligible` distinct from READY | `KEEP` | Fresh object again shows prospective eligible=true while not READY. |
| READY semantics | `KEEP` | `HIDDEN_SECOND_FORMAL_GATE=false`; no READY object yet. |
| first Analyst-authoritative READY→PRE_FORMAL | `INSUFFICIENT_EVIDENCE` | Still unobserved. |
| multidimensional HOLD | `KEEP` | Method-limit, terminal and queue state remain orthogonally represented. |
| MAIN MECHANISM priority | `KEEP` | MAIN idles because no coherent executable central object exists. |
| prospective SYSTEM-priority exception | `KEEP` | Rule remains calibrated. |
| first SYSTEM-priority exception use | `INSUFFICIENT_EVIDENCE` | No live use. |
| rolling one-in-three theory-backward supply | `KEEP` | Current rolling scientific window is 3/3 MECHANISM but explicitly descriptive, not a target. |
| theory-backward quality floor | `KEEP` | Fresh selection was coherent/falsifiable and occurred when the 1-in-3 floor was already satisfied. |
| `NO_COHERENT_MECHANISM_TARGET` rule | `KEEP` | No evidence of escape-hatch use. |
| first `NO_COHERENT_MECHANISM_TARGET` use | `INSUFFICIENT_EVIDENCE` | Unobserved. |
| SYSTEM value under MECHANISM priority | `KEEP` | No starvation signal; 3/3 is not treated as a desired ratio. |
| classification-completeness gating | `KEEP` | Analyst-reviewed material population is 13/13 complete. |
| universal numeric readiness/support thresholds | `KEEP` | Continue prohibiting them. |
| equal-privilege comparator | `KEEP` | No new defect; literature strengthens claim-local sequence-state reduction families, not a universal threshold. |
| signal-before-strong-claim | `KEEP` | No new defect. |
| ordinary-reduction-first | `KEEP` | Fresh object used a prospectively fixed ordinary reduction and stopped cleanly. |
| claim-type separation | `KEEP` | Negative MECHANISM result was not relabeled SYSTEM for rescue. |
| legacy Top-k sparse-support weakness | `TIGHTEN` | Historical local weakness remains; do not generalize a numeric replacement programme-wide. |

## Mandatory Funnel v2.1 findings

1. `claim_ceiling` remains a current-object prospective type. The fresh object was MECHANISM before outcome and remained MECHANISM at closure.
2. No completed SYSTEM object was upgraded in place to MECHANISM.
3. `preformal_eligible` remains meaningfully distinct from readiness: the fresh prospective contract used `preformal_eligible_pre_outcome=true`, while no READY status or prior scientific success was required.
4. `HIDDEN_SECOND_FORMAL_GATE=false`. The first real READY→PRE_FORMAL remains unobserved.
5. HOLD dimensions continue to preserve method/terminal/queue distinctions; no new information-losing primary-enum use was observed.
6. MAIN performed no SYSTEM-over-comparable-MECHANISM execution; `system_priority_exception.used=false`.
7. `NO_COHERENT_MECHANISM_TARGET` remains unused; no evidence it is an escape hatch.
8. The fresh theory-backward object was genuinely mechanism-level and falsifiable rather than a relabeled SYSTEM edge case. It was selected while the rolling floor was already 2/3 and was cleanly reduced without rescue.
9. SYSTEM research value remains preserved. The current 3/3 MECHANISM rolling window is explicitly descriptive, not a quota target, and MAIN remains permitted to prioritize integrity-protecting SYSTEM work prospectively when justified.
10. PRE_FORMAL/PASS remains `REACHABLE_BUT_NARROW`.
11. Funnel policy conclusions are based on `classification_completeness=13/13`; conversion/disposition rates remain descriptive only.
12. First READY→PRE_FORMAL remains `INSUFFICIENT_EVIDENCE`.

## Calibration dimensions

- `gate_drift`: the recent semantic-preflight tightening is evidence-driven by two observable pre-adoption failures; no additional scientific success/novelty gate was added this run.
- `justification_trace`: strong for the semantic-preflight rule, now linked both to the historical defect and a clean post-adoption implementation example.
- `false_positive_control`: currently strong. Exact source/API binding, no-repair rule, fixed reductions, fresh Analyst review and dependency fail-close collectively prevent the known repair/rescue path.
- `false_negative_risk`: acceptable. The preflight checks representation fidelity rather than requiring positive results, and the fresh MECHANISM object could enter with `preformal_eligible=true` before being reduced.
- `duplicate_guards`: no new guard should be added. Producer preflight plus downstream containment have different information value: prevention versus fail-closed containment.
- `moving_goalposts`: `LOW_CURRENT_HISTORICAL_LOCALIZED_CONCERN_RESOLVED_PROSPECTIVELY`. Historical defects stay method-limited; no past object is rewritten; the promised post-adoption test has now been met.
- `pass_reachability`: `REACHABLE_BUT_NARROW`. Semantic preflight is an integrity fidelity requirement, not a success criterion. First READY→PRE_FORMAL is still the most important untested transition.
- `comparator_calibration`: healthy. Current literature suggests stronger Markov/suffix/causal-state/predictive-state comparators only for a **fresh claim that requires them**, with matched information/resource privilege.
- `signal_before_reduction`: healthy. The programme does not require every Discovery question to show a positive effect before it can be tested, but strong promotion claims still require a supported phenomenon.
- `claim_type_separation`: healthy.
- `research_worthiness_vs_novelty`: healthy; SYSTEM value remains preserved and MECHANISM negatives are not laundered into another claim class.
- `external_calibration`: new Literature strengthens ordinary sequence-state reductions but does not justify a universal numeric threshold or a broader novelty gate.
- `opportunity_cost`: further tightening of admission/readiness now has lower expected information gain than watching live v2.1 transitions.

## Mechanism-supply health

**`HEALTHY_SMALL_N_QUALITY_FLOOR_HELD_13_OF_13_COMPLETE`**.

The Analyst-reviewed portfolio is `MECHANISM=7 / SYSTEM=6`. The last three autonomous safe scientific SUB selections are all MECHANISM, but the newest one was selected when the floor was already satisfied at 2/3, so there is no evidence of quota manufacturing. Treat 3/3 as descriptive only; do not turn it into a target or suppress worthwhile SYSTEM work.

## Funnel observability

**`GOOD_V2_1_COMPLETE_13_OF_13_POST_ADOPTION_PREFLIGHT_OBSERVED`**.

All 13 reviewed material candidates have mandatory v2.1 classification fields. The new object’s prospective binding, diagnostic, result, exact-head CI and independent Analyst closure are traceable. MAIN consumed the fresh Analyst generation and remained idle without conflicting reclassification.

## PRE_FORMAL gate calibration

**`ELIGIBILITY_READINESS_SEPARATION_REPLICATED_READY_TRANSITION_UNTESTED`**.

Current authoritative eligible=0 and READY=0. Multiple prospective MECHANISM objects, including the fresh post-adoption object, have occupied an eligibility-in-principle state before outcome without being READY. This is evidence that eligibility is not prior scientific success. No Analyst-authoritative READY object exists, so the first READY→PRE_FORMAL transition remains `INSUFFICIENT_EVIDENCE` and should be audited for development-readiness semantics rather than outcome success.

## Prospective recommendations

1. Keep the current terminal/API semantic-preflight rule and its method-limit containment; do **not** add a stricter scientific admission/novelty/readiness threshold merely because only one post-adoption live example exists.
2. Continue recording exact source/docs/tests bindings for terminal-relevant categorical/public-API semantics and watch for recurrence. Any future outcome-exposed terminal-semantic repair remains method-limited for that object.
3. Keep classification-completeness gating, the one-in-three mechanism floor as a floor only, and intentional MAIN idle behavior when no coherent high-information object exists.
4. Audit the first READY→PRE_FORMAL, first MAIN SYSTEM-priority exception, and first `NO_COHERENT_MECHANISM_TARGET` use as the next high-information methodology events.
5. Apply stronger literature-backed sequence-state comparators only to fresh claims whose information structure makes them relevant; privilege-match them rather than imposing a universal comparator ladder on unrelated objects.

## Utility request

None created. Live rollout remains higher-information than a synthetic methodology probe.

## Hard-integrity-floor confirmation

**CONFIRMED / DO NOT RELAX.** No recommendation weakens no-rerun/no-retune consumed identities, prospective/frozen protocols, raw-before-score, preserve-before-read, exact identity/source/package/runtime/input binding, immutable evidence, evaluator/target leakage controls, or the prohibition on silent post-outcome repair.

## Confidence

**HIGH** in the current `WELL_CALIBRATED` classification for the methodology as presently specified; **HIGH** that the specific R16-R18 producer-preflight defect is now prospectively implemented end-to-end at least once; **MODERATE-HIGH** on long-run operational durability because this is the first post-adoption live case; **INSUFFICIENT_EVIDENCE** for first READY→PRE_FORMAL, first MAIN SYSTEM-priority exception, and first no-coherent-target use.

## Authoritative/current refs inspected

- stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- previous Methodology `METHCAL-20260920T182012+0900-R18-6B2F9C41@820bb63ca6a0ad117d9e2f6ff971bb692d7efcf1`
- Control `CTRL-20260920T165000+0900-R15-6C2F8A41@64611f391391844d60659732a50a22cf009a5797`
- Evidence Analyst `EVA-20260920T190536+0900-R18-AC1DB49E@fec9320a8e8c868f4df91dafb1af75c640ae995a`
- MAIN `MAIN-20260920T191546+0900-PRIMARY-FUNNEL21-HOLD-R18-8C2F41D7`; final run-report branch tip `9d2bb49356d4ad3c009ce7a049f3a2285035a5e4`
- SUB `SUB-20260920T184410+0900-THEORY-CONTEXTPRED-7A4C2E91@8a90af450ff3f76ae4b45ed120f476d62fbc3df8`
- research `research/exploratory-sub-context-conditioned-prediction-20260920@f0a4157d869561e4201aca1c37663305bc5c8a5d`; prospective binding `01d4cc8daf07be67b8f633434030241276a0a4b0`; diagnostic `38c6f3cc972898c170fdf5853190ca33de8f6882`; exact-head CI `35502970668` success attempt 1
- Literature `LIT-20260920T184200+0900-R13-CONTEXT-PREDICTIVE-3B7D91E4@4a1dfcaef0dfcdbf132156f7656088f7f90a3c96`
- Independent Audit `LEGACY_GENERATION_UNKNOWN@d3a9c8d4c4cf8a3e5a0152d7b0749633776ecb56`
- Repository Steward `LEGACY_GENERATION_UNKNOWN@e53df976b98d56b8e37a5cbfc20f1aeb84caadeb` (stale)
- Utility request bus `d4d0f75f1a57df1298e49e67448158ab12a2754f`
- authoritative `evidence/*`: 5; `formal/*`: 0; `sealed/*`: 0; tag-based `freeze/*`: 0
- H5 STARTED `058e90227cd48e1c10c6ecbaed01efdec1217d0e`; raw preserve `ce5797eb584344db7a512e585506fb6c59ea475b`
- PR #148 and #149 open/unmerged
