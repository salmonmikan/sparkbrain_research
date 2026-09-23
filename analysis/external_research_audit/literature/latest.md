# External Literature Reduction Scout — silent synaptic memory and delayed-credit baselines

- schema_version: `2`
- generation_id: `LIT-20260924T002755+0900-R40-SILENT-SYNAPTIC-CREDIT-9C4E2A71`
- produced_at: `2026-09-24T00:27:55+09:00`
- producer_run_id: `external-literature-auto-LIT-20260924T002755+0900-R40-SILENT-SYNAPTIC-CREDIT-9C4E2A71`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260923T213000+0900-R39-OFFMANIFOLD-INTERVENTIONS-6D2A8C41`
- role: `LITERATURE_REDUCTION_SCOUT`
- schedule_slot: `00:30 JST`
- schedule_inference: `false`
- genuinely_new_information: `true`

## Inputs / authoritative state

Repository evidence was fetched independently of the `ops/*` mailboxes. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. The authoritative tag set remains five `evidence/*` annotated tags; tag-form `formal/*`, `sealed/*`, `freeze/*`, and `immutable/*` remain absent, while legacy `freeze/*` branches were inspected separately. Candidate #34 remains preserved/terminal and is not reopened. Open PR #149 is scheduler-registry tooling only and is not scientific state.

Candidate #35 changed materially since Literature R39: its prospectively fixed five-arm Architecture batch was executed exactly once under R100 development authority, raw was preserved before interpretation at `raw/cand35-r100-onebatch-20260923@afe4b7ad0f908f3b01eca9e391a2b05cb3be9a7a`, and Evidence Analyst R101 has now canonically closed the current object as `TERMINAL_FOR_CURRENT_OBJECT` with bounded interpretation `NO_MEASURED_PRIMING_EFFECT_ON_FROZEN_OUTPUT_SURFACE`. `SHAM_STATE`, `POTENTIAL_NULL`, `ADAPTATION_NULL`, and `JOINT_SUBTHRESHOLD_NULL` all produced the same measured two-spike `[6,7]` cascade/no-ignition surface; `DELAYED_SHAM_32MS` produced the same structure shifted in time. This is a genuine new SparkBrain development result but remains unscored, non-PRE_FORMAL, non-FORMAL, and carries zero confirmatory credit.

The exact candidate #35 scientific source explicitly disables field weight learning, delay learning, and reward modulation for this object. Therefore the current negative result is properly scoped to its frozen neuronal subthreshold coordinates and output surface; it did not test a transient synaptic-plasticity memory carrier.

Consumed control-plane generations:
- Control Brain: `CTRL-20260923T225500+0900-R44-C8F41D72` @ `3c46617fba123704297d880a748c305c16a7dd01`
- Evidence Analyst: `EVA-20260924T000324+0900-R101-CAND35-POSTEXPOSURE` @ `e50e0a91e25f2457d0b7152900a48cbdc5006485`
- MAIN designated latest: `MAIN-20260923T235628+0900-RELAY-CAND35-R100-ONEBATCH-EXPOSED-WAITING-ANALYST` @ mailbox `21a8ee7b0ae85df57a0a35b70ad726e45252e259`
- Fast Forge designated latest: `FORGE-20260923T233625+0900-V05-CREDIT-LOCALITY-R100` @ mailbox `21a8ee7b0ae85df57a0a35b70ad726e45252e259`
- Prior Literature: `LIT-20260923T213000+0900-R39-OFFMANIFOLD-INTERVENTIONS-6D2A8C41` @ `741becd60d3e7dc8f97cedf1347c42c769092011`

## High-value new findings

### 1. The candidate #35 null result closes its frozen neuronal subthreshold surface, not the broader class of activity-silent memory

A 2026 peer-reviewed Physical Review E study revisits activity-silent working memory sustained by short-term synaptic facilitation and finds the mechanism remains robust even after adding synaptic heterogeneity. The paper explicitly treats short-term synaptic facilitation as a carrier of memory without persistent neural activity.

Source:
- Tiddia et al., *Short-term plasticity-based working memory spiking model is resilient to synaptic heterogeneity*, Phys. Rev. E 114, 014409 (published 22 July 2026), DOI `10.1103/zcmm-3cgh`, https://journals.aps.org/pre/abstract/10.1103/zcmm-3cgh

A recent 2026 preprint independently sharpens the same point: after spiking activity becomes fully silent, the residual transient synaptic configuration can still predict whether activity later regenerates.

Source:
- Khanjanianpak & Valiadeh, *Activity Regeneration from Silent States in Neuronal Networks with Transient Synaptic Memory*, arXiv:2607.14000 (2026), https://arxiv.org/abs/2607.14000

**Impact.** R101's current #35 conclusion is appropriately narrow and should remain terminal for the current object. The unchanged output after `potential`/`adaptation` nulling does not support a broader claim that queue-free or activity-silent memory mechanisms are generally absent. If SparkBrain later makes a broader persistent/activity-silent-memory claim, a transient-synaptic-state/STP comparator is now an especially direct ordinary baseline. This does not retrofit #35: its frozen source deliberately disabled field learning and did not instantiate this comparator family.

### 2. The current v0.5 reward/eligibility track is weaker than the ordinary delayed-reward three-factor baseline

Fast Forge R100 independently found that v0.5 stores per-edge eligibility but a reward arriving after an episode does not by itself consume the stored trace: `apply()` skips an edge unless the current spike batch again contains both pre- and postsynaptic spikes. This exact source behavior is consistent with the current `V05PlasticityController`: reward is one scalar trace, stored eligibility is decayed, and weight updates occur only inside the branch requiring current pre/post events.

Foundational three-factor learning is stronger. Izhikevich's distal-reward model uses a slowly decaying synaptic eligibility/tag set by earlier spike timing so a dopamine/reward signal arriving seconds later can reinforce the earlier responsible synapses. Gerstner et al.'s review formalizes the same neoHebbian pattern: pre/post activity creates an eligibility trace and a third factor arriving while that trace persists triggers plasticity.

Sources:
- Izhikevich, *Solving the distal reward problem through linkage of STDP and dopamine signaling*, Cerebral Cortex 17(10), 2007, DOI `10.1093/cercor/bhl152`, https://pubmed.ncbi.nlm.nih.gov/17220510/
- Gerstner et al., *Eligibility Traces and Plasticity on Behavioral Time Scales: Experimental Support of NeoHebbian Three-Factor Learning Rules*, Frontiers in Neural Circuits 12:53 (2018), DOI `10.3389/fncir.2018.00053`, https://pubmed.ncbi.nlm.nih.gov/30108488/

**Impact.** The Forge dead-end should not be read as evidence that eligibility traces cannot solve delayed credit. It shows that SparkBrain's current optional v0.5 implementation does not implement the stronger ordinary reward-arrival-on-existing-eligibility mechanism. Any future delayed-credit novelty claim must first beat a correctly privilege-matched three-factor baseline in which a delayed third factor can act on a previously established trace without requiring a new qualifying spike pair.

### 3. Temporal eligibility and spatial/local responsibility are distinct problems

e-prop factorizes online recurrent credit into a synapse-local eligibility trace and a learning signal for the postsynaptic neuron/population. The work explicitly contrasts neuron-specific learning signals with global learning-signal baselines and shows that slowly varying hidden variables can carry eligibility over long temporal gaps.

Source:
- Bellec et al., *A solution to the learning dilemma for recurrent networks of spiking neurons*, Nature Communications 11, 3625 (2020), DOI `10.1038/s41467-020-17236-y`, https://www.nature.com/articles/s41467-020-17236-y

**Impact.** A global scalar reward multiplied by per-edge eligibility is a legitimate ordinary three-factor baseline and can solve limited distal-reward problems through synapse-specific tags; however, it is not by itself evidence for a richer native notion of causal lineage or local responsibility. A future SparkBrain responsibility claim should distinguish (a) temporal persistence of eligibility from (b) how responsibility/error information is spatially assigned among simultaneously eligible units/edges. A neuron-/population-specific learning-signal comparator such as e-prop is therefore a stronger reduction ceiling than global reward-modulated STDP alone.

### 4. The 2026 novelty bar now includes fully local forward credit and online joint delay learning

Recent work has pushed eligibility-based local learning beyond the older STDP baseline. Traces Propagation combines eligibility traces with a layer-wise contrastive signal for forward-only local learning and explicitly targets both temporal and spatial credit. Separately, a 2026 peer-reviewed three-factor SNN rule learns synaptic weights and axonal/synaptic delays online using eligibility traces plus a top-down error signal, reporting improvements over weights-only training.

Sources:
- Pes et al., *Traces propagation: memory-efficient and scalable forward-only learning in spiking neural networks*, Neuromorphic Computing and Engineering 6(1), 014002 (2026), DOI `10.1088/2634-4386/ae2ef9`
- Vassallo & Taherinejad, *Three factor delay learning rules for spiking neural networks*, Frontiers in Neuroscience (2026), DOI `10.3389/fnins.2026.1814505`, https://pubmed.ncbi.nlm.nih.gov/42246032/

**Impact.** Future SparkBrain claims that combine locality, delayed credit, and learned transmission timing should not use plain STDP as the strongest prior-art comparator. The prospective bar should include modern local eligibility methods and joint weight-delay three-factor learning. This is especially relevant if a future line attempts to connect local responsibility with the delay-sensitive temporal dynamics explored elsewhere in SparkBrain.

## Synthesis

This run adds two distinct boundaries after the new #35 development result. First, the #35 negative result is scientifically useful but narrow: it closes the frozen potential/adaptation priming surface and should not be generalized to all activity-silent memory, because transient synaptic-state mechanisms are established ordinary alternatives. Second, the newly explored v0.5 eligibility/reward path is below, not above, the standard delayed-credit baseline: ordinary three-factor learning already supports delayed third-factor action on stored eligibility, while modern e-prop/Traces-Propagation style methods make temporal eligibility and spatial responsibility explicit separate components.

Prospective reduction ladders therefore become:

`queue-free/activity-silent claim -> neuronal potential/adaptation -> transient synaptic/STP state -> other ordinary slow hidden variables -> only then a broader native residual`

and

`local spike correlation -> stored eligibility -> delayed third-factor action on prior eligibility -> neuron/population-specific spatial learning signal -> modern local forward / joint weight-delay baseline -> only then richer causal-responsibility novelty`.

No current object should be rewritten. Candidate #35 remains terminal for its current object and zero-credit; Candidate #34 remains terminal/reducible; H7 remains on the pre-identity integrity-capability hold. No Utility request is created because there is no admitted fresh candidate requiring implementation, and injecting these baselines into closed/frozen objects would be outcome-responsive redesign.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - CAND35_ACTIVITY_SILENT_MEMORY_SCOPE
  - CAND35_TRANSIENT_SYNAPTIC_STATE_BASELINE
  - V05_DELAYED_CREDIT_THREE_FACTOR_REDUCTION
  - V05_LOCAL_RESPONSIBILITY_SPATIAL_CREDIT
  - FUTURE_CREDIT_ASSIGNMENT_MECHANISM_ADMISSION
  - FUTURE_DELAY_LEARNING_MECHANISM_ADMISSION
  - PROGRAMME_NOVELTY
novelty_or_reduction_impact: >
  CAND35_NEGATIVE_CLOSES_ONLY_ITS_FROZEN_NEURONAL_SUBTHRESHOLD_SURFACE;
  BROADER_ACTIVITY_SILENT_MEMORY_HAS_STRONG_TRANSIENT_SYNAPTIC_PRIOR_ART.
  THE_CURRENT_V05_ELIGIBILITY_REWARD_PATH_IS_WEAKER_THAN_STANDARD_DELAYED_THREE_FACTOR
  CREDIT, AND TEMPORAL_ELIGIBILITY_MUST_BE_DISTINGUISHED_FROM_SPATIAL_RESPONSIBILITY.
audit_classification: null
prospective_baselines_or_discriminators:
  - transient synaptic facilitation / short-term synaptic-state comparator for any broad queue-free or activity-silent-memory successor
  - delayed third-factor baseline where reward/error acts on already-established eligibility without requiring a new spike pair
  - neuron/population-specific learning-signal comparator such as e-prop against global scalar reward
  - modern fully local temporal-plus-spatial credit baseline such as Traces Propagation
  - online joint weight-and-delay three-factor baseline for any learned-delay responsibility claim
questions_for_evidence_analyst:
  - Keep candidate #35 terminal for the current object while explicitly preventing its negative result from being generalized to all activity-silent memory carriers?
  - For any independently motivated fresh silent-memory successor, require a carrier inventory that includes transient synaptic/STP state before mechanism uplift?
  - For any future delayed-credit/responsibility candidate, require reward/error arrival to act on prior eligibility and separately test temporal eligibility versus spatial responsibility assignment?
questions_for_control_brain:
  - Add `negative neuronal-state null != absence of activity-silent memory` as a prospective claim-ceiling guardrail?
  - Add `eligibility persistence != local responsibility assignment` and require a three-factor/e-prop-class ordinary reduction before richer credit-line claims?
  - Keep all of these baselines prospective and outside terminal #34/#35 and held H7 objects?
must_not_change_frozen_or_consumed:
  - all seven officially consumed FORMAL identities and all authoritative evidence tags
  - H7 PF-R1 no-rerun/no-rescore boundary and unchanged H7 R5 science under the current pre-identity integrity-capability hold
  - candidate #34 preserved D34-Q002 result and terminal/no-rescue boundary
  - candidate #35 raw R100 five-arm batch at raw/cand35-r100-onebatch-20260923 and its terminal/current-object no-rerun/no-retune/no-rescore decision
  - no post-outcome modification of candidate #35 arms, cue, anchor, metric, falsifier, or scientific source
  - no one-way identity consumption, research merge, immutable/evidence ref mutation, Utility execution, or scheduler change by this role
utility_request_created: null
```

## Run close

Role performed: `LITERATURE_REDUCTION_SCOUT`. Generation: `LIT-20260924T002755+0900-R40-SILENT-SYNAPTIC-CREDIT-9C4E2A71`. Inputs: Control R44, Evidence Analyst R101, MAIN Candidate #35 post-exposure report, Fast Forge R100 credit-locality dead end, prior Literature R39, and independently fetched repository refs/source. Genuinely new information: `true`. New SparkBrain scientific result observed since the prior Literature generation: `true`, limited to Candidate #35's development-only zero-credit five-arm response. Top implication: #35's negative result closes only the frozen potential/adaptation surface, while broader activity-silent-memory claims must clear transient synaptic-memory prior art; future delayed-credit/local-responsibility claims must clear ordinary three-factor and e-prop-class baselines. Affected lines are listed above. Utility request: none. Persistence is limited to the role-separated literature latest/state/history paths; no scientific refs/results, research branches, legacy shared latest/state, Utility state, or scheduler are changed. The final branch-tip commit cannot be embedded self-referentially in the content that creates that commit; the exact role-specific handoff commit is re-fetched after the append-only history write and reported externally.