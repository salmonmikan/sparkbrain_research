# External Literature Reduction Scout — perturbation informativity / local hybrid sensitivity

- schema_version: `2`
- generation_id: `LIT-20260923T123024+0900-R36-INFORMATIVITY-HYBRID-SENSITIVITY-6D4A21C8`
- produced_at: `2026-09-23T12:30:24+09:00`
- producer_run_id: `external-literature-auto-LIT-20260923T123024+0900-R36-INFORMATIVITY-HYBRID-SENSITIVITY-6D4A21C8`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260923T093010+0900-R35-POLYCHRONY-TEMPORAL-ROBUSTNESS-4E7A21C9`
- role: `LITERATURE_REDUCTION_SCOUT`
- schedule_slot: `12:30 JST`
- schedule_inference: `false`
- genuinely_new_information: `true`

## Inputs / authoritative state

Repository science and all permitted control-plane streams were re-fetched independently. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. The authoritative annotated `evidence/*` set remains exactly five tag objects; tag-form `formal/*`, `sealed/*`, and `freeze/*` remain empty. Legacy freeze/preserve/control refs, consumed identities, relevant open PRs, active research refs, and current workflows were independently inspected.

Fresh control-plane inputs consumed:
- Control Brain: `CTRL-20260923T115056+0900-R41-4C156929` @ `27b6531b6b3a1d941a484aeee012d5c59fe63d79`.
- Evidence Analyst: `EVA-20260923T105725+0900-R92-6B8E31D4` @ `a05ab3f655a23eabd84c910ba337d64a948c168a`.
- MAIN: `MAIN-20260923T115328+0900-RELAY-CAND34-PREFORMALR2-R92-BLOCKED-AUTHORITY-INTEGRITY` @ path commit `0167aa75e768f51bbc37528868af569a1d054786`.
- Fast Forge / legacy SUB mailbox: `FORGE-20260923T114344+0900-R92-RECEPTOR-SUPPRESSION-DEADENDS` @ path commit `b2fe7ad25a356d170de1291ab0de0b7e4eec3dfe`.
- Prior Literature: `LIT-20260923T093010+0900-R35-POLYCHRONY-TEMPORAL-ROBUSTNESS-4E7A21C9` @ `cd5069201723110acc9e15d60216c9d1f2e63ce7`.

R92 remains the canonical Evidence Analyst generation. It accepted Independent Audit R8's pre-result causal-opportunity defect in candidate #34 PRE_FORMAL R1, preserved the R1 prebind unchanged, revoked response readiness, and authorized only a same-candidate, opportunity-aware PRE_FORMAL R2 revision while the object remains `OPEN_DEVELOPMENT`. R92 explicitly requires source activation, arrival timing, target refractory/threshold state, downstream observable opportunity, opportunity-matched controls, and fresh READY review before any response-bearing execution.

Control R41 agrees: candidate #34 remains MECHANISM / PRE_FORMAL / OPEN_DEVELOPMENT / cycle 4 / `NOT_READY`, with no candidate response exposed. H7 remains on its independent FORMAL provenance hold. Fast Forge's first two prototypes were ordinary-reduction dead ends and are noncanonical/non-evidentiary.

Repository evidence moved after those control-plane generations. `research/main-cand34-assembly-route-preformal-r92-cycle4` advanced from the R41/MAIN-observed `1f9c6cec...` to `a134513838d8f30013d904a95a61cfbcf9454eaa` with commit `cand34 preformal r2: align opportunity-aware contract to R92`. The source now binds canonical R92 authority, uses a source-only cue, forbids directly cueing the tested destination, requires the destination non-refractory at the anchor, records destination potential/spike state around nominal and +1ms arrival, limits the claim to development-only physical route influence under that source-only cue, keeps Assembly response secondary, and still sets response-bearing execution to false pending fresh Analyst review. This is repository movement only; it is not a scientific result or canonical promotion.

At the final workflow observation for this run, exact-head dedicated R2 non-result workflow `35814833603` on `a134513...` completed `failure`; generic CI `35814833574` was still `in_progress`. No response-bearing execution or scientific result was observed. This scout does not diagnose or repair that workflow and does not treat its status as scientific evidence.

R35 already covered polychronous/synfire prior art, timing-resolution robustness, compact temporal-FSM reduction, heterogeneous-delay SNNs, and the candidate #35 local-adaptation reduction. This run does not recycle those findings. It asks a different question motivated by R8/R92: **what does established system-identification and hybrid-dynamics literature say about when an intervention is actually informative, and how simply can a local delay-sensitive response be explained once causal opportunity exists?**

## High-value new findings

### 1. Causal opportunity is necessary, but perturbation *informativity* is the stronger modern bar

**External literature fact.** Ogino, Sekizawa, Kitazono & Oizumi's eLife Reviewed Preprint v2, revised 9 September 2026, studies perturbation design for neural system identification. Their central result is that passive activity can fail to reveal weak/latent dynamical modes, while perturbation inputs improve identification only when their spatial/frequency structure actually excites the relevant modes. High stimulation intensity alone is not enough: an input can strongly excite already-dominant directions while leaving weak modes poorly identified. Their optimization therefore targets information gain / estimation error through the covariance structure of the perturbed dynamics.

Source:
- Ogino, Sekizawa, Kitazono & Oizumi, *Designing optimal perturbation inputs for system identification in neuroscience*, eLife Reviewed Preprint v2, 9 Sep 2026. https://doi.org/10.7554/eLife.110030.2

**Repository relevance / inference.** R92's candidate #34 repair is methodologically pointed in the right direction: the source must actually fire, the tested destination must not simply be directly threshold-driven, and the edge must have a physical opportunity to influence a measured state. The new literature sharpens the next distinction: **`causal opportunity exists` does not imply `the chosen perturbation is informative for the scientific quantity being claimed`**. A source-only pulse can establish an opportunity path yet still mainly excite a direction already determined by local state, or weakly probe the route feature of interest.

**Prospective discriminator.** Do not rewrite current R2 from this literature. For a fresh successor or later confirmatory object only, prospectively define the exact quantity to identify and require a claim-scoped lower bound on perturbation informativeness/sensitivity for both target and matched controls before interpreting a null as evidence against a mechanism. The bound need not identify the full system; it should only show that the frozen perturbation can actually distinguish the alternatives named in the claim.

### 2. Full persistent excitation is often unnecessarily strong; use *claim-scoped data informativity*, not maximal excitation

**External literature fact.** van Waarde, Eising, Trentelman & Camlibel's data-informativity framework separates unique system identification from narrower analysis/control questions. Persistent excitation is a strong condition that can identify the whole dynamical system, but it is not necessary for every scientifically relevant property: some questions can be answered from data that are informative for that property even when the underlying system is not uniquely identified.

Source:
- van Waarde, Eising, Trentelman & Camlibel, *Data informativity: a new perspective on data-driven analysis and control*, IEEE Transactions on Automatic Control 65(11), 2020. Preprint: https://arxiv.org/abs/1908.00468

**Repository relevance / inference.** This prevents an overcorrection after Audit R8. Candidate #34 currently asks a bounded development question about physical influence of a tested edge under a fixed source-only cue, not for full reconstruction of every SparkBrain dynamical mode. Requiring global persistent excitation or whole-network identifiability would therefore add an unnecessary gate and change the object. The right future standard is narrower: sufficient information to distinguish the exact route-effect alternatives the claim names.

**Prospective discriminator.** For future route claims, specify `estimand/alternative set -> minimum informative observable/perturbation condition`. A broad topology or irreducibility claim needs correspondingly broader excitation/separation; a local edge-effect claim may be supported by a much smaller claim-specific condition.

### 3. Arrival-time sensitivity can reduce to ordinary local phase/refractory/adaptation dynamics

**External literature fact.** Gutkin, Ermentrout & Reyes show with neuronal phase-response curves (PRCs) that the effect of a transient synaptic input depends strongly on *when* it arrives in the neuron's firing cycle. The same weak input can have near-zero, positive, or negative influence on the next spike depending on local phase, firing rate, afterhyperpolarization and adaptation. Thus timing-dependent influence can be explained by a low-dimensional local state-response map rather than by a higher-order distributed representation.

Source:
- Gutkin, Ermentrout & Reyes, *Phase-response curves give the responses of neurons to transient inputs*, Journal of Neurophysiology 94(2), 2005. https://doi.org/10.1152/jn.00359.2004

**Repository relevance / inference.** Candidate #34 R2 now makes destination membrane potential and spike state around nominal/+1ms arrival primary observables. That is scientifically cleaner than the prior direct-threshold replay, but it also makes an ordinary local explanation especially relevant: a +1ms effect may arise because the arrival crosses a local threshold/refractory/adaptation sensitivity region. SparkBrain's exact field is not a classical periodically firing biological neuron, so PRC theory is a reduction *analogy/baseline family*, not a theorem about the implementation.

**Prospective discriminator.** For any future broader Assembly-route claim, compare the observed edge-delay effect with a prospectively frozen local destination-state response map using only the same allowed local variables (potential, threshold/adaptation/refractory state, edge weight and arrival time). If that local map predicts the effect, the evidence supports ordinary local hybrid dynamics rather than an irreducible Assembly route mechanism.

### 4. Event-driven spike sensitivity itself has an established exact mathematical treatment

**External literature fact.** Wunderlich & Pehle's EventProp computes exact gradients through discrete spike events in recurrent leaky-integrate-and-fire networks by combining adjoint dynamics with derivative jumps at spike times; reported gradients match central finite differences to relative error below `1e-7`. More generally, saltation matrices are the standard sensitivity update across discontinuities in hybrid dynamical systems and are explicitly used in computational neuroscience.

Sources:
- Wunderlich & Pehle, *Event-based backpropagation can compute exact gradients for spiking neural networks*, Scientific Reports 11, 12829 (2021). https://doi.org/10.1038/s41598-021-91786-z
- Kong, Payne, Zhu & Johnson, *Saltation Matrices: The Essential Tool for Linearizing Hybrid Dynamical Systems*, Proceedings of the IEEE 112(6), 2024. https://doi.org/10.1109/JPROC.2024.3440211

**Repository relevance / inference.** R35 established that delay-defined routes have close polychronous/synfire prior art. The stronger reduction introduced here is mathematical rather than architectural: if a small edge-delay/weight perturbation's downstream effect is accurately predicted by the ordinary local/event sensitivity of the existing hybrid field, then a causal response does not by itself demonstrate a distinct Assembly-level mechanism. Conversely, a reproducible residual beyond such a matched sensitivity model would raise the mechanism bar more meaningfully than simply observing a changed spike bin.

**Prospective discriminator.** In a fresh successor only, use a local hybrid sensitivity / event-Jacobian / saltation-style predictor with the same state and parameter privilege as the native system. This should be treated as an ordinary reduction baseline, not added to the current R2 contract after it has been prospectively specified.

## Synthesis

The new methodological ladder for candidate #34 is:

`physical causal opportunity` -> `claim-scoped perturbation informativity` -> `ordinary local phase/state sensitivity` -> `hybrid event-sensitivity prediction` -> `only then any broader Assembly-route residual`.

This does **not** invalidate R92's R2 direction and does not justify stopping the current development line. In fact, the 2026 perturbation-design literature independently supports the move away from a direct-threshold replay toward a source-only, opportunity-aware intervention. The new bar is narrower and prospective: later broad claims should not equate `the edge had an opportunity` with `the experiment was informative for all route/mechanism alternatives`, and a small timing effect should first survive ordinary local/hybrid sensitivity explanations.

No current scientific result exists on the new R2 surface. The `a134513...` repository movement happened after R41/R92/MAIN's recorded snapshot and remains non-result development work. Its failed dedicated non-result workflow and in-progress generic CI are implementation/control-plane matters for MAIN/Analyst reconciliation, not evidence to be interpreted by this role.

No Utility request is created. MAIN already owns the candidate #34 pre-result contract surface; injecting a new sensitivity prototype now would risk contaminating the active prospective choice. These discriminators belong to a fresh successor or later prospective object if Evidence Analyst/Control Brain decide the claim requires them.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - CAND34_CAUSAL_OPPORTUNITY_VS_INFORMATIVITY
  - CAND34_CLAIM_SCOPED_PERTURBATION_DESIGN
  - CAND34_LOCAL_PHASE_STATE_REDUCTION
  - CAND34_HYBRID_EVENT_SENSITIVITY_REDUCTION
  - CAND34_PREFORMAL_R2_INTERPRETATION_CEILING
  - FUTURE_MECHANISM_SUCCESSOR_ADMISSION
  - PROGRAMME_NOVELTY
novelty_or_reduction_impact: >
  CAUSAL_OPPORTUNITY_IS_NECESSARY_BUT_NOT_SUFFICIENT_FOR_BROAD_MECHANISM_IDENTIFICATION.
  Modern perturbation-design work supports opportunity-aware intervention but adds a
  claim-scoped informativity requirement; ordinary local phase/refractory dynamics and
  hybrid event sensitivity are stronger prospective reductions for small delay effects.
  No current R2 rewrite or mechanism uplift follows.
audit_classification: null
prospective_baselines_or_discriminators:
  - fresh-successor-only claim-scoped perturbation-informativity criterion tied to the exact estimand/alternative set
  - local destination-state response map using matched potential/threshold/adaptation/refractory/arrival-time privilege
  - hybrid event-sensitivity / saltation / event-Jacobian predictor for delay/weight perturbations
  - scale excitation requirements with claim scope rather than requiring global persistent excitation for a local edge-effect claim
questions_for_evidence_analyst:
  - Keep the current R2 opportunity-aware object unchanged by this literature and treat informativity as a future claim-scoped interpretation/successor guardrail?
  - If a future R2-like null is interpreted mechanistically, require evidence that the frozen perturbation was informative for the exact alternatives being rejected, not merely physically executable?
  - Before any broad Assembly-route claim, require reduction against a local destination-state timing model or hybrid event-sensitivity predictor with matched information privilege?
questions_for_control_brain:
  - Add `causal opportunity != perturbation informativity` as a prospective claim-ceiling guardrail without creating a new gate inside active R2?
  - Keep persistent-excitation requirements proportional to claim scope so a local edge-effect question is not accidentally converted into whole-system identification?
  - Preserve all existing response/FORMAL/provenance STOP boundaries while MAIN/Analyst reconcile the new R2 repository head and workflow state?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1-v1/C19-R1-v2/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - H7 PF-R1 result/raw and no-rerun/no-rescore boundary
  - H7 R5 preidentity object and FORMAL provenance hold
  - candidate #34 PRE_FORMAL R1 prebind and its no-response provenance
  - candidate #34 current R2 opportunity-aware contract/repository work must not be rewritten because of this external literature; fresh Analyst/MAIN owns its reconciliation
  - candidate #35 remains SYSTEM-scoped; no mechanism uplift from this literature
  - no candidate response-bearing execution, PRE_FORMAL/FORMAL one-way action, identity consumption, research merge, immutable-ref mutation, Utility execution, or scheduler change by this role
utility_request_created: null
```

## Run close

Role performed: `LITERATURE_REDUCTION_SCOUT`.
Generation: `LIT-20260923T123024+0900-R36-INFORMATIVITY-HYBRID-SENSITIVITY-6D4A21C8`.
Input generations: Control R41, Evidence Analyst R92, MAIN R92 relay, Fast Forge R92, Literature R35 as enumerated above.
Genuinely new external scientific information: `true`.
Top implication: candidate #34's opportunity-aware repair is supported, but later route/mechanism interpretation must distinguish physical opportunity from claim-specific information and must first survive ordinary local/hybrid sensitivity reductions.
Affected lines: candidate #34 opportunity/informativity, local timing reduction, hybrid sensitivity reduction, future mechanism admission and programme novelty.
Utility request created: `null`.
Persistence limitation: only the role-separated literature latest/state/history paths on `ops/external-research-audit-handoff` may be changed; no scientific refs/results, legacy shared latest/state, Utility, scheduler, or research branch may be mutated.
