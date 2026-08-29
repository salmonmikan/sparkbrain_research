# SparkBrain v0.6 Control Qualification Report

## Decision

```text
Primary qualification worlds:     9 / 9 passed
Primary evidence records:        81 / 81 passed
Control qualification worlds:    36 / 36 contract-complete
Control evidence records:       324 / 324 present and unique
G3 / G4 / G5 adapters:          not yet qualified
V06-15 qualification ready:      false
V06-15 confirmatory ready:       false
PR #10 release merge-ready:      false
```

The control grid is an engineering qualification of adapter behaviour. It is not a frozen
confirmatory run and does not upgrade the Primary scientific claim.

## Grid shape

The four required non-comparator controls were run over the same development grid as the Primary:

```text
4 conditions × 3 world families × 3 seeds = 36 control worlds
36 worlds × 9 evidence domains             = 324 result records
```

World families:

- identifier permutation;
- temporal perturbation;
- Field threshold/magnitude perturbation.

Seeds:

```text
0, 1, 2
```

Every public adapter emits exactly one record for every evidence domain, including negative records.
No missing, duplicate, or unexpected control result is permitted.

## 1. No-endogenous control

The adapter uses the real Primary runtime and suppresses reinjection at every allowed endogenous
generation depth.

Expected and observed contract:

```text
learned local proposals may be prepared
normal endogenous reinjection is suppressed
later endogenous Field Sparks: 0
external observations remain external
positive self-confirming updates: 0
```

This control passes taxonomy non-interference only. It must not pass endogenous origin, causal chain,
boundary, relation, re-entry, or persistence domains.

## 2. Readout-only control

The adapter learns the same anonymous local transition state and produces the expected structural
proposal, but never places that proposal into the Field.

Expected and observed contract:

```text
main structural proposal count:      1
alternate structural proposal count: 1
later Field Spark count:              0
```

This separates a data-structure prediction from a normally thresholded endogenous Field event. It
passes taxonomy non-interference only.

## 3. Count/time/current/energy-matched random control

The adapter first records the Primary accepted reinjection schedule, then creates deterministic
random-target proposals outside the learned main path with matched:

- proposal count;
- scheduled arrival times;
- effective current magnitudes;
- total reinjection energy;
- generation-depth profile.

The random events pass through the same `FieldReinjectionGate` and may create normally thresholded
Field Sparks. They do not carry a learned sequential parent lineage and do not commit positive
learning.

This is stronger than a no-noise control: it asks whether merely injecting the same amount of event
energy at the same times can reproduce the claimed structured capability.

The qualified control passes taxonomy non-interference only.

## 4. Shuffled anonymous-relation control

The adapter preserves the earlier Primary mechanisms and learned evidence:

- endogenous origin;
- same-input/different-history response;
- autonomous chain;
- anonymous boundary effect;
- relation stabilization;
- reversal/reacquisition statistics;
- taxonomy non-interference.

Before relation re-entry, it swaps the anonymous external targets carried by the learned relation
state and recomputes content-valid structural link IDs.

Expected and observed contract:

```text
acquired relation re-enters the wrong target
reversed relation re-enters the opposite target
returned relation re-enters the wrong target
correct relation re-entry: false
persistence-locus target transfer: false
```

This is a direct placement control. It shows that closed-loop re-entry depends on the learned
relation state's actual anonymous source-target organization rather than only on the existence of
some reliability number.

## Domain expectations

| Condition | Expected positive evidence |
|---|---|
| no-endogenous | taxonomy non-interference only |
| random endogenous matched | taxonomy non-interference only |
| readout-only | taxonomy non-interference only |
| shuffled relation | early Primary domains plus taxonomy; relation re-entry and persistence locus must fail |

A control adapter is considered qualified only when both its expected positives and expected
failures occur over every development family/seed pair.

## Self-confirmation and taxonomy boundaries

Across all four controls:

```text
self-confirmation violations: 0
taxonomy hash match:          1.0
```

Observer view renaming is required to leave the normalized runtime state unchanged.

## Validation

The first control-grid push, GitHub Actions run `33266833787`, stopped at Ruff because `Callable`
was imported from `typing` rather than `collections.abc`. No runtime test executed in that run. The
import was corrected without changing the experimental contract.

The corrected control adapter and test grid passed in GitHub Actions run `33266953863` on Python
3.11 and Python 3.13:

```text
Install: PASS
Ruff lint: PASS
Local readiness: PASS
Default test suite: PASS
Bundle validation: PASS
```

## Remaining qualification blockers

The current normalized interface is now implemented for:

1. Primary;
2. no-endogenous;
3. random endogenous matched;
4. readout-only;
5. shuffled relation.

Still missing:

6. G3 generic recurrent comparator;
7. G4 explicit Assembly-conditioned comparator;
8. G5 typed functional-head comparator.

The manifest remains `UNFROZEN`, qualification readiness remains false, and the held-out 5 × 10 run
must not start.

## Claim boundary

This report supports only that four required controls have executable, deterministic, fail-closed
3 × 3 qualification adapters with complete result coverage and the intended positive/negative
patterns.

It does not establish confirmatory Level 1, Level 2, or Level 3 support, architectural uniqueness,
comparator inferiority, held-out generalization, or release readiness.
