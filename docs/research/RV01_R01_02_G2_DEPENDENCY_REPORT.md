# RV01 R01-02 — Explicit G2 Dependency Report

## Decision

R01-02 holds the learned G1 transition table fixed and compares its raw proposals with the same
proposals after explicit G2 confirmation-gated adaptation.

```text
raw candidate generation survives without G2: YES
external stabilization requires G2:            YES
timing correction requires G2:                 YES
reversal requires G2:                          YES
reacquisition requires G2:                     YES
long-run selectivity requires G2:              YES
G1-only route remains static:                  YES
prepare/reinject alone can self-confirm:        NO
positive G2 commits without external match:      0
```

R01-02 is complete. The current v0.6 burden is now separated:

```text
G1 supplies explicit source-target-time candidates.
G2 supplies explicit externally confirmed confidence, timing calibration,
contradiction, reversal, and reacquisition state.
```

## Experimental isolation

G1 is trained symmetrically on:

```text
unit:0 -> unit:1 at +5 ms
unit:0 -> unit:2 at +5 ms
```

Both candidates therefore begin with:

```text
raw confidence = 0.5
raw relative arrival = +5 ms
```

The G1-only comparison remains a fixed read of that same learned table. It does not receive G2 path
confidence, timing correction, confirmed counts, or contradicted counts.

G2 then receives externally registered phases:

```text
Phase 1  unit:1 observed 3 times at +7 ms
Phase 2  unit:2 observed 6 times at +7 ms
Phase 3  unit:1 observed 6 more times at +7 ms
```

Each episode creates two G2 eligibilities from the unchanged G1 candidates. The externally observed
target confirms one path and contradicts the other.

## Initial state

```text
G1-only unit:1 confidence: 0.5
G1-only unit:2 confidence: 0.5
G2 unit:1 confidence:      0.5
G2 unit:2 confidence:      0.5
positive commits:             0
```

A prepare-only probe creates eligibility but no external outcome. Its positive commit count remains
zero.

## Stabilization phase

After three external unit:1 outcomes:

```text
unit:1 confirmed / contradicted: 3 / 0
unit:2 confirmed / contradicted: 0 / 3

G2 unit:1 adapted confidence: 0.75
G2 unit:2 adapted confidence: 0.20

G1-only unit:1 confidence:    0.50
G1-only unit:2 confidence:    0.50
```

G1 continues to emit both raw candidates equally. The externally selected preference exists only in
G2 state.

## Timing correction

The externally observed lag is +7 ms while G1 remains fixed at +5 ms.

After three unit:1 matches:

```text
G1-only relative arrival: +5.000 ms
G2 relative arrival:      +5.784 ms
```

The existing G2 implementation does not directly converge to the full +2 ms correction. It applies
an exponential update to the residual error of a proposal that is already corrected. With learning
rate 0.2, the first three corrections are:

```text
+0.400 ms
+0.640 ms
+0.784 ms
```

This is preserved as the actual frozen behaviour rather than silently repaired inside RV01.

## Reversal phase

After six external unit:2 outcomes:

```text
unit:1 confirmed / contradicted: 3 / 6
unit:2 confirmed / contradicted: 6 / 3

G2 unit:1 adapted confidence: 4/11 ~= 0.3636
G2 unit:2 adapted confidence: 7/11 ~= 0.6364

G1-only candidates: 0.5 / 0.5
```

The changed external contingency reverses G2 selectivity while the underlying G1 proposal table
remains unchanged.

## Reacquisition phase

After six additional external unit:1 outcomes:

```text
unit:1 confirmed / contradicted: 9 / 6
unit:2 confirmed / contradicted: 6 / 9

G2 unit:1 adapted confidence: 10/17 ~= 0.5882
G2 unit:2 adapted confidence:  7/17 ~= 0.4118
confidence gap:                 3/17 ~= 0.1765
```

The preregistered engineering gap for this dependency assay is 0.15. G1-only remains exactly tied at
0.5 / 0.5.

## External evidence accounting

```text
prepare-only positive commits: 0
stabilization confirmed commits: 3
post-reversal confirmed commits: 9 cumulative
post-reacquisition commits:      15 cumulative
```

The cumulative positive commit count equals the cumulative external match count exactly.
Endogenous proposal preparation alone never increments it.

## Interpretation

The strongest supported statement is:

> G2 is not required for G1 to emit raw next-event candidates. It is required in the current
> architecture for externally grounded candidate selection, local confidence calibration, timing
> correction, contradiction accumulation, reversal, reacquisition, and maintained selectivity.

Combined with R01-01, the present architecture can be stated more precisely as:

```text
G1 = explicit candidate transition memory
G2 = explicit external confirmation and revision memory
Field = normal-rule execution and thresholding of their proposals
```

This is a limiting result for the claim that v0.6 experience dependence already resides in generic
Field Dynamics.

## Validation

The first R01-02 test run exposed an incorrect expected timing correction of +0.976 ms. Inspection of
the frozen G2 recurrence showed that it learns residual error after applying the previous correction,
so the correct three-step value is +0.784 ms. The frozen implementation was not changed; the test was
corrected to its actual recursion.

GitHub Actions run `33288274372` passed on Python 3.11 and Python 3.13:

```text
Install:           PASS
Ruff lint:         PASS
Local readiness:  PASS
Full pytest:       PASS
Bundle validation: PASS
```

## Next gate

R01-03 introduces the smallest externally gated local rule that writes directly into ordinary Field
connection weights and delays. It may not create a G1-like source-target proposal table or a G2-like
confirmed/contradicted path table under new names.
