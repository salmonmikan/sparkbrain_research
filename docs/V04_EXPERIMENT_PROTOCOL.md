# SparkBrain v0.4 experiment protocol

## Shared rules

- CPU-only reference path.
- Fixed random seed and exact config are recorded.
- No answer labels or semantic parser enter the field.
- Every experiment has a matched control.
- Engineering tests are distinct from scientific multi-seed evaluation.
- Generated artifacts must retain negative results.

## E04-1 Temporal order

Input elements are identical; only order changes.

```text
A -> B -> C
C -> B -> A
A+B+C at the same time
```

Primary metric: number of distinct cascade signatures.  This only establishes timing sensitivity.

## E04-2 Temporal coincidence

Three individually weak receptor events are routed through different conduction delays.

- aligned condition: arrivals reach a convergence unit together;
- dispersed condition: arrivals remain separated.

Primary metrics: convergence-unit spike count, total spikes, burst and Ignition count.

## E04-3 Repetition and omission

A periodic `tick` pulse repeats. Compare early and late firing, then advance beyond the expected next event without supplying it.

Primary metrics: early/late spike count and number of explicit omission prediction-error pulses.

## E04-4 Moving point

A dot moves left-to-right or right-to-left through a small frame sequence. Frames are converted to local temporal-difference pulses.

Primary metric: direction-conditioned cascade signatures.

## E04-5 Motif in noise

A fixed time pattern recurs among random low-amplitude events.

Primary metrics: recurring cascade count, motif/control selectivity, and Ignition rate. The current reference runner is an engineering seed and requires a stronger matched-noise protocol before any learning claim.

## E04-6 Action feedback

Deferred from the core acceptance gate. A later protocol will associate recurring signatures with actions and compare reward learning against shuffled signatures and frozen plasticity.

## Release gates

- v0.4 unit tests pass;
- full engineering suite has no regression;
- demo and artifact generation are deterministic;
- static visualizer has no external runtime dependency;
- docs state the scientific boundaries;
- no existing v0.3 result is rewritten.
