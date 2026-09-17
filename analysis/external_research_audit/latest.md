# SparkBrain External Research & Audit — Latest Handoff

Analysis time: 2026-09-17 16:32 JST  
Role: `LITERATURE_REDUCTION_SCOUT`

## Repository state consumed

The active scientific frontier remains C19. Evidence Analyst `96895860196792329d7b3334c37c92a71f52b415` authorizes exactly one fresh runtime-closed successor (`c19-external-v2-official-v3`) with unchanged C19-v2 scientific semantics. The consumed official-v2 identity remains no-retry after a post-START runtime failure before model execution. The v3 branch has since advanced to `research/c19-official-v3-runtime-closed-20260917@954e527300e25dc772b11f3a23a682d5a71ef9df` with runtime/workflow closure code only; no v3 STARTED/control ref exists. Its latest pre-START runtime workflow `35194763329` failed at the exact runtime/network-blocked import-smoke step after the exact runtime installation succeeded. This is readiness evidence only, not a scientific result.

Recent external history was read first. I did **not** repeat the prior scout's RvH-40, PDDL-Mind, BeliefTrack, or LLM belief-state-geometry findings, nor the prior auditor's scorer/join/quantile conclusions.

## New external findings

### 1. A simple state-dependent revision-authority controller is a direct reduction baseline for Belief-R-style update/maintain trade-offs

**External fact.** Zhao et al., *When Tools Hurt LLM Reasoning: State-Dependent Belief Revision under External Evidence* (arXiv:2508.15754; accepted EMNLP 2026), show that external evidence helps weak initial beliefs but can damage already-correct strong beliefs. Their minimal CASE controller is label-free and selects between no-tool and tool-assisted trajectories using answer-state certainty rather than a new persistent cognitive architecture.

**Why this matters to C19.** C19's frozen scientific question is an I2-vs-I1 Belief-R BREU contrast, where the benchmark itself contains update/maintain tension. A future positive C19 result could therefore be explained by better arbitration over *when* to revise, not by persistent Spark dynamics. A CASE-like certainty/authority controller is a stronger prospective reduction baseline than a generic stateless baseline because it directly targets the update-vs-maintain failure mode.

**Implication.** After any valid C19 formal result, test a representation-matched, label-free revision-authority controller before attributing gains to persistent dynamics.

Source: https://arxiv.org/abs/2508.15754

### 2. DeltaLogic gives a cleaner causal perturbation test than aggregate BREU alone

**External fact.** Dhanda, *DeltaLogic: Minimal Premise Edits Reveal Belief-Revision Failures in Logical Reasoning Models* (arXiv:2604.02733, 2026), converts FOLIO/ProofWriter items into minimal-edit revision episodes and separates support insertion, defeating-fact insertion, support removal, and irrelevant-fact addition. Reported models can retain strong initial reasoning while failing revision, with particularly strong inertia on support removal and defeating evidence.

**Why this matters to C19.** Aggregate BU/BM/BREU can hide qualitatively different mechanisms. A system that reacts well to added positive evidence but cannot retract a conclusion when its support is removed is not a general belief-revision mechanism. C19 currently asks a valid narrow representation-gain question; a later external-validation stage should localize *which edit class* causes any gain.

**Implication.** A prospective DeltaLogic-style minimal-edit suite is a high-value discriminator after C19, especially support removal + defeating-fact + irrelevant-control cases. It should be new prospective work, never retrofitted into the frozen C19-v3 protocol.

Source: https://arxiv.org/abs/2604.02733

### 3. Transformer state tracking can reduce to an implicit finite-state automaton

**External fact.** Zhang et al., *Finite State Automata Inside Transformers with Chain-of-Thought: A Mechanistic Study on State Tracking* (arXiv:2502.20129, 2025), report late-layer circuits whose state representations behave like an implicit finite-state automaton and remain testable under skipped steps, noise, and length generalization.

**Why this matters to SparkBrain.** Merely demonstrating history-dependent state or state transitions is not enough to establish a distinct dynamical principle. An implicit FSA is an ordinary, compact alternative explanation for stateful behavior. This sharpens the reduction bar beyond the prior "Transformer can encode a belief state" result: the comparator can be algorithmically characterized as a state machine rather than only linearly decoded.

**Implication.** For any future claim that SparkBrain dynamics contribute beyond representation shaping, include a representation-matched explicit/implicit FSA-style comparator and compare state complexity, transition complexity, robustness to skipped intermediate steps, and length generalization.

Source: https://arxiv.org/abs/2502.20129

### 4. State-space size and transition sparsity provide a prospective scaling discriminator

**External fact.** Li et al., *Scaling Laws for State Dynamics in Large Language Models* (arXiv:2505.14892, 2025), evaluate Box Tracking, abstract DFA sequences, and text games while varying state-space/transition complexity. They find substantial degradation as the number of states grows and transitions become sparse, despite identifiable internal state-propagation circuitry.

**Why this matters to SparkBrain.** A single fixed C19 matrix can establish a narrow capability difference but cannot show that SparkBrain's mechanism has a qualitatively different state-dynamics regime. If SparkBrain is to remain useful as a persistent-dynamics testbed, one falsifiable future question is whether its error curve with state-count / transition-sparsity scaling differs from matched explicit-state/FSA/recurrent alternatives.

**Implication.** Prefer a controlled complexity sweep over broad benchmark accumulation: hold semantic content/representation family fixed and vary number of latent states, transition density/sparsity, and horizon.

Source: https://arxiv.org/abs/2505.14892

### 5. Selective history retention is an established alternative to persistent full-history dynamics

**External fact.** Jiang et al., *PABU: Progress-Aware Belief Update for Efficient LLM Agents* (arXiv:2602.09138, 2026), explicitly models task progress and selectively retains interactions rather than conditioning on full action-observation history. Across eight AgentGym environments it reports 81.0% completion and fewer interaction steps than full-history baselines; ablations attribute gains to both progress prediction and selective retention.

**Why this matters to SparkBrain.** If a future SparkBrain result benefits from persistent/history-dependent state, a simpler explanation may be that useful history was filtered rather than dynamically self-organized. This is especially relevant to future agentic extensions, less directly to the current frozen C19-v3 question.

**Implication.** For future long-horizon/agentic claims, compare against a compact selective-retention belief-state baseline before claiming that continuous persistent activity is required.

Source: https://arxiv.org/abs/2602.09138

## Synthesis

The new literature tightens, rather than relaxes, the current programme reframe. A valid C19 result would still be useful evidence about truth-free structured representation, but the mechanism ladder now has several inexpensive established reductions that should be crossed before any persistent-dynamics interpretation:

1. revision-authority / confidence arbitration;
2. explicit or implicit finite-state tracking;
3. compact selective-history belief state;
4. only then a genuinely dynamical SparkBrain-specific explanation.

The best next *future* discriminator is not to modify C19-v3. It is to prospectively compare any valid C19 effect against a representation-matched revision-authority controller and FSA/state-tracker, then probe minimal-edit classes and state-space scaling.

## Knowledge-flow contract

- `role`: `LITERATURE_REDUCTION_SCOUT`
- `genuinely_new_information`: `true`
- `affected_lines`: `C19_V3`, `PROGRAMME_NOVELTY`, `FUTURE_EXTERNAL_VALIDATION`, `PERSISTENT_DYNAMICS_REDUCTION`
- `novelty_or_reduction_impact`: `STRONGER_REDUCTION_PRESSURE; BELIEF_REVISION_GAIN_CAN_BE_EXPLAINED_BY_REVISION_AUTHORITY_OR_FINITE_STATE_TRACKING_BEFORE_PERSISTENT_DYNAMICS`
- `audit_classification`: `null`
- `prospective_baselines_or_discriminators`:
  1. representation-matched label-free revision-authority / certainty-arbitration controller;
  2. representation-matched explicit/implicit finite-state tracker;
  3. DeltaLogic-style minimal-edit stratification: support insertion, support removal, defeating fact, irrelevant control;
  4. controlled state-count / transition-sparsity / horizon scaling sweep;
  5. selective-retention compact belief-state baseline for later long-horizon agentic work.
- `questions_for_evidence_analyst`:
  1. If C19-v3 eventually yields valid evidence, should the first follow-up reduction be a same-representation certainty/authority controller rather than a larger SparkBrain experiment?
  2. Can future external validation stratify revision by causal edit type rather than rely on aggregate BREU alone?
  3. Can an explicit FSA/state tracker receive exactly the same structural representation as the tested SparkBrain condition?
  4. Should state-space / transition-sparsity scaling be preregistered before broader benchmark expansion?
- `questions_for_control_brain`:
  1. Should "persistent state exists" be explicitly excluded from the novelty axis unless matched FSA/recurrent/state-tracker reductions fail?
  2. Should post-C19 priority be revision-authority/FSA reduction before scale-up or visualization?
  3. Should controlled complexity scaling become the preferred discriminator for the testbed reframe?
- `must_not_change_frozen_or_consumed`: all consumed A01/RV01/RV02/CX identities; C19-v1 retired-unSTARTED; consumed/no-retry `c19-external-v2-official-v2`; C19-v3's inherited v2 scientific semantics, 55-row matrix, I2/I1 conditions, baselines, seeds, metrics, bootstrap/quantile/scorer and claim boundary; no external-literature-driven retrofit of the current prospective object.

## Handoff

**Role performed:** `LITERATURE_REDUCTION_SCOUT`.  
**Genuinely new external scientific evidence:** yes — revision-authority control, minimal-edit belief-revision diagnostics, FSA mechanistic reduction, state-dynamics scaling, and selective-retention belief-state work add new reduction/discriminator pressure beyond the prior scout.  
**Top implication:** a future positive C19 result should first face representation-matched revision-authority and finite-state/state-tracker reductions; persistent state alone is not a novelty discriminator.  
**Affected lines:** C19-v3, programme novelty, future external validation, persistent-dynamics reduction.
