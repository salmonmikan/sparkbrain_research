# RV01 R01-09A — Output Readout and Internal-Causality Report

## Decision

R01-09A compares the RV01 physical Field route with an explicit external sequence readout attached to
a fixed, noncontinuing Field.

```text
fixed Field internally continues:                     NO
external readout can mimic sequence output:            YES
removing readout removes the mimicked output:           YES
internal Field-edge intervention changes readout:       NO
readout-state transplant moves output:                  YES
readout-state transplant moves Field Dynamics:          NO
RV01 Field continues without external readout:          YES
RV01 internal-edge intervention changes Field Dynamics: YES
RV01 connection transplant moves Field Dynamics:        YES
```

The external output-only explanation is rejected for the current internal-causality claim. Generic
trainable recurrent and reservoir-computing explanations remain viable.

## Alternative model

`ExternalSequenceReadout` stores an explicit mapping:

```text
current cue -> externally returned sequence
```

It is deliberately outside the Field. The fixed Field itself remains weak and produces no later
internal unit activity.

After observing:

```text
0 -> 1 -> 2 -> 3
```

the readout can return:

```text
1 -> 2 -> 3
```

from cue `0`, even though the Field still emits no internal continuation.

## Readout removal and transplant

Resetting the learned readout removes the output. Copying its learned state into another readout
restores the output while the attached naive Field remains dynamically silent.

Thus the learned effect moves with the readout object, not with the recurrent physical substrate.

## Internal-edge intervention

Suppressing Field edge `1 -> 2` in the fixed Field does not change the external readout result:

```text
readout before intervention: 1 -> 2 -> 3
readout after intervention:  1 -> 2 -> 3
```

The intervention changes the Field connection hash, but the output-only predictor never consults that
causal route.

## RV01 physical route

In the RV01 condition:

- no external readout is present;
- the trained Field itself emits `1 -> 2 -> 3`;
- the untrained Field emits no continuation;
- targeted suppression of the learned middle edge removes downstream Field activity;
- active matched suppression on a disjoint route preserves the target route;
- transplanting learned ordinary connection state moves the internal trajectory.

Therefore the later units are part of the intervenable recurrent Dynamics rather than a presentation-
layer reconstruction.

## Narrow interpretation

The strongest supported statement is:

> RV01's canonical continuation and missing-middle traces are not generated solely by an external
> cue-to-sequence readout attached to an otherwise noncontinuing Field. Their causal locus is inside
> the learned recurrent connection substrate.

The following stronger statements are not supported:

```text
RV01 is not reservoir computing
RV01 is not a generic recurrent neural network
RV01 is architecturally unique
RV01 is superior to ESN / RNN / GRU / state-space models
```

A fixed recurrent reservoir can possess internally causal state while learning only a readout, and a
trainable recurrent network can store equivalent pairwise weights. Those comparisons remain required
under R01-09B.

## Validation

GitHub Actions runs `33290124637` and `33290142373` passed on Python 3.11 and Python 3.13:

```text
Install:           PASS
Ruff lint:         PASS
Local readiness:  PASS
Full pytest:       PASS
Bundle validation: PASS
```

## Next gate

R01-09B must compare the same frozen canonical tasks against actual recurrent alternatives rather
than an output-only lookup:

- fixed random recurrent reservoir with learned readout;
- Echo State Network-style autoregressive model;
- simple trainable recurrent model where dependencies permit;
- explicit reporting of parameter count, learned-state locus, intervention response, and failure
  cases.

Comparator success is retained as evidence against architectural uniqueness.
