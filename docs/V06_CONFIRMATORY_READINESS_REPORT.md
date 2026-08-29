# SparkBrain v0.6 Confirmatory Readiness Report

## Current decision

```text
qualification execution-ready: false
confirmatory execution-ready:  false
PR #10 merge-ready for v0.6 release: false
```

This is an intentional fail-closed result, not a failed Primary result.

## Programme order implemented before confirmatory work

The revised research order has been implemented through:

```text
V06-12  relation re-entry into later normal-rule Field Dynamics
V06-13  direct persistence-locus reset/transplant
V06-14  supporting validity assays
V06-15  Primary and four required control qualification adapters
```

Current engineering findings include:

- relation re-entry changes later normally thresholded Field Dynamics after acquisition, reversal,
  and reacquisition;
- demonstrated experience effects transfer with explicit anonymous G1 local-transition state and
  boundary-consistency state, not with matched Field state alone;
- forward missing-middle, prefix, branching, omission, and shortcut-control assays exist as supporting
  diagnostics;
- the parameterized Primary passes 9/9 development worlds and 81/81 evidence-domain records;
- four non-comparator controls satisfy their expected positive and negative patterns over 36/36
  development control worlds and 324/324 complete evidence records.

None of these are the frozen 5 × 10 held-out confirmatory execution.

## Confirmatory software contract

`src/sparkbrain/evaluation/v06_confirmatory.py` defines:

- qualification and confirmatory phases;
- required world-family and seed counts;
- all Primary/control/comparator conditions;
- nine required evidence domains;
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

Families:

- identifier permutation;
- temporal perturbation;
- Field threshold/magnitude perturbation.

### Confirmatory

```text
5 held-out world families × 10 perturbation seeds
```

Held-out family contracts:

- sparse identity/topology permutation;
- lag dispersion;
- threshold/magnitude bands;
- branch competition;
- contingency cycles.

## Required condition matrix

All eight conditions must emit one record for every required evidence domain:

1. Primary G0/G1/G2 route;
2. no-endogenous generation;
3. count/time/current/energy-matched random endogenous events;
4. readout-only without Field reinjection;
5. shuffled anonymous relation state;
6. G3 generic recurrent comparator;
7. G4 explicit Assembly-conditioned comparator;
8. G5 typed functional-head comparator.

Qualification requires:

```text
3 × 3 × 8 × 9 = 648 records
```

Current normalized qualification coverage:

```text
Primary:          9 worlds × 9 domains =  81 records
four controls:   36 worlds × 9 domains = 324 records
current total:                            405 records
missing G3–G5:   27 worlds × 9 domains = 243 records
```

Confirmatory requires:

```text
5 × 10 × 8 × 9 = 3,600 fresh records
```

A missing, duplicate, or unexpected record blocks scoring.

## Adapters currently accepted by the manifest

The current fail-closed manifest marks the following adapters ready:

- `sparkbrain.evaluation.v06_confirmatory_primary_adapter.run_condition`;
- `sparkbrain.evaluation.v06_confirmatory_controls.run_no_endogenous`;
- `sparkbrain.evaluation.v06_confirmatory_controls.run_random_matched`;
- `sparkbrain.evaluation.v06_confirmatory_controls.run_readout_only`;
- `sparkbrain.evaluation.v06_confirmatory_controls.run_shuffled_relation`.

Their shared interface emits all nine evidence-domain records, including explicit negative records.

## Primary qualification result

```text
worlds passed:          9 / 9
records passed:        81 / 81
deterministic replay:  PASS
```

This result spans identifier, timing, and Field-gain perturbations. It preserves rather than hides the
persistence limitation: local-transition transplant transfers the learned response; local-transition
reset removes it.

## Control qualification result

```text
control worlds contract-complete: 36 / 36
control result records present:   324 / 324
self-confirmation violations:       0
taxonomy hash mismatch:             0
```

Expected result pattern:

| Condition | Intended positive domains |
|---|---|
| no-endogenous | taxonomy non-interference only |
| random endogenous matched | taxonomy non-interference only |
| readout-only | taxonomy non-interference only |
| shuffled relation | early Primary domains plus taxonomy; relation re-entry and persistence must fail |

The random condition matches Primary reinjection count, scheduled time, effective current, total
energy, and generation-depth profile while removing learned sequential parentage.

## Current blockers

### 1. G3 generic recurrent comparator

Generic neural/recurrent building blocks exist under `sparkbrain.baselines.neural`, but no reviewed G3
adapter yet consumes the V06-15 world specification and emits the shared nine-domain result schema.

### 2. G4 explicit Assembly comparator

The v0.5 codebase contains explicit Assembly machinery, but no isolated G4 adapter yet maps it to the
same world, intervention, relation re-entry, persistence, and result interface.

### 3. G5 typed functional-head comparator

A typed prediction/action/memory/reward-head comparator has not yet been qualified. It must remain
under `sparkbrain.baselines` and outside the Primary dependency graph.

### 4. Threshold wiring review

The manifest preregisters:

```text
minimum overall success fraction:       0.80
minimum each-family success fraction:   0.70
maximum null false-positive fraction:   0.10
minimum targeted-minus-control effect:  0.50
required taxonomy hash match fraction:  1.00
maximum self-confirmation violations:   0
```

Before freeze, the final scoring path must be reviewed to ensure that null-control false positives,
selective-effect metrics, taxonomy equality, and self-confirmation counts are enforced rather than
merely stored in result metadata.

### 5. Code and manifest freeze

The current manifest still uses:

```text
code_ref = UNFROZEN
```

A full lowercase 40-character Git SHA is allowed only after all eight adapters, scoring rules,
schemas, and exclusions pass qualification review.

## Interpretation remains fail-closed

- Primary passes, comparators fail: Primary supported under frozen scope.
- Primary and comparators pass: Primary supported; architectural uniqueness is not established.
- Primary fails, comparator passes: comparator-only success; negative for the Primary hypothesis.
- all fail: tested capability unsupported.

No control or comparator result may be relabelled as Primary success.

## Persistence limitation carried into confirmatory work

The direct reset/transplant suite indicates that demonstrated experience effects follow explicit
anonymous G1 local-transition state and anonymous boundary-consistency state. Matched Field state
alone does not transfer them.

The current system is therefore best described as:

```text
Dynamic Field
+ explicit anonymous local-transition memory
+ explicit anonymous external-consistency memory
+ normal-rule reinjection and boundary coupling
```

Qualification and confirmatory work must test this architecture as it exists. It must not add a new
persistent state merely to rescue a distributed-Field interpretation after observing a negative
result.

## Next implementation work

1. enforce every frozen threshold in the scoring path;
2. implement and qualify isolated G3, G4, and G5 adapters;
3. complete and review the 648-record qualification matrix;
4. freeze code SHA, manifest hash, thresholds, exclusions, and artifact schema;
5. execute the fresh 5 × 10 × 8 × 9 held-out matrix;
6. preserve all negative results, strongest counterexamples, and comparator interpretations;
7. proceed to V06-16 only after the complete matrix and final taxonomy audit.

## Release boundary

`main` must remain unchanged and PR #10 must remain Draft while readiness is false.
