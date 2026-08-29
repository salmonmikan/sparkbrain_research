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
- focused and adversarial foundation/G0/G1/G2 tests.

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

G2 is not yet reinjected into the Field and is not a forward-completion result. It establishes the
confirmation-gated local transition substrate required by V06-06.

## Validation

Local focused validation before push:

```text
G2 focused tests: 12 passed
compileall: PASS
line-length audit: PASS
```

GitHub Actions run `33247919075` passed on both Python 3.11 and Python 3.13. Each job completed:

```text
Install: PASS
Ruff lint: PASS
Local readiness: PASS
Default test suite: PASS
Bundle validation: PASS
```

## Next vertical slice

V06-06 connects accepted G1/G2 proposals to normal-rule Field reinjection with confidence, energy,
depth, lifetime, and branch budgets. Endogenous pulses must pass ordinary membrane integration,
inhibition, threshold, refractory, and adaptation rules; they may not force a Spark.

## Scientific status

Engineering foundation, one negative G0 diagnostic, G1 local expectation, and G2
confirmation-gated local adaptation only. No v0.6 forward-completion, branching,
reality-correction, functional-utility, causal-pathway, or memory-locus scientific gate has been
evaluated.
