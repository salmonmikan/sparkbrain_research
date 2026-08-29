# SparkBrain v0.6 Experiment Protocol
## Amended Foundation Preregistration for Functional Endogenous Sparks

## Frozen baseline

- source: `main@03a5c662a5ea100fac3288b6aa3e82c1d41f0546`;
- v0.5 artifacts, claims, and negative findings remain immutable;
- v0.6 uses a separate namespace and additive checkpoint schema;
- Protocol Amendment 001 was adopted before confirmatory v0.6 Gate evaluation;
- the pre-amendment protocol remains in Git history.

Normative amendment:

```text
docs/V06_PROTOCOL_AMENDMENT_001_ENDOGENOUS_SPARK_FUNCTION.md
```

## Revised primary question

> Can the persistent Dynamic Field generate endogenous Sparks that are not direct copies of current
> external input, let them causally participate in later internal Dynamics, prediction, action, and
> memory, and form stable externally correctable functional relations without an explicit Assembly
> or semantic unit in runtime?

Missing-middle is one validity assay and is not the sole Primary Goal.

## Primary architecture order

```text
G0  Field-only spontaneous continuation       Primary
G1  local temporal expectation traces         Primary
G2  sparse/local transition adaptation        Primary
G3  generic recurrent predictor               Comparator
G4  explicit Assembly-conditioned predictor   Comparator
```

G3-only success means the external predictor supplied the function. G4-only success means explicit
Assembly memory was useful and the observer-only hypothesis was not supported.

## Required distinctions

Every experiment must separate:

- external observation from endogenous prediction;
- internally originated activity from copied input, fixed-delay echo, queue replay, and random pulse;
- current external input from persistent internal-state effects;
- an endogenous event from its downstream causal participation;
- a stable functional relation from a human semantic label;
- eligibility creation from externally confirmed learning commit;
- observer description from runtime computation;
- forward completion before a future cue from retrospective reconstruction;
- readout-only prediction from normal-rule Field reinjection;
- G0/G1/G2 Primary mechanisms from G3/G4 comparators.

## Endogenous Spark evidence levels

### L1 — Endogenous origin

A Spark is internally originated. This is insufficient by itself.

### L2 — Predictive validity

The Spark precedes and predicts a later Field or external event better than matched controls.

### L3 — Functional relation

The Spark or lineage changes later Dynamics, prediction, action, or memory; forms an externally
confirmed stable relation; remains correctable; and has selective causal effects under intervention.

The confirmatory programme targets L3.

## Amended experiment families

### E06-0 Internal-Noise and Direct-Echo Null

Run externally silent, random-pulse, copied-target, fixed-delay echo, pending-queue, and
frequency-only controls.

Measure:

- endogenous event rate;
- direct-copy rate;
- queue dependency;
- false relation formation;
- internal-only confidence growth;
- bounded termination.

### E06-1 Internally Originated Non-Copy Spark

Supply a controlled external prefix, then determine whether the Field produces an endogenous Spark
at a target/time not directly supplied by the current input.

Required exclusions:

- same-target immediate copy;
- fixed-delay echo;
- retained scheduled event;
- evaluator-specified target;
- random-noise coincidence.

### E06-2 Persistent-State Dependence

Present the same current external pulse to Fields with different valid histories while matching
current visible input and runtime budgets.

Primary question:

```text
Does prior Field state change the endogenous response?
```

Controls:

- history reset;
- trace reset;
- local-transition reset;
- queue reset;
- shuffled history;
- identical-state replay.

### E06-3 Autonomous Endogenous Chain

After a first endogenous Spark, allow bounded external silence and test whether it causally produces
later endogenous Sparks or Cascades through normal Field rules.

Measure:

- chain depth;
- later-event precision;
- branch count;
- energy use;
- false-chain rate;
- queue-replay dependence;
- effect of suppressing the root event.

### E06-4 Prediction Participation

Compare prediction with and without the endogenous event or responsible path.

The target is raw Field or external event/time/polarity, not a human outcome label.

### E06-5 Action Participation

Expose primitive action channels whose external effects are initially unknown to the runtime.
Determine whether an endogenous Spark changes action probability or choice and whether later
external consequences confirm or contradict that relation.

Controls:

- no endogenous event;
- random endogenous event;
- action-shuffle;
- consequence-shuffle;
- readout-only;
- matched action cost.

### E06-6 Memory Participation

Determine whether an endogenous event changes an eligibility, externally committed transition,
persistent trace, or later recall-like response.

An internal event alone must not commit a positive update.

### E06-7 External Confirmation and Contradiction

Match, contradict, or expire live pending endogenous chains. Measure cancellation, external
following, path recalibration, and self-confirmation violations.

### E06-8 Functional-Relation Revision

After a stable Spark-to-consequence or Spark-to-action relation is acquired, reverse the external
contingency.

Measure:

- change detection;
- relation revision latency;
- stale action or prediction;
- unnecessary revision in stable controls;
- recovery if the old rule returns;
- catastrophic overwrite.

### E06-9 Causal Endogenous-Path Intervention

Intervene on:

- the endogenous root event;
- local temporal trace;
- transition path;
- Field-state projection;
- queue branch;
- reinjection path;
- downstream eligibility or action-bias path.

Compare targeted, matched-random, and sham intervention. Assembly overlap is described only after
measuring the functional effect.

### E06-10 Physical-Trajectory Functional Equivalence

Create or observe physically different Spark trajectories. Determine post-hoc whether they have
matched causal relations to later prediction, action, memory, external consequence, and correction.

Surface or Assembly similarity alone cannot establish equivalence.

This is an observer-level scientific analysis and does not feed a role label into runtime.

### E06-11 Missing-Middle Validity Assay

Test `A → B → [C omitted] → D_external`.

C counts as forward completion only when:

```text
created_at(C_endogenous) < arrival_at(D_external)
```

Retrospective reconstruction after D is reported separately. Passing this assay alone does not pass
L3 or the full v0.6 programme.

### E06-12 Memory Component Reset and Transplant

Reset or transplant one of:

- weight/delay;
- threshold/adaptation;
- persistent trace;
- local transition state;
- externally gated relation state;
- endogenous queue.

Determine which component carries experience-dependent endogenous behaviour.

### E06-13 Observer and Self-Confirmation Adversarial Suite

Required attacks:

- observer ON/OFF;
- observer mutation attempt;
- internal-only recurrence;
- endogenous event counted as external;
- evaluator target leakage;
- action/outcome label leakage;
- pending queue shortcut;
- G3/G4 hidden-path shortcut;
- generation-depth runaway.

## Revised core Gate order

1. **Gate A — Runtime integrity and observer independence**
2. **Gate B — Endogenous origin and non-copy**
3. **Gate C — Persistent-state dependence**
4. **Gate D — Autonomous internal continuation**
5. **Gate E — Causal downstream participation**
6. **Gate F — Functional relation acquisition**
7. **Gate G — External correction and revision**
8. **Gate H — Memory-locus and relation stability**

Missing-middle results are reported under E06-11 and contribute supporting evidence to Gates B–G,
but they are not a standalone required definition of success.

## Gate A — Runtime integrity and observer independence

- local deterministic reference;
- provenance and checkpoint integrity;
- forbidden-field audit;
- observer ON/OFF equality;
- zero self-confirmation violations.

## Gate B — Endogenous origin and non-copy

- internally originated Spark;
- no direct current-input copy;
- no fixed-delay echo explanation;
- no pending-queue explanation;
- no evaluator target;
- false-generation ceiling under null controls.

## Gate C — Persistent-state dependence

- identical current external input produces history-appropriate differences;
- identical full runtime state reproduces identical response;
- removing candidate memory state reduces the history effect.

## Gate D — Autonomous internal continuation

- endogenous root changes later internal activity under silence;
- later activity exceeds queue replay and matched random controls;
- bounded safety constraints remain active.

## Gate E — Causal downstream participation

- targeted root/path intervention changes later Dynamics, prediction, action, or memory;
- targeted effect exceeds matched random and sham;
- collateral damage remains bounded.

## Gate F — Functional relation acquisition

- externally confirmed Spark relations improve held-out prediction, action, or memory;
- internal-only recurrence does not increase relation confidence;
- frequency, surface, readout-only, and no-endogenous controls are exceeded;
- no human semantic label enters runtime.

## Gate G — External correction and revision

- contradiction cancels or redirects stale paths;
- the external event remains authoritative;
- reversal updates behaviour without requiring unconditional full reset;
- stable controls avoid excessive revision.

## Gate H — Memory-locus and relation stability

- reset/transplant identifies at least one candidate experience carrier;
- functional relations persist across held-out conditions;
- physically different trajectories may be grouped only by matched causal relations;
- hidden evaluator or external-predictor memory is excluded.

## Confirmatory reporting rules

- report L1, L2, and L3 separately;
- report each causal effect with matched random and sham controls;
- report null and negative results as first-class artifacts;
- report missing-middle separately from the full functional programme;
- do not call an internal event meaningful because it recurs;
- do not call a relation semantic because it changes an action;
- preserve raw runtime trace and evaluator metadata separately;
- cite Protocol Amendment 001 in every confirmatory report.

## Current implementation boundary

V06-00–V06-06 implement provenance, observer isolation, G0 diagnostic, G1 local expectation, G2
external-confirmation-gated local adaptation, and normal-rule reinjection. They do not yet establish
L2 or L3, live external correction, autonomous endogenous chains, functional relations,
missing-middle completion, or memory location.
