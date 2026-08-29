# SparkBrain v0.6 Endogenous Evidence Engineering Report

## Scope

This report records the first V06-08 evaluation contracts added after Protocol Amendment 001. It
does not report a scientific Level-1, Level-2, or Level-3 result.

## Why the evaluator is separate

The Primary runtime must not know whether an event is labelled a successful non-copy candidate or a
functional-relation candidate. Those judgements belong to the evaluation layer.

The implementation therefore lives at:

```text
src/sparkbrain/evaluation/v06_endogenous.py
```

and consumes immutable runtime values. It does not feed a class, motif, Assembly, missing target, or
human semantic label back into `sparkbrain.v06`.

## Non-copy origin audit

`audit_endogenous_origin(...)` rejects an event as a clean Level-1 research candidate when any of
the following applies:

- the event is actually external;
- it directly copies a current external target, polarity, magnitude, and time window;
- it matches a preregistered fixed-delay echo control;
- the paired queue-drained control has not excluded pending-queue replay;
- the evaluator supplied the target;
- the event lacks the persistent origin-state hash required for a state-grounded claim.

Passing this audit means only that several shortcut explanations have been excluded. It does not
establish prediction, utility, functional relation, or meaning.

## Persistent-state dependence assessment

`assess_persistent_state_dependence(...)` compares three runs:

```text
reference history + current input
same reference history replay + same current input
alternate valid history + same current input
```

A state-dependence candidate requires:

1. exactly the same current input hash in all runs;
2. deterministic response and final state for the same prior state;
3. a distinct alternate prior-state hash;
4. a changed endogenous response trace under the alternate history.

This prevents input differences or nondeterministic replay from being misreported as internal-state
dependence.

## Current boundary

The evaluator has not yet been connected to a canonical Field world that demonstrates a passing
non-copy or state-dependence result. The code defines the fail-closed evidence contract required for
that experiment.

## Focused test scope

The focused suite covers:

- a clean candidate;
- external-event rejection;
- direct-copy rejection;
- known fixed-delay echo rejection;
- queue-control and evaluator-target requirements;
- missing origin-state rejection;
- invalid control provenance;
- deterministic same-state replay;
- history-dependent response candidate;
- unchanged response under different history;
- nondeterministic replay rejection;
- mismatched current-input rejection;
- external response-event rejection;
- Assembly/motif field absence.

## Claim boundary

This engineering slice supports only that v0.6 has explicit evaluation contracts for distinguishing
an internally originated event from several shortcut explanations and for testing whether a matched
current input is transformed differently by a persistent prior Field state.

It does not support:

- an observed non-copy endogenous Spark;
- predictive validity;
- autonomous internal continuation;
- causal participation;
- functional relation acquisition;
- functional meaning;
- missing-middle completion.
