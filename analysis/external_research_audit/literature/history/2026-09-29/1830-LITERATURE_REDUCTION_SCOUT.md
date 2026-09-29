# External Literature Reduction Scout — typed ascending signals and topology prior art

- schema_version: `2`
- generation_id: `LIT-20260929T183113+0900-R50-ASCENDING-SIGNAL-TYPING-TOPOLOGY-PRIORART`
- produced_at: `2026-09-29T18:31:13+09:00`
- role: `LITERATURE_REDUCTION_SCOUT`
- status: `NON_EVIDENTIARY / NONCANONICAL`
- genuinely_new_information: `true`
- new_scientific_result: `false`

Freshness: main policy was re-fetched at `main@59fc994b39d0ba02682e972161bb46801592d25b`. Human Directive index remains `ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d` / blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`, unchanged from R49. Current durable inputs are Control R123 and Evidence Analyst R170. M1-002 remains the critical path; SB003 remains `ALLOCATED_CONDITIONAL_INACTIVE`. Canonical science remains 35/35 terminal, 0 active, 0 queued, 8 consumed FORMAL identities.

## Findings

1. **Jin et al. 2026, FlyGM / arXiv:2602.17997 — direct topology-comparator prior art**
   - Classes: `NOVELTY_REDUCTION`, `SYSTEM_LEVEL_COMPARATOR`, `DESIGN_PRIMITIVE`.
   - The preprint instantiates the adult Drosophila connectome as a graph policy and compares it with degree-preserving rewired, random-graph and MLP controllers under a shared learning pipeline, reporting better learning/performance for the connectomic graph.
   - Function supplied: a directly relevant external comparator ladder for structured/connectomic topology claims.
   - Limitation: preprint; whole-connectome learned controller, different scale/training/resource regime from FLY-0; the comparison does not establish SparkBrain biological fidelity or topology superiority.
   - Consequence: a future SparkBrain scientific claim of merely “structured topology beats degree-preserving rewired/random in embodied fly control” would be strongly reduced by existing prior art and needs a more specific prospective discriminator.

2. **Cheong et al. 2024, Current Biology, doi:10.1016/j.cub.2024.01.071 — ascending does not mean realized outcome**
   - Classes: `NOVELTY_REDUCTION`, `DESIGN_PRIMITIVE`.
   - Ascending histaminergic neurons are driven by descending motor commands and activate before wing motion, functioning as predictive corollary-discharge signals rather than sensory consequences of completed movement.
   - Function supplied: a reason to type ascending signals by provenance/semantics rather than treating every ascending frame as realized-world evidence.
   - Limitation: a specific flight circuit; it does not imply SparkBrain receipt IDs, authority tokens or transaction semantics are biologically grounded.

3. **Chen et al. 2023, Nature Neuroscience, doi:10.1038/s41593-023-01281-z — ascending populations carry differentiated behavioral-state channels**
   - Classes: `DESIGN_PRIMITIVE`, `NOVELTY_REDUCTION`.
   - Hundreds of ascending neurons encode self-motion and discrete actions and target different integrative sensory/action-selection brain regions.
   - Function supplied: typed self-motion/action-state channels and destination-specific routing as an established biological design primitive.
   - Limitation: population coding of behavioral state is not an exact event-sourcing or outcome-receipt protocol and does not establish whole-system equivalence.

4. **Dallmann et al. 2025, Nature, doi:10.1038/s41586-025-09554-2 — feedback masking is channel-specific**
   - Classes: `DESIGN_PRIMITIVE`, `NO_MATERIAL_CHANGE`.
   - During walking/grooming, movement-encoding leg proprioceptor output is selectively suppressed while position-encoding proprioceptors remain active; descending pathways drive the context-specific gating circuit.
   - Function supplied: explicit signal class plus mask/gate reason is preferable to a single global “feedback available” bit.
   - Limitation: selective proprioceptive gating does not imply masked data are globally invalid or dictate SparkBrain software metadata.

5. **Karashchuk et al. 2024/2025, eLife 99005 — delay is a causal control variable, not bookkeeping**
   - Classes: `DESIGN_PRIMITIVE`, `SYSTEM_LEVEL_COMPARATOR`, `NO_MATERIAL_CHANGE`.
   - A layered fly-walking model loses perturbation robustness as sensorimotor delays exceed physiological ranges, while local feedback/control supports robust walking within bounded delays.
   - Function supplied: keep sensory/motor delay budgets explicit and matched when comparing FLY-0 topology/controller variants.
   - Limitation: this is a computational walking model, not proof that any SparkBrain topology is biologically necessary or superior.

## Handoff

Literature R50 sharpens, but does not expand, current R170 authority.

For future R22-style outcome reconciliation, distinguish at least:
`PREDICTIVE_MOTOR_COPY | REALIZED_BEHAVIORAL_STATE | EXTERNAL/REAFFERENT_OUTCOME | MASKED/GATED_FEEDBACK`.
An ascending message must not be promoted to realized-outcome evidence solely because its direction is ascending.

For FLY-0/SB003 comparisons, FlyGM is now an explicit external prior-art comparator: structured-vs-rewired-vs-random superiority after learning is not a clean novelty claim by itself. Preserve the current nested matched-null strategy, and keep delay/training/resource differences explicit before any topology-specific science.

No M1 stop, no additional review gate, no SB003 activation-condition change, no Revisit trigger, no scientific execution. The R170 narrow observer remains an optional B/C engineering input; the full R22 receipt path remains separately scoped and unverified. Scientific credit remains 0.
