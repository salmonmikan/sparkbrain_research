# SparkBrain Methodology Calibration Audit — 2026-09-20 17:27 JST

schema_version: `2`  
generation_id: `METHCAL-20260920T172730+0900-R17-A3D8F6C1`  
produced_at: `2026-09-20T17:27:30+09:00`  
producer_run_id: `methodology-calibration-auto-20260920T172730+0900-R17-A3D8F6C1`  
authority_scope: `METHODOLOGY_ADVISORY_ONLY`  
supersedes_generation_id: `METHCAL-20260920T162049+0900-R16-E7C19A42`

## Run disposition

**`MATERIAL_CALIBRATION_UPDATE`**

## Overall classification

**`SLIGHTLY_TOO_PERMISSIVE`** — unchanged from R16.

The new evidence strengthens, rather than resolves, the narrow R16 defect: a second independent theory-backward MECHANISM Discovery reached an outcome-bearing path before a terminal-relevant public-API accessor mismatch was discovered, then repaired the same object from `PredictionDecision.next_event` to the stable API's `PredictionDecision.value`. This confirms that terminal/API semantic preflight was not a one-off weakness.

Crucially, this fresh SUB object was created and executed **before** Control Brain adopted the R16 tightening at 16:50 JST. It therefore does **not** show that the new prospective rule failed. Instead, the downstream response is now well calibrated: Control refused clean same-object ratification, recommended `HOLD_METHOD_LIMITED` pending fresh Analyst review, prohibited rerun/rescue/promotion, and MAIN later fail-closed because the authoritative Analyst generation predates the new SUB generation.

The remaining calibration gap is therefore producer-side prevention: the programme has adopted the correct prospective boundary, but has not yet demonstrated it on a fresh object that starts after adoption.

## Strongest new calibration evidence

### 1. The same preflight failure class independently recurred

Fresh SUB generation `SUB-20260920T164759+0900-THEORY-PRESEM-5A8C2D71` created `CAND-V05-PRESEMANTIC-FUNCTION-TRANSFER-01` on `research/exploratory-sub-presemantic-function-transfer-20260920`.

Prospective binding `e4f30b4655d483ac0d64c28798122abd7b241b02` fixed a genuine mechanism-level question, `claim_ceiling=MECHANISM`, pre-outcome eligibility in principle, A/B/C patterns, direct-nearest-neighbor and presemantic-prototype+label-lookup reductions, terminal map, falsifier and first-terminal stop.

The first diagnostic commit `1875dfac036512f771c5ffad304595d89bff42a8` failed lint before outcome-bearing tests. After a module-layout correction, commit `fe1459d5b58d20a8efed150e7c102759def83927` reached the actual prediction path and failed in pytest because `PredictionDecision` had no `next_event` attribute. Only after that outcome exposure did correction `ee2a2e9f188b6f709073353342bab32cb7da4e06` change the terminal-relevant accessor from `.next_event` to `.value`. Final research head `c68da076d846d85ad556f875d632ab6f68d68453` then passed exact-head CI `35497715398`.

This is materially the same methodology class as the prior endogenous-continuation `None -> withhold` correction: exact stable API semantics were knowable before the first outcome-bearing execution, but terminal-relevant operationalization was corrected only after the execution exposed the mismatch.

### 2. The new Control rule did not exist when that SUB probe ran

Control generation `CTRL-20260920T165000+0900-R15-6C2F8A41` was produced after the SUB generation and after its research commits. Control explicitly adopted `PROSPECTIVE_TERMINAL_API_SEMANTIC_PREFLIGHT_TIGHTENED`:

- bind terminal-relevant categorical/public-API semantics against exact source/docs/tests before outcome-bearing execution;
- persist repair lineage and outcome exposure;
- repaired same-object reruns may remain engineering/debugging information but do not automatically gain clean closure/promotion/readiness;
- when scientific disposition depends on the repaired predicate, require a fresh prospectively bound object/probe.

Because the second defect predates adoption, current evidence justifies **maintaining** `TIGHTEN`, not claiming the prospective correction has already failed.

### 3. Downstream false-positive containment now works correctly

Control did not ratify SUB's proposed clean `REJECT`. Its preferred prospective classification, if Evidence Analyst independently confirms the defect, is `MECHANISM`, `preformal_eligible=false`, `NOT_READY`, `HOLD_METHOD_LIMITED`, `TERMINAL_FOR_CURRENT_OBJECT`, `NOT_QUEUED`, with reason `OUTCOME_EXPOSED_TERMINAL_REPRESENTATION_REPAIR_AFTER_API_CONFORMANCE_MISS`. No same-object rerun, rescue, SYSTEM relabel or PRE_FORMAL promotion is permitted.

MAIN generation `MAIN-20260920T171704+0900-PRIMARY-FUNNEL21-FAILCLOSED-91E6C4A2` then observed that SUB was newer than authoritative Analyst R16 and blocked with `FAIL_CLOSED_ANALYST_DEPENDENCY_ADVANCED_UNREVIEWED_SUB_GENERATION`. It did not import SUB's proposed disposition or recompute canonical funnel metrics. This is strong evidence that freshness-dependent control-plane observability and authority separation are well calibrated.

## Funnel v2.1 audit

| Gate / behavior | Classification | Finding |
| --- | --- | --- |
| hard one-way integrity floor | `KEEP` | Do not relax. |
| prospective terminal semantic binding | `TIGHTEN` | Repeated pre-adoption failures make the justification trace stronger. |
| producer-side terminal API/source conformance preflight | `TIGHTEN` | Correct rule now exists; post-adoption effectiveness remains unvalidated. |
| Control outcome-exposed repair containment | `KEEP` | Fresh Control response correctly withholds clean closure/promotion/readiness. |
| repaired same-object clean closure/promotion ban | `KEEP` | Correct prospective boundary. |
| repair lineage / `outcome_exposed` observability | `KEEP` | Both defects are reconstructable and not silent. |
| freshness/dependency fail-closed reconciliation | `KEEP` | MAIN excludes the unreviewed newer SUB object from canonical metrics. |
| current-object `claim_ceiling` | `KEEP` | Fresh object was prospectively MECHANISM, not a prestige relabel. |
| same-object SYSTEM→MECHANISM upgrade ban | `KEEP` | No violation. |
| fresh successor semantics | `KEEP` | Clean confirmation, if valuable, must be a fresh object. |
| `preformal_eligible` distinct from READY | `KEEP` | Existing prospective `true / NOT_READY` examples remain valid. |
| READY semantics | `KEEP` | No hidden second Formal gate observed. |
| first Analyst-authoritative READY→PRE_FORMAL | `INSUFFICIENT_EVIDENCE` | Still unobserved. |
| multidimensional HOLD | `KEEP` | `HOLD_METHOD_LIMITED` is appropriate for the pending method defect. |
| MAIN MECHANISM priority | `KEEP` | MAIN blocks rather than manufacturing work. |
| prospective SYSTEM-priority exception | `KEEP` | First live use still unobserved. |
| first SYSTEM-priority exception use | `INSUFFICIENT_EVIDENCE` | No live use. |
| rolling 1-in-3 theory-backward supply | `KEEP` | Pending rolling window is SYSTEM, MECHANISM, MECHANISM = 2/3. |
| theory-backward quality floor | `KEEP` | The new question is genuinely mechanism-level and falsifiable. |
| `NO_COHERENT_MECHANISM_TARGET` rule | `KEEP` | No use; no escape-hatch evidence. |
| first `NO_COHERENT_MECHANISM_TARGET` use | `INSUFFICIENT_EVIDENCE` | Unobserved. |
| SYSTEM value under MECHANISM priority | `KEEP` | No new starvation signal. |
| classification-completeness gating | `KEEP` | Canonical metrics remain Analyst R16 11/11; pending SUB is excluded until review. |
| universal numeric readiness/support thresholds | `KEEP` | Continue prohibiting them. |
| equal-privilege comparator | `KEEP` | No new calibration defect. |
| ordinary-reduction-first | `KEEP` | No scientific bar change warranted. |
| claim-type separation | `KEEP` | Method failure is not converted into SYSTEM or novelty credit. |
| legacy Top-k sparse-support weakness | `TIGHTEN` | Historical local weakness remains; do not generalize a number programme-wide. |

## Mandatory v2.1 findings

1. `claim_ceiling` remains current-object prospective typing; no permanent topic/prestige use observed.
2. No completed SYSTEM object is being upgraded in place to MECHANISM.
3. `preformal_eligible` and READY remain nonduplicate.
4. `HIDDEN_SECOND_FORMAL_GATE=false`; first READY→PRE_FORMAL remains unobserved.
5. HOLD dimensions are informative; method limitation can be represented without pretending the scientific hypothesis itself was cleanly rejected.
6. No MAIN SYSTEM-over-comparable-MECHANISM execution occurred; `system_priority_exception.used=false`.
7. `NO_COHERENT_MECHANISM_TARGET` remains unused.
8. The fresh theory-backward selection is genuinely mechanism-level; the defect is methodological, not label gaming.
9. SYSTEM architecture/testbed/reproducibility value remains preserved.
10. PRE_FORMAL/PASS remains `REACHABLE_BUT_NARROW`.
11. Policy conclusions remain gated by reviewed `classification_completeness`; pending newer SUB is not silently added to conversion statistics.
12. First READY→PRE_FORMAL remains `INSUFFICIENT_EVIDENCE`.

## General calibration

- `gate_drift`: a real prospective Control tightening was introduced after R16; no success/novelty/reduction threshold changed.
- `justification_trace`: now **stronger**. Two independent outcome-exposed terminal/API representation mismatches support the same preflight tightening.
- `false_positive_control`: downstream containment is strong; upstream residual risk remains until post-adoption preflight is demonstrated.
- `false_negative_risk`: do not convert a method-limited object into a scientific negative merely because a repaired diagnostic is convenient. A fresh object is appropriate only if the question remains worth the cost.
- `duplicate_guards`: do not add another scientific gate. Enforce the existing prospective semantic-binding guard at the producer.
- `moving_goalposts`: `LOCALIZED_MODERATE_CONCERN_CONTAINED_PROSPECTIVELY`. Historical defects are visible and not rewritten; Control now explicitly prevents repaired same-object results from acquiring clean promotion/readiness credit.
- `pass_reachability`: `REACHABLE_BUT_NARROW`; preflight tightening is methodological fidelity, not an extra success criterion.
- `comparator_calibration`: no new defect.
- `claim_type_separation`: healthy.
- `research_worthiness_vs_novelty`: healthy.
- `external_calibration`: no new Literature/Audit generation since R16 that changes thresholds. Literature continues to support explicit semantics; Independent Audit remains narrow H5 `ROBUST_SO_FAR`.
- `opportunity_cost`: do not add universal thresholds or broader gate strictness. The highest-information next calibration event is a fresh **post-adoption** object that exercises the tightened preflight.

## Mechanism-supply health

**`HEALTHY_SMALL_N_QUALITY_FLOOR_HELD_PENDING_METHOD_LIMIT_CLASSIFICATION`**.

The Analyst-authoritative reviewed pool remains 11/11 complete, MECHANISM=5 / SYSTEM=6. The fresh pending SUB is a coherent theory-backward MECHANISM object and the observed rolling window is `SYSTEM,MECHANISM,MECHANISM` = 2/3, with no no-coherent-target exception. It must not be canonicalized until fresh Analyst review.

## Funnel observability

**`GOOD_AND_FAIL_CLOSED_11_OF_11_REVIEWED_PLUS_1_PENDING`**.

The canonical reviewed population stays 11/11 complete. The newer SUB object is explicitly pending rather than silently entering metrics. MAIN blocks on the stale Analyst dependency and preserves the authority boundary. This is a positive v2.1 observability result.

## PRE_FORMAL gate calibration

**`ELIGIBILITY_READINESS_SEPARATION_REPLICATED_READY_TRANSITION_UNTESTED`**.

Canonical eligible=0 and READY=0. Earlier prospective objects demonstrate `preformal_eligible=true / NOT_READY`, so eligibility does not require prior success. The first real READY→PRE_FORMAL remains the highest-information unresolved calibration event. `HIDDEN_SECOND_FORMAL_GATE=false`.

## Prospective recommendations

1. **Keep the R16/R17 preflight tightening; do not tighten the scientific bar.** Require exact source/docs/tests conformance for terminal-relevant API/categorical semantics before the first outcome-bearing execution.
2. Treat the new presemantic function-transfer object as a calibration example of a **pre-adoption** producer-side defect, not as evidence that the new Control rule failed.
3. Preserve the current Control containment: outcome-exposed repaired same-object runs may inform debugging but must not automatically receive clean scientific closure, promotion, or readiness. If scientifically worth confirming, spawn a fresh prospectively bound object.
4. Keep MAIN's dependency-aware fail-closed behavior and classification-completeness gating.
5. Audit the first fresh object started after the 16:50 Control adoption to see whether terminal/API semantic preflight actually prevents recurrence.
6. Continue watching the first READY→PRE_FORMAL, first live SYSTEM-priority exception, and first `NO_COHERENT_MECHANISM_TARGET` use.

## Utility request

None created. Live post-adoption rollout is a higher-information test of methodology calibration than a synthetic Utility probe.

## Hard-integrity-floor confirmation

**CONFIRMED / DO NOT RELAX.** No recommendation weakens one-way identities, frozen/prospective protocols, raw-before-score, preserve-before-read, exact bindings, immutable evidence, leakage controls, or the ban on silent post-outcome repair.

## Confidence

**HIGH** that the preflight defect has repeated independently; **HIGH** that the second occurrence predates Control's prospective tightening; **HIGH** that Control and MAIN now contain the downstream false-positive risk correctly; **MODERATE** until producer-side prevention is observed on a fresh post-adoption object; **INSUFFICIENT_EVIDENCE** for READY→PRE_FORMAL, first MAIN SYSTEM-priority exception, and first no-coherent-target use.

## Authoritative/current refs inspected

- `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- prior Methodology `METHCAL-20260920T162049+0900-R16-E7C19A42@1d4ab30c2a268fb612462b60bb498b15cc017643`
- Control `CTRL-20260920T165000+0900-R15-6C2F8A41@64611f391391844d60659732a50a22cf009a5797`
- Evidence Analyst `EVA-20260920T160240+0900-R16-3D7A91C4@eea87c0e67807605c8fdd10408650da4192fb06b`
- MAIN `MAIN-20260920T171704+0900-PRIMARY-FUNNEL21-FAILCLOSED-91E6C4A2@1fdfe192a25c656a02b5841745654d4025fb9882`
- SUB `SUB-20260920T164759+0900-THEORY-PRESEM-5A8C2D71@77f5549edb508a3c65cd7ef9378e8c03ea56f282`
- SUB research: binding `e4f30b4655d483ac0d64c28798122abd7b241b02`; first outcome-bearing accessor failure head `fe1459d5b58d20a8efed150e7c102759def83927`; repair `ee2a2e9f188b6f709073353342bab32cb7da4e06`; final head `c68da076d846d85ad556f875d632ab6f68d68453`; final CI `35497715398=success`
- Literature `LIT-20260920T153056+0900-R12-RECEPTOR-TIES-4D8C2A71@a66abf755d859da60bbc98f61950053f66a6d9c1`
- Independent Audit `LEGACY_GENERATION_UNKNOWN@d3a9c8d4c4cf8a3e5a0152d7b0749633776ecb56`
- Repository Steward `LEGACY_GENERATION_UNKNOWN@e53df976b98d56b8e37a5cbfc20f1aeb84caadeb` (stale)
- authoritative `evidence/*`: 5; `formal/*`: 0; `sealed/*`: 0; tag-based `freeze/*`: 0
- H5 STARTED `058e90227cd48e1c10c6ecbaed01efdec1217d0e`; raw preserve `ce5797eb584344db7a512e585506fb6c59ea475b`
- PR #148 and #149 open/unmerged
