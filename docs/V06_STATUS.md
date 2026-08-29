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
- focused and adversarial foundation/G0/G1 tests.

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

G1 is not yet reinjected into the Field and is not a forward-completion result. It is the local,
Assembly-free transition-memory substrate required by the next slice.

## Validation

The G1 head passed GitHub Actions on Python 3.11 and 3.13, including Ruff, local readiness, the
default test suite, and bundle validation.

## Next vertical slice

V06-05 implements G2 sparse local transition adaptation and connects G1 proposals to the existing
provenance ledger through two-phase eligibility. Positive transition updates must remain pending
until matching external confirmation; internal-only activity must not increase confidence.

## Scientific status

Engineering foundation, one negative G0 diagnostic, and the G1 local expectation component only.
No v0.6 forward-completion, branching, reality-correction, functional-utility, causal-pathway, or
memory-locus scientific gate has been evaluated.
