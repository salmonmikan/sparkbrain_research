# External Literature Reduction Scout — intervention realism and causal abstraction for candidate #35

- schema_version: `2`
- generation_id: `LIT-20260923T213000+0900-R39-OFFMANIFOLD-INTERVENTIONS-6D2A8C41`
- produced_at: `2026-09-23T21:28:17+09:00`
- producer_run_id: `external-literature-auto-LIT-20260923T213000+0900-R39-OFFMANIFOLD-INTERVENTIONS-6D2A8C41`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260923T183000+0900-R38-SUBTHRESHOLD-STATE-SUFFICIENCY-3B7E21C6`
- role: `LITERATURE_REDUCTION_SCOUT`
- schedule_slot: `21:30 JST`
- schedule_inference: `false`
- genuinely_new_information: `true`

## Authoritative inputs

Stable `main` is `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. Current authoritative evidence remains five `evidence/*` tags; tag-form `formal/*`, `sealed/*`, and `freeze/*` are empty, while legacy freeze branches and preserve refs were independently inspected. Candidate #34's PRE_FORMAL result remains preserved at `preserve/cand34-d34-q002-r94-raw-20260923@4d45f1135bcb607f1e663648cd8335333eb98de4` and was not reinterpreted. Open PRs #148/#149 are non-scientific repository work.

Consumed generations/commits:
- Control Brain `CTRL-20260923T155900+0900-R43-A91C4E6B` @ `1592c3b52a8a545aa2503fd4618c0a761921ef1e`
- Evidence Analyst `EVA-20260923T210010+0900-R99-6F2B8C14` @ `59dbcdc2e3541e78a64f64e16fa0be5ef38efc26`
- MAIN `MAIN-20260923T205800+0900-PRIMARY-H7-FORMAL-R5-R98-BLOCKED-SIDECAR` @ `ae3d90f4f423e1bd75e4b4393bc6974eaacbbafd`
- Fast Forge `FORGE-20260923T193417+0900-NOOP-H7-PREFETCH-R97` @ `b721f54ecb2293bbaaae9a26d475bb75fc290c02`
- Prior Literature `LIT-20260923T183000+0900-R38-SUBTHRESHOLD-STATE-SUFFICIENCY-3B7E21C6` @ `5046658b3994ccce1cdd9a88fe912fc97c8f8b0b`

Evidence Analyst R99 supersedes prior H7 FORMAL GO after a NON_RESULT readiness run failed closed before identity creation at the already-required protected-sidecar capability gate. No H7 identity was consumed and no scientific result exists. Candidate #35 therefore becomes the only coherent canonical forward-motion surface, but only for science-invariant preserve-before-read/provenance plumbing; response execution remains STOP.

Candidate #35 remains `research/main-cand35-queue-free-subthreshold-architecture-r96-cycle3@8ea6581544c642ad74f1a95955ab2c5f795afccc`, exact-head CI green and without response generation. The frozen arms clone a queue-empty anchor and directly set `potential=0`, `adaptation=0`, or both for all non-receptor units. R38 already established that the underlying 18 ms membrane and 90 ms adaptation traces are ordinary leaky/adaptive state. This run asks a distinct question: whether coordinate-wise nulling faithfully probes the natural mechanism or can create counterfactual states outside the naturally reachable state set.

## High-value findings

### 1. Coordinate interventions can be off-manifold and can create misleading mechanistic evidence

Grant, Han, Tartaglini & Potts show that common internal causal interventions can shift representations away from a model's natural distribution. Their analysis distinguishes harmless divergence in a behavioral null-space from pernicious divergence that activates dormant pathways and can create misleading positive or negative evidence.

Source: Grant et al., *Addressing divergent representations from causal interventions on neural networks*, arXiv:2511.04638 (2025; revised 2026), https://arxiv.org/abs/2511.04638

This does not prove candidate #35's explicit causal-state nulls are invalid. However, its `POTENTIAL_NULL`, `ADAPTATION_NULL`, and `JOINT_SUBTHRESHOLD_NULL` arms splice coordinates to zero while preserving the remainder of a naturally reached anchor. Those tuples are valid simulator states but are not yet shown to be states the frozen natural dynamics can reach.

Impact: a future R2 difference establishes synthetic-null component sensitivity. It does not by itself establish that the naturally operating queue-free memory is uniquely carried by that coordinate. A null effect also does not fully close the natural role if the synthetic state induces compensating dynamics.

### 2. Neural-dynamics methodology distinguishes within-manifold from outside-manifold perturbations

A broad neural-population-dynamics review distinguishes perturbations consistent with the circuit's naturally occupied low-dimensional manifold from perturbations that create activity the circuit would not naturally express. Outside-manifold perturbations can still reveal useful dynamics, but within-manifold perturbations are cleaner tests of natural computation.

Source: *Measurement, manipulation and modeling of brain-wide neural population dynamics* (2021), https://pmc.ncbi.nlm.nih.gov/articles/PMC7840924/

Impact: current R2 remains a legitimate surgical intervention experiment, but its strongest claim should stay at component sensitivity under the frozen nulls. A broader natural-memory attribution needs a fresh reachable-state or matched-natural-history counterfactual.

### 3. Causal abstraction is a stronger reduction test than coordinate necessity

Geiger et al. formalize when a simpler high-level model is a faithful causal abstraction of a lower-level system under interventions. Interchange interventions compare the counterfactual behavior of aligned low- and high-level variables, and the JMLR framework supports graded faithfulness.

Sources:
- Geiger et al., *Causal Abstraction: A Theoretical Foundation for Mechanistic Interpretability*, JMLR 26(83), 2025, https://www.jmlr.org/papers/v26/23-0058.html
- Geiger et al., *Inducing Causal Structure for Interpretable Neural Networks*, ICML 2022, https://proceedings.mlr.press/v162/geiger22a.html

Impact: a future reduction should ask whether a privilege-matched model containing only ordinary leaky potential, adaptation, threshold/refractory state and time reproduces the same intervention-conditioned responses. If yes, candidate #35 is causally reducible at the tested scope even if its native state coordinates are individually necessary.

### 4. A single global intervention score can hide state-dependent failure, and small combinations of ordinary models can explain more than one monolithic baseline

Li et al. (2026) show that global interchange-intervention accuracy can conceal regions where a proposed interpretation fails; state/input partitioning can reveal missing distinctions and intermediate variables. Pîslar, Magliacane & Geiger (2025) show that combining simple high-level causal models can provide a more faithful abstraction than requiring one model to explain all inputs.

Sources:
- Li et al., *Bucketing the Good Apples: A Method for Diagnosing and Improving Causal Abstraction*, arXiv:2605.02234, https://arxiv.org/abs/2605.02234
- Pîslar, Magliacane & Geiger, *Combining Causal Models for More Accurate Abstractions of Neural Networks*, arXiv:2503.11429, https://arxiv.org/abs/2503.11429

Impact: any fresh #35 or H7 successor attempting a broader mechanism claim should prospectively stratify counterfactual faithfulness across anchor/cue/state regions and should rule out a small composition of ordinary reductions, not merely one baseline at a time.

## Synthesis

This is genuinely new relative to R38. R38 established the ordinary leaky/adaptive mechanism floor; R39 adds an intervention-validity distinction: **surgical state sensitivity is not automatically natural-state mechanism attribution**. The appropriate prospective ladder is:

`frozen coordinate-null sensitivity` -> `reachable-state / intervention-realism check` -> `privilege-matched leaky/adaptive causal abstraction` -> `state-region-stratified faithfulness and small compositions of ordinary reductions` -> `only then a broader persistent-state residual`.

The current R96 candidate #35 object must not be retrofitted. H7 remains on a non-result sidecar capability HOLD. No Utility request is created.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - CAND35_STATE_NULL_INTERVENTION_REALISM
  - CAND35_REACHABLE_STATE_MANIFOLD
  - CAND35_LOCAL_CAUSAL_ABSTRACTION_REDUCTION
  - CAND35_SYSTEM_CLAIM_CEILING
  - H7_FUTURE_STATE_CONDITIONAL_CAUSAL_ABSTRACTION
  - FUTURE_SYSTEM_TO_MECHANISM_ADMISSION
  - PROGRAMME_NOVELTY
novelty_or_reduction_impact: >
  COORDINATE_NULL_EFFECTS_DO_NOT_BY_THEMSELVES_ESTABLISH_A_NATURAL_MECHANISM.
  Candidate #35's null arms are valid surgical interventions, but recent intervention-faithfulness
  work adds an off-manifold/reachability failure mode. Broader natural-state attribution should
  survive a reachable-state check and privilege-matched causal abstraction by ordinary leaky/adaptive dynamics.
audit_classification: null
prospective_baselines_or_discriminators:
  - fresh-successor-only reachable-state / nearest-natural-state support check for each null arm
  - matched natural-history counterfactual without direct coordinate surgery where prospectively feasible
  - privilege-matched causal abstraction with potential, adaptation, dynamic threshold, refractory/time and frozen decay laws
  - prospectively fixed intervention-faithfulness evaluation across multiple anchor/cue/state regions
  - small composition/mixture of ordinary reductions before any irreducibility claim
questions_for_evidence_analyst:
  - Keep current candidate #35 object unchanged and interpret any later R2 effect as synthetic-null component sensitivity unless intervention realism is separately established?
  - For any fresh successor, require reachable-state or matched-natural-history counterfactual evidence before broader natural-memory attribution?
  - Require causal-abstraction faithfulness against an ordinary leaky/adaptive model before SYSTEM-to-MECHANISM uplift?
questions_for_control_brain:
  - Add `surgical coordinate effect != natural-state mechanism attribution` as a prospective claim-ceiling guardrail?
  - Keep intervention-realism checks outside the frozen current candidate #35 object?
  - For future mechanism claims, prefer state-region-stratified counterfactual faithfulness over one aggregate intervention score?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1-v1/C19-R1-v2/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - H7 PF-R1 no-rerun/no-rescore boundary and unchanged H7 R5 science under sidecar capability HOLD
  - candidate #34 preserved D34-Q002 result and terminal/no-rescue boundary
  - candidate #35 Discovery/R1 contract and R96 R2 exact non-result binding surface
  - no candidate #35 response/PRE_FORMAL/FORMAL action under current authority
  - no outcome-responsive null-arm/cue/anchor/metric/falsifier rewrite
  - no one-way identity consumption, research merge, immutable-ref mutation, Utility execution, or scheduler change
utility_request_created: null
```

## Run close

Role performed: `LITERATURE_REDUCTION_SCOUT`. Generation: `LIT-20260923T213000+0900-R39-OFFMANIFOLD-INTERVENTIONS-6D2A8C41`. Input generations: Control R43, Evidence Analyst R99, MAIN H7 R5 blocked-sidecar, Fast Forge R97 no-op, prior Literature R38. Genuinely new external information: `true`. Top implication: candidate #35's coordinate-null interventions can show surgical component sensitivity without yet proving the same coordinates are the natural carrier of queue-free memory; a fresh successor should distinguish reachable/on-manifold counterfactuals from intervention artifacts and test ordinary leaky/adaptive causal abstractions. Affected lines: candidate #35 intervention realism/reachability/causal abstraction and future H7 state-conditional abstraction. Utility request: none. Persistence limitation: the exact commit SHA of this append-only history record is generated by this write and cannot be embedded self-referentially inside the record; it must be read from the resulting commit/branch tip immediately after persistence.