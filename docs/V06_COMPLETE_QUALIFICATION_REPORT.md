# SparkBrain v0.6 Complete Qualification Matrix Report

## Decision

```text
world families:                         3
seeds per family:                       3
conditions:                             8
evidence domains:                       9
complete result records:              648 / 648
strict metric coverage:                PASS
null/control/safety gates:             PASS
Primary qualification:                 PASS
G3 recurrent qualification:            PASS
G4 explicit Assembly qualification:    PASS
G5 typed functional-head qualification: PASS
architectural uniqueness established:  NO
held-out confirmatory execution:       NOT RUN
```

This is a development qualification result. It is not the frozen 5 × 10 held-out confirmatory suite
and does not upgrade the current engineering candidates into confirmatory Level 1, 2, or 3 support.

## Matrix

```text
3 development families × 3 seeds × 8 conditions × 9 evidence domains
= 648 unique records
```

Every condition emits exactly one record for every family, seed, and evidence-domain combination.
Missing, duplicate, or unexpected records fail closed.

Conditions:

1. Primary G0/G1/G2 Field route;
2. no-endogenous generation;
3. count/time/current/energy-matched random endogenous events;
4. readout-only without Field reinjection;
5. shuffled anonymous relation state;
6. G3 generic recurrent/transition comparator;
7. G4 explicit Assembly-conditioned comparator;
8. G5 typed prediction/action/reward/memory-head comparator.

## Strict scoring result

The complete matrix passes the engineering scoring contract:

```text
Primary overall success fraction:        1.00
Primary minimum family fraction:         1.00
null false-positive fraction:            0.00
minimum targeted-minus-matched effect:   1.00
taxonomy hash match fraction:            1.00
self-confirmation violations:               0
control contract fraction:               1.00
```

A Primary result cannot be supported merely because its evidence flags are high. The strict scorer
also requires every null, selective-intervention, taxonomy, self-confirmation, and control-matching
gate to pass.

## Primary result

The parameterized Primary route passed all nine evidence domains in every development world:

```text
9 / 9 worlds
81 / 81 records
```

The Primary result includes:

- non-copy endogenous Field activity;
- same-input/different-history response;
- sequential endogenous chain;
- selective anonymous boundary effect;
- external relation stabilization;
- reversal and reacquisition;
- relation re-entry into later normal-rule Field Dynamics;
- persistence-locus transfer/reset result;
- taxonomy non-interference.

The persistence result remains limiting: the tested experience effects follow explicit anonymous
local-transition and boundary-consistency states rather than matched Field state alone.

## Control result

The four required controls produced the preregistered positive and negative patterns in all 36
control worlds and all 324 control records.

- no-endogenous and readout-only do not produce later endogenous Field capability;
- matched random events receive the same event count, schedule, current, energy, and depth profile but
  lack the learned sequential lineage;
- shuffled relation state preserves early Dynamics while redirecting relation re-entry and removing
  the correct persistence transfer;
- all control engineering contracts pass;
- self-confirmation remains zero;
- taxonomy hash equality remains complete.

## G3 result — generic recurrent comparator

G3 passed:

```text
9 / 9 worlds
81 / 81 records
```

G3 is an isolated external autoregressive transition-score model. Generated tokens do not train it.
Its success demonstrates that the current development worlds do not require excitable Field
Dynamics: a much simpler explicit transition predictor can reproduce the tested evidence pattern.

This is evidence **against architectural uniqueness**, not evidence against the Primary capability
itself.

## G4 result — explicit Assembly comparator

G4 passed:

```text
9 / 9 worlds
81 / 81 records
```

G4 explicitly stores named Assembly prototypes and uses Assembly IDs to drive rollout, boundary
state, external relation state, reset, and transplant. It is isolated under `sparkbrain.baselines` and
is forbidden from the Primary import graph.

Its success shows that explicit Assembly state can also solve the development worlds. The current
qualification therefore does not establish that the observer-only Assembly choice is necessary for
performance.

## G5 result — typed functional-head comparator

G5 passed:

```text
9 / 9 worlds
81 / 81 records
```

G5 intentionally uses:

```text
prediction_head
action_head
reward_head
memory_head
privileged scalar reward
```

These structures are prohibited in the Primary runtime but valid in the isolated comparator. G5
success shows that a human-designed functional decomposition can reproduce the development evidence.
It does not count as SparkBrain support.

## Interpretation

The strict scorer returns the development interpretation:

> Primary and at least one comparator are supported; architectural uniqueness is not established.

In fact all three comparators are supported in the current qualification grid.

Therefore the strongest correct interpretation is:

> The present development worlds verify that the Primary implementation can execute the proposed
> closed-loop endogenous capability under its engineering contracts. They do not show that this
> capability specifically requires the SparkBrain architecture, because a generic transition
> predictor, explicit Assembly system, and typed functional-head system also solve the same worlds.

## Why this is still useful

The qualification suite has now exposed the real burden for held-out science. New worlds must not
merely repeat deterministic four-node transition lookup. They must discriminate among:

- event-driven Field Dynamics;
- generic autoregressive transition prediction;
- explicit Assembly-conditioned sequence memory;
- typed human functional heads.

The held-out families must therefore include perturbations where architecture matters, especially:

- sparse/topological variation;
- lag dispersion rather than one exact delay;
- threshold/magnitude bands;
- genuine branch competition;
- repeated contingency cycles;
- causal interventions whose effects cannot be satisfied by replaying an explicit stored chain.

## Validation

The first integrated run detected that the comparator world specification used a different relation
re-entry gain from the Primary. The test correctly rejected all nine G3 world-spec equality checks.
The comparator specification was changed to the exact Primary normalization rather than weakening
the test.

The corrected complete matrix passed GitHub Actions run `33268619204` on Python 3.11 and Python 3.13:

```text
Install: PASS
Ruff lint: PASS
Local readiness: PASS
Default test suite: PASS
Bundle validation: PASS
```

## Remaining blockers

The qualification adapters and strict scorer are complete, but execution remains intentionally
unfrozen.

Before the confirmatory run:

1. implement the five held-out world families for all eight adapters;
2. demonstrate held-out adapter qualification without using confirmatory outcomes to tune thresholds;
3. review branch-competition and comparator-fairness contracts;
4. freeze the full Git SHA, manifest hash, thresholds, exclusions, and artifact schema;
5. execute a fresh `5 × 10 × 8 × 9 = 3,600` record matrix;
6. preserve comparator success, Primary failure, and all negative outcomes without post-hoc rescue.

`main` remains unchanged and PR #10 remains Draft.
