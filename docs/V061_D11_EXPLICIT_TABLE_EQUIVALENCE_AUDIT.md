# v0.6.1 D11 — Explicit-Table Equivalence Audit

## 1. Purpose

D10 indicates that the current boundary-to-consistency compression loses the historical proposal/path
return address required for causally selective feedback. Retaining a return address is therefore a
plausible requirement for a future mechanism.

It is not sufficient evidence of a new SparkBrain principle.

A mechanism can preserve anonymous IDs and still be nothing more than:

```text
lineage/path key
    -> stored target or score
    -> direct lookup
```

This audit separates obvious explicit lookup, typed privilege, self-confirmation, transient causal
eligibility candidates, distributed Field candidates, and honest explicit transition memory.

## 2. Static classifications

### Forbidden privileged structure

A mechanism is rejected from the Primary boundary when it directly uses:

```text
Assembly key
typed prediction/action/reward/memory head
evaluator target
scalar reward
semantic role or meaning
correct action or answer
```

Such mechanisms remain valid comparators.

### Invalid self-confirming mechanism

A mechanism is rejected when internally generated activity can create its own positive evidence.
External observation must remain authoritative.

### Explicit target lookup

A persistent lineage/context-keyed state that directly returns a target is classified as an
explicit lookup system, even when every identifier is anonymous.

### Explicit transition memory

Persistent state keyed by transition, path, proposal lineage, or context is reported as explicit
transition memory unless stronger evidence shows that the organization is genuinely distributed
and not table-equivalent.

This category is not automatically forbidden. SparkBrain v0.6 already contains explicit anonymous
transition state. The requirement is honest classification.

### Transient causal-eligibility candidate

A bounded, expiring, externally gated lineage trace that cannot directly return a target survives
static rejection. It remains only a candidate and must pass behavioral equivalence, lineage swap,
contradiction, and state-locus tests.

### Distributed Field candidate

A decaying distributed Field trace without direct target lookup also survives static rejection. It
must still prove causal-lineage selectivity and independent Field-side transfer. Calling a vector
“distributed” does not establish learned Field organization.

## 3. Canonical audit examples

| Mechanism | Classification | Static conclusion |
|---|---|---|
| lineage/context → next target | explicit target lookup | not emergent Field organization |
| Assembly → target | forbidden privileged structure | comparator only |
| typed action/reward heads | forbidden privileged structure | comparator only |
| internally reinforced lineage score | invalid self-confirming mechanism | reject |
| expiring externally gated lineage eligibility | transient causal-eligibility candidate | requires experiments |
| decaying Field consequence trace | distributed Field candidate | requires experiments |
| persistent local transition credit | explicit transition memory | report honestly; test equivalence |

## 4. Why a static pass is never enough

The audit deliberately never returns “emergent Field organization = true.”

A mechanism that avoids forbidden field names may still reproduce a compact explicit table
behaviorally. Therefore surviving candidates require:

1. lineage-swap selectivity;
2. matched-correlation rejection;
3. contradiction and reversal correction;
4. no internal positive commit;
5. future shared-root competition change;
6. reset/transplant localization;
7. scaling tests as physical trajectories vary while structural consequence is held fixed;
8. comparison to the smallest explicit table that reproduces the same behavior.

## 5. Smallest-equivalent-table challenge

For every proposed mechanism, construct an explicit baseline with the minimum state needed to match:

```text
input event history
lineage identity
external observation history
future trajectory selection
boundary behavior
```

Then compare:

```text
state size and locality
update locality
need for global lookup
response to identifier permutation
response to physical trajectory substitution
state transplant behavior
generalization to unseen lineage combinations
```

If the proposed mechanism and the compact table remain behaviorally and structurally equivalent,
report the mechanism as explicit memory rather than as emergent Field organization.

## 6. SparkBrain acceptance boundary

A future causal-credit mechanism may become part of SparkBrain only after it shows more than improved
test performance.

It must demonstrate that:

```text
external evidence follows actual anonymous causal lineage
credit cannot be generated internally
world changes correct the influence
future local competition changes
ambiguity can remain bounded and plural
state remains local/expiring or genuinely distributed
no target can be obtained by direct keyed query
the effect is not reducible to a smaller explicit predictor without losing behavior
```

Failure of the last condition is not an engineering failure. It is a scientific classification:
the system is an explicit anonymous predictive memory rather than the stronger Field-organized
SparkBrain hypothesis.

## 7. P5 behavioral extension

D11 static classification is now paired with P5 behavioral table-equivalence. Both the proposed
mechanism and its smallest explicit predictor must cover the complete intervention set:

```text
matched causal lineage
lineage swap
external contradiction
external absence
internal replay only
world-relation permutation
state-locus transplant
bounded ambiguity
identifier permutation
physical trajectory substitution
unseen lineage combination
```

P5 fails closed when either side omits a challenge.

The behavioral decision is intentionally asymmetric:

```text
candidate == smaller/equal established-minimal explicit predictor
    -> classify as behaviorally explicit-table-equivalent

candidate != one tested explicit predictor
    -> that tested predictor is falsified
    -> emergence is NOT established
```

The second rule is essential. Otherwise a sufficiently weak baseline would make any complicated
mechanism appear emergent. A non-equivalence result must survive progressively smaller and stronger
explicit baselines, state-locality inspection, and P1-P4 causal tests before a stronger architectural
claim can even be considered.

Anonymous IDs do not provide an exemption. A persistent lineage-keyed score or transition state that
reproduces the same behavior as a compact table remains explicit transition memory even when no
semantic names appear in runtime.

No future causal-credit mechanism has yet established P5 non-reducibility. This is an allowed
negative/underdetermined diagnostic state.

## 8. Implementation

Static D11 audit:

```text
src/sparkbrain/evaluation/v061_explicit_table_equivalence_audit.py
tests/v06/test_explicit_table_equivalence_audit.py
```

Behavioral P5 plus P3/P4 protocol:

```text
src/sparkbrain/evaluation/v061_p3_p5_diagnostic_protocol.py
tests/v06/test_p3_p5_diagnostic_protocol.py
```

These files audit descriptors and hypothetical/diagnostic observations. They do not implement a new
learning mechanism, change Primary runtime, tune thresholds, or re-execute candidate-003.
