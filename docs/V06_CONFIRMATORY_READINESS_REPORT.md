# SparkBrain v0.6 Confirmatory Readiness Report

## Current decision

```text
qualification execution-ready: false
confirmatory execution-ready:  false
PR #10 merge-ready for v0.6 release: false
```

This is an intentional fail-closed result, not a test failure.

## Completed before confirmatory work

The remaining programme order has been revised and implemented through:

```text
V06-12  relation re-entry into later normal-rule Field Dynamics
V06-13  direct persistence-locus reset/transplant
V06-14  supporting validity assays
```

Current findings include:

- a closed single-world relation-reentry engineering candidate;
- an explicit-state-dominant persistence-locus result;
- supporting forward, prefix, branching, omission, and origin-control assays.

These results are not imported into a confirmatory result matrix. V06-15 requires fresh executions
after freeze.

## Confirmatory software contract

`src/sparkbrain/evaluation/v06_confirmatory.py` now defines:

- qualification and confirmatory phases;
- required world-family and seed counts;
- all Primary/control/comparator conditions;
- required evidence domains;
- frozen thresholds and exclusions;
- immutable manifest hashing;
- full family × seed × condition × evidence coverage checks;
- duplicate, missing, and unexpected result rejection;
- Primary/comparator interpretation rules;
- explicit comparator-only negative interpretation;
- full Git-SHA freeze requirement.

## World and seed shape

### Qualification

```text
3 development world families × 3 perturbation seeds
```

The draft includes:

- identifier permutation;
- temporal perturbation;
- Field threshold/magnitude perturbation.

### Confirmatory

```text
5 held-out world families × 10 perturbation seeds
```

The draft includes held-out:

- sparse identity/topology permutation;
- lag dispersion;
- threshold/magnitude bands;
- branch competition;
- contingency cycles.

## Required condition matrix

All eight conditions must be present for every required evidence domain:

1. Primary G0/G1/G2 route;
2. no-endogenous generation;
3. count/energy/time-matched random endogenous events;
4. readout-only without Field reinjection;
5. shuffled anonymous relation state;
6. G3 generic recurrent comparator;
7. G4 explicit Assembly-conditioned comparator;
8. G5 typed functional-head comparator.

Qualification requires:

```text
3 × 3 × 8 × 9 = 648 records
```

Confirmatory requires:

```text
5 × 10 × 8 × 9 = 3,600 records
```

A missing, duplicate, or unexpected record blocks scoring.

## Current blockers

### Code freeze

The draft manifest uses:

```text
code_ref = UNFROZEN
```

A full lowercase 40-character Git SHA is required after all adapters and schemas are reviewed.

### Parameterized Primary adapter

Canonical engineering probes exist, but no single frozen adapter yet runs every evidence domain over
an arbitrary world-family/seed specification.

### Unified control adapters

The repository contains engineering no-history, no-reinjection, no-reentry, reset, and readout-only
controls. They are not yet normalized to the V06-15 result interface.

The following controls are still absent as complete adapters:

- count/energy/time-matched random endogenous events;
- shuffled anonymous relation state.

### G3 comparator

Generic neural/recurrent building blocks exist under `sparkbrain.baselines.neural`, but no frozen G3
adapter currently consumes the V06-15 world specification and emits the shared evidence-result
schema.

### G4 comparator

The v0.5 codebase contains explicit Assembly machinery, but no isolated G4 adapter currently maps it
to the same world, resource, intervention, and result interface.

### G5 comparator

A typed prediction/action/memory/reward-head comparator has not yet been implemented. It must remain
under `sparkbrain.baselines` and outside the Primary dependency graph.

## Frozen draft thresholds

```text
minimum overall success fraction:       0.80
minimum each-family success fraction:   0.70
maximum null false-positive fraction:   0.10
minimum targeted-minus-control effect:  0.50
required taxonomy hash match fraction:  1.00
maximum self-confirmation violations:   0
```

Changing a threshold, exclusion, family, seed set, or adapter after freeze changes the manifest hash
and requires a new preregistration.

## Interpretation is fail-closed

- Primary passes, comparators fail: Primary supported under frozen scope.
- Primary and comparators pass: Primary supported, architectural uniqueness not established.
- Primary fails, comparator passes: comparator-only success, negative for Primary hypothesis.
- all fail: tested capability unsupported.

No comparator result can be re-labelled as Primary success.

## Persistence limitation carried into V06-15

The initial reset/transplant suite indicates that the demonstrated experience effects follow explicit
anonymous G1 local-transition state and boundary-consistency state. Matched Field state alone did not
transfer the learned response.

V06-15 therefore evaluates the existing explicit-state-dominant architecture. It must not add a new
persistent state merely to rescue a distributed-Field claim after seeing qualification results.

## Next implementation work

1. define the normalized world-family and result adapter protocol;
2. implement Primary, no-endogenous, readout-only, random-matched, and shuffled-relation adapters;
3. implement isolated G3/G4/G5 adapters;
4. run and review the 3 × 3 qualification matrix;
5. freeze code SHA, manifest hash, thresholds, exclusions, and artifact schema;
6. execute the fresh 5 × 10 held-out matrix;
7. preserve all negative results and comparator interpretations;
8. proceed to V06-16 only after the matrix is complete.

## Release boundary

`main` must remain unchanged and PR #10 must remain Draft while either readiness report is false.
