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

## Authoritative inputs

Repository evidence was fetched independently of the `ops/*` mailboxes. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. Current authoritative tags remain five `evidence/*` tags, with no tag-form `formal/*`, `sealed/*`, `freeze/*`, or `immutable/*`; legacy freeze branches and preserve refs were separately inspected. Open PR #149 is scheduler-registry tooling rather than scientific state.

Consumed control-plane generations/commits:
- Control Brain `CTRL-20260923T225500+0900-R44-C8F41D72` @ `3c46617fba123704297d880a748c305c16a7dd01`
- Evidence Analyst `EVA-20260924T000324+0900-R101-CAND35-POSTEXPOSURE` @ `e50e0a91e25f2457d0b7152900a48cbdc5006485`
- MAIN `MAIN-20260923T235628+0900-RELAY-CAND35-R100-ONEBATCH-EXPOSED-WAITING-ANALYST` @ `ops/orchestrator-run-report@21a8ee7b0ae85df57a0a35b70ad726e45252e259`
- Fast Forge `FORGE-20260923T233625+0900-V05-CREDIT-LOCALITY-R100` @ `ops/orchestrator-run-report@21a8ee7b0ae85df57a0a35b70ad726e45252e259`
- Prior Literature `LIT-20260923T213000+0900-R39-OFFMANIFOLD-INTERVENTIONS-6D2A8C41` @ `741becd60d3e7dc8f97cedf1347c42c769092011`

Candidate #35 materially advanced after R39. The prospectively fixed five-arm Architecture batch ran exactly once and was preserved before interpretation at `raw/cand35-r100-onebatch-20260923@afe4b7ad0f908f3b01eca9e391a2b05cb3be9a7a`. Evidence Analyst R101 now marks the current object `TERMINAL_FOR_CURRENT_OBJECT` with bounded interpretation `NO_MEASURED_PRIMING_EFFECT_ON_FROZEN_OUTPUT_SURFACE`: `SHAM_STATE`, `POTENTIAL_NULL`, `ADAPTATION_NULL`, and `JOINT_SUBTHRESHOLD_NULL` yielded the same two-spike `[6,7]` cascade/no-ignition surface, and `DELAYED_SHAM_32MS` yielded the same structure shifted in time. This is a new SparkBrain development result, but it is unscored, non-PRE_FORMAL, non-FORMAL, and has zero confirmatory credit.

The exact candidate #35 scientific source explicitly disables weight learning, delay learning, and reward modulation, so this result targets the frozen neuronal subthreshold coordinates and output surface rather than a transient synaptic-plasticity memory carrier.

## High-value findings

### 1. Candidate #35's negative result does not generalize to the broader class of activity-silent memory

Tiddia et al. report a 2026 peer-reviewed spiking working-memory model in which short-term synaptic facilitation sustains activity-silent memory and remains robust under added synaptic heterogeneity. A recent 2026 preprint similarly reports that residual transient synaptic configuration after complete spiking silence can predict later activity regeneration.

Sources:
- Tiddia et al., *Short-term plasticity-based working memory spiking model is resilient to synaptic heterogeneity*, Phys. Rev. E 114, 014409 (22 July 2026), DOI `10.1103/zcmm-3cgh`, https://journals.aps.org/pre/abstract/10.1103/zcmm-3cgh
- Khanjanianpak & Valiadeh, *Activity Regeneration from Silent States in Neuronal Networks with Transient Synaptic Memory*, arXiv:2607.14000 (2026), https://arxiv.org/abs/2607.14000

**Impact.** R101's #35 conclusion should remain terminal and narrow. Unchanged output after potential/adaptation nulling does not establish the absence of all queue-free/activity-silent memory mechanisms. Any fresh broader silent-memory successor should include transient synaptic/STP state as an ordinary comparator. This is prospective only: #35's exact frozen source did not instantiate that mechanism family.

### 2. SparkBrain's current v0.5 reward/eligibility path is weaker than the standard delayed-reward three-factor baseline

Fast Forge R100 found that v0.5 keeps per-edge eligibility, but delayed reward alone does not consume that stored trace. Exact stable-main source confirms that eligibility is decayed on `apply()`, while an edge is skipped unless the current spike batch contains both pre- and postsynaptic spikes; reward is a single scalar trace used only inside the later update branch.

Ordinary three-factor learning is stronger. Izhikevich's distal-reward mechanism and the broader neoHebbian eligibility-trace literature allow a synaptic tag created by earlier pre/post activity to be converted into plasticity when a delayed third factor such as dopamine/reward arrives while the tag persists.

Sources:
- Izhikevich, *Solving the distal reward problem through linkage of STDP and dopamine signaling*, Cerebral Cortex 17(10), 2007, DOI `10.1093/cercor/bhl152`, https://pubmed.ncbi.nlm.nih.gov/17220510/
- Gerstner et al., *Eligibility Traces and Plasticity on Behavioral Time Scales: Experimental Support of NeoHebbian Three-Factor Learning Rules*, Frontiers in Neural Circuits 12:53 (2018), DOI `10.3389/fncir.2018.00053`, https://pubmed.ncbi.nlm.nih.gov/30108488/

**Impact.** Forge's dead-end does not argue against eligibility traces in general. It shows that the current optional v0.5 implementation falls below a standard delayed-credit baseline. Any future delayed-credit novelty claim should compare against a correctly privilege-matched rule where a delayed third factor can act on prior eligibility without requiring a new qualifying spike pair.

### 3. Temporal eligibility and spatial/local responsibility are separate credit-assignment problems

Bellec et al.'s e-prop factorizes recurrent online credit into synapse-local eligibility traces and neuron/population-specific learning signals. Slowly changing hidden variables can carry eligibility across long temporal gaps, while the separate learning signal determines where error/reward information is assigned.

Source:
- Bellec et al., *A solution to the learning dilemma for recurrent networks of spiking neurons*, Nature Communications 11, 3625 (2020), DOI `10.1038/s41467-020-17236-y`, https://www.nature.com/articles/s41467-020-17236-y

**Impact.** Global reward plus per-edge eligibility is a legitimate ordinary baseline and can solve limited distal reward through selective synaptic tags. It is not by itself evidence for a richer native causal-lineage/local-responsibility mechanism. Future SparkBrain responsibility claims should separately test temporal trace persistence and spatial responsibility allocation, with an e-prop-class neuron/population-specific learning signal as a stronger reduction ceiling than global reward-modulated STDP alone.

### 4. The 2026 novelty bar includes fully local forward credit and online joint delay learning

Pes et al.'s Traces Propagation combines eligibility traces with a layer-wise contrastive signal for forward-only local learning and explicitly addresses temporal plus spatial credit. Vassallo & Taherinejad report a 2026 peer-reviewed three-factor rule for online joint learning of synaptic weights and axonal/synaptic delays in feedforward and recurrent SNNs.

Sources:
- Pes et al., *Traces propagation: memory-efficient and scalable forward-only learning in spiking neural networks*, Neuromorphic Computing and Engineering 6(1), 014002 (2026), DOI `10.1088/2634-4386/ae2ef9`
- Vassallo & Taherinejad, *Three factor delay learning rules for spiking neural networks*, Frontiers in Neuroscience (2026), DOI `10.3389/fnins.2026.1814505`, https://pubmed.ncbi.nlm.nih.gov/42246032/

**Impact.** Future claims combining locality, delayed credit, and learned timing should not use plain STDP as the strongest prior-art comparator. Modern local-forward credit rules and joint weight-delay three-factor learning should be included prospectively before any richer SparkBrain credit/responsibility novelty claim.

## Synthesis

Two distinct boundaries are now clearer. The new #35 result is useful but narrow: it closes the frozen neuronal potential/adaptation priming surface and must not be generalized to all activity-silent memory because transient synaptic-state mechanisms are established ordinary alternatives. Separately, the v0.5 eligibility/reward path is below the standard delayed-credit baseline: ordinary three-factor rules already support delayed third-factor action on stored eligibility, while e-prop-class methods explicitly separate temporal eligibility from spatial responsibility.

Prospective reduction ladders:

`queue-free/activity-silent claim -> neuronal potential/adaptation -> transient synaptic/STP state -> other ordinary slow hidden variables -> only then a broader native residual`

`local spike correlation -> stored eligibility -> delayed third-factor action on prior eligibility -> neuron/population-specific spatial learning signal -> modern local-forward / joint weight-delay baseline -> only then richer causal-responsibility novelty`.

No current object is rewritten. Candidate #35 remains terminal for its current object and zero-credit; Candidate #34 remains terminal/reducible; H7 remains on its pre-identity integrity-capability hold. No Utility request is created because there is no admitted fresh candidate requiring implementation and injecting these baselines into terminal/held objects would be outcome-responsive redesign.

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

Role performed: `LITERATURE_REDUCTION_SCOUT`. Generation: `LIT-20260924T002755+0900-R40-SILENT-SYNAPTIC-CREDIT-9C4E2A71`. Inputs: Control R44, Evidence Analyst R101, MAIN Candidate #35 post-exposure report, Fast Forge R100 credit-locality dead end, prior Literature R39, and independently fetched repository refs/source. Genuinely new information: `true`. New SparkBrain scientific result observed since prior Literature: `true`, limited to Candidate #35's development-only zero-credit five-arm response. Top implication: #35's negative result closes only the frozen potential/adaptation surface, while broader activity-silent-memory claims must clear transient synaptic-memory prior art; future delayed-credit/local-responsibility claims must clear ordinary three-factor and e-prop-class baselines. Affected lines are listed above. Utility request: none. Persistence is restricted to role-separated literature latest/state/history paths; no scientific refs/results, research branches, legacy shared latest/state, Utility state, or scheduler are changed. Exact final branch-tip persistence cannot be embedded self-referentially in this append-only file; the branch tip is re-fetched after this write and reported externally.