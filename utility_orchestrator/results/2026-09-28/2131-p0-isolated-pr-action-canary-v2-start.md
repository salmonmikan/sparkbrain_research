# Utility P0 isolated PR action canary v2 — start

schema_version: 2
generation_id: UTILITY-20260928T213104+0900-P0-ISOLATED-PR-ACTION-CANARY-V2
assignment_mode: AUTONOMOUS_IDLE
autonomous_task_id: UTILITY-20260928T213104+0900-P0-ISOLATED-PR-ACTION-CANARY-V2
status: IN_PROGRESS
max_runs: 1
evidentiary_status: NON_EVIDENTIARY_OPERATIONAL_DIAGNOSTIC_ONLY
scientific_authority: NONE

Objective: isolate the current pull-request creation action from MAIN by testing one draft PR between two fresh Utility-owned canary branches, without targeting main or any scientific/build branch.

Trigger/source: open incident INC-GITHUB-MUTATION-RECURRENCE-20260928-001; Control R113; MAIN R178 five-of-five pre-GitHub PR-create refusals while MAIN report publication succeeded.

Directive freshness: ops/human-directives head 8ce979b9ec0bc7eede5225c0403698f8886d3e8d, active-index blob 1ba1e173344f36e14d0e21e6f3e823254e031f7d, no delta from prior durable Utility state.

Ownership checks: Control-owned Utility assignment is schema-v2 clean IDLE; durable Analyst is R167; MAIN R178 owns M1-002; Relay is unallocated. No MAIN, M1-002, scientific, FORMAL, evidence, scheduler, or other-role mailbox mutation is permitted.

Allowed actions: create one fresh Utility-owned base branch and one head branch from current main, add one inert marker to the head, attempt one draft PR creation purpose under the five-total-attempt ceiling with fresh readback before retries, read back result, close the draft PR if created, then publish Utility-owned diagnostic state/results.

Forbidden actions: merge; target main with the canary PR; workflow dispatch; scientific execution; FORMAL/immutable/evidence mutation; scheduler mutation; force push; bypass of any refused boundary.

Stop condition: stop PR creation on first verified success or after five total failed attempts; complete after Utility-owned diagnostic publication.
