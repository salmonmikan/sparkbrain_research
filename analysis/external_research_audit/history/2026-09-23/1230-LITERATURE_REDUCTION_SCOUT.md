# Literature Reduction Scout — 2026-09-23 12:30 JST

- schema_version: `2`
- generation_id: `LIT-20260923T123024+0900-R36-INFORMATIVITY-HYBRID-SENSITIVITY-6D4A21C8`
- produced_at: `2026-09-23T12:30:24+09:00`
- producer_run_id: `external-literature-auto-LIT-20260923T123024+0900-R36-INFORMATIVITY-HYBRID-SENSITIVITY-6D4A21C8`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260923T093010+0900-R35-POLYCHRONY-TEMPORAL-ROBUSTNESS-4E7A21C9`
- role: `LITERATURE_REDUCTION_SCOUT`
- genuinely_new_information: `true`

## Authoritative inputs

- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- Control Brain: `CTRL-20260923T115056+0900-R41-4C156929` @ `27b6531b6b3a1d941a484aeee012d5c59fe63d79`
- Evidence Analyst: `EVA-20260923T105725+0900-R92-6B8E31D4` @ `a05ab3f655a23eabd84c910ba337d64a948c168a`
- MAIN report: `MAIN-20260923T115328+0900-RELAY-CAND34-PREFORMALR2-R92-BLOCKED-AUTHORITY-INTEGRITY` @ `0167aa75e768f51bbc37528868af569a1d054786`
- Fast Forge report: `FORGE-20260923T114344+0900-R92-RECEPTOR-SUPPRESSION-DEADENDS` @ `b2fe7ad25a356d170de1291ab0de0b7e4eec3dfe`
- prior literature: `LIT-20260923T093010+0900-R35-POLYCHRONY-TEMPORAL-ROBUSTNESS-4E7A21C9` @ `cd5069201723110acc9e15d60216c9d1f2e63ce7`
- authoritative `evidence/*`: five annotated tags unchanged; `formal/*`, `sealed/*`, `freeze/*`: empty
- H7 R5 direct head: `2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`
- candidate #34 PRE_FORMAL R1 remains preserved no-result prebind at `2de73b9d0f21a2e8f07b43ca517b5247e6a7dfd0`

R92 accepts Audit R8's causal-opportunity defect and authorizes only an opportunity-aware same-candidate PRE_FORMAL R2 revision, with fresh READY review required before any response. During this scout, the direct R2 branch advanced to `a134513838d8f30013d904a95a61cfbcf9454eaa`, aligning the source-only cue/opportunity contract to canonical R92. That repository movement is NON_RESULT and not yet a fresh Analyst disposition. The exact-head dedicated non-result contract workflow `35814833603` completed `failure`; generic CI `35814833574` remained in progress at observation. No scientific response was exposed.

## New high-value findings

### 1. Opportunity is not the same as perturbation informativity

Ogino et al.'s eLife Reviewed Preprint v2 (9 Sep 2026) develops optimal perturbation design for neural system identification. Perturbations reveal weak/latent dynamics only when their spatial/frequency pattern excites the relevant modes; high intensity alone can leave weak modes uninformative.

Source: Ogino, Sekizawa, Kitazono & Oizumi, *Designing optimal perturbation inputs for system identification in neuroscience*, eLife Reviewed Preprint v2. https://doi.org/10.7554/eLife.110030.2

Implication: R92's source-only opportunity-aware repair is methodologically supported, but a future broad null/causal interpretation needs more than physical executability. The frozen perturbation must be informative for the exact alternatives being rejected. Do not retrofit this as a new gate into current R2.

### 2. Informativity should scale with claim scope

van Waarde et al.'s data-informativity framework shows that full persistent excitation/unique whole-system identification is stronger than necessary for many narrower analysis questions.

Source: van Waarde, Eising, Trentelman & Camlibel, *Data informativity: a new perspective on data-driven analysis and control*, IEEE TAC 65(11), 2020. https://arxiv.org/abs/1908.00468

Implication: candidate #34's bounded local edge-effect question should require claim-specific informativeness, not global persistent excitation. Broader topology/irreducibility claims would need broader separating information.

### 3. Delay sensitivity has a low-dimensional local-state reduction

Gutkin, Ermentrout & Reyes show via neuronal phase-response curves that the same weak transient input can have near-zero, positive, or negative spike-timing influence depending on local phase, firing rate, afterhyperpolarization and adaptation.

Source: Gutkin, Ermentrout & Reyes, *Phase-response curves give the responses of neurons to transient inputs*, J Neurophysiol 94(2), 2005. https://doi.org/10.1152/jn.00359.2004

Implication: a future candidate-#34 `+1ms` effect may reduce to a local destination-state timing map using potential/threshold/adaptation/refractory/arrival-time information, rather than requiring an irreducible Assembly-route explanation. This is a prospective baseline family; SparkBrain is not assumed to be a classical oscillator.

### 4. Event-driven hybrid sensitivity is established ordinary machinery

EventProp computes exact gradients through spike-event discontinuities in recurrent LIF networks, and saltation matrices provide the general sensitivity update at hybrid jumps.

Sources:
- Wunderlich & Pehle, *Event-based backpropagation can compute exact gradients for spiking neural networks*, Scientific Reports 11, 12829 (2021). https://doi.org/10.1038/s41598-021-91786-z
- Kong, Payne, Zhu & Johnson, *Saltation Matrices: The Essential Tool for Linearizing Hybrid Dynamical Systems*, Proceedings of the IEEE 112(6), 2024. https://doi.org/10.1109/JPROC.2024.3440211

Implication: in a fresh successor, test whether a matched local/event sensitivity model predicts the edge-delay/weight intervention effect. A residual beyond that is more informative for mechanism novelty than a timing shift alone.

## Synthesis

Prospective ladder:

`physical causal opportunity` -> `claim-scoped perturbation informativity` -> `local phase/state response reduction` -> `hybrid event-sensitivity reduction` -> `broader Assembly-route residual`.

This literature does not invalidate or rewrite current R2. It independently supports R92's opportunity-aware direction while raising a later interpretation/reduction bar. No Utility request is created because MAIN already owns the active pre-result surface and inserting a new diagnostic now could contaminate prospective choices.

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
audit_classification: null
prospective_baselines_or_discriminators:
  - fresh-successor-only claim-scoped perturbation-informativity criterion
  - local destination-state timing-response model with matched information privilege
  - hybrid event-sensitivity / saltation / event-Jacobian predictor
  - excitation requirements proportional to claim scope rather than global persistent excitation by default
questions_for_evidence_analyst:
  - Keep active R2 unchanged by this literature and treat informativity as a later interpretation/successor guardrail?
  - Require future mechanistic nulls to establish informativity for the exact rejected alternatives, not merely physical opportunity?
  - Require local-state/hybrid-sensitivity reduction before broad Assembly-route claims?
questions_for_control_brain:
  - Add `causal opportunity != perturbation informativity` as a prospective claim ceiling without changing active R2?
  - Keep excitation requirements proportional to claim scope?
  - Preserve existing response/FORMAL/provenance STOP boundaries during R2 reconciliation?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1-v1/C19-R1-v2/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - H7 PF-R1 no-rerun/no-rescore boundary and H7 R5 provenance hold
  - candidate #34 R1 prebind/no-response provenance
  - candidate #34 current R2 repository work must not be rewritten because of this literature
  - candidate #35 remains SYSTEM-scoped
  - no response-bearing execution, one-way identity, research merge, immutable-ref mutation, Utility execution, or scheduler change by this role
utility_request_created: null
```

## Run close

Role performed: `LITERATURE_REDUCTION_SCOUT`.
Generation: `LIT-20260923T123024+0900-R36-INFORMATIVITY-HYBRID-SENSITIVITY-6D4A21C8`.
Input generations: Control R41 / Evidence Analyst R92 / MAIN R92 relay / Fast Forge R92 / Literature R35.
Genuinely new external scientific information: `true`.
Top implication: opportunity-aware intervention is necessary, but later mechanism claims must distinguish physical opportunity from claim-specific information and survive ordinary local/hybrid sensitivity reductions.
Affected lines: candidate #34 opportunity/informativity, local timing reduction, hybrid sensitivity reduction, future mechanism admission, programme novelty.
Utility request created: `null`.
Persistence limitation: literature latest/state/history only; no scientific refs/results, research branches, Utility, scheduler, or legacy shared latest/state changed.
