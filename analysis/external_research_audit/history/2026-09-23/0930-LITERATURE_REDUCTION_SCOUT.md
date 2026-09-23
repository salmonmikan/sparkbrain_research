# External Literature Reduction Scout — polychrony / temporal-resolution robustness

- schema_version: `2`
- generation_id: `LIT-20260923T093010+0900-R35-POLYCHRONY-TEMPORAL-ROBUSTNESS-4E7A21C9`
- produced_at: `2026-09-23T09:30:10+09:00`
- producer_run_id: `external-literature-auto-LIT-20260923T093010+0900-R35-POLYCHRONY-TEMPORAL-ROBUSTNESS-4E7A21C9`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260923T063434+0900-R34-INTERVENTIONAL-EQUIVALENCE-8F4C21A7`
- role: `LITERATURE_REDUCTION_SCOUT`
- schedule_slot: `09:30 JST`
- schedule_inference: `false`
- genuinely_new_information: `true`

## Inputs / authoritative state

Repository science and all permitted control-plane streams were re-fetched independently. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. The authoritative annotated `evidence/*` set remains exactly five tag objects; tag-form `formal/*`, `sealed/*`, and `freeze/*` remain empty. Legacy freeze branches, preserve refs, control refs, consumed identities and open PR state were independently inspected.

Fresh control-plane inputs consumed:
- Control Brain: `CTRL-20260923T085000+0900-R40-5E1C7A94` @ `f25d48598584bffc5ca736c6ac52c50a94688d89`.
- Evidence Analyst: `EVA-20260923T090047+0900-R90-B84D2C71` @ `91684ca2539d89c6866feecbf1a9e28f26aef2fa`.
- MAIN: `MAIN-20260923T085900+0900-RELAY-CAND34-ARCHR1-R89-COMPLETED-9A4C2E71` @ `18c9d30aed961b719a4c12db329e9adeb40f2db7`; mailbox tip observed `706a3ba3c25f6c69a791504c93c5ddf540abf96a`.
- SUB: `SUB-20260923T083602+0900-QFD-QUEUEFREE-STATE-R89-6B2E4C91` @ `18c9d30aed961b719a4c12db329e9adeb40f2db7`; mailbox tip observed `706a3ba3c25f6c69a791504c93c5ddf540abf96a`.
- Prior Literature: `LIT-20260923T063434+0900-R34-INTERVENTIONAL-EQUIVALENCE-8F4C21A7` @ `027fa9fc45648269c2ebe0ae6408162d155fe840`.

Evidence Analyst R90 canonically advances candidate #34 to MECHANISM / OPEN_DEVELOPMENT / Architecture R2 / `preformal_eligible=true` / `NOT_READY`, allowing prospective contract closure but forbidding response-bearing candidate testing, PRE_FORMAL execution and FORMAL action. Candidate #35 is newly canonical as SYSTEM / DISCOVERY / OPEN_DEVELOPMENT and queued for a separate SUB Discovery R1.

After R90, repository evidence moved independently: `research/main-cand34-assembly-route-architecture-r90-cycle2` advanced to `a6455a3929b86ad25fd106ea93a03604192fc3be` with a prospectively frozen NON_EVIDENTIARY R2 contract and exact-head generic CI `35802555790` completed `success`. This movement has not yet been canonically dispositioned by a newer Analyst generation, so this scout treats it as repository evidence only, not as a control-plane promotion.

The R2 contract fixes a `+1ms` target-edge delay perturbation, a 64ms measurement window, integer `target_prototype_relative_spike_bins`, a five-arm target/matched-control intervention family, global assembly/unit reductions, and an interventional-equivalence falsifier. Stable v0.5 Assembly extraction rounds spike timing into 2ms relative bins. The underlying field itself is deterministic event-driven with delayed arrivals rather than a fixed-step ODE solver. These exact repository facts matter for the literature below.

R34 already covered interventional equivalence / non-unique route graphs. This run does not repeat that result. It asks a different question: **how much of candidate #34's precise delay-sensitive route phenomenon is already ordinary polychronous/synfire computation, and how vulnerable are timing signatures to numerical or measurement resolution?**

## High-value new findings

### 1. Precise delay-defined recurrent routes are classic ordinary prior art: polychronization and synfire chains

**External literature fact.** Izhikevich's polychronization model shows that a minimal recurrent spiking network with axonal conduction delays and STDP can spontaneously form reproducible, time-locked but non-synchronous firing groups with millisecond precision. Synfire-chain models likewise propagate precisely timed spatiotemporal sequences through recurrent or layered circuits.

Sources:
- Izhikevich, *Polychronization: Computation with Spikes*, Neural Computation 18(2), 2006. https://pubmed.ncbi.nlm.nih.gov/16378515/
- Jin, *Spiking neural network for recognizing spatiotemporal sequences of spikes*, Physical Review E 69, 021905, 2004. https://journals.aps.org/pre/abstract/10.1103/PhysRevE.69.021905

**Repository relevance / inference.** Candidate #34's target-edge transmission-null and `+1ms` delay effects can be scientifically interesting, but a precise lagged Assembly route that is disrupted by weight or delay perturbation is not, by itself, a novel computational primitive. An ordinary synfire/polychronous coincidence-propagation explanation sits very close to the claimed mechanism surface.

**Prospective discriminator.** For any fresh successor after the frozen R2 object, compare against a matched delay-line/synfire or polychronous coincidence-propagation model with the same local timing/weight information privilege and comparable state/resource budget. A residual claim should survive after this ordinary timing mechanism reproduces as much of the complete response vector as it can.

### 2. Millisecond route structure can be dominated by time-resolution / synchrony artifacts even when coarse network activity looks unchanged

**External literature fact.** Pauli et al. reproduced the classic polychronization model and found extreme sensitivity to numerical/time resolution. With closely matched firing rates and similar coarse network dynamics, their group-finding results changed from about 13,000 groups in a 1ms-locked configuration to 151 groups at 0.1ms spike/delay resolution—a roughly 90-fold reduction. They concluded that the original study substantially overstated group counts because 1ms discretization induced artificial synchrony. They recommend explicit robustness checks at higher simulation precision whenever exact spike timing matters.

Source:
- Pauli, Weidel, Kunkel & Morrison, *Reproducing Polychronization: A Guide to Maximizing the Reproducibility of Spiking Network Models*, Frontiers in Neuroinformatics 12:46, 2018. https://doi.org/10.3389/fninf.2018.00046

**Repository relevance / inference.** SparkBrain's stable field is event-driven, so the exact fixed-step failure mode from Pauli et al. does **not** transfer directly. The analogous risk here is measurement/discretization resonance: candidate #34 freezes a `+1ms` perturbation while the existing Assembly representation rounds relative spike times into 2ms bins. A causal effect that appears only because a 1ms shift crosses a 2ms rounding boundary would be evidence about the chosen representation, not necessarily about a robust physical route feature.

**Prospective discriminator.** Do not rewrite the now-frozen R2 object. For a fresh successor only, predeclare either (a) continuous-time spike-response metrics, or (b) multiple independently frozen timing resolutions / bin phases, and require the route conclusion to be qualitatively stable. Victor–Purpura or van Rossum spike-train distances are established continuous-time alternatives that avoid making a single hard bin boundary the sole timing observable.

### 3. A precisely timed spiking route can still reduce to a simple finite-state recognizer

**External literature fact.** Jin's recurrent spiking synfire-chain recognizer accepts a specific spatiotemporal spike sequence and explicitly maps the computation of the network to a finite-state machine. Thus detailed spike timing and a concrete propagation chain do not imply that the computational principle itself requires a richer distributed mechanism.

Source:
- Jin, *Spiking neural network for recognizing spatiotemporal sequences of spikes*, Physical Review E 69, 021905, 2004. https://doi.org/10.1103/PhysRevE.69.021905

**Repository relevance / inference.** Candidate #34 can legitimately ask whether particular lagged route features are causally identifiable, but later novelty language should separate `physical route realization` from `computational irreducibility`. A route may be intervention-sensitive yet computationally reducible to a compact state machine that tracks progress through a temporal sequence.

**Prospective discriminator.** A future candidate #34 successor should include a matched temporal-progress finite-state/synfire recognizer or equivalent low-state route-progress baseline whenever the claim rises from physical route causality to a broader computational-mechanism claim. This is more specific than a generic recurrent baseline because it reproduces exact sequence progress using minimal discrete state.

### 4. Heterogeneous / learnable delays are now an ordinary modern SNN substrate, not an exotic mechanism

**External literature fact.** Learnable axonal delays materially improve temporal recognition in SNNs, and 2026 work reports online three-factor rules that jointly learn weights and synaptic/axonal delays in feedforward and recurrent LIF networks, with substantial gains over weights-only baselines. A peer-reviewed 2026 recurrent SNN study also stores precise temporal patterns using many heterogeneous delays per synapse and overlapping spiking motifs.

Sources:
- Sun, Chua, Devos & Botteldooren, *Learnable axonal delay in spiking neural networks improves spoken word recognition*, Frontiers in Neuroscience 17, 2023. https://doi.org/10.3389/fnins.2023.1275944
- *Three factor delay learning rules for spiking neural networks*, Frontiers in Neuroscience, 2026. https://pubmed.ncbi.nlm.nih.gov/42246032/
- Perrinet, *Working Memory in a Recurrent Spiking Neural Networks With Heterogeneous Synaptic Delays*, Proceedings of the Austrian Symposium on AI, Robotics, and Vision, 2026. https://doi.org/10.34749/3061-1466.2026.55

**Repository relevance / inference.** If candidate #34 later observes a strong dependence on exact edge delay, that result still sits inside an established family of ordinary temporal SNN mechanisms. The novelty bar is not merely `delay matters`; it is whether SparkBrain's specific local Assembly-route responsibility remains after ordinary heterogeneous-delay sequence mechanisms and matched timing resources are accounted for.

## Secondary newly active line: candidate #35

Candidate #35's queue-free `potential` / `adaptation` priming question already has the right SYSTEM ceiling. Classical adaptive integrate-and-fire work models membrane potential and adaptation as sufficient local dynamical state, and spike-frequency adaptation alters signal processing from roughly 10ms to beyond 1s. Brette & Gerstner's two-variable AdEx model reproduced detailed-model spike timing to high accuracy, while Benda et al. show adaptation-current / dynamic-threshold mechanisms directly alter stimulus-response gain.

Sources:
- Brette & Gerstner, *Adaptive Exponential Integrate-and-Fire Model as an Effective Description of Neuronal Activity*, Journal of Neurophysiology 94, 2005. https://doi.org/10.1152/jn.00686.2005
- Benda, Maler & Longtin, *Linear Versus Nonlinear Signal Transmission in Neuron Models With Adaptation Currents or Dynamic Thresholds*, Journal of Neurophysiology 104, 2010. https://doi.org/10.1152/jn.00240.2010

This does not create a new #35 mechanism hypothesis. It sharpens the ordinary reduction: if the later weak-cue divergence is predicted by frozen local membrane potential, adaptation, threshold margin and their known decay equations, close the SYSTEM object rather than attributing the effect to Assembly-level memory.

## Synthesis

The new candidate-#34 reduction ladder is:

`delay-sensitive Assembly route effect` → `ordinary polychronous/synfire coincidence propagation` → `timing-resolution/bin-phase robustness` → `compact temporal-progress FSM reduction` → `only then any broader route-mechanism residual`.

The most consequential new issue is the conjunction of external and repository evidence: the live R2 contract uses a `+1ms` perturbation and an integer relative-spike-bin observable, while stable Assembly extraction bins timing at 2ms. Because precise spiking-route literature contains known discretization/synchrony pathologies, **future confirmatory interpretation must not equate a bin-boundary-sensitive effect with a robust temporal mechanism**. R2 itself must remain frozen; any precision/continuous-time discriminator belongs to a fresh prospective successor.

No Utility request is created. MAIN owns the candidate #34 Architecture R2 surface and has already frozen a non-evidentiary contract at `a6455a...`; injecting a new timing-resolution diagnostic into that same frozen object would be literature-driven protocol rewriting.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - CAND34_ASSEMBLY_TEMPORAL_ROUTE_IDENTIFIABILITY
  - CAND34_TEMPORAL_RESOLUTION_ROBUSTNESS
  - CAND34_POLYCHRONOUS_SYNFIRE_REDUCTION
  - CAND34_TIMING_BIN_PHASE_SENSITIVITY
  - CAND34_COMPUTATIONAL_FSM_REDUCTION
  - CAND35_LOCAL_ADAPTATION_REDUCTION
  - FUTURE_MECHANISM_SUCCESSOR_ADMISSION
  - PROGRAMME_NOVELTY
novelty_or_reduction_impact: >
  PRECISE_DELAY_ROUTE_EFFECTS_HAVE_CLOSE_POLYCHRONOUS_SYNFIRE_PRIOR_ART_AND_A_KNOWN_TEMPORAL_DISCRETIZATION_FAILURE_MODE.
  Candidate #34 must not treat +1ms delay sensitivity or integer spike-bin changes alone as a novel/robust mechanism.
  Future successors should test matched ordinary delay-line/synfire explanations, continuous-time or multi-resolution timing robustness, and compact temporal-state reduction.
audit_classification: null
prospective_baselines_or_discriminators:
  - matched synfire/polychronous coincidence-propagation comparator with equal timing and local-state privilege
  - fresh-successor-only continuous-time spike metric or prospectively frozen multi-resolution/bin-phase robustness
  - compact temporal-progress finite-state recognizer with matched information privilege
  - matched heterogeneous-delay recurrent SNN ceiling when resource/learning privilege can be aligned
  - for candidate #35, local membrane/adaptation/threshold-margin state-transition prediction before any Assembly-level interpretation
questions_for_evidence_analyst:
  - Preserve candidate #34 R2 exactly as frozen and reserve timing-resolution robustness for a fresh successor rather than retrofitting R2?
  - If a later #34 response depends on `+1ms` delay, cap the claim unless the effect is robust to representation/binning or independently visible in continuous-time response observables?
  - Treat synfire/polychronous and compact temporal-FSM explanations as ordinary future reduction baselines for broader candidate-#34 mechanism claims?
  - Keep candidate #35 at SYSTEM scope whenever frozen local potential/adaptation dynamics predict the weak-cue effect?
questions_for_control_brain:
  - Add `delay sensitivity != novel temporal mechanism` and `bin-boundary sensitivity != robust route evidence` as prospective claim-ceiling guardrails?
  - Keep all new precision/synfire/FSM discriminators outside the already-frozen candidate #34 R2 object?
  - Preserve H7 provenance hold and all existing one-way boundaries unchanged?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1-v1/C19-R1-v2/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - H7 PF-R1 development result/raw and no-rerun/no-rescore boundary
  - H7 R5 preidentity object and FORMAL provenance hold
  - candidate #34 Architecture R1 exact completed head and results
  - candidate #34 R2 contract at a6455a3929b86ad25fd106ea93a03604192fc3be must not be rewritten in place because of this literature
  - candidate #35 remains prospective SYSTEM Discovery; no mechanism uplift from literature
  - no candidate response-bearing execution, PRE_FORMAL/FORMAL action, one-way identity, research merge, immutable-ref mutation, Utility execution, or scheduler change by this role
utility_request_created: null
```
