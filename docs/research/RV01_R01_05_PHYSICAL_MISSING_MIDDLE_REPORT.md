# RV01 R01-05 — Physical Missing-Middle Report

## Decision

R01-05 tests whether the physical connection state learned in R01-03/04 can bridge a missing middle
state before a later external event arrives, and whether that internally generated state causally
contributes to the later internal trajectory.

```text
forward missing middle generated:                   YES
downstream state generated before later input:      YES
future external D/H preloaded in queue:              NO
targeted middle-edge suppression removes main D:    YES
matched active control suppression preserves main:  YES
matched control path is itself impaired:             YES
intervention strength matched:                       YES
untrained Field completes the gap:                   NO
G1/G2 or tolerant matcher used:                      NO
selective causal effect:                             1.0
```

This is a canonical engineering candidate for Gate E. It is not a held-out or multi-scale completion
result.

## Training world

Two independent physical sequences are learned in the same uniform eight-unit Field:

```text
main:    0 -> 1 -> 2 -> 3
control: 4 -> 5 -> 6 -> 7
```

The durable acquired state is stored only in ordinary connection weights and delays. All short-lived
external unit traces are cleared before the assay.

## Test input

Every intact, intervention, and untrained condition receives the exact same external schedule:

```text
100 ms  unit:0  main cue A
100 ms  unit:4  control cue E
105 ms  unit:1  main prefix B
105 ms  unit:5  control prefix F

120 ms  unit:3  later external D
120 ms  unit:7  later external H
```

Units 2 and 6 are omitted.

The Field first runs only to 119 ms. External D and H are not scheduled until after that forward
window. Their external event IDs are therefore absent from the event queue while completion is being
measured.

## Intact physical Field

Before the later external events are scheduled, the Field produces:

```text
100.000 ms  units 0, 4   external cues
105.000 ms  units 1, 5   external prefixes
110.375 ms  units 2, 6   internally propagated missing states
115.750 ms  units 3, 7   internally propagated downstream states
```

The main path therefore contains:

```text
A -> B -> endogenous C -> endogenous D
```

with both C and D generated before external D at 120 ms.

## Targeted causal intervention

The learned physical edge:

```text
unit:1 -> unit:2
```

is set to zero while all other learned physical state and all current input are retained.

Result before 120 ms:

```text
main C: absent
main D: absent
control G: present
control H: present
```

The downstream main state is therefore not merely correlated with the prefix; it depends on the
learned physical route through the omitted middle state.

## Active matched intervention

The corresponding learned control edge:

```text
unit:5 -> unit:6
```

is suppressed with exactly the same pre-intervention weight, delay, and post-intervention weight.
Both paths are active in the same run.

Result before 120 ms:

```text
main C: present
main D: present
control G: absent
control H: absent
```

Thus the main impairment is selective rather than a generic consequence of editing one learned edge.

## Untrained control

The uniform untrained Field receives the same six external events. Before 120 ms it produces only the
externally supplied cue/prefix units:

```text
0, 4, 1, 5
```

Neither omitted middle nor downstream state is generated.

## Late external events

Only after the forward assay ends are the external D/H events scheduled at 120 ms. They are processed
normally in all conditions. Their later arrival cannot explain the pre-120 ms C/D or G/H activity.

## No matcher shortcut

The R01-05 route contains no:

- G1 `LocalTemporalExpectation`;
- G2 `SparseLocalTransitionAdaptation`;
- `EndogenousPulseProposal` scheduler;
- Assembly or motif detector;
- similarity or tolerance matcher;
- explicit missing-target identifier;
- future-event lookup.

The evidence is the ordinary physical Field trajectory itself.

## Interpretation

The strongest supported statement is:

> In a canonical physical Field, an externally learned connection-and-delay pattern can generate an
> omitted middle state and a downstream state before the corresponding later external event exists in
> the queue. Suppressing the physical route into the missing state selectively removes the downstream
> state, while an equally strong active control intervention does not impair the main path.

This is stronger than merely recognizing an incomplete pattern. It remains a small deterministic
sequence with explicit external unit placement, pre-existing dense connectivity, fixed local learning
parameters, and no external contradiction/cancellation mechanism in the RV01 physical route yet.

## Validation

GitHub Actions run `33288877153` passed on Python 3.11 and Python 3.13:

```text
Install:           PASS
Ruff lint:         PASS
Local readiness:  PASS
Full pytest:       PASS
Bundle validation: PASS
```

## Next gate

R01-06 tests overlapping physical histories. The first requirement is preservation of more than one
supported branch without an explicit winner or branch-state table. Competitive resolution is tracked
separately and is not granted merely because two branches co-fire.
