# SparkBrain External Research — Literature Reduction Scout

Timestamp: `2026-09-18 04:30 JST`
Role: `LITERATURE_REDUCTION_SCOUT`

## Inputs consumed

Current repository state was fetched independently; `ops/*` branches were used only for designated handoff/report paths.

- `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- Control Brain `d40f83ababcddf0b1e72621c77b10a8c4900badb`
- Evidence Analyst `b09d90d0545a0448ea5a310f9373969e7471b15d`
- Orchestrator report branch `a4ff0f85d5c7a89d1f21817775d57ead85ddd21c`
- MAIN latest/state/history through `0431-main.md`
- SUB latest/state/history through `0347-sub.md`
- previous Literature history `2026-09-17/1632-LITERATURE_REDUCTION_SCOUT.md`
- current PRIMARY branch `research/c19-r2-fsa-state-tracker-spec-20260918@5d5d171cf872baed7a636fd246ab36f3a91a6716`
- immutable C19-v4 evidence tag/commit
- current open PR set: empty

Fresh repository observation: ordinary CI `35265194183` is now `completed/success` on exact R2 head `5d5d171...`, in addition to dedicated pre-START success `35265194243`. This is readiness only; R2 remains identity-free, unSTARTED and not execution-authorized.

## New literature findings

### Predictive State Representations

Predictive-state theory represents dynamical state directly through predictions of future observable tests rather than nominal hidden state. Littman, Sutton & Singh (NeurIPS 2001) show multi-step action-conditional predictive representations; Singh, James & Rudary (UAI 2004) formalize PSRs and show they are more general than fixed-order Markov and HMM/POMDP classes in the relevant representational sense.

Reduction implication: a future R2 `SURVIVES_FSA_REDUCTION` result rejects only one exact seven-state FSA. It does not exclude a compact target-blind predictive-state representation. A future PSR/TPSR comparator should freeze dimension, test set and learning budget prospectively and must not use C19-v4 per-example outcomes for design.

### Computational mechanics / epsilon-machines

Shalizi & Crutchfield formalize causal states as equivalence classes of histories that yield the same future predictive distribution. These states are minimal sufficient predictive statistics and induce Markov state dynamics even when the observed process is non-Markovian.

Novelty implication: history-derived, persistent, pre-semantic predictive state is an established formal object. A later causal-state reconstruction can act as a reduction diagnostic: if a compact epsilon-machine preserves the relevant behavior, the mechanism reduces toward ordinary predictive-state structure; persistent counterexamples identify a sharper residual claim.

### Local causal states

Rupe et al. (Chaos 2025) build local causal states from spacetime lightcones and predictive equivalence, recovering coherent self-organized structures from local interactions without semantic labels.

Programme implication: locality + pre-semantic history + emergent predictive organization cannot by itself carry SparkBrain novelty. The remaining Spark-specific target must be narrower, such as lineage/provenance-specific local credit and changed future competition under constraints not already captured by predictive-state/local-causal-state formalisms.

### Reservoir universality / fading memory

Grigoryeva & Ortega prove universality results for echo-state/reservoir systems over broad fading-memory filter classes. This does not prove SparkBrain is a reservoir and explicitly depends on fading-memory assumptions.

Discriminator implication: prospectively compare SparkBrain to a resource/state-matched reservoir while moving a causally relevant event farther into the past with current/recent input held matched. Ordinary fading/washout that is tracked by a reservoir increases reduction pressure; durable non-fading lineage-sensitive influence would be a stronger discriminator.

### Automata extraction

Weiss, Goldberg & Yahav (ICML 2018) extract finite automata from trained RNNs using queries and counterexamples. This suggests a better post-R2 workflow than indefinitely designing one-off FSAs manually.

Method implication: prospectively freeze an extraction protocol over a frozen SparkBrain/input oracle. A compact extracted DFA/WFA that reproduces held-out behavior is strong reduction evidence; counterexamples become direct candidates for the next discriminator.

## Synthesis

The post-R2 reduction ladder should be organized by representational class rather than mechanism names:

`exact hand-designed FSA -> extracted/learned finite-state abstraction -> PSR/epsilon-machine predictive-state compression -> reservoir/fading-memory reduction -> only then narrower Spark-specific residual mechanism`.

The main novelty-bar update is that **pre-semantic, local, history-derived predictive state and emergent organization already have established external formalisms**. The scientifically interesting residual is therefore narrower: actual anonymous historical provenance / lineage-specific local credit, plus persistence that cannot be compressed into an ordinary predictive-state or fading-memory representation under matched information/state/resource privilege.

## Sources

- Littman, Sutton & Singh (2001), *Predictive Representations of State*, NeurIPS: https://proceedings.neurips.cc/paper/2001/hash/1e4d36177d71bbb3558e43af9577d70e-Abstract.html
- Singh, James & Rudary (2004), *Predictive State Representations: A New Theory for Modeling Dynamical Systems*, UAI, DOI 10.5555/1036843.1036905.
- Shalizi & Crutchfield (2001), *Computational Mechanics: Pattern and Prediction, Structure and Simplicity*, J. Stat. Phys.; arXiv:cond-mat/9907176.
- Rupe, Kashinath, Kumar & Crutchfield (2025), *Unsupervised discovery of extreme weather events using universal representations of emergent organization*, Chaos 35, DOI 10.1063/5.0267915.
- Grigoryeva & Ortega (2018), *Echo state networks are universal*, Neural Networks 108, PMID 30317134.
- Grigoryeva & Ortega (2018), *Universal discrete-time reservoir computers with stochastic inputs and linear readouts using non-homogeneous state-affine systems*, JMLR 19(24).
- Weiss, Goldberg & Yahav (2018), *Extracting Automata from Recurrent Neural Networks Using Queries and Counterexamples*, ICML/PMLR 80.

## Knowledge-flow contract

- `role`: `LITERATURE_REDUCTION_SCOUT`
- `genuinely_new_information`: `true`
- `affected_lines`: `C19_R2_FSA_STATE_TRACKER`, `PROGRAMME_NOVELTY`, `POST_R2_REDUCTION`, `PERSISTENT_DYNAMICS_RESIDUAL`, `FUTURE_EXTERNAL_VALIDATION`
- `novelty_or_reduction_impact`: stronger reduction pressure; R2 survival alone cannot support persistent-dynamics novelty; local/pre-semantic/history-derived predictive emergence is not a unique novelty axis.
- `audit_classification`: null
- `prospective_baselines_or_discriminators`: PSR/TPSR; epsilon-machine/causal-state reconstruction; extracted DFA/WFA; resource-matched reservoir; remote-history/washout scaling; local-causal-state diagnostic when relevant.
- `questions_for_evidence_analyst`: prioritize extracted/learned state reduction after R2 survival; place predictive-state compression before stronger persistent-dynamics claims; define a prospective remote-history discriminator; do not alter current R2 from this literature.
- `questions_for_control_brain`: remove local/pre-semantic/predictive-state emergence as standalone novelty axes; organize reductions by representation class; consider non-fading lineage-specific credit under matched privilege as the narrower residual target.
- `must_not_change_frozen_or_consumed`: immutable C19-v4, consumed C19-v2/v3, consumed R1-v1/v2, R1 transient outputs, consumed A01/RV01/RV02/CX, legacy immutable refs, current R2 pre-formal scientific/statistical/resource semantics, scheduler definitions.
