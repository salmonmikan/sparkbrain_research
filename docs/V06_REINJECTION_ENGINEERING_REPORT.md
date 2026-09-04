# SparkBrain v0.6 Reinjection Engineering Report

## Scope

V06-06 connects a registered G1/G2 `EndogenousPulseProposal` to the retained v0.4 temporal
excitable Field. It establishes a normal-rule path for internal predictions but does not yet run a
forward-completion experiment.

## Core contract

```text
G1/G2 proposal
    ↓
provenance and pending-state check
    ↓
confidence / energy / depth / lifetime / branch gates
    ↓
ordinary SynapticArrival
    ↓
retained Field integration
    ↓
sub-threshold state or Spark under ordinary rules
```

The gate does not construct a `SpikeEvent`. It schedules current into a target unit. The Field then
applies its existing membrane decay, signed current integration, dynamic threshold, refractory,
adaptation, inhibition, recurrent propagation, and event-count safety limits.

## Confidence and current

The reference effective current is bounded as:

```text
effective = polarity * min(max_current, magnitude * confidence**power * gain)
```

This is an engineering rule, not a biological claim. Confidence below the configured minimum
produces no queue mutation. A weak accepted proposal may change membrane potential without firing.

## Safety gates

The implementation rejects or fails closed on:

- unregistered or content-mismatched proposals;
- already resolved proposals;
- duplicate scheduling;
- arrivals in the past;
- expired proposals;
- low confidence;
- excessive generation depth;
- per-window proposal-budget exhaustion;
- per-origin branch-budget exhaustion;
- per-window energy-budget exhaustion;
- malformed or unknown target units.

## Provenance and learning boundary

Scheduling an endogenous arrival:

- leaves its origin `endogenous-unconfirmed`;
- does not increment external observation counts;
- does not commit an eligible positive update;
- does not confirm another internal proposal.

Later external matching and stale-chain correction remain V06-07 responsibilities.

## Focused tests

The V06-06 focused tests verify:

- sub-threshold reinjection does not force a Spark;
- sufficient current can fire only through the ordinary threshold;
- refractory state applies to reinjected arrivals;
- low-confidence rejection leaves the Field unchanged;
- unregistered and modified proposal rejection;
- generation-depth and duplicate bounds;
- energy, per-window proposal, and branch budgets;
- unknown-target failure before queue mutation;
- deterministic Assembly-free gate state;
- no positive learning or external observation from reinjection alone.

## CI

GitHub Actions run `33248216849` passed on Python 3.11 and Python 3.13, including installation,
Ruff, local readiness, the default test suite, and bundle validation.

## Claim boundary

This result supports only that internally originated predictions can be re-entered into the actual
Field computation path without bypassing the retained excitation rules. It does not support forward
missing-middle completion, a Field-embedded internal model, reality correction, semantic meaning,
functional utility, or a localized memory substrate.
