# External Literature Reduction Scout — spike-response kernel / history-filter reduction

- schema_version: `2`
- generation_id: `LIT-20260923T153000+0900-R37-SPIKE-RESPONSE-KERNEL-5A8C21E7`
- produced_at: `2026-09-23T15:30:00+09:00`
- producer_run_id: `external-literature-auto-LIT-20260923T153000+0900-R37-SPIKE-RESPONSE-KERNEL-5A8C21E7`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260923T123024+0900-R36-INFORMATIVITY-HYBRID-SENSITIVITY-6D4A21C8`
- role: `LITERATURE_REDUCTION_SCOUT`
- schedule_slot: `15:30 JST`
- schedule_inference: `false`
- genuinely_new_information: `true`

## Inputs / authoritative state

Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. Authoritative annotated `evidence/*` remains five objects; tag-form `formal/*`, `sealed/*`, and `freeze/*` remain empty. Existing preserve/control refs, consumed identities and current candidate/H7 research heads were independently re-fetched rather than inferred from any `ops/*` mailbox.

Consumed control-plane generations:
- Control Brain: `CTRL-20260923T125800+0900-R42-7C9E41B2` @ `7035ace9b0ef980602dcb124e8974be5640d7377`
- Evidence Analyst: `EVA-20260923T150251+0900-R94-8E6A31C4` @ `5cee6ef496eb9465550fb9c0be5295e587027dfb`
- MAIN: `MAIN-20260923T152800+0900-PRIMARY-CAND34-PREFORMALR2-R94-WAITING-RESPONSE` @ `93a433aa78c7e63a1c654d01a1c8c1f7f287c5e8`
- Fast Forge: `FORGE-20260923T143553+0900-ASSEMBLY-RETENTION-CAPACITY-R93` @ `93a433aa78c7e63a1c654d01a1c8c1f7f287c5e8`
- Prior Literature: `LIT-20260923T123024+0900-R36-INFORMATIVITY-HYBRID-SENSITIVITY-6D4A21C8` @ `5228e5271f9a87c47d6ed1c68b10a24c92d0c996`

Candidate #34's closed R2 scientific contract is unchanged at `research/main-cand34-assembly-route-preformal-r92-cycle4@43d0f25541a3c447d4c7156303647ae94f3119f4`; the exact R94-bound executor remains `research/main-cand34-assembly-route-preformal-r93-response@8ce961dc88fb52afa6399093fce1e3de7e982f2b`. R94 prospectively authorized exactly one bounded `D34-Q002` response with raw-preserve-before-interpretation and no repeat/no FORMAL.

After the designated MAIN report was persisted, its one-shot workflow `35826846989` completed `success` and produced one raw artifact (`cand34-d34-q002-r94-raw`, 3612 bytes, artifact digest `sha256:38a50cf3d63be3355d3d95387d155a6f0e550d998026ccdd38743a07520171f4`). Direct preserve-ref re-fetch still finds no `preserve/cand34*` ref. In accordance with R94/MAIN one-way ordering, this Literature Scout **did not download, read, decode, score, summarize or otherwise inspect the raw artifact**. Its scientific content remains outside this generation. Workflow completion and artifact existence are execution/provenance facts only, not a scientific result available to this role.

R35 already covered polychronization/synfire, timing-bin robustness, temporal FSMs and heterogeneous-delay SNNs. R36 covered perturbation informativity, local phase/state response and hybrid/saltation sensitivity. This run therefore asks a narrower reduction question that had not yet been explicitly tested in the literature stream: **do the exact R2 observables already match standard spike-response/history-filter models closely enough that an ordinary local input-output description is the immediate reduction floor?**

## High-value new findings

### 1. The frozen D34-Q002 observables map almost directly onto a classical Spike Response Model

Gerstner's Spike Response Model treats an incoming spike through a postsynaptic response kernel, while generalized SRM formulations represent membrane potential as an input-response kernel plus a post-spike/refractory kernel. In generalized integrate-and-fire comparisons, the SRM kernel explicitly depends on time since the neuron's last spike and can accurately approximate detailed spike trains.

Sources:
- W. Gerstner, *Time structure of the activity in neural network models*, Physical Review E 51, 738 (1995), https://doi.org/10.1103/PhysRevE.51.738
- R. Jolivet et al., *Generalized Integrate-and-Fire Models of Neuronal Activity Approximate Spike Trains of a Detailed Model to a High Degree of Accuracy*, Journal of Neurophysiology, https://doi.org/10.1152/jn.00190.2004

**Impact.** R2 freezes exactly the ingredients an SRM-like local reduction would use: a source spike, fixed edge weight/delay, destination membrane potential at nominal and `+1 ms`, and destination spike/refractory history. A future observed `+1 ms` effect that is simply predicted by a translated postsynaptic kernel plus refractory/post-spike kernel is ordinary single-edge dynamics, not evidence for an Assembly-specific route mechanism. This is more concrete than R36's general phase-response/saltation ceiling because it specifies a compact generative predictor matched to the actual recorded fields.

### 2. A point-process history/coupling model is a strong ordinary baseline for the spike-level and secondary Assembly response

Truccolo et al. formulate spike probability from a neuron's own spike history, past activity of other neurons and external covariates within one conditional-intensity model. Related population GLM work shows that compact multi-neuron models can capture detailed spatiotemporal spike correlations when coupling and spike-history terms are included.

Sources:
- W. Truccolo et al., *A Point Process Framework for Relating Neural Spiking Activity to Spiking History, Neural Ensemble, and Extrinsic Covariate Effects*, Journal of Neurophysiology (2005), https://doi.org/10.1152/jn.00697.2004
- J. Pillow et al., *Spatio-temporal correlations and visual signalling in a complete neuronal population*, Nature 454, 995–999 (2008), https://doi.org/10.1038/nature07140

**Impact.** A fresh successor can fit/freeze a privilege-matched local history/coupling filter using source spikes, destination history and the intervention/cue covariates, then ask whether it predicts the destination response and the secondary Assembly spike export. If it does, the broader route effect is reducible to ordinary history-dependent point-process dynamics even if the native implementation contains an Assembly object.

### 3. Standard response-function theory provides a lower-cost susceptibility baseline before richer mechanism claims

Cessac, Ampuero & Cofré derive a general linear-response relation for spiking neuronal networks with potentially unbounded spike-history memory: weak time-dependent stimuli can alter spatiotemporal spike correlations in a way predicted from spontaneous statistics, intrinsic dynamics and connectivity.

Source: B. Cessac, I. Ampuero & R. Cofré, *Linear Response of General Observables in Spiking Neuronal Network Models*, Entropy 23, 155 (2021), https://doi.org/10.3390/e23020155

**Impact.** For sufficiently weak perturbations, a prospectively frozen susceptibility/response-function predictor is an ordinary reduction below a special Assembly-route explanation. Failure of this linear baseline would be informative, but not yet a mechanism residual.

### 4. Failure of a linear reduction still does not imply an Assembly-specific mechanism

Helias et al. show that generic pulse-coupled threshold units with finite synaptic weights can have fast, non-linear transient responses that differ qualitatively from diffusion-limit linear response: amplitude dependence, excitation/inhibition asymmetry and background-state dependence arise without a special Assembly mechanism.

Source: M. Helias et al., *Instantaneous Non-Linear Processing by Pulse-Coupled Threshold Units*, PLOS Computational Biology 6(9):e1000929 (2010), https://doi.org/10.1371/journal.pcbi.1000929

**Impact.** The prospective reduction ladder should not jump from `linear response failed` to `Assembly mechanism survived`. It should next test a finite-weight nonlinear threshold/SRM/history model with matched local privilege. Only a reproducible residual beyond those ordinary local dynamics would strengthen an Assembly-specific mechanism claim.

## Synthesis

The closest newly identified ordinary reduction ladder for the exact R2 measurement surface is:

`local spike-response kernel + refractory history` -> `source/destination history-and-coupling point-process model` -> `weak perturbation susceptibility where applicable` -> `finite-weight nonlinear threshold response` -> `broader Assembly-route residual`.

This does **not** authorize any retrofit to the already-closed R2 contract and does not permit post-exposure comparator shopping. The one-shot raw artifact now exists but remains intentionally unread by this role until durable raw preservation is established. Any of these reductions belong to a fresh prospective successor or separately authorized future development object after the preserved R2 result has been dispositioned by Evidence Analyst.

No Utility request is created. MAIN owns the active result/preservation boundary; launching a new comparator implementation now would be outcome-sensitive and could contaminate the prospective separation.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - CAND34_PREFORMAL_R2_INTERPRETATION_CEILING
  - CAND34_LOCAL_SPIKE_RESPONSE_KERNEL_REDUCTION
  - CAND34_HISTORY_COUPLING_FILTER_REDUCTION
  - CAND34_LINEAR_AND_NONLINEAR_RESPONSE_REDUCTION
  - CAND34_FUTURE_ASSEMBLY_ROUTE_IRREDUCIBILITY
  - FUTURE_MECHANISM_SUCCESSOR_ADMISSION
  - PROGRAMME_NOVELTY
novelty_or_reduction_impact: >
  D34_Q002_OBSERVABLES_ADMIT_A_CLOSE_ORDINARY_SPIKE_RESPONSE_KERNEL_AND_HISTORY_FILTER_REDUCTION.
  The frozen source-spike / edge-delay / destination-potential-and-spike fields align directly
  with established SRM and point-process history/coupling models. A delay-sensitive positive
  response therefore does not by itself establish an Assembly-specific route mechanism.
  No current R2 rewrite, result interpretation, or mechanism uplift follows.
audit_classification: null
prospective_baselines_or_discriminators:
  - fresh-successor-only SRM-style local kernel using source spike, edge weight/delay and destination post-spike/refractory state to predict the exact nominal/+1ms fields
  - privilege-matched point-process GLM/history-coupling filter for destination spikes and secondary Assembly spike export
  - weak-response susceptibility predictor where perturbation magnitude justifies it
  - finite-weight nonlinear threshold/SRM extension before treating linear-model failure as a mechanism residual
  - frozen out-of-fit validation and complexity/resource accounting for any future reduction comparison
questions_for_evidence_analyst:
  - After exact D34-Q002 raw preservation and disposition, keep any positive R2 interpretation below Assembly-specific mechanism unless a fresh successor prospectively survives the local SRM/history-filter reduction?
  - Treat a +1ms effect predicted by a translated PSP/refractory kernel as ordinary single-edge dynamics rather than native route irreducibility?
  - Keep all newly identified comparators outside the already-exposed/closed R2 object and require a fresh prospective contract if pursued?
questions_for_control_brain:
  - Add `delay-sensitive local response != Assembly-specific mechanism` with SRM/history-filter reduction as a prospective claim ceiling?
  - Preserve raw-before-interpretation as the immediate hard floor now that the one-shot workflow produced an artifact?
  - Prevent outcome-responsive comparator additions to R2; reserve these reductions for a fresh successor after Analyst disposition?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1-v1/C19-R1-v2/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - H7 PF-R1 no-rerun/no-rescore boundary and H7 R5 provenance hold
  - candidate #34 closed R2 scientific contract at 43d0f25541a3c447d4c7156303647ae94f3119f4
  - candidate #34 exact executor at 8ce961dc88fb52afa6399093fce1e3de7e982f2b
  - D34-Q002 must not be repeated; its raw artifact must not be interpreted before durable exact-byte preservation
  - no post-exposure comparator/metric/threshold/cue/intervention rewrite inside R2
  - candidate #35 remains SYSTEM-scoped
  - no one-way identity consumption, research merge, immutable-ref mutation, Utility execution, or scheduler change by this role
utility_request_created: null
```

## Run close

Role performed: `LITERATURE_REDUCTION_SCOUT`. Generation: `LIT-20260923T153000+0900-R37-SPIKE-RESPONSE-KERNEL-5A8C21E7`. Inputs: Control R42, Evidence Analyst R94, MAIN R94 waiting-response stream plus post-report completed workflow/provenance observation, Fast Forge R93, prior Literature R36. Genuinely new external scientific information: `true`. Top implication: the exact R2 observables have a close established ordinary reduction in spike-response kernels and history/coupling models, so a positive delay effect alone cannot carry Assembly-specific mechanism novelty. A raw PRE_FORMAL artifact exists but was not read because no durable `preserve/cand34*` ref was present. Utility request: none. Persistence is limited to the role-separated literature latest/state/history paths; no scientific refs/results, research branches, legacy shared latest/state, Utility or scheduler are changed.
