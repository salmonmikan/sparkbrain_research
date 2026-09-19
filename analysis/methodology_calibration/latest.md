# SparkBrain Methodology Calibration Audit — 2026-09-19 17:20 JST

## Overall classification

**`SLIGHTLY_OVERCONSERVATIVE`**

This is a material improvement from the prior `MIXED_CALIBRATION` result. The key uncertainty from the 16:21 audit — whether the new `DISCOVERY -> ARCHITECTURE_STUDY / PRE_FORMAL -> FORMAL` funnel would actually change behaviour — now has positive operational evidence.

SUB used the Discovery fallback to select a bounded synthetic question rather than repeat a blanket no-op. The raw top-k churn phenomenon was then **reduced cleanly to ordinary hyperplane geometry**, yet Evidence Analyst did **not** misuse that reduction to declare the whole research question worthless. Instead, it preserved the reduction, separated claim type, and promoted only a distinct architecture/system question: whether hard routing-set swaps interact with persistent recurrent state to create delayed amplification. MAIN has already created a fixed DEV-only architecture-study harness on a new research branch. No formal identity, STARTED, TEST access, or consumed evidence was reused.

So the largest overconservative defect identified in the previous audit is already being corrected in practice. The methodology is not yet `WELL_CALIBRATED` because (a) Control Brain's latest durable handoff still reflects the older programme-wide HOLD/no-op interpretation and predates this correction, and (b) the first MAIN architecture cycle has not produced a valid result yet — its first CI run failed at lint before tests. Formal integrity itself remains appropriately strict.

## Material change since the prior audit

1. **The anti-stall correction is now empirically demonstrated in durable handoff/repository state.** SUB performed one bounded `DISCOVERY` cycle on top-k router margin/churn using synthetic-only data and explicitly labeled it `NON_EVIDENTIARY`.
2. **Reduction no longer automatically kills research-worthiness.** The Discovery result found the raw churn event exactly reducible to ordinary top-k geometry, but Evidence Analyst classified the remaining architecture question as `PROMOTE_TO_ARCHITECTURE_STUDY` instead of rejecting it under the new-computational-principle bar.
3. **Claim-type separation is active, not merely aspirational.** Evidence Analyst explicitly states that the promoted object is an architecture/system-integration question, not a novelty claim, and binds one DEV-only cycle with fixed data, perturbations, metrics, controls, thresholds, and stop conditions.
4. **MAIN has begun implementing the promoted lower-layer object prospectively.** Branch `research/main-topk-persistent-amplification-arch-study-20260919` now contains a fixed harness at `08c284e14d36e22d8b7b357b6f76b385daef40bd`. The first CI run failed at lint before test/execution, so there is no new architecture result yet and no outcome-responsive redesign opportunity has arisen.
5. **Formal doctrine is unchanged.** `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; consumed evidence remains immutable; C19-R2's FSA terminal evidence still points to `6197fa801a78a0c5de4c2b6ff5d03216ac5539db`.

## Gate calibration

| Gate / rule | Classification | Current finding |
| --- | --- | --- |
| No rerun/retune/rescore; immutable evidence; raw-before-score / preserve-before-read | `KEEP` | Hard integrity floor remains justified and untouched. |
| Prospective protocol / exact binding / STARTED no-clobber | `KEEP` | Appropriate for FORMAL; lower layers correctly remain outside formal one-way machinery unless promoted fresh. |
| Positive candidate signal before strong mechanistic `REDUCED_BY_*` language | `KEEP` | Still needed to separate absent signal from explanation by reduction. |
| Equal-privilege comparator matching, including world/task/regime labels | `KEEP` | NI01 audit remains a concrete justification. |
| Stronger-privilege counterfactual/replay/global-critic ceilings | `CLARIFY` | Useful ceilings, not automatic equal-standing mechanistic reject gates unless privilege is matched. |
| New-computational-principle novelty bar | `KEEP` | Appropriate for the strongest novelty claim. |
| Applying that same bar to architecture/system/testbed work | `SPLIT_BY_CLAIM_TYPE` | The current top-k promotion demonstrates the correct alternative in practice. |
| `NO_HIGH_VALUE_FORMAL_OBJECT => programme-wide HOLD/no-op` | `RELAX` | The Evidence Analyst now correctly rejects this implication. FORMAL may remain empty while lower layers run. |
| Observable/question-level exhaustion instead of broad H1-H9-family exhaustion | `CLARIFY` | SUB's new question shows prior family coverage need not imply observable exhaustion. Make this the durable default rather than an implicit exception. |
| Fresh/independently motivated object requirement | `CLARIFY` | Keep anti-rescue purpose, but fresh architecture/literature-seeded questions are admissible when prospectively defined and independent of consumed outcomes. |
| Default three-cycle exploratory budget | `KEEP` | Current Discovery used cycle 1 and explicitly avoided rescue tuning. |
| Stop new-principle claim after convincing ordinary reduction | `SPLIT_BY_CLAIM_TYPE` | Correctly applied: raw top-k churn novelty was reduced, while the distinct architecture question remained researchable. |
| Architecture-study cycle must stop for Analyst review before redesign/promotion | `KEEP` | Good protection against lower-layer outcome-responsive tuning. |
| Fixed architecture “signal” thresholds being treated as scientific novelty thresholds | `CLARIFY` | The current 2.0/1.5 AUC-ratio criteria are acceptable as prospective bounded architecture decision aids, but are not calibrated novelty or formal-admission thresholds and must not be reused as such without independent justification. |
| H7 as the only plausible *central novelty* residual | `CLARIFY` | Reasonable for current central novelty, but not a filter over architecture/discovery candidates. |
| Control-plane adoption of the new lower-layer doctrine | `CLARIFY` | Evidence Analyst/SUB have adopted it; latest durable Control Brain still predates the change and describes repeated no-op as not a throughput defect. Treat this as stale doctrine until the next Control run reconciles it, not as a reason to revert lower-layer work. |

## Mandatory calibration dimensions

### `gate_drift`

The important new drift is a **prospective relaxation of research allocation**, not of evidence integrity. This is now observable in actual behaviour: safe Discovery occurred, its ordinary reduction was retained, and only a distinct architecture question was promoted. That is the exact correction recommended previously.

### `justification_trace`

Formal gates remain traceable to concrete failures/audits: C19-R2 supports strong ordinary-reduction pressure; NI01 supports explicit privilege matching; the repository's execution preauthorization explicitly preserves no-rerun, frozen protocols, one-way STARTED, and post-outcome no-repair rules. The new lower-layer allocation rule is justified by the earlier repeated no-op equilibrium and now has one successful bounded-use example.

### `false_positive_control`

Still strong. The new architecture object is explicitly `NON_EVIDENTIARY`, DEV-only, with no formal identity or TEST use. The main new false-positive risk is **threshold laundering**: descriptive architecture cutoffs must not later be presented as validated novelty/formal thresholds merely because they were prospectively fixed here.

### `false_negative_risk`

Materially reduced. The top-k case is a useful demonstration: a reducible low-level phenomenon was not allowed to support novelty, but its reduction also did not suppress a separate system-integration question. This is healthier than the previous formal-or-stop behaviour.

### `duplicate_guards`

No new evidence supports removing integrity guards. Consolidate implementation where useful, but preserve their distinct scientific purposes.

### `moving_goalposts`

Still **LOW_RETROACTIVE_RISK**. The top-k Discovery was synthetic and non-evidentiary; the architecture cycle was prospectively specified before outcome. The failed first CI stopped at lint before tests, so no scientific outcome exists to tune against. Consumed/formal evidence remains untouched.

### `pass_reachability`

Still **REACHABLE_BUT_NARROW**. The formal path remains: prospectively positive native signal -> fresh exact-bound object -> matched equal-privilege reductions -> fixed intervention/falsifier -> one-way preserved evidence. The new lower layers improve the chance of discovering an object that deserves this path without weakening the path itself.

### `comparator_calibration`

Unchanged in principle: equal-privilege reductions can directly bear on mechanistic claims; stronger-privilege replay/global-causal ceilings should be labeled separately. The new architecture study's `no_persistent_state` control is an appropriate within-model architecture control, but any later novelty claim would still require broader ordinary matched reductions.

### `signal_before_reduction`

Correctly used in the new workflow. The raw top-k event had a real observed synthetic signal and was then reduced exactly. The programme did not infer a stronger unexplained mechanism from the signal; it formulated a new independent delayed-persistence question instead.

### `claim_type_separation` / `research_worthiness_vs_novelty`

This dimension has materially improved. Evidence Analyst explicitly distinguishes architecture/system value from new-principle novelty and has operationalized that distinction in allocation. This is the strongest new calibration evidence in this run.

### `external_calibration`

No newer Literature/Audit result supersedes the previous audit inputs. COMA/C3/concurrent responsibility remain prospective stronger-privilege ceilings; NI01 remains `WEAKENED` only at the equal-privilege mechanistic interpretation, with canonical terminal evidence unchanged.

### `opportunity_cost`

Current allocation is better balanced. One bounded Discovery cycle generated a concrete architecture question at low integrity risk. Further global tightening would currently have lower expected information gain than allowing this kind of bounded lower-layer work to proceed and converge under stop rules.

## Prospective recommendations

1. **Keep the four-layer funnel and current claim-type separation.** The first post-change cycle supports it.
2. **Let the top-k architecture cycle complete only under its already fixed DEV-only contract.** Mechanical lint/CI fixes are fine if they do not change scientific semantics; do not alter perturbations, metrics, controls, thresholds, seed, horizon, or data based on results.
3. **Do not promote architecture cutoffs into novelty thresholds.** Any later PRE_FORMAL/FORMAL object needs fresh justification and prospective definition.
4. **Require the next Control Brain handoff to reconcile its stale “no-op is not a throughput defect” wording with the now-demonstrated lower-layer funnel.** FORMAL HOLD may remain, but lower-layer productive work should be recognized when safe.
5. **Keep observable-level exhaustion as the standard for no-op.** Prior family coverage is evidence against duplication, not a blanket research ban.
6. **Preserve the three-cycle budget and stop-after-cycle review.** This is functioning as intended against rescue tuning.
7. **Keep equal-privilege reductions separate from stronger-privilege ceilings in all future candidate state.**
8. **Do not alter consumed/frozen evidence.** All methodology changes remain prospective.

## Utility request

**None created.** The material calibration question is already owned by the current MAIN architecture-study lane; creating a Utility request would duplicate an active bounded owner rather than add information.

## Hard-integrity-floor confirmation

Confirmed unchanged: no rerun/retune/rescore of consumed identities; frozen/prospective protocols; raw-before-score; preserve-before-read; exact identity/source/package/runtime/input binding; immutable evidence; no evaluator/target leakage; no silent post-outcome repair.

## Bottom line

The programme is now **only slightly overconservative rather than mixed**: formal integrity remains strong, while the most important allocation defect has begun to correct itself in real runs. The remaining methodological concern is not “too much rigor” in FORMAL; it is ensuring that Control Brain catches up with the lower-layer doctrine and that non-evidentiary architecture signal thresholds never quietly become de facto novelty gates.
