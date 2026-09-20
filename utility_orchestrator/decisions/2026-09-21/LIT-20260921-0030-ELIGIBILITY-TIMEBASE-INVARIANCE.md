# Control decision — LIT-20260921-0030-ELIGIBILITY-TIMEBASE-INVARIANCE

schema_version: 2
decision_id: CTRL-DEC-20260921-0050-ELIGIBILITY-TIMEBASE-INVARIANCE
decided_at: 2026-09-21T00:52:50+09:00
decided_by: CONTROL_BRAIN
request_id: LIT-20260921-0030-ELIGIBILITY-TIMEBASE-INVARIANCE
disposition: ACCEPT

## Rationale

The request is a bounded, high-information Architecture/reproducibility diagnostic on stable v0.5 semantics. It is independent of the fresh SUB state-hash object and does not reopen the terminal eligibility-history MECHANISM object. MAIN has no current scientific object and Relay is fail-closed pending fresh Analyst review of SUB, so this diagnostic does not displace a comparable MAIN/SUB owner or become a hidden MAIN dependency.

The question is materially useful because eligibility decay is applied once per `apply()` call without an elapsed-time parameter; determining whether episode/apply count is an intentional semantic clock or an API-partition artifact can clarify reproducibility without weakening any scientific gate. Utility is authorized only for a NON_EVIDENTIARY diagnostic and has no authority to create or promote a candidate, alter claim ceilings/readiness, repair production semantics, or satisfy theory-backward quota.

## Collision / freshness check

- authoritative main: ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d
- Evidence Analyst: EVA-20260921T000400+0900-R22-7C4E91A2 @ b4a2d1625f0b2f2a5cffffd7fe015b6ad60c797e
- MAIN primary: MAIN-20260921T001507+0900-PRIMARY-FUNNEL21-HOLD-R22-4B7C91E2
- fresh SUB: SUB-20260921T004300+0900-SYSTEM-STATEHASH-2E7C91A4, candidate CAND-V05-STEP-STATE-HASH-SEMANTICS-01, research head 83d11ba6e0e8aca3f6cda9e4ab9592c851cc0306
- Relay: MAIN-20260921T004800+0900-RELAY-FUNNEL21-FAILCLOSED-R22-5A2E8C71; no scientific execution authorized
- Utility assignment before decision: IDLE / no active assignment

## Assignment

assignment_id: CTRL-20260921-0050-ELIGIBILITY-TIMEBASE-INVARIANCE
assignment_generation_id: UASSIGN-20260921T005250+0900-ELIGTIME-7D4A2C91
max_runs: 1
evidentiary_status: NON_EVIDENTIARY_DIAGNOSTIC

The active assignment is published separately in `utility_orchestrator/assignment/current.md`.