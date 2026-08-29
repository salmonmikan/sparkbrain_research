# SparkBrain v0.6 Held-Out Adapter Preflight Report

## Status

The held-out adapter layer is implemented for all eight confirmatory conditions and has passed a
shape, resource-contract, deterministic-replay, repository-lint, full-test, and bundle preflight.

This report does **not** disclose or aggregate held-out capability pass rates. The purpose of the
preflight is to establish that the frozen execution layer can consume the held-out world contract
without missing records, hidden condition-specific specifications, non-finite metrics, or invalid
resource declarations.

## Implemented condition adapters

```text
Primary
no-endogenous
random-matched
readout-only
shuffled-relation
G3 generic recurrent comparator
G4 explicit Assembly comparator
G5 typed prediction/boundary/memory/reward comparator
```

Every adapter consumes the same immutable `HeldoutWorldParameters` object for a given family and
seed and emits:

- one `HeldoutConditionExecution`;
- all nine `EvidenceDomain` records;
- one `ConditionResourceRecord`;
- the held-out world specification hash;
- a semantic replay hash that excludes wall-clock time.

## Held-out axes consumed by the Primary adapter

The Primary adapter obtains the following only from the held-out world specification:

- sparse active-unit identity and distractor topology;
- main, alternate, control, and competing paths;
- competing-path exposure counts;
- training lag profiles and evaluation lags;
- threshold and cue-magnitude band;
- anonymous relation-reentry gain;
- anonymous outbound port identities;
- old, new, and third raw external targets;
- contingency-cycle targets and phase lengths;
- boundary lag and episode spacing.

No family-specific success patch or held-out answer table is present in the adapter.

## Control contracts

### No endogenous

All local transition learning may remain present, but reinjection at every generation depth is
suppressed. The control must produce no endogenous Field Spark and no positive internal-only commit.

### Random matched

The random condition copies the Primary proposal schedule's:

- event count;
- scheduled time;
- effective current;
- total energy;
- generation depth.

It replaces causal local targets with deterministic non-main targets derived from family ID and seed.
It does not construct a sequential causal parent chain.

### Readout only

The local temporal model may emit proposal data, but no proposal is reinjected into the Field. The
control therefore distinguishes a prediction object from an actual normally thresholded Field Spark.

### Shuffled relation

The early endogenous chain is retained, while learned anonymous external targets are cyclically
rotated among the held-out old/new/third targets before relation re-entry. This tests whether the
specific learned relation, rather than merely the existence of relation state, causes the later
Field response.

## Comparator disclosure

Resource records explicitly distinguish architectural privileges.

- G3 declares no privileged information, but bypasses the normal excitable Field threshold.
- G4 declares explicit Assembly state and reports the number of Assembly entries.
- G5 declares typed prediction, boundary, and memory heads plus scalar reward observations.

Comparator success cannot be silently counted as evidence that the Primary Assembly-free,
taxonomy-free mechanism was responsible.

## Preflight execution

The first complete adapter preflight used:

```text
held-out families: 5
seeds:              seed 100 only
conditions:         8
executions:         40
result records:     360
resource records:   40
capability aggregation: disabled
```

The preflight verified:

- every family/condition execution was present exactly once;
- every execution emitted all nine evidence domains;
- every execution emitted one valid resource record;
- all conditions for one family referenced the same specification hash;
- metrics were finite;
- comparator privileges were declared;
- representative semantic replay hashes were deterministic;
- no execution-shape capability score was aggregated.

## Validation

The exact downloaded branch state used for the adapter preflight passed:

```text
python -m compileall -q src tests
python -m ruff check <held-out adapter files and tests>
python -m pytest -q tests/v06/test_confirmatory_heldout_adapters.py
python -m ruff check .
python -m pytest -q
python scripts/validate_release_bundle.py
```

The full five-family, eight-condition, seed-100 matrix also completed with a complete preflight
report.

## Remaining freeze boundary

Before the 5-family × 10-seed × 8-condition confirmatory matrix is interpreted:

1. create an immutable confirmatory freeze branch from this preflight state;
2. record the frozen branch and world-contract identities;
3. run the fresh 400 executions and emit 3,600 result records plus 400 resource records;
4. do not modify thresholds, family specifications, adapters, or scoring rules after inspecting the
   confirmatory result;
5. aggregate only with the already frozen confirmatory scorer;
6. retain negative and comparator results as first-class artifacts.

Infrastructure-only invalidation must be documented explicitly and must not be used to tune a
scientific outcome.

## Scientific boundary

Passing this preflight establishes only that the confirmatory execution layer is structurally ready.
It does not establish that the Primary passes held-out Level 1, Level 2, or Level 3 criteria, that it
outperforms G3/G4/G5, or that the current explicit local-transition and consistency memories are
sufficiently Field-embedded.
