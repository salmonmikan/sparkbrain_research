# SparkBrain v0.6 Master Plan — Post-V06-11 Revision
## Close the Loop, Locate the Experience, Then Confirm

**Status:** normative remaining-work plan  
**Supersedes for post-V06-11 sequencing:** the remaining-work order in `docs/V06_MASTER_PLAN.md`  
**Normative amendments:**

1. `V06_PROTOCOL_AMENDMENT_001_ENDOGENOUS_SPARK_FUNCTION.md`
2. `V06_PROTOCOL_AMENDMENT_002_UNTYPED_RELATIONAL_DYNAMICS.md`
3. `V06_PROTOCOL_AMENDMENT_003_RELATION_REENTRY_AND_CONFIRMATION.md`

## 1. Current research position

The current branch contains single-world engineering candidates for:

```text
Level 1
same current input + different prior transition state
    -> different normally thresholded endogenous Field Spark

Level 2
endogenous root Spark
    -> later anonymous endogenous Spark chain
    -> selective loss under targeted intervention

partial Level 3
endogenous chain
    -> anonymous outbound boundary event
    -> changed raw external stream
    -> externally stabilized anonymous relation
    -> relation reversal and reacquisition
```

These results are important, but they do not yet close the cognitive loop. The currently revised
anonymous relation is still largely a record observed after the world interaction.

The unresolved loop is:

```text
B_t
 -> outbound world interaction
 -> raw external consequence
 -> anonymous relation state changes
 -> B_future changes because of that relation state
```

Until the last arrow is demonstrated, Gate G is open.

## 2. Remaining-work priority

```text
P1  V06-12A  Relation Re-entry
P2  V06-13   Persistence Locus
P3  V06-12B  Validity Assays
P4  V06-13.5 Confirmatory Generalization
P5  V06-14   Brain Lab / Audit / Release
```

This ordering intentionally prioritizes falsification and loop closure over adding more task
capabilities.

## 3. V06-12A — Relation Re-entry

### 3.1 Goal

Demonstrate that existing externally stabilized anonymous relation state changes a later Field
trajectory and later anonymous boundary event.

### 3.2 No-new-memory constraint

The implementation may add a stateless or execution-record-only adapter, but no second learned
relation table, reward system, semantic type, action policy, prediction head, or memory module.

```text
existing UntypedBoundaryConsistency
        ↓
derived transient support
        ↓
EndogenousPulseProposal / ordinary Field current
        ↓
normal Field Dynamics
```

### 3.3 Minimum experiment

Create three compatible relation states while holding the later Field and input fixed:

```text
S_old       port:7 -> unit:8 dominant
S_reversed  port:7 -> unit:9 dominant
S_returned  port:7 -> unit:8 dominant again
```

Transparently derive one bounded anonymous re-entry pulse from the dominant structural relation.
The pulse must traverse the ordinary reinjection and Field threshold path.

Expected engineering pattern:

```text
same later Field state + same trigger + S_old
    -> endogenous unit:8 Spark -> anonymous boundary port associated with unit:8

same later Field state + same trigger + S_reversed
    -> endogenous unit:9 Spark -> anonymous boundary port associated with unit:9

same later Field state + same trigger + S_returned
    -> endogenous unit:8 Spark again
```

The IDs remain anonymous. The runtime is not told which result is correct, valuable, predictive, or
action-like.

### 3.4 Required controls

- empty consistency state;
- consistency reset after acquisition;
- no-reentry;
- shuffled relation-state assignment;
- tied or low-margin relation state;
- matched-random path suppression;
- targeted re-entry suppression;
- internal-only recurrence;
- identical-state deterministic replay;
- observer/evaluator absent;
- taxonomy labels renamed/permuted.

### 3.5 Pass condition

A relation-state change must cause a later anonymous Field/boundary trace change, and the effect must
move with the relation state under transplant while disappearing under targeted reset or suppression.

### 3.6 Failure interpretation

- If only observer metrics change, the loop is not closed.
- If the effect requires a correct-action label or reward, the Primary hypothesis fails for this
  implementation.
- If the adapter stores a second learned state, the experiment is invalid.
- If the result is only a direct readout and never enters Field Dynamics, Gate G remains failed.

## 4. V06-13 — Persistence Locus

### 4.1 Goal

Determine where each observed experience-dependent effect is actually carried.

### 4.2 Effects to localize

- same-input/different-history endogenous Spark;
- autonomous chain continuation;
- anonymous boundary event;
- external relation reliability;
- relation reversal and reacquisition;
- relation re-entry effect.

### 4.3 Component matrix

| Component | Reset | Transplant | Necessary candidate | Sufficient candidate |
|---|---:|---:|---:|---:|
| Field membrane/residual | yes | yes | measured | measured |
| Threshold/adaptation | yes | yes | measured | measured |
| Persistent traces | yes | yes | measured | measured |
| G1 transition statistics | yes | yes | measured | measured |
| G2 path calibration | yes | yes | measured | measured |
| Eligibility | yes | compatible only | measured | measured |
| Pending endogenous queue | yes | no persistent claim | measured | not a memory claim |
| Anonymous consistency links | yes | yes | measured | measured |
| Static boundary/world wiring | control | control | architecture | not learned memory |
| Re-entry adapter | disable | no learned state to move | causal path | not a memory carrier |

### 4.4 Reset logic

After experience, replace exactly one component with its naive state. Keep all other compatible state
and the later input fixed.

### 4.5 Transplant logic

Move exactly one trained component into a naive compatible runtime. Keep the receiver's other state
naive and use a held-out later input.

### 4.6 Interpretation matrix

```text
Only G1/G2 reset removes all effects
    -> Dynamic Field + explicit local transition memory interpretation

Consistency reset removes re-entry; consistency transplant transfers it
    -> external relation persistence localized to explicit consistency state

Field/adaptation/trace transplant transfers an independent effect
    -> stronger distributed Field-memory candidate

Multiple components jointly necessary, none sufficient alone
    -> distributed interaction candidate

No reproducible reset/transplant mapping
    -> unresolved locus; do not call it memory
```

The result may weaken the SparkBrain claim. That is an intended outcome of V06-13.

## 5. V06-12B — Validity Assays

### 5.1 Position

These assays test internal-model-like properties after relation re-entry and locus analysis. They do
not define the project.

### 5.2 Assays

- forward missing-middle;
- prefix continuation;
- branching futures;
- omission and distractor conditions;
- retrospective reconstruction;
- external contradiction;
- temporal rule reversal;
- no-history and queue-only controls.

### 5.3 Missing-middle invariant

```text
created_at(C_endogenous) < arrival_at(D_external)
```

A post-D reconstruction is reported separately.

### 5.4 Branching requirement

Multiple alternatives must remain represented without treating one internally generated branch as
external evidence. Branch confidence may change only through later raw external consistency.

## 6. V06-13.5 — Confirmatory Generalization Suite

### 6.1 Purpose

Promote or reject the single-world engineering candidates using frozen multi-world, multi-seed,
held-out evaluation.

### 6.2 Freeze boundary

Before confirmatory execution, freeze and hash:

- Primary runtime source;
- observer/evaluator source;
- world generators;
- development and confirmatory seed lists;
- metrics and success thresholds;
- intervention schedules;
- comparator budgets;
- artifact schema.

No tuning is allowed after opening confirmatory results. Corrections require a new protocol version
and a fresh held-out seed set.

### 6.3 Held-out world families

At minimum:

1. unit-ID and port-ID permutations;
2. chain lengths 2–6 and branch factors 1–3;
3. lag and magnitude bands not used in development;
4. mixed polarity and threshold bands;
5. distractor/noise densities;
6. reversal at early, middle, and late phases;
7. partial observation and omissions;
8. compatible reset/transplant mappings;
9. physically different trajectories with matched structural consequences.

### 6.4 Required controls and comparators

Primary controls:

- no endogenous generation;
- random endogenous generation;
- pending-queue/readout-only;
- no re-entry;
- relation-state shuffle;
- targeted, matched-random, and sham interventions.

Comparators:

- G3 generic recurrent predictor;
- G4 explicit Assembly-conditioned predictor;
- G5 typed prediction/action/memory/reward-head system.

Comparators remain isolated and are evaluated under matched input and approximately matched resource
budgets where feasible.

### 6.5 Confirmatory outcomes

Report separately:

- Level-1 endogenous-origin support rate;
- Level-2 targeted causal-participation effect;
- Level-3 stabilization, re-entry, revision, and reacquisition support;
- false-generation and false-revision rates;
- self-confirmation violations;
- held-out degradation;
- comparator advantages;
- strongest failure worlds.

No aggregate score may hide a failed causal or provenance invariant.

### 6.6 Decision rules

Exact numerical thresholds must be frozen before running the suite. At minimum:

- every provenance, self-confirmation, taxonomy, and observer invariant is hard-fail;
- targeted effects must exceed matched-random and sham effects with uncertainty excluding zero;
- re-entry must outperform no-reentry and shuffled-state controls;
- reversal must alter later Dynamics, not only a stored metric;
- stable worlds must remain stable;
- failures and comparator-only successes must be retained as negative evidence.

## 7. V06-14 — Brain Lab, Audit, and Completion

### 7.1 Brain Lab

Visualize without influencing runtime:

- external, endogenous, and boundary events;
- current-arrival causal lineage;
- local transition and anonymous consistency state;
- relation re-entry pulses;
- reset/transplant conditions;
- intervention differences;
- revision and reacquisition;
- observer projections.

### 7.2 Taxonomy and non-interference audit

- observer/evaluator physically absent versus present;
- taxonomy rename and permutation;
- forbidden source/config/checkpoint/trace fields;
- G3/G4/G5 isolation;
- no hidden reward, correct action, answer, Assembly, or semantic type;
- identical normalized runtime trace, boundary events, updates, RNG state, and checkpoint continuation.

### 7.3 Completion paths

Positive completion, bounded positive completion, negative completion, and unresolved completion are
all valid. Release must state exactly which path occurred.

## 8. Release blockers

The following block release review:

- relation state has not re-entered later Dynamics;
- persistence locus has not been tested by reset and transplant;
- confirmatory held-out suite has not been frozen and run;
- comparators have not been evaluated or explicitly scoped as unavailable with a documented impact;
- taxonomy or observer non-interference is incomplete;
- strongest counterexamples are missing;
- negative artifacts are omitted.

## 9. Current permitted claim

Before completion, the strongest claim remains:

> SparkBrain v0.6 contains single-world engineering candidates for history-dependent endogenous
> Field Sparks, sequential endogenous causal participation, anonymous world coupling, and externally
> revised anonymous relation state. Relation re-entry, persistence locus, and held-out generalization
> remain unresolved.

## 10. Immediate implementation sequence

```text
1. Add stateless relation re-entry adapter over existing consistency state.
2. Demonstrate same Field/current input + old/reversed/returned relation state -> different Field and
   boundary traces.
3. Add consistency reset and transplant controls.
4. Record whether the effect is fully localized to explicit consistency state.
5. Only then expand V06-13 component reset/transplant matrix.
```
