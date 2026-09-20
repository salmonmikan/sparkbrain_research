# MAIN PRIMARY — Receptor simultaneity ordering Architecture cycle 1

Timestamp: `2026-09-20 10:19 JST`  
Worker role: `main`  
Execution mode: `PRIMARY`  
Evidence Analyst authority: `639a5f7baba926502965bc9fea4cdcfb9f749068`  
Research layer: `ARCHITECTURE_STUDY`  
Candidate: `CAND-V05-RECEPTOR-SIMULTANEITY-ORDERING-01`  
Exploration cycle: `DISCOVERY 1 / ARCHITECTURE_STUDY 1`

## Allocation / integrity

FAST PATH remained valid. Stable `main` re-fetched at `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; the latest Evidence Analyst handoff remained `639a5f7baba926502965bc9fea4cdcfb9f749068`; the prior MAIN lease was `COMPLETED`, so no fresh same-object MAIN collision existed. Current SUB work is already completed and is the independent Discovery that produced this promotion candidate; MAIN did not absorb any other SUB lane. Authoritative `evidence/*` remains five annotated tags. Preserve/control refs remain present and open PRs remain unrelated governance work. No integrity disagreement required FULL RECONCILIATION.

## Prospective binding and static characterization

MAIN created `research/main-v05-receptor-simultaneity-ordering-contract-arch-study-20260920` from exact stable main. The prospective contract was fixed before interpretation at commit `00ab02d9b9acd9a68090858cac21f1ea2fa5e244`, binding:

- `src/sparkbrain/v05/receptors.py@86c1cfea1ea70cada5c277d8f5047c32ea611a5c`
- `src/sparkbrain/v05/brain.py@652552f8dc6a53a68e441f593e9bfd82cebb9f7c`
- `src/sparkbrain/v04/contracts.py@9d3ae216a518ff6d409a67cd02f34f1dc20a8ab8`
- `src/sparkbrain/v05/worlds.py@454b05c0347a58687b7d0c50c3a56dd744164946`
- `tests/v05/test_v05_receptors.py@acab9ff77f9abfbe5a5961b5f8ef88ac980b94a3`

Raw machine facts were persisted before interpretation at `6dbc696e4e8b2b4bab62067c3297edb02da9605e`. No dynamic permutation diagnostic or aggregation comparator was run.

## NON_EVIDENTIARY Architecture result

The fixed terminal mapped once to **`ORDER_UNSPECIFIED_AND_REACHABILITY_UNESTABLISHED`** on final research head `705b652f0eb426c7e39a75a9f901be10483d0e63`.

`SignalPulse` and the public receptor/brain API do not prohibit duplicate exact `(time_ms, channel)` keys. `MultiTimescaleReceptorBank.process()` and `IntegratedV05Brain.process_episode()` both sort only by `(time_ms, channel)`, so exact-key ties retain caller iterable order under stable sorting, and receptor gain/state is updated sequentially per pulse. However, stable-main supported docs/tests do not declare exact-key tie order to be intentional semantics, do not declare exact-key simultaneous events to be an unordered multiset, and canonical v0.5 worlds/callers do not intentionally demonstrate duplicate exact `(time_ms, channel)` events. The named v0.4 simultaneous world uses distinct channels at one timestamp, while v0.5 `order_shuffle` uses a temporal event multiset rather than specifying same-key tie behavior.

Therefore this cycle establishes only an **API/reproducibility corner whose ordering semantics are unspecified and whose supported same-key reachability is not established**. It does not establish a scientific mechanism, a supported-path failure, or a need for aggregation. Any dynamic comparator or API policy is a fresh object requiring fresh Analyst authority.

This is **NON_EVIDENTIARY ARCHITECTURE_STUDY** information only. New FORMAL scientific evidence: `none`. New PRE_FORMAL development evidence: `none`.

## Workflow / stop state

Exact-head ordinary CI run `35481067945` is currently `in_progress` on head `705b652f0eb426c7e39a75a9f901be10483d0e63`. It is repository-integrity confirmation only and cannot alter the already fixed terminal.

No official TEST, formal identity, STARTED marker, scorer, preserve/evidence mutation, consumed-identity retry, production source mutation, dynamic probe, rerun/retune, same-run cycle 2, PRE_FORMAL/FORMAL promotion, merge, or Utility request occurred.

Stop reason: **`VALID_STATIC_TERMINAL_MAPPED_WAITING_EXACT_HEAD_ORDINARY_CI`**.  
Final lease target: **`WAITING_EXTERNAL`**.  
Next MAIN/Relay action: collect only CI run `35481067945` for exact head `705b652f0eb426c7e39a75a9f901be10483d0e63`; if successful, persist `COMPLETED` and STOP for fresh Evidence Analyst review. Do not run another receptor permutation diagnostic, aggregation comparator, cycle 2, PRE_FORMAL, or FORMAL continuation.

Work left for SUB: only genuinely independent bounded Discovery under current Analyst allocation; do not continue this receptor object.  
Utility request created: `none`.  
Persistence result: MAIN-owned latest/state/lease/history fast-forward persistence on `ops/orchestrator-run-report`; no force push.
