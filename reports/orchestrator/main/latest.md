# SparkBrain Research Orchestrator — MAIN latest

Timestamp: `2026-09-17T17:47:32+09:00`  
Worker role: `main`  
Evidence Analyst authority consumed: `b9c14e9e171bf765447aa45e71b7ba75cc7ce357`

## MAIN frontier

C19 official-v3 is the primary frontier. MAIN consumed the Analyst-authorized v3 runtime-closure object end-to-end through the prospectively fixed post-START contingency. The exact package is `research/c19-official-v3-runtime-closed-20260917@84b244959f249da916a36906508ead0830052e9b`, protocol `c19-external-v2-official-protocol-v3`, identity `c19-external-v2-official-v3`.

The v3 branch reached exact-head green pre-START validation (`35199692189: success`) and CI (`35199692097: success`). STARTED authority was then created at `control/c19-official-v3-started-20260917@915b7b21abe6ef936fa18e81e4a5117712d20f28`, bound to the exact package and Analyst authority with `no_retry: true` and raw-before-targets/scoring constraints.

## One-way execution and terminal disposition

One-way workflow `35200352569` / job `105133356842` completed with **failure after STARTED**. Exact runtime installation, STARTED/package verification, official input/cache verification, and target-blind acquisition all succeeded. The workflow then failed at `Persist raw predictions immutably before evaluator targets`.

The diagnostic artifact confirms a target-blind run manifest for `95,920` generated rows with raw SHA-256 `fe08f475b2ba7b0e5e38c61595a23bb54863a7bfd66a3d62663442d99f639978`, but the raw predictions themselves were not retained in the diagnostic artifact and no canonical `preserve/*` ref was created. Evaluator targets were never materialized and scoring never started. Therefore there is **no PASS / FAIL / INCONCLUSIVE scientific result** and the diagnostic artifact is not immutable raw evidence.

MAIN classified the event under the Analyst's prospective `V3_POST_START_FAILURE` branch and appended canonical control bookkeeping at `control/c19-official-v3-started-20260917@294d947ade2f906e284d5e1eed5ad57ac7527947`:

- state: `POST_START_FAILURE`
- identity consumed: true
- retry allowed: false
- automatic v4: forbidden
- failure stage: immutable raw preservation after target-blind acquisition and before evaluator targets
- raw generated in workflow: true / 95,920 rows
- raw immutably preserved: false
- evaluator targets materialized: false
- scoring started: false
- terminal scientific result: none
- diagnostic artifact: `10487408980`, diagnostic-only

No v3 `preserve/*` or `evidence/*` authority exists.

## Critical-path fixes completed

Before STARTED, MAIN's v3 critical path closed the earlier runtime-only blockers without changing scientific semantics: exact runtime dependency closure, same-environment import smoke, network-blocked synthetic acquisition smoke, scorer regression in pre-START validation, and exact-head CI. The original import-smoke defect (`scripts` treated as an importable package) was mechanically corrected; the exact head then passed both pre-START and CI.

After STARTED, MAIN did **not** repair-and-rerun the raw-preservation failure. The prospective contingency explicitly requires consume/no-retry/STOP. MAIN only reconciled the workflow, preserved diagnostic metadata, recorded the append-only post-START control disposition, and stopped scientific execution.

## Same-run continuation and stop

Consumed prospective branches: `V3_PRE_START_BLOCKER` -> `V3_PRE_START_READY_FOR_ONE_WAY` -> `V3_POST_START_FAILURE`.

The run stops because `c19-external-v2-official-v3` failed after STARTED. Re-running the identity, silently reconstructing/recovering raw as evidence, repairing preservation and retrying, scoring from a non-authoritative diagnostic artifact, or automatically creating v4 would violate the Analyst handoff. A fresh prospective Evidence Analyst decision is now required.

New scientific information: **none**. New operational/integrity information: the target-blind model path executed successfully under the frozen v3 runtime, but the immutable raw-preservation mechanism failed before any evaluator target or score was opened.

## SUB boundary / concurrency

Formal `sub_lane` and `sub_fallback` remain null. MAIN did not absorb SUB work. Concurrent SUB activity is explicitly NON_EVIDENTIARY exploratory incubation on `research/exploratory-sub-revision-authority-fsa-20260917`; it is independent of C19 and was not used by MAIN.

The latest SUB stream correctly observed the v3 one-way failure without diagnosing or touching it. No Analyst role split was invalidated and no MAIN blocker was delegated to SUB.

## Repository reconciliation

- `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d` remains stable substrate and unprotected.
- open PRs: `0`.
- open operational Issues: `#139`, `#147`; Issue #147 remains operationally stale versus canonical v2/v3 control state.
- consumed v2 identity `c19-external-v2-official-v2` remains untouched/no-retry.
- v3 identity `c19-external-v2-official-v3` is now consumed/no-retry by `POST_START_FAILURE`.
- historical freeze/preserve/formal/evidence authorities were not modified.

## Next MAIN action

**STOP and return to Evidence Analyst.** Do not retry v3 and do not design or create v4 in this run. The next Analyst must consume `control/c19-official-v3-started-20260917@294d947ade2f906e284d5e1eed5ad57ac7527947` and decide prospectively whether C19 terminates or whether any new distinct object is scientifically justified.
