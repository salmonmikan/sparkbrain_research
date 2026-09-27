# Utility autonomous task start — SB002 integration readback

schema_version: 2
started_at: 2026-09-28T03:27:29+09:00
assignment_mode: AUTONOMOUS_IDLE
autonomous_task_id: UTILITY-AUTO-20260928T032729+0900-SB002-INTEGRATION-READBACK
max_runs: 1
evidentiary_status: NON_EVIDENTIARY_INTEGRATION_AND_PROVENANCE_RECONCILIATION_ONLY

## Objective

Independently verify the Evidence Analyst R160 to MAIN R165 SB002 integration transaction, including exact-head/tree binding, PR/CI/merge identity, durable MAIN publication, and the post-merge ownership boundary.

## Trigger / source

- Utility assignment pointer is schema-v2 clean IDLE.
- HUMAN-20260928-001 prioritizes integrated-system acceleration and explicitly permits Utility provenance/readback verification outside MAIN's critical path.
- Evidence Analyst R160 authorized exact-head SB002 PR integration.
- MAIN R165 reports SB002 integrated to main and stopped for fresh Analyst reconciliation.

## Ownership checks at start

- Control: CTRL-20260927T235243+0900-R98-RD006-V4-AUDIT-RECONCILIATION
- Evidence Analyst: EVA-20260928T025931+0900-R160-SB002-EXACT-HEAD-INTEGRATION-AUTHORITY
- MAIN: MAIN-20260928T032256+0900-PRIMARY-R165-SB002-INTEGRATED
- MAIN status: SYSTEM_BUILD_SB002_INTEGRATED_COMPLETE_WAIT_ANALYST
- Relay allocation: none; scheduler remains Control-owned dependency wait
- SB002 owner at integration: MAIN
- main head at task start: 76b0cc94edf0fec2e46d69978e0794a37759b862

## Allowed actions

- Read-only verification of R160 authority/receipt, R165 history/latest/state/lease, PR #158, CI, main/source refs and commit/tree identity.
- Read-only ownership/collision reconciliation.
- Utility-owned start/result/state publication only.

## Forbidden actions

- No SB002 code, test, PR, main, system-build or scientific artifact mutation.
- No scientific execution, comparator run, scoring, rescore, held-out access or result reinterpretation.
- No mutation of Analyst, MAIN, Control or scheduler state.
- No inference of a next SYSTEM_BUILD milestone before fresh Analyst/Control authority.

## Stop condition

Stop after one bounded readback report, or immediately if Analyst/MAIN ownership materially supersedes R160/R165 during the final freshness check.
