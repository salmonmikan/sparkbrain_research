# RV01 R01-03 — Direct Physical Field Plasticity Report

## Decision

R01-03 implements the smallest current candidate that writes external temporal experience directly
into ordinary `TemporalExcitableField` connection weights and delays.

```text
G1 transition table used:                 NO
G2 path adaptation used:                  NO
reward or correct-action signal used:     NO
pairwise learned controller table used:   NO
long-lived state outside Field edges:     NO
external sequence changes physical edges: YES
endogenous-only activity changes edges:   NO
unit-ID permutation supported:            YES
bounded weights and delays:               YES
```

The engineering mechanism is valid as a direct-physical-plasticity candidate. R01-03 does not by
itself establish that the learned physical state can replace G1/G2 capability; that is tested in
R01-04 and later gates.

## Mechanism

Implementation:

```text
src/sparkbrain/research/rv01/direct_field_plasticity.py
```

The controller receives a sequence of externally originated unit events. Its only working state is a
short-lived trace indexed by the recently observed unit:

```text
unit_id
time_ms
magnitude
external event ID
```

When a later external unit event arrives within the local temporal window:

```text
previous external unit
        ↓ causal lag
current external unit
        ↓
existing physical Connection.weight increases
existing physical Connection.delay moves toward observed lag
```

The reverse physical edge receives bounded anti-causal depression. No new edge is created, and no
persistent source-target proposal, path score, confirmed count, contradicted count, Assembly,
semantic label, reward trace, or expected future target is stored by the controller.

After training, clearing all unit-local traces leaves the learned connection weights and delays
unchanged.

## Canonical setup

The probe begins with a uniform fully connected four-unit Field:

```text
initial weight:    0.05
initial delay:     8.0 ms
base threshold:    0.80
training interval: 5.0 ms
training episodes: 3
```

External training sequence:

```text
0 -> 1 -> 2 -> 3
```

All physical connections initially have the same weight and delay. Therefore the later structured
edge pattern is not supplied by topology initialization.

## Learned physical pattern

After three externally observed episodes:

```text
causal adjacent edges:
0 -> 1
1 -> 2
2 -> 3

weight: 0.05 -> approximately 0.959796
delay:  8.00 -> 5.375 ms
```

Reverse edges:

```text
1 -> 0
2 -> 1
3 -> 2

weight: 0.05 -> 0.0
delay:  remains 8.0 ms
```

All nonadjacent edges remain:

```text
weight: 0.05
delay:  8.0 ms
```

Thus the external temporal order changes the ordinary Field connection graph selectively rather than
creating a separate sequence table.

## Endogenous self-training guard

The same event sequence marked as `ENDOGENOUS_UNCONFIRMED` produces:

```text
external observation count: 0
ignored endogenous count:   12
physical update count:       0
connection hash change:      NO
```

Internally generated activity therefore cannot confirm or strengthen its own physical route in this
candidate.

## Unit permutation

A nonconsecutive sequence is trained with the identical local rule:

```text
3 -> 1 -> 4 -> 0
```

The corresponding causal adjacent edges potentiate and reverse edges depress. The rule contains no
special cases for units 0, 1, 2, or 3.

## Boundedness

After 100 training episodes:

- weights remain within `[0.0, 1.25]`;
- delays remain within `[0.5, 20.0]` ms;
- the repeatedly causal edge saturates at the configured maximum weight;
- its delay converges toward the observed 5 ms lag;
- the reverse edge saturates at the configured minimum weight.

## Difference from earlier plasticity implementations

Existing v0.4/v0.5 plasticity code contains optional reward modulation, and the v0.5 controller owns
a persistent pair-indexed eligibility mapping. R01-03 does not reuse those states as its candidate.
It keeps only short-lived unit-local external traces and writes durable effects directly into the
Field's existing physical connections.

## Interpretation

The strongest supported statement is:

> A category-free, externally gated, unit-local rule can encode an observed temporal order directly
> into ordinary Field connection weights and delays without G1, G2, reward, Assembly, or a learned
> pairwise controller table. The learned state survives removal of the controller's short-lived
> traces, while endogenous-only activity cannot write the same state.

This is not yet evidence of an endogenous cognitive transition substrate. A stronger result requires
that the learned physical Field state itself generate later normally thresholded continuation,
branching, correction, and revision under the RV01 comparison rules.

## Validation

GitHub Actions run `33288605914` passed on Python 3.11 and Python 3.13:

```text
Install:           PASS
Ruff lint:         PASS
Local readiness:  PASS
Full pytest:       PASS
Bundle validation: PASS
```

## Next gate

R01-04 tests whether the connection state learned here, after all unit-local traces are cleared and
without G1/G2 runtime machinery, can produce a history-dependent endogenous Field chain from the same
current cue. It includes untrained, alternate-history, connection-reset, connection-transplant, and
endogenous-only-training controls.
