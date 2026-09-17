# SparkBrain External Research — Literature Reduction Scout

Timestamp: `2026-09-18 04:30 JST`
Role: `LITERATURE_REDUCTION_SCOUT`

## Repository context

Current science was re-fetched independently from the repository; `ops/*` branches were treated only as control-plane mailboxes.

- `main`: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- Evidence Analyst: `ops/evidence-analyst-handoff@b09d90d0545a0448ea5a310f9373969e7471b15d`
- Control Brain: `ops/control-brain-handoff@d40f83ababcddf0b1e72621c77b10a8c4900badb`
- Orchestrator report branch observed: `ops/orchestrator-run-report@a4ff0f85d5c7a89d1f21817775d57ead85ddd21c`
- Current PRIMARY research object: `research/c19-r2-fsa-state-tracker-spec-20260918@5d5d171cf872baed7a636fd246ab36f3a91a6716`
- Scientific parent: immutable C19-v4 package `74bfe6b4a39758656f291baaa3f16236e3e71964`
- Authoritative C19-v4 evidence: `evidence/c19-official-v4-c19-external-v2-official-v4` -> `a0f83318356ced1c84863737803080d0dc69d208`
- Open PRs: `0`

R2 is still PRE-FORMAL and has no formal identity or STARTED ref. Its exact seven-state tracker, same-I2 representation, pair-reset semantics, zero-fit budget, target-free `atomic_idx` cluster bootstrap, raw-before-score boundary and narrow reduction-only interpretation were frozen before any R2 outcome. Dedicated pre-START and ordinary CI are both green on exact head `5d5d171...`; fresh Evidence Analyst authority is still required before any formal identity/STARTED.

The prior literature stream already covered revision-authority arbitration, DeltaLogic/minimal-edit revision diagnostics, finite-state structure inside Transformers, state-space scaling, and selective-history belief-state models. Those findings are not repeated below.

## Genuinely new external findings

### 1. Predictive State Representations are a stronger post-R2 reduction family than one hand-enumerated FSA

Littman, Sutton & Singh (NeurIPS 2001) represent dynamical state directly by multi-step, action-conditional predictions of future observations. Singh, James & Rudary (UAI 2004) further formalize Predictive State Representations (PSRs), in which state is a vector of predictions about observable tests rather than a nominal hidden state. The UAI work shows PSRs can be more general than fixed-order Markov and hidden-state models.

This matters because a future `SURVIVES_FSA_REDUCTION` result would reject only the exact seven-state R2 tracker. It would not establish that SparkBrain-specific persistent dynamics are required: a low-dimensional predictive-state model could still compress the same history into observable future-prediction coordinates without Spark-specific coalition semantics.

Prospective implication: after R2, if further reduction is warranted, define a target-blind PSR/TPSR-style comparator under the same visible I2 envelope and freeze its state dimension/test set/learning budget before outcomes. Do not retrofit it to C19-v4 per-example results.

Sources:
- Littman, Sutton & Singh, *Predictive Representations of State*, NeurIPS 2001: https://proceedings.neurips.cc/paper/2001/hash/1e4d36177d71bbb3558e43af9577d70e-Abstract.html
- Singh, James & Rudary, *Predictive State Representations: A New Theory for Modeling Dynamical Systems*, UAI 2004, DOI 10.5555/1036843.1036905.

### 2. Computational mechanics already formalizes minimal history-derived predictive state

Shalizi & Crutchfield's computational mechanics defines causal states as equivalence classes of histories with the same conditional distribution over futures. The resulting epsilon-machine is a minimal sufficient predictive representation, with causal-state dynamics that are Markov even when the observed process is not.

This is a direct novelty-bar issue for SparkBrain. `history-derived`, `persistent`, `pre-semantic`, and `predictively useful` internal states are not by themselves distinctive. There is an established formal theory that asks for the *minimal predictive partition of histories*.

Prospective implication: a later reduction/diagnostic could reconstruct causal states (or an approximate epsilon-machine) from a SparkBrain/world trajectory under a prospectively fixed observable envelope, then ask whether a compact causal-state model preserves the behavior currently attributed to SparkBrain dynamics. If yes, the mechanism reduces toward ordinary predictive-state structure; if not, the counterexamples identify the remaining claim more sharply.

Sources:
- Shalizi & Crutchfield, *Computational Mechanics: Pattern and Prediction, Structure and Simplicity*, J. Stat. Phys. 2001 / arXiv:cond-mat/9907176.
- Related causal-state exposition in *The Computational Structure of Spike Trains*, PLoS Comput Biol 2010: https://pmc.ncbi.nlm.nih.gov/articles/PMC2849313/

### 3. Local causal states substantially raise the bar for claims based on local emergence

Rupe, Kashinath, Kumar & Crutchfield (Chaos 2025) use spacetime lightcones and predictive equivalence classes of local pasts to construct **local causal states** that identify coherent, self-organized structures in complex spatiotemporal systems without semantic labels. The framework is explicitly local and grounded in limits on causal influence propagation.

This matters beyond R2. SparkBrain's longer-horizon residual motif emphasizes local, pre-semantic activity and emergent organization. But locality + history + predictive equivalence + emergent coherent structure already have a constructive external formalism. Therefore `local`, `pre-semantic`, or `self-organizing predictive state` should not be treated as novelty axes by themselves.

The residual Spark-specific question must remain narrower: whether actual anonymous historical provenance and later external evidence produce selective lineage-specific credit / changed future competition under constraints that predictive-state or local-causal-state models do not already capture.

Source:
- Rupe et al., *Unsupervised discovery of extreme weather events using universal representations of emergent organization*, Chaos 35 (2025), DOI 10.1063/5.0267915: https://pubmed.ncbi.nlm.nih.gov/40758815/

### 4. Reservoir universality gives a formal reduction test for fading-memory behavior

Grigoryeva & Ortega (Neural Networks 2018) prove echo-state networks are universal uniform approximants for discrete-time fading-memory filters with uniformly bounded inputs. Related state-affine reservoir results establish universality for fading-memory stochastic filters with linear readouts.

This does **not** prove SparkBrain is a reservoir and does not cover arbitrary non-fading memory. It does establish a useful falsification boundary: if the behavior SparkBrain is meant to explain is causal, time-invariant and effectively fading-memory, then a conventional reservoir family can in principle approximate it.

Prospective implication: after finite-state/predictive-state reductions, use a resource/state-matched reservoir comparator together with a **remote-history / washout scaling test**. Hold current input and recent history matched while moving a causally relevant event farther into the past. If SparkBrain's effect decays like an ordinary fading-memory filter and a matched reservoir tracks it, novelty pressure increases. A persistent non-fading effect that survives prospective controls would be more discriminating.

Sources:
- Grigoryeva & Ortega, *Echo state networks are universal*, Neural Networks 108 (2018), PMID 30317134: https://pubmed.ncbi.nlm.nih.gov/30317134/
- Grigoryeva & Ortega, *Universal discrete-time reservoir computers with stochastic inputs and linear readouts using non-homogeneous state-affine systems*, JMLR 19(24), 2018: https://jmlr.org/beta/papers/v19/18-020.html

### 5. Automata extraction offers a better reduction workflow than an endless hand-designed FSA ladder

Weiss, Goldberg & Yahav (ICML 2018) use Angluin-style active learning plus abstraction to extract deterministic finite automata approximating trained RNN state dynamics, with counterexamples used to refine the abstraction.

For SparkBrain, this suggests a methodological improvement after the exact R2 test. Rather than manually inventing R3/R4 finite-state trackers, prospectively define an automata-extraction experiment over a frozen SparkBrain/input oracle. A compact extracted DFA/WFA that reproduces the target behavior would be strong reduction evidence; persistent counterexamples would directly identify where finite-state abstraction fails and therefore where a sharper discriminator should be placed.

Source:
- Weiss, Goldberg & Yahav, *Extracting Automata from Recurrent Neural Networks Using Queries and Counterexamples*, ICML 2018: https://proceedings.mlr.press/v80/weiss18a.html

## Reduction synthesis

R2 is scientifically sensible, but a positive R2 survival would still leave several established reductions open. The external literature now supports a more principled ladder:

`exact hand-designed FSA -> extracted/learned finite-state abstraction -> PSR / epsilon-machine predictive-state compression -> reservoir/fading-memory reduction -> only then a narrower Spark-specific residual claim`.

The most important novelty-bar change is that **pre-semantic, local, history-derived predictive state and emergent organization are already established concepts in computational mechanics and predictive-state modeling**. SparkBrain's residual scientific target should therefore remain centered on something stronger: anonymous causal provenance / lineage-specific local credit and genuinely nontrivial persistence that survives matched predictive-state and fading-memory reductions.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - C19_R2_FSA_STATE_TRACKER
  - PROGRAMME_NOVELTY
  - POST_R2_REDUCTION
  - PERSISTENT_DYNAMICS_RESIDUAL
  - FUTURE_EXTERNAL_VALIDATION
novelty_or_reduction_impact: >
  STRONGER_REDUCTION_PRESSURE. A future R2 survival rejects only one exact
  seven-state tracker. Predictive-state representations, epsilon-machine /
  causal-state compression, automata extraction, and fading-memory reservoir
  families remain live ordinary reductions. Local/pre-semantic/predictive
  emergence alone is not a defensible novelty axis.
audit_classification: null
prospective_baselines_or_discriminators:
  - target-blind PSR/TPSR comparator with prospectively frozen dimension/test set/budget
  - causal-state / epsilon-machine reconstruction under a frozen observable envelope
  - prospective DFA/WFA extraction from SparkBrain behavior with held-out counterexamples
  - resource/state-matched ESN/reservoir comparator
  - remote-history / washout scaling test to distinguish fading from non-fading persistence
  - local-causal-state diagnostic if future claims rely on spatial/local emergence
questions_for_evidence_analyst:
  - If R2 survives, should the next reduction be learned/extracted finite-state abstraction before another hand-designed mechanism?
  - Should PSR/epsilon-machine compression be placed ahead of any stronger persistent-dynamics claim?
  - Can a future remote-history test freeze current/recent input while moving only the causal event farther into the past?
  - Keep R2 frozen exactly as written; treat all findings here as future prospective work only.
questions_for_control_brain:
  - Explicitly remove local/pre-semantic/predictive-state emergence from the programme novelty axes unless it beats causal-state/local-causal-state reductions?
  - Adopt a post-R2 reduction ladder based on representational class rather than one-off mechanism names?
  - Treat non-fading lineage-specific causal credit under matched state/lookup/resource budgets as the narrower remaining novelty target?
must_not_change_frozen_or_consumed:
  - immutable C19-v4 package/preserve/evidence/tag and terminal PASS
  - consumed C19-v2/v3 identities
  - consumed R1-v1 and R1-v2 identities and controls
  - R1 transient unpreserved outputs
  - consumed A01/RV01/RV02/CX identities and legacy immutable refs
  - current R2 pre-formal mechanism/statistics/resource semantics in response to this literature
  - no formal R2 identity or STARTED without fresh Evidence Analyst authorization
```
