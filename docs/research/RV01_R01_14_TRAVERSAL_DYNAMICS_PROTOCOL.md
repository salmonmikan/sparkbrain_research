# RV01 R01-14 Traversal Dynamics Discrimination Protocol

## Status

R01-14 is a new post-R01-13A research line. It does not reopen, repair, rerun,
retune, or reinterpret R01-12F or the fixed R01-13A development result.

Historical anchors remain read-only:

```text
R01-12F raw result SHA-256:
e3f0cef5428c1b9a550c986404c1435952bd23fd0bdc0cc24a73b8e0c9f70ff4

R01-13A development_result.json SHA-256:
1ab43a8950be572b163e7bba4950b23d5258933e5463dc3d944f41eaea2adf60

R01-13A suite hash:
ec6228563d5060872345c582b87c18cae03af4ad36895d08f4ee9f4b18b0178e
```

R01-14 protocol identifier:

```text
rv01-r01-14-traversal-dynamics-v1
```

## Motivation

R01-13A reproduced the R01-12 raw high-coverage / low-selectivity signature, but
its registered ordered-retention advantage disappeared in every family after
matching distinct-candidate breadth. The preregistered R01-13B state-locus
admission criterion therefore failed and R01-13B remains closed.

The residual observation was narrower: at a common distinct-candidate breadth,
the Field often reached that breadth with fewer emitted events than the fixed
resource-matched reservoir. Equal-event truncation also created a Field advantage
in the disjoint negative family, so the residual cannot be assumed to be an
interference-specific retention mechanism.

R01-14 asks only:

> Does the Field traverse distinct candidate states with fewer revisits or earlier
> first visits than the fixed reservoir, and is any such difference specific to
> interference rather than a general rollout-coding difference?

Ordered retention is not a primary R01-14 endpoint. It was already discriminated
in R01-13A and will not be rescued with a replacement score.

## Scientific firewall

1. R01-12F and R01-13A evidence are immutable historical motivation.
2. The R01-12 Field implementation is reused without architecture or threshold
   changes.
3. `ResourceMatchedSparseReservoir` is reused without weakening or retuning.
4. R01-14 uses a fresh seed namespace and fresh world-grid salt.
5. No R01-12 or R01-13 held-out world is executed.
6. Traversal metrics are evaluator-side read-only functions of generated unit IDs.
7. No route label, correctness label, reward, utility, or future outcome is used to
   decide which generated events count as traversal.
8. Disjoint routes and shared-cue branches remain mandatory reference families.
9. A broad difference that also appears in disjoint routes is classified as a
   substrate-general rollout difference, not an interference mechanism.
10. Development failures are preserved and cannot be repaired in-place.

## Fresh world contract

R01-14 keeps the 96-unit scale and the same five family geometries used in R01-13,
while changing both seed namespace and world-grid salt.

Development seeds:

```text
400, 401, 402, 403, 404
```

Reserved future held-out seeds:

```text
500, 501, 502, 503, 504, 505, 506, 507, 508, 509
```

This yields 25 development worlds and reserves 50 held-out worlds. Held-out
capability is closed in the initial runner.

## Route-agnostic traversal measures

For each generated trace `u_1 ... u_T`, define:

- `event_count = T`;
- `distinct_count = |{u_t}|`;
- `revisit_count = event_count - distinct_count`;
- `revisit_rate = revisit_count / event_count`;
- `new_state_yield = distinct_count / event_count`;
- `first_visit_positions`: one-based event indices of first visits, in discovery
  order;
- `normalized_discovery_auc`: the mean cumulative distinct fraction over the raw
  event sequence, normalized by the trace's final distinct count.

These measures are independent of the expected route identity.

## Common-breadth traversal view

For each paired Field/reservoir probe:

```text
B = min(Field distinct_count, reservoir distinct_count)
```

For each system independently, take the shortest original-order prefix that contains
exactly `B` distinct unit IDs. No reranking, subsampling, route-aware filtering, or
label-aware selection is permitted.

Registered common-breadth endpoints are:

- events required to reach `B` distinct states;
- revisits before reaching `B`;
- revisit rate in that prefix;
- new-state yield in that prefix;
- normalized discovery AUC in that prefix.

The primary directional quantity is:

```text
Delta_events = Field events_to_common_breadth
             - reservoir events_to_common_breadth
```

Negative `Delta_events` means the Field reaches the same distinct breadth with fewer
emissions. This is traversal efficiency only; it does not imply correctness or
selectivity.

## Discrimination logic

### P14-A1 — traversal-efficiency replication

Report `Delta_events`, revisit counts/rates, new-state yield, and discovery AUC for
all five families. No tuned threshold is used.

If the R01-13A residual was accidental, the common-breadth event difference should
collapse or become inconsistent on the fresh development grid.

### P14-A2 — interference specificity

A traversal difference is considered interference-specific only if it is absent or
materially weaker in the disjoint and shared-cue reference families while appearing
consistently in shared-prefix, reversal, or dense-load families.

If the same direction is already clear in disjoint routes, the supported conclusion
is a substrate-general rollout/repetition difference.

### P14-A3 — selectivity firewall

Contamination, exact-route recovery, and ordered retention may be retained as
secondary historical-context outputs from the underlying runs, but they are not used
to admit a traversal mechanism. R01-14 cannot convert a broad/dirty traversal pattern
into a claim of clean continuation.

## Interpretation boundaries

Even a strong R01-14 traversal result will not establish:

- Field superiority;
- architectural uniqueness;
- clean branch selection;
- causal lineage preservation;
- causal-credit assignment;
- that another recurrent system cannot reproduce the traversal signature.

The strongest allowed positive statement is:

> Under the fixed comparator and fresh R01-14 worlds, the Field reaches a matched
> distinct-state breadth with fewer revisits / earlier first visits.

Whether that difference is interference-specific is a separate result determined by
the reference families.

## A01 boundary

R01-14 can inform only the availability and temporal traversal of candidate states.
It cannot show that an anonymous external outcome returns selectively to the causal
lineage that produced it. If the traversal difference is substrate-general, A01 must
not treat it as evidence of lineage-specific credit routing.

## Execution boundary

The initial implementation may execute only the 25 development worlds. The 50
reserved held-out worlds may be instantiated and hashed, but capability execution
must raise. Any future held-out execution requires an explicit freeze review and a
new seal.