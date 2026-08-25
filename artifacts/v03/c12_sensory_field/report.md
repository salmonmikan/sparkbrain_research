# C12 computational sensory-gate report

Protocol: `c12-sensory-field-v1`  
Run: `c12-sensory-field-main-v1`  
Seeds: 2601, 2602, 2603, 2604, 2605

## Result

- G04 acceptance: **pass**
- predictable-repetition active-Spark reduction: 1.000000
- predictable-repetition downstream-active-work reduction: 1.000000
- change / explicit-omission recall: 1.000000
- bounded-goal low-salience recall delta: 1.000000
- irrelevant false-activation increase: 0.000000 percentage points
- stimulus-specificity recall: 1.000000

## Omission and work definitions

An omission is an explicit adapter observation that a previously expected channel is absent.
It is scored as value zero against the local prediction, then value zero is committed as the
latest local observation. It is not inferred from an absent key and is not evaluator truth.
The checked raw change/omission rows demonstrate recovery under this definition.

Every channel is inspected and scored. Repetition reduces emitted Sparks and downstream active
work; it does **not** reduce dense channel inspection/scoring in this implementation. These
counters are computational observations, not energy measurements.

## Claim boundary

This is a deterministic local computational sensory gate. It is not a biological sensory-system
reproduction, semantic understanding result, hardware-efficiency result, or change to C06/C08
negative findings or scientific claim grades. Failed ablations and adversarial rows are retained.
