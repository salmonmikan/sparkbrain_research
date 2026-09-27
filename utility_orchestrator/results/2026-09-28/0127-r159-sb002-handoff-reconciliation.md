# Utility result — R159 / SB002 handoff reconciliation

schema_version: 2
completed_at: 2026-09-28T01:27:40+09:00
assignment_mode: AUTONOMOUS_IDLE
autonomous_task_id: UTILITY-AUTO-20260928T012240+0900-R159-SB002-HANDOFF-RECONCILIATION
status: COMPLETED
classification: R159_BRIDGE_VERIFIED_SB002_MAIN_ACK_PENDING
evidentiary_status: NON_EVIDENTIARY_HANDOFF_AND_PERSISTENCE_RECONCILIATION_ONLY
scientific_authority: NONE

## Result

Evidence Analyst R159 is durably complete through the retained GitHub Actions persistence bridge, and its SB002 allocation has an unambiguous owner and target. MAIN has not yet durably acknowledged R159 and the target branch is not yet present, so this is a normal handoff wait rather than a persistence incident.

## Persistence verification

- request_id: EA-R159-20260928T010015JST
- request branch commit: a2d4203ac8b0d96b8f1cbacf901eb614b9a24285
- request blob: 790aefe083dee0784787666e52d9425bb49675b7
- request SHA-256: fa9c0d7689c0326170afb84f31fb040e1be67b68f2f503ca1b03dbfb6b9ff629
- receipt request SHA-256 match: true
- expected target head: 7e1942e8dfe5fa5333d956ab717e041f79206075
- result commit: 17a58e31127f8e2e47848ef4794f53bcd3908900
- result parent matches expected target head: true
- history exact match: true
- latest exact match: true
- state exact match: true
- receipt persistence_complete: true
- receipt scientific_execution: false
- active pointer debt: none

The persisted state's `REQUEST_TO_BE_PUBLISHED` value is the exact generation-time payload recorded inside the request. It is not treated as present-tense failure evidence because the later durable receipt, containing commit and byte-exact target files independently establish completion.

## Ownership / collision check

- Utility assignment: schema-v2 clean IDLE
- Evidence Analyst: EVA-20260928T010015+0900-R159-SB002-ATOMICITY-CLARIFICATION
- MAIN durable state: MAIN-20260927T233306+0900-PRIMARY-R163-RD006-V4-RETURN-ALIGNMENT-AUDIT
- Control: CTRL-20260927T235243+0900-R98-RD006-V4-AUDIT-RECONCILIATION
- Relay: DEPENDENCY_WAIT_SUSPENDED under Control
- SB002 build_id: BUILD-SB-002-CAUSAL-SCOPE-REVISION-PILOT
- SB002 owner: MAIN
- target branch: system-build/sb002-causal-scope-revision-pilot-20260928
- target branch observed: absent
- MAIN acknowledged R159: false
- collision disposition: Utility did no SB002 work and stopped after reconciliation

## Scope and integrity

No SB002 implementation, build execution, scientific execution, workflow dispatch, scoring, rescore, artifact mutation, branch creation, scientific/control ref mutation or scheduler change was performed.

Canonical science remains unchanged: 35/35 terminal, zero active, zero scientifically queued, eight consumed FORMAL identities. RD005 remains consumed one-way; RD006 v1-v4 remain closed with scientific credit 0. SB002 is NON_EVIDENTIARY_SYSTEM_BUILD only.

P0 remains CLOSED_P0_RECOVERED. This successful bridge verification proves only the tested R159 transaction and does not prove the prior incident's internal root cause.

## Stop / follow-up

stop_reason: R159_TARGET_UNAMBIGUOUS_MAIN_DURABLE_ACK_PENDING
follow_up_recommendation: MAIN should re-fetch R159, implement only R158 plus R159 on the designated SB002 branch, and stop after publication for fresh Analyst reconciliation.
