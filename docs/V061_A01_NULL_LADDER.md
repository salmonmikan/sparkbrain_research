# v0.6.1 A01 Null Ladder

## Purpose

A01 is a minimal causal-credit bridge. It must be compared against strong alternatives rather than a
weak lookup strawman.

This document freezes the null families to be bound into the A01 proposal before any A01 capability
execution.

## N1 — Minimal explicit local eligibility memory

N1 receives exactly the same admissible causal evidence as A01:

```text
exact parent boundary only
same pre-observation anonymous relation match/contradiction classification
no fallback-only positive credit
no internal-replay positive credit
no external-absence positive credit
```

Persistent state per existing local path is exactly:

```text
external_consistent_count
external_contradicted_count
```

with the same fixed Beta prior `(1, 1)` and the same derived causal reliability:

```text
(1 + external_consistent_count)
/ (2 + external_consistent_count + external_contradicted_count)
```

N1 uses the same centered causal gain and `[0, 1]` confidence cap as A01.

N1 is explicitly allowed to be boring. If A01 and N1 match across strengthened P5 while N1 is no
larger and no more lookup-privileged, A01 is classified as explicit anonymous transition memory.

N1 may not use:

```text
evaluator correct target
semantic relation role
scalar reward
Assembly ID
typed action/prediction/reward state
future test identity
```

## N2 — Compact explicit relation-to-path table

N2 tests whether A01's behavior depends only on a compact keyed decomposition rather than the
historical runtime path.

N2 may store only the smallest established mapping needed to reproduce:

```text
anonymous boundary relation evidence
-> local path causal-support state
```

It must be subjected to:

```text
identifier permutation
physical trajectory substitution
state-locus transplant
unseen lineage combination
```

If N2 matches endpoints but requires more global lookup than A01, strengthened P5 reports structural
non-equivalence rather than emergence.

N2 minimality must be demonstrated; it cannot be asserted by naming the implementation "minimal".

## N3 — Resource-matched recurrent causal trace

N3 is the generic recurrent null motivated by the mixed RV01 R01-12D development result. It does not
import RV01 weights or held-out outcomes.

N3 receives the same anonymous event stream and the same admissible exact-parent external causal
evidence as A01. It must not receive evaluator targets or privileged labels.

Resource matching must account for at least:

```text
persistent scalar state
peak transient state
external observation count
active-output budget
generation / update budget
```

N3 must be tested on the same P1-P5 intervention families, including interference and bounded
ambiguity. Matching or beating A01 on one endpoint is not sufficient; temporal response,
contamination/ambiguity behavior, update locality, and state requirements remain descriptive parts of
the comparison.

## N4 — Relation-only downstream control

N4 preserves ordinary anonymous consistency and relation re-entry but blocks the new world-to-local
credit bridge.

It answers whether an apparent A01 improvement is actually caused by pre-existing downstream
relation behavior rather than the new upstream coupling.

Expected result if A01's bridge is causal:

```text
A01 changes future local competition after exact external evidence
N4 may change relation/re-entry output
N4 does not change the corresponding future local competition
```

## Non-compensatory use

No null failure can compensate for an A01 P1-P4 failure.

Likewise, A01 passing P1-P4 does not establish emergent Field organization. Strengthened P5 can still
classify it as explicit memory.

The intended interpretation ladder is:

```text
A01 fails P1-P4
    -> causal bridge hypothesis fails

A01 passes P1-P4 and N1/N2 reproduce it under strengthened P5
    -> explicit anonymous transition memory

A01 passes P1-P4 and defeats one tested explicit null
    -> that null is falsified only

A01 remains non-reduced after the full explicit + recurrent ladder
    -> stronger claim remains open
    -> emergence still requires the wider evidence programme
```

## Freeze boundary

Any material change to N1-N4 after A01 proposal binding requires a new A01 proposal generation before
capability outcomes are observed.
