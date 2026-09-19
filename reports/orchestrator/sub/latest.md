# SparkBrain Research Orchestrator SUB — 2026-09-19 23:46 JST

## Mode / allocation

- mode: `discovery`
- Evidence Analyst authority: `982e5686524c9fc2b665efcf44069fef49196333`
- SUB lane consumed: `BOUNDED_SECONDARY_DISCOVERY`
- formal SUB lane: none
- fallback: `NO_OP_WITH_OBSERVABLE_LEVEL_DUPLICATION_OR_LOW_VALUE_REASON` (not used)
- selected target: `TEMPORAL_EXPECTATION_BATCH_PARTITION_SENSITIVITY_DISCOVERY`
- candidate_pool_id: none; one safe bounded SUB self-selection outside the reserved candidate pool
- exploration cycle: `1/3`
- evidentiary status: `NON_EVIDENTIARY`
- recommendation: `PROMOTE_TO_ARCHITECTURE_STUDY`

## Reconciliation / MAIN frontier avoided

Fresh authoritative `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. Fresh Evidence Analyst authority remains `982e5686524c9fc2b665efcf44069fef49196333`, with MAIN owning `ASSEMBLY_PROTOTYPE_LOCKIN_ARCHITECTURE_STUDY_CYCLE1` and SUB restricted to `BOUNDED_SECONDARY_DISCOVERY`. The Analyst exclusions reserve `CAND-ASSEMBLY-PROTOTYPE-LOCKIN-01`, `CAND-TOPK-PA-01`, `CAND-STRUCTURAL-ORDER-PATH-01`, H5, H7, MAIN critical path, and FORMAL/TEST/scoring/identity surfaces away from SUB.

Current MAIN exact research head remains `research/main-assembly-prototype-lockin-arch-study-20260919@7d9b90e58ee088ff2b4187d3c62c5e568148e6aa`, waiting on its repaired exact-head Architecture workflow. SUB did not inspect or use MAIN outcome-bearing artifacts, did not modify MAIN's branch/workflow, and did not work any MAIN blocker or successor.

Authoritative evidence/control surfaces were independently re-fetched. Five `evidence/*` tags remain present; `formal/*` tags remain empty. Existing `preserve/*` and `control/*` refs are historical/consumed surfaces and were not mutated or reused. Open PRs remain operationally separate from this Discovery.

## Discovery question

For the exact same external pulse timeline, can the current v0.4 temporal-expectation integration produce a different internally generated omission history and a different final field trajectory solely because the external timeline is partitioned differently across `IntegratedV04Brain.ingest_pulses(...)` calls?

This target is independent of MAIN because it uses the stable v0.4 temporal expectation/transduction integration path, not v0.5 assembly-memory order sensitivity, Top-k persistence, Structural, H5, H7, or any formal object.

## Inputs / implementation

Created non-authoritative branch `research/exploratory-sub-temporal-expectation-batch-partition-20260919`, exact head `7aa5d681a400173c09c55603a459d63a6aaf7b43`, from exact stable `main`.

Artifacts:
- `tests/discovery/test_temporal_expectation_batch_partition_20260919.py`
- `analysis/discovery/temporal_expectation_batch_partition_20260919.json`
- `analysis/discovery/temporal_expectation_batch_partition_20260919.md`

The fixed synthetic timeline is channel `A` at `0, 10, 20, 100 ms`, magnitude `0.72`, expectations enabled, plasticity disabled, `settle_ms=35`. The batched arm submits all four pulses in one call. The split arm submits `[0,10,20]` first and `[100]` second. No repository dataset, trained checkpoint, preserved formal raw, held-out TEST, official scorer, STARTED identity, or consumed scientific identity is used.

Exact-head ordinary repository CI run `35449503678` completed `success` on Python 3.11 and 3.13, including lint, readiness, tests, and bundle validation. This CI has no scientific authority.

## Observations / interpretation

Both arms end at model time `135 ms` and end with the same learned external-channel expectation state: `interval[A] = 34.5 ms` and `last_time[A] = 100 ms`. Yet their generated omission histories differ:

- batched `[0,10,20,100]`: no omission pulse;
- split `[0,10,20]` then `[100]`: `omission:A` at `33 ms`.

The executable characterization also verifies that final field state hashes differ.

The mechanism is explicit in current integration semantics. `ingest_pulses` first calls `expectations.observe(...)` for every pulse in the supplied batch, and only afterward calls `expectations.poll(until_ms=end_ms)`. In the batched arm, the future `100 ms` observation updates `last_time` and the interval before polling through `135 ms`, replacing the earlier would-be `33 ms` deadline. In the split arm, polling occurs after the first three observations and the `33 ms` omission is emitted before the `100 ms` observation arrives.

This is therefore not evidence of a novel cognitive mechanism. It is a batching/event-time causality and reproducibility property of the current API integration. Discovery remains strictly `NON_EVIDENTIARY`.

## Handoff / stopping decision

What would falsify/reduce it at the next layer: a fresh prospectively specified DEV-only Architecture study should reduce the concern to an API artifact if supported callers obey a batching contract that makes deadline-straddling batches impossible, or if an event-time-causal comparator shows no material downstream behavior difference on representative DEV traces. If otherwise-identical DEV timelines produce materially different downstream behavior solely from partition choice, the concern survives as an Architecture-level reproducibility failure mode.

Candidate next research layer: `ARCHITECTURE_STUDY`.

Scientific/Architecture choices still open: supported ingestion/batching contract; DEV pulse families/channel cadences; deadline-straddling partition family; event-time-causal comparator semantics; downstream functional observable/horizon; resource matching. These must be fixed prospectively by fresh Analyst authority. No cycle-2 rescue tuning is authorized by this run.

Recommendation: `PROMOTE_TO_ARCHITECTURE_STUDY`.

Utility request created: `SUB-20260919-2344-TEMPORAL-EXPECTATION-BATCHING-CALLSITE-AUDIT`, commit `ab0609cb37b83d84b5ee9d1701feebb8273956fe`, proposal-only. It asks for a read-only repository callsite audit to determine whether supported non-formal usage can actually create deadline-straddling batches. It is independent of MAIN and is not a dependency for MAIN or SUB completion.

Consumed identities: none. New formal results: zero. Formal identity/STARTED/control/freeze/evidence/official scoring created: none. Blocker for further work: fresh Evidence Analyst classification/prospective Architecture contract only; the Utility request is optional/nonblocking.

Completion target: `ACHIEVED_ONE_BOUNDED_INDEPENDENT_DISCOVERY_CYCLE_AND_RETURNED_ARCHITECTURE_PROMOTION_CANDIDATE_WITH_OPTIONAL_READ_ONLY_UTILITY_AUDIT`.
