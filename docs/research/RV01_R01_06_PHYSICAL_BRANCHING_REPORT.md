# RV01 R01-06 — Physical Branching and Ambiguity Report

## Decision

R01-06 tests whether overlapping externally observed histories can coexist in ordinary physical Field
connections without an explicit branch object, winner ID, correct branch, or transition table.

```text
equal histories preserve both branches:          YES
mild exposure bias preserves weaker branch:       YES
physical support remains graded:                  YES
single history invents an unobserved branch:      NO
untrained Field completes either branch:          NO
targeted branch-A suppression is selective:       YES
targeted branch-B suppression is selective:       YES
explicit winner/branch runtime state used:         NO
coactive ambiguity supported:                     YES
competitive resolution supported:                 NO
```

The engineering candidate supports physical coexistence and graded branch strength. It does not yet
support a claim that the Field resolves ambiguity through competition or selects one contextually
appropriate future.

## Overlapping histories

The shared prefix and two continuations are:

```text
branch A: 0 -> 1 -> 2 -> 4
branch B: 0 -> 1 -> 3 -> 5
```

Both are written by the same externally gated direct-physical-plasticity rule. Durable state remains
ordinary connection weights and delays.

The branching assay uses a lower but still ordinary Field threshold of `0.30` and a smaller causal
potentiation rate of `0.25`. This keeps a mildly less frequent branch above threshold while preserving
a measurable physical strength difference.

## Equal exposure

Each branch is observed three times.

With one later cue at unit 0, the Field produces:

```text
1
├─ 2 -> 4
└─ 3 -> 5
```

Both complete physical trajectories occur. The two divergence edges have matching learned weight and
delay.

## Mildly biased exposure

Exposure counts:

```text
branch A: 3
branch B: 2
```

Both branches still complete, but their physical support is graded:

```text
branch A divergence weight: approximately 0.504898
branch B divergence weight: approximately 0.353265

branch A divergence delay: 5.375 ms
branch B divergence delay: 5.750 ms
```

The more frequently observed branch activates earlier, while the weaker branch is not deleted or
collapsed by a hard winner-selection convention.

This is an observer description of the physical trajectory. The runtime stores no confidence label
or branch priority.

## Single-history and untrained controls

When only branch A is trained:

```text
1 -> 2 -> 4
```

is produced, while branch B is absent.

The untrained uniform Field produces no later branch completion under the same cue.

Thus coactivation in the overlap condition is not caused by a fixed branch generator or by the test
evaluator inserting both futures.

## Causal branch interventions

### Suppress branch A divergence

Setting only physical edge `1 -> 2` to zero yields:

```text
branch A: absent
branch B: 1 -> 3 -> 5 remains
```

### Suppress branch B divergence

Setting only physical edge `1 -> 3` to zero yields:

```text
branch A: 1 -> 2 -> 4 remains
branch B: absent
```

The two branch trajectories therefore depend on separable physical paths rather than one duplicated
observer interpretation of the same event sequence.

## What is not established

R01-06 does not yet show:

- inhibitory competition between futures;
- context-dependent selection of one branch;
- calibrated probabilities;
- branch confidence derived from later outcomes;
- suppression of an obsolete branch after contingency reversal;
- scalable ambiguity with many overlapping paths;
- robustness to noise or timing dispersion.

The current mechanism supports **coactive ambiguity**, not competitive decision-making.

## No explicit branch ontology

The candidate execution route imports no:

- `LocalTemporalExpectation`;
- `SparseLocalTransitionAdaptation`;
- `EndogenousPulseProposal`;
- Assembly;
- winner ID;
- chosen/correct branch field;
- branch reward.

Branch A and B names exist only in the experiment/evaluator code used to describe the two physical
paths.

## Interpretation

The strongest supported statement is:

> In a canonical overlapping-history Field, direct physical connection plasticity can retain and
> later express two supported continuations from one shared prefix. A mild exposure imbalance changes
> weights, delays, and activation timing without automatically erasing the weaker continuation.
> Selective physical-edge interventions independently remove either branch.

This addresses the first half of R01-06. The second half—whether generic Field dynamics can resolve
competition under context without an explicit winner mechanism—remains open.

## Validation

GitHub Actions run `33289021804` passed on Python 3.11 and Python 3.13:

```text
Install:           PASS
Ruff lint:         PASS
Local readiness:  PASS
Full pytest:       PASS
Bundle validation: PASS
```

## Next gate

R01-07 changes the externally observed continuation. A local heterosynaptic competition rule must
weaken the obsolete physical gateway and strengthen the new one without confirmed/contradicted
counters. Potentiation-only learning is retained as a control because it is expected to preserve both
old and new routes rather than revise.
