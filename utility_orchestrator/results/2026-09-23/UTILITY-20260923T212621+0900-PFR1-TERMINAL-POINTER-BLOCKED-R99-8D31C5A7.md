# Utility terminal-assignment reconciliation — R99 refresh

schema_version: 2
generation_id: UTILITY-20260923T212621+0900-PFR1-TERMINAL-POINTER-BLOCKED-R99-8D31C5A7
produced_at: 2026-09-23T21:26:21+09:00
producer_run_id: utility-auto-20260923T212621+0900-pfr1-terminal-pointer-reconcile
mode: FAIL_CLOSED
status: BLOCKED
selected_task: PFR1_TERMINAL_ASSIGNMENT_POINTER_RECONCILIATION
fast_forge_support: false
scientific_authority: NONE

## Assignment / lifecycle

Control-owned `utility_orchestrator/assignment/current.md` remains schema-v2 `ACTIVE` for the exact PF-R1 development-provenance preservation assignment. That assignment has `max_runs: 1`; Utility already completed the one authorized run, exact-byte durability was verified, and Evidence Analyst R99 independently records PF-R1 as `COMPLETED`, `run_count: 1`, `max_runs: 1`, `DURABLY_AVAILABLE_EXACT_BYTES_VERIFIED`.

The terminal assignment was not re-executed. Because the pointer is not clean IDLE, Utility did not enter Autonomous Idle and did not perform Fast Forge support. The existing append-only completion-acknowledgement request remains open; no duplicate request was created.

## Ownership checks immediately before mutation

- Evidence Analyst: `EVA-20260923T210010+0900-R99-6F2B8C14` at `59dbcdc2e3541e78a64f64e16fa0be5ef38efc26`.
- MAIN/Relay: `MAIN-20260923T205800+0900-PRIMARY-H7-FORMAL-R5-R98-BLOCKED-SIDECAR` at `ops/orchestrator-run-report@fa292cf3a2484c513d3f90372ca9f014948f5c1d`; H7 readiness is blocked before identity/start on protected-sidecar capability.
- Fast Forge: `FORGE-20260923T193417+0900-NOOP-H7-PREFETCH-R97`; no Forge object, no promotion proposal, no independent opening.
- Control: `CTRL-20260923T155900+0900-R43-A91C4E6B` at `1592c3b52a8a545aa2503fd4618c0a761921ef1e`.
- Stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`.

## Material observations

Evidence Analyst R99 supersedes the prior R97/R98 H7 FORMAL GO after direct NON_RESULT readiness failed closed at the concealed protected-sidecar capability check. No FORMAL identity was created or consumed, no STARTED was created, no protected evaluation was accessed, no official scoring occurred, and no new scientific result was produced. H7 is now a nonterminal integrity/capability hold. Candidate #35 is temporarily reprioritized for MAIN-only NON_RESULT preserve-before-read/provenance work under the no-executable-mechanism exception; candidate response execution remains STOP pending fresh Analyst.

These changes do not create Utility authority. Utility remains blocked solely by the stale terminal assignment pointer and does not touch H7, #35, #34, or any scientific result surface.

## Exact refs

- utility assignment pointer blob: `56309a85df157ac2f3f1b2682ef9fff509d5a679`
- utility pre-run mailbox commit: `6a59edbe80f572a305c5f26234c437317a5eaf99`
- Evidence Analyst commit: `59dbcdc2e3541e78a64f64e16fa0be5ef38efc26`
- MAIN/Relay commit: `fa292cf3a2484c513d3f90372ca9f014948f5c1d`
- Fast Forge state blob: `1ac1997bdac3263b44aa467eb397707a46bc76f8`
- Control commit: `1592c3b52a8a545aa2503fd4618c0a761921ef1e`
- H7 science branch/head: `research/main-h7-formal-r5-runtime-identity-r88-cycle12@2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`
- H7 controller branch/head: `research/main-h7-r5-oneway-controller-r98@f21dc7521af7413adcc46a2561271e0b8852f371`
- Candidate #35 branch/head: `research/main-cand35-queue-free-subthreshold-architecture-r96-cycle3@8ea6581544c642ad74f1a95955ab2c5f795afccc`
- existing Control-action request: `utility_orchestrator/requests/UTILREQ-20260923T192250+0900-PFR1-COMPLETION-ACK-POINTER-CLOSE.md`

## Hard floor

- terminal PF-R1 assignment re-executed: false
- rerun/reconstruct/regenerate/retune/rescore: false
- PRE_FORMAL/FORMAL action: false
- identity created/consumed: false
- protected/held-out access: false
- official scoring: false
- result-bearing workflow dispatched: false
- scientific branch mutation: false
- immutable/formal/sealed/evidence/control/preserve destructive mutation: false
- scheduler mutation: false
- research PR merge: false
- MAIN/Relay/Forge ownership collision: false

## Stop reason / follow-up

stop_reason: TERMINAL_ASSIGNMENT_STILL_ACTIVE_PENDING_CONTROL_ACK_FAIL_CLOSED

follow_up_recommendation: Control should acknowledge the already-completed exact PF-R1 assignment generation and compare-and-swap close/archive it; return the pointer to clean schema-v2 IDLE if no distinct new assignment is intended. Utility must not re-execute the consumed assignment or fall through to Autonomous Idle before that reconciliation.

request_created: none
new_scientific_result: false
