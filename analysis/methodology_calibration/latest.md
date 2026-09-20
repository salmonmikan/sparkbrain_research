# SparkBrain Methodology Calibration Audit — 2026-09-20 16:20 JST

schema_version: `2`  
generation_id: `METHCAL-20260920T162049+0900-R16-E7C19A42`  
produced_at: `2026-09-20T16:20:49+09:00`  
producer_run_id: `methodology-calibration-auto-20260920T162049+0900-R16-E7C19A42`  
authority_scope: `METHODOLOGY_ADVISORY_ONLY`  
supersedes_generation_id: `METHCAL-20260920T152243+0900-R15-91C4E7B2`

## Run disposition

**`MATERIAL_CALIBRATION_UPDATE`**

## Overall classification

**`SLIGHTLY_TOO_PERMISSIVE`** — changed from `WELL_CALIBRATED`.

The Funnel-v2.1 allocation, candidate-supply, claim-typing, HOLD observability and eligibility/readiness rules continue to behave well. The material new calibration defect is narrower: a terminal-relevant representation mismatch in the fresh endogenous-continuation MECHANISM Discovery was discovered only after the first outcome-bearing diagnostic ran; the harness was then changed from expecting `action=None` to accepting the stable API's literal `action="withhold"`, rerun, and the corrected run was used to close the same prospective object as a negative terminal. The correction was transparent, NON_EVIDENTIARY, source-consistent and did not change seed/timing/input/metric/threshold/state, so this is not evidence of broad post-hoc rescue. It is nevertheless an outcome-exposed modification of an operationalized terminal predicate and therefore exposes a real prospective-freeze boundary that is currently too permissive.

Prospectively, the programme should distinguish a scientifically equivalent representation repair from a **prospectively clean terminal test**. After outcome exposure, a terminal-relevant harness repair may be useful engineering/debugging information, but the corrected rerun should not by itself receive clean prospective closure/promotion/readiness credit for that same object. If the distinction can affect allocation or scientific disposition, a fresh prospectively bound object/probe is the clean route.

## Strongest new calibration evidence

### 1. The fresh MECHANISM object was genuinely prospective — until a terminal representation mismatch was exposed

Fresh SUB generation `SUB-20260920T155600+0900-THEORY-ENDOCONT-4C7A2E91` created `CAND-V05-ENDOGENOUS-CONTINUATION-01` from stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. Prospective binding `edd8dc67f1b1ab22fc8b2914cab774c1aadf49de` fixed `claim_ceiling=MECHANISM`, `preformal_eligible=true` in principle, readiness `NOT_READY`, seed/config/training count, the driven probe, immediate empty-input probe, a conditional queue-clear reduction, observables, three terminal paths, falsifier and a one-cycle stop.

The literal first terminal required the empty step to have zero lower-field spikes, zero internal patterns, no mature Assembly activation, no prediction **and no action**. The first diagnostic commit `8df025745b803fbfac326072b0283719b59ec082` operationalized that as an exact expectation `"action": None` and CI run `35494974118` failed after the diagnostic had executed.

Stable main already specified before the run that `AssemblyActionPolicy.choose()` returns `ActionDecision(None, "withhold", 1.0)` for null/suppressed/immature activation. Correction commit `d039f0012b0cbe3826146ed76ae6b791b4abe848`, made after the failed outcome-bearing run, changed the assertion from `None` to `"withhold"` and added queue assertions. Corrected CI `35495129863` succeeded; final exact-head CI `35495326487` also succeeded at research head `af201c25d3a5e7f1fde15b07b82aa0aad77cbd3f`.

The final report and Evidence Analyst correctly explain that `withhold` with `assembly_id=null` is the implementation's null-activation representation, not causal endogenous continuation. Scientifically that interpretation is plausible and source-grounded. Methodologically, however, the representation mapping was not bound before the first outcome-bearing execution even though the stable source made it knowable. This is precisely the type of avoidable post-outcome normalization that a prospective protocol should catch in preflight.

### 2. The repair did not become positive-result rescue or a new novelty claim

The corrected object remained `NON_EVIDENTIARY`, `MECHANISM`, and was closed `REJECT`; no SYSTEM rescue, cycle 2, PRE_FORMAL, FORMAL, consumed identity, official scorer, immutable-evidence mutation or research merge occurred. The driven step was functional, while the immediate empty step had zero spikes/patterns/mature Assembly/prediction and an already-empty field queue. Evidence Analyst normalized the raw suffix-bearing terminal to the prospectively intended scientific meaning and explicitly bounded the result to one fixed default supported configuration/seed/timing. Any broader endogenous-continuation question requires a fresh candidate.

This limits the seriousness of the defect: it is **localized protocol permissiveness**, not evidence of programme-wide moving goalposts or novelty inflation.

### 3. Funnel v2.1 otherwise remains healthy and more observable

Evidence Analyst generation `EVA-20260920T160240+0900-R16-3D7A91C4@eea87c0e67807605c8fdd10408650da4192fb06b` now classifies all `11/11` material candidates with mandatory v2.1 fields. Portfolio is MECHANISM=5 / SYSTEM=6; PRE_FORMAL eligible=0; READY=0. Rolling autonomous SUB selection is delayed reward=`MECHANISM`, evaluation order=`SYSTEM`, endogenous continuation=`MECHANISM` = `2/3` theory-backward. No `NO_COHERENT_MECHANISM_TARGET` exception was used and no preferred mechanism ratio was inferred.

The new endogenous-continuation object is a genuine mechanism-level, falsifiable theory-backward selection and was chosen when the rolling floor was already satisfied at `2/3`; it was not a relabeled SYSTEM edge case. Current MAIN generation `MAIN-20260920T161602+0900-PRIMARY-FUNNEL21-HOLD-6D2B8C41` consumed fresh Analyst R16 and remained scientifically idle with `system_priority_exception.used=false`, because no comparable executable MECHANISM or independently high-value integrity-protecting SYSTEM object was allocated.

## Funnel v2.1 gate audit

| Gate / behavior | Classification | Calibration finding |
| --- | --- | --- |
| hard one-way scientific integrity floor | `KEEP` | Do not relax. The new defect argues for better preflight, not weaker prospective integrity. |
| prospective terminal semantic binding | `TIGHTEN` | Terminal-relevant API semantics must be bound before first outcome-bearing execution. |
| terminal-relevant public-API/source conformance preflight | `TIGHTEN` | Stable source already defined null activation as literal `withhold`; preflight should have caught the mismatch. |
| post-outcome representation repair policy | `TIGHTEN` | Transparent repair may remain engineering/debugging information, but corrected rerun should not automatically count as prospectively clean closure/promotion/readiness for the same object. |
| current-object `claim_ceiling` | `KEEP` | Fresh object was MECHANISM before outcome; no post-outcome type upgrade. |
| same-object SYSTEM→MECHANISM upgrade ban | `KEEP` | No violation observed. |
| fresh SYSTEM→MECHANISM successor semantics | `KEEP` | Stronger/new questions still require fresh objects. |
| `preformal_eligible` distinct from readiness | `KEEP` | Fresh object again began `eligible=true / NOT_READY`; eligibility was closed only after its terminal disposition. |
| PRE_FORMAL `READY` semantics | `KEEP` | No hidden second Formal gate observed; first READY transition still untested. |
| first Analyst-authoritative `READY -> PRE_FORMAL` transition | `INSUFFICIENT_EVIDENCE` | No READY candidate exists. |
| HOLD multidimensional model | `KEEP` | New REJECT uses null hold plus terminal/not-queued state; 11/11 fields complete. |
| MAIN MECHANISM priority | `KEEP` | MAIN remains idle rather than manufacturing low-value work. |
| prospective `system_priority_exception` | `KEEP` | Rule remains sound; first actual use remains untested. |
| first `system_priority_exception` use | `INSUFFICIENT_EVIDENCE` | No live use. |
| rolling one-in-three theory-backward supply | `KEEP` | New mechanism selection was not quota-forced; rolling share remains 2/3. |
| theory-backward quality floor | `KEEP` | New object had a real mechanism discriminator and falsifier. |
| `NO_COHERENT_MECHANISM_TARGET` rule | `KEEP` | No use yet; first use remains untested. |
| first `NO_COHERENT_MECHANISM_TARGET` use | `INSUFFICIENT_EVIDENCE` | No live use. |
| SYSTEM value under MECHANISM priority | `KEEP` | Prior high-information SYSTEM work remains retained; no evidence of starvation. |
| classification-completeness-gated metrics | `KEEP` | `11/11`; counts remain descriptive small-N statistics. |
| universal numeric readiness/support threshold prohibition | `KEEP` | No evidence supports one. |
| equal-privilege / claim-matched comparator discipline | `KEEP` | Conditional queue-clear reduction was fixed prospectively and was not opportunistically invoked when continuation was absent. |
| signal-before-strong-claim | `KEEP` | No strong mechanism claim was promoted from the negative Discovery. |
| ordinary-reduction-first interpretation | `KEEP` | Negative is object-local; broader timing/config/self-trigger questions require fresh objects. |
| claim-type separation / research worthiness vs novelty | `KEEP` | MECHANISM negative was not rescued into SYSTEM; independent SYSTEM value remains preserved. |
| legacy Top-k sparse-support weakness | `TIGHTEN` | Historical local weakness remains; do not generalize its numeric threshold. |
| programme-wide numeric support/readiness threshold | `KEEP` | Continue prohibiting one. |

## Mandatory v2.1 findings

1. **Claim ceiling gaming:** not observed. Endogenous continuation was prospectively MECHANISM and remained the same claim type after outcome.
2. **Same-object SYSTEM→MECHANISM upgrade:** not observed.
3. **Eligibility vs READY duplication:** not observed; this fresh object again occupied `preformal_eligible=true / NOT_READY` before outcome.
4. **Hidden second Formal gate:** `false`; no READY transition exists yet.
5. **HOLD observability:** healthy at `11/11` classification completeness.
6. **SYSTEM priority exception:** not triggered; first actual MAIN use remains untested.
7. **NO_COHERENT_MECHANISM_TARGET:** no use; first-use calibration remains untested.
8. **Theory-backward authenticity:** healthy. The new object was a genuine mechanism discriminator, not a relabeled API edge case.
9. **SYSTEM value under MECHANISM priority:** still healthy; previous SYSTEM reproducibility/testbed work remains legitimate.
10. **PRE_FORMAL/PASS reachability:** `REACHABLE_BUT_NARROW`; eligibility-without-readiness is repeatedly demonstrated, READY→PRE_FORMAL remains unobserved.
11. **Metric policy:** classification completeness is `11/11`; conversion rates remain descriptive only.
12. **First READY→PRE_FORMAL:** still `INSUFFICIENT_EVIDENCE`.

## General calibration

- `gate_drift`: no new Control doctrine or scientific threshold. A **live object-level reinterpretation** occurred: literal `no action` was normalized after outcome exposure to semantic `no causal Assembly action / default withhold only`. It is evidence-driven by stable source but occurred too late to count as clean prospective binding.
- `justification_trace`: strong for tightening terminal-semantic preflight. The stable source made the output convention knowable before the first diagnostic; the initial failure and subsequent assertion change provide direct traceable evidence.
- `false_positive_control`: generally strong, but accepting corrected same-object reruns as prospectively clean could enable future outcome-responsive rescue if left unconstrained.
- `false_negative_risk`: also relevant. A method-repaired negative should not automatically close a potentially valuable mechanism object as though the terminal had been cleanly preregistered. Fresh prospective confirmation is preferable when disposition matters.
- `duplicate_guards`: no new redundant guard is needed; strengthen the existing prospective-binding layer rather than adding another scientific novelty threshold.
- `moving_goalposts`: **`LOCALIZED_MODERATE_CONCERN`**. No programme-wide threshold drift or positive-result rescue occurred, but one terminal-relevant representation predicate was changed after outcome exposure.
- `pass_reachability`: **`REACHABLE_BUT_NARROW`**. No READY candidate yet.
- `comparator_calibration`: appropriate and claim-local.
- `claim_type_separation`: healthy.
- `research_worthiness_vs_novelty`: healthy.
- `external_calibration`: fresh Literature emphasizes explicit model/event semantics and supports making semantic conventions explicit prospectively; it does not justify any universal scientific threshold.
- `opportunity_cost`: keep scientific gates unchanged; the highest-value correction is cheap preflight/repair-status discipline, not more restrictive admission or novelty criteria.

## Mechanism-supply health

**`HEALTHY_BALANCED_SMALL_N_WITH_METHOD_REPAIR_CAUTION`**.

The rolling autonomous window is `MECHANISM,SYSTEM,MECHANISM = 2/3`; the newest MECHANISM choice was made while the floor was already satisfied and had a genuine falsifier. No exception was used and no preferred ratio should be inferred. The only new concern is methodological cleanliness of the terminal test, not candidate-supply quality.

## Funnel observability

**`GOOD_V2_1_IMPLEMENTATION_11_OF_11_WITH_REPAIR_LINEAGE_VISIBLE`**.

All 11 material candidates have v2.1 fields. The endogenous object exposes its prospective binding, initial failed diagnostic, harness correction, final head and terminal normalization, so the repair is not silent. That transparency is a strength; the remaining defect is that the corrected same-object run was still treated as clean enough for terminal scientific disposition.

## PRE_FORMAL gate calibration

**`ELIGIBILITY_READINESS_SEPARATION_REPLICATED_READY_TRANSITION_UNTESTED`**.

The endogenous object prospectively had `preformal_eligible=true / NOT_READY`, again demonstrating that eligibility is not prior success. No READY candidate exists. `HIDDEN_SECOND_FORMAL_GATE=false`. The first Analyst-authoritative READY→PRE_FORMAL remains the highest-information unresolved Funnel-v2.1 event.

## Prospective recommendations

1. **Tighten preflight, not the science bar.** Before first outcome-bearing execution, bind terminal-relevant categorical/public-API outputs to semantic predicates verified against exact source/docs/tests. A literal value may be used only when its representation is itself part of the claim.
2. After outcome exposure, if a terminal-relevant harness predicate is repaired, persist `outcome_exposed=true`, mismatch/repair class, and whether the semantic predicate changed. A corrected rerun may inform engineering/debugging, but should not automatically receive prospectively clean closure, promotion or readiness credit for the same object.
3. If such a repaired result would materially determine scientific disposition or next-layer allocation, use a fresh candidate/probe with the corrected semantic contract. Apply this **prospectively only**; do not rewrite or rescore the current endogenous-continuation history.
4. Keep Funnel v2.1 allocation, claim-ceiling, eligibility/readiness, HOLD, mechanism-supply and numeric-threshold rules otherwise unchanged.
5. Continue auditing the first actual MAIN `system_priority_exception`, first `NO_COHERENT_MECHANISM_TARGET`, and first Analyst-authoritative `READY -> PRE_FORMAL` transition.

## Utility request

None created. The live endogenous-continuation repair already provides the relevant calibration evidence; a synthetic Utility probe would add less information than applying the clarified boundary prospectively.

## Hard-integrity-floor confirmation

**CONFIRMED / DO NOT RELAX.** The recommendation strengthens prospective protocol fidelity while retaining the scientific purpose of no rerun/retune consumed identities, frozen/prospective protocols, raw-before-score, preserve-before-read, exact identity/source/package/runtime/input binding, immutable evidence, leakage control and no silent post-outcome repair.

## Confidence

**HIGH** that the representation mismatch was outcome-exposed and avoidable by preflight; **HIGH** that current Funnel-v2.1 typing/supply/observability otherwise remains healthy; **MODERATE** on how restrictive future same-object repair handling should be for purely NON_EVIDENTIARY Discovery; **INSUFFICIENT_EVIDENCE** for READY→PRE_FORMAL, first MAIN SYSTEM-priority exception and first no-coherent-target use.

## Authoritative/current refs inspected

- `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- Evidence Analyst `EVA-20260920T160240+0900-R16-3D7A91C4@eea87c0e67807605c8fdd10408650da4192fb06b`
- Control Brain `CTRL-20260920T145000+0900-R14-7B3E2D91@14285844f80fa844b5aaac9ccf4d2fed95b6fb35`
- MAIN `MAIN-20260920T161602+0900-PRIMARY-FUNNEL21-HOLD-6D2B8C41@12626287db4e75abb029f7dc5b1a875e756ae450`
- SUB `SUB-20260920T155600+0900-THEORY-ENDOCONT-4C7A2E91@46ef5643dc1f9f53790f83de504c3a85e6efbc1c`
- endogenous research: binding `edd8dc67f1b1ab22fc8b2914cab774c1aadf49de`; initial diagnostic `8df025745b803fbfac326072b0283719b59ec082`; correction `d039f0012b0cbe3826146ed76ae6b791b4abe848`; head `af201c25d3a5e7f1fde15b07b82aa0aad77cbd3f`
- CI `35494974118=failure`, `35495129863=success`, final `35495326487=success`
- Literature `LIT-20260920T153056+0900-R12-RECEPTOR-TIES-4D8C2A71@a66abf755d859da60bbc98f61950053f66a6d9c1`
- Independent Audit `LEGACY_GENERATION_UNKNOWN@d3a9c8d4c4cf8a3e5a0152d7b0749633776ecb56`
- Repository Steward `LEGACY_GENERATION_UNKNOWN@e53df976b98d56b8e37a5cbfc20f1aeb84caadeb`
- Utility bus `d4d0f75f1a57df1298e49e67448158ab12a2754f`
- authoritative `evidence/*`: 5; `formal/*`: 0; `sealed/*`: 0; tag-based `freeze/*`: 0
- H5 STARTED `058e90227cd48e1c10c6ecbaed01efdec1217d0e`; raw preserve `ce5797eb584344db7a512e585506fb6c59ea475b`
- PR #148 and #149 independently re-fetched open/unmerged
