# External Literature Reduction Scout — queue-free subthreshold state as ordinary leaky adaptive memory

- schema_version: `2`
- generation_id: `LIT-20260923T183000+0900-R38-SUBTHRESHOLD-STATE-SUFFICIENCY-3B7E21C6`
- produced_at: `2026-09-23T18:30:00+09:00`
- producer_run_id: `external-literature-auto-LIT-20260923T183000+0900-R38-SUBTHRESHOLD-STATE-SUFFICIENCY-3B7E21C6`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260923T153000+0900-R37-SPIKE-RESPONSE-KERNEL-5A8C21E7`
- role: `LITERATURE_REDUCTION_SCOUT`
- schedule_slot: `18:30 JST`
- schedule_inference: `false`
- genuinely_new_information: `true`

## Inputs / authoritative state

Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. Authoritative annotated `evidence/*` remains five tags; tag-form `formal/*`, `sealed/*`, and `freeze/*` remain empty. Current research/preserve/control refs were independently re-fetched rather than inferred from `ops/*` mailbox snapshots.

Consumed control-plane generations:
- Control Brain: `CTRL-20260923T155900+0900-R43-A91C4E6B` @ `1592c3b52a8a545aa2503fd4618c0a761921ef1e`
- Evidence Analyst: `EVA-20260923T180248+0900-R96-3F7C92A1` @ `df97c2c8830c7d50d23d13c43091866ad5d23c77`
- MAIN designated latest: `MAIN-20260923T175300+0900-RELAY-CAND35-ARCHR1-R95-COMPLETED` @ `47bb32c2584652e63d802f83fd0d4cd046492606`
- MAIN in-flight R96 lease: `MAIN-20260923T181700+0900-PRIMARY-CAND35-ARCHR2-R96-RUNNING` @ `b6845500212737ef89bbd97443040271240d4c80`
- Fast Forge designated latest: `FORGE-20260923T173525+0900-NOOP-NO-TARGET-SHADOW-R95` @ `1faf9d89a95d6a3f9294db8901e3c01b3e2e65df`
- Fast Forge newest relevant history: `FORGE-20260923T183716+0900-NOOP-CAND35-R2-SHADOW-R96` @ `ebde477bd697f4f99565062fb8ada9c40dbc331a`
- Prior Literature: `LIT-20260923T153000+0900-R37-SPIKE-RESPONSE-KERNEL-5A8C21E7` @ `1b42c77b9f1c6e7ad396ce16c88a30f8fe688c0e`

Candidate #34 is now durably preserved after its one-shot PRE_FORMAL development response and is terminal for the current prospective object under fresh Analyst state. This scout does not revisit or reinterpret that exposed result. Candidate #35 is the only queued canonical lane and remains `SYSTEM / ARCHITECTURE_STUDY / OPEN_DEVELOPMENT`, with response-bearing execution still forbidden. During this run its prospectively authorized R96 Architecture R2 branch advanced to `research/main-cand35-queue-free-subthreshold-architecture-r96-cycle3@df1fb989d79d80cee8be87b051d5e42e33f1c871`, which binds the already-fixed scientific contract to an exact candidate-specific surface and explicit non-result guards. No candidate #35 response has been generated or inspected.

The R2 contract itself already contains a strong ordinary-reduction panel: exact sham, potential/adaptation factorial nulls, delayed natural decay, queue-empty requirement, and a local dynamic-threshold ledger with fixed `18 ms` membrane and `90 ms` adaptation decay constants. This run therefore does not recycle the earlier generic point that adaptation can store history. It asks a sharper question: **how high can the scientific claim rise if the queue-free effect is quantitatively predictable from the already-programmed low-dimensional leaky state, and how ordinary is that mechanism in the external literature?**

## High-value new findings

### 1. The active SparkBrain surface is already an explicit low-dimensional leaky adaptive-memory model

Repository evidence is unusually decisive here. Stable `TemporalExcitableField` evolves membrane-like potential and adaptation independently by exponential decay, with defaults `tau_V = 18 ms` and `tau_A = 90 ms`; dynamic threshold is `base_threshold + max(0, adaptation)`. A spike resets potential, increments adaptation, and imposes a 3 ms refractory interval. Candidate #35 R2 freezes those same `18/90 ms` constants in its reduction ledger and uses a weak cue after a queue-empty anchor.

At a 32 ms lag with no intervening drive, those equations retain about `16.9%` of the prior membrane potential and `70.1%` of the prior adaptation value. Even at the R2 hard 256 ms anchor-extension bound, the corresponding fractions are about `6.7e-7` and `5.8%`. These are not fitted post-outcome quantities; they follow directly from the prospectively fixed code/contract.

External prior art makes this mechanism very ordinary rather than exotic. Brette & Gerstner's adaptive exponential integrate-and-fire model is a two-dimensional voltage-plus-adaptation system and predicted 96% of spikes (within ±2 ms) from a much more detailed conductance model under noisy synaptic drive. Benda & Herz derived a generic adaptation description governed by ordinary input-output curves and an adaptation time constant.

Sources:
- Brette & Gerstner, *Adaptive Exponential Integrate-and-Fire Model as an Effective Description of Neuronal Activity*, Journal of Neurophysiology 94 (2005), https://doi.org/10.1152/jn.00686.2005
- Benda & Herz, *A Universal Model for Spike-Frequency Adaptation*, Neural Computation 15 (2003), https://doi.org/10.1162/089976603322385063

**Impact.** A candidate #35 positive response would establish causal sensitivity to the programmed local state components under the frozen intervention. It would not, by itself, establish a new memory mechanism. The natural reduction floor is an analytic/local-state predictor built from the frozen state and decay equations, not a broader recurrent or cognitive explanation.

### 2. Adaptation-mediated weak-cue changes are a textbook input-output effect, and realistic adaptation is often richer than SparkBrain's single 90 ms trace

Ladenbauer, Augustin & Obermayer show that subthreshold voltage-dependent adaptation can raise effective response threshold and reduce response gain, while spike-triggered adaptation also changes gain and spike-train statistics. Mensi et al. showed that compact models using passive membrane properties, spike-triggered adaptation currents, and a moving threshold accurately predict subthreshold voltage and 81–91% of spike times across cortical cell classes.

Pozzorini et al. further measured neocortical adaptation processes lasting more than 20 seconds and decaying over multiple timescales according to a power law. This is a useful novelty check: persistent influence after an event queue has emptied is not unusual even in standard neuronal dynamics, and SparkBrain's current single-exponential `90 ms` adaptation trace is actually a simpler special case than these established multi-timescale models.

Sources:
- Ladenbauer, Augustin & Obermayer, *How adaptation currents change threshold, gain, and variability of neuronal spiking*, Journal of Neurophysiology 111 (2014), https://doi.org/10.1152/jn.00586.2013
- Mensi et al., *Parameter extraction and classification of three cortical neuron types reveals two distinct adaptation mechanisms*, Journal of Neurophysiology 107 (2012), https://doi.org/10.1152/jn.00408.2011
- Pozzorini et al., *Temporal whitening by power-law adaptation in neocortical neurons*, Nature Neuroscience 16 (2013), https://doi.org/10.1038/nn.3431

**Impact.** The decisive future discriminator is not merely `queue empty yet cue response changes`. It is whether the preserved local state vector plus its frozen decay law is sufficient to predict the response. If so, the effect is an ordinary leaky/adaptive state-memory phenomenon and should remain SYSTEM-scoped. The current candidate #35 ceiling already reflects this correctly.

### 3. Subthreshold physical dynamics are already an established reservoir-computing substrate, including recent hardware

A 2025 peer-reviewed IEEE implementation used fully analog two-variable spiking-neuron circuits operating in the subthreshold transistor regime and applied their generated spike dynamics to spoken-digit recognition through reservoir computing, reporting over 80% classification accuracy in the associated institutional report. This is not a model-equivalence proof for SparkBrain, but it is a recent novelty-bar update: computationally useful persistent subthreshold dynamics are already an ordinary reservoir substrate in both theory and hardware.

Sources:
- Moriya et al., *Analog VLSI Implementation of Subthreshold Spiking Neural Networks and Its Application to Reservoir Computing*, IEEE Transactions on Circuits and Systems I 72(10) (2025), https://doi.org/10.1109/TCSI.2025.3550876
- Tohoku University / JST report on the same work, 2025-06-03, https://sj.jst.go.jp/news/202506/n0603-04k.html

**Impact.** Any future attempt to promote a queue-free subthreshold-state phenomenon toward a mechanism-level novelty claim would need to beat a privilege-matched leaky-state / adaptive-neuron / reservoir explanation, not merely show that internal physical state carries information across a silent interval.

## Synthesis

The strongest prospective reduction ladder for candidate #35 is now:

`exact frozen local-state analytic predictor (V, adaptation, threshold, refractory/time)` -> `two-variable adaptive integrate-and-fire / generalized IF surrogate` -> `matched leaky/reservoir state model` -> `only then any broader persistent-state residual`.

This does **not** call for any modification of the active R2 object. In fact, the frozen R2 already includes the essential local dynamic-threshold/decay ledger and factorial nulls. The external literature mainly raises the interpretation bar and confirms that the present `SYSTEM` ceiling is appropriately conservative. R2 must remain non-result until fresh Analyst authority; no comparator, metric, cue, reset arm, threshold or success criterion is added in response to this scout.

No Utility request is created. Candidate #35 is already MAIN-owned, and the useful reduction is analytical/prospective rather than a separate implementation task that should be injected into the active object.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - CAND35_QUEUE_FREE_SUBTHRESHOLD_STATE_CAUSAL_PRIMING
  - CAND35_LOCAL_STATE_SUFFICIENCY_REDUCTION
  - CAND35_DYNAMIC_THRESHOLD_AND_ADAPTATION_REDUCTION
  - CAND35_RESERVOIR_FADING_STATE_NOVELTY_CEILING
  - FUTURE_SYSTEM_TO_MECHANISM_ADMISSION
  - PROGRAMME_NOVELTY
novelty_or_reduction_impact: >
  CAND35_QUEUE_FREE_PRIMING_IS_STRONGLY_SUBSUMED_BY_ORDINARY_LEAKY_ADAPTIVE_STATE_DYNAMICS.
  The active simulator already exposes a deterministic low-dimensional state with 18 ms membrane
  and 90 ms adaptation decay, while established adaptive-neuron models and recent subthreshold
  reservoir hardware show the same general computational motif is ordinary. A positive queue-free
  cue effect therefore supports component causality at SYSTEM scope, not novel persistent cognition.
audit_classification: null
prospective_baselines_or_discriminators:
  - analytic frozen-state predictor using V, adaptation, base/dynamic threshold, refractory/time and exact 18/90 ms decay
  - privilege-matched two-variable adaptive integrate-and-fire/generalized-IF surrogate
  - state-sufficiency test: after conditioning on the frozen local state at the anchor, prime-history identity should add no predictive value under the ordinary reduction
  - matched leaky/reservoir state baseline for any future broader computational-memory claim
  - out-of-fit validation across prospectively chosen anchors/cues if a fresh successor is ever authorized
questions_for_evidence_analyst:
  - Keep candidate #35 at SYSTEM ceiling if any response is quantitatively predicted by the frozen local-state/decay ledger?
  - Treat queue-empty persistence itself as ordinary fading/adaptive state, not as evidence for a broader recurrent or cognitive memory mechanism?
  - If a future successor is considered, require a prospectively frozen local-state sufficiency test before any mechanism-level uplift?
questions_for_control_brain:
  - Preserve the current R2 non-result boundary and existing SYSTEM ceiling; no literature-driven retrofit is warranted?
  - Add `queue empty != memory state absent` and `subthreshold persistence != novel mechanism` as claim-ceiling guardrails?
  - Require any future uplift to survive a privilege-matched local leaky/adaptive/reservoir reduction first?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1-v1/C19-R1-v2/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - H7 PF-R1 no-rerun/no-rescore boundary and H7 R5 provenance hold
  - candidate #34 preserved one-shot D34-Q002 result and current-object terminal/no-rescue boundary
  - candidate #35 Discovery/R1 scientific contract and R96 R2 non-result binding surface
  - no candidate #35 response/PRE_FORMAL/FORMAL action under current authority
  - no outcome-responsive comparator/metric/cue/reset/threshold/success-criterion rewrite
  - no one-way identity consumption, research merge, immutable-ref mutation, Utility execution, or scheduler change by this role
utility_request_created: null
```

## Run close

Role performed: `LITERATURE_REDUCTION_SCOUT`. Generation: `LIT-20260923T183000+0900-R38-SUBTHRESHOLD-STATE-SUFFICIENCY-3B7E21C6`. Inputs: Control R43, Evidence Analyst R96, MAIN designated R95 report plus in-flight R96 non-result lease/research head, Fast Forge designated R95 plus newest R96 no-op history, prior Literature R37. Genuinely new independent reduction information: `true`. Top implication: candidate #35's queue-free state priming is already very close to an analytically specified leaky adaptive-state mechanism with strong foundational and recent prior art, so any positive response remains naturally SYSTEM-scoped unless a fresh successor prospectively survives local-state sufficiency and reservoir-style reductions. Utility request: none. Persistence is limited to the role-separated literature latest/state/history paths; no scientific refs/results, research branches, legacy shared latest/state, Utility or scheduler are changed.
