# v0.6.1 P1–P2 — Anonymous Causal-Credit Diagnostic Protocol

## 1. Position

Candidate-003 showed that anonymous world consistency does not reorganize earlier shared-root
trajectory competition. Before a new mechanism is implemented, SparkBrain needs a protocol that can
distinguish causal anonymous credit from correlation, self-confirmation, reward substitution, and
resource mismatch.

This protocol is architecture-neutral. It may later evaluate a SparkBrain proposal or RV01, but it
belongs to neither implementation and does not assume either succeeds.

## 2. P1 — Causal lineage versus matched correlation

Two anonymous lineages are constructed with exactly matched:

```text
event count
event times
effective current
energy cost
```

Only one lineage causally produces the outbound boundary event whose later raw external consequence
is observed.

### Required trials

| Trial | Causal lineage | Evidence | Required update |
|---|---|---|---|
| external match A | A | external consequence matches | selectively strengthen A |
| lineage swap | B | same consequence, causal path exchanged | selectively strengthen B |
| contradiction | A | different external consequence | selectively weaken/redirect A |
| external absence | A | no external consequence | no positive credit |
| internal replay only | A | internally generated recurrence only | no positive credit or commit |

The lineage-swap trial is essential. A mechanism that always favors lineage A, the more frequent
lineage, the lower-ID lineage, or the previously successful lineage fails even if one trial appears
correct.

## 3. Fail-closed contracts

### Resource matching

Causal and matched lineages must have identical resource signatures. A timing, current, event-count,
or energy difference invalidates the comparison.

### External evidence

Positive credit requires an actual external observation. Internal recurrence and omission cannot be
converted into confirming evidence.

### Contradiction

External contradiction must weaken or redirect the causally responsible lineage while leaving a
matched noncausal lineage comparatively unchanged.

### Self-confirmation

The following is forbidden:

```text
internal event
    -> internally predicted consequence
    -> positive commit
```

An internal event becomes positive evidence only after an independent external event confirms the
relation.

## 4. P2 — Fixed local state, permuted world relation

The local temporal state is held byte-identical while the anonymous world consequence changes.

```text
same G1/local state
same current input
same event resources
world relation A -> world relation B
```

The observed quantity is future shared-root trajectory competition.

### Interpretation

```text
future competition changes
    -> evidence that world relation circulates back into local trajectory formation

only final relation re-entry changes
    -> downstream-only loop remains

nothing changes
    -> no world-to-transition circulation
```

A changed final readout is not sufficient. The protocol asks whether the earlier anonymous local
competition itself changes.

## 5. Acceptance criteria for a future mechanism

A mechanism passes P1–P2 only when:

1. matched resources are exact;
2. positive credit follows the actual causal lineage after lineage swap;
3. matched correlation does not receive equivalent credit;
4. internal-only recurrence cannot create positive credit;
5. contradiction selectively weakens or redirects the causal lineage;
6. changed anonymous world relations alter future local competition with local observations held
   fixed;
7. no evaluator target, reward scalar, correct action, role, Assembly key, or semantic label enters
   runtime;
8. the effect can be reset, transplanted, and causally suppressed;
9. the resulting state is audited for equivalence to an explicit transition/lookup table.

## 6. What this protocol does not assume

It does not assume that the correct solution is:

```text
an eligibility trace
a Field-distributed trace
a local gain rule
a winner-take-all process
```

Those remain competing hypotheses. P1–P2 define observations that any proposed solution must
explain.

## 7. Current Primary expectation

Under the frozen v0.6 structure, P2 is expected to show:

```text
local transition state fixed
world relation changed
future G1 selection unchanged
```

because anonymous consistency state feeds relation re-entry but does not feed G1 transition
competition.

This expected failure is a diagnostic baseline, not a target to hide.

## 8. Implementation artifact

Observer/evaluator contracts are implemented in:

```text
src/sparkbrain/evaluation/v061_anonymous_credit_diagnostic_protocol.py
tests/v06/test_anonymous_credit_diagnostic_protocol.py
```

The code evaluates trial validity and hypothetical mechanism observations. It does not implement a
new SparkBrain learning rule.
