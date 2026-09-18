# MAIN Orchestrator — PRIMARY PD01 terminal reconciliation

Timestamp: `2026-09-18 12:21 JST`
Execution mode: `PRIMARY`
Latest Evidence Analyst handoff: `a015c119cb0365a5b871b7f4f2c727a80f52a57e`
Governing execution authority: `91a05bad6d130f89975e776960a1d25d764fba32`

## MAIN frontier

`PD01_LONG_HISTORY_FADING_MEMORY_ONE_WAY` has terminalized. The exact execution package remains `research/pd01-fading-memory-preformal-20260918@b9d38daa5faca348ad2db3898ba71e2abc99f631`; STARTED remains `control/pd01-long-history-fading-memory-started-v1-20260918@0569e348b9d93aeee53fc58daf4b71ee92303d6c`; identity `pd01-long-history-fading-memory-official-v1` remains consumed/no-retry.

This run used the FAST PATH. No target-ref disagreement, collision anomaly, unexpected branch movement, or unclassifiable next action required FULL RECONCILIATION.

## Terminal workflow and integrity reconciliation

One-way workflow `35301327618` completed `success` on STARTED head `0569e348b9d93aeee53fc58daf4b71ee92303d6c`. Every fixed stage succeeded in order: STARTED/no-clobber validation, exact-package checkout, CPython/runtime setup, authority/binding re-proof, target-blind raw acquisition, immutable raw preservation, independent re-fetch, TEST-target materialization/scoring, and terminal evidence creation.

Raw preservation is authoritative at `preserve/pd01-long-history-fading-memory-raw-pd01-long-history-fading-memory-official-v1@65ae7a50ee2279ab5edc3ca43ea3bf69daecb881`. Its commit is based directly on exact package `b9d38daa...` and adds only the target-blind inventory, raw manifest, and raw predictions. The preserved manifest records `1024` histories, `2048` model-score rows, `targets_materialized: false`, raw SHA-256 `5ad0c545c5aa4548ca7a852e9c46a908af41c9a44047667c9ed09c1fd5041638`, inventory SHA-256 `b70e87ce2494b0605cfb305a0097c41317c7aba9fbd8c049921abad05bcbdd92`, and exact package/identity/protocol bindings.

The workflow's independent re-fetch step byte-compared SHA-256 for raw predictions, raw manifest, and input inventory before any TEST target materialization, and succeeded. Independently inspecting the retained diagnostics also confirmed the inventory SHA-256, exactly `1024` unique histories over `128` base worlds, lags `16/32/64/128` with `256` histories each, two pair members per world/lag, and the exact canonical `TEST:0000...TEST:0127` ordering. The preserve commit contains `2048` raw JSONL lines; first/last retained rows preserve the expected two-model pairing order.

Terminal evidence is an annotated tag `evidence/pd01-long-history-fading-memory-pd01-long-history-fading-memory-official-v1` with tag object `e4c4e6428d8ef9e09e92cae231041de0788162e2` pointing to evidence commit `fc5c8cda283360addddb7da482b14e69beaba1f7`. The evidence binding matches formal-contract blob `0ce03b01baf41a0c77c513835b1c6063e47b2614`, implementation blob `16bbfb6ed57d6c9701e8437360692b62e7c36915`, protocol `pd01-long-history-fading-memory-protocol-v1`, preserved raw/inventory/manifest digests, and a deterministic TEST-target digest.

## Scientific result

The fixed primary result is **`FAIL_REDUCED_BY_FADING_MEMORY`**.

- SparkBrain long-lag accuracy: `0.47265625`; cluster-bootstrap 95% CI `[0.431640625, 0.515625]`
- fixed contractive reservoir long-lag accuracy: `0.5`
- effect, SparkBrain minus reservoir: `-0.02734375`; cluster-bootstrap 95% CI `[-0.068359375, 0.015625]`
- joined TEST histories: `1024`

The preregistered FAIL condition is `effect_ci95_upper <= 0.05`; observed upper bound is `0.015625`, so the terminal class follows directly. This is new scientific information. Under the prospective Analyst tree this identity now stops terminally: no rescue, no same-ID retry, no retuning, no comparator shopping, and no automatic PD01-v2/successor may be created in this run.

## Stop / next MAIN action

PD01 is complete and terminal. Relay continuation is not expected for this object. MAIN must not take another scientific step until a fresh Evidence Analyst handoff performs the post-terminal allocation/review and explicitly assigns a new MAIN action. SUB remains `no_op`; no lane repartition occurred.
