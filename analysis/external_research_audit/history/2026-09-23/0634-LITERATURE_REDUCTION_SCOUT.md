# External Literature Reduction Scout — interventional equivalence / route-graph identifiability

- schema_version: `2`
- generation_id: `LIT-20260923T063434+0900-R34-INTERVENTIONAL-EQUIVALENCE-8F4C21A7`
- produced_at: `2026-09-23T06:34:34+09:00`
- producer_run_id: `external-literature-auto-LIT-20260923T063434+0900-R34-INTERVENTIONAL-EQUIVALENCE-8F4C21A7`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260923T033100+0900-R33-REALIZATION-RUNTIME-5B7E2A91`
- role: `LITERATURE_REDUCTION_SCOUT`
- schedule_slot: `06:30 JST`
- schedule_inference: `false`
- genuinely_new_information: `true`

## Inputs / authoritative state

Repository science and control-plane mailboxes were re-fetched independently. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. The authoritative annotated `evidence/*` set remains five tags; tag-form `formal/*`, `sealed/*`, and `freeze/*` remain empty. The active H7 Cycle-11 source/executor branch is `research/main-h7-formal-r4-source-executor-r85-cycle11@02382fbc7d3838159598015e488c6ce49ac34efc`.

Fresh inputs consumed:
- Control Brain: `CTRL-20260923T055000+0900-R39-C31A7D52` @ `c93f870e47bdb5b1613475e079c0a6dee2aa1753`.
- Evidence Analyst: `EVA-20260923T061000+0900-R87-7B3D91E4` @ `f03769227e888a70ea674eb627d4d311a1229c95`.
- MAIN: `MAIN-20260923T061858+0900-RELAY-H7-FORMALR4-C11-R87-BLOCKED-RUNTIME-BINDING-7B3D91E4` @ `79d5109389f89d781d47e6e541cd87228859c872` (state-path commit; mailbox tip observed `5b116229ae1f91c4d69f2866825797c0a2e59b77`).
- SUB: `SUB-20260923T053741+0900-NOOP-SCAN-R86-62D4A1B7` @ `f71ad78d3bc486816741d345976506db74d50223`.
- Prior Literature: `LIT-20260923T033100+0900-R33-REALIZATION-RUNTIME-5B7E2A91` @ `c25dce890612dcc9b5614f987f4cdeb85e1f5652`.

H7 remains NON_EVIDENTIARY and preidentity. MAIN is currently BLOCKED on a frozen runtime-binding mismatch: the committed torch distribution RECORD hash observed in the clean exact-lock runtime does not match the frozen expected hash, so R87 requires fresh versioned reassessment and forbids silent normalization/rebinding. No evaluation commitment, FORMAL identity, STARTED ref, seed reveal, protected evaluation, result-bearing workflow, official score, scientific preserve, or evidence object exists.

R33 already covered state-coordinate realization equivalence and runtime reproducibility. This run asks a different question: **even if an intervention has a genuine causal effect, does the finite intervention family identify a unique causal route graph/topology?**

## High-value new findings

### 1. Interventional data generally identifies an interventional equivalence class, not automatically a unique causal graph

**External literature fact.** Hauser & Bühlmann formalized interventional Markov equivalence: a fixed family of intervention experiments refines observational Markov equivalence, but in general the result is still an equivalence class represented by an interventional essential graph rather than a unique DAG.

Sources:
- Hauser & Bühlmann, *Characterization and Greedy Learning of Interventional Markov Equivalence Classes of Directed Acyclic Graphs*, JMLR 13 (2012): https://www.jmlr.org/papers/v13/hauser12a.html
- Hauser & Bühlmann, *Jointly interventional and observational data: estimation of interventional Markov equivalence classes of directed acyclic graphs*, JRSS-B (2015): https://arxiv.org/abs/1303.3216

**Repository relevance / inference.** A future H7 result showing a nonzero effect of the frozen dynamic TOP1 cut policy can establish that the policy matters under the tested distribution. It does **not** by itself identify a unique internal causal graph, route topology, or edge orientation. A broad route-structure claim should therefore be scoped to the interventional equivalence class induced by the actually frozen intervention family unless additional interventions separate the remaining alternatives.

### 2. Full structural identification is an intervention-design problem; sample size cannot compensate for an intervention family that fails to separate alternatives

**External literature fact.** Active causal-discovery work treats intervention selection as a structural-identifiability problem. Graph separating systems are sufficient in the idealized setting because interventions must cut/separate the relevant edges; lower bounds and optimal-design results show that the *choice* of intervention targets determines which directions can be identified.

Sources:
- He & Geng, *Active Learning of Causal Networks with Intervention Experiments and Optimal Designs*, JMLR 9 (2008): https://jmlr.org/papers/v9/he08a.html
- Hauser & Bühlmann, *Two Optimal Strategies for Active Learning of Causal Models from Interventional Data* (2012/2014): https://arxiv.org/abs/1205.4174
- Elahi et al., *Adaptive Online Experimental Design for Causal Discovery*, ICML 2024: https://arxiv.org/abs/2405.11548

**Repository relevance / inference.** The current R4 intervention family was frozen to test a narrow causal-policy effect, not to orient every possible native route edge. That is scientifically coherent. But any future successor claiming a uniquely identified responsible topology should prospectively specify the graph features it seeks to identify and demonstrate that its intervention family forms an adequate separating/identifying design for those features. Repeating the same cut policy at more seeds cannot resolve structural ambiguity that the intervention design itself never separates.

### 3. General/soft/unknown-target interventions preserve additional equivalence; target semantics are part of the identifiability contract

**External literature fact.** Yang, Katcoff & Uhler extend interventional equivalence to general interventions that alter mechanisms without necessarily deleting all parent dependencies. Jaber et al. show that with soft interventions and unknown targets, even observational+interventional data can identify only a `Ψ`-Markov equivalence class. A 2026 scalable contrastive method likewise targets the identifiable PDAG/equivalence class available under unknown soft interventions rather than assuming unique recovery.

Sources:
- Yang, Katcoff & Uhler, *Characterizing and Learning Equivalence Classes of Causal DAGs under Interventions*, ICML 2018: https://proceedings.mlr.press/v80/yang18a.html
- Jaber et al., *Causal Discovery from Soft Interventions with Unknown Targets: Characterization and Learning*, NeurIPS 2020: https://proceedings.neurips.cc/paper/2020/hash/6cd9313ed34ef58bad3fdd504355e72c-Abstract.html
- Zhang et al., *Scalable Contrastive Causal Discovery under Unknown Soft Interventions* (2026): https://arxiv.org/abs/2603.03411

**Repository relevance / inference.** H7's dynamic TOP1 intervention target is selected from current native state by a deterministic policy rather than being one fixed physical node across all rows. The target is not “unknown” in the current implementation, so unknown-target theory is not directly applicable; however, fixed-target perfect-intervention identifiability guarantees also cannot simply be imported. The selector, target mapping, and intervention semantics are part of the causal object. Future topology claims should freeze and expose that mapping explicitly and assess equivalence under the actual dynamic policy.

### 4. Because SparkBrain is recurrent, static-DAG interventional equivalence is only a template; topology claims need a temporal/unrolled causal object

**External literature fact.** Interventional causal discovery for time-series/dynamical systems is treated separately from static DAG discovery. IDYNO explicitly models time-delayed and instantaneous relations under observational/interventional time-series data, while CAnDOIT outputs a time-series PAG and notes the need to represent temporal structure and latent confounding. These methods illustrate that causal structure in a dynamic system is tied to lagged/time-indexed variables rather than a single static feedback graph.

Sources:
- Gao et al., *IDYNO: Learning Nonparametric DAGs from Interventional Dynamic Data*, ICML 2022: https://proceedings.mlr.press/v162/gao22a.html
- Castri et al., *CAnDOIT: Causal Discovery with Observational and Interventional Data from Time Series*, Advanced Intelligent Systems (2024): https://doi.org/10.1002/aisy.202400181

**Repository relevance / inference.** Any future H7 graph-identification claim should define whether the graph is a time-unrolled/lagged causal graph, a summary graph, or another explicit dynamic causal object. Applying static-DAG I-MEC language directly to recurrent feedback without this temporal semantics would overstate identifiability. For the present R4 narrow dynamic-policy effect, no graph-structure claim is required.

## Synthesis

The new reduction/identifiability bar is:

`causal effect of a frozen intervention policy` → `features identifiable under that intervention family` → `interventional equivalence class` → `unique topology only if a prospective separating/identifying intervention design collapses the class`.

This is distinct from R33. R33 showed that internal coordinates can be non-unique even for the same realization; R34 shows that **even after choosing causal variables, a finite intervention family can leave multiple causal structures interventionally indistinguishable**.

No current R4 rewrite follows. R4 is already scoped to a narrow dynamic-policy causal effect and its frozen scientific fields must remain untouched. The present runtime-binding block is a separate preidentity provenance/runtime matter for fresh Analyst disposition.

No Utility request is created. A graph-separation prototype would be a new science choice and would contaminate the current frozen R4 object; it belongs, if ever needed, in a fresh successor after R4 disposition.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - H7_FORMAL_R4_CLAIM_SCOPE
  - H7_FUTURE_INTERVENTIONAL_EQUIVALENCE
  - H7_CAUSAL_STRUCTURE_IDENTIFIABILITY
  - H7_DYNAMIC_INTERVENTION_TARGET_SEMANTICS
  - H7_TEMPORAL_CAUSAL_GRAPH_SCOPE
  - FUTURE_MECHANISM_SUCCESSOR_ADMISSION
  - PROGRAMME_NOVELTY
novelty_or_reduction_impact: >
  INTERVENTIONAL_EQUIVALENCE_SHARPENS_UNIQUE_ROUTE_GRAPH_CLAIM_NO_CURRENT_R4_REWRITE_OR_MECHANISM_UPLIFT.
  A causal effect under the frozen intervention policy does not by itself identify a unique route graph.
  Structural claims are limited to the equivalence class induced by the actual intervention family unless a prospectively sufficient separating design resolves the remaining alternatives.
audit_classification: null
prospective_baselines_or_discriminators:
  - compute/report the interventional equivalence class induced by the frozen intervention family for any future graph-structure claim
  - predeclare exactly which route/edge features are claimed identifiable
  - use a fresh-successor-only separating/covering intervention design if unique topology is claimed
  - freeze dynamic target-selector/target-map semantics as part of the intervention definition
  - formulate recurrent claims on an explicit time-unrolled/lagged dynamic causal object
  - if the intervention family does not identify a unique graph, report equivalence-class scope rather than unique topology
questions_for_evidence_analyst:
  - Keep current R4 scoped to the frozen dynamic-policy effect and do not infer unique route topology from any future PASS?
  - For a future topology successor, require an explicit identifiability target and an intervention family shown to separate the claimed alternatives?
  - Treat dynamic target selection and temporal graph semantics as part of the prospective causal-identification contract?
questions_for_control_brain:
  - Add "intervention effect != unique causal graph" as a future H7 claim-ceiling guardrail?
  - Keep interventional-equivalence/separating-design work prospective and outside the frozen R4 comparator/intervention panel?
  - Preserve all current R4 preidentity STOP boundaries while the runtime-binding mismatch is reassessed?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1-v1/C19-R1-v2/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - H7 PF-R1 development result/raw and no-rerun/no-rescore boundary
  - stopped H7 R1/R2/R3 historical objects and classifications
  - H7 R4 claim/estimand/worlds/intervention/comparator panel/thresholds/bootstrap-decision/falsifier/concealed-evaluation/raw-gate/scorer semantics
  - H7 R4 exact recovered runtime lock/manifest and frozen package/resource choice
  - no FORMAL identity, STARTED, evaluation commitment/seed reveal, protected evaluation, result-bearing workflow, official scoring, scientific preserve/evidence ref, research merge, immutable-ref mutation, Utility execution, or scheduler change by this role
utility_request_created: null
```
