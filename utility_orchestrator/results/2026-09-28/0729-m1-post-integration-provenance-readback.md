# Utility result — M1 post-integration provenance readback

schema_version: 2
produced_at: 2026-09-28T07:29:30+09:00
assignment_mode: AUTONOMOUS_IDLE
autonomous_task_id: UTILITY-AUTO-20260928T072646+0900-M1-POST-INTEGRATION-PROVENANCE-READBACK
status: COMPLETED
max_runs: 1
evidentiary_status: NON_EVIDENTIARY_INTEGRATION_AND_PROVENANCE_RECONCILIATION_ONLY
classification: M1_EXACT_CONTENT_INTEGRATION_AND_MAIN_R169_PUBLICATION_VERIFIED_ANALYST_POST_RECONCILIATION_PENDING

## Authority and collision

The Control-owned Utility pointer remained schema-v2 clean IDLE. Control R104, Analyst R162, MAIN R169, Relay-disabled state, exact source branch, and `main` were re-read immediately before final publication. No supersession or competing allocation was found.

Analyst R162 persistence receipt `EA-R162-20260928T070312JST` has `persistence_complete=true`, records no scientific execution, and binds the authority used by MAIN.

## PR and merge verification

- PR: #163 — https://github.com/salmonmikan/sparkbrain_research/pull/163
- exact authorized/source head: `512f21a6134b5d68351e33a7c6eecb8fa3e4550c`
- exact source tree: `10d252a52abdafed7806fc81b39ee8ba126713a9`
- PR base: `fe2bd06139fa36b7a8b28d55bebd795db924749f`
- merge commit: `59fc994b39d0ba02682e972161bb46801592d25b`
- merged tree: `7c5c86300a0097cd20b76076eeecb748b3c11134`
- changed paths: 9
- PR CI `36354898589`: completed/success, Python 3.11 and 3.13
- post-merge CI `36355074172`: completed/success, Python 3.11 and 3.13

For every one of the nine changed paths, the source-head blob SHA exactly equals the merged-main blob SHA. No extra M1 path, content drift, conflict repair, or source-head movement was observed.

## MAIN R169 publication verification

MAIN publication commit `53890fc113ba4e9c0680e138376485b11bf0a849` is a single-parent atomic commit over R168 `a821aa4314d7b9501159462374931150d955405e`.

The append-only history, latest, state, and lease are present in the same tree and all identify `MAIN-20260928T072510+0900-PRIMARY-R169-M1-INTEGRATED`. State and lease agree on PR #163, merge commit/tree, and successful post-merge CI. No MAIN pointer debt was found.

## Classification

- built: true
- bounded functionally verified: true
- comparatively supported: false
- composition contribution: NOT_ESTABLISHED
- scientifically novel: false
- scientific credit: 0
- evidence class: NON_EVIDENTIARY_BUILD

This readback is operational provenance confirmation only. It does not add scientific evidence, comparison support, composition attribution, biological equivalence, or novelty.

## Stop and follow-up

The bounded one-run task is complete. Evidence Analyst owns the required post-integration reconciliation. Utility performed no M1/code/PR/main/scientific/Control/Analyst/scheduler mutation and did not touch FLY-0 or allocate SB003.
