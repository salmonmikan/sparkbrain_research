# SparkBrain v0.6 Taxonomy-Boundary Engineering Report

## Scope

Protocol Amendment 002 extends the observer-only boundary from explicit Assembly state to human
functional categories. This report records the initial fail-closed implementation guard. It does not
establish autonomous causal function or a scientific Level-2/Level-3 result.

## Core distinction

The Primary runtime is category-free, not structure-free.

It may represent:

- anonymous unit, channel, region, and outbound-port identity;
- event time, magnitude, polarity, and provenance;
- causal parent and local path identity;
- persistent, transition, eligibility, and external-consistency state;
- bounded generation resources.

It must not represent observer categories as cognitive object types, including:

- PredictionRelation;
- ActionRelation;
- MemoryRelation;
- RewardRelation;
- FunctionalRole;
- MeaningState;
- scalar reward, correct action, utility target, or semantic label.

Structural fields such as `predicted_arrival_ms` and `prediction_error` remain allowed. They specify
a scheduled time or mismatch quantity; they do not classify a relation as predictive.

## Runtime guard

`src/sparkbrain/v06/taxonomy.py` adds canonical functional field and class-name sets. The package
initializer installs those fields into the recursive v0.6 runtime-mapping validator before exposing
the Primary modules.

Normal imports of either `sparkbrain.v06` or `sparkbrain.v06.foundation` execute the package
initializer first, so the guard applies to runtime pulses, nested runtime state, and checkpoints
constructed through the package.

The guard rejects canonical fields such as:

```text
prediction_relation
action_relation
memory_relation
reward_relation
relation_type
functional_role
action_bias
reward
reward_value
utility_target
meaning
semantic_state
```

## Source-tree audit

The engineering audit parses executable AST identifiers in `src/sparkbrain/v06/*.py` and reports
forbidden functional class declarations or annotated/assigned runtime fields. Prose and comments do
not count as runtime ontology. `taxonomy.py` itself is excluded because it necessarily names the
forbidden categories it audits.

This exact-name audit is one layer, not proof that no disguised semantic substitute can ever be
introduced. Review, dependency tests, schema audits, taxonomy permutation, and comparator isolation
remain required.

## Taxonomy-variant equality

`verify_taxonomy_variant_runtime_equality(...)` compares runtime mappings produced under differently
named evaluator views. Variant names are ignored; every runtime value is recursively validated and
must be identical.

This is the initial code contract for future tests in which:

- `predictive-view` is renamed;
- outbound-port descriptions are permuted;
- observer/evaluator packages are removed;
- typed G5 comparators are absent.

The complete Field/queue/RNG/checkpoint equality experiment remains future V06-11/V06-14 work.

## Focused tests

`tests/v06/test_taxonomy_boundary.py` covers:

- installation of Amendment-002 fields into the foundation guard;
- rejection of typed relation fields in pulse metadata;
- rejection of nested `relation_type` state;
- continued acceptance of structural timing, mismatch, consistency, and anonymous port fields;
- equality under evaluator-view renaming;
- failure when a taxonomy variant changes runtime state;
- source-tree absence of forbidden typed functional objects.

## CI

The first run, `33251498240`, stopped at Ruff because one test import block was unsorted. No runtime
or test failure was reached. The import was corrected without weakening the checks.

GitHub Actions run `33251603653` then passed on Python 3.11 and Python 3.13. Each job completed:

```text
Install: PASS
Lint: PASS
Local readiness: PASS
Test: PASS
Bundle validation: PASS
```

## Claim boundary

This slice supports only that the current v0.6 Primary package rejects a defined canonical set of
predeclared functional relation fields, contains no audited typed functional class in its source
tree, and can require identical runtime mappings across evaluator taxonomy names.

It does not yet establish:

- full semantic-ontology absence against every possible alias;
- runtime equality with the entire evaluator package physically removed;
- autonomous endogenous causal chains;
- anonymous outbound-boundary coupling;
- externally stabilized relations;
- a functional meaning candidate;
- Level-2 or Level-3 scientific evidence.
