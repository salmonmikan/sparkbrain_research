# SparkBrain v0.6 Strict Confirmatory Scoring Report

## Scope

The initial confirmatory contract defined all required thresholds, but the legacy aggregate scorer
mainly evaluated Primary and comparator success fractions. V06-15 now has a separate strict scorer
that enforces the control, causal-selectivity, taxonomy, and self-confirmation thresholds before a
Primary result can be supported.

Implementation:

```text
src/sparkbrain/evaluation/v06_confirmatory_scoring.py
tests/v06/test_confirmatory_strict_scoring.py
```

This is an engineering scoring contract. It does not score an actual frozen held-out run yet.

## Fail-closed entry requirements

Strict scoring refuses to run unless:

1. the manifest is execution-ready;
2. `code_ref` is a frozen lowercase 40-character Git SHA;
3. every family × seed × condition × evidence record exists exactly once;
4. every family × seed × condition group has identical metric metadata across its nine domain
   records;
5. every condition supplies its required finite metrics.

A missing or inconsistent metric blocks scoring rather than being interpreted as zero.

## Required metric contract

### Primary

Each Primary world must provide:

```text
chain_targeted_impairment
chain_matched_impairment
boundary_targeted_impairment
boundary_matched_impairment
taxonomy_hash_match
self_confirmation_violations
```

### Non-comparator controls

Each control world must provide:

```text
control_contract_passed
taxonomy_hash_match
self_confirmation_violations
```

### G3/G4/G5 comparators

Each comparator world must provide at minimum:

```text
taxonomy_hash_match
self_confirmation_violations
```

Comparator-specific resource and architecture metrics remain additional requirements before freeze.

## Enforced gates

### Primary raw success

```text
overall Primary evidence success >= 0.80
minimum per-family Primary success >= 0.70
```

This is necessary but no longer sufficient.

### Null false-positive gate

The false-positive fraction includes:

- every capability domain except taxonomy for no-endogenous;
- every capability domain except taxonomy for matched-random endogenous events;
- every capability domain except taxonomy for readout-only;
- relation re-entry and persistence-locus domains for shuffled relation state.

```text
maximum null false-positive fraction <= 0.10
```

### Causal selectivity gate

For every Primary world, the scorer computes:

```text
chain selective effect
  = targeted chain impairment - matched-random chain impairment

boundary selective effect
  = targeted boundary impairment - matched-random boundary impairment
```

The minimum value across every world and both effect types must satisfy:

```text
minimum selective effect >= 0.50
```

A high average cannot hide one world with no selective effect.

### Taxonomy non-interference gate

Every Primary, control, and comparator world must provide a matching normalized runtime hash under
the required taxonomy/observer variants.

```text
required taxonomy hash match fraction = 1.00
```

One mismatch fails the gate.

### Self-confirmation gate

The scorer sums one de-duplicated violation count per family × seed × condition group.

```text
maximum self-confirmation violations = 0
```

One violation anywhere in the complete matrix fails the gate.

### Control-contract gate

Every non-comparator control must report that its engineering matching/suppression contract was
actually satisfied.

```text
control contract fraction = 1.00
```

For example, a random control that did not really match count, time, current, and energy cannot be
used to support the Primary result even if its capability flags are false.

## Interpretation

The strict scorer distinguishes:

- `primary_raw_supported`: Primary success fractions pass;
- `control_and_safety_gates_passed`: all null/selectivity/taxonomy/self-confirmation/control gates
  pass;
- `primary_supported`: both of the above pass;
- supported comparators;
- comparator-only success.

A raw Primary success is explicitly rejected when any safety/control gate fails.

Comparator-only success remains a negative result for the Primary SparkBrain hypothesis.

## Adversarial tests

The focused suite verifies that Primary support is rejected by:

- excessive no-endogenous false positives;
- a selective effect below 0.50;
- one taxonomy-hash mismatch;
- one self-confirmation violation;
- one failed control contract;
- one missing required metric;
- inconsistent metric metadata within one world/condition;
- incomplete matrix coverage.

It also verifies that a clean complete matrix passes and that comparator-only success remains
negative for the Primary hypothesis.

## Validation

GitHub Actions run `33267401237` passed on Python 3.11 and Python 3.13:

```text
Install: PASS
Ruff lint: PASS
Local readiness: PASS
Default test suite: PASS
Bundle validation: PASS
```

## Remaining boundary

Strict scoring is ready as a contract, but confirmatory execution remains blocked because G3, G4,
and G5 adapters have not yet passed the shared 3 × 3 qualification interface and no code/manifest
freeze has occurred.

The existing legacy aggregate scorer remains available for historical contract tests. The frozen
V06-15 execution must use `score_strict_confirmatory_results(...)`.
