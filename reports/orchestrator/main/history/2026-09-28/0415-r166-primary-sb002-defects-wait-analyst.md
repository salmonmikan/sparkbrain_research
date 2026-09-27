# MAIN PRIMARY R166 — SB002 post-merge defects, waiting for Analyst repair authority

generated_at: 2026-09-28T04:15:57+09:00
generation_id: MAIN-20260928T041557+0900-PRIMARY-R166-SB002-DEFECTS-WAIT-ANALYST
execution_mode: PRIMARY
work_mode: SYSTEM_BUILD
status: SYSTEM_BUILD_SB002_POSTMERGE_DEFECTS_WAIT_ANALYST_REPAIR_AUTHORITY
new_build_result: false
new_scientific_result: false

## Fresh authority and ownership

Current main is `292c80b3e77fd7176eae6329de14882187689ee2`. The latest commit after the SB002 merge changes only Control scheduler role selection and does not alter SB002 code.

The latest complete durable Analyst authority remains R160, `EVA-20260928T025931+0900-R160-SB002-EXACT-HEAD-INTEGRATION-AUTHORITY`, at Analyst target head `6cedfd56ddc3e88e73441ea8b0db59932ccd90fb`. R160 authorized exact-head PR integration, then required MAIN to stop after merge for fresh Analyst reconciliation. It does not authorize post-merge repair or the next IPM1 milestone.

MAIN R165 already completed that authority: PR #158 merged as `76b0cc94edf0fec2e46d69978e0794a37759b862`, with the exact authorized tree `f4806298df53d12a6c1845aaa78ebd8e0c126a73` and successful PR CI `36340192931` on Python 3.11/3.13.

Control R100 at `13e3667ac485ce8857c2e6e8a3363aa32dc54909` records MAIN as waiting for Analyst rolling-contract or repair authority. Relay is disabled in dependency-wait and has no competing allocation.

## Confirmed post-merge engineering defects

Control R99/R100 independently confirmed three defects on main:

- P1 `SB002-DUPLICATE-EVIDENCE-IDENTITY`: repeated delivery can accumulate the same evidence more than once because no stable evidence identity is preserved.
- P2 `SB002-CHECKPOINT-ROUTE-LEDGER-COMPLETENESS`: restore can accept a router component without a corresponding route ledger.
- P2 `SB002-CHECKPOINT-GLOBAL-SEQUENCE-PERMUTATION`: restore does not require evidence sequences to be the unique complete range `1..sequence`.

These are concrete engineering defects rather than a missing-review gate. They invalidate the current operational claim that the integrated implementation is fully bounded-functionally verified until repair and reverification complete.

Current classification:

- built: true
- prior bounded functional verification: true
- current functional verification status: `REPAIR_AND_REVERIFY_REQUIRED`
- comparatively supported: false
- composition contribution: `NOT_ESTABLISHED`
- scientifically novel: false
- scientific credit: 0
- evidentiary status: `NON_EVIDENTIARY_BUILD`

## Disposition

No code, branch, PR, CI, experiment or scientific object was changed in this run. Control's prioritization does not substitute for the Analyst allocation required by `MAIN.md`.

MAIN therefore ends this run in `WAITING_ANALYST_AUTHORITY`. A fresh durable Analyst generation must define the repair target, permitted files/interfaces, acceptance tests, resource/claim boundary and exact stop condition before MAIN starts repair work. The IPM1 rolling contract and FLY-0 direction are likewise not inferred as MAIN execution authority from Human Directive or Control state alone.

No result-bearing science, rerun, retune, rescore, held-out access, immutable-ref mutation or scheduler change occurred.

新しい科学結果: なし
