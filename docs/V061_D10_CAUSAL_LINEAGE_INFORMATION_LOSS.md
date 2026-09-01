# v0.6.1 D10 — Causal Lineage Information-Loss Audit

## Scope

Static observer-side source audit. Candidate-003 is not re-executed and the Primary runtime is not modified.

## Outbound boundary lineage

`BoundaryEvent` retains:

```text
generation_depth
source_proposal_ids
source_spark_id
source_state_hash
source_unit_id
```

The outbound event therefore has enough information to identify the Spark, unit, proposal lineage, generation depth, and source state that reached the world boundary.

## Consistency compression

| State class | Stored fields | Proposal/path return address |
|---|---|---|
| AnonymousLinkState | port_id, target, polarity, consistent_count, inconsistent_count, mean_lag_ms, lag_m2, mean_magnitude_ratio, last_boundary_event_id, last_external_event_id | — |
| PortExposureState | boundary_count, externally_paired_count, expired_count | — |

## Audit result

```text
boundary has causal lineage: True
consistency retains proposal return address: False
register_boundary consumes return address: False
re-entry recovers historical return address: False
lineage information loss confirmed: True
first loss boundary: BoundaryEvent -> PendingBoundaryExposure/AnonymousLinkState
```

## Mechanistic interpretation

The current architecture does not merely lack an update call from anonymous world consistency to G1. It loses the historical return address needed to make such an update causally selective.

```text
endogenous proposal/path lineage
    -> Spark
    -> BoundaryEvent  [lineage still present]
    -> PendingBoundaryExposure / AnonymousLinkState
                     [proposal/path return address discarded]
    -> external consistency reliability
    -> relation re-entry from compressed relation
```

Relation re-entry may attach a current boundary lineage to a newly generated proposal. That does not reconstruct the historical local lineage whose prior world consequence established the relation. The stored relation can therefore support a target, but it cannot identify which earlier local temporal process should receive externally evidenced credit or contradiction.

## Consequence for future SparkBrain hypotheses

A future anonymous feedback mechanism needs a bounded, expiring causal return address across the world boundary. Retaining it is not sufficient by itself: the mechanism must still pass lineage-swap, matched-correlation, contradiction, self-confirmation, reset/transplant, and explicit-table-equivalence tests.

The return address must not contain semantic role, reward, correct action, or an evaluator-selected target. It may identify only anonymous causal lineage.
