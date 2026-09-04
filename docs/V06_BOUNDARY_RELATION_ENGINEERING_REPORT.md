# SparkBrain v0.6 Anonymous Boundary Relation Engineering Report

## Scope

V06-10 extends the V06-09 endogenous chain into an anonymous Field-to-world boundary and records
external consistency without creating prediction, action, memory, reward, role, or meaning types in
the Primary runtime.

Under Protocol Amendment 002, this is a **single-world partial Level-3 engineering candidate**:

- the endogenous chain causally reaches an anonymous outbound boundary;
- the boundary event causally changes the raw external event stream;
- repeated external events stabilize an anonymous structural relation;
- internal-only boundary recurrence cannot stabilize that relation;
- targeted boundary suppression has a selective effect beyond an active matched-random control.

It is partial because contingency reversal and relation revision have not yet been demonstrated.

## Runtime architecture

```text
external-in cue
        ↓
anonymous endogenous Spark chain
        ↓
actual terminal Field Spark
        ↓
structural BoundaryCoupling
        ↓
anonymous field-to-world port event
        ↓
world-side physical adapter
        ↓
raw external-in pulse
        ↓
externally gated anonymous consistency state
```

The Field does not receive an action name, correct port, outcome class, scalar reward, utility value,
or semantic label.

## Runtime ontology

Primary runtime values are limited to structural quantities:

- anonymous unit, path, port, proposal, Spark, boundary, and external-event IDs;
- direction, time, magnitude, polarity, lag, and generation depth;
- causal parentage and source-state hashes;
- externally gated consistency, inconsistency, exposure, expiry, and reliability counts;
- boundary, world, event, energy, lifetime, and branch state.

The implementation does not define:

```text
PredictionRelation
ActionRelation
MemoryRelation
RewardRelation
FunctionalRole
MeaningState
correct_action
scalar_reward
outcome_class
```

## Canonical world

Two disjoint anonymous chains are used:

```text
main:    unit:0 -> unit:1 -> unit:2 -> unit:3 -> port:7
control: unit:4 -> unit:5 -> unit:6 -> unit:7 -> port:9
```

The world-side adapter maps the ports to raw external pulses:

```text
port:7 -> external-in unit:8 after 10 ms
port:9 -> external-in unit:9 after 10 ms
```

These mappings exist only as world physics. The Field receives no indication that one port is
correct, useful, rewarded, predictive, or action-like.

Three repeated main and control episodes are run in each condition.

## Canonical engineering result

### Sham

```text
main terminal endogenous Sparks: 3
control terminal endogenous Sparks: 3
port:7 boundary events: 3
port:9 boundary events: 3
external unit:8 events: 3
external unit:9 events: 3
port:7 -> unit:8 externally consistent count: 3
port:9 -> unit:9 externally consistent count: 3
link reliability after three consistent events: 0.8
```

### Targeted boundary suppression

`port:7` is suppressed while the internal main chain remains intact:

```text
main terminal endogenous Sparks: unchanged
port:7 boundary events: 0
external unit:8 events: 0
```

### Active matched-random boundary suppression

The equally active disjoint `port:9` is suppressed:

```text
main terminal endogenous Sparks: unchanged
port:7 boundary events: 3
external unit:8 events: 3
```

### Internal-only condition

Both world links are suppressed after boundary emission:

```text
port:7 boundary events: 3
port:9 boundary events: 3
raw external responses: 0
anonymous positive link states: 0
positive G2 commits: 0
```

Boundary recurrence by itself therefore does not stabilize a port-to-external relation.

## Causal engineering comparison

```text
sham main boundary count:           3
targeted main boundary count:       0
matched-random main boundary count: 3
targeted boundary impairment:       1.0
matched-random impairment:          0.0
selective boundary effect:          1.0

sham main external count:           3
targeted main external count:       0
matched-random main external count: 3
selective external-stream effect:   1.0
```

The targeted intervention changes the world-facing event stream without destroying the internal
terminal Spark. The active matched-random intervention changes the disjoint control stream without
damaging the main stream.

## External stabilization

`UntypedBoundaryConsistency` first stores a pending anonymous boundary exposure. It does not create a
positive link from that exposure alone. A matching registered external event may pair with at most
one pending boundary event and update only the structural tuple:

```text
(port_id, external_target, polarity, lag, magnitude ratio, reliability)
```

No relation type or functional label is stored.

After three externally paired events, the reference reliability is:

```text
(prior consistent 1 + observed consistent 3)
------------------------------------------------ = 0.8
(prior consistent 1 + prior inconsistent 1 + observed 3)
```

## Taxonomy non-interference

The observer can project the same boundary trace under arbitrary descriptive labels. Permuting
`view-alpha` and `view-beta` changes only the observer artifact. The Primary state hash remains
unchanged.

The test therefore checks a concrete Amendment-002 invariant:

```text
rename or permute an observer taxonomy
        -> no Primary runtime change
```

## Provenance correction discovered during implementation

The retained v0.4 `UnitState.source_pulse_ids` is cumulative across a unit's lifetime. Using that
cumulative list to identify the causal root of a new Spark caused prior-episode proposal roots to
leak into later episodes.

V06-10 corrects the adapter without modifying v0.4:

1. peek the actual pulse IDs arriving at each unit at the current event time;
2. run the retained Field;
3. assign proposal roots only from those per-arrival pulse IDs;
4. retain cumulative `source_pulse_ids` only as a legacy diagnostic field.

This correction prevents repeated episodes from mixing causal lineages.

## Validation

The clean post-fix branch run was:

```text
GitHub Actions run 33252273946
Python 3.11: PASS
Python 3.13: PASS
Install: PASS
Ruff lint: PASS
Local readiness: PASS
Default test suite: PASS
Bundle validation: PASS
```

Focused tests cover:

- anonymous structural boundary emission;
- boundary suppression without Spark mutation;
- raw world feedback without reward or answer labels;
- no relation stabilization from internal-only exposure;
- stabilization only after a registered external event;
- endogenous-event rejection as external consistency;
- targeted versus active matched-random boundary intervention;
- selective world-stream effects;
- observer taxonomy permutation non-interference;
- forbidden runtime taxonomy absence;
- repeated-episode causal-lineage isolation.

## Claim boundary

The strongest permitted statement for this slice is:

> In a canonical Assembly-free and taxonomy-free engineering world, a history-dependent endogenous
> Spark chain reached an anonymous outbound boundary and causally changed the raw external event
> stream. Repeated external events stabilized an anonymous structural relation, while internal-only
> recurrence did not. Targeted boundary suppression removed the corresponding external stream while
> preserving the internal terminal Spark, and an active stage-matched control-port intervention did
> not impair the target stream.

This is a single-world, externally stabilized anonymous relation engineering candidate. It is **not
yet a completed Level-3 result**, because relation revision under changed external contingencies,
held-out worlds/seeds, memory-locus analysis, and broader causal controls remain outstanding. It does
not establish semantic, linguistic, subjective, or human-like meaning.
