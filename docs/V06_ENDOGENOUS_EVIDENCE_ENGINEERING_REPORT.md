# SparkBrain v0.6 Endogenous Evidence Engineering Report

## Scope

This report records the V06-08 evidence contracts and their first canonical persistent-transition-
state probe after Protocol Amendment 001. It does not report a scientific Level-2 or Level-3 result
and does not establish a Field-causal endogenous Spark.

## Why the evaluator is separate

The Primary runtime must not know whether an event is judged a successful non-copy candidate or a
functional-relation candidate. Those judgements belong to the evaluation layer.

The implementation therefore lives at:

```text
src/sparkbrain/evaluation/v06_endogenous.py
src/sparkbrain/evaluation/v06_state_probe.py
```

and consumes runtime values without feeding a class, motif, Assembly, missing target, correct action,
or human semantic label back into `sparkbrain.v06`.

## Non-copy origin audit

`audit_endogenous_origin(...)` rejects an event as a clean Level-1 research candidate when any of
the following applies:

- the event is actually external;
- it directly copies a current external target, polarity, magnitude, and time window;
- it matches a preregistered fixed-delay echo control;
- pending-queue replay has not been excluded;
- the evaluator supplied the target;
- the event lacks the persistent origin-state hash required for a state-grounded claim.

Passing this audit means only that several shortcut explanations have been excluded. It does not
establish prediction, utility, causal participation, functional relation, or meaning.

## Persistent-state dependence assessment

`assess_persistent_state_dependence(...)` compares three runs:

```text
reference history + current input
same reference history replay + same current input
alternate valid history + same current input
```

A state-dependence candidate requires:

1. exactly the same current-input hash in all runs;
2. deterministic response and final state for the same prior state;
3. a distinct alternate prior-state hash;
4. a changed endogenous response trace under the alternate history.

Run-specific event IDs are excluded from the behavioural response signature. This prevents different
identifiers, different inputs, or nondeterministic replay from being reported as persistent-state
dependence.

## Canonical engineering probe

The first connected probe uses the same current external event in every condition:

```text
current input: unit:0 at 100 ms
```

Only the prior externally learned local-transition history changes:

```text
reference history: unit:0 -> unit:1 after 5 ms, repeated three times
reference replay:  same history reconstructed independently
alternate history: unit:0 -> unit:2 after 5 ms, repeated three times
no-history control: no learned transition
```

Observed engineering result:

```text
reference response target:       unit:1
reference replay response target: unit:1
alternate response target:       unit:2
no-history endogenous events:    0
same-state replay deterministic:  true
prior-state hashes distinct:      true
response changed with history:    true
origin audits passed:             true
engineering candidate:            true
```

The proposal target is learned from prior external transitions rather than supplied by the evaluator.
It differs from the current external target, survives a queue-free construction, carries its origin-
state hash, and is rejected by the audit if direct-copy, fixed-delay echo, queue, or evaluator-target
controls are violated.

## Important limitation

This probe localizes the observed dependence to persistent G1 local-transition state. It does not yet
show that membrane potential, adaptation, recurrent Field state, or a self-sustaining Field trajectory
stores the experience. The generated value is an endogenous proposal; the probe does not by itself
show a causally effective Field Spark or autonomous internal chain.

Accordingly, this is a positive **engineering candidate** for non-copy proposal origin and persistent
transition-state dependence, not a scientific Level-2 predictive-cognition or Level-3 functional-
relation result.

## Focused test scope

The evaluator and canonical probe suites cover:

- clean non-copy candidates;
- external-event rejection;
- direct-copy rejection;
- known fixed-delay echo rejection;
- queue-control and evaluator-target requirements;
- missing origin-state rejection;
- invalid control provenance;
- deterministic same-state replay;
- history-dependent response candidates;
- unchanged response under different history;
- nondeterministic replay rejection;
- mismatched current-input rejection;
- external response-event rejection;
- identity-independent behavioural signatures;
- same input with different learned histories;
- no-history no-generation control;
- insufficient-history no-generation control;
- Assembly/motif/answer-field absence.

## CI

GitHub Actions run `33249930145` passed on Python 3.11 and Python 3.13. Both jobs passed installation,
Ruff, local readiness, the default test suite, and bundle validation.

## Claim boundary

This engineering slice supports only:

> A canonical Assembly-free local-transition probe can generate a non-copy endogenous proposal whose
> response is deterministic for the same learned state, changes under a different learned history,
> and disappears when that transition history is absent.

It does not support:

- a scientifically established internally originated Field Spark;
- autonomous internal continuation;
- predictive validity in held-out worlds;
- causal downstream participation;
- functional relation acquisition;
- functional or semantic meaning;
- memory localization beyond the explicit G1 transition state;
- missing-middle completion as a primary scientific result.
