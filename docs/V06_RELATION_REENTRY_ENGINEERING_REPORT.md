# SparkBrain v0.6 Relation Re-entry Engineering Report

## Scope

V06-12 tests whether externally acquired anonymous relation state is merely recorded or actually
changes a later normal-rule Field trajectory.

Protocol Amendment 003 requires this step before the existing single-world Level-3 candidate can be
described as a closed functional loop. The implementation reuses the existing
`AnonymousLinkState`/`UntypedBoundaryConsistency` state and the existing `FieldReinjectionGate`; it
does not add a new semantic memory, reward state, action selector, or evaluator-chosen winner.

This is an engineering result, not a confirmatory multi-world Level-3 result.

## Runtime path

```text
previous anonymous boundary event
        ↓
raw external event
        ↓
existing anonymous consistency state
        ↓
read-only structural projection
        ↓
EndogenousPulseProposal
        ↓
existing FieldReinjectionGate
        ↓
ordinary membrane / threshold / refractory / adaptation
        ↓
later Field Spark or no Spark
```

All eligible links are projected through the same rule. The evaluator does not select the strongest
link. Competing proposals enter the Field and ordinary current magnitude and threshold determine
which target fires.

## Structural projection

The reference implementation reads only existing anonymous values:

- outbound port ID;
- external target ID;
- polarity;
- consistency and inconsistency counts;
- reliability;
- mean lag;
- mean magnitude ratio;
- causal source references.

The effective current is a bounded category-free function of the existing reliability and magnitude
ratio. No field states that a relation is predictive, action-related, memory-related, rewarded,
correct, useful, or meaningful.

## Canonical conditions

The same `port:7` relation is examined after four previously established world histories.

### Acquisition

```text
learned relation: port:7 -> unit:8
reliability:      0.8
projected current: 0.72
accepted proposals: 1
later Field Spark: unit:8
```

### Reversal

```text
old relation: port:7 -> unit:8, reliability 0.5, current 0.45
new relation: port:7 -> unit:9, reliability 0.8, current 0.72
accepted proposals: 2
later Field Spark: unit:9
```

Both eligible links are projected. The evaluator does not perform `argmax`; ordinary Field threshold
separates the stronger and weaker currents.

### Return to the original contingency

```text
old relation: port:7 -> unit:8, reliability 7/11, current 6.3/11
new relation: port:7 -> unit:9, reliability 0.5, current 0.45
later Field Spark: unit:8
```

The restored relation dominance is therefore accompanied by a restored later Field response.

### Stable world

```text
relation: port:7 -> unit:8
reliability: 10/11
later Field Spark: unit:8
```

## Required controls

### No relation re-entry

No structural proposal is scheduled and no later Spark occurs.

### Consistency reset

The acquired relation artifact remains available to the evaluator, but the runtime consistency state
presented to the re-entry mechanism is empty. No proposal and no later Spark occur.

### Matched unrelated relation

A learned relation on `port:9` does not affect a probe on `port:7`. No target proposal or later Spark
occurs.

### Internal-only exposure

Boundary recurrence without returned external events creates no positive anonymous link and therefore
cannot change the re-entry response.

### Relation suppression

Suppressing re-entry for the probed port returns both acquired and reversed conditions to the same
baseline response. This distinguishes relation-state use from unrelated differences in the earlier
training histories.

## Self-confirmation boundary

Relation re-entry does not increment:

- external observation count;
- committed positive G2 updates;
- independent evidence count.

The consistency state is read but not mutated by the re-entry probe. A Spark caused by relation
re-entry remains endogenous and cannot positively confirm the state that generated it.

## Runtime ontology inventory

The Primary runtime uses:

- anonymous port and target IDs;
- timing, magnitude, polarity, and reliability;
- provenance and causal parent IDs;
- existing consistency state;
- proposal and reinjection budgets;
- ordinary Field state.

It contains no:

```text
Assembly state
PredictionRelation
ActionRelation
MemoryRelation
RewardRelation
correct action
scalar reward
utility target
functional role
meaning state
```

## Focused validation

`tests/v06/test_relation_reentry.py` verifies:

- acquired relation changes later Field Dynamics;
- reversal changes the later endogenous Field Spark;
- return to the old contingency restores the old Field response;
- stable relation preserves the response;
- no-reentry and consistency-reset controls remove the effect;
- an unrelated active relation does not reproduce the target effect;
- all eligible links use one projection rule rather than evaluator `argmax`;
- no external observation or positive self-confirmation is created;
- runtime remains Assembly-free and taxonomy-free.

## Claim boundary

The strongest permitted statement is:

> In a canonical taxonomy-free engineering construction, externally acquired and revised anonymous
> consistency state was reused through the ordinary proposal and Field-reinjection path. Relation
> acquisition, reversal, and reacquisition changed the identity of a later normally thresholded Field
> Spark, while no-reentry, consistency-reset, matched-unrelated, relation-suppression, and
> internal-only controls removed or failed to reproduce the effect.

This closes the previously missing causal loop in one controlled world. It does not establish
multi-world generalization, a distributed Field memory, semantic meaning, autonomous value,
human-like action selection, or a confirmatory Level-3 result.
