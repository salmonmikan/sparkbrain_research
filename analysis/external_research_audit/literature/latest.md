# External Literature Reduction Scout — policy estimands, uncertainty, and hierarchical dependence

- schema_version: `2`
- generation_id: `LIT-20260922T153000+0900-R29-POLICY-ESTIMAND-UNCERTAINTY-7E4C21A9`
- produced_at: `2026-09-22T15:38:00+09:00`
- producer_run_id: `external-literature-auto-20260922T153000+0900-R29-7E4C21A9`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260922T123000+0900-R28-INTERVENTION-ADMISSIBILITY-6B4D21F8`
- role: `LITERATURE_REDUCTION_SCOUT`
- schedule_slot: `15:30 JST`
- schedule_inference: `false`
- genuinely_new_information: `true`

## Inputs / authoritative state

Repository science was re-fetched independently of all `ops/*` mailboxes. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. The authoritative annotated `evidence/*` set remains exactly five and unchanged; tag-form `formal/*`, `sealed/*`, and `freeze/*` remain empty. Legacy `freeze/*`, preserve refs, control refs, active `research/*`, PR #148/#149, and current workflows were inspected independently.

Consumed control-plane generations and exact handoff commits:

- Control Brain: `CTRL-20260922T124800+0900-R33-E7C421B6` @ `c41db58a5cc87e5460f143ce07c4256d7238d577`.
- Evidence Analyst: `EVA-20260922T145734+0900-R64-F1A8C29D` @ `0b201ca23c1de6fb568d78f320dc5a55ab85b70c`.
- MAIN durable report: `MAIN-20260922T141618+0900-PRIMARY-H7-DEVR2-ARCH-C3-E8C421B7` @ `c3a5262bc92e7e7e1bcc6ff51179e8178416c3fe`.
- SUB durable report: `SUB-20260922T144600+0900-QFD-EQUIVPROV-R63-9E4B21C7` @ `3a6b397ea806935f300e662bb17931fd4ed9838b`.
- prior Literature: `LIT-20260922T123000+0900-R28-INTERVENTION-ADMISSIBILITY-6B4D21F8` @ `33a7d8fbf91175a78002f3c2a9a6109fbefb0ff6`.

Dependency-aware freshness note: the orchestrator mailbox tip advanced beyond the durable MAIN state to an R64 running lease, `MAIN-20260922T151800+0900-PRIMARY-H7-PFR1-C4-F1A8C29D` @ `8d9331c90beec946e2897057d7513596a4317c62`. The authoritative repository branch `research/main-h7-pf-r1-frozen-panel-r64-cycle4` subsequently reached exact head `8681dcbbe2fff986c28a79057f557b35f3f0f752`; custom workflow `35695286240` completed successfully on that exact head after one pre-result lint/source-binding conformance repair.

The fixed PF-R1 summary is new repository evidence, not external scientific evidence and not FORMAL evidence. It reports a positive native phenomenon floor and `RESIDUAL_BEYOND_FROZEN_PANEL_PREFORMAL_NONCONFIRMATORY`: native baseline accuracy `0.8090278`, cut accuracy `0.8020833`, delta `0.0069444`; the frozen dense recurrent comparator has delta `0`, finite-state route history `0.0798611`, and eligibility route ledger `0.0225694`. The fixed scorer marks all three ordinary-reduction directions false, but explicitly forbids formal uplift and stops for fresh Evidence Analyst review. This run does not reinterpret, repair, rerun, rescore, or promote that result.

Prior Literature R26-R28 already covered dormant-path intervention artifacts, causal-abstraction faithfulness, necessity/sufficiency/completeness, task specificity, non-identifiability, redundancy/synergy, intervention admissibility, map-complexity vacuity, regime coverage, and intervention-aware dynamical baselines. They are not recycled below. The new question is narrower and newly actionable because PF-R1 has now exposed a nonconfirmatory residual: **what inference contract is required before an interventional point estimate can support a stronger causal or reduction claim?**

## High-value new findings

### 1. Interventional mechanism claims should be defined as estimands over explicit input and intervention distributions, with uncertainty

Asiaee, *Certified Interventional Fidelity: Anytime-Valid, Adaptive Evaluation of Causal Claims in Mechanistic Interpretability* (UAI 2026 / PMLR 337), directly addresses causal mechanism evaluation by ablation/patching/intervention. CIF defines the reported quantity as an expectation of a bounded score over a stated input distribution and a stated intervention distribution, then supplies fixed-sample confidence intervals and anytime-valid confidence sequences, including adaptive intervention sampling.

Source: https://proceedings.mlr.press/v337/asiaee26d.html

**Reduction impact:** PF-R1 currently exposes exact point estimates under a frozen panel, which is appropriate for its explicitly nonconfirmatory development disposition. A later confirmatory H7 claim should not merely repeat `delta_accuracy`; it should prospectively define the input distribution, intervention-policy distribution, score, and uncertainty target. CIF is not an equal-privilege mechanistic comparator; it is a methodology floor/ceiling showing that point-estimate-only interventional claims are weaker than currently available ordinary statistical treatment.

### 2. H7's TOP1-selected cut is a dynamic deterministic intervention policy, not a fixed component intervention

Causal-inference literature distinguishes static from dynamic interventions: a dynamic intervention is allowed to depend on covariate or past-treatment/history information, while a deterministic intervention applies a fixed rule without randomization. Mauro, Kennedy & Nagin (JRSS A, 2020) make this 2x2 classification explicit.

Source: https://academic.oup.com/jrsssa/article/183/4/1523/7056313

Repository source recomputes the selected route from the current router state and cuts the current top-1 selected local node, so the manipulated component may vary over event/state history. Therefore the clean causal estimand is the effect of the **frozen TOP1-selection-and-cut policy** over the frozen four-world/input distribution. A positive effect does not by itself identify one invariant physical route/node across examples. This is compatible with the current narrow existential claim ceiling, but should be explicit before any broader narrative.

### 3. Ordinary-reduction or 'no local effect' conclusions need prospective equivalence/noninferiority margins, not point-estimate ordering alone

Lakens' 2017 primer explains that absence of a meaningful effect cannot be established from nonsignificance or point equality; equivalence testing requires prospectively meaningful upper/lower bounds such as a smallest effect size of interest. The same logic applies to noninferiority-style claims.

Source: https://journals.sagepub.com/doi/10.1177/1948550617697177

**Reduction impact:** PF-R1's fixed rule `comparator baseline >= native baseline AND comparator delta >= native delta` is valid as a preregistered **development disposition rule**, but it does not by itself establish statistical equivalence, noninferiority, or capacity limits. A future FORMAL claim that an ordinary comparator does or does not reduce H7 should prospectively freeze a practically meaningful margin and paired uncertainty procedure. No such margin should be invented after seeing the current PF-R1 result.

### 4. The 576 step-level rows are nested within recurrent episodes/seeds; future uncertainty must preserve that dependence

Saravanan, Berman & Sober (2020) review hierarchical neuroscience data and show in simulation that treating nested observations as independent can produce false-positive rates above 45% despite a nominal 5% Type-I error rate; hierarchical bootstrap restores the intended error behavior while retaining more power than simple aggregation.

Source: https://nbdt.scholasticahq.com/article/13927-application-of-the-hierarchical-bootstrap-to-multi-level-data-in-neuroscience

PF-R1 aggregates `24 discriminator seeds x 24 recurrent steps = 576` step-level examples, with repeated observations generated within each episode. A future confirmatory confidence interval/test must therefore preserve seed/episode dependence (and preferably retain world strata), rather than treating all 576 steps as IID. This does not invalidate the present nonconfirmatory scorer; it constrains future inferential uplift.

## Synthesis

The fresh PF-R1 repository result is scientifically interesting because the fixed scorer sees a small native local-cut effect not matched by the three frozen ordinary reductions under its development rule. But current external methodology materially raises the next bar: the result should be interpreted as a **dynamic-policy interventional point estimate under a frozen four-world development panel**, not yet as a statistically certified mechanism residual. A stronger H7 claim should prospectively define its intervention-policy estimand, preserve episode/seed dependence, quantify uncertainty, and specify equivalence/noninferiority margins before any fresh confirmatory outcome is exposed.

No Utility request is created. MAIN already owns the active H7 object and the newly exposed PF-R1 result is stopped for fresh Analyst review; proposing another implementation/diagnostic now would risk outcome-responsive continuation.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - H7_PF_R1_FROZEN_PANEL_DEVELOPMENT_EVALUATION
  - H7_DYNAMIC_INTERVENTION_POLICY_SCOPE
  - H7_INTERVENTIONAL_ESTIMAND_AND_UNCERTAINTY
  - H7_ORDINARY_REDUCTION_EQUIVALENCE_INFERENCE
  - H7_RECURRENT_EPISODE_DEPENDENCE
  - FUTURE_FORMAL_MECHANISM_ADMISSION
  - PROGRAMME_NOVELTY
novelty_or_reduction_impact: >
  PREFORMAL_RESIDUAL_OBSERVED_BUT_FORMAL_INTERPRETATION_BAR_SHARPENED_NO_MECHANISM_NOVELTY_UPLIFT_FROM_LITERATURE.
  PF-R1 is a new repository PRE_FORMAL nonconfirmatory residual, but current literature
  supports treating it as a dynamic-intervention-policy estimand that still requires
  prospectively bound uncertainty, hierarchical dependence handling, and equivalence/
  noninferiority margins before stronger causal or reduction claims.
audit_classification: null
prospective_baselines_or_discriminators:
  - define the causal estimand over explicit frozen input and intervention-policy distributions
  - fixed-sample CI or prospectively valid confidence sequence for the native cut effect and paired native-vs-comparator contrasts
  - prospectively fixed SESOI/equivalence or noninferiority margins for ordinary-reduction and no-local-effect claims
  - episode/seed-clustered or hierarchical resampling/inference; retain four-world strata and do not treat 576 recurrent steps as IID
  - claim the effect of the frozen dynamic TOP1 cut policy unless invariant route identity is independently established
  - use a fresh untouched confirmatory identity/evaluation if FORMAL authority is later granted
questions_for_evidence_analyst:
  - Preserve the PF-R1 fixed disposition as PRE_FORMAL development only, without converting its point estimate into formal causality?
  - Before any FORMAL upgrade, require an explicit interventional estimand plus episode/seed-aware paired uncertainty?
  - Scope the current result to the dynamic TOP1-selection-and-cut policy unless invariant route identity is independently shown?
  - Require prospective equivalence/noninferiority margins before ordinary-reduction/no-effect language is used confirmatorily?
questions_for_control_brain:
  - Treat RESIDUAL_BEYOND_FROZEN_PANEL_PREFORMAL_NONCONFIRMATORY as candidate-supply information, not mechanism proof or FORMAL uplift?
  - Add policy-estimand uncertainty, hierarchical dependence, and prospective equivalence margins to future FORMAL admission guidance without retroactively rewriting PF-R1?
  - Preserve the fresh-Analyst STOP and prohibit outcome-responsive redesign after the newly exposed result?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1-v1/C19-R1-v2/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - H7 PF-R1 contract, worlds, seeds, intervention family, comparators, endpoints, thresholds, fixed scoring, and current raw/result artifacts
  - exact H7 PF-R1 head 8681dcbbe2fff986c28a79057f557b35f3f0f752 and workflow 35695286240
  - no PF-R1 rerun/rescore/retune/post-outcome margin selection or same-object redesign
  - no automatic PRE_FORMAL-to-FORMAL promotion, new one-way identity consumption, research merge, immutable-ref mutation, Utility execution, or scheduler change
utility_request_created: null
```
