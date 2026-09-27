# Utility autonomous task start — M1 post-integration provenance readback

schema_version: 2
started_at: 2026-09-28T07:27:00+09:00
assignment_mode: AUTONOMOUS_IDLE
autonomous_task_id: UTILITY-AUTO-20260928T072646+0900-M1-POST-INTEGRATION-PROVENANCE-READBACK
max_runs: 1
evidentiary_status: NON_EVIDENTIARY_INTEGRATION_AND_PROVENANCE_RECONCILIATION_ONLY

## Objective

Independently verify the exact PR, merge, post-merge CI, and atomic MAIN R169 publication for Integrated Prototype Milestone 1, without changing M1 or becoming a MAIN dependency.

## Trigger / source

- Utility assignment pointer is schema-v2 clean IDLE with no active assignment.
- No newer open Utility request exists.
- HUMAN-20260928-001 prioritizes M1 integration and explicitly allows independent Utility provenance/readback verification.
- Evidence Analyst R162 authorized exact-head PR/merge and required post-merge provenance.
- MAIN R169 reports M1 integrated through PR #163 and is stopped for Analyst post-integration reconciliation.

## Ownership checks at start

- Control: CTRL-20260928T065013+0900-R104-M1-WAIT-ANALYST
- Evidence Analyst: EVA-20260928T070312+0900-R162-M1-EXACT-HEAD-PR-MERGE
- MAIN: MAIN-20260928T072510+0900-PRIMARY-R169-M1-INTEGRATED
- Relay: intentionally disabled; no competing allocation
- M1 owner: MAIN
- main: 59fc994b39d0ba02682e972161bb46801592d25b
- MAIN state branch: 53890fc113ba4e9c0680e138376485b11bf0a849

## Allowed actions

- Read-only verification of Analyst R162 exact-head authority.
- Read-only verification of PR #163, source head, mergeability history, PR CI, merge commit/tree, changed paths and post-merge CI.
- Read-only verification of MAIN R169 atomic history/latest/state/lease publication.
- Utility-owned start/result/state publication only.

## Forbidden actions

- No M1 code, tests, source branch, PR, main, Analyst, MAIN, Relay or Control mutation.
- No scientific execution, comparator run, scoring, held-out access or claim reinterpretation.
- No FLY-0/SB003 promotion or mixing.
- No scheduler mutation.

## Stop condition

Stop after one bounded provenance report, or immediately if assignment, Analyst, MAIN, Control, PR, main or exact refs materially supersede the recorded ownership before final publication.
