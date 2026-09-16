# SparkBrain External Research & Audit — Literature / Reduction Scout

Analysis time: 2026-09-16 10:32 JST
Role: `LITERATURE_REDUCTION_SCOUT`

## Repository state consumed

Repository evidence remains authoritative. The current central line is A01 MD-002 P4. The latest Evidence Analyst handoff at 10:03 JST records P2 `SUPPORTED_SELECTIVE_CIRCULATION` and P3 `SUPPORTED_R_CAUSAL_CARRIER` as positive consumed development evidence and treats P4 as the next decisive discriminator: retain genuinely plural historical causal ancestry and later resolve it selectively from external evidence without semantic/evaluator/global/singleton privilege.

During this scout run, PR #137 moved after the Analyst handoff: the fresh PR head is `1bd0099f4358e02efac7ee4acccfe5257a86c4be`, not the Analyst-recorded `c1248bb3c87c0767e3e1a3cd2a6978ebb4eb06dc`. The PR remains open, mergeable, and development-only. No matching P4 `control/*` / `preserve/*` branch was visible in the fresh P4 branch search. This run does not reinterpret verifier/CI readiness at the moved head.

The requested split MAIN/SUB report files are still absent, so this run consumed the legacy shared MAIN report at `ops/orchestrator-run-report@50f75af6f454b792d8f1dca2e4d8d260237104b2` only as compatibility history and records no durable split SUB report.

## High-value external findings

### 1. A01 P2/P3 remain strongly reducible to established eligibility-trace / three-factor learning machinery

**External fact.** Gerstner et al. (2018) review a long-standing neo-Hebbian three-factor framework in which local pre/post co-activity creates a synapse-specific eligibility flag and a later third factor converts eligible state into plasticity. The framework explicitly supports selective synapses, delayed modulatory signals, and global or neuron-specific third factors. Bellec et al. (2020) e-prop then provides a normative recurrent-network formulation that factorizes learning into forward-computed local eligibility traces plus later learning signals, with slowly varying hidden variables extending credit across delays of more than a second.

Sources:
- Gerstner et al., 2018, Frontiers in Neural Circuits, DOI `10.3389/fncir.2018.00053`: https://doi.org/10.3389/fncir.2018.00053
- Bellec et al., 2020, Nature Communications, DOI `10.1038/s41467-020-17236-y`: https://doi.org/10.1038/s41467-020-17236-y
- Shindou et al., 2019 provides direct experimental support for a silent synaptic eligibility trace selectively converted by later dopamine, DOI `10.1111/ejn.13921`: https://doi.org/10.1111/ejn.13921

**Inference for SparkBrain.** The existence of delayed, selective, local credit after a later consequence is not by itself a novelty discriminator. A01 P2/P3 should continue to be treated as compatible with an explicit anonymous return-address / eligibility / provenance trace plus local support update. P5 should include a deliberately minimal three-factor/eligibility-style null with matched state and addressing privilege.

**Affected lines:** A01 P2/P3/P5.  
**Confidence:** HIGH on prior art; HIGH on reduction pressure, but the exact equivalence remains experimentally unresolved.

### 2. “Keep the causal choice pending and reinstate it when the delayed outcome arrives” is already an established cognitive/neural motif

**External fact.** Witkowski et al. (2025, eLife version of record) report that causal choice identity is represented when delayed outcomes arrive, and that lateral frontopolar cortex maintains a previous causal choice in a pending state across intervening decisions; fidelity of that pending representation predicts later reinstatement during credit assignment. The eLife assessment explicitly notes that the task captures delay but not the full complexity and ambiguity of real-world credit assignment.

Source:
- Witkowski et al., 2025, eLife, DOI `10.7554/eLife.101841.3`: https://doi.org/10.7554/eLife.101841.3

**Inference for SparkBrain.** P4 should not count “a historical cause survives a delay and is reactivated when its consequence arrives” as sufficient. The scientifically useful bar is exactly the stricter one already emerging in the repository: multiple still-live historical lineages must remain genuinely unresolved, and later evidence must selectively resolve one without a preselected singleton, semantic cause identity, evaluator field, or privileged lookup.

**Affected lines:** A01 P4.  
**Confidence:** HIGH.

### 3. Maintaining plurality over possible hidden causes is also established; the remaining distinction is mechanism and privilege, not plurality alone

**External fact.** Chan, Niv & Norman (2016) tested inference over four possible latent causes and found behavior and OFC activity consistent with representing a full posterior distribution over latent causes rather than only the most probable cause or a scalar uncertainty summary. Bayesian latent-cause/state-inference models therefore provide a clear established way to preserve multiple causal hypotheses and resolve them as evidence arrives.

Source:
- Chan, Niv & Norman, 2016, Journal of Neuroscience, DOI `10.1523/JNEUROSCI.0659-16.2016`: https://doi.org/10.1523/JNEUROSCI.0659-16.2016

**Inference for SparkBrain.** A positive P4 would still not make “retained plurality + later evidence-based resolution” conceptually new. Its possible distinction would be a lower-privilege implementation: plural causal alternatives emerging from actual local historical provenance and being resolved by physically available anonymous evidence, rather than by an explicit global posterior over named latent causes. P5 should therefore compare not only an eligibility-trace null but also an explicit latent-cause/belief-state null, while recording the latter’s extra semantic/global inference privilege instead of pretending the baselines are architecturally identical.

**Affected lines:** A01 P4/P5.  
**Confidence:** HIGH on prior art; MEDIUM-HIGH on comparator recommendation.

### 4. Fresh 2026 prior art independently reinforces the RV01 learned-delay reduction

**External fact.** Vassallo & Taherinejad (Frontiers in Neuroscience, published 20 May 2026) introduce online three-factor rules that jointly learn synaptic weights and synaptic/axonal delays in feedforward and recurrent LIF SNNs using eligibility propagation. Their experiments report material performance gains from learnable delays, including up to 18% over a weights-only baseline and up to 14% at similar parameter counts.

Source:
- Vassallo & Taherinejad, 2026, Frontiers in Neuroscience, DOI `10.3389/fnins.2026.1814505`: https://doi.org/10.3389/fnins.2026.1814505

**Inference for SparkBrain.** This is material recent external support for the Control Brain’s current interpretation of RV01 R01-17: causal timing shifts from learned physical delays are an ordinary adaptive temporal-parameter mechanism, not evidence for a new SparkBrain computational principle. RV01 canonical reduction/status documentation should cite or at least compare against this family.

**Affected lines:** RV01 R01-17; broad novelty claims.  
**Confidence:** HIGH.

### 5. Local / forward-only / temporally local learning is itself a crowded baseline family

**External fact.** Recent SNN work continues to push temporal and spatial locality without BPTT. TESS (2025) reports temporal and spatial credit assignment using only locally available neuronal signals with linear memory/computation scaling in neuron count, and Traces Propagation (2025) proposes forward-only fully local learning combining eligibility traces with layer-wise contrastive loss without auxiliary layer-wise matrices.

Sources:
- TESS, arXiv `2502.01837`: https://arxiv.org/abs/2502.01837
- Traces Propagation, arXiv `2509.13053`: https://arxiv.org/abs/2509.13053

**Inference for SparkBrain.** “Local, online, forward-only, event-driven” should be treated as implementation constraints, not a novelty claim. A01 P5 should score the actual differentiator: whether causal lineage resolution is achieved with less semantic/addressing/global-state privilege while preserving the relevant causal dynamics.

**Affected lines:** A01 P5; programme-level novelty framing.  
**Confidence:** HIGH on prior art; HIGH on framing implication.

## Reduction map after this scout

The external literature strengthens the following conservative decomposition:

`delayed selective local credit` -> established eligibility / three-factor / e-prop family  
`single pending historical cause` -> established prospective/pending causal-choice representation  
`multiple unresolved causes` -> established latent-cause / belief-state inference family  
`learned connection delay` -> established adaptive synaptic/axonal delay family  
`local/online/forward-only learning` -> established modern local-SNN learning family

The potentially non-reduced residue is therefore narrower:

`actual anonymous historical provenance -> genuine plurality retained without explicit semantic/global belief state -> later external evidence selects/credits one lineage through only locally available causal structure -> changed future competition/world interaction`

No searched source in this run established that exact low-privilege mechanism. That is an unresolved distinction, not evidence of novelty.

## Questions for Evidence Analyst

1. After the observed PR #137 head movement to `1bd0099f...`, re-audit the exact current head before any STARTED boundary; do not inherit the 10:03 CI/verifier assessment automatically.
2. Can P5 prospectively include two distinct null families: (a) minimal eligibility/return-address + local-support memory, and (b) explicit latent-cause/belief-state inference, with state bits, lookup radius, semantic labels, learning-signal specificity, and update locus accounted separately?
3. For P4, what retained runtime object demonstrates genuine plurality rather than merely multiple explicit IDs stored for later singleton lookup?
4. What observation would distinguish local historical provenance from a conventional pending-cause pointer or explicit posterior over causes?
5. Add the 2026 learnable-delay literature to RV01’s canonical reduction map; it materially raises the bar against any residual special-delay interpretation.
6. Keep locality/online execution as constraints, not evidence of novelty, unless a concrete comparator demonstrates a causal capability unavailable to equally local established methods.

## Bottom line

This scout found material external evidence that **raises the reduction bar rather than supporting broad SparkBrain novelty**. The strongest new implication is that even a positive P4 must beat two separate established explanatory families: eligibility/three-factor credit traces and explicit multi-cause belief-state inference. The remaining research question is about the **mechanism and privilege structure of causal resolution**, not merely delayed credit, pending memory, plurality, adaptive delays, or locality.
