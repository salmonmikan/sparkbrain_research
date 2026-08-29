# SparkBrain v0.6 Status

## Implemented on `v06`

- V06-00 baseline and protocol foundation;
- V06-01 external/endogenous provenance contracts;
- endogenous proposal, chain, match, and eligibility records;
- two-phase learning with external-confirmation-only positive commit;
- V06-02 Assembly-free runtime-state validation;
- immutable post-hoc observer trace;
- observer ON/OFF non-interference helper;
- post-hoc trajectory observer in `sparkbrain.observers`;
- additive `0.6-dev1` checkpoint integrity contract;
- V06-03 G0 Field-only queue-control probe;
- V06-04 G1 local temporal expectation memory;
- V06-05 G2 sparse local transition adaptation;
- V06-06 bounded normal-rule Field reinjection;
- V06-07 external-authoritative reality correction and stale-branch cancellation;
- focused and adversarial foundation/G0/G1/G2/reinjection/reality tests.

## G0 canonical engineering diagnostic

The same immutable prefix Field state is cloned into three conditions:

```text
intact queue
fully drained queue
shuffled queue
```

In the minimal canonical topology, the intact condition produces two later spikes, while the fully
drained condition produces zero. The current interpretation is therefore:

```text
status: not_observed_after_queue_drain
pending_queue_dependency: true
```

This is an engineering diagnostic, not a confirmatory Gate B result. The inherited v0.4 Field does
not spontaneously continue after all scheduled arrivals are removed. G0 remains unsupported.

## G1 engineering slice

G1 stores local source-target lag statistics only from external-to-external event pairs. It can
produce bounded `EndogenousPulseProposal` values containing target, predicted time, magnitude,
polarity, confidence, local path, lifetime, generation depth, and energy cost.

The following boundaries are tested:

- proposal generation does not increase learned transition counts;
- endogenous source or target events cannot train the model;
- reversed transitions remain distinct;
- timing variance reduces proposal confidence;
- insufficient observations produce no proposal;
- state serialization is deterministic;
- no Assembly or evaluator label appears in G1 state.

## G2 engineering slice

G2 wraps G1 proposals in a sparse path-specific adaptation layer and registers every proposal as a
provenance chain with an uncommitted `LearningEligibility` record.

The path state is not changed when a proposal is generated or reinjected. A matching external event
is required before the eligibility can commit and before timing, magnitude, or reliability
corrections are applied to that local path. An endogenous event cannot resolve a proposal or raise
path confidence. A contradictory external event may reduce path reliability, but cannot create a
positive committed update.

G2 state remains keyed only by local path identifiers such as `local:unit:1->unit:2`; it contains no
Assembly ID, motif ID, global sequence representation, or evaluator answer label. Pending state is
bounded and fails closed before partial registration when its budget is exhausted. An external event
that arrives after the eligibility lifetime expires is rejected before it can partially confirm the
proposal or enter the ledger.

## V06-06 reinjection slice

`FieldReinjectionGate` converts a registered, still-unconfirmed proposal into an ordinary
`SynapticArrival` for a concrete `unit:<id>` target. The injected current is scaled by proposal
confidence and is bounded by independent current, energy, generation-depth, per-window proposal,
branch, lifetime, and duplicate-scheduling limits.

The gate never emits a Spike directly. A reinjected event can produce a Spark only if the retained
v0.4 Field later integrates enough current to cross its ordinary dynamic threshold. Refractory,
adaptation, inhibition, recurrent propagation, and event safety limits remain active. A
sub-threshold reinjection remains sub-threshold.

Reinjection does not change the provenance event from `endogenous-unconfirmed`, does not increment
external observations, and does not commit positive learning. Unknown targets and unsafe proposals
fail before queue mutation.

## V06-07 reality-correction slice

`RealityCorrectionEngine` accepts only `external` observations. It compares a new external event
against live pending G2 proposals, expires predictions whose lifetime has elapsed, confirms at most
one matching proposal, marks incompatible due predictions as contradicted, and schedules the
external event into the Field as the authoritative current.

A matching external event cancels the queued endogenous root arrival before the external arrival is
scheduled, so the prediction and observation are not double-counted. A contradiction cancels the
root arrival and, when an endogenous Spark has already propagated, also cancels tracked descendant
arrivals. Descendant cancellation uses a runtime provenance index reconstructed from the retained
Field's deterministic Spark pulse hashes; it does not use Assembly IDs or observer output.

The reality engine rejects endogenous events presented as observations, duplicate external-event
processing, observations in the Field past, and unknown target units before correction begins.
External confirmation remains the only positive G2 commit route.

This slice establishes correction mechanics and provenance-safe queue cancellation. It does not yet
establish forward missing-middle completion, because no canonical prefix/missing-middle experiment
has been evaluated.

## Validation

G2 hardening validation:

```text
G2 focused tests: 12 passed
compileall: PASS
line-length audit: PASS
GitHub Actions run 33247919075: PASS on Python 3.11 and 3.13
```

V06-06 validation:

```text
reinjection focused tests: 11 added
GitHub Actions run 33248216849: PASS on Python 3.11 and 3.13
Ruff lint: PASS
Local readiness: PASS
Default test suite: PASS
Bundle validation: PASS
```

V06-07 validation:

```text
reality-correction focused tests: 8 added
GitHub Actions run 33249195833: PASS on Python 3.11 and 3.13
Ruff lint: PASS
Local readiness: PASS
Default test suite: PASS
Bundle validation: PASS
```

## Next vertical slice

V06-08 will connect external observations, G1/G2 proposals, normal-rule reinjection, intermediate
endogenous Sparks, and external reality into a canonical prefix and missing-middle runner. The
Primary missing-middle criterion remains `t(C_endo) < t(D_external)`; after-the-fact reconstruction
will be reported separately and cannot satisfy the forward-completion gate.

## Scientific status

Engineering foundation, one negative G0 diagnostic, G1 local expectation, G2
confirmation-gated local adaptation, normal-rule reinjection, and external-authoritative correction
only. No v0.6 forward-completion, branching, functional-utility, causal-pathway, or memory-locus
scientific gate has been evaluated.
