# RV01 R01-09B — Echo-State Reservoir Comparison Report

## Decision

R01-09B implements an actual deterministic Echo State Network-style recurrent comparator rather
than another output lookup.

```text
RV01 physical Field reproduces 0 -> 1 -> 2 -> 3:        YES
fixed recurrent reservoir + learned readout reproduces it: YES
same current token, different prior context changes output: YES
context-state ablation collapses the difference:           YES
equal branch evidence retains two candidate probabilities: YES
readout refit reverses and reacquires a route:              YES
learned readout transplant reproduces behaviour:           YES
generated tokens self-train the comparator:                 NO
resource-matched architectural comparison completed:       NO
RV01 architectural uniqueness established:                 NO
generic recurrent explanation remains viable:              YES
```

The passive output-only explanation rejected in R01-09A remains rejected. A genuine recurrent-state
explanation does not.

## Comparator architecture

`FixedEchoStateAutoregressor` contains:

- deterministic fixed random input weights;
- deterministic fixed sparse recurrent weights;
- leaky recurrent hidden state;
- a learned linear ridge-regression readout;
- autoregressive rollout;
- learned-readout reset and transplant;
- no import from the RV01 physical Field runtime.

Only the readout is fitted. The random recurrent substrate remains fixed.

The reference comparator uses:

```text
token count:              6
reservoir units:         24
fixed parameters:       720
learned readout values: 150
training transitions:    15 for the canonical continuation assay
```

This is deliberately not resource matched to the four-unit RV01 Field. The result tests explanatory
possibility, not efficiency or superiority.

## Basic continuation

Training:

```text
0 -> 1 -> 2 -> 3
```

From prefix `0`, the reservoir autoregressively emits:

```text
1 -> 2 -> 3
```

The RV01 learned physical Field emits the same sequence. Therefore the basic continuation capability
is non-unique.

## Same current token, different prior context

The recurrent comparator is trained on:

```text
0 -> 1 -> 2 -> 4
0 -> 3 -> 2 -> 5
```

At the prediction point, the current token is `2` in both cases.

```text
prefix 0,1,2 -> token 4
prefix 0,3,2 -> token 5
```

The hidden-state hashes differ. Thus the comparator exhibits the same broad form:

```text
response = F(current input, prior internal state)
```

that motivated SparkBrain.

When the recurrent context is reset immediately before the last token, both prefixes produce the
same hidden-state hash and the context-specific prediction collapses. This is an explicit causal
intervention on the comparator's recurrent state.

## Branch ambiguity

Equal training evidence is supplied for:

```text
0 -> 1 -> 2 -> 4
0 -> 1 -> 3 -> 5
```

At prefix `0,1`, tokens `2` and `3` are the top two readout candidates and receive equal probability
mass. The comparator can therefore preserve multiple alternatives at its output distribution rather
than being restricted to one deterministic lookup.

This does not make the output probabilities equivalent to simultaneous physical Field branches. It
shows that branch uncertainty alone does not distinguish RV01 from recurrent alternatives.

## Revision and reacquisition

The readout is fitted successively to:

```text
old: 0 -> 1 -> 2 -> 3
new: 0 -> 1 -> 4 -> 5
old: 0 -> 1 -> 2 -> 3
```

Observed rollout:

```text
acquired: 1 -> 2 -> 3
reversed: 1 -> 4 -> 5
returned: 1 -> 2 -> 3
```

The learned readout hash changes under reversal and returns to the original value after the original
training set is restored. Transplanting the acquired readout state into an identical fixed reservoir
reproduces the acquired route.

This revision is supervised batch refitting, not the same online local physical learning rule used by
RV01. It nevertheless remains a viable capability-level alternative.

## Self-confirmation boundary

Autoregressively generated tokens do not modify the learned readout. The learned-state dictionary is
byte-equivalent before and after rollout.

The comparator therefore does not pass its own generated future back as positive training evidence.

## Interpretation

R01-09A established:

> RV01's internal trajectory is not merely a presentation-layer cue-to-sequence lookup.

R01-09B establishes the limiting counterpart:

> A fixed recurrent reservoir with a trained readout can reproduce the basic continuation, maintain
> context-sensitive internal state, represent branch uncertainty, reverse and reacquire a route
> under refitting, and transfer behaviour with learned-state transplant.

Therefore the following claim is rejected:

```text
RV01 continuation itself proves a new or unique recurrent architecture.
```

The following narrower claim remains supported:

```text
RV01 stores and executes the canonical route inside ordinary intervenable physical connection state,
without G1/G2 runtime tables or an external sequence readout.
```

## Remaining fair-comparison requirements

Architectural comparison still requires:

- matched or explicitly normalized parameter/state budgets;
- the same online exposure stream rather than comparator batch refitting;
- the same local-information restrictions;
- timing and energy metrics;
- identical branch, noise, omission, reversal, and continual-learning worlds;
- matched intervention definitions;
- held-out seeds and topology changes;
- strongest failure-world reporting.

Until those tests are complete, the generic trainable recurrent explanation remains viable.

## Validation

The integrated RV01 branch CI covering the reservoir implementation and focused tests passed on
Python 3.11 and Python 3.13. The suite verifies deterministic replay, learned-state non-mutation,
context ablation, ambiguity, refit revision, transplant, invalid-contract rejection, and comparator
isolation from the RV01 Field runtime.

## Next gate

R01-10 reconstructs post-hoc relation candidates from physically different trajectories while
requiring Observer removal and taxonomy renaming to leave the runtime byte-equivalent.
