# SparkBrain Theory Specification v0.6
## Untyped Functional Endogenous Dynamics

Status: **V06-00–V06-08 engineering work in progress; no confirmatory Level-2/Level-3 claim**  
Target namespace: `sparkbrain.v06`  
Baseline: `main@03a5c662a5ea100fac3288b6aa3e82c1d41f0546`  
Normative amendments:

1. `docs/V06_PROTOCOL_AMENDMENT_001_ENDOGENOUS_SPARK_FUNCTION.md`
2. `docs/V06_PROTOCOL_AMENDMENT_002_UNTYPED_RELATIONAL_DYNAMICS.md`

## 1. Central hypothesis

The Primary runtime must not require an explicit Assembly, semantic unit, or predeclared functional
relation type.

v0.6 tests whether a persistent Dynamic Field can generate endogenous Sparks that are not direct
copies of current external input, let those Sparks causally alter later anonymous Field states and
boundary-crossing events, and stabilize or revise those relations through external interaction.

```text
world-to-field event
      ↓
persistent Dynamic Field
      ↓
endogenous Spark X
      ↓
later anonymous internal state / event / boundary crossing
      ↓
changed external stream
      ↓
external consistency or contradiction changes the responsible path
```

Prediction, action, memory, reward, role, and meaning are not runtime types. They are possible
post-hoc descriptions of causal trace properties.

## 2. Runtime ontology and observer taxonomy

### 2.1 Runtime ontology

The runtime contains execution-level structure only:

- anonymous unit/channel/region/boundary-port identity;
- time, magnitude, polarity, and duration;
- event origin and boundary direction;
- causal parent and local path identity;
- current and persistent Field state;
- local lag and signed influence state;
- eligibility and external consistency state;
- bounded transition reliability;
- generation and safety budgets.

This ontology states **where, when, how strongly, and through which path** an event occurred. It does
not state why the event matters or which human functional category it belongs to.

### 2.2 Observer taxonomy

An evaluator may later ask whether an endogenous lineage:

- preceded a later event and improved future estimation;
- changed an anonymous outbound boundary-port event;
- changed persistent state after a gap;
- changed the later world-to-field stream;
- changed its future behaviour after contradiction.

These may be reported as predictive, boundary-effect, persistence, world-coupling, and correction
views. They are queries over the same trace, not separate runtime relation classes.

### 2.3 Non-reification rule

The Primary runtime must not contain:

```text
PredictionRelation
ActionRelation
MemoryRelation
RewardRelation
FunctionalRole
MeaningState
```

A lineage may satisfy several observer views. No one-hot functional class is required or permitted.

## 3. Meaning is not an attribute

The runtime must not attach:

```text
meaning = "danger"
semantic_state = "food"
role_type = "prediction"
concept_label = "cat"
```

The most primitive relation available to runtime is category-neutral:

\[
U(i,j)=
\left(
source_i,
 target_j,
 \Delta t,
 signed\ influence,
 reliability,
 provenance,
 external\ consistency
\right)
\]

An observer may estimate a wider causal signature:

\[
R_X=
\left\{
(X \rightarrow Y_k),
\Delta t_k,
\Delta P(Y_k\mid do(X)),
stability_k,
consistency_k
\right\}
\]

`Y_k` may be an anonymous internal event, state component, outbound boundary event, or external
event. The signature contains no human semantic label and need not exist as one global runtime object.

A functional meaning candidate is, at most, an observer conclusion that a stable causal signature
has formed and remains externally revisable. It is not semantic understanding.

## 4. Runtime state

The Primary state is:

\[
B_t=(F_t,Q_t^{in},Q_t^{endo},Q_t^{out},Z_t,T_t,H_t,R_t,C_t,L_t)
\]

- `F_t`: current excitable-Field state;
- `Q_in`: world-to-field event queue;
- `Q_endo`: endogenous proposal and reinjection queue;
- `Q_out`: anonymous field-to-world boundary events;
- `Z_t`: persistent local traces;
- `T_t`: local anonymous transition state;
- `H_t`: homeostatic and adaptation state;
- `R_t`: generation and resource budgets;
- `C_t`: external consistency state;
- `L_t`: externally gated eligibility and local relation updates.

No Assembly ID, motif label, semantic label, hidden world-state label, correct-action identity,
relation type, reward value, or functional role belongs to `B_t`.

## 5. Event directions and provenance

Every pulse has execution-relevant direction and provenance.

Direction candidates:

- world-to-field;
- field-internal;
- field-to-world boundary.

Endogenous status candidates:

- external;
- endogenous-unconfirmed;
- endogenous-confirmed;
- endogenous-contradicted;
- endogenous-expired.

Only a world-to-field external event counts as an observation. An internally generated event remains
endogenous even if it causes a normal Field Spark or outbound boundary event.

## 6. Two-phase learning and external authority

An endogenous path may create temporary eligibility but cannot commit a positive update from its own
activity.

```text
endogenous lineage
      ↓
uncommitted local eligibility
      ↓
later external consistency
      ↓
commit, contradict, or expire
```

Positive strengthening requires a later registered external event or externally observed world-loop
consistency. Internal recurrence cannot count as confirmation.

This rejects:

```text
internally produce X
  → internally observe X
  → increase confidence in X
```

External mismatch may weaken, redirect, or retire the responsible anonymous path. The external event
is authoritative but need not cause a full Field reset.

## 7. No privileged reward

A global scalar reward supplied by an experimenter would predefine value and therefore does not
belong to the Primary v0.6 track.

The world may emit raw external pulses. Anonymous homeostatic variables may exist as ordinary state
components, but the runtime must not receive `good`, `bad`, `reward`, `punishment`, `goal`, or correct-
action labels.

Reward-driven or typed value systems belong only to isolated comparators.

## 8. Boundary coupling without an action type

The Field may emit through an anonymous outbound port:

```text
internal Dynamics
      ↓
outbound port:k
      ↓
world transition
      ↓
later world-to-field events
```

The runtime stores the boundary crossing and causal lineage. It does not store `action_type`, action
meaning, or correctness. The observer may later report that the lineage influenced behaviour.

## 9. Persistence without a memory type

Experience may alter:

- weights or delays;
- thresholds or adaptation;
- persistent traces;
- local transition state;
- eligibility;
- boundary-coupling state;
- pending working state.

The runtime does not create a `MemoryRelation`. A memory-like conclusion requires delayed effect,
reset, transplant, and matched-control evidence.

## 10. Revised endogenous evidence levels

### Level 1 — Endogenous origin

A normally thresholded Field Spark is generated without a direct external event at that target/time.
This remains compatible with noise, echo, or useless activity until controls exclude them.

### Level 2 — Causally Participating Endogenous Spark

The Spark changes a later anonymous internal state, endogenous event, boundary event, or external
event stream. Targeted intervention must exceed matched random and sham controls.

### Level 3 — Externally Stabilized Relational Endogenous Spark

The Spark or lineage participates in a stable, externally confirmable and revisable pattern of
anonymous causal relations across held-out conditions. The observer may derive multiple functional
views afterward.

Level 3 is the central v0.6 target. It is not a claim of subjective, linguistic, or human semantic
meaning.

## 11. Generator hierarchy

```text
G0  Field-only spontaneous continuation       Primary
G1  local temporal expectation traces         Primary
G2  sparse/local transition adaptation        Primary
G3  generic recurrent predictor               Comparator
G4  explicit Assembly-conditioned predictor   Comparator
G5  typed functional-head system               Comparator
```

G0–G2 are the Primary SparkBrain mechanisms.

- G3-only success means a generic external predictor supplied the function.
- G4-only success means explicit Assembly state was required.
- G5-only success means predeclared human functional categories were required.

## 12. Non-copy and persistent-state requirements

An endogenous Spark is not accepted merely because its origin flag is internal. Primary evidence
must distinguish it from:

- a direct copy of current input;
- a fixed-delay echo;
- a pending queue event;
- random noise;
- a frequency-only response;
- an evaluator-supplied target;
- a typed comparator leaking into the Primary path.

The same current external input under different valid prior states may produce different internal
responses when history warrants it. Identical full state must reproduce identically.

## 13. Untyped causal participation

An endogenous Spark becomes candidate cognitive material only when it changes later computation.
The Primary measurement is the complete anonymous trace difference:

\[
\Delta Trace_X = Trace(do(X=present)) - Trace(do(X=suppressed))
\]

The trace may include:

- later internal events;
- later state components;
- outbound boundary events;
- later external events;
- anonymous local transition or eligibility changes.

The runtime does not label any component as prediction, action, memory, or reward. Observer views are
derived after causal measurement.

## 14. Untyped relation stabilization

A candidate relation is stabilized when:

- the anonymous source-to-target causal effect recurs across episodes;
- it survives held-out perturbations where appropriate;
- external consistency raises its local reliability;
- contradiction lowers or redirects it;
- internal-only recurrence does not strengthen it;
- targeted intervention removes the effect;
- no typed relation field is needed.

The relation may remain distributed across local state rather than becoming a named object.

## 15. Functional observer projections

The observer may apply several projections to a stable relation signature.

### Predictive view

Did the lineage precede and improve estimation of a later event?

### Boundary-effect view

Did the lineage change anonymous outbound-port events?

### Persistence view

Did the lineage leave a delayed state effect that survives the required controls?

### World-coupling view

Did boundary activity change the later external stream?

### Correction view

Did external mismatch revise the responsible anonymous path?

These are non-exclusive measurements. Renaming, deleting, or permuting them must not change runtime.

## 16. Missing-middle as one validity assay

For `A → B → [C omitted] → D`, forward completion requires:

\[
t(C_{endo}) < t(D_{external})
\]

Inference after D is retrospective reconstruction. Passing this assay supports one form of temporal
validity but does not by itself establish Level 2 or Level 3.

## 17. Physical trajectory and observer equivalence

Physically different trajectories may be post-hoc functional-equivalence candidates only if they
have matched causal relation signatures under intervention and external revision.

```text
Episode 1: 13 -> 27 -> 41
Episode 2: 14 -> 29 -> 38
Episode 3: 12 -> 27 -> 42
```

Unit similarity or Assembly similarity alone is insufficient. No equivalence label returns to the
Primary runtime in v0.6.

## 18. Taxonomy-independence requirement

For identical seed, initial state, and external stream, runtime output must remain identical when:

- observer/evaluator packages are absent;
- observer view names are changed;
- the evaluator permutes which outbound ports it describes as actions;
- prediction, memory, reward, and outcome terminology is removed from artifacts;
- the typed G5 comparator is disabled.

The following must match:

- Field trace;
- internal and outbound queues;
- local updates;
- boundary events;
- RNG state;
- state hash;
- checkpoint continuation.

Only observer artifacts may differ.

## 19. Scientific evidence order

1. runtime, observer, and taxonomy independence;
2. non-copy endogenous Field Spark;
3. persistent-state dependence;
4. bounded autonomous internal continuation;
5. untyped causal participation;
6. externally stabilized anonymous relation;
7. external correction and revision;
8. persistence-locus and physical-trajectory analysis;
9. missing-middle and other validity assays;
10. G3/G4/G5 comparator interpretation.

## 20. Current implementation and current limits

Implemented engineering foundation includes:

- external/endogenous provenance;
- two-phase eligibility;
- Assembly-free runtime validation;
- immutable observer trace;
- G0 queue-drain diagnostic;
- G1 local temporal expectation;
- G2 externally gated sparse local adaptation;
- normal-rule reinjection;
- external-authoritative reality correction;
- non-copy and state-dependence evaluation contracts;
- one single-world, history-dependent, normally thresholded Field-Spark candidate.

Not yet established:

- multi-world Level-1 evidence;
- autonomous endogenous chains;
- untyped causal participation;
- anonymous boundary coupling;
- externally stabilized relations;
- relation revision;
- taxonomy independence under full future functionality;
- persistence locus outside explicit local transition state;
- physical-trajectory causal equivalence;
- confirmatory missing-middle validity;
- semantic meaning, concepts, value formation, organs, consciousness, AGI, or biological equivalence.

`docs/V06_RUNTIME_INVARIANTS.md` and both Protocol Amendments are normative.
