# EXPLORATORY / NON_EVIDENTIARY — Temporal expectation batch-partition sensitivity

## Scope

- Mode: `discovery`
- Target: `TEMPORAL_EXPECTATION_BATCH_PARTITION_SENSITIVITY_DISCOVERY`
- Exploration cycle: `1/3`
- Base: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- Evidentiary status: `NON_EVIDENTIARY`
- Recommendation: `PROMOTE_TO_ARCHITECTURE_STUDY`

This is a bounded synthetic/integration diagnostic only. It does not use repository datasets, trained checkpoints, formal preserved raw, held-out TEST, official scorers, STARTED identities, or consumed scientific identities.

## Question

Does `IntegratedV04Brain` produce a different internally generated omission history and downstream field trajectory for the exact same external pulse timeline solely because that timeline is partitioned differently across `ingest_pulses` calls?

This is independent of the active MAIN frontier. MAIN owns the v0.5 assembly prototype-lock-in Architecture study. This target stays on the stable v0.4 temporal expectation/transduction integration path and does not touch MAIN's active branch, candidate, workflow, blocker, or immediate successor.

## Prospectively fixed micro-experiment

External input is the same in both arms:

- channel `A`
- pulse times `0, 10, 20, 100 ms`
- magnitude `0.72`
- expectations enabled
- plasticity disabled
- `settle_ms=35`

Only API partition changes.

### Batched arm

One call contains all four pulses: `[0, 10, 20, 100]`.

`ingest_pulses` first calls `expectations.observe(...)` for every input row. The late `100 ms` observation therefore updates the learned interval before the omission poll runs through `135 ms`. The learned interval is `34.5 ms`, so the new deadline is `144.85 ms`; no omission is emitted.

### Split arm

First call: `[0, 10, 20]`, settled to `55 ms`. Second call: `[100]`, settled to `135 ms`.

After the first call the learned interval is `10 ms` and the omission deadline is `33 ms`, so the first call emits `omission:A` at `33 ms`. The later `100 ms` observation then produces the same final learned interval as the batched arm: `34.5 ms`.

## Observation

The branch-local executable regression characterization asserts all of the following against the actual repository implementation:

- both arms end at `135 ms`;
- batched arm omission times: `[]`;
- split arm omission times: `[33.0]`;
- both arms end with `expectations.interval["A"] == 34.5`;
- both arms end with `expectations.last_time["A"] == 100.0`;
- final field state hashes differ.

Thus the same external pulse timeline and the same final expectation state can yield different internally generated prediction-error events and different field trajectories solely from ingestion partition.

## Reduction / interpretation

The effect is fully explainable by current control flow, not by a newly discovered cognitive mechanism:

1. `ingest_pulses` sorts the provided batch.
2. It observes every external pulse in that batch.
3. Only after all observations are consumed does it call `expectations.poll(until_ms=end_ms)`.
4. Omission deadlines that would have occurred between early and late observations in the same batch can therefore be erased by the late observation before polling.

This is an Architecture/API causality and reproducibility concern. It is not scientific evidence and does not support a novelty claim.

## What would falsify or reduce it

A fresh prospectively specified DEV-only Architecture study should reduce the issue to an API artifact if either:

- supported callers obey a fixed batching contract that makes deadline-straddling partitions impossible; or
- an event-time-causal comparator shows that batching differences do not materially change downstream activity/action on representative DEV traces.

If otherwise-identical DEV timelines produce materially different downstream behavior solely from partition choice, the concern survives as an Architecture-level reproducibility failure mode.

## Open scientific / Architecture choices

- supported ingestion and batching contract;
- DEV pulse families and channel cadences;
- deadline-straddling partition family;
- event-time-causal comparator semantics;
- downstream functional observable and horizon;
- resource matching.

Do not continue with rescue tuning on this Discovery branch. Any next-layer study requires fresh Evidence Analyst promotion and a new prospective contract.
