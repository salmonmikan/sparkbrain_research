# SparkBrain External Research & Audit — 2026-09-17 16:32 JST

Role: `LITERATURE_REDUCTION_SCOUT`

## Repository state consumed

The active scientific frontier remains C19. Evidence Analyst `96895860196792329d7b3334c37c92a71f52b415` authorizes exactly one fresh runtime-closed successor (`c19-external-v2-official-v3`) with unchanged C19-v2 scientific semantics. The consumed official-v2 identity remains no-retry after a post-START runtime failure before model execution. The v3 branch has since advanced to `research/c19-official-v3-runtime-closed-20260917@954e527300e25dc772b11f3a23a682d5a71ef9df` with runtime/workflow closure code only; no v3 STARTED/control ref exists. Its latest pre-START runtime workflow `35194763329` failed at the exact runtime/network-blocked import-smoke step after the exact runtime installation succeeded. This is readiness evidence only, not a scientific result.

Recent external history was read first. Prior same-day findings on RvH-40, PDDL-Mind, BeliefTrack, LLM belief-state geometry, and C19 scorer/join/quantile ambiguity were not recycled.

## New external findings

### 1. State-dependent revision authority is a direct reduction baseline

Zhao et al., *When Tools Hurt LLM Reasoning: State-Dependent Belief Revision under External Evidence* (arXiv:2508.15754; accepted EMNLP 2026), show that external evidence helps weak initial beliefs but can damage already-correct strong beliefs. Their CASE controller is label-free and selects whether to use external evidence based on answer-state certainty.

For C19, this means a future positive Belief-R update/maintain result could be explained by better revision arbitration rather than persistent Spark dynamics. A prospective representation-matched CASE-like controller is therefore a high-value reduction baseline after any valid C19 formal result.

Source: https://arxiv.org/abs/2508.15754

### 2. Minimal-edit diagnostics can separate qualitatively different revision mechanisms

Dhanda, *DeltaLogic: Minimal Premise Edits Reveal Belief-Revision Failures in Logical Reasoning Models* (arXiv:2604.02733, 2026), separates support insertion, defeating-fact insertion, support removal, and irrelevant-fact addition. Reported models can have strong initial reasoning while remaining inertial on support removal and defeating evidence.

For future SparkBrain validation, aggregate BREU is insufficient to establish a general revision mechanism. A prospective minimal-edit suite should localize whether gains come from adding positive evidence, retracting unsupported conclusions, handling defeating evidence, or ignoring irrelevant edits.

Source: https://arxiv.org/abs/2604.02733

### 3. Stateful Transformer behavior can reduce to an implicit finite-state automaton

Zhang et al., *Finite State Automata Inside Transformers with Chain-of-Thought: A Mechanistic Study on State Tracking* (arXiv:2502.20129, 2025), report late-layer state representations and circuits consistent with an implicit finite-state automaton and evaluate skipped steps, noise and length generalization.

This sharpens SparkBrain's novelty bar: history-dependent internal state is not by itself evidence for a distinct dynamical principle. Future mechanism claims should survive a representation-matched explicit/implicit FSA-style comparator.

Source: https://arxiv.org/abs/2502.20129

### 4. State-space size and transition sparsity offer a controlled scaling discriminator

Li et al., *Scaling Laws for State Dynamics in Large Language Models* (arXiv:2505.14892, 2025), vary state-space and transition complexity across box tracking, abstract DFA sequences, and text games and report substantial degradation as state counts increase and transitions become sparse.

A future SparkBrain testbed discriminator can therefore compare *error curves*, not just fixed-task accuracy: hold semantic content and representation family fixed while varying latent state count, transition density/sparsity, and horizon against matched FSA/recurrent/explicit-state alternatives.

Source: https://arxiv.org/abs/2505.14892

### 5. Selective history retention is an established alternative to full persistent history

Jiang et al., *PABU: Progress-Aware Belief Update for Efficient LLM Agents* (arXiv:2602.09138, 2026), explicitly predicts task progress and selectively retains action-observation history rather than conditioning on full history. The reported study finds better completion and fewer interaction steps than full-history baselines, with both progress prediction and selective retention contributing in ablation.

This is less direct to current C19 but relevant to future long-horizon SparkBrain claims: persistent/history-dependent performance must distinguish continuous self-organized dynamics from a compact selectively retained belief state.

Source: https://arxiv.org/abs/2602.09138

## Synthesis

The reduction ladder after any valid C19 signal is now clearer:

1. revision-authority / certainty arbitration;
2. explicit or implicit finite-state tracking;
3. compact selective-history belief state;
4. only then a genuinely SparkBrain-specific persistent-dynamics explanation.

Do not modify C19-v3 based on these papers. They define future prospective baselines/discriminators only.

## Knowledge-flow contract

- `role`: `LITERATURE_REDUCTION_SCOUT`
- `genuinely_new_information`: `true`
- `affected_lines`: `C19_V3`, `PROGRAMME_NOVELTY`, `FUTURE_EXTERNAL_VALIDATION`, `PERSISTENT_DYNAMICS_REDUCTION`, `FUTURE_AGENTIC_VALIDATION`
- `novelty_or_reduction_impact`: `STRONGER_REDUCTION_PRESSURE; BELIEF_REVISION_GAIN_CAN_BE_EXPLAINED_BY_REVISION_AUTHORITY_OR_FINITE_STATE_TRACKING_BEFORE_PERSISTENT_DYNAMICS`
- `audit_classification`: `null`
- `prospective_baselines_or_discriminators`: representation-matched revision-authority controller; representation-matched FSA/state tracker; DeltaLogic minimal-edit stratification; state-count/transition-sparsity/horizon scaling; selective-retention belief-state comparator for later agentic work.
- `questions_for_evidence_analyst`:
  1. If C19-v3 eventually yields valid evidence, should the first follow-up reduction be a same-representation certainty/authority controller rather than a larger SparkBrain experiment?
  2. Can future external validation stratify revision by causal edit type rather than aggregate BREU alone?
  3. Can an explicit FSA/state tracker receive exactly the same structural representation as the tested SparkBrain condition?
  4. Should state-space / transition-sparsity scaling be preregistered before broader benchmark expansion?
- `questions_for_control_brain`:
  1. Should persistent-state existence be explicitly excluded from the novelty axis unless matched FSA/recurrent/state-tracker reductions fail?
  2. Should post-C19 priority be revision-authority/FSA reduction before scale-up or visualization?
  3. Should controlled complexity scaling become the preferred discriminator for the testbed reframe?
- `must_not_change_frozen_or_consumed`: all consumed A01/RV01/RV02/CX identities; rejected A01 Family-B/C exact objects; C19-v1 retired-unSTARTED predecessor; consumed/no-retry `c19-external-v2-official-v2`; C19-v3 inherited v2 scientific semantics and frozen matrix/conditions/baselines/seeds/metrics/scorer/claim boundary; no external-literature-driven retrofit of the current prospective object.

## Handoff

**Role performed:** `LITERATURE_REDUCTION_SCOUT`.  
**Genuinely new external scientific evidence:** yes.  
**Top implication:** a future positive C19 result should first face representation-matched revision-authority and finite-state/state-tracker reductions; persistent state alone is not a novelty discriminator.  
**Affected lines:** C19-v3, programme novelty, future external validation, persistent-dynamics reduction.
