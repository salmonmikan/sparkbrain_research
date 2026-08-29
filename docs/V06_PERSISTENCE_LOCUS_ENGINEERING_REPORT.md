# SparkBrain v0.6 Persistence-Locus Engineering Report

## Scope

V06-13 asks where the experience-dependent effects demonstrated by V06-08 and V06-12 are actually
stored. It uses direct reset and transplant rather than adding a new memory module.

The result is intentionally constraining: in the current canonical construction, the tested effects
follow explicit anonymous transition and consistency state. A distributed Field persistence carrier
is not supported by this initial suite.

This is an engineering localization result, not a complete causal decomposition of every v0.6 state
component.

## Question

For each candidate carrier:

```text
necessity:
reset the component -> does the learned effect disappear?

partial sufficiency:
transplant the component into a matched recipient -> does the effect move?

specificity:
transplant unrelated state -> does the response remain absent or redirect appropriately?
```

Recipient Fields are constructed in matched states before the learned component is introduced.

## Local-transition locus

The donor G1 state contains the externally learned anonymous transition:

```text
unit:0 -> unit:1 after approximately 5 ms
```

All recipients receive the same current external event at `unit:0`.

### Transplant

```text
transplant donor G1 state
        -> generated Field Spark: unit:1
```

### Reset

```text
empty G1 state
        -> no generated Spark
```

### Field-only transfer

The donor Field state after the current event is transferred without the learned G1 state.

```text
donor Field state + empty G1 state
        -> no generated Spark
```

### Unrelated learned state

```text
transplant unit:0 -> unit:2 state
        -> generated Field Spark: unit:2
```

The response therefore follows the explicit local-transition state rather than the matched recipient
Field state.

## Anonymous consistency locus

The donor consistency state contains:

```text
port:7 -> unit:8
consistent count: 3
reliability: 0.8
```

A common anonymous `port:7` boundary event is then presented to matched recipient Fields through the
relation-reentry mechanism.

### Transplant

```text
transplant donor consistency state
        -> generated Field Spark: unit:8
```

### Reset

```text
empty consistency state
        -> no generated Spark
```

### Unrelated port

```text
transplant port:9 -> unit:9 state
probe port:7
        -> no generated Spark
```

### Alternate target on the same port

```text
transplant port:7 -> unit:9 state
        -> generated Field Spark: unit:9
```

The re-entry response therefore follows the explicit anonymous consistency state.

## Assessment

The canonical assessment is:

```text
local transition reset removes effect:                  true
local transition transplant moves effect:               true
unrelated local state redirects effect:                  true
Field state alone transfers local effect:                false

consistency reset removes effect:                        true
consistency transplant moves effect:                     true
unrelated-port consistency transfers target effect:      false
alternate same-port consistency redirects effect:        true

recipient Field states matched:                          true
positive self-confirming updates:                        0
explicit-state dominant candidate:                       true
distributed Field persistence supported:                 false
```

## Scientific interpretation

The honest current interpretation is:

> The demonstrated experience-dependent response is principally carried by explicit anonymous G1
> local-transition state and anonymous boundary-consistency state. The Dynamic Field executes and
> thresholds the consequences of those states, but the initial reset/transplant evidence does not
> show that the matched Field state itself carries the learned relation.

This is an important limitation, not a failed test implementation.

The current architecture is therefore best described as:

```text
Dynamic Field
    + explicit anonymous local-transition memory
    + explicit anonymous external-consistency memory
    + normal-rule reinjection and causal boundary coupling
```

rather than as a wholly distributed self-organizing Field memory.

## What remains unresolved

The current suite does not yet separately localize:

- G2 path adaptation beyond the G1 learned-state probe;
- eligibility state;
- threshold/adaptation baselines under a learned protocol;
- learned weight/delay state;
- persistent multi-timescale traces;
- pending endogenous queue state;
- interaction effects among G1, G2, consistency, threshold, and Field residual state;
- necessity/sufficiency across multiple world structures and seeds.

Those components must be tested individually and in combinations before a final persistence-locus
claim.

## Self-confirmation and taxonomy boundary

Transplant evaluation does not create positive learning updates. No scalar reward, correct action,
functional relation type, Assembly state, or semantic label is introduced.

`memory` is used only as an observer description of reset-sensitive and transplantable persistence.
The runtime stores anonymous structural state.

## Focused validation

`tests/v06/test_persistence_locus.py` verifies:

- local-transition state transfers the same-input response;
- resetting local-transition state removes the response;
- matched Field state alone does not transfer it;
- unrelated local state redirects rather than reproduces the donor response;
- consistency state transfers relation-reentry behaviour;
- consistency reset removes it;
- unrelated-port state does not reproduce it;
- alternate same-port state redirects it;
- recipient Field states are matched;
- no positive self-confirmation occurs;
- the suite is deterministic.

GitHub Actions run `33259017964` passed for the current persistence-locus head on Python 3.11 and
Python 3.13, including installation, Ruff, local readiness, the default test suite, and bundle
validation.

## Claim boundary

This result supports an **explicit-state-dominant persistence-locus engineering candidate**. It does
not support distributed Field memory, biological memory equivalence, emergent concepts, semantic
meaning, or confirmatory generalization.

If later component interaction tests do not reveal an independent Field carrier, the final v0.6
report must preserve this limitation rather than adding a new state mechanism to rescue the stronger
claim.
