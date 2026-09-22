# External Literature Reduction Scout — 2026-09-22 12:30 JST

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

## Repository and control-plane snapshot consumed

Science source-of-truth was independently refreshed: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; five unchanged annotated `evidence/*` tags; zero tag-form `formal/*`, `sealed/*`, or `freeze/*`; 13 legacy freeze branches; 24 preserve branches; existing STARTED/control refs unchanged. Historical H7 exploratory remains `research/exploratory-sub-h7-trace-causality-20260917@3b5f122d287025bd9e0aec3a5266704236e6a3d5`. Historical R50 remains `research/main-semantic-active-work-localization-r50-cycle2@d090fd2e57680c5a97b9fd0d036fc65a008078ec`.

Consumed generations:

- Control `CTRL-20260922T105700+0900-R32-C5A721D4@544bede4c5131ea57e5b93903bab5279d066a0c0`.
- Evidence Analyst `EVA-20260922T120158+0900-R60-D5E721A4@8cfdb2abb72ff0cfcf616d3400d578db7c20a84d`.
- MAIN `MAIN-20260922T111654+0900-PRIMARY-FUNNEL21-IDLE-R59-A6D4C219@c138d166554daea20bf3ea30f304730b3de1ada5`.
- SUB `SUB-20260922T113500+0900-NOOP-R59INTENTIONALIDLE-A6D4C219@49572dfeb1aa7da7986ac545a10f1e4e89f5d15e`.
- Prior Literature `LIT-20260922T093207+0900-R27-SPECIFICITY-IDENTIFIABILITY-8C3A21F5@237b3c1100e082624ce08d0ac2d7fcb9c7d3dd6d`.

R60 activates `H7-DEV-R1-CLAIM-SCOPED-CAUSAL-CONTRACT` as `MECHANISM / ARCHITECTURE_STUDY / ACTIVE`, `preformal_eligible=true`, `NOT_READY`. Authority is static-contract-only: freeze claim scope, one intervention family, matched reductions, privilege/resource envelope, and falsifier; STOP before result-bearing intervention. A new branch `research/main-h7-dev-r1-claim-scoped-causal-contract-r60-cycle1` was observed at the main head, and initial CI `35683397927` completed successfully. Durable MAIN/SUB report streams were still R59 at the last refresh, so this run consumes no R60 result-bearing science.

## New findings

### 1. Intervention admissibility / well-posedness is a separate causal integrity requirement

Zane, Batenkov, Urbaniak, Zucker & Witty, *A Counterfactual Semantics for Hybrid Dynamical Systems* (NeurIPS 2025), formalize interventions as transformations of hybrid-system constraints and show that interventions can render hybrid systems ill-posed. They identify conditions preserving solution existence, uniqueness, and measurability.

Source: https://proceedings.neurips.cc/paper_files/paper/2025/hash/21e7127fed68ca30862a008d6b50718d-Abstract-Conference.html

For H7 this adds a failure mode distinct from R26 dormant-path activation: an intervention can be scientifically ambiguous because it creates a state/event combination outside the native admissible dynamics or a non-unique continuation. The frozen intervention family should therefore include a native-semantics well-posedness criterion.

### 2. Unconstrained alignment maps can make causal abstraction tautological

Sutter, Minder, Hofmann & Pimentel, *The Non-Linear Representation Dilemma: Is Causal Abstraction Enough for Mechanistic Interpretability?* (NeurIPS 2025), show that sufficiently expressive nonlinear alignment maps can perfectly align models to high-level algorithms even when the underlying models cannot solve the task; random initialized models can reach perfect interchange-intervention alignment in their example.

Source: https://proceedings.neurips.cc/paper_files/paper/2025/hash/dbb98528c9870377f3f0d133aae6050b-Abstract-Conference.html

For H7, native route/state variables or a simple prospectively frozen mapping are preferable. Flexible learned alignment must be counted as information/representation privilege and tested out of sample; otherwise apparent mechanistic distinctness may be supplied by the map rather than the native dynamics.

### 3. Causal abstractions can be regime-dependent inside one task

Pîslar, Magliacane & Geiger, *Combining Causal Models for More Accurate Abstractions of Neural Networks* (CLeaR 2025), show that different high-level causal models can better describe different input-dependent computational states and expose a trade-off between model coverage and interchange-intervention faithfulness.

Source: https://proceedings.mlr.press/v275/pislar25a.html

This is different from R27 task specificity. Even within the same task, a route abstraction may be faithful only in some dynamical/input regimes. A future H7 claim should pre-stratify or report the coverage/faithfulness envelope instead of silently globalizing one local route explanation.

### 4. Intervention-aware reservoir and state-space models are strong ordinary dynamical reductions

Zhao et al., *Detecting dynamical causality via intervened reservoir computing* (Communications Physics 2024), reconstruct nonlinear causal networks by comparing reservoir-generated closed-loop and intervened-loop trajectories. Nejatbakhsh & Wang, *Identifying Neural Dynamics Using Interventional State Space Models* (ICML 2025), explicitly distinguish observational association from causal interpretation and introduce intervention-aware SSMs with identifiability results and novel-perturbation prediction.

Sources: https://www.nature.com/articles/s42005-024-01730-6 ; https://proceedings.mlr.press/v267/nejatbakhsh25a.html

Therefore counterfactual trajectory response is not by itself novel lineage-responsibility evidence. A future H7 object should compare against an intervention-aware recurrent/reservoir/state-space reduction under matched information privilege where possible, or label it a stronger-privilege ceiling. Held-out perturbation generalization is more discriminating than fitting only the intervention family used to define the claimed route.

## Synthesis

R60 makes H7 actionable as a static Architecture contract, and the literature now gives three additional prospective constraints that are materially distinct from R26/R27: **intervention admissibility, abstraction-map complexity, and regime coverage**. Alongside those constraints, intervention-aware reservoir/iSSM work raises the ordinary baseline for causal dynamical response.

This run does not execute or request an H7 experiment, does not alter the historical H7 exploratory result, and does not create a Utility request. Literature guidance may inform the still-unfrozen static R60 contract, but once its intervention/comparator/resource/falsifier choices are frozen, this role must not rewrite them in response to outcomes.

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
  Interventions can make native hybrid dynamics ill-posed, expressive alignment maps can make causal abstraction vacuous,
  and intervention-aware reservoir/state-space methods already provide strong ordinary perturbation-response causal baselines.
  No current H7 mechanism uplift follows from literature alone.
audit_classification: null
prospective_baselines_or_discriminators:
  - admissibility/well-posedness check for every frozen intervention under native event/state semantics
  - native-variable or prospectively frozen low-complexity route/state abstraction map
  - charge flexible alignment-map complexity as information/representation privilege
  - held-out intervention-family generalization
  - explicit dynamical/input regime coverage versus causal faithfulness
  - equal-privilege intervention-aware recurrent/reservoir/state-space comparator where feasible, otherwise stronger-privilege ceiling
  - retain R26 dormant-path and R27 specificity/non-identifiability controls
questions_for_evidence_analyst:
  - While H7-DEV-R1 is static-only, require a native-semantics intervention admissibility criterion in addition to dormant-path controls?
  - Require native or prospectively complexity-bounded route/state alignment and held-out intervention checks if a learned map is used?
  - Scope future H7 conclusions to the dynamical/input regimes actually covered unless cross-regime faithfulness is prospectively shown?
questions_for_control_brain:
  - Add intervention well-posedness and abstraction-map complexity as H7 Architecture failure modes without introducing a hidden FORMAL gate?
  - Treat intervention-aware reservoir/iSSM methods as ordinary reduction targets or stronger-privilege ceilings according to information privilege?
  - Preserve STOP-before-result-bearing-work until the R60 static contract is independently reviewed?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1-v1/C19-R1-v2/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - canonical H5/PD01/NI01 decisions and consumed STARTED/control/preserve refs
  - historical H7 exploratory branch remains NON_EVIDENTIARY and unchanged
  - H7-DEV-R1 remains Architecture development only until fresh Analyst authority permits result-bearing work
  - no outcome-responsive rewrite after H7 intervention/comparator/resource/falsifier choices are frozen
  - candidate #32 predecessor remains terminal for the old object; no same-object rescue
  - no STARTED/TEST/PRE_FORMAL/FORMAL promotion, scientific workflow dispatch, research merge, immutable-ref mutation, or scheduler change by this role
utility_request_created: null
```
