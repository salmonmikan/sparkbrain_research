# SparkBrain v0.6 Protocol Amendment 002
## Prediction, Action, Memory, and Reward Remain Observer Projections

**Amendment date:** 2026-08-29  
**Branch:** `v06`  
**Adopted before:** V06-09 confirmatory autonomous-chain and functional-relation experiments  
**Normative after:** Protocol Amendment 001  
**Preserves:** all accepted V06-00–V06-08 engineering results and negative findings

## 1. Reason for the amendment

Protocol Amendment 001 correctly re-centred v0.6 on internally originated Sparks and moved
missing-middle completion to a validity assay. The remaining Master Plan still described downstream
function with categories such as:

```text
prediction
action
memory
reward / beneficial outcome
```

Those terms are legitimate **scientific questions asked by an observer**. They must not become
predeclared relation types or privileged modules in the Primary runtime.

If the runtime contains objects such as:

```text
PredictionRelation
ActionRelation
RewardRelation
MemoryRelation
```

then a human has already decided what kind of function an internal Spark is allowed to have. This
would reintroduce a semantic ontology after v0.4 removed semantic Spark labels and v0.6 removed
explicit Assembly state.

The correction is therefore:

> The Primary runtime stores and updates only anonymous events, state changes, local transitions,
> causal lineage, boundary crossings, and externally gated consistency. Prediction, action, memory,
> reward, role, and meaning are post-hoc projections over the same runtime trace.

## 2. Runtime is category-free, not structure-free

The runtime still needs minimal structural distinctions to execute causal dynamics.

### Permitted structural information

- anonymous unit, channel, region, or boundary-port ID;
- event time, magnitude, polarity, and duration;
- external-in, endogenous, and field-to-world boundary direction;
- causal parent and local path IDs;
- lag statistics and signed local influence;
- membrane, threshold, adaptation, refractory, and persistent trace state;
- eligibility and externally confirmed or contradicted consistency state;
- confidence or reliability of an anonymous transition;
- bounded generation resources.

These fields say **where, when, how strongly, and through which causal path** something happened.
They do not say what the event means or what functional category it belongs to.

### Forbidden functional ontology in the Primary runtime

- prediction relation or prediction role;
- action relation, policy role, or correct-action identity;
- reward relation, scalar reward target, utility label, or value class;
- memory relation, memory role, or recall class;
- outcome class, goal class, semantic role, functional role, or meaning field;
- one-hot assignment of a Spark lineage to any of the above;
- a dedicated prediction, action, memory, reward, or semantic head on the Primary path.

## 3. Untyped causal relation substrate

The Primary runtime may embody a local relation only in a category-neutral form such as:

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

A reference record may contain:

```text
source event/state reference
target event/state/boundary reference
lag distribution
signed effect size
stability or reliability
causal lineage
external match / contradiction status
```

It must not contain:

```text
relation_type = prediction
relation_type = action
relation_type = memory
relation_type = reward
meaning = ...
```

The relation may remain distributed across Field, local transition, eligibility, and boundary state;
a global `FunctionalRelation` object is not required and is not the Primary design.

## 4. Observer projections

The same anonymous runtime lineage may be inspected through several non-exclusive evaluation views.
These views are questions, not runtime classes.

### Predictive projection

Does the endogenous lineage precede and improve the distributional prediction of a later anonymous
Field or external event?

### Boundary-effect projection

Does suppressing the lineage change which anonymous field-to-world boundary-port events occur?
The observer may call this an action effect. The runtime sees only a boundary crossing.

### Persistence projection

Does the lineage change later state after a delay, survive a gap, or transfer under reset/transplant?
The observer may call this a memory effect. The runtime stores only persistent state changes.

### World-coupling projection

Does a boundary event alter the later external event stream? The runtime sees a new external stream;
the observer may describe the causal loop.

### Correction projection

Does an external mismatch reduce, redirect, or retire the anonymous local relation? This is measured
from state and trace changes, not from a semantic correction label.

One lineage may satisfy several views at once. It must not be forced into exactly one functional
class.

## 5. No privileged reward in the Primary v0.6 track

A scalar `reward` supplied by the experimenter would define value before Spark relations have formed.
Therefore the Primary v0.6 track does not use a privileged reward field or `RewardRelation`.

The world may return ordinary raw external pulses and may contain anonymous internal homeostatic
channels. Such channels are processed as ordinary state variables; they are not named `good`, `bad`,
`reward`, `punishment`, or `goal` in runtime.

A reward-driven or value-head system may be implemented only as a clearly isolated comparator. If
only that comparator acquires useful behaviour, v0.6 must report that untyped relation formation was
not sufficient.

## 6. Boundary events instead of predeclared actions

The Primary runtime may emit a pulse through an anonymous outbound port:

```text
field event
    -> outbound port:7
    -> world transition
    -> later external pulses
```

The world adapter may physically interpret `port:7`, but the Field does not receive a semantic action
name or correct-action label. The evaluator may later ask whether an endogenous Spark changed the
outbound-port distribution and whether that change altered the world.

## 7. Persistent state instead of a memory relation

The runtime does not update a `MemoryRelation`. It changes ordinary Field, trace, transition,
eligibility, or boundary state.

Memory is an observer conclusion requiring evidence such as:

- an effect remains after a delay;
- reset of a candidate component removes the effect;
- transplant of that component transfers part of the effect;
- matched unrelated state does not transfer it.

## 8. Prediction is a temporal test, not a runtime role

An endogenous Spark is not tagged `predictive`. The evaluator calls it predictive only when:

- it precedes a later event;
- its presence changes the estimated future distribution;
- targeted suppression removes that advantage;
- matched random, echo, queue, and frequency controls do not explain the result;
- the external event can confirm or contradict the responsible path.

## 9. Revised evidence levels

### Level 1 — Endogenous origin

A non-copy internal Field Spark occurred.

### Level 2 — Causally Participating Endogenous Spark

The Spark changes a later anonymous internal state, endogenous event, boundary event, or externally
visible event stream under targeted intervention.

### Level 3 — Externally Stabilized Relational Endogenous Spark

The Spark or lineage participates in a stable, externally confirmable and revisable pattern of
anonymous causal relations across held-out conditions. Observer projections may subsequently report
predictive, boundary-effect, persistence, or world-coupling properties.

Level 3 remains a functional proto-meaning candidate only in qualified post-hoc discussion. It is
not semantic understanding.

## 10. Revised central question

> Can a persistent Dynamic Field generate endogenous Sparks not directly supplied by current input,
> let them causally alter later anonymous Field states and boundary-crossing events, and stabilize or
> revise those relations through external interaction, while prediction, action, memory, reward,
> role, and meaning remain observer-derived descriptions rather than runtime types?

## 11. Revised work packages

```text
V06-09  Autonomous endogenous chain and untyped causal participation
V06-10  Untyped relation stabilization and anonymous boundary coupling
V06-11  External revision and observer projection analysis
V06-12  Missing-middle and other validity assays
V06-13  Persistence-locus and causal dynamic-path analysis
V06-14  Brain Lab, taxonomy-independence audit, and local release
```

## 12. Required taxonomy-independence tests

1. Delete all evaluator projection labels and run the same runtime episode.
2. Rename `predictive`, `boundary-effect`, `persistence`, and `world-coupling` views.
3. Permute which outbound ports the evaluator describes as actions.
4. Remove every scalar reward or correct-action file from the Primary run.
5. Run with the Observer and typed evaluation package entirely absent.
6. Scan runtime source, checkpoint, config, and trace for forbidden functional fields.
7. Verify identical Field trace, outbound events, learning updates, RNG state, and state hash.
8. Verify that one lineage may satisfy multiple observer views without a one-hot runtime type.

Any runtime difference caused only by evaluation taxonomy is a Gate A failure.

## 13. Typed comparator

A separate comparator may use explicit prediction/action/memory/reward heads. It must be isolated
from the Primary import graph and receive the same input and resource budget where possible.

Interpretation:

- Primary untyped dynamics succeeds: supports taxonomy-independent relation formation.
- Typed comparator alone succeeds: explicit human functional categories were useful; the Primary
  SparkBrain hypothesis is not supported for that experiment.
- Both succeed: compare generalization, intervention specificity, stability, and resource cost.

## 14. Effect on existing implementation

The current V06-00–V06-08 code remains usable because its Primary runtime currently operates on
anonymous targets, timing, magnitude, polarity, provenance, local transitions, reinjection, and
external consistency. It has not yet implemented dedicated prediction/action/memory/reward relation
objects.

Future work must not introduce those types during V06-09 or V06-10. Existing evaluator terms may be
retained only as post-hoc metric names.

## 15. Audit rule

Every future implementation report must contain two explicit inventories:

```text
Runtime ontology
Observer/evaluator taxonomy
```

The runtime inventory must contain no PredictionRelation, ActionRelation, RewardRelation,
MemoryRelation, FunctionalRole, MeaningState, or equivalent hidden substitute.
