# External Literature Reduction Scout — FLY-0 distributed sensorimotor control and comparator ladder

- schema_version: `2`
- role: `LITERATURE_REDUCTION_SCOUT`
- generation_id: `LIT-20260928T063000+0900-R46-FLY0-DISTRIBUTED-CONTROL-B7D3C4A1`
- produced_at: `2026-09-28T06:30:00+09:00`
- producer_run_id: `external-literature-auto-LIT-20260928T063000+0900-R46-FLY0-DISTRIBUTED-CONTROL-B7D3C4A1`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_NON_EVIDENTIARY_NONCANONICAL_HANDOFF`
- supersedes_generation_id: `LIT-20260927T062709+0900-R45-RV02-RD006-REACHABILITY-91C4A8E2`
- genuinely_new_information: `true`
- new_sparkbrain_scientific_result: `false`

## Scope and freshness

The 06:30 JST slot resolved to exactly one internal role: `LITERATURE_REDUCTION_SCOUT`. The current Human Directive index is `ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d`, index blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`. Relative to Literature R45, `HUMAN-20260928-001` and `HUMAN-20260928-002` are newly applicable material directives. This run interprets them as requiring parallel prior-art and comparator support for completed M1 and isolated FLY-0 without creating a review gate or scientific credit.

Control R103 records M1 built and bounded-functionally verified at exact head `512f21a6134b5d68351e33a7c6eecb8fa3e4550c`, with fresh Analyst reconciliation pending before PR/merge. FLY-0 is an isolated NON_EVIDENTIARY/NONCANONICAL Forge prototype at `c9538544b04108a950e841cbc90b626259d7e3ff`, not an M1 dependency and without SB003 allocation. Its structured, degree-preserving rewired and random variants match the declared static resource envelope; observed fired-event totals differ.

## High-value literature findings

### 1. Whole-CNS fly control is distributed: local sensory-effector loops with long-range supervision

**Classification:** `NOVELTY_REDUCTION`, `DESIGN_PRIMITIVE`, `SYSTEM_LEVEL_COMPARATOR`.

Bates et al. (2026) report the first adult fly connectome uniting brain and ventral nerve cord. Their influence analysis finds that effectors are primarily influenced by local sensory cells from the same body part, forming local feedback loops; ascending and descending circuits link these loops into behavior-centric modules, while learning/navigation regions act as supervisors.

**Function supplied:** an established architecture for fast local embodied control coordinated by slower or higher-level ascending/descending pathways.

**Known limitations:** the result is anatomical plus model-based influence analysis, not proof that any reduced synthetic topology reproduces fly dynamics or behavior. The full connectome has orders of magnitude more structure than FLY-0.

**Must not imply:** a local loop plus descending modulation is not novel by itself, and FLY-0 cannot be called a fly-brain reproduction or biologically equivalent system.

**SparkBrain impact:** HUMAN-20260928-002's preferred split—local micro-control below, SparkBrain state/goal modulation above—is strongly supported as an engineering design primitive. A future SB003 should add an explicit ascending state-feedback surface as well as descending modulation; this is a prospective integration suggestion, not a blocker for the current Forge fixture.

Source: Bates et al., *Nature* 656, 957–970 (2026), DOI: https://doi.org/10.1038/s41586-026-10735-w

### 2. Connectome-constrained LIF is already a direct sensorimotor comparator

**Classification:** `NOVELTY_REDUCTION`, `DESIGN_PRIMITIVE`, `SYSTEM_LEVEL_COMPARATOR`.

Shiu et al. (2024) constructed a whole-brain leaky integrate-and-fire model from adult Drosophila connectivity and neurotransmitter identity and used it to describe sensorimotor transformations for feeding and grooming.

**Function supplied:** a known connectome-constrained spiking reference architecture mapping sensory activation through recurrent network dynamics to descending or motor output.

**Known limitations:** it remains a simplified model with explicit assumptions about neuron dynamics, signs, inputs and readouts; connectome-derived success does not establish biological completeness, general behavior or a unique causal role for topology.

**Must not imply:** successful event propagation in FLY-0 is not a new fly-inspired computational principle, nor does it show superiority over a standard LIF implementation.

**SparkBrain impact:** if FLY-0 is ever promoted to an evidence-bearing topology question, a reduced connectome-constrained LIF replacement is a stronger system-level comparator than random topology alone. It is not required to retain or integrate the present noncanonical engineering primitive.

Source: Shiu et al., *Nature* (2024), DOI: https://doi.org/10.1038/s41586-024-07763-9

### 3. Premotor organization is modular and body-part specific, not one generic recurrent motif

**Classification:** `DESIGN_PRIMITIVE`, `NOVELTY_REDUCTION`, `NO_MATERIAL_CHANGE`.

Lesser et al. (2024) find that leg and wing premotor networks form modules linking motor neurons with related muscle functions. Most motor-neuron input is local; leg modules show synaptic organization supporting hierarchical recruitment, whereas wing steering networks use a different organization consistent with their biomechanics.

**Function supplied:** local premotor modules, hierarchical recruitment and body-part-specific controller specialization.

**Known limitations:** connectomic wiring does not by itself establish dynamic control, and leg/wing differences argue against treating one motif as a universal fly controller.

**Must not imply:** FLY-0's bilateral role graph is not a faithful substitute for fly premotor circuitry merely because it has sensory, local, motor and modulation roles.

**SparkBrain impact:** a future SB003 should prefer plural local modules with an explicit action/body mapping and retain a simple generic modular-controller replacement. This refines later integration design without invalidating the current topology probe.

Source: Lesser et al., *Nature* 631, 369–377 (2024), DOI: https://doi.org/10.1038/s41586-024-07600-z

### 4. A degree-preserving rewire is necessary but not the full topology null ladder

**Classification:** `SYSTEM_LEVEL_COMPARATOR`, `DESIGN_PRIMITIVE`.

Lin et al. (2024) compare the adult fly connectome against several null families rather than one rewire: directed Erdős–Rényi variants, degree-preserving configuration models, spatial nulls and a neuropil-block model that preserves degree sequences and inter/intra-neuropil connection structure. Roberts and Coolen (2012) further show that naive accept-all directed edge swaps can sample degree-preserving graphs with bias; their detailed-balance construction targets a uniform ensemble while conserving every in/out degree.

**Function supplied:** a prospective comparator ladder and an unbiased ensemble-generation criterion for directed topology claims.

**Known limitations:** richer nulls answer different questions and can over-constrain away the effect of interest; anatomy-only nulls do not equate dynamics, activity exposure or task performance.

**Must not imply:** FLY-0's single deterministic degree-preserving control is not invalid for bounded engineering, but it is insufficient for a scientific claim of topology-specific advantage.

**SparkBrain impact:** any fresh scientific successor should use multiple independent rewires and report the distribution, preserve role blocks/signs/delays as appropriate, add a block/spatially constrained null when biological topology is claimed, and report fired-event/activity exposure alongside selectivity. Activity counts must not be relabeled as energy efficiency.

Sources: Lin et al., *Nature* 634, 153–165 (2024), DOI: https://doi.org/10.1038/s41586-024-07968-y; Roberts & Coolen, *Physical Review E* 85, 046103 (2012), DOI: https://doi.org/10.1103/PhysRevE.85.046103

## Novelty and Revisit disposition

- No Revisit trigger fires.
- M1 remains NON_EVIDENTIARY_BUILD with no scientific-credit transfer.
- FLY-0 remains NON_EVIDENTIARY/NONCANONICAL; no SB003 identity is allocated here.
- Existing fly control literature materially reduces any novelty claim for local loops, descending modulation, connectome-constrained spiking and modular premotor organization.
- The literature does not establish whole-system equivalence between FLY-0, M1 or SparkBrain and a fly nervous system.
- No candidate, PRE_FORMAL object, FORMAL step, result-bearing dispatch or scientific claim is created.

## Prospective design and comparator handoff

1. Retain FLY-0 as a useful bounded engineering fixture; do not stop M1 reconciliation or ordinary integration.
2. If SB003 is later allocated, expose both descending modulation and ascending local-state feedback, with plural local modules and explicit world/action continuity.
3. Add component replacements prospectively: a simple modular controller and a reduced connectome-constrained LIF controller.
4. Add interaction ablations prospectively: remove descending modulation, ascending feedback, or local recurrence separately.
5. For any scientific topology claim, use an ensemble of unbiased degree-preserving role-block rewires plus a suitable block/spatial null, and separate topology effect from activity exposure.
6. Keep COMPONENT_FUNCTION, SYSTEM_BUILD, COMPOSITION_CONTRIBUTION and SCIENTIFIC_NOVELTY as separate conclusions.

## Machine-usable knowledge-flow contract

- affected_lines: `M1_SYSTEM_BUILD; FLY0_FORGE; FUTURE_SB003; FUTURE_FLYLIKE_SCIENTIFIC_SUCCESSOR`
- novelty_or_reduction_impact: `LOCAL_SENSORIMOTOR_LOOPS_DESCENDING_SUPERVISION_CONNECTOME_LIF_AND_MODULAR_PREMOTOR_CONTROL_ARE_ESTABLISHED; FLY0_ENGINEERING_VALUE_RETAINED; BIOLOGICAL_FIDELITY_AND_TOPOLOGY_NOVELTY_NOT_ESTABLISHED`
- revisit_proposal/status: `null / NO_NEW_TRIGGER`
- audit_classification: `null`
- must_not_change_frozen_or_consumed: `all consumed/formal/evidence identities; M1 exact-head claim boundary; FLY0 noncanonical status; no SB003 allocation by Literature`
- scientific_mutations: `0`

## Run close

Exactly one internal role was performed: `LITERATURE_REDUCTION_SCOUT`. Four material findings were produced. Genuinely new information relative to durable Literature R45: `true`. New SparkBrain scientific result: `false`.
