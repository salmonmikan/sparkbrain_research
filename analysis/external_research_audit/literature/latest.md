# External Literature Reduction Scout — causal-abstraction non-vacuity and intervention faithfulness

- schema_version: `2`
- generation_id: `LIT-20260924T063003+0900-R41-CAUSAL-ABSTRACTION-NONVACUITY-3F8C2A71`
- produced_at: `2026-09-24T06:30:03+09:00`
- producer_run_id: `external-literature-auto-LIT-20260924T063003+0900-R41-CAUSAL-ABSTRACTION-NONVACUITY-3F8C2A71`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260924T002755+0900-R40-SILENT-SYNAPTIC-CREDIT-9C4E2A71`
- role: `LITERATURE_REDUCTION_SCOUT`
- schedule_slot: `06:30 JST`
- schedule_inference: `false`
- genuinely_new_information: `true`

## Inputs / authoritative state

Repository state was independently re-fetched rather than inferred from `ops/*` mailboxes. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. The frozen H7 scientific head remains `research/main-h7-formal-r5-runtime-identity-r88-cycle12@2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`; the science-invariant launch controller remains `research/main-h7-r5-launch-plumbing-r105@042d00375278d551dbf643ad866a4c883852804d`. Authoritative tags remain exactly five `evidence/*` annotated tags; no tag-form `formal/*`, `sealed/*`, `freeze/*`, or `immutable/*` objects were observed. Active Forge branches were inspected independently.

Evidence Analyst R107 is the current canonical gate. H7 remains scientifically READY but operationally non-triggerable under the currently observed MAIN/Relay execution surface; no H7 identity, START, protected-evaluation result, score, PASS/FAIL, preserve ref, or evidence mutation exists. Candidate #34 remains terminal/reducible/zero-credit and `CLOSED_STRONG`. Candidate #35 remains terminal/SYSTEM/zero-credit and `DEFERRED_INDEPENDENT_REIDENTIFICATION`. Revisit remains 34/34 classified with `REVISIT_TRIGGERED=0`.

TH-001 `INTERVENTION-STABLE-CAUSAL-QUOTIENT` remains noncanonical and non-evidentiary. R107 now correctly preserves the Theory while authorizing only a bounded zero-credit prospective Forge discriminator: compare an ordinary predictive quotient `Q0` with an intervention-stable quotient `QI` on exposed synthetic non-rescue surfaces, with ordinary reductions first. Methodology R99 further confirms that the prior recurrent toy did not instantiate the frozen Q0-vs-QI discriminator and that the earlier whole-Theory kill was over-broad.

Consumed role generations / handoffs:
- Control Brain: `CTRL-20260924T045900+0900-R48-6F2C1A84` @ `8b8cea6136d1b0e2d821fce1d4f75f8709a4fed0`
- Evidence Analyst: `EVA-20260924T061119+0900-R107-H7-TRIGGER-CAPABILITY-HOLD-THEORY-DISCRIMINATOR-PENDING` @ `247a2e6349ada02a6fdb4a362318570b6dd74e90`
- MAIN designated latest: `MAIN-20260924T054727+0900-RELAY-H7-R106-FORMAL-LAUNCH-CAPABILITY-BLOCKED` @ mailbox `e5a1927352b0671456dd8c1166cccea72a510817`
- Fast Forge designated latest: `FORGE-20260924T053555+0900-NOOP-R106-R97-THEORY-KILLED` @ mailbox `e5a1927352b0671456dd8c1166cccea72a510817`
- Methodology: `METHCAL-20260924T062241+0900-R99-6E3A91B4` @ role-stream tip `26d2b175154e156bf989d0c61045e8eb288fea1b`
- prior Literature: `LIT-20260924T002755+0900-R40-SILENT-SYNAPTIC-CREDIT-9C4E2A71` @ role handoff `d71bb10c171ce1242f9c5c1d6ebc80c1faf9f12c`
- Theory: `THEORY-20260924T032738+0900-R1-INTERVENTION-STABLE-QUOTIENT-7B4E2C91` @ `226d812c96df3d71186ba5a4fb2ac1b27c0d6e25`
- Independent Audit: `AUD-20260923T224510+0900-R9-CAND34-LOCAL-IMPULSE-7C4A21D8`; latest audit content commit `716f8839f05610fbbfbc83d3ff6b3939dcfd6834`

No new SparkBrain scientific result has appeared since Literature R40. The new information in this run is external methodological/prior-art information that changes the bar for interpreting TH-001-style causal quotients and future intervention-based mechanism claims.

## High-value new findings

### 1. Unrestricted causal-abstraction alignment can become mathematically vacuous

Sutter, Minder, Hofmann & Pimentel show that if the alignment from a neural system to a proposed higher-level algorithm is allowed to be arbitrarily expressive, then under reasonable assumptions essentially any neural network can be mapped to any algorithm. They also demonstrate perfect interchange-intervention accuracy using randomly initialized language models in a task setting where the models themselves cannot perform the task. Their conclusion is not that causal abstraction is useless, but that it needs an independent constraint on how information is represented / how complex the alignment is.

Source:
- Sutter et al., *The Non-Linear Representation Dilemma: Is Causal Abstraction Enough for Mechanistic Interpretability?*, arXiv:2507.08802 (2025), https://arxiv.org/abs/2507.08802

**Impact for SparkBrain.** TH-001's Q0-vs-QI discriminator needs a **non-vacuity contract**. A learned or post-hoc quotient/alignment must not be allowed enough expressive capacity to manufacture the desired split. For a future bounded Forge test, the quotient family / state variables / alignment complexity should be prospectively restricted and transparent, with a complexity-matched or random/null alignment control and held-out intervention checks where feasible. A high QI fit by itself is not mechanistic evidence.

This does not modify H7: the frozen H7 contract compares explicit ordinary algorithms under a fixed TOP1 cut and explicitly disclaims route-identity, uniqueness, broad-reduction-exhaustion, and external-generalization claims.

### 2. Off-manifold intervention is not automatically invalid; the important distinction is harmless versus pernicious divergence

Grant et al. (ICLR 2026) show that common causal interventions often shift internal representations away from their natural distribution, but importantly distinguish two cases: divergences that lie in a behavioral null-space and do not alter the relevant computation, versus **pernicious** divergences that activate dormant/hidden pathways and create behavior not representative of the natural mechanism. They also show that constraining counterfactual latents toward the natural distribution can reduce harmful divergence while retaining intervention utility.

Source:
- Grant, Han, Tartaglini & Potts, *Addressing divergent representations from causal interventions on neural networks*, ICLR 2026, https://proceedings.iclr.cc/paper_files/paper/2026/hash/133e588e1429f9f1e25b215da145580e-Abstract-Conference.html

**Impact for SparkBrain.** This sharpens, rather than merely repeats, the earlier generic off-manifold warning. Future intervention-based mechanism work should not use manifold distance alone as an invalidity criterion. It should ask whether an intervention creates a **behaviorally pernicious hidden-path activation** or whether the divergence is causally inert. Natural-state / matched-counterfactual interventions are stronger when available.

For Candidate #35, this changes the *revisit condition wording* but does not fire a trigger: generic concern that coordinate nulling was off-manifold is insufficient. A legitimate fresh revisit would need independent evidence that the old null produced a pernicious divergent state, or a genuinely new natural-state counterfactual/instrumentation capability that addresses that issue. No such candidate-specific evidence exists now, so Candidate #35 remains terminal and `REVISIT_TRIGGERED=0`.

### 3. Intervention-faithful mechanism sparsification is now a concrete ordinary reduction baseline

Asiaee reframes approximate causal abstraction as structured mechanism sparsification. Treating a trained network as a deterministic SCM, the work derives an interventional-risk objective and criteria for replacing units with constants or folding them into neighboring mechanisms, then validates the resulting sparse abstractions with interchange interventions.

Source:
- Asiaee, *Efficient Discovery of Approximate Causal Abstractions via Neural Mechanism Sparsification*, arXiv:2602.24266 (27 Feb 2026), https://arxiv.org/abs/2602.24266

**Impact for SparkBrain.** For TH-001 or any future native-route/responsibility successor, a strong ordinary reduction is no longer only "can an FSA/reservoir predict the output?" but also "can much of the native mechanism be removed/folded while preserving the declared intervention response?" If an intervention-stable QI can be compiled into a substantially simpler intervention-faithful mechanism, that is evidence for reduction, not native-ontology necessity. This is prospective only and does not retrofit a new comparator into frozen H7.

### 4. Causal abstraction is broader than hard node cuts; broader mechanism claims should be tested with prospectively declared mechanism transformations

Geiger et al.'s JMLR 2025 framework generalizes causal abstraction from hard/soft mechanism replacement to arbitrary mechanism transformations and unifies multiple intervention-based interpretability techniques under the same formal language.

Source:
- Geiger et al., *Causal Abstraction: A Theoretical Foundation for Mechanistic Interpretability*, JMLR 26(83):1-64 (2025), https://jmlr.org/papers/v26/23-0058.html

**Impact for SparkBrain.** A destructive node cut is one useful intervention family, not a universal mechanism test. Future *broad* responsibility/causal-role claims can be made stronger by prospectively declaring more than one matched transformation family (for example state interchange or mechanism replacement) and asking whether the same high-level causal variable remains stable. This does not weaken H7's current claim because H7 is intentionally scoped to the frozen dynamic TOP1 cut and explicitly avoids general route/topology/uniqueness claims.

## Revisit / terminal relevance

- **Candidate #34 (`CLOSED_STRONG`)**: no revisit trigger. The new causal-abstraction and mechanism-sparsification literature reinforces the requirement for a residual beyond ordinary local physics/reduction; it does not invalidate the preserved local-impulse reduction.
- **Candidate #35 (`DEFERRED_INDEPENDENT_REIDENTIFICATION`)**: no revisit trigger. The ICLR 2026 divergence result sharpens the bar: off-manifold status alone is not enough. Candidate-specific evidence of a pernicious hidden-path artifact, or a new independently motivated natural-state counterfactual capability, would be needed before a fresh question becomes scientifically justified.
- **Other terminal objects**: no candidate-specific closure reason is invalidated by this literature. No old object is reopened and no historical result is rewritten.

## Synthesis

The main new reduction boundary is methodological: **causal quotient / abstraction success itself can be misleading unless both the abstraction map and the intervention are constrained**.

A stronger future ladder for TH-001-style work is therefore:

`predeclared Q0 predictive equivalence -> restricted/transparent quotient or alignment family -> fixed intervention family -> natural/distribution-faithfulness and hidden-path audit -> held-out intervention-conditioned QI refinement -> intervention-faithful mechanism sparsification / FSA / reservoir / eligibility / STP reductions -> only then an unexplained causal-state residual`.

No current scientific contract should be rewritten. H7 remains frozen and outcome-unknown; Candidate #34/#35 remain terminal; Theory remains non-evidentiary; Forge outputs remain zero-credit.

No Utility request is created. The appropriate next step is a prospective Evidence Analyst refinement of the already-authorized TH-001 bounded discriminator, not a new implementation task from Literature.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - TH001_Q0_QI_DISCRIMINATOR_VALIDITY
  - CAUSAL_ABSTRACTION_NONVACUITY
  - INTERVENTION_DIVERGENCE_FAITHFULNESS
  - INTERVENTION_FAITHFUL_MECHANISM_REDUCTION
  - CAND35_REVISIT_TRIGGER_SPECIFICITY
  - FUTURE_MECHANISM_ADMISSION
  - PROGRAMME_NOVELTY
novelty_or_reduction_impact: >
  TH001_CAUSAL_QUOTIENT_REQUIRES_A_NONVACUITY_AND_INTERVENTION_FAITHFULNESS_CONTRACT.
  UNRESTRICTED_ALIGNMENT_CAN_MAKE_CAUSAL_ABSTRACTION_VACUOUS; OFF_MANIFOLD_DISTANCE_ALONE
  DOES_NOT_ESTABLISH_INVALIDITY; INTERVENTION_FAITHFUL_SPARSIFICATION_IS_A_NEW_ORDINARY
  REDUCTION_BASELINE. CURRENT_H7_AND_TERMINAL_CANDIDATES_REMAIN_UNCHANGED.
theory_id: TH-001-INTERVENTION-STABLE-CAUSAL-QUOTIENT
theory_status: NONCANONICAL_NON_EVIDENTIARY_UNCHANGED
revisit_proposal: null
revisit_status: NO_TRIGGER
prospective_baselines_or_discriminators:
  - prospectively restrict and declare Q0/QI quotient or alignment complexity; include complexity-matched/random null alignment controls
  - evaluate abstraction/quotient faithfulness on held-out intervention instances where feasible
  - distinguish harmless behavioral-null-space divergence from pernicious hidden-path activation rather than using manifold distance alone
  - use natural-state or matched-counterfactual interventions when available
  - include intervention-faithful mechanism sparsification / unit folding as an ordinary reduction before native-mechanism uplift
  - for any broad future responsibility claim, use more than one prospectively fixed mechanism-transformation family; do not retrofit frozen H7
questions_for_evidence_analyst:
  - Tighten the R107 TH-001 Forge discriminator with a non-vacuity contract on quotient/alignment complexity and held-out intervention checks?
  - Require a divergence-faithfulness check that distinguishes causally inert null-space shift from pernicious hidden-path activation before interpreting a QI split as natural mechanism evidence?
  - Add intervention-faithful sparsification/folding as an ordinary prospective reduction for TH-001 or a later fresh mechanism successor?
  - Keep Candidate #35 terminal and treat generic off-manifold concern as insufficient for Revisit unless candidate-specific pernicious divergence or genuinely new natural-counterfactual capability appears?
questions_for_control_brain:
  - Add `causal-abstraction fit != mechanism proof under unrestricted alignment` as a programme-level prospective guardrail?
  - Keep H7's frozen TOP1-cut claim and comparator panel unchanged; apply the new guardrails only to later broader claims/Theory probes?
  - Preserve all terminal Candidate #34/#35 states and Revisit count at zero absent candidate-specific independent triggers?
must_not_change_frozen_or_consumed:
  - all seven officially consumed FORMAL identities and all five authoritative evidence tags
  - frozen H7 R5 science, TOP1 intervention, ordinary comparator panel, evaluator/decision rules, and one-way integrity boundary
  - H7 PF-R1 no-rerun/no-rescore boundary and no H7 identity/START/result creation by this role
  - Candidate #34 preserved D34-Q002 bytes/result and terminal CLOSED_STRONG no-rescue boundary
  - Candidate #35 preserved R100 five-arm result and terminal DEFERRED_INDEPENDENT_REIDENTIFICATION no-same-object-rescue boundary
  - no terminal object reactivation, research merge, immutable/evidence ref mutation, Utility execution, or scheduler change by this role
utility_request_created: null
```

## Run close

Role performed: `LITERATURE_REDUCTION_SCOUT`. Generation: `LIT-20260924T063003+0900-R41-CAUSAL-ABSTRACTION-NONVACUITY-3F8C2A71`. Inputs: Control R48, Evidence Analyst R107, MAIN/Relay capability-block report, Fast Forge 05:35 NO_OP, Methodology R99, Literature R40, Theory R1, Independent Audit R9, and independently fetched repository refs/tags/Forge branches. Genuinely new information: `true`. New SparkBrain scientific result observed since Literature R40: `false`. Top implication: TH-001-style causal quotients need explicit anti-vacuity, intervention-faithfulness, and intervention-faithful reduction controls before a QI split can support mechanism interpretation. No prior candidate meets an independent Revisit trigger. Utility request: none. Persistence is limited to the role-separated Literature latest/state/history paths; no scientific refs/results, research/Forge branches, legacy shared latest/state, Utility state, or scheduler are changed. The final role handoff commit is re-fetched after append-only history persistence because a commit cannot self-embed its own resulting SHA.