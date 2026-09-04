# SparkBrain v0.6 Held-Out World Contract

## Status

This document defines the **shape** of the five-family held-out world grid before any Primary or
comparator capability outcome is used for tuning.

```text
world families: 5
seeds:          10  (100 through 109)
world specs:    50
conditions:      8
real evidence domains: 9
future frozen result records: 3,600
```

Implementation:

```text
src/sparkbrain/evaluation/v06_confirmatory_heldout_spec.py
```

The module generates pure deterministic data. It does not run the Primary, G3, G4, G5, or any null
control and therefore does not reveal a confirmatory pass/fail outcome.

## Shared-condition rule

Every condition must consume the same `HeldoutWorldParameters` value for a given `(family, seed)`.
No adapter may silently replace a world with an easier condition-specific variant.

Allowed condition-specific differences are limited to the preregistered architectural intervention:

- Primary G0/G1/G2 route;
- no endogenous generation;
- matched random endogenous events;
- readout-only;
- shuffled anonymous relation state;
- G3 generic recurrent/transition predictor;
- G4 explicit Assembly-conditioned comparator;
- G5 typed functional-head comparator.

All world identities, raw event schedules, branch alternatives, thresholds, lag profiles, boundary
ports, external targets, contingency cycles, and perturbation seeds remain shared.

## Family 1 — heldout-sparse-permutation

Purpose:

- test non-contiguous anonymous identity and sparse active support;
- prevent reliance on compact consecutive unit numbering;
- retain inactive and distractor units outside the task paths;
- permute outbound-port identities.

Contract:

- 64 possible units;
- less than half active;
- disjoint active and distractor sets;
- permuted main, alternate, control, and third-branch paths;
- external relation targets outside all chain paths.

This family does not by itself prove topological Field superiority. It prevents a narrow fixed-ID
implementation from qualifying as held-out generalization.

## Family 2 — heldout-lag-dispersion

Purpose:

- replace one exact transition delay with multiple nonuniform edge-lag profiles;
- vary episode spacing independently;
- test whether an architecture relies on a single memorized clock interval.

Contract:

- at least six distinct training lag profiles;
- three nonuniform evaluation edge lags;
- nonuniform episode spacing;
- all timing remains causal and positive;
- the later external boundary delay remains independently varied.

Adapters may learn from the supplied training profiles but may not receive the evaluator's expected
future event time.

## Family 3 — heldout-threshold-band

Purpose:

- test ordinary Field threshold and input-magnitude regimes outside the three development settings;
- preserve the requirement that Primary endogenous events pass normal Field integration;
- make threshold bypass explicit for external comparators.

Contract:

- ten distinct thresholds spanning below 0.40 to above 0.65;
- cue magnitude always exceeds the corresponding ordinary threshold;
- relation re-entry gain is derived from the same frozen `threshold / 0.60` rule;
- every comparator reports whether it bypasses Field thresholding.

## Family 4 — heldout-branch-competition

Purpose:

- distinguish a real simultaneous-alternative problem from deterministic four-node lookup;
- make comparator success scientifically informative;
- test intervention selectivity when multiple branches share one current cue.

Contract:

- at least three competing paths share the same root cue;
- each branch has positive exposure;
- exposure counts are close rather than trivially separated;
- the strongest and runner-up branches differ by one exposure;
- the weakest differs from the strongest by two exposures;
- no evaluator-selected winner enters runtime;
- all branches and their raw outcomes remain recorded.

A held-out adapter that discards alternatives before runtime execution fails this contract even when
its final target happens to match the most exposed branch.

## Family 5 — heldout-contingency-cycles

Purpose:

- test more than one reversal and reacquisition;
- distinguish retained relation history from one-time replacement;
- detect uncontrolled relation proliferation and catastrophic overwrite.

Contract:

```text
old -> new -> old -> third -> new -> old
```

- six phases;
- five contingency changes;
- phase lengths vary deterministically between two and four episodes;
- internal chain and outbound-port identity remain fixed;
- only raw external target mapping changes;
- no scalar reward or correct-action target is supplied.

## Structural fields only

The held-out specification contains:

- anonymous unit and port identities;
- main, alternate, control, and competition paths;
- active and distractor supports;
- lag profiles and episode spacing;
- threshold, magnitude, and category-free re-entry gain;
- raw external target identities;
- branch exposure counts;
- contingency targets and phase lengths.

It contains no:

```text
Assembly ID
correct action
reward value
utility target
outcome label
functional role
meaning state
relation type
```

G4 and G5 may construct their privileged comparator state inside isolated baseline adapters. That
privileged information must be reported as comparator-specific and must not alter the shared world
specification.

## Freeze and execution order

1. generate and validate all 50 pure world specifications;
2. review family definitions, resource accounting, and branch-competition semantics;
3. implement all eight adapters against this exact data contract;
4. test adapter shape, deterministic replay, record coverage, and condition isolation without
   changing the world specification from capability outcomes;
5. freeze the full Git SHA, world-grid hash, manifest hash, thresholds, exclusions, and artifact
   schema;
6. execute one fresh 3,600-record held-out matrix;
7. preserve every Primary failure and comparator success without post-hoc world or threshold edits.

Qualification results cannot be relabelled as held-out evidence.

## Current non-claim

Defining these 50 worlds does not establish that any architecture passes them. The Primary and all
comparators remain `adapter_ready = false` for the confirmatory phase until implementation, review,
and one-way freeze are complete.
