# MAIN Orchestrator — RELAY C19-R1 successor-v2

Timestamp: `2026-09-18 03:45 JST`
Execution mode: `RELAY`
Evidence Analyst authority: `966018058f296098805982a8d206102741c3842c`

## MAIN frontier

The active MAIN object is the prospectively authorized final operational successor for C19-R1:

- package branch/head: `research/c19-r1-revision-authority-runtime-closed-v2-20260918@a23975c5713347eaa459161f538a8f0c3db6152e`
- identity: `c19-r1-revision-authority-official-v2`
- protocol: `c19-r1-revision-authority-protocol-v2`
- STARTED ref/commit: `control/c19-r1-revision-authority-started-v2-20260918@a230e250021cea113c42d674da2bfc31dc0a3549`
- one-way workflow: `35260650772`

## Relay reconciliation

The prior PRIMARY lease was `WAITING_EXTERNAL` with heartbeat `03:21 JST`, older than the 20-minute collision window. No newer lease appeared before mutation. The exact package head remained `a23975c...`; Evidence Analyst tip remained exactly `966018...`; the planned STARTED and preserve namespaces were absent and the planned evidence tag was absent.

Both exact-head pre-START gates are green on `a23975c...`:

- dedicated pre-START `35258035210` — `success`
- ordinary CI `35258035223` — `success`

The consumed-v1 -> successor-v2 diff remains exactly the four prospectively allowed operational files. Frozen scientific contract/protocol/preregistration bindings and the readiness-derived runtime manifest were unchanged.

## STARTED / one-way transition

Current Analyst contingency `R1_V2_PRE_START_READY` explicitly permits fresh STARTED followed by exactly one one-way execution when all gates remain clean. Relay therefore created the STARTED ref from the exact package SHA and added only:

`artifacts/v03/c19_external_validation/r1/official_v2/STARTED.json`

The STARTED marker binds:

- Evidence Analyst `966018058f296098805982a8d206102741c3842c`
- exact package `a23975c5713347eaa459161f538a8f0c3db6152e`
- scientific protocol v1 + execution protocol v2
- identity `c19-r1-revision-authority-official-v2`
- runtime manifest `cdb7a2a075f76d4b65b51fc7d0b46f7ecda98646e33902420b2a7e5b7d604fc5`
- both successful admission runs
- `no_retry: true`

Package -> STARTED comparison confirms the STARTED JSON is the only changed path.

The configured exactly-once one-way workflow `35260650772` was triggered from STARTED commit `a230e250...` and is currently `in_progress`.

## Scientific / integrity state

There is no new scientific result at this checkpoint. STARTED has now crossed the one-way boundary, so successor-v2 is consumed and may never be retried or repaired as the same identity.

No preserve/evidence result has yet been claimed. The prior consumed v1 remains untouched. No SUB-reserved work was touched.

## Stop / next relay action

Lease is `WAITING_EXTERNAL`; no useful local critical-path work remains while workflow `35260650772` runs.

Next MAIN/RELAY must collect that same workflow only:

- SUCCESS: independently verify preserve/evidence refs and terminal classification, persist terminal state, STOP before any new object.
- FAILURE after STARTED: preserve diagnostics, classify `R1_V2_POST_START_FAILURE`, keep v2 consumed/no-retry, terminate the R1 reduction line, and create no automatic v3.
