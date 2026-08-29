# SparkBrain v0.6 Runtime Invariants
## Assembly Observer-Only / Anti-Self-Confirmation Contract

This document is a fail-closed implementation contract for the primary v0.6 runtime.

## 1. Dependency boundary

Allowed:

```text
observer → immutable runtime trace
evaluation → runtime output
Brain Lab → observer artifact + runtime artifact
```

Forbidden:

```text
runtime → Assembly observer
runtime → observer-generated Assembly ID
runtime → evaluator hidden label
```

## 2. Forbidden runtime fields

The primary runtime, its checkpoint, and its JSONL trace must reject:

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
```

An observer artifact may contain `observed_assembly_id`, but that value must not return to runtime.

## 3. Provenance state machine

```text
external
endogenous-unconfirmed
endogenous-confirmed
endogenous-contradicted
endogenous-expired
```

Only `external` is an observation. Confirmation changes the status of a prediction; it never
reclassifies the prediction as an external event.

## 4. Two-phase learning

At internal prediction time:

```text
eligibility += candidate update
committed positive update = 0
```

After a registered external event confirms the same path:

```text
committed positive update += bounded eligibility
```

Contradiction or expiry:

```text
committed positive update = 0
```

## 5. No self-confirmation

The following loop is prohibited:

```text
endogenous prediction
  → endogenous Field spike
  → count as observation
  → increase confidence
```

An endogenous event must not increment external observation count, independent evidence count,
positive training count, or confirmation count.

## 6. Forward completion

A primary missing-middle completion requires:

```text
created_at(C_endogenous) < arrival_at(D_external)
```

If C is generated from the call that already processed D, it is retrospective reconstruction and
must not enter the primary forward-completion metric.

## 7. Observer non-interference

Observer ON and OFF runs with the same seed and input must have identical:

- Field trace;
- internal event queue;
- predictions;
- actions;
- learning updates;
- RNG state;
- state hash;
- checkpoint continuation.

The observer may copy, aggregate, cluster, annotate, and render. It may not mutate state, schedule
an event, update confidence, choose an action, or change a threshold.

## 8. Internal-generation safety

Every endogenous chain must be bounded by:

- generation-depth limit;
- energy budget;
- proposal budget per window;
- time to live;
- branch budget;
- normal refractory, inhibition, and adaptation rules;
- an explicit no-generation state.

## 9. Required adversarial tests

1. inject a forbidden Assembly field;
2. use an endogenous event as external confirmation;
3. grow confidence in an internal-only run;
4. generate C only after D and report it as forward completion;
5. leak the evaluator target into runtime metadata;
6. use a pending delayed queue as learned continuation;
7. let the observer mutate a trace;
8. let a generic recurrent comparator leak into the primary path;
9. keep a contradicted chain active;
10. exceed generation depth or energy budget.

Any violation must fail closed or create an explicit failed-gate artifact.
