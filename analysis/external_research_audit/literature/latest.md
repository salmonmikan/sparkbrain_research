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

Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. Authoritative `evidence/*` remains five annotated tags; tag-form `formal/*`, `sealed/*`, and `freeze/*` remain empty. Preserve/control refs, consumed identities, relevant PRs and workflows were independently inspected.

Consumed control-plane generations:
- Control Brain: `CTRL-20260923T115056+0900-R41-4C156929` @ `27b6531b6b3a1d941a484aeee012d5c59fe63d79`
- Evidence Analyst: `EVA-20260923T105725+0900-R92-6B8E31D4` @ `a05ab3f655a23eabd84c910ba337d64a948c168a`
- MAIN: `MAIN-20260923T115328+0900-RELAY-CAND34-PREFORMALR2-R92-BLOCKED-AUTHORITY-INTEGRITY` @ `0167aa75e768f51bbc37528868af569a1d054786`
- Fast Forge: `FORGE-20260923T114344+0900-R92-RECEPTOR-SUPPRESSION-DEADENDS` @ `b2fe7ad25a356d170de1291ab0de0b7e4eec3dfe`
- Prior Literature: `LIT-20260923T093010+0900-R35-POLYCHRONY-TEMPORAL-ROBUSTNESS-4E7A21C9` @ `cd5069201723110acc9e15d60216c9d1f2e63ce7`

R92 remains canonical. It accepts Audit R8's causal-opportunity defect in candidate #34 PRE_FORMAL R1, preserves R1 unchanged, and permits only an opportunity-aware same-candidate R2 revision with fresh READY review before response-bearing execution.

Repository movement occurred after those mailbox generations. Candidate #34 R2 now ends at `research/main-cand34-assembly-route-preformal-r92-cycle4@43d0f25541a3c447d4c7156303647ae94f3119f4`. The science-affecting implementation is at parent `a134513...`; the final commit changes only tests for the canonical opportunity-aware closure. The R2 source binds canonical R92, uses source-only cues, never directly cues the tested destination, predeclares target/control opportunity metadata, records destination potential/spike state around nominal and +1ms arrival, keeps Assembly response secondary, limits scope to development-only physical route influence, and leaves response execution disabled pending fresh Analyst review. Exact-head non-result workflow `35814951495` and generic CI `35814951496` both completed `success`. No candidate response, PRE_FORMAL scientific result, FORMAL action, or scientific evidence was produced. Evidence Analyst remained R92 after this movement, so the head is repository evidence awaiting fresh canonical disposition.

R35 already covered synfire/polychronous prior art, timing-resolution robustness, temporal-FSM reduction and heterogeneous-delay SNNs. This run adds a different layer: **when is an intervention actually informative, and can a delay-sensitive effect reduce to ordinary local/hybrid sensitivity once physical opportunity exists?**

## High-value new findings

### 1. Physical opportunity is not the same as perturbation informativity

Ogino, Sekizawa, Kitazono & Oizumi's eLife Reviewed Preprint v2 (revised 9 Sep 2026) shows that perturbation-based neural system identification improves when input spatial/frequency structure excites otherwise weak or latent dynamical modes; strong stimulation alone can still leave important modes poorly identified.

Source: *Designing optimal perturbation inputs for system identification in neuroscience*, eLife Reviewed Preprint v2. https://doi.org/10.7554/eLife.110030.2

**Impact.** R92's source-only opportunity-aware repair is directionally supported, but later broad interpretation needs a stricter distinction: an edge can have a physical opportunity to act while the frozen perturbation is still weakly informative for the exact scientific alternatives being compared. Do not retrofit a new gate into current R2; for a fresh successor, prospectively bind the exact estimand/alternative set and a claim-scoped informativity/sensitivity condition before treating a null as mechanistic evidence.

### 2. Full persistent excitation is often too strong; informativity should scale with claim scope

van Waarde, Eising, Trentelman & Camlibel show that persistent excitation sufficient for unique whole-system identification is not necessary for every narrower analysis/control property.

Source: *Data informativity: a new perspective on data-driven analysis and control*, IEEE TAC 65(11), 2020. https://arxiv.org/abs/1908.00468

**Impact.** Candidate #34's bounded local edge-effect question should not be converted into a whole-network system-identification task. The future requirement should be the minimum information needed to distinguish the exact alternatives named by the claim; broader topology or irreducibility claims require correspondingly broader excitation/separation.

### 3. Arrival-time effects can reduce to a low-dimensional local state response

Gutkin, Ermentrout & Reyes show with neuronal phase-response curves that the same weak transient input can have near-zero, positive, or negative spike-timing effect depending on arrival phase, firing rate, afterhyperpolarization and adaptation.

Source: *Phase-response curves give the responses of neurons to transient inputs*, J Neurophysiol 94(2), 2005. https://doi.org/10.1152/jn.00359.2004

**Impact.** Candidate #34 R2 now measures destination membrane/spike state around edge arrival, making a matched local explanation particularly relevant. A future +1ms effect may be explainable by potential/threshold/adaptation/refractory/arrival-time state without an irreducible Assembly mechanism. PRC theory is a prospective baseline family, not a theorem about SparkBrain's exact field.

### 4. Event-driven spike sensitivity has established ordinary mathematics

EventProp computes exact gradients through spike-event discontinuities in recurrent LIF networks, while saltation matrices are the standard sensitivity update at hybrid jumps and are used in computational neuroscience.

Sources:
- Wunderlich & Pehle, *Event-based backpropagation can compute exact gradients for spiking neural networks*, Scientific Reports 11, 12829 (2021). https://doi.org/10.1038/s41598-021-91786-z
- Kong, Payne, Zhu & Johnson, *Saltation Matrices: The Essential Tool for Linearizing Hybrid Dynamical Systems*, Proceedings of the IEEE 112(6), 2024. https://doi.org/10.1109/JPROC.2024.3440211

**Impact.** In a fresh successor, a matched local event-Jacobian/saltation-style predictor can test whether ordinary hybrid sensitivity already predicts the delay/weight intervention response. A residual beyond that is a stronger mechanism discriminator than a changed timing observable alone.

## Synthesis

Prospective ladder:

`physical causal opportunity` -> `claim-scoped perturbation informativity` -> `local phase/state response reduction` -> `hybrid event-sensitivity reduction` -> `broader Assembly-route residual`.

This literature does **not** invalidate or rewrite active R2 and provides no mechanism uplift. It independently supports the move away from direct-threshold replay toward opportunity-aware intervention while raising the bar for later interpretation. Current R2 remains a non-result development object awaiting fresh Analyst disposition despite exact-head CI/contract success.

No Utility request is created; MAIN already owns the active pre-result surface, and inserting a new sensitivity prototype now could contaminate prospective choices.

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
  Opportunity-aware intervention is supported, but broad interpretation requires
  claim-scoped informativity and should first survive ordinary local/hybrid sensitivity reductions.
  No current R2 rewrite or mechanism uplift follows.
audit_classification: null
prospective_baselines_or_discriminators:
  - fresh-successor-only claim-scoped perturbation-informativity criterion tied to the exact estimand/alternative set
  - local destination-state response map with matched potential/threshold/adaptation/refractory/arrival-time privilege
  - hybrid event-sensitivity / saltation / event-Jacobian predictor
  - excitation requirements proportional to claim scope rather than global persistent excitation by default
questions_for_evidence_analyst:
  - Keep current R2 unchanged by this literature and treat informativity as a future claim-scoped interpretation/successor guardrail?
  - If a future R2-like null is interpreted mechanistically, require evidence that the frozen perturbation was informative for the exact rejected alternatives, not merely physically executable?
  - Before broad Assembly-route claims, require reduction against a matched local destination-state timing model or hybrid event-sensitivity predictor?
questions_for_control_brain:
  - Add `causal opportunity != perturbation informativity` as a prospective claim ceiling without adding a gate inside active R2?
  - Keep excitation requirements proportional to claim scope?
  - Preserve all current response/FORMAL/provenance STOP boundaries while fresh Analyst disposition catches up to the new R2 head?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1-v1/C19-R1-v2/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - H7 PF-R1 no-rerun/no-rescore boundary and H7 R5 provenance hold
  - candidate #34 PRE_FORMAL R1 prebind/no-response provenance
  - candidate #34 current R2 opportunity-aware repository work must not be rewritten because of this literature
  - candidate #35 remains SYSTEM-scoped
  - no response-bearing execution, one-way identity, research merge, immutable-ref mutation, Utility execution, or scheduler change by this role
utility_request_created: null
```

## Run close

Role performed: `LITERATURE_REDUCTION_SCOUT`. Genuinely new external scientific information: `true`. Top implication: opportunity-aware intervention is necessary, but later mechanism interpretation must distinguish physical opportunity from claim-specific information and survive ordinary local/hybrid sensitivity reductions. Utility request: none. Persistence is limited to the role-separated literature latest/state/history paths; no scientific refs/results, research branches, legacy shared latest/state, Utility or scheduler were changed.
