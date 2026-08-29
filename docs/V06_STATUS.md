# SparkBrain v0.6 Status

## 1. Active programme order

Three protocol amendments are normative.

1. **Amendment 001 — Functional endogenous Sparks**  
   Missing-middle is a validity assay rather than the Primary objective.
2. **Amendment 002 — Untyped relational Dynamics**  
   Prediction, action, memory, reward, role, and meaning remain observer/evaluator projections rather
   than Primary runtime types.
3. **Amendment 003 — Relation re-entry and confirmatory order**  
   Learned anonymous relation state must alter later normal-rule Dynamics before release, and formal
   multi-world/multi-seed qualification must precede Brain Lab/release work.

The remaining execution order is:

```text
V06-12  Relation re-entry and closed-loop causal use       implemented
V06-13  Persistence-locus reset and transplant            implemented
V06-14  Supporting validity assays                        implemented
V06-15  Qualification and held-out confirmatory suite     qualification complete
V06-16  Brain Lab, taxonomy audit, reproduction, release  blocked
```

The central question is:

> Can a persistent Dynamic Field generate endogenous Sparks not directly supplied by current input,
> let them causally alter later anonymous Field and boundary states, stabilize and revise anonymous
> external relations, and let those learned relations re-enter later normal-rule Dynamics while all
> human functional categories remain observer-derived?

## 2. Runtime boundary

The Primary runtime may contain anonymous unit/path/port IDs, event timing, magnitude, polarity,
provenance, causal lineage, Field state, local-transition state, consistency state, eligibility,
queue state, and bounded execution resources.

It must not contain:

```text
Assembly state
PredictionRelation
ActionRelation
MemoryRelation
RewardRelation
FunctionalRole
MeaningState
correct action
scalar reward
outcome class
goal label
```

G3/G4/G5 comparators are isolated under `sparkbrain.baselines.v06` and must not enter the Primary
import graph.

## 3. Implemented engineering path

Implemented through V06-14:

- external/endogenous provenance and two-phase learning;
- Assembly-free runtime and observer/taxonomy guards;
- G0 queue-drain diagnostic;
- G1 anonymous local temporal expectation;
- G2 externally gated sparse transition adaptation;
- bounded normal-rule Field reinjection;
- external-authoritative reality correction;
- same-input/different-history endogenous Field Spark;
- sequential endogenous chain and causal interventions;
- anonymous Field-to-world boundary events;
- raw external feedback without reward/correct-action labels;
- external relation stabilization, reversal, and reacquisition;
- anonymous relation re-entry into later Field Dynamics;
- direct reset/transplant persistence-locus probes;
- forward missing-middle, prefix, branching, omission, retrospective, and shortcut validity assays.

## 4. Core engineering findings

### G0 remains negative

```text
intact pending queue  -> later activity
fully drained queue   -> no later activity
```

The inherited Field does not spontaneously continue after every scheduled arrival is removed.
Field-only spontaneous continuation remains unsupported.

### Level-1 candidate

The same current external input produces different normally thresholded endogenous Field Sparks after
different learned local-transition histories. No-history and no-reinjection controls produce none.

### Level-2 candidate

A cue can produce a sequential anonymous internal chain under external silence. Preserving the root
Spark while suppressing its expansion removes later Sparks; a stage-matched active intervention on a
disjoint chain leaves the target chain intact.

```text
targeted downstream impairment: 1.0
matched-random impairment:       0.0
selective effect:                1.0
```

### External relation and revision candidate

A terminal endogenous Spark reaches an anonymous outbound port and changes the raw external stream.
Returned external events stabilize an anonymous relation. Internal boundary recurrence alone cannot
strengthen it. World contingency reversal shifts relation dominance, and return of the old
contingency restores it.

### Relation re-entry candidate

The learned anonymous consistency state is projected through one category-free rule into an
`EndogenousPulseProposal`, then passes through the existing reinjection and ordinary Field threshold.
Acquired, reversed, and reacquired relations produce different later Field Sparks. Reset, unrelated,
internal-only, no-reentry, and suppression controls remove the effect.

The loop is therefore closed in the engineering construction:

```text
Brain state
  -> anonymous boundary event
  -> world
  -> raw external event
  -> anonymous consistency state
  -> relation re-entry
  -> later normal-rule Field Dynamics
```

### Persistence-locus limitation

Direct reset/transplant gives an important limiting result:

```text
G1 local-transition transplant      -> learned endogenous response transfers
G1 local-transition reset           -> learned response disappears
matched donor Field state alone     -> learned response does not transfer

boundary-consistency transplant     -> relation re-entry transfers
boundary-consistency reset          -> relation re-entry disappears
matched Field state alone           -> relation re-entry does not transfer
```

The honest current architecture description is:

```text
Dynamic Field
+ explicit anonymous local-transition memory
+ explicit anonymous external-consistency memory
+ normal-rule reinjection and boundary coupling
```

```text
explicit-state dominant candidate:       true
distributed Field persistence supported: false
```

No new persistent state may be added merely to rescue a distributed-Field interpretation of this
negative result.

## 5. V06-15 qualification result

### Matrix completeness

```text
3 development world families
× 3 seeds
× 8 conditions
× 9 evidence domains
= 648 / 648 complete unique records
```

All eight adapters share the same normalized family/seed/evidence interface.

### Strict gates

```text
Primary overall success fraction:        1.00
Primary minimum family fraction:         1.00
null false-positive fraction:            0.00
minimum targeted-minus-matched effect:   1.00
taxonomy hash match fraction:            1.00
self-confirmation violations:               0
control contract fraction:               1.00
```

A missing metric, duplicate/missing result, null-control failure, insufficient selective effect,
taxonomy mismatch, self-confirmation violation, or failed control-matching contract blocks support.

### Primary

```text
9 / 9 worlds passed
81 / 81 evidence records passed
```

### Required controls

```text
36 / 36 control worlds satisfied their contracts
324 / 324 control evidence records present
```

- no-endogenous: no later endogenous Field capability;
- readout-only: structural proposal without Field effect;
- matched-random: Primary event count, time, current, energy, and depth matched without learned
  sequential lineage;
- shuffled relation: earlier Dynamics preserved while correct relation re-entry and persistence
  transfer fail.

### G3 generic recurrent comparator

```text
9 / 9 worlds passed
81 / 81 records passed
```

A simple isolated autoregressive transition predictor reproduces the current development evidence.
The current worlds do not establish that excitable Field Dynamics are necessary.

### G4 explicit Assembly comparator

```text
9 / 9 worlds passed
81 / 81 records passed
```

An isolated system with explicit Assembly IDs and Assembly-conditioned rollout/relation state also
solves the current development worlds.

### G5 typed functional-head comparator

```text
9 / 9 worlds passed
81 / 81 records passed
```

An isolated system with explicit prediction/action/reward/memory heads and privileged scalar reward
also solves the current development worlds.

### Qualification interpretation

> Primary and all three comparators are supported in the development grid; architectural uniqueness
> is not established.

This is not a failure of the Primary implementation. It is a failure of the current development
worlds to discriminate which architecture is necessary.

## 6. Validation

The first complete-matrix run correctly failed because the comparator world specification used a
different relation-reentry gain from Primary. The shared comparator specification was changed to the
exact Primary normalization rather than weakening the equality test.

The corrected complete matrix passed GitHub Actions run `33268619204` on Python 3.11 and Python 3.13:

```text
Install: PASS
Ruff lint: PASS
Local readiness: PASS
Default test suite: PASS
Bundle validation: PASS
```

Additional accepted runs include the earlier relation-reentry, persistence-locus, validity,
Primary-only, control-only, and strict-scoring suites documented in their engineering reports.

## 7. Current manifest state

### Qualification

All eight adapter paths are qualification-ready. The manifest remains intentionally:

```text
code_ref = UNFROZEN
```

Therefore formal execution readiness remains false until a reviewed SHA is frozen.

### Held-out confirmatory

Qualification readiness is not reused. All adapters remain held-out-not-ready because the five
confirmatory world-family contracts have not been implemented and qualified.

## 8. Remaining work before release

### Held-out world contract

Implement for all eight conditions:

1. sparse identity/topology permutation;
2. lag dispersion;
3. threshold/magnitude bands;
4. genuine branch competition;
5. repeated contingency cycles.

The families must not be renamed copies of the deterministic development chain. Branch competition
must contain real simultaneous alternatives.

### Comparator fairness

Record, per world and condition:

- observed training events;
- generated internal events;
- persistent state size;
- intervention count;
- wall-clock time;
- privileged information;
- whether ordinary Field thresholds are used or bypassed.

### Freeze and confirmatory execution

After held-out adapter qualification:

```text
freeze full Git SHA
freeze manifest hash
freeze thresholds and exclusions
freeze result/artifact schema
run 5 families × 10 seeds × 8 conditions × 9 domains
= 3,600 fresh records
```

Development records cannot be relabelled as held-out evidence.

### V06-16

Only after the complete held-out result review:

- final observer/taxonomy removal and permutation audit;
- Brain Lab read-only visualization;
- local clean-room reproduction;
- claim-boundary and strongest-counterexample review;
- release decision.

## 9. Current scientific boundary

Supported only as engineering foundation/candidates:

- Assembly-free and taxonomy-guarded Primary runtime;
- closed-loop relation re-entry;
- explicit-state-dominant persistence locus;
- complete development qualification interface and strict controls;
- Primary capability in three development families;
- comparator capability in the same families.

Not yet established:

- held-out multi-world/multi-seed Level 1, 2, or 3;
- architectural uniqueness;
- distributed Field persistence;
- genuine branch-competition superiority;
- physical-trajectory causal equivalence;
- semantic meaning, concepts, autonomous value formation, organs, consciousness, or AGI.

`main` remains unchanged and PR #10 remains Draft.
