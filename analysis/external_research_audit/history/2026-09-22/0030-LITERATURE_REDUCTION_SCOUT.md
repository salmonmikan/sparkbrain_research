# External Literature Reduction Scout — event-driven sparse eligibility localization

- schema_version: `2`
- generation_id: `LIT-20260922T003849+0900-R23-EVENTSPARSE-6F3A91C8`
- produced_at: `2026-09-22T00:38:49+09:00`
- producer_run_id: `external-literature-auto-20260922T003849+0900-R23-6F3A91C8`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260921T213000+0900-R22-SELECTION-AWARE-INFERENCE-7C4A21E9`
- role: `LITERATURE_REDUCTION_SCOUT`
- schedule_slot: `00:30 JST`
- schedule_inference: `false`
- genuinely_new_information: `true`

## Inputs / authoritative state

Repository evidence was re-fetched independently from control-plane mailboxes before interpretation and again before persistence. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; annotated `evidence/*` remains exactly five; tag-form `formal/*`, `sealed/*`, and `freeze/*` remain empty; 13 legacy `freeze/*` branches remain historical source snapshots. PR #148/#149 remain open/unmerged and are not scientific evidence.

Consumed control-plane generations and exact handoff commits:

- Control Brain: `CTRL-20260921T230354+0900-R26-8D4C21A7` @ `0e38771af4dacefab079a9389dece4c6a48f1240`
- Evidence Analyst: `EVA-20260922T002600+0900-R48-8C4A21F6` @ `86290dcbd85a45e89acc56263685cd9338963726`
- MAIN: `MAIN-20260922T001545+0900-PRIMARY-FUNNEL21-HOLD-R46-IDLE-5B7D21C9` @ `c462af2cbea084f4cb1898c7c993c1e93eeccf8e`
- SUB: `SUB-20260921T234211+0900-NOOP-R46NOMECH-7C3A91E5` @ `d6506817c0ad0db0d5817cd26092f6c6f59b4e92`
- prior Literature: `LIT-20260921T213000+0900-R22-SELECTION-AWARE-INFERENCE-7C4A21E9` @ `1c8cb3f86d1ef63a12c2b1b9ff984f717723ec7c`

The material delta is Evidence Analyst R48's fresh SYSTEM Architecture admission `CAND-RESOURCE-SEMANTIC-ACTIVE-WORK-LOCALIZATION-01`. It asks whether a behaviorally consequential plastic/reward workload can localize semantically active work under equal task semantics and prospectively decomposed subsystem counters, without reopening or post-hoc subtracting consumed H5. The candidate has `claim_ceiling=SYSTEM`, `preformal_eligible=false`, cycle count 0, and MAIN is authorized only for static/read-only contract work before any synthetic outcome. No matching fresh research branch exists yet.

Stable source gives the exact reduction surface: every processed spiking event currently calls `_decay_eligibilities()`, which loops over every connection; firing increments eligibility on outgoing edges; reward application again scans all connections and only then skips non-plastic or zero-eligibility edges. This is implementation-faithful current behavior, not a statement that a dense eligibility scan is mechanistically necessary.

## High-value external findings

### 1. Event-driven e-prop is now direct prior art for semantically active eligibility localization

Korcsak-Gorzo et al., *Event-driven eligibility propagation in large sparse networks: efficiency shaped by biological realism* (arXiv:2511.21674, 2025), explicitly translate time-driven e-prop into an event-driven implementation for recurrent spiking networks while retaining continuous dynamics, weight updates, strict locality, and sparse connectivity. They report scalability to millions of neurons without compromising learning performance.

Impact: a future positive SparkBrain result showing that behaviorally consequential eligibility work can be localized/event-triggered would be strongly subsumed by an established ordinary mechanism/implementation family. It would support a SYSTEM efficiency characterization, not mechanism novelty, unless a residual distinction survives an equal-semantics modern event-driven eligibility baseline.

### 2. SparseProp raises the baseline from “dense current implementation” to exact sparse/event-driven algorithms

Engelken, *SparseProp: Efficient Event-Based Simulation and Training of Sparse Recurrent Spiking Neural Networks* (NeurIPS 2023; DOI 10.52202/075280-0161), gives a numerically exact event-based sparse SNN algorithm that avoids iterating through all neurons at every network spike, reducing the stated per-spike forward/backward complexity from `O(N)` to `O(log N)` and demonstrating a >4-orders-of-magnitude speed-up in a million-neuron sparse LIF simulation.

Impact: if the candidate's ordinary comparator is only SparkBrain's dense/global scanning implementation, a large positive reduction may mostly measure data-structure/event-scheduling engineering. A stronger prospective baseline should include an optimized sparse/event-driven representation with equal information and exact task semantics. Any remaining SparkBrain-specific claim must survive that baseline.

### 3. Three-factor delayed credit also has an established event-triggered local implementation family

Quintana et al., *ETLP: Event-based Three-factor Local Plasticity for online learning with neuromorphic hardware* (arXiv:2301.08281, 2023), use a presynaptic spike trace, postsynaptic membrane voltage, and a third factor that also acts as an update trigger. They report competitive accuracy with a clear computational-complexity advantage versus BPTT/eProp and provide an FPGA proof of concept.

Impact: a global/delayed third factor does not imply that every synapse must be visited at every event or time step. Future SparkBrain resource claims should therefore compare global all-edge maintenance with ordinary trigger-driven local-plasticity baselines rather than treat locality itself as a novel consequence of the architecture.

### 4. The decisive discriminator is scaling under exact semantic equivalence, not a one-point sparse-workload win

This is a repository-plus-literature inference. Both the 2025 event-driven e-prop work and SparseProp derive their efficiency from sparse connectivity/event structure. SparkBrain's current global eligibility decay is paid once per processed event across all connections, so the expected advantage of a local/event-driven alternative depends on total edge count, event rate, active/outgoing degree, size/lifetime of the nonzero-eligibility set, and reward frequency.

A fresh contract should therefore bind a scaling/crossover study prospectively rather than report only one sparse workload. Equal semantics should include the same event/reward timing and equivalent resulting weight/prediction trajectory to the precision appropriate for the model; an optimized baseline must retain any history needed to realize delayed reward correctly rather than gain by silently deleting state or information privilege. Operation-count claims should remain separate from wall-clock, memory, cache, or energy claims unless those resource metrics are independently bound.

## Reduction consequence

The active R48 object is a reasonable fresh SYSTEM resource question, but the external bar is now higher than “does localized eligibility beat SparkBrain's current global scan?” Event-driven eligibility propagation, sparse exact simulation/training, and trigger-driven three-factor local plasticity are all established. A positive result is therefore ordinary resource-localization evidence unless it survives equal-semantics optimized event-driven/sparse baselines and exposes a residual SparkBrain-specific scaling or mechanism property.

This literature does not reopen H5. H5 remains immutable and consumed at its registered `FAIL_NO_USEFUL_WORK_REDUCTION`; its role here is only the source of a prospective interpretation question. No PRE_FORMAL or FORMAL uplift is supported.

No Utility request is created. Evidence Analyst has already admitted the fresh object and MAIN owns the static/read-only contract cycle; a parallel implementation request would duplicate active authority and risk contaminating prospective comparator selection.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - CAND_RESOURCE_SEMANTIC_ACTIVE_WORK_LOCALIZATION_01
  - H5_EVENT_ROUTING_WORK_REDUCTION_INTERPRETATION
  - ELIGIBILITY_RESOURCE_ACCOUNTING
  - EVENT_DRIVEN_PLASTICITY_BASELINES
  - PROGRAMME_ARCHITECTURE_EFFICIENCY
novelty_or_reduction_impact: >
  STRONG_ORDINARY_EVENT_DRIVEN_SPARSE_LOCALIZATION_REDUCTION_NO_MECHANISM_NOVELTY_UPLIFT.
  Modern event-driven e-prop, exact sparse event simulation/training, and event-triggered
  three-factor local plasticity already establish strong ordinary baselines for localizing
  semantically active eligibility/credit work. A positive SparkBrain result against its
  current global scan remains SYSTEM/resource evidence unless it survives equal-semantics
  optimized event-driven/sparse comparators and a prospectively fixed scaling study.
audit_classification: null
prospective_baselines_or_discriminators:
  - exact-semantics current/global eligibility implementation versus timestamp/lazy or event-triggered eligibility with an active-eligibility set
  - event-driven e-prop-style baseline retaining all history required for delayed reward
  - SparseProp-style exact sparse/event-driven data-structure baseline rather than only a dense scan
  - ETLP-style third-factor-triggered local update baseline where applicable
  - prospective scaling/crossover sweep over total edges, active degree/event rate, nonzero-eligibility-set size/lifetime, and reward frequency
  - verify equal event/reward timing and equivalent weight/prediction trajectory; do not trade away semantics or information privilege for speed
  - bind operation count separately from wall-clock, memory, cache, and energy claims
questions_for_evidence_analyst:
  - Keep CAND-RESOURCE-SEMANTIC-ACTIVE-WORK-LOCALIZATION-01 SYSTEM-only and treat event-driven e-prop, SparseProp, and ETLP as mandatory ordinary reductions before any uplift?
  - Require equal-semantics comparators to preserve delayed-reward/eligibility state and resulting weight/prediction trajectories, not merely final task accuracy?
  - Require a prospectively fixed scaling/crossover study so a positive result is not overgeneralized from one sparse regime?
questions_for_control_brain:
  - Add modern event-driven eligibility and exact sparse simulation as ordinary efficiency baselines for future resource claims?
  - Keep H5 frozen/consumed and use it only as motivation for the fresh object, never as data to subtract/reweight or reopen?
  - Keep PRE_FORMAL/FORMAL unchanged and cap any current-object positive result at SYSTEM unless a residual survives optimized equal-semantics baselines?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - H5 exact package/STARTED/raw-preserve/evidence chain and canonical FAIL_NO_USEFUL_WORK_REDUCTION
  - CAND-RESOURCE-SEMANTIC-ACTIVE-WORK-LOCALIZATION-01 prospective fresh-object boundary; no post-hoc H5 subtraction, rerun, rescore, relabel, or reopen
  - no synthetic outcome in the current static-contract cycle, no STARTED/TEST, no PRE_FORMAL/FORMAL promotion, no research merge, no immutable-ref mutation, and no scheduler change by this role
utility_request_created: null
```