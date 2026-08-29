# SparkBrain Theory Specification v0.6 — Endogenous Spark Function

Status: **V06-00–V06-06 engineering foundation implemented; Protocol Amendment 001 adopted before confirmatory science**  
Target namespace: `sparkbrain.v06`  
Baseline: `main@03a5c662a5ea100fac3288b6aa3e82c1d41f0546`  
Normative amendment: `docs/V06_PROTOCOL_AMENDMENT_001_ENDOGENOUS_SPARK_FUNCTION.md`

## 1. Central hypothesis

The Primary runtime must not require an explicit Assembly state or semantic unit.

v0.6 tests whether a persistent Dynamic Field can generate endogenous Sparks that are not direct
copies of current external input, allow those Sparks to participate causally in subsequent internal
Dynamics, prediction, action, and memory, and form stable externally correctable functional
relations through continued interaction with the world.

```text
external signal
      ↓
persistent Dynamic Field
      ↓
endogenous Spark X
      ↓
subsequent Spark / Cascade / prediction / action / memory effect
      ↓
external consequence
      ↓
confirmation, contradiction, or revision of the responsible path
```

Missing-middle completion is one controlled assay of this capacity. It is not the central definition
of v0.6.

## 2. Meaning is not a Spark attribute

The runtime must not attach a human semantic value to a Spark:

```text
meaning = "danger"
semantic_state = "food"
concept_label = "cat"
```

A candidate functional meaning is treated only as an observed relation pattern:

\[
FunctionalRelation(X) \approx Relations(
    X,
    OtherInternalEvents,
    Predictions,
    Actions,
    MemoryChanges,
    ExternalConsequences,
    Corrections
)
\]

The Primary runtime may contain causal transition state, eligibility, action bias, and externally
confirmed local relation state. It must not contain a human-readable meaning field. A post-hoc
observer may describe recurring functional relations but may not feed them back into runtime.

## 3. Observer boundary

Assembly remains an observer concept:

```text
immutable runtime trace
      ↓
post-hoc Assembly / trajectory / functional-relation observer
```

The runtime path is:

```text
persistent Field state
      ↓
G0/G1/G2 endogenous transition
      ↓
internal pulse proposal
      ↓
normal-rule Field reinjection
      ↓
later internal and external consequences
```

For identical initial state, seed, and external input:

\[
Runtime(Observer=ON)=Runtime(Observer=OFF)
\]

Field traces, queues, predictions, actions, learning updates, RNG state, and state hashes must be
identical. Only observer artifacts may differ.

## 4. Runtime state

The Primary runtime state is:

\[
B_t=(F_t,Q_t^{ext},Q_t^{endo},Z_t,T_t,H_t,R_t,C_t,L_t)
\]

- `F`: current excitable-Field state;
- `Q_ext`: external event queue;
- `Q_endo`: endogenous proposal queue;
- `Z`: persistent local traces;
- `T`: local transition state;
- `H`: homeostatic and adaptation state;
- `R`: generation budgets;
- `C`: reality-matching state;
- `L`: externally gated local eligibility and relation updates.

No Assembly ID, prototype, membership, semantic label, hidden world-state label, or correct action
belongs to `B_t`.

## 5. Endogenous Spark levels

### Level 1 — Endogenous Event

A Spark is internally originated rather than directly supplied by an external pulse.

This is necessary but weak. Random noise or a delayed echo may satisfy it.

### Level 2 — Predictive Endogenous Spark

An internally originated Spark is generated from persistent state before a later external event and
predicts a future Field or world transition better than matched random, echo, queue, and
frequency-only controls.

### Level 3 — Functionally Relational Endogenous Spark

An endogenous Spark or causal lineage:

- changes later internal Dynamics;
- changes a prediction;
- changes an action or action bias;
- changes a memory or eligibility update;
- forms a stable relation with later external consequences;
- remains externally correctable;
- loses the relevant function under targeted dynamic-path intervention beyond matched random
  controls.

Level 3 is the central v0.6 target. It remains a functional relation claim, not semantic
understanding.

## 6. Provenance

Every runtime pulse has exactly one origin:

- `external`;
- `endogenous-unconfirmed`;
- `endogenous-confirmed`;
- `endogenous-contradicted`;
- `endogenous-expired`.

Only `external` counts as an observation. A prediction that causes a Field Spark remains a
prediction until later external confirmation.

## 7. Two-phase learning

An endogenous path may create a temporary eligibility record, but it cannot commit a positive
update.

```text
endogenous generation
      ↓
uncommitted eligibility
      ↓
later registered external consequence
      ↓
commit, contradict, or expire
```

Positive learning is committed only after a registered external event or externally grounded
consequence confirms the responsible path. Contradiction and expiry cannot increase confidence.

This rejects:

```text
predict X
  → internally fire X
  → count X as observed
  → increase confidence
```

## 8. Functional relation without a meaning field

For an endogenous event or lineage `X`, the scientifically relevant object is not a label but a
relation profile measured over experience:

\[
R(X)=
\left(
P(Y_{internal}|X),
P(Y_{external}|X),
P(Y_{external}|X,a),
\Delta Prediction,
\Delta Action,
\Delta Memory,
Correction(X)
\right)
\]

- `Y_internal`: later Sparks, Cascades, or persistent-state changes;
- `Y_external`: later raw external events;
- `a`: action primitive;
- `Delta Prediction`: causal change in prediction;
- `Delta Action`: causal change in action probability or choice;
- `Delta Memory`: causal change in eligible or committed memory state;
- `Correction(X)`: response to later confirmation or contradiction.

The runtime may embody these relations in local transitions and path state. The observer may estimate
and compare `R(X)` after the run. Neither side assigns a human word to X.

## 9. Generator hierarchy

```text
G0  Field-only spontaneous continuation       Primary
G1  local temporal expectation traces         Primary
G2  sparse/local transition adaptation        Primary
G3  generic recurrent predictor               Comparator
G4  explicit Assembly-conditioned predictor   Comparator
```

G0–G2 are the SparkBrain Primary mechanisms. G3 and G4 are alternative explanations and performance
comparators.

- G3-only success means an external recurrent predictor supplied the cognition.
- G4-only success means explicit Assembly state was useful and the observer-only hypothesis was not
  supported.

## 10. Non-copy and state-dependence requirements

An endogenous Spark is not considered a meaningful research result merely because its origin flag is
internal.

Primary evidence must distinguish it from:

- a direct copy of the current external target;
- a fixed-delay echo;
- a remaining scheduled queue event;
- a random noise pulse;
- a frequency-only response;
- a hidden evaluator cue.

The same external input under different persistent Field states should be able to produce different
endogenous responses when history warrants it.

## 11. Internal causal participation

An endogenous Spark becomes a candidate cognitive material only when it changes later computation.
Required intervention targets include:

- the endogenous event itself;
- its local transition path;
- its persistent trace source;
- its reinjection branch;
- its downstream eligibility or action-bias path.

The intervention order is:

```text
intervene on Dynamics
      ↓
measure lost or changed function
      ↓
use the observer afterward to describe recurring trajectories
```

An Assembly ID must not be chosen first as the Primary intervention target.

## 12. External correction

A functionally useful endogenous Spark remains a hypothesis, not an observation.

When external reality agrees:

- the responsible eligibility may commit;
- timing, magnitude, or local relation confidence may update;
- repeated confirmed relations may stabilize.

When external reality disagrees:

- stale branches are cancelled or suppressed;
- confidence decreases;
- the external event is processed as authoritative input;
- the whole Field must not be unconditionally reset unless a matched control proves that necessary;
- the internal chain may not self-confirm.

## 13. Missing-middle as a validity assay

For an external sequence `A → B → [C omitted] → D`, forward completion requires:

\[
t(C_{endo}) < t(D_{external})
\]

Inferring C after D arrives is retrospective reconstruction and is scored separately.

Passing this assay does not by itself establish Level 3 functionality. Failing it does not by itself
invalidate all forms of functionally relational endogenous activity.

## 14. Physical trajectory versus functional relation

A functional relation need not be tied to exactly the same physical unit sequence.

For example:

```text
Episode 1: 13 -> 27 -> 41
Episode 2: 14 -> 29 -> 38
Episode 3: 12 -> 27 -> 42
```

may be considered a post-hoc functional-equivalence candidate only if the trajectories have matched
causal consequences across prediction, action, memory, and correction. Surface similarity alone is
insufficient.

This equivalence is an observer-level scientific conclusion unless and until a future version tests
whether the runtime itself requires such a role representation.

## 15. Memory location

v0.6 tests where experience-dependent changes reside:

- weight or delay;
- threshold or adaptation baseline;
- persistent multi-timescale state;
- local transition state;
- endogenous queue and working continuation state;
- externally gated eligibility and relation state.

Reset and transplant experiments must distinguish temporary pending state from persistent learned
state.

## 16. Revised scientific evidence order

1. runtime integrity and observer independence;
2. internally originated, non-copy Spark generation;
3. dependence on persistent internal state rather than only current input;
4. bounded autonomous internal continuation;
5. causal participation in later Dynamics;
6. stable externally confirmed relations to prediction, action, or memory;
7. external correction and relation revision;
8. memory-locus and causal-path analysis;
9. missing-middle and other controlled validity assays.

## 17. Current implemented contracts

- external/endogenous event provenance;
- endogenous proposals and chains;
- two-phase eligibility;
- external-confirmation-only positive learning;
- Assembly-free runtime-state validation;
- immutable observer trace;
- observer ON/OFF equality helper;
- fail-closed development checkpoint integrity;
- G0 queue-drain diagnostic;
- G1 local temporal expectation;
- G2 externally gated sparse local adaptation;
- confidence- and budget-bounded normal-rule Field reinjection.

## 18. Current non-claims

The implemented foundation does not yet establish:

- non-copy state-dependent endogenous cognition;
- autonomous endogenous Spark chains;
- causal downstream participation;
- stable prediction/action/memory relations;
- relation equivalence across physical trajectories;
- live reality correction;
- forward missing-middle completion;
- a resolved memory locus;
- semantic meaning, concepts, organs, consciousness, AGI, or biological equivalence.

`docs/V06_RUNTIME_INVARIANTS.md` remains normative for implementation safety. Protocol Amendment 001
is normative for scientific scope after V06-06.
