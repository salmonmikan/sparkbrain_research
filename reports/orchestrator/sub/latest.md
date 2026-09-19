# SparkBrain Research Orchestrator SUB — 2026-09-20 00:41 JST

## Mode / allocation

- mode: `discovery`
- Evidence Analyst authority: `862dd62cdce58f06e5c782b4b54212d93e40212e`
- SUB lane consumed: `BOUNDED_SECONDARY_DISCOVERY`
- formal SUB lane: none
- fallback: `NO_OP_WITH_OBSERVABLE_LEVEL_DUPLICATION_OR_LOW_VALUE_REASON` (not used)
- selected target: `FIELD_SOURCE_LINEAGE_CAP_PERMUTATION_SENSITIVITY_DISCOVERY`
- candidate_pool_id: none; one safe bounded SUB self-selection outside the MAIN-reserved candidate pool
- exploration cycle: `1/3`
- evidentiary status: `NON_EVIDENTIARY`
- recommendation: `REJECT`

## MAIN frontier avoided / integrity

Fresh `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d` and fresh Evidence Analyst authority remains `862dd62cdce58f06e5c782b4b54212d93e40212e`. MAIN owns `CAND-TEMPORAL-BATCH-PARTITION-01` on `research/main-temporal-batch-partition-arch-study-20260920@7fa4391bbf34cf25e10b708ce64acddf07bf7f42`; SUB did not continue that candidate, inspect outcome-bearing Architecture artifacts, modify MAIN's branch, or take any MAIN blocker/successor. MAIN workflow `35451528895` completed successfully during this run, but its scientific artifacts were deliberately not opened by SUB.

Five authoritative evidence tags remain present; formal/sealed/freeze tags remain empty and 13 legacy freeze branches remain preserved. No consumed identity, official TEST, formal raw/scorer, STARTED/control, preserve/evidence authority, immutable evidence, or merge surface was touched.

## Discovery implementation / observations

Created non-authoritative branch `research/exploratory-sub-field-source-lineage-cap-20260920` from exact stable main. Test commit: `1a91187173a713d87f343b871ec16b94ee956bfb`; prospective question/reduction binding and exact research head: `21af9d2a5546cc081f4fe4472540ab8a17760c7c`.

The fixed synthetic experiment uses one field unit, no recurrent connections, `max_sources_per_unit=16`, and twenty distinct simultaneous arrivals `p00..p19` at `1.0 ms`, each with current `0.06`. Only enqueue order changes. Exact-head ordinary CI `35452444346` completed `success` on Python 3.11 and 3.13.

Both arms emit exactly one spike and have identical physical spike observables and identical unit state once `source_pulse_ids` is removed. Ascending enqueue retains `p04..p19`; descending enqueue retains `p15..p00`. The retained sets have Jaccard `0.6`, while full `field.state_hash()` differs because bounded source provenance is serialized.

The result is exactly explained by current implementation: same-time arrivals preserve insertion-counter order; `_source_tuple` appends unseen IDs and keeps only the last 16. Current production-code search found no source-ID consumer that changes current, threshold, refractory, adaptation, or another physical update. This is bounded provenance-buffer bookkeeping/reproducibility sensitivity, not a new memory or causal mechanism.

## Handoff / stop

Evidentiary status: `NON_EVIDENTIARY`. Recommendation: `REJECT`. Candidate next scientific layer: `NONE_SCIENTIFICALLY`. Keep only an engineering note that full state hashes can differ from provenance ordering while the physical state projection is identical.

What would falsify the reduction is a fresh current-code path where source IDs themselves causally affect physical updates or downstream behavior under otherwise identical currents/timestamps/targets; none was found. Scientific choices still open: none. No cycle-2 tuning/sweep is warranted.

Utility request created: none. Consumed identities: none. New formal results: zero. Blockers: none.

Completion target: `ACHIEVED_ONE_BOUNDED_INDEPENDENT_DISCOVERY_CYCLE_AND_STOPPED_AFTER_EXACT_BOOKKEEPING_REDUCTION`.
