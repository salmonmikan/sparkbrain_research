# SparkBrain v0.6 Endogenous Chain Engineering Report

## Scope

V06-09 adds an Assembly-free, taxonomy-free runtime and canonical intervention suite for testing
whether an actual endogenous Field Spark can become the causal source of later anonymous internal
Field events during external silence.

Under Protocol Amendment 002, this is a **single-world Level-2 engineering candidate**: the root
Spark causally changes later anonymous events. It is not a confirmatory Level-2 result and does not
yet establish a Level-3 externally stabilized and revisable anonymous causal relation.

## Runtime path

```text
external-in cue event
        ↓
G1/G2 anonymous local proposal
        ↓
normal-rule Field reinjection
        ↓
endogenous Field Spark at depth 1
        ↓
new local proposal created only after that Spark occurs
        ↓
normal-rule Field reinjection
        ↓
endogenous Field Spark at depth 2
        ↓
repeat within depth / energy / proposal budgets
```

The later proposal is not preloaded with the root proposal. It is created only after the preceding
endogenous `SpikeEvent` has occurred. Proposal records retain anonymous source and target identity,
source origin, source time, generation depth, local path, causal parent, reinjection decision, and
intervention reason.

## Runtime ontology inventory

The Primary runtime contains only:

- anonymous unit and local-path IDs;
- external-in and endogenous event direction;
- time, magnitude, polarity, and generation depth;
- causal proposal and Spark parentage;
- local lag and transition state;
- eligibility and external-consistency state;
- bounded reinjection, branch, event, lifetime, and energy state;
- anonymous intervention targets and runtime counters.

It contains no:

```text
Assembly state
PredictionRelation
ActionRelation
MemoryRelation
RewardRelation
FunctionalRole
MeaningState
correct action
scalar reward
outcome class
```

## Observer/evaluator taxonomy inventory

The evaluator derives only post-hoc views:

- whether the root changed later anonymous internal events;
- the size and timing of that anonymous downstream trace;
- targeted versus matched-random impairment;
- whether external-observation or positive-update counts changed;
- whether a physical unit or local path was necessary in this canonical world.

These view names are not fed back into runtime. The same lineage is not assigned a one-hot function
class.

## Canonical world

The canonical suite learns two disjoint anonymous external transition chains:

```text
main:    unit:0 -> unit:1 -> unit:2 -> unit:3
control: unit:4 -> unit:5 -> unit:6 -> unit:7
```

The Field has no physical synaptic connections in this probe. During evaluation it receives only two
external-in cue events:

```text
unit:4 cue at 100 ms
unit:0 cue at 150 ms
```

All later units in each chain are generated from local transition state, reinjection, and actual Field
threshold crossings during external silence.

## Canonical engineering result

```text
sham main chain:                    1 -> 2 -> 3
sham control chain:                 5 -> 6 -> 7

targeted expansion suppression:    1
matched-random expansion control:  1 -> 2 -> 3
matched-random control chain:       5

root reinjection suppression:       no main endogenous Spark
downstream reinjection suppression: 1
```

The targeted intervention suppresses expansion from anonymous main-chain `unit:1`, preserving the
root Spark while removing both later anonymous Sparks. The matched-random intervention suppresses
the same expansion stage in the active disjoint control chain at `unit:5`; the main chain remains
intact.

```text
sham downstream count:           2
targeted downstream count:       0
matched-random downstream count: 2
targeted impairment:             1.0
matched-random impairment:       0.0
selective effect:                1.0
```

## Anti-shortcut boundaries

- each later proposal is created at the preceding endogenous Spark time;
- future chain steps are not preloaded in one pending queue;
- proposal sources remain `endogenous-unconfirmed`;
- only actual Field `SpikeEvent` values can expand the chain;
- suppressing root reinjection removes the complete main chain;
- suppressing the next reinjection path preserves the root but removes later Sparks;
- an active, stage-matched intervention on the disjoint control chain leaves the main chain intact;
- no external observation is synthesized during silence;
- no endogenous-only chain commits a positive G2 update;
- no Assembly, functional type, human meaning, correct target, or scalar reward enters runtime.

## Current limitation

The chain is produced by anonymous local transition state learned from externally observed unit
transitions. It is stronger than a preloaded pending queue because each next proposal is created only
after the preceding endogenous Field Spark, but it remains a deliberately simple G1/G2 mechanism.

The current result does not establish:

- confirmatory reproduction across preregistered worlds and seeds;
- an effect on an anonymous outbound boundary event or external event stream;
- external stabilization of the chain relation across held-out perturbations;
- relation revision after a changed world contingency;
- delayed persistence outside the explicit local transition state;
- equivalence of physically different trajectories by matched causal signature;
- memory stored in membrane, adaptation, topology, or recurrent Field state;
- functional, linguistic, subjective, or semantic meaning.

## Claim boundary

The strongest permitted statement for this slice is:

> In a canonical Assembly-free and taxonomy-free engineering world, an actual endogenous Field
> Spark causally initiated later anonymous endogenous Field Sparks during external silence;
> suppressing the target expansion or reinjection path selectively removed the downstream chain,
> while an equally staged active intervention on a disjoint control chain did not damage the target
> chain. The internal chain created neither external observations nor positive self-confirming
> learning updates.

This is a V06-09 **Level-2 engineering candidate**, not a confirmatory Gate-D/Gate-E result and not a
Level-3 externally stabilized relational result.
