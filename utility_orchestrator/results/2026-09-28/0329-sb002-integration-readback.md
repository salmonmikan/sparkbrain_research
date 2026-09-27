# Utility result — SB002 exact-tree integration readback

schema_version: 2
completed_at: 2026-09-28T03:29:32+09:00
assignment_mode: AUTONOMOUS_IDLE
autonomous_task_id: UTILITY-AUTO-20260928T032729+0900-SB002-INTEGRATION-READBACK
status: COMPLETED
classification: SB002_EXACT_TREE_INTEGRATION_VERIFIED_ANALYST_RECONCILIATION_PENDING
evidentiary_status: NON_EVIDENTIARY_INTEGRATION_AND_PROVENANCE_RECONCILIATION_ONLY
scientific_authority: NONE

## Result

Evidence Analyst R160's exact-head integration authority and MAIN R165's SB002 merge are durably and transactionally consistent. PR #158 merged the unchanged authorized source head, and the resulting main commit has the exact same tree as the authorized SB002 source tree. MAIN history/latest/state/lease were atomically published as R165 with no active pointer debt.

SB002 is therefore integrated stable substrate as a bounded NON_EVIDENTIARY_BUILD. The next owner is Evidence Analyst for fresh post-merge reconciliation. Utility does not infer a next milestone from HUMAN-20260928-001 and performed no SB002 implementation or scientific work.

## R160 persistence verification

- request_id: EA-R160-20260928T025931JST
- request branch commit: 796972861f0c52a5b4d24f7edb07597fd62d7a0d
- request blob: 438443a9b1cdc22eb665da87a63bae95cb156096
- request SHA-256: fa99e5b53198af9a799f0ba5b7d1d79211406ef76355d5cc7688f4c66335c1ff
- receipt SHA-256 match: true
- expected target head: 17a58e31127f8e2e47848ef4794f53bcd3908900
- result commit: 6cedfd56ddc3e88e73441ea8b0db59932ccd90fb
- result parent matches expected target head: true
- history exact match: true
- latest exact match: true
- state exact match: true
- receipt persistence_complete: true
- receipt scientific_execution: false
- active pointer debt: none

The earlier malformed R160 request remains non-authoritative and was not reused.

## SB002 integration verification

- Analyst-authorized source branch: system-build/sb002-causal-scope-revision-pilot-20260928
- authorized source head: 720e18bcff53be76c861fa8c09d24d5320b90455
- authorized source tree: f4806298df53d12a6c1845aaa78ebd8e0c126a73
- PR: #158
- PR head: 720e18bcff53be76c861fa8c09d24d5320b90455
- PR base before merge: cf0bc45262824f1fe282ccd7b785b3ea50be2099
- PR state: merged
- PR CI run: 36340192931
- PR CI conclusion: success
- changed files: 8
- merge method: squash
- main merge commit: 76b0cc94edf0fec2e46d69978e0794a37759b862
- main merge parent: cf0bc45262824f1fe282ccd7b785b3ea50be2099
- main merge tree: f4806298df53d12a6c1845aaa78ebd8e0c126a73
- source tree equals merge tree: true
- current main head equals merge commit: true

## MAIN durable publication

The single MAIN publication commit `282981a96148e071e2f985bf8b8f60563cda9563` atomically added/updated:

- append-only history: `reports/orchestrator/main/history/2026-09-28/0322-r165-primary-sb002-integrated.md`
- latest cache
- state cache
- lease cache

All four independently read back as MAIN R165. State and lease agree on build ID, Analyst R160, source head, PR #158, merge commit/tree, non-evidentiary status and stop boundary.

## Ownership / collision check

- Utility assignment: schema-v2 clean IDLE
- Control: CTRL-20260927T235243+0900-R98-RD006-V4-AUDIT-RECONCILIATION
- Evidence Analyst: EVA-20260928T025931+0900-R160-SB002-EXACT-HEAD-INTEGRATION-AUTHORITY
- MAIN: MAIN-20260928T032256+0900-PRIMARY-R165-SB002-INTEGRATED
- MAIN status: SYSTEM_BUILD_SB002_INTEGRATED_COMPLETE_WAIT_ANALYST
- Relay allocation: none
- next authority: fresh Evidence Analyst post-merge reconciliation
- collision disposition: Utility performed readback only and did not enter the MAIN critical path

HUMAN-20260928-001 is active human-originated strategic intent but has not yet been durably dispositioned by the observed Control R98 or converted by Analyst R160 into a rolling follow-on contract. It does not independently authorize Utility to select or implement the next SYSTEM_BUILD milestone.

## Claim and integrity boundary

- built: true
- bounded-functionally verified: true
- comparatively supported: false
- composition contribution: NOT_ESTABLISHED
- scientifically novel: false
- scientific credit: 0
- evidentiary status: NON_EVIDENTIARY_BUILD
- new scientific result: false

No experiment, comparator, capability score, RD005/RD006 reuse, terminal-object reopening, held-out access, immutable/evidence ref mutation, Analyst/MAIN/Control mutation or scheduler change was performed.

P0 remains CLOSED_P0_RECOVERED. This successful readback verifies the tested R160/R165/SB002 integration path only; it does not prove the prior incident's internal root cause.

## Stop / follow-up

stop_reason: SB002_INTEGRATION_VERIFIED_FRESH_ANALYST_RECONCILIATION_REQUIRED
follow_up_recommendation: Evidence Analyst should reconcile main commit 76b0cc94edf0fec2e46d69978e0794a37759b862, preserve the non-evidentiary claim boundary, and define any next bounded milestone or rolling SYSTEM_BUILD contract under HUMAN-20260928-001 after Control reconciliation.
