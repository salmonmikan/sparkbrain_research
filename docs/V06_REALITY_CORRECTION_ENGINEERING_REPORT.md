# SparkBrain v0.6 Reality-Correction Engineering Report

## Scope

V06-07 adds external-authoritative reality matching and stale endogenous branch cancellation to the
accepted G1/G2 and Field reinjection foundation. It is an engineering slice; it does not claim
forward missing-middle completion.

## Runtime sequence

```text
pending endogenous proposal(s)
        ↓
external event arrives
        ↓
validate external provenance, time, and target
        ↓
expire stale proposals
        ↓
select at most one matching proposal
        ↓
cancel queued predicted root/descendant arrivals
        ↓
confirm or contradict G2 path
        ↓
schedule actual external current into the Field
```

## Match behavior

A matching external observation:

- cancels the queued endogenous root arrival;
- commits at most one matching G2 eligibility;
- updates only the externally confirmed local path;
- enters the Field as the authoritative current;
- prevents prediction and observation from being double-counted.

## Contradiction behavior

A due incompatible prediction:

- is marked `endogenous-contradicted`;
- receives no positive learning commit;
- lowers the affected local-path reliability;
- has its queued root arrival removed;
- has known descendant arrivals removed when an endogenous Spark has already propagated;
- does not force a total Field reset.

## Descendant provenance

The retained v0.4 Field hashes each Spike into a pulse ID for recurrent delivery. V06-07
reconstructs that deterministic hash after each observed Spark and records which endogenous proposal
roots contributed to the descendant pulse. Queue cancellation can therefore remove tracked
recurrent descendants without consulting an Assembly ID or observer artifact.

This lineage index is runtime provenance, not an Assembly detector. It does not cluster trajectories,
name recurring structures, choose actions, or modify prediction confidence.

## Expiration

An unconfirmed proposal whose lifetime has elapsed is marked `endogenous-expired`, removed from G2
pending state, deprived of positive learning credit, and cancelled from the remaining Field queue.

## Adversarial boundaries

Focused tests cover:

- matching external input replacing a queued prediction without double current;
- contradiction after an endogenous Spark, including descendant-queue cancellation;
- expiry before unrelated external input;
- rejecting an endogenous event presented as reality;
- rejecting duplicate external-event processing;
- allowing one external event to commit at most one matching branch;
- validating the external target before mutation;
- Assembly-free deterministic reality state.

## CI

GitHub Actions run `33249195833` passed on Python 3.11 and Python 3.13. Both jobs passed installation,
Ruff, local readiness, the default test suite, and bundle validation.

## Claim boundary

V06-07 supports the existence of provenance-safe external correction mechanics for pending
endogenous Field activity. It does not support a forward internal model, missing-middle completion,
branch calibration, semantic meaning, functional utility, causal Field pathways, or memory-locus
claims. Those require V06-08 and later gates.
