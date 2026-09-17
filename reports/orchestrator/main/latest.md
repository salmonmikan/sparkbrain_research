# MAIN Orchestrator — RELAY C19-R2 authority packaging

Timestamp: `2026-09-18 06:58 JST`
Execution mode: `RELAY`
Evidence Analyst authority: `719b9e74063e5e10f6226fd49f1835036ed75e5b`

## MAIN frontier

RELAY continued the prospectively authorized C19-R2 critical path. The frozen scientific package remains `5d5d171cf872baed7a636fd246ab36f3a91a6716`; its scientific contract, seven-state mechanism, transition/reset/readout, scoring method, cluster definition, seeds, thresholds and success criteria were not changed.

The operational execution envelope is now at `research/c19-r2-fsa-state-tracker-spec-20260918@5a8155af6d6d7dacaa4413386d2a93c4eda3ca08`, with fresh identity `c19-r2-fsa-state-tracker-official-v1` prospectively bound but still unSTARTED and unconsumed.

## Authority packaging and mechanical fix

The authorized package now includes exact identity/Analyst binding, STARTED/preserve/evidence namespaces, a target-blind R2 runner, raw+manifest+target-free `atomic_idx` source-map preservation, preserve/refetch-before-target scoring, and a one-way workflow.

The first authority-package pre-START run `35279107972` failed before any scientific/runtime gate at Ruff lint only: 20 `E501` line-length findings in the newly added operational scripts. RELAY classified this under the prospectively allowed mechanical pre-START fix path and changed formatting only. No behavior or scientific semantics were changed.

Final exact head after that formatting-only repair is `5a8155af6d6d7dacaa4413386d2a93c4eda3ca08`.

## Final exact-head validation

- dedicated R2 pre-START `35279500982`: `in_progress` at handoff;
- ordinary CI `35279500925`: `in_progress` at handoff.

The current Evidence Analyst tip was re-fetched and remains `719b9e74063e5e10f6226fd49f1835036ed75e5b`.

## STARTED / evidence boundary

No STARTED ref was created. No official R2 data was accessed. No raw/preserve/evidence ref was created. No R2 scoring occurred. The identity remains unconsumed.

Lease is `WAITING_EXTERNAL`. The next MAIN/RELAY may create STARTED exactly once only after both final-head checks complete successfully and fresh Analyst/head/identity/control/preserve/evidence collision checks remain clean.

## New scientific information

None. This run produced operational readiness/authority progress only. The observed pre-START failure was lint-only and has no scientific interpretation.
