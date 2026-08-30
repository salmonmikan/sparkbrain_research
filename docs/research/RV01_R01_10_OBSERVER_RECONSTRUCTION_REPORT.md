# RV01 R01-10 — Observer Reconstruction Report

## Decision

R01-10 asks whether physically different learned trajectories can be grouped post hoc by stable
world consequence and matched causal-intervention signature without placing an equivalence class,
concept, Assembly, function, or meaning type in runtime.

```text
physically disjoint routes share one observer cluster:       YES
routes with different physical timing share that cluster:    YES
different raw external consequence is separated:             YES
equal cluster members share the causal-loss signature:       YES
Observer execution changes runtime trace:                    NO
Observer taxonomy renaming changes cluster membership:       NO
removing Observer changes runtime trace:                      NO
runtime stores functional-equivalence state:                 NO
post-hoc relation-candidate reconstruction supported:        YES
concept or semantic meaning formation supported:             NO
```

This is an Observer-side relation reconstruction candidate. It is not a runtime concept or meaning
formation result.

## Physical trajectories

Three separately trained recurrent Fields are used.

```text
trajectory A
path:       0 -> 1 -> 2 -> 3
interval:   5.0 ms
boundary:   port:101
world event: external:12

trajectory B
path:       4 -> 5 -> 6 -> 7
interval:   6.0 ms
boundary:   port:202
world event: external:12

trajectory C
path:       8 -> 9 -> 10 -> 11
interval:   4.5 ms
boundary:   port:303
world event: external:13
```

A and B have disjoint unit identities, different ordinary connection states, different boundary
ports, and different event timing. C is also physically disjoint but has a different raw world
consequence.

Every trajectory is stored as an immutable runtime record containing:

- physical path and training interval;
- intact Field units and times;
- targeted-intervention Field units and times;
- intact and intervened runtime hashes;
- learned connection-state hash;
- anonymous boundary count;
- raw external target identity.

No cluster ID is present in those records.

## Causal signature

The Observer derives a signature from immutable evidence only:

```text
raw external target
intact internal-chain event count
intact boundary count
targeted boundary impairment
targeted downstream impairment
```

The targeted intervention suppresses the physical middle edge of each route.

For all three trajectories:

```text
intact terminal reached:               YES
targeted terminal reached:            NO
targeted downstream impairment:       1.0
targeted boundary impairment:         1.0
```

A and B additionally share `external:12`, so they receive the same exact Observer signature and the
same cluster. C produces `external:13`, so it remains separate despite having the same intervention
loss shape.

## Why physical timing is excluded from the equivalence signature

A and B have different learned delays and different intact spike times. R01-10 intentionally asks
whether two physically distinct realizations can support the same world-facing causal relation.

Therefore physical timing remains visible in the immutable trajectory but is not required to match
for this particular Observer view.

This is not a claim that timing is irrelevant in general. A timing-sensitive Observer view could
legitimately separate them. Observer projections are non-exclusive analyses rather than unique
runtime ontologies.

## Observer non-interference

Before and after reconstruction, the canonical runtime-bundle hash is identical.

The Observer has no methods to:

- schedule an arrival;
- reinject a pulse;
- update a connection;
- present an external event;
- change a threshold;
- alter a queue;
- write a cluster into runtime.

Removing the Observer entirely leaves the runtime bundle unchanged.

## Taxonomy renaming

The same immutable trajectories are reconstructed twice with different human-readable taxonomy
prefixes.

```text
view-alpha-*
renamed-view-omega-*
```

Labels change. Cluster IDs and trajectory membership do not.

Thus human naming remains outside the causal computation.

## Runtime ontology boundary

The physical trajectory records contain no:

```text
functional_equivalence
concept_id
meaning_state
assembly_id
functional_role
relation_type
correct action
reward
```

The phrase “same relation” exists only as an Observer interpretation of a shared raw consequence and
shared causal signature.

## Interpretation

The strongest supported statement is:

> In a canonical engineering construction, two physically disjoint learned Field trajectories with
> different timing and ports can be grouped post hoc because they produce the same raw external
> consequence and lose that consequence under the same class of targeted physical intervention.
> Observer execution, removal, and taxonomy renaming do not change runtime.

The following stronger statement is not supported:

> The runtime formed a concept, understood that the trajectories mean the same thing, or created an
> internally reusable equivalence class.

R01-10 therefore demonstrates an evidence-preserving way to discuss relation candidates without
putting those categories into the Primary runtime. It does not yet show that such equivalence changes
future cognition or transfers to unseen physical realizations.

## Validation

The integrated branch CI covering the observer reconstruction, physical trajectories, intervention
controls, deterministic replay, and source-boundary tests passed on Python 3.11 and Python 3.13.

## Next gate

R01-11 tests safety and resource containment of the physical substrate:

- bounded event and queue growth;
- bounded recurrent fan-out;
- loop/oscillation containment;
- local failure containment;
- plasticity saturation and lower bounds;
- continued prohibition on endogenous self-confirmation;
- complete resource records for every stress condition.
