# SparkBrain v0.6 Anonymous Relation Revision Engineering Report

## Scope

V06-11 tests whether one anonymous outbound port can retain, weaken, replace, and later reacquire
structural consistency with different raw external targets when only the world contingency changes.

The Primary runtime remains Assembly-free and taxonomy-free. It receives no action name, correct
port, reward, utility, outcome class, functional role, or meaning value.

This is a **single-world Level-3 relation-state engineering candidate** under Protocol Amendment 002.
It is not a confirmatory Level-3 result because held-out worlds/seeds, broader intervention controls,
causal reuse of the revised relation state, and persistence-locus analysis remain outstanding.

## Experimental structure

The internal anonymous chain and outbound port remain fixed:

```text
unit:0 -> unit:1 -> unit:2 -> unit:3 -> port:7
```

Only the world-side physical mapping changes.

### Phase 1 — acquisition

```text
port:7 -> raw external unit:8
```

Three episodes.

### Phase 2 — reversal

```text
port:7 -> raw external unit:9
```

Three episodes. The port identity, internal chain, boundary coupling, event budgets, and relation
update rule remain unchanged.

### Phase 3 — return to the original contingency

```text
port:7 -> raw external unit:8
```

Three episodes.

### Stable control

```text
port:7 -> raw external unit:8
```

Nine episodes with no reversal.

## Anonymous update rule

The runtime stores only anonymous structural states keyed by:

```text
(port_id, external_target, polarity)
```

Each registered external pairing updates:

- consistent count;
- inconsistent count for other active target links on the same port;
- mean lag and lag variance;
- mean magnitude ratio;
- anonymous reliability;
- causal event references.

No functional relation type is stored.

## Engineering result

### Phase 1 — initial acquisition

```text
port:7 -> unit:8 consistent count:   3
port:7 -> unit:8 inconsistent count: 0
old-link reliability:                0.8
new-link state:                      absent
```

### Phase 2 — world reversal

```text
old unit:8 consistent count:   3
old unit:8 inconsistent count: 3
old-link reliability:          0.5

new unit:9 consistent count:   3
new unit:9 inconsistent count: 0
new-link reliability:          0.8
```

The new anonymous link first exceeds the old link after the second reversal episode.

### Phase 3 — original world rule returns

```text
old unit:8 consistent count:   6
old unit:8 inconsistent count: 3
old-link reliability:          7/11 ~= 0.6364

new unit:9 consistent count:   3
new unit:9 inconsistent count: 3
new-link reliability:          0.5
```

The original link first exceeds the reversal link again after the second return episode.

The old relation history is not erased during reversal. Its consistency count remains available and
is extended when the old world rule returns.

### Stable control

```text
link count:                        1
unit:8 consistent count:           9
unit:8 inconsistent count:         0
unit:8 reliability:                10/11 ~= 0.9091
unit:9 relation:                   absent
```

The stable world does not create an unnecessary second link or false revision.

## Self-confirmation boundary

Across acquisition, reversal, return, and stable control:

```text
positive G2 commits from internal recurrence: 0
```

The anonymous consistency state changes only after raw registered external events return from the
world adapter. Boundary recurrence alone cannot raise relation reliability.

## What has and has not been revised

### Revised

The externally gated anonymous structural relation state shifts from:

```text
port:7 -> unit:8
```

to:

```text
port:7 -> unit:9
```

and later shifts back when the external contingency returns.

### Not yet revised

The relation state is not yet used to alter the Field's future chain, select among competing ports,
or change the probability of a later boundary event. Therefore this slice demonstrates externally
driven relation-state revision, not adaptive use of revised relations.

## Runtime ontology inventory

The Primary state contains:

- anonymous unit, path, proposal, Spark, boundary, port, and external-event IDs;
- time, magnitude, polarity, lag, direction, and generation depth;
- causal parentage;
- pending exposure, consistency, inconsistency, expiry, and reliability counts;
- normal Field, transition, reinjection, and resource state.

It does not contain:

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

The evaluator reports:

- initial anonymous-link acquisition;
- reliability crossing after reversal;
- reliability crossing after return;
- stable-control proliferation;
- old-relation retention;
- self-confirmation count;
- taxonomy absence.

These descriptions do not enter the Primary runtime.

## Validation

```text
GitHub Actions run 33252757980
Python 3.11: PASS
Python 3.13: PASS
Install: PASS
Ruff lint: PASS
Local readiness: PASS
Default test suite: PASS
Bundle validation: PASS
```

The focused suite verifies:

- initial old-link acquisition;
- new-link dominance after world reversal;
- old-link reacquisition after rule return;
- old relation history retention;
- stable-world single-link behaviour;
- zero internal positive commits;
- taxonomy-free runtime state;
- deterministic replay.

## Claim boundary

The strongest permitted statement for this slice is:

> In a canonical taxonomy-free engineering world, an anonymous outbound port formed an externally
> gated structural relation with one raw external target, shifted reliability toward a different raw
> target after the world contingency changed, and shifted back when the original contingency
> returned. Stable controls did not create an unnecessary competing relation, and internal-only
> activity did not positively confirm the relation.

Together with V06-09 and V06-10, this satisfies the *shape* of a Level-3 externally stabilized and
revisable anonymous relation in one controlled engineering construction. It does not yet establish a
confirmatory Level-3 result, semantic meaning, value formation, adaptive port selection, generalized
world modelling, or human-like cognition.
