# SparkBrain v0.6 Master Plan
## Untyped Functional Endogenous Dynamics in an Assembly-Free Field

**Baseline:** `main@03a5c662a5ea100fac3288b6aa3e82c1d41f0546`  
**Target:** `0.6.0.dev0`  
**Environment:** local CPU reference; no required cloud runtime, external LLM API, or dedicated
neuromorphic hardware.  
**Normative amendments:**

1. `docs/V06_PROTOCOL_AMENDMENT_001_ENDOGENOUS_SPARK_FUNCTION.md`
2. `docs/V06_PROTOCOL_AMENDMENT_002_UNTYPED_RELATIONAL_DYNAMICS.md`

## 1. Destination

v0.6 asks whether an already running Dynamic Field can generate an internal Spark not directly
supplied by the current external input and then use that Spark as causal material for later Dynamics.
It does not predeclare what kind of function the Spark has.

```text
world-to-field event
        ↓
persistent Dynamic Field
        ↓
endogenous Spark X
        ↓
later anonymous Field state / internal event / outbound boundary event
        ↓
changed external event stream
        ↓
external consistency, contradiction, or revision of the responsible path
```

The Primary runtime contains no explicit Assembly and no predeclared Prediction, Action, Memory,
Reward, Role, or Meaning relation type.

```text
immutable runtime trace
        ↓
──────────────── Observer Boundary ────────────────
        ↓
post-hoc trajectory / Assembly / causal-relation analysis
        ↓
optional predictive / boundary-effect / persistence / world-coupling views
```

The revised central question is:

> Can a persistent Dynamic Field generate endogenous Sparks not directly supplied by current input,
> let them causally alter later anonymous Field states and boundary-crossing events, and stabilize or
> revise those relations through external interaction, while prediction, action, memory, reward,
> role, and meaning remain observer-derived descriptions rather than runtime types?

Missing-middle completion remains one validity assay. It is not the definition of v0.6.

## 2. Core distinction: runtime ontology versus evaluation taxonomy

### 2.1 Primary runtime ontology

The runtime is permitted to know only execution-relevant structure:

- anonymous unit, channel, region, and boundary-port IDs;
- event time, magnitude, polarity, and duration;
- external-in, endogenous, and field-to-world boundary direction;
- causal parent and local path IDs;
- membrane, threshold, refractory, adaptation, and persistent traces;
- lag statistics and signed local influence;
- eligibility and external consistency state;
- bounded confidence or reliability of an anonymous transition;
- generation energy, depth, lifetime, and branch budgets.

These values describe where, when, and how a transition occurred. They do not describe what it
means.

### 2.2 Observer/evaluator taxonomy

The observer may later ask:

- did X precede and improve estimation of a later event?;
- did X alter an outbound boundary-port event?;
- did X leave a delayed persistent state effect?;
- did an outbound event alter the later external stream?;
- did contradiction revise the responsible path?;

Humans may call these predictive, action-related, memory-related, world-coupled, or corrective effects.
Those names are evaluation views, not runtime classes.

### 2.3 Forbidden reification

The Primary runtime must not contain or infer a one-hot class such as:

```text
PredictionRelation
ActionRelation
RewardRelation
MemoryRelation
FunctionalRole
MeaningState
```

Nor may it contain a dedicated prediction, action, memory, reward, goal, or semantic head on the
Primary path.

One internal lineage may satisfy several observer views simultaneously. It is not forced into one
functional category.

## 3. Meaning is a post-hoc relation candidate, not a value

The following remains prohibited:

```text
spark.meaning = "danger"
spark.semantic_state = "food"
spark.role_type = "prediction"
```

The runtime may embody only generic local causal structure:

\[
U(i,j)=
\left(
source_i,
 target_j,
 \Delta t,
 signed\ influence,
 reliability,
 provenance,
 external\ consistency
\right)
\]

An observer may later estimate a wider relation signature:

\[
R_X=
\left\{
X \rightarrow Y_k,
\Delta t_k,
\Delta P(Y_k \mid do(X)),
stability_k,
external\ consistency_k
\right\}
\]

where each `Y_k` is an anonymous internal event, state component, boundary event, or external event.
There is no runtime field saying which edge is a prediction, action, memory, or reward relation.

A **functional meaning candidate** may be discussed only after a stable, causal, externally
correctable relation signature is observed across held-out conditions. It remains a scientific
description, not a human semantic label and not a runtime object.

## 4. No privileged reward in the Primary track

A scalar reward supplied by the experimenter would define value before the system has formed its own
relations. Therefore:

- the Primary v0.6 runtime has no `reward`, `reward_relation`, correct action, or utility target;
- the world returns ordinary raw external pulses;
- anonymous homeostatic channels, if present, are ordinary state variables rather than `good` or
  `bad` labels;
- a reward-driven system is allowed only as an isolated comparator.

v0.6 tests relation formation and causal world coupling, not full value formation.

## 5. Boundary events instead of predefined actions

The Field may emit an event through an anonymous outbound port:

```text
endogenous Field trajectory
        ↓
outbound port:7 event
        ↓
world changes
        ↓
later world-to-field events
```

The world adapter may implement the physical consequence of `port:7`. The runtime is not told that
this is an action, whether it is correct, or whether its result is rewarding. The observer can later
measure whether an endogenous Spark changed the outbound-port distribution and external stream.

## 6. Persistent state instead of a predefined memory relation

The runtime changes ordinary state:

- membrane or residual state;
- threshold or adaptation;
- persistent traces;
- local transition state;
- eligibility;
- boundary-coupling state;
- pending endogenous state.

An observer may call an effect memory-like only after delay, reset, transplant, and causal controls.
The runtime does not update a `MemoryRelation`.

## 7. Revised endogenous Spark evidence levels

### Level 1 — Endogenous origin

A normally thresholded Field Spark occurs without direct external supply at that target and time.
Noise, fixed echo, queue replay, and evaluator leakage remain alternative explanations to exclude.

### Level 2 — Causally Participating Endogenous Spark

The Spark causally changes a later anonymous internal state, endogenous event, boundary event, or
external event stream. Targeted intervention must exceed matched random and sham controls.

### Level 3 — Externally Stabilized Relational Endogenous Spark

The Spark or lineage participates in a stable, externally confirmable and revisable pattern of
anonymous causal relations across held-out conditions. Observer projections may subsequently report
predictive, boundary-effect, persistence, or world-coupling properties.

Level 3 is the Primary v0.6 target. It is not semantic understanding.

## 8. Generator hierarchy

```text
G0  Field-only spontaneous continuation       Primary
G1  local temporal expectation traces         Primary
G2  sparse/local transition adaptation        Primary
G3  generic recurrent predictor               Comparator
G4  explicit Assembly-conditioned predictor   Comparator
G5  typed function-head system                 Comparator
```

`G5` may contain explicit prediction/action/memory/reward heads. It exists to test whether human
functional categories provide an advantage.

Interpretation:

- G0–G2 success supports Field-embedded, taxonomy-independent Dynamics;
- G3-only success means a generic external predictor supplied the function;
- G4-only success means explicit Assembly state was required;
- G5-only success means typed human functional categories were required in that experiment.

Comparators must not enter the Primary import graph.

## 9. Runtime invariants

1. Explicit Assembly state is forbidden in the Primary runtime.
2. Prediction, action, memory, reward, outcome, goal, role, and meaning relation types are forbidden.
3. Endogenous events are hypotheses, never external observations.
4. Positive learning requires registered external consistency; internal recurrence cannot confirm
   itself.
5. Observer/evaluator removal, renaming, or taxonomy permutation must leave runtime hashes unchanged.
6. No privileged scalar reward or correct-action target enters the Primary run.
7. Internal pulses pass through ordinary threshold, inhibition, refractory, adaptation, and safety
   rules.
8. Generation remains bounded by depth, energy, lifetime, branch count, and proposal count.
9. Direct copies, fixed-delay echoes, pending queue replay, random pulses, and evaluator leakage must
   be excluded.
10. Missing-middle counts as forward completion only before the later external cue.
11. Functional categories may appear only in observer artifacts and reports.
12. The runtime ontology and observer taxonomy must be inventoried separately in every report.

## 10. Core scientific Gates

### Gate A — Runtime, observer, and taxonomy independence

- local deterministic reference;
- provenance and checkpoint integrity;
- explicit Assembly and functional-type field scan;
- Observer ON/OFF equality;
- evaluator package absent/present equality;
- evaluator category rename/permutation equality;
- no scalar reward or correct-action input;
- zero self-confirmation violations.

### Gate B — Endogenous origin and non-copy

- a normally thresholded internal Spark occurs without direct external supply at that target/time;
- copied-input, fixed-delay echo, pending queue, random-noise, and evaluator-target controls are
  excluded;
- G3/G4/G5 are absent from the Primary path.

### Gate C — Persistent-state dependence

- identical current external input under different valid prior states may produce different internal
  responses;
- identical full runtime state deterministically reproduces the same response;
- candidate-state reset changes or removes the history effect;
- no evaluator context label enters runtime.

### Gate D — Autonomous internal continuation

- an internally originated root Spark changes later anonymous internal events under bounded external
  silence;
- the chain exceeds simple pending-queue replay;
- safety budgets remain active;
- suppressing the root or local path selectively changes downstream activity.

### Gate E — Untyped causal participation

- targeted root/path intervention changes the later anonymous runtime trace more than matched random
  or sham intervention;
- at least one effect reaches either a later persistent state component, outbound boundary event, or
  externally visible event stream;
- the effect does not depend on a typed function head;
- collateral damage is bounded.

### Gate F — Untyped relation stabilization

- an anonymous source-to-target relation recurs across episodes and held-out perturbations;
- external consistency stabilizes it while internal-only recurrence does not;
- its causal effect survives surface variation where appropriate;
- relation stability exceeds frequency-only, readout-only, random-event, and no-endogenous controls;
- no `relation_type` is stored in runtime.

### Gate G — External correction and relation revision

- external mismatch cancels, redirects, or weakens stale paths;
- external input remains authoritative;
- changed world contingencies revise later anonymous Dynamics and boundary coupling;
- stable controls do not cause excessive revision;
- no global reward target directs the revision.

### Gate H — Persistence locus and post-hoc functional equivalence

- reset/transplant identifies at least one candidate carrier of experience-dependent behaviour;
- memory is not hidden in an evaluator or external comparator;
- physically different trajectories may be grouped only after matched causal relation signatures are
  observed;
- the grouping remains observer-only and taxonomy permutation does not affect runtime.

## 11. Primary experiments

### E06-0 — Null, copy, echo, and typed-leak controls

Run external silence, random pulses, copied targets, fixed delays, pending queue, frequency-only, and
forbidden typed-field injections.

### E06-1 — Non-copy endogenous Field Spark

Hold current input fixed, vary valid prior state, and measure normally thresholded internal Sparks.

### E06-2 — Same input, different persistent state

Require deterministic same-state replay and history-dependent response differences. Reset candidate
state components one at a time.

### E06-3 — Autonomous endogenous chain

After the root Spark, provide bounded external silence and measure later internal events. Compare
root suppression, local-path suppression, matched random, sham, and queue-drained controls.

### E06-4 — Generic downstream influence

Do not ask runtime whether an event is predictive, action-related, or memory-related. Measure the
complete anonymous runtime-trace difference under `do(root present)` versus `do(root absent)`.

### E06-5 — Anonymous boundary coupling

Provide outbound ports without action names or correct targets. Test whether endogenous trajectories
change port-event distributions and whether port events alter later external streams.

### E06-6 — Delayed persistence

Measure whether an endogenous lineage changes later state after a gap. Use component reset,
transplant, and matched unrelated-state controls. `memory` is only an observer view.

### E06-7 — External relation stabilization

Repeatedly expose an anonymous lineage to later raw external consistency or contradiction. Measure
transition reliability, causal effect, held-out stability, and internal-only controls.

### E06-8 — Contingency reversal

Change the world mapping between anonymous boundary events and later raw external events. Measure
revision without supplying a reward or correct-action target.

### E06-9 — Physical-trajectory relation equivalence

Create physically different lineages and compare their post-hoc causal relation signatures. Do not
merge them in runtime and do not use surface similarity alone.

### E06-10 — Missing-middle validity assay

Retain the strict criterion:

```text
created_at(C_endogenous) < arrival_at(D_external)
```

Score retrospective inference separately. Passing this assay alone does not satisfy Gate F.

### E06-11 — Taxonomy-independence adversarial suite

- remove evaluator view names;
- rename all evaluator categories;
- permute which ports the evaluator calls actions;
- remove reward/correct-action artifacts;
- omit the observer package entirely;
- confirm byte- or normalized-hash-identical runtime traces, state, outbound events, learning updates,
  and RNG state.

### E06-12 — Typed comparator

Compare the untyped Primary path against an isolated system with explicit prediction/action/memory/
reward heads under matched input and resource budgets where feasible.

### E06-13 — Persistence reset and transplant

Test weight/delay, threshold/adaptation, persistent trace, local transition, boundary coupling,
eligibility, and queue state separately.

## 12. Work packages

### V06-00 — Baseline freeze and preregistration

Completed engineering foundation. Preserve v0.5 results and all amendment history.

### V06-01 — Provenance and event contracts

Completed. External and endogenous origins, proposals, chains, matching, and two-phase eligibility.

### V06-02 — Assembly-free runtime and observer boundary

Completed. Extend this boundary under Amendment 002 to all functional evaluation categories.

### V06-03 — G0 Field continuation diagnostic

Completed as a negative diagnostic: canonical continuation disappears after full queue drain.

### V06-04 — G1 local temporal expectation

Completed engineering reference for anonymous local target/time transitions.

### V06-05 — G2 sparse local transition adaptation

Completed engineering reference with external-confirmation-only positive commit.

### V06-06 — Reinjection and safety

Completed. Internal proposals enter normal Field rules rather than forcing a Spark.

### V06-07 — Reality matching and correction

Completed engineering reference for external-authoritative match, contradiction, expiry, and stale
branch cancellation.

### V06-08 — Endogenous origin and state dependence

Current engineering result: one single-world non-copy, history-dependent, normally thresholded Field
Spark candidate. Multi-world confirmatory evidence remains pending.

### V06-09 — Autonomous chain and untyped causal participation

- create bounded internal lineages after a root Spark;
- record the complete anonymous downstream state delta;
- intervene on root, local transition, persistent trace, queue branch, and reinjection path;
- avoid prediction/action/memory relation objects;
- report observer projections only after causal analysis.

### V06-10 — Untyped relation stabilization and boundary coupling

- add anonymous outbound boundary ports;
- record raw causal transitions among internal, boundary, and external events;
- stabilize only generic local relation strengths after external consistency;
- prohibit scalar reward and correct-action targets;
- compare no-endogenous, random-event, readout-only, G3, G4, and G5.

### V06-11 — External revision and observer projections

- reverse anonymous world contingencies;
- update generic local relation state;
- derive predictive, boundary-effect, persistence, world-coupling, and correction views post-hoc;
- test that category renaming or permutation changes only observer artifacts;
- compare physically different trajectories by causal signature.

### V06-12 — Missing-middle and other validity assays

Run forward missing-middle, prefix continuation, branching, omission, and retrospective inference as
separate diagnostics.

### V06-13 — Persistence-locus and causal dynamic-path analysis

Reset, transplant, and intervene on candidate state components. `Memory` remains the observer's
interpretation of persistence, not a runtime type.

### V06-14 — Brain Lab, taxonomy audit, and local release

Visualize raw events, state, provenance, causal lineage, boundary crossings, external consistency,
interventions, and post-hoc observer views. The UI must not feed any category into runtime.

## 13. Required implementation boundaries

Recommended Primary source layout:

```text
src/sparkbrain/v06/
├─ foundation.py
├─ local_expectation.py
├─ local_transition.py
├─ reinjection.py
├─ reality.py
├─ boundary.py
├─ causal_trace.py
├─ persistence.py
├─ interventions.py
└─ brain.py
```

Observer/evaluator layout:

```text
src/sparkbrain/evaluation/
├─ v06_endogenous.py
├─ v06_state_probe.py
├─ v06_causal_views.py
└─ v06_taxonomy_audit.py

src/sparkbrain/observers/v06/
├─ assembly.py
├─ trajectory.py
└─ relation_views.py
```

Comparator layout:

```text
src/sparkbrain/baselines/v06/
├─ recurrent_predictor.py
├─ assembly_conditioned.py
└─ typed_function_heads.py
```

Dependency rule:

```text
Primary runtime  ─X→ observers
Primary runtime  ─X→ evaluation
Primary runtime  ─X→ baselines

observers/evaluation → immutable runtime output
baselines            → experiment adapter only
```

## 14. Required adversarial tests

1. inject `PredictionRelation`, `ActionRelation`, `MemoryRelation`, or `RewardRelation` into runtime;
2. inject scalar reward, correct action, functional role, or meaning label;
3. rename evaluator categories and compare runtime hashes;
4. permute outbound-port interpretation and compare runtime hashes;
5. remove observer/evaluator packages and rerun;
6. count an endogenous event as an external observation;
7. commit positive learning from internal-only recurrence;
8. use pending queue replay as autonomous continuation;
9. let G3/G4/G5 leak into the Primary import graph;
10. generate after a future cue and report forward completion;
11. exceed generation safety budgets;
12. infer functional equivalence from trajectory similarity without causal controls.

## 15. Current status

Engineering-complete or accepted on `v06`:

- provenance and two-phase external commit;
- Assembly-free runtime and immutable observer boundary;
- G0 negative queue-drain diagnostic;
- G1 local transition expectation;
- G2 externally gated sparse adaptation;
- normal-rule Field reinjection;
- external-authoritative correction and stale-chain cancellation;
- non-copy and state-dependence evaluator contracts;
- one single-world Field-Spark engineering candidate.

Not yet established:

- multi-world/seed Level-1 evidence;
- autonomous internal chain;
- generic downstream causal participation;
- anonymous boundary coupling;
- stable untyped external relation;
- external relation revision;
- taxonomy-independent observer projections;
- physical-trajectory functional equivalence;
- confirmatory missing-middle validity;
- persistence locus outside explicit local transition state;
- semantic meaning, concepts, organs, consciousness, or AGI.

## 16. Completion criteria

Positive completion requires Gates A–H and at least one successful G0/G1/G2 Primary route.

The strongest permitted statement is:

> Under controlled pre-semantic conditions, a persistent Dynamic Field generated endogenous Sparks
> not directly supplied by current input. Without explicit Assembly or predeclared prediction,
> action, memory, reward, role, or meaning types in runtime, those Sparks causally altered later
> anonymous Field or boundary states, and externally stabilized relation patterns remained
> correctable across held-out conditions.

Negative completion is valid when all amended Primary experiments, G0–G5 comparisons, taxonomy and
observer audits, multiple seeds, negative artifacts, strongest counterexamples, and persistence-
locus analyses are completed honestly.

v0.6 does not claim semantic understanding, human-like concepts, value formation, organs,
consciousness, AGI, biological equivalence, or physical energy superiority.
