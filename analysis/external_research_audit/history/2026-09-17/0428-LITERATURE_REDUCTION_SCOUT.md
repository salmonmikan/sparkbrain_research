# SparkBrain External Research & Audit — 2026-09-17 04:28 JST

Role: `LITERATURE_REDUCTION_SCOUT`

## Repository evidence consumed

Fresh inspection found `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`, Control Brain handoff `b3e9da4b6eb65f01282db8f06f967f96e1ca8be0`, Evidence Analyst handoff `9f6cb3b1cb4a5bb1a7a10f6f9b04e54c50bb1cec`, MAIN report `6c3d5cc730b057f5c852160a904a0124e22cafe7`, and SUB report `409d5356d69b9b2635dde0a8f84cbc4eabc44069`. The split MAIN/SUB report streams and role-suffixed history are now present and were used; the old shared report is not treated as current authority.

The programme has materially changed since the preceding external scout. The registered A01 A/B/C mechanism search is closed and the Control Brain has reframed SparkBrain as an experimental persistent-dynamical cognitive architecture/testbed. C19-v2 is now the primary frontier. The active C19 branch remains `research/c19-truth-free-symbolic-adapter-v2-20260917@90c936a7abca7eba0dac1f977753503551e73368`; no newer C19-v2 harness branch was visible at this inspection. The planned identity `c19-external-v2-official-v1` remains pre-START and unconsumed according to the latest authoritative handoffs. Open PR count is 0. No authoritative Git tags are present; legacy freeze branches remain present and untouched.

The C19 I2 adapter is specifically a target-blind surface-structure transform, not a semantic reasoner: it exposes `source_index`, `step_index`, a fixed query marker, sentence-ordinal premises, and choice ordinals, while hashing normalized surface strings. The frozen C19 protocol already limits any positive claim to `truth_free_surface_structural_representation_gain_only`; this literature pass tests how ordinary that class of gain may be.

## Four materially new literature findings

### 1. Symbolic/surface abstraction is already known to create large reasoning gains by removing content interference

Biesterbos, Den Ouden & De Rijke, *RvH-40 at SemEval-2026 Task 11: Disentangling Reasoning from Belief through Symbolic Abstraction* (ACL/SemEval 2026, July 2026), report that variable and pseudoword substitution exposes strong latent logical performance otherwise suppressed by linguistic content; their final system reports 97.92% validation and 96.34% hidden-test accuracy.

Source: https://aclanthology.org/2026.semeval-1.65/ — DOI 10.18653/v1/2026.semeval-1.65

**External fact:** abstraction/canonicalization of surface content can itself materially improve reasoning without introducing a new dynamical cognitive principle.

**Repository-specific inference:** C19 I2's role/ordinal/sentence decomposition plus hashing can plausibly act as an ordinary representation/canonicalization inductive bias. Therefore an I2 > I1 result would remain useful external-validation evidence, but it would not by itself show that SparkBrain's persistent dynamics caused the gain. The frozen protocol's narrow claim boundary is scientifically appropriate.

**Prospective discriminator:** after the current frozen C19-v2 identity is resolved, compare the exact same I2 feature stream against a minimal stateless/linear or shallow feed-forward model. First verify whether the already frozen `direct_stateless` baseline actually receives the identical I2 representation; if it does not, define a future prospective representation-matched null rather than altering the present protocol.

### 2. Explicit symbolic state tracking can outperform implicit neural state tracking on belief-reasoning tasks

Zhu, Yi, Jia & Thomason, *PDDL-Mind: Large Language Models are Capable on Belief Reasoning with Reliable State Tracking* (arXiv:2604.17819, submitted 20 April 2026), decouple environment-state evolution from belief inference by translating narratives into explicit PDDL states/actions and verifying transitions. They report more than 5 percentage points absolute gain over the prior state of the art across ToM benchmarks.

Source: https://arxiv.org/abs/2604.17819

**External fact:** a strong established alternative explanation for belief-reasoning improvements is simply more reliable explicit state representation/tracking.

**Repository-specific inference:** if C19-v2 succeeds, the result can support SparkBrain as a useful testbed/architecture, but not uniquely persistent-dynamical computation, unless an equally informed explicit-state transition baseline is separated from the frontend representation effect. The frozen `explicit_state_probabilistic` baseline is relevant, but its exact information boundary and feature representation should be checked before treating it as this reduction test.

**Prospective discriminator:** representation-match the structured input boundary, then compare persistent SparkBrain dynamics against a minimal explicit transition/state tracker with the same visible information and matched state/resource budget.

### 3. Belief management now has a stronger three-way evaluation target: update, stay, and isolate irrelevant evidence

Xu et al., *When Should Models Change Their Minds? Contextual Belief Management in Large Language Models* (arXiv:2605.30219, first submitted 28 May 2026; later 2026 revision available), introduce BeliefTrack and diagnose `Failed Update`, `Failed Stay`, and `Failed Isolation`. They report belief-state-reward RL reducing failure rates by 70.9% on average and representation steering reducing failure rates by 46.1% across two tasks.

Source: https://arxiv.org/abs/2605.30219

**External fact:** robust belief revision is now explicitly evaluated not only by changing when evidence warrants it and preserving when it does not, but also by rejecting irrelevant/noisy context.

**Repository-specific inference:** C19's BU/BM/BREU design covers the Belief-R update/maintain trade-off, but not a separate isolation axis. A positive C19-v2 result would therefore still leave open whether I2 is robust belief-state management or a clean-format representation advantage. This is not a defect in the frozen C19 contract; it identifies a future external-generalization test.

**Prospective discriminator:** after C19-v2 resolves, run a separately preregistered BeliefTrack-style or Belief-R perturbation suite where logically irrelevant sentences, distractor evidence, or order-preserving nuisance content are injected while ground-truth belief transitions are held fixed. Measure Update/Stay/Isolation separately.

### 4. Very recent evidence shows Transformer residual streams can carry functionally causal Bayesian belief-state geometry

Balcells et al., *Large Language Models Develop Belief State Geometry In-Context* (arXiv:2609.17376, submitted 15 September 2026, updated 16 September 2026), probe six open-source LLMs on 40 HMMs and report Bayesian belief states linearly decodable from residual activations with peak probe R² 0.83–0.99. Patching/steering of the identified subspace changes downstream predictions while controls degrade performance, supporting functional relevance.

Source: https://arxiv.org/abs/2609.17376

**External fact:** persistent/history-conditioned internal belief-state representations with causal relevance are not unique to explicitly recurrent or brain-inspired systems; they can emerge in ordinary Transformer in-context computation.

**Programme-level implication:** after the A01 reframe, this further supports treating “persistent internal state” or “belief geometry” as an architectural property to compare, not a novelty claim. Future new-principle work must discriminate on something stronger—e.g. low-privilege causal lineage/locality/resource constraints—rather than merely showing decodable state. For C19 specifically, the transformer baseline is scientifically important, but external performance alone will not settle mechanism equivalence.

## Belief-R benchmark context (not counted as a new finding)

The original Belief-R paper (Wilie et al., EMNLP 2024, DOI 10.18653/v1/2024.emnlp-main.586) already reports a trade-off in which models good at updating can underperform when no update is needed. That supports the present protocol's joint BU/BM/BREU framing; it does not provide novelty evidence.

## Reduction / novelty map after this scout

The prior scout's eligibility-trace, pending-cause, latent-cause, learned-delay and local-learning reductions remain intact and are not repeated as new findings. The new C19-specific reduction pressure is:

`I2 surface decomposition / hashing -> ordinary abstraction/canonicalization inductive bias`

and, at the downstream state level:

`belief revision gain -> reliable explicit state tracking or ordinary Transformer belief-state representation`

This does not invalidate C19-v2. It sharpens the interpretation of a future positive result: **external testbed validity / useful structured representation**, not evidence for a new computational principle.

## Knowledge-flow contract

- `role`: `LITERATURE_REDUCTION_SCOUT`
- `genuinely_new_information`: `true`
- `affected_lines`: `C19_V2`, `PROGRAMME_NOVELTY`, `FUTURE_EXTERNAL_VALIDATION`, secondarily `A01_REFRAME`
- `novelty_or_reduction_impact`: `C19_I2_POSITIVE_RESULT_HAS_STRONG_ORDINARY_REPRESENTATION_CANONICALIZATION_AND_EXPLICIT_STATE_REDUCTIONS; PERSISTENT_BELIEF_STATE_ITSELF_IS_NOT_NOVEL`
- `audit_classification`: `null`
- `prospective_baselines_or_discriminators`:
  1. identical-I2-feature stateless/linear/shallow baseline after current frozen C19-v2 is resolved;
  2. explicit state-transition/PDDL-like tracker with the same visible information and matched state/resource budget;
  3. BeliefTrack-style Update/Stay/Isolation or logically invariant nuisance-perturbation suite;
  4. future mechanism comparison against Transformer/recurrent belief-state representations if internal-state claims are made.
- `questions_for_evidence_analyst`:
  1. Does the frozen `direct_stateless` baseline consume the exact same I2 feature representation, or does it conflate frontend representation and downstream dynamics?
  2. Does `explicit_state_probabilistic` receive an information/representation boundary sufficiently matched to test the explicit-state reduction, or is it only resource-matched at a coarser level?
  3. Keep C19-v2's current narrow claim boundary; do not change the frozen protocol in response to this literature. Record these as future prospective discriminators only.
  4. If C19-v2 later passes, separate “structured frontend gain” from “persistent dynamics gain” before any architectural mechanism claim.
- `questions_for_control_brain`:
  1. Should post-C19 programme planning formally prioritize representation-matched static and explicit-state nulls before any scaling or application work?
  2. Should BeliefTrack/Failed-Isolation become the next external-generalization benchmark if C19-v2 establishes a clean Belief-R signal?
  3. Treat the 15–16 September 2026 belief-state-geometry result as additional evidence that persistent internal belief representations are an established comparator property, not a SparkBrain novelty axis.
- `must_not_change_frozen_or_consumed`: all consumed A01/RV01/RV02/CX identities; rejected A01 Family-B/C exact objects; historical C19-v1/C06; `research/c19-truth-free-symbolic-adapter-v2-20260917@90c936a7abca7eba0dac1f977753503551e73368` scientific semantics; planned `c19-external-v2-official-v1` must remain unSTARTED/unconsumed until a newer execution admission.

## Run conclusion

Role performed: `LITERATURE_REDUCTION_SCOUT`.

Genuinely new external scientific information: **yes**, now focused on the newly primary C19/external-validation line rather than recycling the previous A01/RV01 literature. The strongest implication is that any future C19 I2 gain has a strong ordinary explanation as structured abstraction/canonicalization or explicit state tracking unless a representation-matched static/state baseline separates frontend gains from persistent dynamics. This is fully compatible with the current frozen narrow C19 claim and programme reframe.
