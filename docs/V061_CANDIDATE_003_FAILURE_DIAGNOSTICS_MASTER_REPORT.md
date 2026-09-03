# v0.6.1 Candidate-003 Failure Diagnostics — Master Report

## 1. Research boundary

Candidate-003 is a consumed one-way confirmatory dataset. Its 400 executions and 3,600 evidence
records are not rerun, repaired, or rescored in this diagnostic programme.

The diagnostic branch is observer/evaluator-side. It asks what the negative result means for
SparkBrain, not how to make the frozen test pass.

RV01 remains a separate research line.

## 2. Formal result retained unchanged

```text
Primary overall success:        403 / 450 = 0.8956
Primary minimum family success:  59 / 90 = 0.6556  FAIL
minimum selective effect:        0.00             FAIL
control-contract fraction:       0.98             FAIL
Primary supported:               false

G3 recurrent supported:          true
G4 Assembly-conditioned:         true
G5 typed functional heads:       true
```

Formal interpretation:

> Comparator-only success is negative for the Primary SparkBrain hypothesis under the frozen scope.

Diagnostics below refine the mechanism interpretation but do not change this decision.

## 3. Capabilities that survived the fresh confirmatory suite

Across all Primary worlds, the following remained intact:

```text
endogenous-origin
same current input / different history dependence
taxonomy and observer non-interference
external-authoritative evidence rules
```

The negative result therefore does not reduce to “SparkBrain cannot generate internal activity.”
The failure occurs when internal activity must remain organized as a stable, selective, and
world-relevant causal process.

## 4. Failure atlas

| Class | Worlds | Mechanistic description |
|---|---:|---|
| CLEAN | 30 | all nine Primary domains pass |
| L-A | 5 | main and alternate temporal trajectories co-express |
| L-B1 | 4 | temporally stable alternate trajectory excludes the world-facing main trajectory |
| L-B2 | 1 | main path is near threshold and appears only intermittently through residual Field integration |
| C0 | 4 | stored dominant relation is correct, but later Field expression abstains |
| C1 | 3 | old relation remains dominant and later expression also collapses |
| C2 | 3 | new and old relation links co-express before later hysteresis/abstention |

All 47 failed Primary evidence cells are concentrated in two families:

```text
lag dispersion:       31
contingency cycles:   16
other families:        0
```

## 5. D2 — Lag trajectory autopsy

### 5.1 Source-level mechanism

The current local expectation score combines:

```text
transition frequency
×
temporal stability derived from lag variance
```

Balanced chronological presentation correctly removed batched recency bias. However, the
schedule-to-profile mapping gives the main and alternate branches different lag-variance samples.
A less exposed alternate branch can therefore have higher G1 confidence when its assigned lag
profiles are more stable.

The reconstructed root-current/threshold ratio correctly classifies all ten lag-dispersion worlds:

```text
main ratio >= 1.0 -> L-A dual trajectory expression
main ratio <  1.0 -> L-B alternate-only expression
```

### 5.2 Meaning for SparkBrain

The local mechanism is doing what it was designed to do: prefer a temporally stable anonymous
transition. The problem is that temporal stability is not the same as later anonymous world
relevance.

## 6. D3 — Causal baseline validation

Five lag worlds have a frozen selective effect of zero. Mechanistically, their main sham trajectory
is absent before intervention.

```text
no main sham baseline
    -> targeted impairment reported as 1.0
    -> matched impairment reported as 1.0
    -> formal selective effect 0.0
```

The formal score remains valid under its preregistered definition. The diagnostic interpretation is
more specific:

> Causal selectivity cannot be inferred because the target trajectory was not expressed in the
> baseline condition.

This is not evidence that targeted and matched lesions destroyed the same healthy main process.

## 7. D4 — Relation storage and Field use

Repeated-contingency failures split into at least two distinct processes.

### Storage failure

An older anonymous relation remains dominant after the world changes.

### Expression failure

The correct relation is dominant, but its reliability/current is insufficient to cross the ordinary
Field threshold.

### Superposition

Several relation links remain sufficiently reliable to generate concurrent Field activity.

Therefore:

```text
correct relation storage
!=
proposal eligibility
!=
Field expression
!=
unique functional action
```

Calling all four stages “memory” hides the actual failure locus.

## 8. D5 — Persistence and failure locus

Existing reset/transplant evidence gives a limiting architecture description:

```text
G1 transition state transplant
    -> learned chain behavior transfers

G1 transition reset
    -> learned chain behavior disappears

anonymous consistency transplant
    -> relation re-entry transfers

anonymous consistency reset
    -> relation re-entry disappears

matched Field state alone
    -> long-lived learned effect does not transfer
```

The current demonstrated experience carriers are explicit anonymous transition and consistency
states. The Field executes, integrates, thresholds, and can contribute transient residual effects,
but distributed learned Field memory is not currently supported.

## 9. D6 — Comparator contrast

G3, G4, and G5 are diagnostic positive controls, not replacement designs.

```text
G3
    explicit transition abstraction
    physical lag process largely abstracted away

G4
    explicit Assembly identity
    trajectory boundary supplied by design

G5
    typed prediction/action/reward/memory separation
    functional decomposition supplied by design
```

Their success establishes that the frozen benchmark capabilities do not require the current
SparkBrain architecture. It does not establish that they solve the same physical event-time problem
more elegantly; in lag dispersion they avoid much of the process that destabilizes Primary.

## 10. D7–D8 — Temporal–functional decoupling

Four observer-only counterfactuals isolate the missing path.

### Lag assignment permutation

Hold constant:

```text
branch identities
exposure counts
total lag multiset
world-consistency winner
```

Permute only which branch receives the dispersed lag samples. G1 selection flips with lag ownership.

### Consequence permutation

Hold local transition observations fixed and swap observer-side world consistency. G1 selection does
not change.

### Storage/expression cross

Hold relation counts and dominant target fixed while changing only Field expression demand. Relation
storage remains the same while Spark expression changes.

### Equal-evidence ambiguity

Equal local evidence produces co-maximal branches. A singleton chosen by deterministic reporting
order is not an internally justified functional winner.

Combined causal picture:

```text
local temporal evidence
    -> G1 trajectory competition
    -> Field
    -> boundary
    -> world
    -> anonymous relation evidence
    -X-> future G1 trajectory competition
```

The crossed arrow is the central missing causal circulation.

## 11. D9 — Hypothesis discrimination

### Strongest integrative diagnosis

**Missing anonymous causal-credit circulation.** External consequences are stored downstream, but do
not reorganize the earlier local temporal lineage that produced them.

### Partially valid diagnosis

**Evaluator/ontology mismatch.** Some L-A and C2 failures are plural anonymous alternatives rather
than complete absence. However, this cannot explain L-B or C0 and cannot rescue the formal result.

### Supported benchmark conclusion

**Explicit transition abstraction is sufficient for the frozen capability suite.** This is negative
for architectural necessity.

### Currently unsupported explanation

**Distributed learned Field memory already exists.** Current transplant evidence points elsewhere.

### Rejected sufficient explanation

**Threshold or gain calibration alone.** It can change abstention or superposition, but cannot cause
world evidence to reorganize earlier trajectory competition.

### Valid unresolved outcome

**Current SparkBrain premises may be insufficient.** This must remain available if anonymous/local
credit mechanisms reduce to explicit predictors or typed reward under another name.

## 12. D10–D11 — Historical address loss and anti-table boundary

D10 separates two facts that must not be conflated:

```text
outbound BoundaryEvent
    -> still contains Spark/proposal/unit lineage

persistent anonymous consistency state
    -> does not retain the historical proposal/path return address
```

The current problem is therefore stronger than a missing update function: after consistency
compression, the system no longer represents which earlier local temporal lineage should receive a
selective consequence update.

D11 then prevents an easy but scientifically weak escape. A future mechanism is not considered a
new SparkBrain principle merely because it stores anonymous identifiers. Persistent lineage/context
state that acts as a keyed predictor is explicit transition memory; evaluator targets, scalar reward,
typed functional heads, correct actions/answers, Assembly runtime keys, and self-confirming positive
updates remain outside the Primary boundary.

## 13. Revised SparkBrain research question

The next question is not whether a threshold can be tuned to recover candidate-003.

It is:

> Can externally evidenced consequences circulate through anonymous causal lineage and reorganize
> future local trajectory competition, while remaining local, externally confirmed, reversible,
> bounded, observer-independent, and non-equivalent to a hidden explicit sequence predictor?

## 14. P1–P2 fail-closed causal-credit contracts

P1 requires exact resource matching between causal and correlated anonymous lineages. Positive
credit must follow the actual causal lineage after identity swap; external contradiction must
selectively correct it; external absence and internal replay cannot create positive credit.

P2 holds local transition state byte-identical while changing only the anonymous world relation. The
required output is a change in later shared-root competition. A changed final relation re-entry is
not sufficient.

Under the current architecture, P2 remains structurally negative: anonymous consistency can affect
relation re-entry, but there is no demonstrated path back into G1 competition.

## 15. P3 — State-locus cross-transplant

P3 separates four independently controlled state loci:

```text
L = local transition state
F = Field membrane/adaptation/trace state
C = anonymous consistency state
R = transient historical return-address state
```

Every non-transplanted locus must remain byte/hash-identical to the recipient. The protocol records
future shared-root competition separately from downstream re-entry.

Existing D5/D10 evidence maps onto this cross as:

```text
L-only
    -> demonstrated chain behavior follows explicit local transition state

F-only
    -> demonstrated long-lived learned chain effect does not follow matched carried Field state

C-only
    -> downstream relation re-entry follows consistency state
    -X-> no demonstrated upstream G1 competition transfer

R
    -> lineage exists transiently on outbound BoundaryEvent
    -> historical address is not retained by persistent consistency compression
```

P3 now supplies direct falsifiers rather than treating this localization as final:

- a valid **F-only** donor competition transfer falsifies the strong reading that the demonstrated
  learned functional effect is not already Field-distributed;
- a valid **C-only** donor competition transfer falsifies the no relation-to-G1 diagnosis;
- selective recovery of the correct historical lineage from current persistent state without a
  retained address falsifies the D10 information-loss interpretation.

R is not manufactured for retrospective v0.6.1 analysis. Adding persistent R would be a future
mechanism experiment.

## 16. P4 — Bounded ambiguity continuation

Equal local evidence can produce genuinely co-maximal trajectories. P4 therefore forbids an early
singleton from being treated as success merely because the evaluator wants one answer.

Required shape:

```text
co-maximal A + B
    -> preserve bounded plurality
    -> later independent external evidence
    -> future local competition differentiates the causally supported lineage
```

External contradiction must demote or redirect the causal lineage. External absence and internal
replay must not create positive differentiation.

This preserves the valid portion of the evaluator/ontology-mismatch hypothesis but narrows it:
plurality can be legitimate initially, yet the system must still use later world evidence to
reorganize future local competition. Under P2/D8, the current downstream-only architecture is
expected to fail this continuation requirement. That expected negative is not a tuning target.

A forced winner-take-all mechanism is therefore not assumed to be a solution; it can hide the
uncertainty without creating causal credit.

## 17. P5 — Behavioral table-equivalence

P5 extends D11 from static descriptors to behavioral reduction. Candidate and explicit baseline must
both cover the complete intervention set:

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

Missing a challenge fails closed.

For each candidate, construct the smallest explicit predictor that can consume the same admissible
history and reproduce future competition, boundary/re-entry behavior, and positive external commits.
Compare state size/locality, global keyed queries, identifier permutation, physical substitution,
transplant behavior, and unseen combinations.

The decision is deliberately asymmetric:

```text
candidate == smaller/equal established-minimal explicit predictor
    -> explicit anonymous predictive/transition memory

candidate != one tested explicit predictor
    -> that tested predictor is falsified
    -> emergent Field organization is NOT established
```

The second rule prevents a weak table baseline from manufacturing an emergence claim. Anonymous IDs,
decay, or local storage do not exempt persistent transition credit from explicit-memory
classification.

No future causal-credit mechanism has yet demonstrated P5 non-reducibility.

## 18. What has been rejected or materially weakened

The combined D1–D11 and P1–P5 record now rejects or materially weakens:

```text
threshold/gain calibration as a sufficient explanation
explicit Assembly identity as necessary
evaluator singleton mismatch as a complete explanation
current demonstrated long-lived learned effect already residing in Field state alone
anonymous consistency already closing the loop into G1
forced early winner-take-all as a required ambiguity solution
anonymous IDs being sufficient to distinguish persistent credit from an explicit table
static non-lookup source structure being sufficient to claim emergence
the current Primary already demonstrating anonymous causal-credit circulation
```

The Field-memory statement remains explicitly falsifiable by a valid future F-only transfer; it is
not a claim that distributed Field learning is impossible in principle.

## 19. What remains viable

### A. Bounded transient externally gated causal eligibility / return address

Still viable only if actual external evidence follows causal lineage through P1, changes future
competition under P2, localizes cleanly in P3, preserves bounded ambiguity in P4, and survives P5
reduction. Internal replay cannot positive-update it.

### B. Genuine distributed Field consequence trace

Still viable, but current D5 does not demonstrate it. It requires independent Field-side functional
transfer in P3 plus causal-lineage selectivity in P1 and non-reduction in P5.

### C. Joint retained-address plus local/Field update

Still viable as a mechanism class. P3 joint crosses can distinguish it from R-only, C-only, F-only,
or L-only explanations. No such mechanism is established by this diagnostic PR.

### D. Honest explicit anonymous transition memory

Still viable as an engineering and scientific architecture. If it is the smallest behavioral
explanation, it should be reported as explicit predictive memory rather than as emergent Field
organization.

### E. Negative completion

Still fully viable. If all admissible causal-credit candidates either fail P1–P4 or collapse under
P5 to compact explicit memory / privileged reward-like state, the correct result is that the current
SparkBrain premises are insufficient for the stronger claim.

## 20. Final current conclusion

> SparkBrain v0.6 formed endogenous and history-dependent activity, but its demonstrated long-lived
> organization separates into an upstream explicit local temporal-memory locus and a downstream
> anonymous consistency/re-entry locus. The Field executes physical Dynamics and can carry transient
> residual state, but current transfer evidence does not show that it alone carries the demonstrated
> learned functional bias. Externally observed consequence is not demonstrated to return to the
> historical local lineage before future shared-root competition, and the historical proposal/path
> return address is discarded by persistence. A future causal-credit mechanism must therefore pass
> causal-lineage, world-permutation, state-locus, bounded-ambiguity, and explicit-table-equivalence
> falsifiers. If the surviving mechanism is behaviorally just a compact persistent lineage-keyed
> predictor, it is explicit transition memory, not evidence for the stronger emergent-Field
> SparkBrain hypothesis.

This conclusion does not revise candidate-003, authorize threshold tuning, implement a new Primary
mechanism, or import RV01. Negative completion remains a valid endpoint.
