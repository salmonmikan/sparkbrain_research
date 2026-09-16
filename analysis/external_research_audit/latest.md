# SparkBrain External Research & Audit — Latest Handoff

Analysis time: 2026-09-17 04:28 JST  
Role: `LITERATURE_REDUCTION_SCOUT`

## Current repository context

Fresh inspection found `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`, Control Brain handoff `b3e9da4b6eb65f01282db8f06f967f96e1ca8be0`, Evidence Analyst handoff `9f6cb3b1cb4a5bb1a7a10f6f9b04e54c50bb1cec`, MAIN report `6c3d5cc730b057f5c852160a904a0124e22cafe7`, and SUB report `409d5356d69b9b2635dde0a8f84cbc4eabc44069`. Split MAIN/SUB report streams and role-suffixed histories are present and were consumed.

The registered A01 A/B/C mechanism search is now closed and the programme has been reframed as an experimental persistent-dynamical cognitive architecture/testbed. C19-v2 is the primary frontier. The active C19 branch remains `research/c19-truth-free-symbolic-adapter-v2-20260917@90c936a7abca7eba0dac1f977753503551e73368`; official one-way execution is not admitted. The current source contains a source-only protocol validator that is intentionally incapable of official execution, so MAIN's current task is still executable harness/source-runtime-package binding on synthetic/dev fixtures only.

The I2 adapter is target-blind surface structuring: it exposes source/step indices, a fixed query marker, sentence-ordinal premises and choice ordinals while hashing normalized surface strings. The frozen protocol already limits a positive claim to `truth_free_surface_structural_representation_gain_only`.

## Four new literature findings

### 1. Surface/symbolic abstraction itself is a strong ordinary explanation for representation gains

Biesterbos, Den Ouden & De Rijke, *RvH-40 at SemEval-2026 Task 11: Disentangling Reasoning from Belief through Symbolic Abstraction* (ACL/SemEval 2026) show that variable/pseudoword substitution can expose latent reasoning otherwise suppressed by linguistic content; their final system reports 97.92% validation and 96.34% hidden-test accuracy.

- https://aclanthology.org/2026.semeval-1.65/
- DOI: 10.18653/v1/2026.semeval-1.65

**Implication for C19:** an I2 > I1 result can plausibly arise from ordinary abstraction/canonicalization inductive bias rather than SparkBrain-specific persistent dynamics. That does not invalidate C19; it reinforces the present narrow claim boundary.

**Future prospective discriminator:** after the current frozen C19-v2 identity resolves, feed the exact same I2 features to a minimal stateless/linear or shallow model. First verify whether the frozen `direct_stateless` baseline already receives the identical I2 representation; if not, define a future representation-matched null rather than altering the present protocol.

### 2. Explicit symbolic state tracking is a strong established alternative to implicit neural belief dynamics

Zhu, Yi, Jia & Thomason, *PDDL-Mind: Large Language Models are Capable on Belief Reasoning with Reliable State Tracking* (arXiv:2604.17819, 20 April 2026) decouple environment-state evolution from belief inference using explicit PDDL states/actions and verified transitions, reporting >5 percentage points absolute gain over prior SOTA across ToM benchmarks.

- https://arxiv.org/abs/2604.17819

**Implication for C19:** a positive external-validation result does not uniquely validate persistent-dynamical computation if equally informed explicit state tracking can produce the gain. The frozen `explicit_state_probabilistic` family is relevant, but its exact information/representation boundary should be checked before claiming it closes this reduction.

**Future prospective discriminator:** use the same structured visible information and matched state/resource budget for a minimal explicit transition/state tracker versus SparkBrain dynamics.

### 3. Belief management now has a stronger three-way target: Update, Stay, and Isolation

Xu et al., *When Should Models Change Their Minds? Contextual Belief Management in Large Language Models* (arXiv:2605.30219, first submitted 28 May 2026) introduce BeliefTrack and diagnose `Failed Update`, `Failed Stay`, and `Failed Isolation`. They report belief-state-reward RL reducing failure rates by 70.9% on average and representation steering reducing failure rates by 46.1% across two tasks.

- https://arxiv.org/abs/2605.30219

**Implication for C19:** BU/BM/BREU covers Belief-R's update/maintain trade-off but not a distinct isolation axis. A C19 pass could therefore still reflect clean-format representation gain rather than robust contextual belief management.

**Future prospective discriminator:** a separately frozen BeliefTrack-style or Belief-R nuisance-perturbation suite with irrelevant evidence/noise while logical belief transitions are held fixed, reporting Update/Stay/Isolation separately.

### 4. Very recent evidence shows ordinary Transformers can carry functionally causal Bayesian belief-state geometry

Balcells et al., *Large Language Models Develop Belief State Geometry In-Context* (arXiv:2609.17376, submitted 15 September and updated 16 September 2026) report belief states linearly decodable from residual streams across six open-source LLMs and 40 HMMs, with peak probe R² 0.83–0.99; patching/steering the identified subspace changes downstream predictions while controls degrade performance.

- https://arxiv.org/abs/2609.17376

**Programme implication:** persistent/history-conditioned internal belief representations with causal relevance are an established comparator property, not a SparkBrain novelty axis. Future new-principle claims need a stronger discriminator such as low-privilege causal lineage/locality/resource constraints. For C19, the transformer baseline remains important but external performance alone cannot settle mechanism equivalence.

## Reduction map / interpretation

The prior scout's eligibility-trace, pending-cause, latent-cause, learned-delay and local-learning reductions remain intact and are not repeated as new findings.

The new C19-specific reduction pressure is:

`I2 surface decomposition + hashing -> ordinary abstraction/canonicalization inductive bias`

and downstream:

`belief-revision gain -> reliable explicit state tracking or ordinary Transformer belief-state representation`

This does **not** invalidate C19-v2. It sharpens what a positive outcome may establish: external testbed validity and useful structured representation, not a new computational principle.

## Knowledge-flow contract

- `role`: `LITERATURE_REDUCTION_SCOUT`
- `genuinely_new_information`: `true`
- `affected_lines`: `C19_V2`, `PROGRAMME_NOVELTY`, `FUTURE_EXTERNAL_VALIDATION`, secondarily `A01_REFRAME`
- `novelty_or_reduction_impact`: `C19_I2_POSITIVE_RESULT_HAS_STRONG_ORDINARY_REPRESENTATION_CANONICALIZATION_AND_EXPLICIT_STATE_REDUCTIONS; PERSISTENT_BELIEF_STATE_ITSELF_IS_NOT_NOVEL`
- `audit_classification`: `null`
- `prospective_baselines_or_discriminators`: identical-I2-feature stateless/shallow null; representation-matched explicit-state tracker; Update/Stay/Isolation perturbation suite; matched Transformer/recurrent belief-state comparator for future internal-state claims.
- `questions_for_evidence_analyst`:
  1. Does frozen `direct_stateless` consume the exact same I2 representation, or are frontend representation and downstream dynamics confounded?
  2. Is `explicit_state_probabilistic` representation/information matched strongly enough to test the explicit-state reduction?
  3. Preserve the current C19-v2 protocol and claim boundary; these are future prospective discriminators only.
  4. If C19-v2 passes, explicitly separate structured-frontend gain from persistent-dynamics gain before making an architectural mechanism claim.
- `questions_for_control_brain`:
  1. Should post-C19 planning prioritize representation-matched static and explicit-state nulls before scaling/application work?
  2. If C19 establishes a clean Belief-R signal, should BeliefTrack/Failed-Isolation be the next external-generalization test?
  3. Treat the 15–16 September 2026 belief-state-geometry result as additional evidence that persistent belief state is an established comparator property.
- `must_not_change_frozen_or_consumed`: all consumed A01/RV01/RV02/CX identities; rejected A01 Family-B/C exact objects; historical C19-v1/C06; C19-v2 scientific semantics at `90c936a7...`; `c19-external-v2-official-v1` remains unSTARTED/unconsumed until a newer execution admission.

## Handoff

**Role performed:** `LITERATURE_REDUCTION_SCOUT`.  
**Genuinely new external scientific information:** yes — focused on the newly primary C19 line, not recycled A01/RV01 prior art.  
**Top implication:** a future C19 I2 gain has strong ordinary explanations as abstraction/canonicalization or explicit state tracking unless a representation-matched static/state baseline separates frontend gains from persistent dynamics.  
**Affected lines:** C19-v2, programme novelty framing, future external validation.  
