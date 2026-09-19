# EXPLORATORY / NON_EVIDENTIARY — bounded field source-lineage cap

## Scope

- target: `FIELD_SOURCE_LINEAGE_CAP_PERMUTATION_SENSITIVITY_DISCOVERY`
- exploration cycle: `1/3`
- source: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- relevant source blobs: `src/sparkbrain/v04/field.py@e2279d69cd04030238317361d5ee3abdc1009c32`, `src/sparkbrain/v04/topology.py@9129161bd2e7f7cd0ec70684e176700f128d4a6b`, `src/sparkbrain/v04/contracts.py@9d3ae216a518ff6d409a67cd02f34f1dc20a8ab8`
- evidentiary status: `NON_EVIDENTIARY`

This target is independent of MAIN's temporal-expectation batch-partition Architecture study. It operates directly on a synthetic `TemporalExcitableField` with expectations, assembly memory, learned routing, formal identities, held-out TEST, official scoring, and preserved raw evidence absent.

## Question

When more than `max_sources_per_unit` distinct simultaneous arrivals hit the same unit, can enqueue order alone change the retained source lineage and serialized state hash while leaving the physical field dynamics invariant?

The current implementation groups same-time arrivals by target, preserves heap insertion order through a monotonic counter, appends unseen `pulse_id` values in that order, and keeps only the last `max_sources_per_unit` entries. The default cap is 16. Source IDs are not used in current/threshold/refractory/adaptation calculations.

## Fixed synthetic micro-experiment

Use a one-unit field with no recurrent connections and `max_sources_per_unit=16`. Schedule the identical multiset of twenty arrivals at `1.0 ms`, each with current `0.06`, target unit 0, and unique pulse IDs `p00..p19`. Compare only two enqueue orders: ascending and descending pulse ID order. Run exactly through `1.0 ms`.

Record the emitted spike's retained `source_pulse_ids`, spike physical observables, the unit physical state with `source_pulse_ids` removed, and the full serialized state hash.

## Prospective interpretation

- If retained lineage differs but physical spike/unit state is identical, reduce the observation to bounded provenance-buffer insertion-order semantics. Recommendation: `REJECT` as a scientific candidate; retain only an engineering/reproducibility note that full state hashes include bounded provenance metadata.
- If physical dynamics differ despite identical arrival currents/timestamps/targets, the reduction fails and the target may warrant `PROMOTE_TO_ARCHITECTURE_STUDY` after fresh Analyst review.
- No parameter sweep, threshold tuning, retry, or cycle-2 rescue is authorized by this file.
