# v0.6.1 P3–P5 — Anonymous Causal-Credit Discrimination Protocol

## 1. Scope and fixed conclusion

This document continues the candidate-003 failure diagnosis. It does not repair v0.6.1, rerun the
formal candidate, alter Primary runtime, tune thresholds, or import RV01 results into the v0.6.1
formal interpretation.

The frozen result remains:

```text
Primary supported: false
G3 supported:      true
G4 supported:      true
G5 supported:      true
```

P3–P5 are falsification protocols for the current mechanistic diagnosis:

> anonymous external causal evidence cannot be routed selectively back to the historical local
> temporal lineage that produced it, because upstream local transition state and downstream
> consistency state remain separate and the historical proposal/path return address is compressed
> away.

A negative conclusion is a valid endpoint. No protocol below assumes that a new SparkBrain mechanism
must survive.

## 2. Starting evidence

The protocol starts from existing D5–D11 evidence, not from new candidate-003 execution.

Current observations relevant to P3–P5 are:

```text
D5: learned chain behavior transfers with explicit G1/local-transition state
D5: matched carried Field state alone does not transfer that long-lived chain behavior
D5: learned anonymous consistency state transfers relation re-entry over a fresh Field
D8/P2: changing anonymous world relation with local evidence fixed does not change G1 selection
D10: BoundaryEvent still carries proposal/Spark/unit lineage
D10: persistent consistency compression does not retain the historical proposal/path return address
D11: anonymous IDs do not exempt a persistent keyed mechanism from explicit-memory classification
```

These observations motivate the current diagnosis but do not establish the correct replacement
mechanism.

---

## 3. P3 — State-locus cross-transplant

### Question

Which state locus is causally sufficient to transfer later shared-root competition or downstream
relation re-entry?

The four independently controlled loci are:

```text
L = local transition state
F = Field membrane/adaptation/trace state
C = anonymous consistency state
R = transient historical return-address state
```

P3 treats every undeclared state difference as an invalid transplant. The intended experiment is not
"copy a runtime and see whether it works"; it is a surgical cross in which every non-transplanted
locus remains byte/hash-identical to the recipient.

### Required crosses

At minimum compare:

| Cross | Question | Diagnostic meaning |
|---|---|---|
| L only | does explicit local transition state carry future competition? | reproduces/extends D5 localization |
| F only | does Field-side state independently carry future competition? | direct falsifier of the current rejection of already-existing distributed learned Field memory |
| C only | can downstream consistency alone reorganize later local competition? | direct falsifier of the current no relation-to-G1 dependency diagnosis |
| R only | can a transient historical return address alone transfer functional bias? | tests whether addressability itself is sufficient |
| C + R | does externally confirmed consistency require a retained causal address to reach earlier competition? | tests a minimal causal-return hypothesis without prescribing an update rule |
| L + C, F + C, F + R, L + R | do effects require a joint state locus? | separates carrier from readout/update dependencies |

### Outcomes

P3 measures two outputs separately:

```text
future shared-root trajectory competition
relation re-entry / boundary-expression signature
```

A transplant that changes only final re-entry does not count as world-to-transition circulation.

### Falsifiers of the current diagnosis

The current interpretation must be revised if any of the following occurs under a valid controlled
cross:

1. **F-only transfer:** matched Field state alone transfers the donor's long-lived future competition.
   This would falsify the current strong reading that demonstrated learned functional state is not
   already Field-distributed.
2. **C-only upstream transfer:** consistency state alone transfers the donor's future G1/shared-root
   competition. This would falsify Gap 1, the claimed absence of a relation-to-G1 dependency.
3. **Persistent historical-address recovery without retained address state:** later consistency state
   reconstructs the correct historical local lineage despite no retained return address. This would
   falsify the D10 information-loss interpretation.

### What current evidence already says

Existing D5 evidence currently supports:

```text
L-only: donor chain behavior transfers
F-only: donor long-lived chain behavior does not transfer
C-only: donor relation re-entry transfers, but this has not transferred G1 competition
```

D10 says the historical R state does not survive into the persistent consistency carrier. Therefore
an R-only persistent transplant cannot be performed on the current compressed state without adding
new information. That absence is itself part of the diagnosis; manufacturing an R state for the
current Primary would be a new mechanism experiment, not a retrospective diagnostic.

The P3 implementation therefore defines the cross-transplant contract and explicit falsifiers. It
does not fabricate missing return-address state or alter Primary.

---

## 4. P4 — Bounded ambiguity continuation

### Question

Can the system preserve genuine early ambiguity and later use raw external evidence to differentiate
which anonymous causal lineage should influence future competition?

D8/E10 showed that equal local evidence can produce co-maximal candidates without an internally
justified singleton. P4 therefore rejects the assumption that a useful system must choose one winner
immediately.

### Initial condition

At least two candidate lineages begin genuinely co-maximal:

```text
lineage A strength = lineage B strength
same admissible resource class
both remain active
```

The protocol requires initial plurality to be preserved and bounded. A forced early singleton is a
failure, not a solution to ambiguity.

### Continuations

The same ambiguous start is followed by four evidence conditions:

| Evidence | Required later behavior |
|---|---|
| external match for A | later competition differentiates in favor of causally supported A |
| external contradiction for A | later competition demotes/corrects A relative to alternatives |
| external absence | no positive causal differentiation |
| internal replay only | no positive differentiation or commit |

The experiment is repeated with causal-lineage identity swapped so fixed-ID preference cannot pass.

### Falsifier of the current H4 interpretation

H4 says some frozen singleton-evaluator failures may actually be valid bounded plurality. P4 tests the
stronger requirement that plurality must remain useful over time.

If the current architecture can preserve co-maximal candidates and, with local observations otherwise
held fixed, later external evidence reorganizes their future shared-root competition, then the
current no-credit-circulation diagnosis is falsified or materially incomplete.

If it preserves plurality but only downstream re-entry changes, H4 remains only a partial evaluator
critique: early plurality may be valid, but the architecture still cannot convert later world evidence
into earlier local competition.

### Current structural expectation

Under the current v0.6.1 structure, P2/D8 predicts:

```text
co-maximal local candidates
    -> later world relation changes
    -> relation/re-entry may change
    -X-> future G1 competition changes
```

Therefore current Primary is expected to fail the continuation criterion. This expected negative is
not to be tuned away.

---

## 5. P5 — Behavioral table-equivalence

### Question

Does a proposed anonymous causal-credit mechanism do anything that the smallest explicit predictor
cannot reproduce under the same interventions?

P5 is deliberately stricter than D11 static inspection. A mechanism is not accepted as emergent
because its fields have anonymous names, because it is local, because it decays, or because it avoids
a method named `lookup`.

### Required behavioral challenge set

Candidate and explicit baseline must both be evaluated on all of:

```text
1. matched causal lineage
2. lineage swap
3. external contradiction
4. external absence
5. internal replay only
6. world-relation permutation with local state fixed
7. state-locus transplant
8. bounded ambiguity continuation
9. identifier permutation
10. physical trajectory substitution
11. unseen lineage combination
```

Missing a challenge fails closed. Static source structure cannot substitute for behavioral coverage.

### Smallest explicit baseline

For every proposed mechanism, construct the smallest explicit transition/lookup predictor that can
consume the same admissible history and reproduce:

```text
future competition signature
boundary/re-entry signature
positive external commit behavior
```

Compare at least:

```text
persistent state units
serialized state size
need for global keyed query
direct target lookup
identifier permutation
physical-trajectory substitution
state-locus transplant
unseen lineage combinations
```

### Classification rules

1. If a smaller-or-equal, established-minimal explicit predictor reproduces all required behavior,
   classify the candidate as **behaviorally explicit-table-equivalent**. Anonymous identifiers do not
   change that conclusion.
2. If the candidate uses evaluator target, correct action/answer, scalar reward, typed functional
   heads, Assembly runtime key, or equivalent privileged structure, reject it from the Primary
   boundary regardless of behavior.
3. If internal activity can create its own positive evidence, reject it as self-confirming.
4. If candidate and explicit baseline differ, the result is only:

   ```text
   tested explicit baseline falsified
   ```

   It is **not** evidence sufficient to declare emergent Field organization. A smaller alternative
   table, a different explicit state decomposition, or a hidden predictor may still reproduce the
   behavior.
5. P5 never returns `emergent Field organization = true` by itself.

### Why unseen combinations and physical substitution matter

A lineage-keyed table can look causal under the training combinations while simply memorizing
historical addresses. Identifier permutation, physical trajectory substitution, and unseen lineage
combinations force the candidate to show whether its behavior depends on local physical organization
rather than a persistent address-to-score mapping.

Even success there is only evidence against the tested compact table; it must be combined with P1–P4
and state-locality evidence before any stronger claim is considered.

---

## 6. What P3–P5 rule out now

The combined diagnostic record rejects or materially weakens the following explanations for the
candidate-003 failure:

| Claim | Status after P3–P5 protocolization |
|---|---|
| threshold/gain calibration is the sufficient repair | rejected by D9; P3–P5 do not reopen it |
| explicit Assembly identity is necessary | rejected as necessary by comparator evidence |
| evaluator singleton mismatch explains the whole negative result | rejected; P4 accepts plurality but still requires later causal differentiation |
| current learned Field state already carries the demonstrated long-lived functional bias | unsupported / partly falsified by D5 F-only transfer result; P3 defines a direct future falsifier |
| anonymous consistency already closes the loop into G1 | rejected for current architecture by D8/P2; P3 C-only is the direct falsifier |
| forced early winner-take-all is required to solve ambiguity | rejected as a protocol assumption; P4 requires bounded initial plurality |
| anonymous identifiers make persistent transition credit non-table-like | rejected; P5 classifies by behavior and state, not naming |
| avoiding an explicit `lookup` call is enough to establish emergence | rejected; P5 requires behavioral non-reduction and still never proves emergence alone |
| current architecture already contains anonymous causal-credit circulation | not supported; present evidence points to a downstream-only loop |

---

## 7. What remains viable

The following remain hypotheses, not accepted mechanisms:

### A. Bounded transient causal eligibility / return address

A short-lived, externally gated historical lineage trace may be sufficient to route consequence back
without becoming persistent target memory. It remains viable only if it:

```text
passes P1 lineage swap and contradiction
passes P2 world-to-future-competition circulation
localizes under P3 without hidden state
preserves bounded ambiguity under P4
survives P5 smallest-table reduction
cannot positive-update from internal replay
```

### B. Genuine distributed Field consequence trace

A decaying Field-side consequence trace remains possible, but current D5 evidence does not show it.
It must independently transfer functional bias in P3 and still follow actual causal lineage under P1.
Calling a state vector distributed is not sufficient.

### C. Joint causal-return mechanism

A mechanism may require both retained causal addressability and a local/Field update process. P3 joint
crosses can distinguish this from R-only, C-only, or F-only explanations. No such mechanism is
established here.

### D. Honest explicit anonymous transition memory

An explicit local transition predictor may remain a scientifically useful architecture. If it is the
smallest behaviorally equivalent explanation, the correct result is to classify it as explicit
anonymous predictive memory rather than emergent Field organization.

### E. Negative completion

H7 remains fully viable:

> the current SparkBrain premises may be insufficient to circulate anonymous causal evidence without
> adding state that is behaviorally just an explicit predictor or a privileged reward-like channel.

If all admissible causal-credit candidates either fail P1–P4 or reduce to compact explicit memory in
P5, that is a valid research conclusion rather than a request for another tuning cycle.

---

## 8. Updated strongest diagnosis

The strongest statement supported by the current evidence is now narrower and more falsifiable:

> The v0.6.1 Primary contains an upstream explicit local temporal-memory locus and a downstream
> anonymous consistency/re-entry locus, but no demonstrated causal carrier that returns externally
> observed consequence to the historical local lineage before future shared-root competition. The
> historical proposal/path return address is lost during persistence. Any future mechanism that
> restores this circulation must survive lineage swap, contradiction, cross-transplant, bounded
> ambiguity, and behavioral table-equivalence tests. If the surviving state reduces to a compact
> persistent lineage-keyed predictor, it must be reported as explicit transition memory rather than
> emergent Field organization.

This statement is falsified by controlled evidence that the current or a future admissible
non-privileged state locus independently carries externally differentiated causal history into future
local competition while resisting a smaller explicit predictor across the full P5 challenge set.

## 9. Implementation

```text
src/sparkbrain/evaluation/v061_p3_p5_diagnostic_protocol.py
tests/v06/test_p3_p5_diagnostic_protocol.py
```

The implementation contains protocol validators and assessments only. It does not implement a new
learning rule, modify Primary runtime, execute candidate-003, change thresholds, or consume RV01
results.
