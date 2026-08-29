# SparkBrain v0.6 Endogenous Evidence Engineering Report

## Scope

This report records the V06-08 evidence contracts and their first canonical persistent-transition-
state Field probe after Protocol Amendment 001. It reports a positive **engineering Level-1
candidate**, not a confirmatory scientific Level-2 or Level-3 result.

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
establish predictive validity, downstream utility, a functional relation, or meaning.

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

## Canonical engineering Field probe

The connected probe uses the same current external event in every condition:

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

For each learned condition, the probe:

1. constructs a fresh three-unit Field;
2. presents the shared current external input;
3. verifies that the external-input queue is drained;
4. generates a local G1 endogenous proposal from prior transition state;
5. registers the proposal with endogenous provenance;
6. reinjects it through `FieldReinjectionGate` as ordinary current;
7. lets the retained membrane, threshold, refractory, and adaptation rules decide whether a Spark
   occurs;
8. runs a cloned no-reinjection control to exclude a remaining Field queue as the cause.

Observed engineering result:

```text
reference Field Spark target:       unit:1
reference replay Field Spark target: unit:1
alternate Field Spark target:       unit:2
no-history endogenous event count:  0
no-reinjection Field Spark count:   0
accepted reinjections per learned condition: 1
Field Sparks per learned condition:          1
same-state replay deterministic:    true
prior-state hashes distinct:        true
response changed with history:      true
origin audits passed:               true
engineering candidate:              true
```

The emitted response is constructed from the actual Field `SpikeEvent`, retains
`endogenous-unconfirmed` provenance, and cites the reinjected `endo:g1-...` proposal as its parent.
It is not merely the proposal object being treated as a Spark.

The target is learned from prior external transitions rather than supplied by the evaluator. It
differs from the current external target, appears only after normal-rule reinjection, disappears in
the no-reinjection and no-history controls, carries its origin-state hash, and is rejected by the
audit if direct-copy, fixed-delay echo, queue, or evaluator-target boundaries are violated.

## Important limitation

The observed history dependence is currently localized to persistent G1 local-transition state. The
result does not yet show that membrane potential, adaptation, recurrent Field state, topology, or a
self-sustaining Field trajectory stores the experience.

The Field Spark is internally originated and state-dependent in this controlled construction, but it
has not yet been shown to:

- predict held-out external consequences across multiple worlds and seeds;
- cause a longer autonomous internal chain;
- improve action, memory, or net utility;
- participate in a stable externally correctable functional relation;
- survive targeted versus matched-random causal intervention.

Accordingly, this is a positive engineering Level-1 candidate, not a scientific Level-2 predictive-
cognition or Level-3 functionally relational result.

## Focused test scope

The evaluator and canonical Field-probe suites cover:

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
- same current input with different learned histories;
- real normal-rule Field reinjection;
- a matched no-reinjection Field control;
- parent provenance from proposal to Field Spark;
- no-history no-generation control;
- insufficient-history no-generation control;
- Assembly/motif/answer-field absence.

## CI

GitHub Actions run `33250148222` passed on Python 3.11 and Python 3.13. Both jobs passed installation,
Ruff, local readiness, the default test suite, and bundle validation.

## Claim boundary

This engineering slice supports only:

> In a canonical Assembly-free local-transition probe, the same current external input can produce a
> real, normally thresholded, non-copy endogenous Field Spark whose target is deterministic for the
> same learned state, changes under a different learned history, and disappears without transition
> history or without reinjection.

It does not support:

- confirmatory Level-1 evidence across multiple preregistered worlds and seeds;
- autonomous internal continuation;
- Level-2 predictive validity;
- causal downstream participation;
- Level-3 functional relation acquisition;
- functional or semantic meaning;
- memory localization beyond explicit G1 transition state;
- missing-middle completion as the definition of v0.6 success.
