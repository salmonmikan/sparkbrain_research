# RV01 R01-07 — Physical Revision and Reacquisition Report

## Decision

R01-07 tests whether the same local, externally gated physical-plasticity rule can replace an
acquired route, later reacquire it, and preserve the intermediate costs of revision without G1, G2,
reward, correct-target labels, or confirmed/contradicted path counters.

```text
initial old route acquired:                    YES
new route becomes active after reversal:       YES
old route becomes active after reacquisition:  YES
stable world invents an alternative:           NO
potentiation without competition removes old:  NO
endogenous-only experience revises weights:    NO
connection reset removes learned behaviour:    YES
connection transplant moves reversed behaviour:YES
G1 / G2 runtime required:                      NO
```

The canonical physical revision candidate is supported. It also exposes a real transient no-route
interval during both reversal and reacquisition.

## Physical setup

Two routes share the same prefix:

```text
old: 0 -> 1 -> 2 -> 3
new: 0 -> 1 -> 4 -> 5
```

The runtime is a `TemporalExcitableField` whose durable acquired state is stored in ordinary
connection weights and delays. The competitive learning controller keeps only short-lived unit-local
external traces and updates locally outgoing physical edges.

It does not store:

```text
confirmed_count
contradicted_count
correct_target
correct_action
relation_table
path_score
reward
```

## Acquisition

After externally observing only the old sequence:

```text
later Field route: 1 -> 2 -> 3
old gateway weight: 0.9597959895689502
new gateway weight: 0.0
```

The unobserved alternative is not emitted.

## Reversal

Four externally observed new-route episodes are applied through the same local rule.

Observed probe sequence after each episode:

```text
reversal step 1: 1                no completed route
reversal step 2: 1                no completed route
reversal step 3: 1 -> 4 -> 5      new route active
reversal step 4: 1 -> 4 -> 5      new route retained
```

At the final reversed state:

```text
old gateway weight: 0.11065306597126337
new gateway weight: 1.2130613194252668
reversal crossing episode: 3
```

The two-episode no-route period is not hidden or counted as successful revision. It is a physical
switching cost caused by depression of the former route before the new route becomes sufficiently
strong.

## Reacquisition

Four old-route episodes are then presented again.

```text
reacquisition step 1: 1 -> 4 -> 5  new route still active
reacquisition step 2: 1            transient no-route interval
reacquisition step 3: 1 -> 2 -> 3  old route active again
reacquisition step 4: 1 -> 2 -> 3  old route retained
```

At the final reacquired state:

```text
old gateway weight: 1.25
new gateway weight: 0.36391839582758
reacquisition crossing episode: 3
```

Again, the intermediate no-route interval is preserved as evidence rather than retrospectively
rewritten as continuous success.

## Stable-world control

Continuing to present the old sequence does not create or activate the unobserved new route.

```text
stable later route: 1 -> 2 -> 3
new route completed: false
```

## Potentiation-only control

A rule that strengthens observed edges but does not locally depress competing outgoing edges leaves
both routes active after reversal.

```text
old route completed: true
new route completed: true
```

Thus the physical switch is not explained by accumulating a second route while silently retaining
the first. Local competition is necessary in this canonical construction.

## Endogenous-only control

Presenting the new sequence as unconfirmed endogenous activity produces:

```text
ignored endogenous observations: 16
connection revision:              none
later route:                      old route only
```

Internally generated activity cannot make its proposed future self-confirming.

## Reset and transplant

Resetting ordinary connection weights and delays removes both acquired routes. Transplanting the
reversed physical connection state into a naive compatible Field transfers the new-route behaviour.

The donor and receiver begin their probes with the same naive membrane, adaptation, refractory,
queue, and counter state. Behaviour moves with the physical connection state.

## Interpretation

The strongest supported statement is:

> In a small canonical Field, externally gated local competition can revise and reacquire a learned
> physical route using only ordinary connection weights and delays. The effect is reset-sensitive,
> transplantable, and unavailable to endogenous-only self-training. Revision is not instantaneous:
> the observed physical Dynamics contain transient periods in which neither route completes.

This is stronger than a static physical-chain result, but it remains a dense, hand-configured,
pairwise connection system. It does not yet establish sparse scaling, robust continual learning,
distributed non-edge-local memory, or architectural superiority over generic trainable recurrent
networks.

## Validation

GitHub Actions run `33289354560` passed on Python 3.11 and Python 3.13:

```text
Install:           PASS
Ruff lint:         PASS
Local readiness:  PASS
Full pytest:       PASS
Bundle validation: PASS
```

## Next gate

R01-08 decomposes the learned physical state into connection weights, delays, unit dynamic state,
short-lived traces, receptor support, fixed topology, and ongoing plasticity. The purpose is to state
precisely where continuation resides rather than calling every Field-owned value distributed memory.
