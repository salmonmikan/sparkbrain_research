# RV01 R01-12 — Continual Interference and Capacity Protocol

## Status

This protocol is adopted after the R01-11 physical resource/safety boundary and before any held-out
interference capability result is opened.

```text
R01-12 development worlds: 5 families × 3 seeds = 15
R01-12 held-out worlds:    5 families × 10 seeds = 50
held-out capability run:   not executed
```

The world contract is implemented in:

```text
src/sparkbrain/research/rv01/interference_contract.py
```

## Research question

RV01 has shown that externally learned pairwise physical weights and delays can generate real Field
continuation without v0.6 G1/G2 runtime state. The present persistence result is nevertheless
edge-localized: route identity follows learned weights and timing follows learned delays.

R01-12 asks:

> When several experiences are written into the same physical Field, do the learned edges preserve
> multiple routes, express graded branch competition, and revise locally without uncontrolled
> interference—or does RV01 reduce to a fragile pairwise transition table embedded in connections?

This is a falsification and capacity experiment. It is not a new memory feature.

## No-rescue constraint

The tested runtime must remain the current RV01 physical architecture:

```text
ordinary Field units
ordinary recurrent connections
learned Connection.weight
learned Connection.delay_ms
external-only local plasticity
bounded execution guard
```

The following may not be added to rescue an interference failure:

```text
G1 LocalTemporalExpectation
G2 SparseLocalTransitionAdaptation
EndogenousPulseProposal planner
Assembly state
route ID in runtime
correct branch label
reward or utility
replay buffer
central sequence table
```

The evaluator may know the structural routes because it generated the world. The runtime may not.

## Development and held-out separation

Development seeds:

```text
0, 1, 2
```

Held-out seeds:

```text
100 through 109
```

The sets are disjoint. Held-out worlds are deterministic pure specifications and may be checked for
shape, hashing, seed replay, and forbidden fields before freeze. Their capability outcomes must not
be used to tune plasticity rates, edge budgets, thresholds, or pass criteria.

## Family 1 — Disjoint routes

Several routes use disjoint units and edges.

Purpose:

- establish the low-interference reference;
- verify that writing one physical route does not damage an unrelated route;
- distinguish global instability from overlap-specific interference.

Expected diagnostic:

```text
train route A
train route B
train route C
probe all routes after every phase
```

A failure here indicates broad instability or resource exhaustion rather than representational
ambiguity.

## Family 2 — Shared-cue branches

Three routes share the same initial cue and diverge immediately.

Purpose:

- test simultaneous outgoing alternatives;
- measure whether the Field represents several physical continuations or collapses to one edge;
- separate exposure frequency from a human-provided correct branch.

The three exposure counts are close and differ by at most two. All branches remain structurally
present in the world specification.

No branch is designated as the correct action. The evaluator reports:

- which branches remain physically active;
- first-Spark distribution;
- cross-branch contamination;
- whether exposure ordering changes the learned distribution.

## Family 3 — Shared-prefix branches

Three routes share two leading units and diverge after the common prefix.

Purpose:

- test interference after an already learned common transition;
- distinguish cue competition from delayed branch competition;
- measure whether the shared prefix remains stable while suffix edges change.

## Family 4 — Opposing-edge reversal

One route contains a directed edge and another route later contains the opposite directed edge.
A disjoint route acts as a control.

Purpose:

- test local reversal without global destruction;
- determine whether direction-specific weights remain separable;
- measure reacquisition and hysteresis;
- verify that the disjoint route is retained.

## Family 5 — Dense route load

Eight routes are exposed under an active-edge budget smaller than the total structural demand.

Purpose:

- reveal capacity pressure rather than hiding it;
- measure which edges survive and why;
- identify whether failure is abrupt, gradual, order-dependent, or localized to high-fanout units;
- compare physical Field storage with a resource-matched reservoir/transition comparator.

The edge budget is part of the preregistered world and may not be raised after seeing a failure.

## Required development measurements

For every world and training phase, record at least:

- exact route and edge exposure counts;
- active physical edge count;
- outgoing active-edge count per unit;
- weight and delay distributions;
- route continuation trace from each cue;
- first generated unit and complete generated chain;
- route retention fraction;
- branch coverage and branch collapse;
- cross-route contamination;
- disjoint-control retention;
- reversal and reacquisition lag;
- queue maximum, spike count, halt reason, and safety-budget status;
- connection-state hash before and after each phase;
- external observation count;
- ignored endogenous plasticity count;
- wall-clock and persistent-state size.

## Required interventions

- reset all learned connection weights/delays;
- transplant only learned weights;
- transplant only learned delays;
- remove one target edge;
- remove a matched disjoint edge;
- reverse training order;
- permute probe order;
- repeat with identical seed and compare hashes;
- disable plasticity after each phase and probe retention;
- stress endogenous-only activity and verify no connection write.

## Primary negative outcomes

The following are valid and must be preserved:

1. disjoint routes survive but overlapping routes catastrophically overwrite one another;
2. only the most recent or most frequent branch survives;
3. dense load causes order-dependent edge eviction;
4. reversal changes unrelated routes;
5. a simple recurrent/reservoir comparator matches or exceeds the physical Field under equal state
   and event budgets;
6. exact route behaviour is recoverable from an explicit edge table with no additional dynamic
   contribution;
7. safety limits terminate useful continuation before the configured capacity is reached.

## Interpretation boundary

Possible outcomes include:

```text
low interference only for disjoint routes
    -> localized edge-memory result

stable shared-prefix and branch distributions under overlap
    -> stronger recurrent-dynamics candidate

order-dependent collapse under dense load
    -> capacity-limited edge table interpretation

physical Field and reservoir remain equivalent
    -> no architectural uniqueness

Field-specific graded competition or graceful degradation
    -> candidate advantage requiring held-out confirmation
```

No development outcome establishes architectural uniqueness.

## Freeze boundary

Before held-out capability execution, freeze:

- this protocol;
- all 50 held-out world specifications and their grid hash;
- plasticity configuration;
- Field and safety budgets;
- evaluator metrics and thresholds;
- development and held-out seed lists;
- comparator configuration and resource budget;
- result and resource schemas;
- full Git SHA.

After opening held-out results, any correction requires a new protocol version and a new held-out seed
set.

## Immediate implementation order

```text
R01-12A  deterministic world contract and shape tests
R01-12B  development runner over 15 worlds
R01-12C  reset/transplant/order/intervention controls
R01-12D  resource-matched reservoir comparison
R01-12E  review and freeze held-out execution contract
```

R01-12A does not execute held-out capability and makes no positive claim.
