# Utility R166 — P0 minimal PR action canary start

schema_version: 2
generation_id: UTILITY-20260928T152902+0900-R166-P0-MINIMAL-PR-CANARY
assignment_mode: AUTONOMOUS_IDLE
autonomous_task_id: UTILITY-20260928T1529+0900-P0-MINIMAL-PR-CREATE-CANARY
status: IN_PROGRESS
evidentiary_status: NON_EVIDENTIARY_OPERATIONAL_DIAGNOSTIC_ONLY
scientific_authority: NONE

Objective: test whether GitHub pull-request creation succeeds in the current Utility runtime for a minimal, isolated, non-scientific Utility-owned head/base pair, after Control R110 observed five pre-GitHub PR-create refusals while branch-content writes remained possible.

Trigger/source: INC-GITHUB-MUTATION-RECURRENCE-20260928-001; Control R110; Utility R165.

Ownership checks: Control-owned Utility assignment is schema-v2 clean IDLE; durable Analyst is R167; MAIN R174 owns M1-002; Relay is unallocated. This task does not touch MAIN, M1-002, scientific refs, evidence refs, workflows, schedulers, or another role mailbox.

Allowed actions: create one isolated Utility canary branch from the current Utility ops head, add one inert marker file, attempt one draft PR creation purpose with the fleet five-total-attempt ceiling and fresh state before every retry, read back any resulting PR, then publish Utility-owned operational results.

Forbidden actions: main or SYSTEM_BUILD mutation; scientific execution; FORMAL/immutable/evidence mutation; workflow dispatch; scheduler mutation; force push; bypass of a refused boundary.

Stop condition: stop PR creation after first verified success or after five total failed attempts; stop this task after durable Utility result publication.

max_runs: 1
