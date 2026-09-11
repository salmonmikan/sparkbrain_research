# RV01 R01-14A Development Result — Traversal Dynamics Discrimination

## Status

R01-14A development execution is complete and fixed.

```text
protocol:                   rv01-r01-14-traversal-dynamics-v1
execution source SHA:       d0c828dda9faf1ff0d455adf02be4e9ef65030fb
workflow run:               34308089316
workflow conclusion:        success
development worlds:         25
final route probes:         100
held-out capability:        NOT EXECUTED
```

Evidence binding:

```text
world grid hash:
15a1d4c862baf1564d8495239f82a767c9ee93c727d539cb4a8fe37d9ea7fa60

suite hash:
a25beeb5148fa846fceba5cfe268d664a941440faaba5f3c08bf1d15adcb4938

development_result.json SHA-256:
4a214059cacc66d473776de7b46455c959ce0ac5c7089c6acfafbc9e0ef91e25

artifact:
ID 10087415924
ZIP SHA-256 fb9e4f6ee01bb41ca0a733480683fafdf3f1d5d1b7e1d141681d241191d50bdd
```

R01-12F and R01-13A remain immutable. No held-out RV01 capability was opened.

## Question

R01-13A showed that the raw Field ordered-retention advantage disappears once the
number of distinct candidates reached is matched. R01-14A therefore did not try to
rescue ordered retention with another correctness score.

Instead it asked a narrower route-agnostic question:

> At a common distinct-state breadth, does the Field require fewer emitted events and
> fewer revisits than the fixed resource-matched reservoir, and is such a difference
> specific to interference?

## Historical-context replication

The fresh R01-14 development grid again reproduced the already-known raw trade-off:

| Context measure | Field | Resource-matched reservoir |
|---|---:|---:|
| mean ordered retention | **1.0000** | 0.8967 |
| exact routes | 40 / 100 | 40 / 100 |
| contamination count | 360 | **293** |
| raw emitted events | 718 | 715 |

This context is not the R01-14 primary endpoint. It confirms only that the new seed
namespace did not destroy the historical pattern.

## Primary common-breadth traversal result

Across 100 paired final-route probes, the common distinct breadth averaged `5.44`
units.

| Traversal measure | Field | Reservoir |
|---|---:|---:|
| events to common breadth | **5.46** | 6.36 |
| mean revisits to common breadth | **0.02** | 0.92 |
| mean revisit rate | **0.0040** | 0.1818 |
| mean new-state yield | **0.9960** | 0.8182 |
| normalized discovery AUC | **0.9986** | 0.9050 |

The paired direction was:

```text
Field faster probes: 59 / 100
Tied probes:         41 / 100
Field slower probes:  0 / 100

Field faster worlds: 20 / 25
Tied worlds:          5 / 25
Field slower worlds:  0 / 25

mean Field - reservoir events to common breadth: -0.90
```

Thus the residual R01-13A observation was not accidental on this fresh development
grid. Under the fixed comparator, the Field generally reaches a matched distinct-state
breadth with fewer repeated emissions.

## Family-level result

| Family | Common breadth | Events F / R | Revisit rate F / R | Faster / tied probes |
|---|---:|---:|---:|---:|
| disjoint routes | 3.00 | **3.00 / 4.80** | **0.000 / 0.370** | 15 / 0 |
| shared-cue branches | 9.00 | 9.00 / 9.00 | 0.000 / 0.000 | 0 / 15 |
| shared-prefix branches | 5.00 | **5.00 / 6.00** | **0.000 / 0.1667** | 15 / 0 |
| edge reversal | 3.27 | **3.40 / 4.27** | **0.0267 / 0.1922** | 9 / 6 |
| dense route load | 6.00 | **6.00 / 6.875** | **0.000 / 0.1813** | 20 / 20 |

Every disjoint world favored the Field, while every shared-cue world tied. All five
shared-prefix worlds favored the Field. All five reversal and dense worlds favored the
Field on their world mean, although some individual route probes tied.

## P14-A1 — traversal-efficiency replication

**SUPPORTED as a descriptive substrate difference.**

The Field reaches the same paired distinct breadth with fewer emissions and fewer
revisits on the fresh development grid. The direction is strong and contains no
Field-slower route probe in this sample.

This does not mean the Field is more correct. At raw scale, exact-route recovery still
ties and Field contamination remains larger.

## P14-A2 — interference specificity

**NOT SUPPORTED.**

The strongest family-level event difference occurs in the disjoint reference family:

```text
Field:     3.00 events to breadth 3
Reservoir: 4.80 events to breadth 3
Delta:    -1.80 events
```

The disjoint family is also perfectly tied on historical correctness context:
ordered retention `1.0 / 1.0`, exact recovery `15 / 15`, and contamination `0 / 0`.
The traversal difference therefore exists even when there is no route interference to
explain.

Shared-cue branches, by contrast, tie exactly on traversal. The effect is therefore
not universal across all topologies, but the disjoint result is sufficient to reject
an interference-specific interpretation.

The supported classification is:

> **topology-conditioned, substrate-general rollout/repetition difference**

rather than a special interference-retention mechanism.

## P14-A3 — selectivity firewall

The firewall remains intact.

R01-14A does not convert efficient distinct-state traversal into clean selection:

- exact-route recovery is still tied overall (`40 / 100` each);
- Field contamination is still higher (`360` vs `293`);
- R01-13A already showed that breadth matching removes the registered ordered-retention
  advantage.

Therefore "less repetition" and "better route selection" must remain separate claims.

## Mechanistic interpretation

The remaining RV01 difference is now localized more narrowly than after R01-12F.

The Field often emits a newly reached unit on successive events, whereas the fixed
reservoir frequently revisits already-generated units before reaching the same number
of distinct states. This is especially clear in disjoint and shared-prefix worlds.

However, because the same effect is strong in disjoint routes, R01-14A does not support
an explanation in terms of interference-specific memory preservation. The difference
is more plausibly attached to the rollout dynamics themselves: temporal propagation,
revisit/repetition structure, or the way activity moves through the shared topology.

This experiment does not identify which Field primitive causes the difference. It only
moves the explanatory locus from "ordered retention under interference" to
"distinct-state traversal / repetition dynamics."

## R01-14A decision

```text
R01-13 breadth explanation of retention gap:   REMAINS SUFFICIENT
R01-14 distinct-state traversal difference:    SUPPORTED descriptively
R01-14 interference specificity:               NOT SUPPORTED
Field exact-route superiority:                 NOT SUPPORTED
Field cleanliness/selectivity superiority:     CONTRADICTED by contamination
R01-14 held-out capability:                    REMAINS CLOSED
```

There is no scientific reason to open R01-14 held-out merely to recover the rejected
interference-specific interpretation. A future held-out study would need a new,
explicitly justified claim target and freeze review.

## Updated RV01 characterization

The strongest supported statement is now:

> The physical Field is a broad, low-selectivity continuation substrate whose raw
> coverage advantage is explained by broader candidate reach, while a separate
> topology-conditioned but non-interference-specific signature remains: it often
> traverses distinct states with fewer repeated emissions than the fixed
> resource-matched reservoir.

In one shorter sentence:

> **Field is strong at broad, low-repetition candidate traversal, but weak at clean
> route isolation and selective attribution.**

## A01 implication

R01-14A further narrows what A01 may borrow from RV01.

RV01 supports the physical availability and rapid traversal of multiple candidate
states without explicit G1/G2 route state. It does not support a special mechanism that
keeps the causally correct lineage privileged under interference.

Because the traversal difference already appears in disjoint routes, A01 must not use
it as evidence of causal-lineage specificity. A01 still has to independently show that
an anonymous outcome returns selectively to the lineage that actually produced it and
changes later local competition for that lineage rather than globally sustaining broad
candidate activity.

## Next boundary

If RV research continues, the next mechanistic question should target the origin of the
repetition difference itself without reopening ordered retention:

> Which ordinary Field-local timing/dynamics property suppresses immediate revisits or
> accelerates first visits, and does an intervention on that property selectively alter
> traversal efficiency while leaving the fixed learning/resource contract intact?

That would require a new protocol and seed boundary. R01-14A is now a fixed development
result and must not be overwritten or rescued.


## 2026-09-11 independent-review correction

The fixed development raw artifact is preserved unchanged. Independent review found that the historical `normalized_discovery_auc` implementation used an ideal-discovery-curve denominator rather than the preregistered `events * final_distinct_count` denominator. Therefore every discovery-AUC value in the fixed R01-14A artifact is **invalid for the registered endpoint and must not be used as scientific evidence**. The implementation is corrected prospectively only; the historical raw JSON and suite hash are not rewritten and this candidate is not rerun.

The non-AUC observations based directly on event counts, distinct counts, revisit counts/rates, ordered retention, exact-route recovery and contamination remain descriptive fixed evidence subject to their existing development-only boundary. The development conclusion that interference specificity was not supported remains a retained negative result. Held-out R01-14 capability remains closed.

The fixed artifact is bound to CPython 3.11.15 and does not claim portable hash reproduction on other interpreters.
