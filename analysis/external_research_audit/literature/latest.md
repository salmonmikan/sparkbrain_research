# External Literature Reduction Scout — intervention admissibility, alignment complexity, and interventional dynamical baselines

- schema_version: `2`
- generation_id: `LIT-20260922T123000+0900-R28-INTERVENTION-ADMISSIBILITY-6B4D21F8`
- produced_at: `2026-09-22T12:30:00+09:00`
- producer_run_id: `external-literature-auto-20260922T123000+0900-R28-6B4D21F8`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260922T093207+0900-R27-SPECIFICITY-IDENTIFIABILITY-8C3A21F5`
- role: `LITERATURE_REDUCTION_SCOUT`
- schedule_slot: `12:30 JST`
- schedule_inference: `false`
- genuinely_new_information: `true`

## Inputs / authoritative state

Repository science was re-fetched independently of all `ops/*` mailboxes. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. The authoritative annotated `evidence/*` set remains exactly five and unchanged; tag-form `formal/*`, `sealed/*`, and `freeze/*` remain empty. Legacy `freeze/*` branches remain 13, `preserve/*` branches remain 24, and existing `control/*` STARTED refs were inspected independently. PR #148 and #149 remain open/unmerged governance work.

Consumed control-plane generations and exact handoff commits:

- Control Brain: `CTRL-20260922T105700+0900-R32-C5A721D4` @ `544bede4c5131ea57e5b93903bab5279d066a0c0`.
- Evidence Analyst: `EVA-20260922T120158+0900-R60-D5E721A4` @ `8cfdb2abb72ff0cfcf616d3400d578db7c20a84d`.
- MAIN report: `MAIN-20260922T111654+0900-PRIMARY-FUNNEL21-IDLE-R59-A6D4C219` @ `c138d166554daea20bf3ea30f304730b3de1ada5`.
- SUB report: `SUB-20260922T113500+0900-NOOP-R59INTENTIONALIDLE-A6D4C219` @ `49572dfeb1aa7da7986ac545a10f1e4e89f5d15e`.
- prior Literature: `LIT-20260922T093207+0900-R27-SPECIFICITY-IDENTIFIABILITY-8C3A21F5` @ final role handoff `237b3c1100e082624ce08d0ac2d7fcb9c7d3dd6d` (`latest.md` path commit `b76e121cf5a005e639b5aabc535112a89ee484ed`).

The material repository/control-plane delta is Evidence Analyst R60. Under the newer development-iteration policy it activates `H7-DEV-R1-CLAIM-SCOPED-CAUSAL-CONTRACT` as a bounded `MECHANISM / ARCHITECTURE_STUDY / ACTIVE` development revision with `preformal_eligible=true` but `preformal_readiness=NOT_READY`. The authorized MAIN action is static contract work only: freeze claim scope, one intervention family, matched ordinary reductions, privilege/resource envelope, and falsifier, then STOP before any result-bearing intervention. Historical H7 exploratory observations remain NON_EVIDENTIARY.

A fresh repository branch `research/main-h7-dev-r1-claim-scoped-causal-contract-r60-cycle1` now exists at the unchanged `main` head; its initial ordinary CI run `35683397927` completed successfully. At the last re-fetch, the durable MAIN/SUB report streams still contained R59, so no R60 MAIN scientific result or result-bearing intervention is consumed by this Literature run. This is dependency-aware freshness, not evidence that MAIN is stale or failed.

Prior Literature R26/R27 already covered intervention-induced dormant paths, causal-abstraction faithfulness, necessity/sufficiency/completeness, task specificity, route non-identifiability, and redundancy/synergy. Those findings are not recycled below. This run asks a narrower question now made actionable by R60: **what additional constraints must the exact frozen intervention family and route/state abstraction satisfy before a causal-responsibility result is interpretable?**

## High-value new findings

### 1. Dynamically triggered interventions can make a hybrid dynamical system ill-posed

Zane, Batenkov, Urbaniak, Zucker & Witty, *A Counterfactual Semantics for Hybrid Dynamical Systems* (NeurIPS 2025), formalize interventions as transformations of hybrid-system constraints and explicitly show that interventions can destroy well-posedness. They give conditions for preserving solution existence, uniqueness, and measurability.

Source: https://proceedings.neurips.cc/paper_files/paper/2025/hash/21e7127fed68ca30862a008d6b50718d-Abstract-Conference.html

**Reduction impact:** R26 established that an intervention may awaken a dormant path; this is a different failure mode. Even without dormant-path activation, an H7 delete/replace/clamp intervention can be scientifically ambiguous if it creates a state/event combination that the native dynamics do not admit, or if the post-intervention trajectory is non-unique. The prospective H7 intervention family should therefore include an **admissibility / well-posedness gate** appropriate to SparkBrain's event-driven recurrent semantics: the intervention must define a unique, executable continuation under the same timing and state-transition rules, rather than merely producing some output in an instrumented implementation.

### 2. Causal abstraction can become vacuous if the route/state alignment map is too expressive

Sutter, Minder, Hofmann & Pimentel, *The Non-Linear Representation Dilemma: Is Causal Abstraction Enough for Mechanistic Interpretability?* (NeurIPS 2025), show theoretically and empirically that unconstrained nonlinear alignment maps can make causal-abstraction tests uninformative. Their experiments obtain perfect interchange-intervention alignment even for randomly initialized models that cannot solve the task.

Source: https://proceedings.neurips.cc/paper_files/paper/2025/hash/dbb98528c9870377f3f0d133aae6050b-Abstract-Conference.html

**Reduction impact:** H7 must not gain mechanistic credit from a flexible post-hoc map between native SparkBrain state/route variables and the high-level responsibility variable. Prefer native identity/readout variables or a simple prospectively frozen map; otherwise map complexity must be counted as information/representation privilege and tested on held-out interventions. This sharpens R27's non-identifiability result into a concrete anti-tautology control.

### 3. A single high-level causal mechanism may be faithful only in part of the input/dynamical regime

Pîslar, Magliacane & Geiger, *Combining Causal Models for More Accurate Abstractions of Neural Networks* (CLeaR 2025), find that different simple high-level causal models can describe different computational states depending on the input, and expose a trade-off between explanation coverage and interchange-intervention faithfulness.

Source: https://proceedings.mlr.press/v275/pislar25a.html

**Reduction impact:** even if one frozen H7 route abstraction is faithful on selected cases, it should not automatically be generalized to all relevant trajectories. A future contract should report the **coverage/faithfulness envelope** or prospectively stratify the dynamical/input regimes to which the route claim applies. This is distinct from R27 task specificity: the same task can traverse different computational states and admit different faithful abstractions.

### 4. Ordinary reservoir/state-space methods already support causal claims from interventions on nonlinear dynamics

Zhao et al., *Detecting dynamical causality via intervened reservoir computing* (Communications Physics 2024), use a reservoir digital twin with closed-loop versus intervened-loop trajectories to reconstruct nonlinear causal networks. Nejatbakhsh & Wang, *Identifying Neural Dynamics Using Interventional State Space Models* (ICML 2025), show that observational state-space models alone are not causally interpretable and propose interventional SSMs that predict responses to novel perturbations with identifiability guarantees.

Sources: https://www.nature.com/articles/s42005-024-01730-6 and https://proceedings.mlr.press/v267/nejatbakhsh25a.html

**Reduction impact:** observing counterfactual trajectory change under an H7 intervention is not by itself a novel lineage-responsibility capability. A strong ordinary reduction/ceiling is an intervention-aware recurrent/reservoir or state-space model that receives matched observations and predicts the same perturbation response. If exact information privilege cannot be matched, these models remain stronger-privilege ceilings rather than equal-privilege baselines. The discriminator should be **out-of-intervention-family generalization under a frozen model**, not only fit to the interventions used to define the route.

## Synthesis

R60 makes H7 active again, but the literature bar is now more precise. The static contract should freeze not merely an intervention family, but an **admissible intervention family plus a complexity-bounded abstraction map and an explicit regime/coverage scope**. Then any native local-responsibility signal should be compared against ordinary intervention-aware recurrent/state-space reductions under matched privilege, or against them as explicitly stronger-privilege ceilings.

This does not authorize an H7 experiment, change the R60 intervention family after it is frozen, or supply a hidden PRE_FORMAL gate. It is prospective Architecture guidance while the R60 static contract is still being fixed. No Utility request is created because MAIN already owns the exact static-contract surface; a parallel implementation request would duplicate or contaminate that prospective choice.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - H7_DEV_R1_CLAIM_SCOPED_CAUSAL_CONTRACT
  - H7_INTERVENTION_ADMISSIBILITY
  - H7_CAUSAL_ABSTRACTION_MAP_COMPLEXITY
  - H7_REGIME_COVERAGE_AND_FAITHFULNESS
  - H7_ORDINARY_INTERVENTIONAL_DYNAMICAL_BASELINES
  - FUTURE_MECHANISM_OBJECT_ADMISSION
  - PROGRAMME_NOVELTY
novelty_or_reduction_impact: >
  INTERVENTION_ADMISSIBILITY_AND_ABSTRACTION_COMPLEXITY_SHARPENING_WITH_ORDINARY_INTERVENTIONAL_DYNAMICS_REDUCTION.
  An intervention can be causally misleading because it makes the native hybrid dynamics ill-posed,
  and a causal-abstraction result can be vacuous when its alignment map is too expressive.
  Intervention-aware reservoirs and state-space models also establish a strong ordinary baseline/ceiling
  for perturbation-response causality. No current H7 mechanism uplift follows from literature alone.
audit_classification: null
prospective_baselines_or_discriminators:
  - admissibility/well-posedness check for every frozen intervention: executable continuation, solution existence, uniqueness, and native event/state semantics
  - native-variable or prospectively frozen low-complexity route/state-to-causal-variable map; charge flexible alignment complexity as information privilege
  - held-out intervention-family generalization rather than evaluating only interventions used to define the route
  - report or pre-stratify dynamical/input-regime coverage versus causal faithfulness
  - equal-privilege intervention-aware recurrent/reservoir/state-space comparator where feasible; otherwise label iSSM/IRC-style analysis a stronger-privilege ceiling
  - retain R26 dormant-path controls and R27 specificity/non-identifiability/equivalence-class claim scoping
questions_for_evidence_analyst:
  - While H7-DEV-R1 is still static-only, require the frozen intervention family to state an admissibility/well-posedness criterion in addition to dormant-path controls?
  - Require the route/state abstraction map to be native or prospectively complexity-bounded, with held-out intervention checks if a learned map is used?
  - Scope any future H7 result to the dynamical/input regimes actually covered unless cross-regime faithfulness is prospectively demonstrated?
questions_for_control_brain:
  - Add intervention well-posedness and abstraction-map complexity as H7 Architecture failure modes without creating a second hidden FORMAL gate?
  - Treat intervention-aware reservoir/iSSM methods as ordinary reduction targets or stronger-privilege ceilings depending on matched information privilege?
  - Preserve the R60 STOP-before-result-bearing-work boundary until the static contract is reviewed with these prospective constraints?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1-v1/C19-R1-v2/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - canonical H5/PD01/NI01 decisions and consumed STARTED/control/preserve refs
  - historical H7 exploratory branch remains NON_EVIDENTIARY and unchanged
  - H7-DEV-R1 remains Architecture development only until fresh Analyst authority permits result-bearing work
  - once the H7 intervention/comparator/resource/falsifier contract is frozen, this literature must not rewrite it outcome-responsively
  - candidate #32 predecessor remains terminal for the old object; no same-object rescue
  - no STARTED/TEST/PRE_FORMAL/FORMAL promotion, scientific workflow dispatch, research merge, immutable-ref mutation, or scheduler change by this role
utility_request_created: null
```
