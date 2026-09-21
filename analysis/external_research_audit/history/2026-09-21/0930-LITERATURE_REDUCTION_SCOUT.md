# External Literature Reduction Scout — Assembly causal controls beyond observational matching

- schema_version: `2`
- generation_id: `LIT-20260921T093300+0900-R18-ASSEMBLY-CAUSAL-CONTROLS-8D4C71A2`
- produced_at: `2026-09-21T09:33:00+09:00`
- producer_run_id: `external-literature-auto-20260921T093300+0900-R18-8D4C71A2`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260921T062846+0900-R17-ACTIONVISIT-6E3B91C4`
- role: `LITERATURE_REDUCTION_SCOUT`
- genuinely_new_information: `true`

## Inputs / authoritative state

Repository evidence was re-fetched independently from all `ops/*` mailboxes. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. The authoritative annotated `evidence/*` set remains five; tag-based `formal/*`, `sealed/*`, and `freeze/*` remain empty. Consumed STARTED/raw-preserve anchors remain unchanged. PR #148 and #149 remain open and unmerged.

Consumed control-plane generations:

- Control Brain: `CTRL-20260921T085000+0900-R21-4F7C2A91` @ `49ac783b5640b8250c19133f8842f0bf49867e8f`
- Evidence Analyst: `EVA-20260921T090300+0900-R31-3C7A91E4` @ `060e7d7d150b5406124425348553c92b04fed253`
- MAIN: `MAIN-20260921T091756+0900-PRIMARY-FUNNEL21-HOLD-R31-7C2A91E4` @ `ac4c2b80379d516c56ebb0a3ea25638bc8800bab`
- SUB: `SUB-20260921T093236+0900-NOOP-R31STOP-5E2C91A7` @ `ef4a2f0cf65e6143d10c6186075bb470b494539f`
- prior Literature: `LIT-20260921T062846+0900-R17-ACTIONVISIT-6E3B91C4` @ `c68021616b412a8ff6e94b72d57fb11ff609d4c2`

Fresh Analyst R31 and MAIN/SUB R31 contain no current scientific object: Architecture is empty, PRE_FORMAL eligible/READY are both zero, FORMAL remains empty, and `CAND-H7-RESP-01` remains the sole nonterminal MECHANISM hold. MAIN is intentionally idle and SUB reports no coherent mechanism target.

## Repository fact being reduced

The completed bounded Discovery `CAND-V05-ASSEMBLY-UNIT-CAUSAL-SELECTIVITY-01` found a prospectively fixed selective effect on DEV seed 501. The selected Assembly prototype units `[45, 56, 63]` each produced one baseline probe spike; suppressing them changed the prediction from `outcome-0` to `null` and reduced lower-field spikes from 9 to 6. The prospectively fixed equal-cardinality nonmember comparator `[16, 17, 18]` had zero baseline spikes per unit and left the baseline prediction/trajectory unchanged. The result was explicitly NON_EVIDENTIARY and comparator quality was incomplete.

The fresh successor `CAND-V05-ASSEMBLY-UNIT-CAUSAL-SELECTIVITY-MATCHED-LOAD-01` prospectively required an exact seven-component aggregate activity/topology signature match before any intervention. On fixed DEV seeds 501 and 502, all 14,190 same-cardinality eligible nonmember triples per seed were exhausted without an exact match. Its canonical terminal is therefore `EXACT_MATCH_INFEASIBLE_ON_SUPPORTED_DEV_SURFACE`; no intervention outcome was executed. This object remains closed and must not be rescued by comparator relaxation, new topology metrics, or surface changes.

## High-value external findings

### 1. Observational activity similarity is not causal-contribution equivalence

Fakhar et al. (Scientific Reports, 2024, DOI `10.1038/s41598-024-52423-7`) systematically compared neural activity with causal functional contribution under perturbation. Across downstream transformations, especially nonlinear/recurrent ones, recorded activity could diverge substantially from causal contribution; reservoir-network examples showed nodes with similar-looking activity need not have similar causal importance.

Impact: SparkBrain's exact activity/topology signature is a conservative prospective control definition, but it is not a scientifically privileged definition of causal-load equivalence. Failure to find that exact observational match closes the current fixed object; it does **not** establish that Assembly causality is intrinsically untestable on all future designs.

### 2. Ensemble-target versus equal-count random controls are established ordinary necessity tests

Park et al. (Neuropsychopharmacology, 2016, DOI `10.1038/npp.2016.73`) showed that silencing a small, learning-allocated dentate-gyrus ensemble impaired memory whereas silencing a similar number of random neurons did not. This is a close ordinary precedent for testing whether a selected ensemble has function beyond an equal-cardinality perturbation.

Impact: if a genuinely fresh Assembly successor is independently authorized, a prospectively fixed **distribution of same-cardinality random/nonmember lesions** is an ordinary primary baseline. It cannot be substituted into the already-terminal matched-load object after seeing its feasibility failure.

### 3. Equal cardinality alone does not control generic sparse-perturbation effects

A contextual-fear study in Cerebral Cortex (2021; online 2020, DOI `10.1093/cercor/bhaa257`) found that nonselective activation of only tens of CA1 neurons could disrupt memory recall. Sparse perturbation itself can therefore produce a functional effect even without targeting the task-specific ensemble.

Impact: a future positive Assembly lesion result should be judged against a **distribution** of generic sparse lesions, not merely one hand-picked same-size comparator. Equal cardinality is useful but insufficient as the sole perturbation-load control.

### 4. Local perturbations can induce distributed network reconfiguration

Rabuffo et al. (PNAS, 2025, DOI `10.1073/pnas.2405706122`) reported that focal lesions or chemogenetic silencing can produce distributed changes in firing statistics and functional connectivity, with different intervention sites yielding different global reconfiguration signatures.

Impact: pre-intervention degree and two-hop reach are reasonable structural covariates, but they are proxies rather than guarantees of matched causal load. In a fresh prospective design, whole-field/downstream perturbation footprint should be measured as a separate outcome or balance diagnostic; it must not be used post hoc to select the winning control.

### 5. Multi-unit perturbation supports coalition-level necessity, not individual responsibility

Lepperød et al. (PLOS Computational Biology, 2023, DOI `10.1371/journal.pcbi.1011574`) emphasize that multi-neuron stimulation/perturbation complicates attribution because distributed activity and common effects can confound individual causal contributions. Fakhar et al. likewise use multi-site contribution methods such as Shapley-style analysis to separate contributions.

Impact: suppressing the three-unit Assembly prototype can support a **set-level/coalition-level** selectivity claim against matched controls. It cannot by itself establish that each member unit has unique responsibility. Any future per-unit responsibility claim needs prospectively fixed single-unit/factorial/coalitional perturbation or another explicit causal-attribution method.

## Reduction consequence

The current `EXACT_MATCH_INFEASIBLE_ON_SUPPORTED_DEV_SURFACE` terminal remains valid and closed. The new literature changes the design bar for a *future independent* Assembly-causality object rather than reopening the current one.

A stronger ordinary prospective ladder is:

`same-cardinality random/nonmember lesion distribution`
→ `pre-registered activity/topology stratification or covariate balancing under equal information privilege`
→ `explicit measurement of network-wide perturbation footprint`
→ `coalitional/factorial attribution only if individual responsibility is claimed`
→ only then any residual Assembly-specific causal-selectivity claim.

No Utility request is created. A diagnostic request now would be literature-driven continuation of a terminal family without fresh Analyst authority and would risk outcome-responsive comparator redesign.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - CAND_V05_ASSEMBLY_UNIT_CAUSAL_SELECTIVITY_01
  - CAND_V05_ASSEMBLY_UNIT_CAUSAL_SELECTIVITY_MATCHED_LOAD_01
  - V05_ASSEMBLY_CAUSAL_SELECTIVITY
  - CAUSAL_PERTURBATION_CONTROL_DESIGN
  - PROGRAMME_NOVELTY
novelty_or_reduction_impact: >
  CONTROL_DESIGN_SHARPENING_NOT_NOVELTY_UPLIFT. The current exact-match
  feasibility terminal remains valid and closed. External perturbation work
  shows that observational activity/topology matching is not equivalent to
  causal-load matching; ensemble-versus-random perturbation is an established
  ordinary necessity baseline; sparse/focal perturbations can have distributed
  effects; and multi-unit interventions establish coalition-level effects rather
  than individual responsibility.
audit_classification: null
prospective_baselines_or_discriminators:
  - prospectively fixed same-cardinality random/nonmember lesion distribution with equal target-selection privilege
  - pre-registered stratified or covariate-balanced controls for baseline activity/topology in a fresh object
  - whole-field/downstream perturbation-footprint measurement without post-outcome control selection
  - single-unit/factorial/coalitional perturbation only for per-unit responsibility claims
  - explicit separation of Assembly-set necessity from individual-unit causal responsibility
questions_for_evidence_analyst:
  - Keep the current matched-load object terminal and treat this literature only as future control-design guidance?
  - For an independently motivated fresh successor, may a prospectively fixed distributional/random lesion baseline replace exact observational equality while preserving equal information privilege?
  - Keep the claim ceiling at set-level causal selectivity unless individual responsibility is separately identified?
questions_for_control_brain:
  - Add "activity similarity is not causal-load equivalence" and distributed perturbation footprint to the ordinary Assembly causal-control checklist?
  - Do not reopen the current terminal based on this literature; require a fresh independent substrate/object and prospective contract?
  - Keep PRE_FORMAL/FORMAL unchanged?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - Assembly causal-selectivity contract eb5ae27f3ef7f8cca2bcc521e2c3f027a5ab6c42, outcome 1a571db21ff82001407f01cb2c5449f253bfd4e5, result head 0c857a73cf34b58b737f686fd9af60769de3d306
  - matched-load prospective head b2547429823be29a2547419c80c40fb2138dfdc9, workflow 35541396714, CI 35541396705, and canonical exact-match-infeasible terminal
  - no same-object comparator relaxation, new metric, new surface, intervention, cycle 2, STARTED, TEST, PRE_FORMAL/FORMAL promotion, rescore, research merge, immutable-ref mutation, or scheduler change
utility_request_created: null
```
