# RV01 R01-08 — Physical Persistence-Locus Report

## Decision

R01-08 decomposes the R01-04 learned continuation into ordinary connection weights, connection
delays, unit dynamic state, short-lived plasticity traces, receptor support, fixed topology, and the
ongoing plasticity flag.

```text
full learned connection state generates chain:       YES
weight reset removes chain:                          YES
learned weights alone transfer path order:           YES
learned delays alone transfer chain:                 NO
delay reset preserves order:                         YES
learned delays change spike timing:                  YES
full connection transplant reproduces exact trace:   YES
unit dynamic state alone transfers chain:            NO
short-lived trace alone transfers chain:             NO
receptor support alone transfers chain:              NO
fixed edge structure alone transfers chain:          NO
ongoing plasticity required during recall:            NO
broad distributed dynamic persistence supported:     NO
edge-localized physical persistence supported:       YES
```

The current acquired transition is physically stored, but its durable locus is specifically the
pairwise connection state rather than a broadly distributed membrane, adaptation, receptor, or
controller-trace state.

## Canonical setup

External training sequence:

```text
0 -> 1 -> 2 -> 3
```

Before training, every directed edge has:

```text
weight: 0.05
delay:  8.0 ms
```

After training, the three causal path edges have approximately:

```text
weight: 0.9597959895689502
delay:  5.375 ms
```

Every recall condition starts from the same naive dynamic Field state and receives the same external
unit:0 cue at 100 ms.

## Full learned connection state

The trained Field produces:

```text
unit:1 at 105.375 ms
unit:2 at 110.750 ms
unit:3 at 116.125 ms
```

No G1, G2, proposal scheduler, external generator, or readout is present in this route.

## Weight reset

All learned weights are reset to 0.05 while learned delays remain at 5.375 ms.

```text
later endogenous chain: none
```

Fast timing alone cannot make the weak physical route cross threshold.

## Weight-only transplant

Learned weights are copied into a naive Field while every delay remains at the original 8.0 ms.

```text
unit:1 at 108 ms
unit:2 at 116 ms
unit:3 at 124 ms
```

The route order transfers without learned delays. Thus, in this canonical construction, learned
weights are sufficient for path identity and propagation.

## Delay-only transplant

Learned delays are copied into a naive Field while every weight remains at 0.05.

```text
later endogenous chain: none
```

Delay state is not sufficient to carry the acquired route.

## Delay reset

The trained weights are retained while all delays are reset to 8.0 ms.

```text
later route: 1 -> 2 -> 3
later times: 108, 116, 124 ms
```

Path identity survives, but the exact timing changes. Delay state therefore acts as temporal
calibration rather than the primary carrier of path identity.

## Full connection transplant

Copying both weights and delays into a naive compatible Field reproduces the donor's units and exact
spike times.

```text
later units: 1 -> 2 -> 3
later times: 105.375, 110.750, 116.125 ms
```

## Unit dynamic state

The external plasticity controller changes no membrane potential, adaptation value, refractory time,
queue state, spike counter, or unit trace inside `TemporalExcitableField` during training. The Field's
dynamic-state hash is identical before and after training.

Copying that dynamic state into a Field with naive connections does not transfer continuation.

This does not prove that membrane or adaptation can never carry experience in a future RV01 design.
It shows that they do not carry the current R01-03/R01-04 learned sequence.

## Short-lived controller trace

The final unit-local external traces are copied into a controller attached to a naive Field. Recall is
then run without further plasticity observations.

```text
controller traces present: yes
later endogenous chain:    none
```

Conversely, clearing those traces after training does not erase the learned route. They are working
state for physical updates, not the durable recall carrier.

## Receptor support and fixed topology

Training changes neither:

- the receptor-ID set;
- the set of directed connection endpoints;
- the number of units or edges.

A naive Field with the same receptors and the same fully connected topology does not continue after
the cue. Static support and connectivity are necessary architecture, but they are not the acquired
sequence state in this assay.

## Ongoing plasticity flag

After learning, every connection's `plastic` flag can be disabled. The already learned chain still
replays with the same units and times.

Ongoing write permission is therefore not required for execution of the acquired route.

## Locus interpretation

The strongest supported interpretation is:

```text
path identity / threshold-crossing capacity
    -> learned ordinary Connection.weight values

temporal calibration
    -> learned ordinary Connection.delay_ms values

not currently supported as durable carriers
    -> membrane potential
    -> adaptation / refractory state
    -> pending queue
    -> unit-local controller trace
    -> receptor set
    -> fixed edge existence
```

This is a positive result for direct physical storage relative to explicit G1/G2 runtime tables.
However, it is not yet a positive result for broadly distributed Field memory. The representation is
still edge-local and pairwise:

```text
source unit -> target unit
weight + delay
```

That can be interpreted as a physicalized transition table embedded in the recurrent substrate. RV01
must therefore retain the pairwise-storage limitation and test generic trainable recurrent-network
explanations directly.

## Validation

GitHub Actions run `33289918236` passed on Python 3.11 and Python 3.13:

```text
Install:           PASS
Ruff lint:         PASS
Local readiness:  PASS
Full pytest:       PASS
Bundle validation: PASS
```

## Next gate

R01-09 separates three claims that are often conflated:

1. the effect is not produced by an external readout or generator;
2. the effect is not a passive fixed-reservoir response;
3. the effect may still be fully explained by a generic trainable recurrent network.

The first two can be tested causally. The third remains a live alternative unless RV01 later shows a
capability or learning property that matched recurrent comparators cannot reproduce.
