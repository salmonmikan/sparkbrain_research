# RV01 R01-13 Activity-Matched Mechanistic Discrimination Protocol

## Status

R01-13 is a new post-formal research line opened only after R01-12F was closed.
It does not reopen, repair, rerun, tune, reinterpret, or replace R01-12F.

R01-12F remains bound to:

```text
candidate:                  rv01-r01-12-interference-heldout-v1
frozen source SHA:          83d2c77d8ae3878727d2ed4e9e78bc169ce064b8
raw result SHA-256:         e3f0cef5428c1b9a550c986404c1435952bd23fd0bdc0cc24a73b8e0c9f70ff4
canonical payload hash:     c014c0513f113e48ddcf5322579106a318f220236d05f25d39c3bd47e88f0673
preservation branch commit: 11b7ed765b09752bf0bc3e9f99984f561300134a
```

R01-13 protocol identifier:

```text
rv01-r01-13-activity-matched-discrimination-v1
```

## Motivation

R01-12D and R01-12F reproduced the same narrow trade-off:

- the physical Field retained ordered route elements more broadly in shared-prefix,
  reversal, and dense-load worlds;
- exact-route recovery remained tied with the preregistered resource-matched reservoir;
- the Field produced more contamination overall;
- disjoint and shared-cue families did not establish a Field advantage;
- dense-load first-hop coverage favored the Field, while the other families tied.

The unresolved mechanistic question is therefore not "does Field win?" but:

> Does the retained ordered-continuation difference survive when the two systems are
> compared at matched emitted-event volume and matched distinct-candidate breadth?

R01-13A attacks two alternative explanations before any state-locus transplant is
allowed.

## Scientific firewall

The following rules are fixed for R01-13A:

1. R01-12F evidence is read-only historical motivation.
2. The R01-12 Field implementation is reused without architecture or threshold changes.
3. `ResourceMatchedSparseReservoir` is reused without weakening, retuning, or changing
   its resource contract.
4. No held-out R01-12 world is rerun.
5. R01-13 uses a fresh seed namespace and a fresh world-grid salt.
6. Activity matching is evaluator-side deterministic prefix truncation only. It cannot
   change training, recurrent dynamics, plasticity, scores, or rollout selection.
7. Exact-route recovery and contamination remain mandatory outputs. A retention gain
   cannot be reported without them.
8. First-hop coverage keeps the original registered semantics and is reported only on
   raw traces. It is not silently redefined on flattened matched traces.
9. Development failures are preserved. R01-13A may motivate a later protocol, but its
   already-produced raw result is not overwritten or rescued.

## Fresh world contract

R01-13 fixes both development and future held-out scale at 96 anonymous units. The
family geometry, exposure pattern, threshold range, lag range, active-output budgets,
and route counts otherwise mirror the R01-12 held-out-scale contract.

Development seeds:

```text
200, 201, 202, 203, 204
```

Future held-out seeds are reserved now but capability remains closed:

```text
300, 301, 302, 303, 304, 305, 306, 307, 308, 309
```

This gives:

- 5 families x 5 development seeds = 25 development worlds;
- 5 families x 10 reserved held-out seeds = 50 future held-out worlds.

The old R01-12 development seeds `0-2` and held-out seeds `100-109` are excluded.

## Registered raw measures

For every final route probe, R01-13 preserves the same raw measures used in R01-12:

- ordered retention;
- exact-route recovery;
- contamination count;
- first-hop coverage;
- generated units / emitted-event count.

In addition, R01-13 reports contamination rate and ordered-match yield so a system
cannot improve an interpretation merely by producing more events.

## Matching view A: emitted-event matching

For one paired Field/reservoir route probe:

```text
B_event = min(len(Field generated units), len(reservoir generated units))
```

Both traces are truncated to their first `B_event` generated units. No reranking,
subsampling, route-aware filtering, or label-aware selection is allowed.

The matched prefixes are rescored for:

- ordered retention;
- exact-route recovery;
- contamination count and contamination rate;
- ordered-match yield.

This tests the simple output-volume null:

> The Field's R01-12 retention advantage is only a consequence of emitting more events.

## Matching view B: distinct-candidate breadth matching

For the same paired probe:

```text
B_distinct = min(number of distinct Field units, number of distinct reservoir units)
```

For each system independently, take the shortest original-order prefix containing
exactly `B_distinct` distinct generated unit IDs.

Again, no reranking or route-aware filtering is permitted.

This view is rescored with the same retention/exact/contamination/yield metrics.
It tests the stronger structured-over-activation null:

> The Field's R01-12 retention advantage is explained by keeping a broader set of
> candidate units active, rather than by a continuation-specific dynamical signature.

## Primary discrimination logic

R01-13A does not use a tuned numerical threshold. Direction and family structure are
reported directly.

### P13-A1 — event-volume discrimination

Primary target families are:

- shared-prefix branches;
- edge reversal;
- dense route load.

If the Field's raw retention difference collapses to zero or reverses after
emitted-event matching, the simple output-volume explanation remains sufficient for
that family.

A positive matched difference is evidence against that null, but is not architectural
uniqueness.

### P13-A2 — candidate-breadth discrimination

If the event-matched difference survives but collapses to zero or reverses after
candidate-breadth matching, the remaining effect is compatible with structured
wide-candidate activation.

If a positive retention difference survives both views, then the two simplest
activation-volume explanations are insufficient for that family. That result would
justify R01-13B state-locus / timing-mechanism interventions.

### P13-A3 — negative controls

Disjoint routes and shared-cue branches remain negative/reference families.
A broad Field advantage appearing there would weaken the interpretation that the
R01-12 signature is interference-specific.

## Interpretation boundaries

Even if P13-A1 and P13-A2 survive, R01-13A will not establish:

- Field superiority;
- unique necessity of the Field architecture;
- semantic or causal understanding;
- clean branch selection;
- causal-credit assignment;
- that another recurrent dynamical system cannot reproduce the same matched signature.

The strongest allowed statement would be:

> The replicated R01-12 ordered-continuation difference is not eliminated by matching
> emitted-event volume or distinct-candidate breadth under the fixed R01-13 evaluator.

If the effect fails either control, that negative result is the result.

## A01 boundary

R01-13 remains a continuation-substrate experiment, not a causal-credit experiment.
Its relevance to A01 is conditional:

- if the Field retains structured continuation after activity/breadth matching, A01 can
  treat RV01 as evidence that candidate lineage availability is physically supportable;
- if the advantage collapses under breadth matching, A01 should not treat RV01
  continuation as a distinct lineage-preservation mechanism;
- in neither case does R01-13 show that anonymous external outcomes return selectively
  to the causal lineage that produced them.

That selective return remains A01's separate discriminator.

## Execution boundary

The initial implementation may execute only the 25 development worlds.
The 50 reserved held-out worlds may be generated and hashed for contract validation,
but capability execution through the R01-13 runner must raise before opening.

A future held-out run requires a new freeze review and explicit seal. It must not be
opened merely because development is favorable.
