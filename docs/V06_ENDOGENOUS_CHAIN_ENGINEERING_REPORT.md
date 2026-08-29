# SparkBrain v0.6 Endogenous Chain Engineering Report

## Scope

V06-09 adds an Assembly-free runtime and canonical intervention suite for testing whether an actual
endogenous Field Spark can become the causal source of later endogenous Sparks during external
silence.

This is an engineering result. It does not yet establish held-out predictive validity, a stable
relation to external consequences, action utility, memory utility, or functional meaning.

## Runtime path

```text
external cue Spark
        ↓
G1/G2 local proposal
        ↓
normal-rule Field reinjection
        ↓
endogenous Field Spark at depth 1
        ↓
new G1/G2 proposal created at that Spark time
        ↓
normal-rule Field reinjection
        ↓
endogenous Field Spark at depth 2
        ↓
repeat within depth / energy / proposal budgets
```

The later proposal is not preloaded with the root proposal. It is created only after the preceding
endogenous `SpikeEvent` has occurred. Proposal records retain source origin, source time, generation
depth, local path, parent proposal, reinjection decision, and intervention reason.

## Canonical world

The canonical suite learns two disjoint external transition chains:

```text
main:    unit:0 -> unit:1 -> unit:2 -> unit:3
control: unit:4 -> unit:5 -> unit:6 -> unit:7
```

The Field has no physical synaptic connections in this probe. During evaluation it receives only two
external cue events:

```text
control cue at 100 ms
main cue at 150 ms
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

The targeted intervention suppresses expansion from main-chain `unit:1`, preserving the root Spark
while removing both downstream Sparks. The matched-random intervention suppresses the same stage in
the active disjoint control chain at `unit:5`; the main chain remains intact.

```text
sham downstream count:           2
targeted downstream count:       0
matched-random downstream count: 2
targeted impairment:             1.0
matched-random impairment:       0.0
selective effect:                1.0
```

## Anti-shortcut boundaries

- each downstream proposal is created at the preceding endogenous Spark time;
- downstream proposal sources remain `endogenous-unconfirmed`;
- only actual Field `SpikeEvent` values can expand the chain;
- suppressing root reinjection removes the complete main chain;
- suppressing the next reinjection path preserves the root but removes later Sparks;
- an active matched-random intervention leaves the target chain intact;
- no external observation is synthesized during silence;
- no endogenous-only chain commits a positive G2 update;
- the Primary runtime contains no Assembly, motif, meaning, correct-action, or outcome-label state.

## Current limitation

The chain is produced by an explicit local transition memory learned from externally observed unit
transitions. It is therefore stronger than a preloaded pending queue, but it is still a deliberately
simple G1/G2 temporal mechanism.

The current result does not show:

- prediction of held-out external outcomes across multiple worlds or seeds;
- a useful change in action or committed memory;
- a stable externally confirmed functional relation;
- relation revision after contingency reversal;
- physical-trajectory functional equivalence;
- memory stored in membrane, adaptation, topology, or recurrent Field state;
- semantic or subjective meaning.

## Claim boundary

The strongest permitted statement for this slice is:

> In a canonical Assembly-free engineering world, an actual endogenous Field Spark causally
> initiated later endogenous Field Sparks under external silence; suppressing the target expansion
> or reinjection path selectively removed the downstream chain, while an equally staged active
> control-chain intervention did not damage the target chain. The internal chain did not create
> external observations or positive self-confirming learning updates.

This is a V06-09 causal-chain engineering candidate, not a completed Level-2 or Level-3 scientific
result.
