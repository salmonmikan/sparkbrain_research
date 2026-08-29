# SparkBrain v0.6 Protocol Amendment 003
## Relation Re-entry, Persistence Locus, and Confirmatory Order

**Amendment date:** 2026-08-29  
**Branch:** `v06`  
**Adopted after:** V06-11 single-world relation-revision engineering candidate  
**Adopted before:** persistence-locus, validity-assay, and confirmatory Gate evaluation  
**Preserves:** all V06-00–V06-11 code, artifacts, negative results, and claim boundaries

## 1. Reason for the amendment

V06-09–V06-11 established the shape of a closed world-facing relation:

```text
endogenous Spark
    -> later anonymous internal Sparks
    -> anonymous outbound boundary event
    -> raw external event
    -> externally gated anonymous relation state
    -> relation revision after world contingency change
```

However, the revised `AnonymousLinkState.reliability` is currently read by evaluators and reports; it
has not yet been shown to alter a later Field trajectory or boundary event. The system can therefore
record that the world changed without yet using that experience in later Dynamics.

A second unresolved problem is evidential scale. Current Level-1, Level-2, and Level-3 results are
single-world engineering candidates. The existing work order did not contain a distinct mandatory
multi-world, multi-seed, held-out confirmatory package before release.

This amendment makes both gaps explicit release blockers.

## 2. Revised central closed-loop requirement

The required loop is:

```text
B_t
  -> anonymous boundary event
  -> raw world transition
  -> external consistency / contradiction
  -> existing anonymous relation state changes
  -> relation state re-enters normal Field Dynamics
  -> B_(t+k) changes
```

Formally, for an externally learned relation state `L_t`, v0.6 must test whether:

\[
B_{t+1}=F(B_t,E_t,L_t)
\]

and whether a controlled intervention on `L_t` changes later anonymous Field or boundary events:

\[
Trace(do(L_t=L_a)) \neq Trace(do(L_t=L_b))
\]

The effect must exceed no-re-entry, reset, sham, and matched-unrelated controls.

## 3. Relation re-entry must reuse existing state

The Primary implementation must not solve this gap by introducing another semantic state machine.
Relation re-entry must initially be a read-only projection of existing anonymous consistency state
through existing normal Field mechanisms.

Permitted reference path:

```text
existing anonymous link reliability
        ↓
category-free local magnitude / confidence
        ↓
EndogenousPulseProposal
        ↓
existing FieldReinjectionGate
        ↓
ordinary membrane / threshold / refractory / adaptation
        ↓
later anonymous Field Spark or no Spark
```

The projection may use only existing structural values such as port ID, anonymous external target,
polarity, lag, magnitude ratio, reliability, causal parentage, and generation budget.

It must not introduce:

```text
good / bad
reward / punishment
correct action
preferred action
prediction role
memory role
functional role
meaning
```

All eligible anonymous links are projected through the same rule. The Primary runtime must not ask an
evaluator which link should win. Competition should arise from relation strength, Field threshold,
inhibition, and ordinary Dynamics.

## 4. Stronger Gate G

Gate G is not passed merely because relation counters change after a world reversal.

Gate G now requires all of the following:

1. world contingency reversal changes existing anonymous relation state;
2. the changed relation state alters a later Field or boundary trace;
3. resetting the relation state removes that altered behaviour;
4. a matched unrelated relation-state change does not reproduce the target effect;
5. returning the old world contingency restores both relation dominance and the corresponding later
   Dynamics;
6. internal-only recurrence cannot create the same change;
7. no scalar reward, correct-action target, or evaluator label directs the re-entry.

A relation-state update without later causal use remains an engineering memory record, not a closed
SparkBrain world loop.

## 5. Persistence-locus priority

After the first relation re-entry result, the next priority is not more functionality. It is to expose
where the demonstrated effects are stored.

The persistence-locus suite must reset and transplant at least:

- current Field membrane/residual state;
- threshold and adaptation state;
- weight and delay state;
- G1 local transition state;
- G2 path adaptation and eligibility state;
- pending endogenous queue state;
- anonymous boundary consistency state;
- relation re-entry working state, if any;
- combinations of the above.

For each component, test:

```text
necessity:
reset component -> does the learned effect disappear?

partial sufficiency:
transplant component -> does the learned effect move?

interaction:
component A alone versus A+B versus full-state transplant
```

A result in which all experience-dependent behaviour disappears with G1/local-transition and
consistency reset, and transfers with those explicit states, must be reported plainly as:

> The current architecture is principally a Dynamic Field plus explicit anonymous transition and
> consistency memory.

That is an important possible negative or limiting result, not a failure to report.

## 6. Revised work order

The unimplemented work packages are renumbered because V06-12–V06-14 had not yet been executed.

```text
V06-12  Relation Re-entry and closed-loop causal use
V06-13  Persistence-locus reset and transplant
V06-14  Validity assays
V06-15  Confirmatory generalization and comparator suite
V06-16  Brain Lab, taxonomy audit, reproduction, and release review
```

### V06-12 — Relation Re-entry

Demonstrate that externally gated anonymous relation state changes later normal-rule Field Dynamics
or anonymous boundary events. Include relation-reset, no-re-entry, matched-unrelated, internal-only,
reversal, and reacquisition controls.

### V06-13 — Persistence locus

Determine which state components are necessary, partially sufficient, distributed, or unresolved for:

- same-input/different-history endogenous Sparks;
- autonomous chain continuation;
- boundary/world coupling;
- anonymous relation stabilization;
- relation revision;
- relation re-entry.

### V06-14 — Validity assays

Run missing-middle, prefix continuation, branching, omission, retrospective inference, noise,
fixed-delay echo, and queue-drain diagnostics as supporting assays. Missing-middle remains one test,
not the project definition.

### V06-15 — Confirmatory generalization and comparators

Freeze code, metrics, thresholds, world generators, and exclusions before confirmatory execution.
Run at minimum:

```text
engineering qualification: 3 world families × 3 seeds
confirmatory suite:         5 held-out world families × 10 seeds
```

If a mechanism is fully deterministic, seeds must still alter preregistered structural or timing
perturbations rather than repeat byte-identical worlds.

Every confirmatory family must cover as applicable:

- endogenous origin;
- same-input/different-state response;
- autonomous causal chain;
- boundary effect;
- external relation stabilization;
- reversal and reacquisition;
- relation re-entry;
- persistence-locus intervention;
- taxonomy/observer non-interference.

Required matched controls and comparators:

- no endogenous generation;
- random endogenous events with matched count/energy/time;
- readout-only without Field reinjection;
- shuffled relation state;
- G3 generic recurrent predictor;
- G4 explicit Assembly-conditioned predictor;
- G5 typed functional-head system.

Report per-world, per-seed, aggregate, failure, and strongest-counterexample artifacts. Comparator-only
success is a negative result for the Primary hypothesis.

### V06-16 — Brain Lab, audit, and release

Only after V06-12–V06-15 review:

- visualize raw Field, provenance, causal lineages, boundary events, relation state, re-entry, reset,
  transplant, and observer projections;
- prove observer/evaluator/taxonomy non-interference on frozen runs;
- provide local reproduction scripts and artifact manifests;
- conduct claim-boundary and release review;
- keep the PR Draft until all release blockers are resolved or explicitly closed as negative results.

## 7. New release blockers

`main` merge and v0.6 release are blocked when any of the following remains true:

- anonymous relation state does not alter later Dynamics;
- relation re-entry works only with reward, correct-action, or evaluator labels;
- persistence locus is untested;
- confirmatory multi-world/multi-seed results are absent;
- G3/G4/G5 comparators are absent from final interpretation;
- observer/taxonomy removal changes runtime;
- internal-only activity can positively confirm itself;
- the strongest negative result or counterexample is omitted.

## 8. State-growth restriction

From this amendment onward, new persistent learned-state categories require explicit protocol review.
V06-12 should reuse existing transition, consistency, eligibility, Field, and queue state. New records
for provenance, immutable measurement, or intervention audit are allowed; new semantic or typed
cognitive state machines are not.

## 9. Scientific interpretation

Possible outcomes include:

### Outcome A — Relation re-entry succeeds and is distributed

Several Field/transition/consistency components jointly carry the learned effect. This supports a
closed, distributed dynamic loop candidate.

### Outcome B — Relation re-entry succeeds but explicit states carry everything

G1/local-transition and consistency state are necessary and sufficient for the effect. This supports
a useful architecture but limits the claim to a Dynamic Field plus explicit anonymous memory.

### Outcome C — Relation state revises but cannot affect later Dynamics

The current Level-3 candidate is downgraded: v0.6 records external relations but does not functionally
use them.

### Outcome D — Only G3/G4/G5 succeeds confirmatorily

The Primary SparkBrain mechanism is not supported for the tested worlds. The comparator result must
be reported without reinterpretation as Primary success.

## 10. Claim boundary

Until V06-12 relation re-entry, V06-13 persistence locus, and V06-15 confirmatory execution pass, the
strongest permitted description remains:

> Single-world engineering candidates exist for endogenous origin, anonymous causal continuation,
> external boundary coupling, and revisable anonymous relation state.

The phrase "closed functional endogenous loop" is not permitted before relation re-entry changes later
Dynamics under intervention.