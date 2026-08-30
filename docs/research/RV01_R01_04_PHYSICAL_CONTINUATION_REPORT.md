# RV01 R01-04 — Physical Endogenous Continuation Report

## Decision

R01-04 tests whether the physical Field connection state produced by R01-03 can itself generate later
normally thresholded activity after a current cue, with G1 and G2 absent from the execution route.

```text
trained physical Field continues:                    YES
untrained uniform Field continues:                   NO
different physical history changes continuation:    YES
connection reset removes continuation:               YES
connection transplant transfers continuation:       YES
short-lived unit-trace reset removes continuation:   NO
endogenous-only training writes continuation:        NO
G1 or G2 runtime required:                           NO
```

This is the first RV01 engineering candidate in which a learned temporal transition is executed from
ordinary physical Field connection weights and delays rather than from `LocalTemporalExpectation` or
`SparseLocalTransitionAdaptation`.

## Training and execution separation

Training uses the externally gated R01-03 rule on the observed sequence:

```text
0 -> 1 -> 2 -> 3
```

After training:

- all controller unit-local traces are cleared;
- the Field membrane, adaptation, refractory, queue, spike counters, and current time remain naive;
- no G1 or G2 object is constructed;
- only ordinary `Connection.weight` and `Connection.delay_ms` differ from the untrained Field.

The later test supplies one current cue:

```text
external unit:0 at 100 ms
```

## Trained Field result

The normally thresholded Field trace is:

```text
unit:0  at 100.000 ms  external cue
unit:1  at 105.375 ms  physical propagation
unit:2  at 110.750 ms  physical propagation
unit:3  at 116.125 ms  physical propagation
```

The later chain is therefore:

```text
1 -> 2 -> 3
```

No future unit event is inserted by a proposal scheduler. Each later event is produced when current
travels over the learned ordinary connection graph and crosses the retained Field threshold.

## Untrained control

The uniform untrained Field receives the same cue and produces only:

```text
unit:0 at 100 ms
```

Its weak uniform recurrent edges do not cross the downstream threshold.

## Different-history control

A second Field is trained on:

```text
0 -> 2 -> 1 -> 3
```

With the same later cue and the same naive dynamic state, it produces:

```text
2 -> 1 -> 3
```

Thus:

```text
same current cue
same initial membrane/adaptation/queue state
different acquired physical connection state
    -> different later Field trajectory
```

## Connection reset

Resetting all connection weights and delays to the uniform pretraining values removes the later
continuation completely.

## Connection transplant

Only learned connection weights, delays, and plastic flags are copied into a naive compatible Field.
The receiver then reproduces the donor's:

```text
later units: 1 -> 2 -> 3
later times: 105.375, 110.750, 116.125 ms
```

The donor and receiver begin from the same naive dynamic Field state. The continuation therefore moves
with the physical connection state.

## Working-trace reset

Clearing every short-lived external unit trace after training does not change the learned connection
hash and does not remove continuation. The controller trace is not the long-lived carrier in this
assay.

## Endogenous-only training control

Presenting the same training sequence as `ENDOGENOUS_UNCONFIRMED` changes no connection and produces
no later continuation under the cue.

```text
external observations during training: 0
ignored endogenous training events:   12
physical connection updates:            0
```

## Interpretation

The strongest supported statement is:

> In a canonical four-unit engineering Field, externally observed temporal order can be stored in
> ordinary physical connection weights and delays. After all learning traces are removed, that state
> is sufficient to generate a history-dependent, normally thresholded endogenous continuation under
> the same current cue. Reset removes the effect and transplant moves it to a naive compatible Field.

This is materially stronger than R01-03 because the physical state is now used as the execution
substrate. It remains a small deterministic construction with a pre-existing dense topology and does
not yet establish robust missing-middle completion, ambiguity preservation, revision, sparse scaling,
or differentiation from reservoir-style recurrent memory.

## Validation

GitHub Actions run `33288675962` passed on Python 3.11 and Python 3.13:

```text
Install:           PASS
Ruff lint:         PASS
Local readiness:  PASS
Full pytest:       PASS
Bundle validation: PASS
```

## Next gate

R01-05 supplies only an external prefix, omits the middle unit, and withholds the later external event
until after the forward-assay window. Targeted and active matched physical-edge interventions test
whether the internally generated missing state causally produces the downstream state rather than
merely resembling it under a tolerant matcher.
