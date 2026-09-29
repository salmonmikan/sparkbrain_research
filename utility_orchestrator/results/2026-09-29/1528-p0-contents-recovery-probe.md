# Utility P0 Contents Recovery Probe

schema_version: 2
autonomous_task_id: AUTOUTIL-20260929T152817+0900-P0-CONTENTS-RECOVERY-PROBE
produced_at: 2026-09-29T15:28:17+09:00
completed_at: 2026-09-29T15:31:00+09:00
assignment_mode: AUTONOMOUS_IDLE
status: COMPLETED
max_runs: 1
evidentiary_status: NON_EVIDENTIARY_OPERATIONAL_DIAGNOSTIC_ONLY
scientific_authority: NONE
incident: INC-GITHUB-MUTATION-RECURRENCE-20260928-001

## Freshness / ownership

- Human Directive index head: `8ce979b9ec0bc7eede5225c0403698f8886d3e8d`
- active-index blob: `1ba1e173344f36e14d0e21e6f3e823254e031f7d`
- directive delta versus prior durable Utility state: none
- Utility assignment: schema-v2 clean IDLE
- durable Control authority: append-only R120
- durable Evidence Analyst: R169
- MAIN: R191
- Relay allocated: false
- M1-002 owner: PRIMARY MAIN
- M1-002 exact head: `2a21d3e879f1db4e81a58273180ad2124e823a5e`
- SB003: `ALLOCATED_CONDITIONAL_INACTIVE`

## Observation

A Utility-owned GitHub Contents `create_file` mutation on
`ops/utility-orchestrator-requests` succeeded on the first attempt at commit
`35f284dfc19995e4fcc32bf59f57fde77b57fb49`, and independent readback
verified the STARTED record.

This succeeded shortly after MAIN R191 recorded five fresh-state
`create_pull_request` attempts, all refused before GitHub, with no PR created.
Control R120 also records five isolated canary PR-create refusals before GitHub.

## Classification

The current sample strengthens the existing bounded P0 classification:
- repository-wide write outage is not supported;
- generic scheduled Contents-create outage is not supported;
- PR creation remains the strongest repeatedly failing mutation surface;
- mutation success/failure is action/path/execution-context/timing sensitive;
- root cause remains UNKNOWN.

A single successful Utility Contents write does not prove fleet-wide recovery and
does not clear P0. It only establishes that this tested Utility-owned Contents
surface was available during this run.

## Collision / integrity

No MAIN/SYSTEM_BUILD source, PR, workflow, scheduler definition, scientific ref,
FORMAL identity, immutable evidence, or another role's mailbox was mutated.
No scientific execution occurred and no scientific credit is created.

## Stop reason

COMPLETED_SINGLE_BOUNDED_P0_CONTENTS_RECOVERY_OBSERVATION

## Follow-up recommendation

Control should keep production and isolated PR-create paths as the primary P0
failure surface while treating generic Contents-write canaries as secondary
health samples rather than proof of recovery.
