# SparkBrain v0.6 Primary Qualification Report

## Status

```text
phase: qualification
condition: Primary G0/G1/G2 route only
world families: 3
perturbation seeds per family: 3
world executions: 9
evidence domains per world: 9
Primary evidence records: 81
passed worlds: 9
passed Primary evidence records: 81
confirmatory claim: not permitted
```

This qualification result validates the parameterized Primary adapter and the engineering artifact
path. It is not a confirmatory result because the seven required control/comparator conditions have
not yet been connected to the frozen matrix.

## Purpose

Earlier v0.6 evidence came from canonical single-world constructions. The first qualification grid
asks whether the Primary mechanism survives real structural changes rather than merely reproducing a
single set of unit IDs, lags, and thresholds.

The grid reruns all required evidence domains:

1. endogenous origin;
2. same-input persistent-state dependence;
3. autonomous endogenous chain;
4. selective anonymous boundary effect;
5. external anonymous relation stabilization;
6. reversal and reacquisition;
7. relation re-entry into later Field Dynamics;
8. persistence-locus reset/transplant;
9. observer/taxonomy non-interference.

## World families

### 1. Identifier permutation

Each seed deterministically permutes the anonymous roles used for:

- main chain;
- alternate-history chain;
- disjoint active control chain;
- old and new raw external targets;
- main and control outbound ports.

The three seeds therefore do not share the same main unit path or main port identity.

### 2. Temporal perturbation

The local and boundary timing is changed structurally:

```text
seed 0: local transition lag 4 ms; boundary lag 8 ms
seed 1: local transition lag 5 ms; boundary lag 10 ms
seed 2: local transition lag 6 ms; boundary lag 12 ms
```

Episode spacing and proposal lifetimes are derived from these timing parameters rather than held at
the canonical constants.

### 3. Field-gain perturbation

The ordinary Field threshold changes:

```text
seed 0: threshold 0.44
seed 1: threshold 0.50
seed 2: threshold 0.56
```

External cue magnitude and the category-free relation-reentry gain are adjusted from the structural
world parameters. The relation-reentry boundary is constrained so that:

```text
reliability 0.50 remains sub-threshold
reliability 7/11 crosses threshold
reliability 0.80 crosses threshold
```

This preserves the intended acquisition/reversal/reacquisition test without an evaluator selecting a
winning target.

## Result

All nine parameterized Primary worlds passed all nine required evidence domains.

```text
identifier-permutation: 3 / 3 worlds passed
 temporal-perturbation: 3 / 3 worlds passed
 field-gain-perturbation: 3 / 3 worlds passed

world total:             9 / 9
evidence records:       81 / 81
```

The test suite also requires deterministic full-grid replay.

## Preserved causal controls

Every world retains:

- no-history no-generation control;
- actual normally thresholded Field Sparks;
- targeted root/expansion intervention;
- active stage-matched disjoint-chain intervention;
- targeted outbound-port suppression;
- active disjoint-port suppression;
- internal-only boundary exposure;
- external stabilization only after raw external return;
- world contingency reversal and reacquisition;
- relation re-entry through ordinary Field rules;
- local-transition reset/transplant;
- consistency reset/transplant;
- taxonomy-view runtime equality;
- zero positive self-confirmation during internal recurrence.

## Persistence limitation preserved

Qualification does not weaken the V06-13 result.

Across all nine worlds:

```text
learned local-transition state transplant -> one target Field response
local-transition reset                    -> no target Field response
```

The qualification metric therefore preserves the explicit-state-dominant persistence finding. It
does not reinterpret successful structural perturbation as distributed Field memory.

## What this does support

The qualification result supports:

> The reviewed Primary adapter can reproduce the current Level-1/Level-2/Level-3 engineering evidence
> shape across three structural world families and three deterministic perturbation seeds while
> preserving the explicit-state persistence limitation and taxonomy-free runtime boundary.

## What this does not support

It does not establish:

- confirmatory multi-world evidence;
- false-positive rates against all required null conditions;
- superiority over matched random or shuffled-relation controls;
- comparison with G3/G4/G5;
- held-out world-family generalization;
- distributed Field memory;
- semantic meaning, concepts, value formation, organs, consciousness, or AGI.

## CI

GitHub Actions run `33261058633` passed on Python 3.11 and Python 3.13 for commit
`47263d4f110fc7ff0aabbc7556dd2fc19c34d77d`.

Both jobs passed:

```text
Install
Ruff lint
Local readiness
Default test suite
Bundle validation
```

## Readiness effect

The parameterized Primary adapter is now marked ready in the current manifest builder:

```text
sparkbrain.evaluation.v06_confirmatory_primary_adapter.run_condition
```

Qualification and confirmatory readiness remain false until the remaining seven adapters and the
full code/manifest freeze are complete.
