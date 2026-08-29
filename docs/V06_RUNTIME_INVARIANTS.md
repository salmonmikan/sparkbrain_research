# SparkBrain v0.6 Runtime Invariants
## Assembly-Free, Taxonomy-Free, Anti-Self-Confirmation Contract

This document is the fail-closed implementation contract for the Primary v0.6 runtime. Protocol
Amendment 002 extends the observer-only boundary from Assembly to all human functional categories.

## 1. Dependency boundary

Allowed:

```text
observer/evaluation → immutable runtime trace
Brain Lab           → runtime artifact + observer artifact
world adapter       ↔ anonymous inbound/outbound boundary events
```

Forbidden:

```text
runtime → Assembly observer
runtime → evaluator projection or label
runtime → typed functional comparator
runtime → hidden answer, reward, or correct-action source
```

## 2. Runtime is category-free, not structure-free

Permitted runtime structure:

- anonymous unit/channel/region/boundary-port IDs;
- event time, magnitude, polarity, duration, and direction;
- external/endogenous provenance;
- causal parent and local path IDs;
- Field, persistent trace, transition, eligibility, and external-consistency state;
- bounded local reliability and generation resources.

Prohibited runtime ontology:

```text
AssemblyState
PredictionRelation
ActionRelation
MemoryRelation
RewardRelation
FunctionalRole
MeaningState
GoalType
OutcomeClass
```

## 3. Forbidden runtime fields

The Primary runtime, checkpoint, config, and JSONL trace must reject fields equivalent to:

```text
assembly_id
assembly_label
assembly_membership
assembly_prototype
assembly_state
motif_id
hidden_state_id
missing_target
correct_action
outcome_label
meaning
semantic_state
concept_label
functional_role
role_type
relation_type
prediction_relation
action_relation
memory_relation
reward_relation
prediction_head
action_head
memory_head
reward_head
action_bias
action_type
action_label
reward
reward_value
utility_target
goal_label
```

An observer artifact may contain descriptive view names. Those values must not return to runtime.

## 4. Observer projections are queries, not types

The evaluator may compute:

- predictive view;
- boundary-effect view;
- persistence view;
- world-coupling view;
- correction view.

One lineage may satisfy several views. Runtime cannot receive a one-hot or soft assignment to those
views.

## 5. No privileged reward or correct action

The Primary v0.6 world returns ordinary raw events. It does not provide a scalar reward, correct-
action identity, goal label, or utility target.

Anonymous homeostatic state is permitted only as ordinary state. A reward/value system belongs to an
isolated comparator and must not enter the Primary import graph.

## 6. Boundary event contract

A field-to-world event is identified only by anonymous port, time, magnitude, polarity, provenance,
and causal lineage. Runtime does not know its human action name or correctness.

The evaluator may later map ports to an action view. Renaming or permuting that map must not alter
runtime.

## 7. Provenance state machine

```text
external
endogenous-unconfirmed
endogenous-confirmed
endogenous-contradicted
endogenous-expired
```

Only `external` is an observation. Confirmation changes the consistency status of a hypothesis; it
never reclassifies it as an external event.

## 8. Two-phase learning

At endogenous generation time:

```text
eligibility += candidate update
committed positive update = 0
```

After a registered external event confirms the same anonymous path:

```text
committed positive update += bounded eligibility
```

Contradiction or expiry:

```text
committed positive update = 0
```

## 9. No self-confirmation

The following loop is prohibited:

```text
endogenous event
  → endogenous Field Spark
  → count as observation
  → increase local reliability
```

An endogenous event must not increment external observation count, independent evidence count,
positive training count, or confirmation count.

## 10. Observer and taxonomy non-interference

For the same seed, initial state, and external stream, the following variants must have identical
runtime output:

- Observer ON versus OFF;
- evaluator package present versus absent;
- evaluator view names renamed;
- outbound-port action descriptions permuted;
- prediction/action/memory/reward terminology removed;
- typed G5 comparator disabled versus physically absent from the Primary dependency graph.

Required equality:

- Field trace;
- internal and boundary queues;
- outbound boundary events;
- local updates;
- RNG state;
- state hash;
- checkpoint continuation.

Only observer/evaluator artifacts may differ.

## 11. Internal-generation safety

Every endogenous lineage must be bounded by:

- generation-depth limit;
- energy budget;
- proposal budget per window;
- time to live;
- branch budget;
- normal refractory, inhibition, threshold, and adaptation rules;
- an explicit no-generation state.

## 12. Forward validity assay

For missing-middle only:

```text
created_at(C_endogenous) < arrival_at(D_external)
```

If C is produced after D is processed, it is retrospective reconstruction. This assay is not the
full definition of v0.6 success.

## 13. Causal-first interpretation

Primary intervention targets anonymous Dynamics:

- endogenous root event;
- local transition path;
- persistent trace;
- reinjection branch;
- outbound boundary path;
- external-consistency update path.

Only after measuring the downstream trace difference may an observer describe the effect as
predictive, action-related, persistent, world-coupled, or corrective.

## 14. Required adversarial tests

1. inject explicit Assembly state;
2. inject Prediction/Action/Memory/Reward relation fields;
3. inject scalar reward, correct action, goal, outcome class, or meaning label;
4. rename evaluator categories and compare runtime hashes;
5. permute outbound-port interpretation and compare runtime hashes;
6. remove observer/evaluator packages and rerun;
7. use an endogenous event as external confirmation;
8. grow confidence in an internal-only run;
9. use a pending delayed queue as autonomous continuation;
10. let G3/G4/G5 leak into the Primary import graph;
11. keep a contradicted branch active;
12. exceed generation safety budgets;
13. infer functional equivalence from surface similarity alone;
14. report after-the-fact reconstruction as forward completion.

Any violation must fail closed or create an explicit failed-Gate artifact.
