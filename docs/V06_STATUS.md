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
- focused and adversarial foundation/G0 tests.

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

This is an engineering diagnostic, not a confirmatory Gate B result. It shows that the inherited
v0.4 Field does not spontaneously continue after all scheduled arrivals are removed. G0 is not yet
supported; this negative boundary determines the next G1 local-expectation slice.

## Next vertical slice

V06-04 implements G1 local temporal expectation traces. It must remain local and Assembly-free,
propose future unit/time activity without a global sequence state, and commit positive learning only
after external confirmation.

## Scientific status

Engineering foundation and one canonical G0 diagnostic only. No v0.6 forward-completion,
branching, reality-correction, functional-utility, causal-pathway, or memory-locus scientific gate
has been evaluated.
