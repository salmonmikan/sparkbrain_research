# v0.6.1 Failure Diagnostics — Current Status

## Role of this branch

This branch analyzes the complete negative candidate-003 result from the SparkBrain hypothesis.
It does not reopen candidate-003, tune frozen thresholds, alter Primary runtime, or attempt to
maximize test pass counts. RV01 remains an independent research line.

The formal result is fixed:

```text
Primary supported: false
G3 supported:      true
G4 supported:      true
G5 supported:      true
```

## Completed diagnostic layers

| Stage | Question | Current result |
|---|---|---|
| D1 | Which worlds fail and how? | 30 clean; lag and contingency failures split into seven mechanistic classes |
| D2 | Why does lag dispersion change trajectory expression? | branch-specific lag variance changes G1 confidence and can defeat the more exposed world-facing branch |
| D3 | What does zero selectivity mean? | five worlds lack a valid main sham baseline; the frozen zero remains valid, but mechanism diagnosis is baseline absence |
| D4 | Is repeated-contingency failure storage or use? | both; correct storage may abstain, old storage may dominate, and several links may co-express |
| D5 | Where do learned effects persist? | chain follows explicit G1 transition state; re-entry follows explicit consistency state; matched Field state alone does not carry the demonstrated long-lived effect |
| D6 | What do comparator successes mean? | explicit abstractions solve the benchmark; they do not establish the same physical-time processing advantage |
| D7 | Are temporal stability and world relevance coupled? | no; observer-only counterfactuals separate them |
| D8 | Which variables causally control the diagnosis? | lag ownership flips G1 selection; world-relation permutation leaves current G1 selection unchanged; storage and expression are separable |
| D9 | Which explanations remain viable? | missing anonymous causal-credit circulation is strongest; threshold-only repair and Assembly necessity are rejected; negative completion remains viable |
| D10 | Where is the causal return address lost? | outbound BoundaryEvent contains lineage, but consistency compression does not retain proposal/path return address |
| D11 | How do we prevent a hidden table from being called emergence? | explicit-target, typed, Assembly, self-confirming, transient-eligibility, distributed-trace, and explicit-transition classes are separated |

## Completed falsification protocols

| Protocol | Question | Current diagnostic status |
|---|---|---|
| P1 | Does credit follow actual causal lineage rather than matched correlation? | fail-closed lineage-swap, contradiction, absence, and internal-replay contracts implemented; no future mechanism has yet passed them |
| P2 | Does changed anonymous world relation reorganize future local competition with local state fixed? | current architecture is structurally negative: relation/re-entry may change while G1 competition remains unchanged |
| P3 | Which state locus transfers competition or re-entry? | cross-transplant contract implemented; existing D5 evidence localizes chain behavior to explicit local-transition state and re-entry to consistency state; Field-only long-lived transfer is not observed; historical return-address state is unavailable after current compression |
| P4 | Can genuine early ambiguity remain plural and later be differentiated by external causal evidence? | bounded-plural continuation contract implemented; forced early singleton is rejected as an assumption; current downstream-only structure is expected to fail later competition differentiation under P2/D8 |
| P5 | Is a proposed anonymous mechanism behaviorally reducible to a compact explicit predictor? | full behavioral challenge and fail-closed table comparison implemented; no proposed future mechanism has established non-equivalence; failure to match one table never proves emergence |

P3–P5 are diagnostic/evaluator mechanisms only. They do not implement a new learning rule or execute
candidate-003.

## Current mechanistic picture

```text
anonymous local transition evidence
    -> G1 frequency × temporal-stability score
    -> shared-root trajectory expression
    -> Field integration and threshold
    -> outbound BoundaryEvent
       [Spark/proposal/unit lineage still present]
    -> PendingBoundaryExposure / AnonymousLinkState
       [historical proposal/path return address compressed away]
    -> anonymous relation reliability
    -> relation re-entry
    -> later Field Spark
```

Two distinct gaps remain supported.

### Gap 1 — No demonstrated relation-to-G1 dependency

Anonymous consistency and relation re-entry do not call or update the G1 local transition-learning
path. Changing later world relation while local evidence remains fixed therefore cannot reorganize
the earlier trajectory competition in the current architecture.

P3 makes this falsifiable: a valid consistency-only transplant that transfers donor future
competition would directly refute this gap.

### Gap 2 — Historical causal return address is lost

Even if a future update call were added, the current stored relation does not identify which
historical local proposal/path lineage produced the externally confirmed boundary event. The system
cannot apply selective external evidence to the original cause after that compression.

P3 makes the stronger claim falsifiable: if the historical lineage can be recovered selectively from
current persistent state without retained return-address information, the D10 information-loss
interpretation must be revised.

## P3 state-locus interpretation

The state loci are now separated as:

```text
L = explicit local transition state
F = Field membrane/adaptation/trace state
C = anonymous consistency state
R = transient historical return address
```

Existing evidence currently supports:

```text
L-only -> demonstrated chain/competition behavior follows explicit local transition state
F-only -> demonstrated long-lived learned chain behavior does not follow carried Field state alone
C-only -> downstream relation re-entry follows consistency state
C-only -X-> no demonstrated transfer into upstream G1 competition
R      -> outbound lineage exists transiently, but the historical address is not retained in
          persistent consistency state and therefore cannot be honestly transplanted retrospectively
```

This narrows, but does not solve, the mechanism problem. In particular, a future F-only transfer is a
direct falsifier of the current rejection of already-present distributed learned Field memory, and a
future C-only upstream transfer is a direct falsifier of Gap 1.

## P4 bounded ambiguity interpretation

Equal local evidence can produce co-maximal candidates without an internally justified singleton.
P4 therefore requires:

```text
co-maximal A + B
    -> bounded plurality retained initially
    -> later independent external evidence
    -> future competition differentiates the causally supported lineage
```

A forced early winner-take-all choice fails the protocol because it hides rather than resolves the
uncertainty. External absence and internal replay must not create positive differentiation.

This sharpens the evaluator-mismatch hypothesis: some frozen plural-output failures may represent
legitimate ambiguity, but that cannot explain the full negative result unless later world evidence
can causally reorganize future local competition. Current P2/D8 evidence says it does not.

## P5 behavioral table-equivalence interpretation

Static naming is no longer sufficient. Candidate and smallest explicit baseline must be compared on
all of:

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

If a smaller-or-equal established-minimal explicit predictor reproduces the candidate on this full
challenge set, the candidate is classified as explicit anonymous predictive/transition memory.
Anonymous IDs, decay, local storage, or the absence of a method named `lookup` do not change that
classification.

Conversely, a mismatch with one explicit baseline only falsifies that tested baseline. P5 never
returns `emergent Field organization = true` by itself.

## Updated strongest SparkBrain diagnosis

> The v0.6.1 Primary contains an upstream explicit local temporal-memory locus and a downstream
> anonymous consistency/re-entry locus, but no demonstrated causal carrier that returns externally
> observed consequence to the historical local lineage before future shared-root competition. The
> historical proposal/path return address is lost during persistence. Any future mechanism that
> restores this circulation must survive lineage swap, contradiction, cross-transplant, bounded
> ambiguity, and behavioral table-equivalence tests. If the surviving state reduces to a compact
> persistent lineage-keyed predictor, it must be reported as explicit transition memory rather than
> emergent Field organization.

This is narrower than saying that an eligibility trace is missing. P3–P5 deliberately leave open
multiple mechanisms and a valid negative completion.

## What is now rejected or materially weakened

```text
threshold/gain calibration as a sufficient explanation
explicit Assembly identity as necessary
evaluator singleton mismatch as a complete explanation
current demonstrated long-lived learned effect already residing in Field state alone
anonymous consistency already closing the loop into G1
forced early winner-take-all as a required ambiguity solution
anonymous IDs being sufficient to make persistent credit non-table-like
static source inspection being sufficient to claim emergence
the current architecture already demonstrating anonymous causal-credit circulation
```

## What remains viable

```text
bounded transient externally gated causal eligibility / return-address trace
    only if it passes P1-P5 and cannot self-confirm

genuinely distributed decaying Field consequence trace
    only if P3 shows independent Field-side functional transfer and P1 shows causal selectivity

joint retained-address + local/Field update mechanism
    not yet demonstrated; P3 joint crosses are intended to localize it

honest explicit anonymous transition memory
    scientifically valid if that is the smallest behavioral explanation, but not the stronger
    emergent-Field claim

negative completion (H7)
    current SparkBrain premises may be insufficient if all admissible mechanisms either fail P1-P4
    or reduce to compact explicit memory in P5
```

## Decision point

No new SparkBrain mechanism is justified merely because it could improve the frozen lag or
contingency scores. Before implementation, a proposed mechanism needs a predeclared P1–P5 mapping and
an explicit smallest-table baseline.

If no candidate can satisfy those constraints without becoming typed reward, evaluator privilege,
self-confirmation, Assembly-keyed prediction, or compact persistent transition lookup, the correct
research outcome is negative completion rather than another tuning cycle.

## Claim boundary

The formal candidate-003 result remains unchanged: Primary is unsupported under the frozen scope and
all three comparators are supported. P1–P5 refine and falsify mechanism interpretations only; they do
not revise the frozen decision, rerun formal evidence, or mix RV01 into v0.6.1.
