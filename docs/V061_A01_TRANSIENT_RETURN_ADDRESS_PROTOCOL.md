# v0.6.1 A01 — Existing Transient Return-Address Credit Bridge

## 1. Position

A01 is the first prospective mechanism candidate admitted after D1-D12 and P1-P5 protocolization.
It is intentionally minimal.

A01 is **not** designed to establish emergent Field organization. Its question is:

> Is the causal lineage already present during exact external pairing sufficient to close the
> world-to-local competition loop if the architecture uses that lineage before persistence compresses
> it away?

The bound proposal record is:

```text
docs/diagnostics/v061/V061_A01_TRANSIENT_RETURN_ADDRESS_PROPOSAL.json
```

Bound proposal specification SHA-256:

```text
2794d1596227eab17c68c46d6874662c3669656edb49e28425f1ef613b66c5dc
```

Status:

```text
PREREGISTERED_NOT_IMPLEMENTED
```

## 2. Existing state reused by A01

A01 must not add a second return-address queue.

It reuses the existing path:

```text
actual generated Spark
    -> BoundaryEvent.source_proposal_ids
    -> PendingBoundaryEvent.event
    -> exact external parent pairing
```

The current consistency timing contract remains unchanged:

```text
maximum_pair_lag_ms = 30.0
pending_ttl_ms      = 40.0
maximum_pending     = 256
```

These are existing runtime values, not A01 tuning parameters.

The provenance ledger already retains proposal ancestry and `local_path_ids` while the pending
boundary is live. A01 may resolve only those historical IDs that are already present in the existing
causal lineage.

## 3. New capability introduced

The only new functional edge under test is:

```text
exact external consequence
    -> existing pending BoundaryEvent lineage
    -> signed anonymous causal evidence
    -> historical local transition lineage
    -> future shared-root competition
```

A01 therefore tests a **credit bridge**, not a new world model, semantic target, reward system,
Assembly, or persistent return-address memory.

## 4. Causal pairing rule

Positive or negative upstream credit is eligible only when the external event explicitly identifies
the pending boundary as a parent:

```text
boundary.event_id in external.parent_event_ids
```

The existing consistency fallback pairing remains available for relation statistics, but it is not
causal evidence for A01.

```text
exact parent pairing
    -> A01 causal evidence may be evaluated

fallback temporal pairing only
    -> consistency may learn
    -> A01 local credit = 0
```

This is the core P1 anti-correlation guard.

## 5. Anonymous match / contradiction rule

A01 may not read the evaluator's `expected_external_target`.

Signed evidence is derived only from the **pre-observation anonymous relation state** for the exact
boundary port.

Before applying the new external observation:

1. collect already-learned relation links for the boundary's `port_id`;
2. consider only links with at least one real external consistency observation;
3. compute their existing anonymous reliability under the unchanged consistency prior;
4. if one relation key `(target, polarity)` has a unique maximum reliability, it is the current
   anonymous relation expectation for this bridge event;
5. if no learned link exists or the maximum is tied, A01 abstains from local credit.

Then:

```text
observed external (target, polarity) == unique prior dominant relation
    -> causal match

observed external (target, polarity) != unique prior dominant relation
    -> causal contradiction

no unique prior dominant relation
    -> unresolved / no local update
```

The ordinary anonymous consistency update still occurs after this pre-observation classification.
No semantic role or correct answer enters the rule.

## 6. Historical lineage attribution

For an exact causal boundary, A01 starts only from `BoundaryEvent.source_proposal_ids`.

For each source proposal, the existing provenance ledger may be followed recursively through
`parent_proposal_ids` to recover the actually recorded local path IDs.

A01 does not search unrelated proposals or choose a path because it has the best score.

All local path IDs in the actual causal ancestry receive the same signed evidence for that boundary.
A matched but noncausal lineage receives no update.

If multiple proposal ancestors genuinely contributed to the same emitted boundary, A01 does not
invent a hidden singleton. Their shared attribution remains plural. P4 is allowed to expose this as a
limitation if later external evidence cannot differentiate them.

## 7. Persistent local causal-support state

A01 adds an explicit anonymous support record to an existing local transition path:

```text
external_consistent_count
external_contradicted_count
```

Initial prior:

```text
consistent    = 0
contradicted  = 0
Beta prior    = (1, 1)
prior causal reliability = 0.5
```

For an exact-parent causal match:

```text
external_consistent_count += 1
```

For an exact-parent causal contradiction:

```text
external_contradicted_count += 1
```

External absence, internal replay, fallback-only pairing, or unresolved relation expectation does not
create positive local credit.

This state is intentionally explicit. A01 is expected to face a strong P5 reduction test rather than
being protected by the word "anonymous".

## 8. Competition influence rule

Let the existing local temporal proposal confidence be:

```text
base_confidence
```

Let:

```text
causal_reliability =
    (1 + external_consistent_count)
    / (2 + external_consistent_count + external_contradicted_count)
```

The neutral prior is `0.5`. A01 applies a centered gain:

```text
causal_gain = causal_reliability / 0.5
adjusted_confidence = min(1.0, base_confidence * causal_gain)
```

Properties fixed before execution:

```text
no external evidence
    -> causal_reliability = 0.5
    -> causal_gain = 1.0
    -> exact baseline behavior unchanged

consistent exact-parent evidence
    -> gain > 1.0

contradictory exact-parent evidence
    -> gain < 1.0 once contradiction dominates

confidence remains inside existing [0, 1] contract
```

There is no tunable mixture coefficient between temporal and causal evidence in A01.

The cap at `1.0` exists only because the current `EndogenousPulseProposal.confidence` contract is
bounded to `[0, 1]`.

## 9. Train / evaluation boundary

A01 adopts the stricter lesson from the CX01 pre-formal review:

- development training phases may update A01 only from declared external observations;
- non-adaptive probe prefixes cannot mutate A01 learned state;
- cue-only readout cannot learn;
- internal generated events cannot update causal support;
- every non-adaptive probe records a learned-state hash before and after evaluation and requires
  equality.

This is protocol quality transfer only; CX01 results are not imported as A01 evidence.

## 10. P1 expectations

### External match

The exact causal lineage must gain support relative to the resource-matched noncausal lineage.

### Lineage swap

When causal responsibility is exchanged, support must follow the new exact parent lineage.

### Contradiction

A contradiction to the unique pre-observation anonymous relation must weaken the exact causal lineage
relative to the matched noncausal lineage.

### External absence

No positive causal-support update.

### Internal replay only

No causal-support update and no positive commit.

Any fixed-lineage preference fails A01.

## 11. P2 expectation

A01 must demonstrate that changing the anonymous world relation, after the required relation history
has been established while local temporal observations are controlled, changes **future shared-root
local competition**.

Changing only final relation re-entry is a failure.

The local state held fixed in the P2 intervention refers to the pre-intervention local temporal state;
A01 is then allowed to change local causal-support state only through the newly observed exact-parent
external evidence prescribed by the trial.

## 12. P3 expectation

A01 preregisters two causally distinct roles:

```text
R = transient return address
    required during external attribution

L = local transition state
    persistent carrier of the learned future-competition effect after attribution
```

Expected P3 signature:

- after learning, valid L-only transplant transfers A01's persistent competition bias;
- F-only does not transfer A01's explicit support counts;
- C-only may transfer relation re-entry but not A01 local competition bias;
- R is necessary during the causal update episode but is not expected to remain as persistent learned
  state after the external pairing is consumed.

Therefore A01 is not evidence for distributed Field memory even if it passes P1-P4.

## 13. P4 expectation

A01 must not force a singleton merely because multiple local lineages are co-maximal.

If separate causal boundary events exist for the competing lineages, later exact-parent external
evidence may differentiate them.

If several candidate lineages are irreducibly merged into one causal BoundaryEvent ancestry, A01
credits the actual causal ancestry set rather than inventing a winner. If this prevents later useful
differentiation, A01 fails P4 for that case.

That failure is informative and is not repaired by ID-based tie breaking.

## 14. P5 explicit null

The primary explicit null is deliberately strong:

```text
path_id -> (external_consistent_count, external_contradicted_count)
```

using the same exact-parent evidence, same anonymous relation classification, same Beta prior, and
same confidence modulation.

If this established-minimal explicit predictor reproduces A01 endpoints, temporal response, update
locus, state transplant, unseen combinations, and state/resource profile, A01 must be classified as:

```text
behaviorally-and-dynamically-explicit-memory-equivalent
```

That is an expected scientifically valid outcome.

A01's purpose is to test whether causal address use is sufficient, not to evade this classification.

## 15. P5 recurrent null

A resource-matched recurrent causal-trace comparator must receive the same admissible external causal
evidence and comparable persistent/transient state budget without direct evaluator targets.

RV01 R01-12D motivates treating generic recurrence as a serious null. Its results are not copied into
A01 and no RV01 held-out outcome is used here.

## 16. A01 stopping observations

A01 is rejected as a causal bridge if any preregistered discriminator shows that:

```text
exact-parent credit does not follow the causal lineage after lineage swap
or
external contradiction cannot selectively correct the causal lineage
or
world-relation change fails to alter future local competition
or
positive support can arise from absence/internal replay/fallback-only correlation
```

If A01 passes P1-P4 but strengthened P5 reduces it to the minimal explicit local eligibility model,
A01 is **completed as explicit anonymous transition memory**, not rescued as emergent Field
organization.

## 17. Implementation boundary

This document freezes the A01 mechanism hypothesis and discriminator mapping. It does not implement
A01 in the v0.6.1 Primary and does not authorize changing candidate-003.

A01 implementation must occur on a separate prospective research branch derived from the accepted
diagnostic protocol state. Any change to the rules above requires a new proposal generation and a new
bound specification hash before capability results are observed.
