# Utility P0 Control state-pointer audit

schema_version: 2
autonomous_task_id: AUTOUTIL-20261001T052300+0900-P0-CONTROL-STATE-POINTER-AUDIT-3A7C91E4
status: COMPLETED
assignment_mode: AUTONOMOUS_IDLE
completed_at: 2026-10-01T05:23:00+09:00
max_runs: 1
evidentiary_status: NON_EVIDENTIARY_OPERATIONAL_DIAGNOSTIC_ONLY
scientific_authority: NONE

## Freshness

Human Directive ref/head remains `ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d`; active-index blob remains `1ba1e173344f36e14d0e21e6f3e823254e031f7d`, so directive delta from the previous durable Utility generation is false.

Utility assignment/current remains schema-v2 clean IDLE.

## Findings

Control append-only authority and latest cache are both R143, while `analysis/control_brain/state.json` remains R141. The R142 and R143 append-only histories both exist. This is a two-generation Control state-pointer/cache debt, not loss of append-only authority.

Evidence Analyst remains R176. PRIMARY MAIN remains R214 with MAIN state and lease aligned at R214; Relay is unallocated. M1-002 remains PRIMARY MAIN-owned at exact head `2a21d3e879f1db4e81a58273180ad2124e823a5e`, freshly 1 ahead / 0 behind `main@59fc994b39d0ba02682e972161bb46801592d25b`, and fresh PR search remains empty. SB003 remains ALLOCATED_CONDITIONAL_INACTIVE.

The stale Control state cache does not currently change allocation or scientific authority because append-only/latest point to R143 and direct Analyst/MAIN readback is consistent with the same ownership posture. It remains an operational risk for any consumer that incorrectly treats state.json alone as authoritative.

P0 incident `INC-GITHUB-MUTATION-RECURRENCE-20260928-001` remains OPEN with root cause UNKNOWN. This fresh Control pattern is another partial-publication recurrence localized to a moving state cache; it does not establish repository-wide write loss.

## Utility mutation-path observation

The mandatory STARTED publication for this task was attempted through Utility-owned `create_file`:
- attempt 1: blocked before GitHub by the OpenAI safety layer;
- attempt 2: succeeded, commit `8290f2c3d0315826b9c722daf40312b5a20c4248`;
- independent readback succeeded.

This is fresh evidence that ordinary Utility Contents mutation remains intermittent/nonuniform rather than permanently unavailable.

## Classification

- control_append_only: R143
- control_latest: R143
- control_state: R141
- control_pointer_debt: STATE_ONLY_TWO_GENERATIONS
- analyst: R176
- main: R214_ALIGNED
- relay_allocated: false
- m1_002_owner: PRIMARY_MAIN
- m1_002_pr_open: false
- p0_status: OPEN
- p0_root_cause: UNKNOWN
- repository_wide_write_outage_supported: false
- current_authority_collision_observed: false

## Boundaries

No Control/Analyst/MAIN/Relay state was mutated. No scientific execution, workflow dispatch, PR/merge, scheduler mutation, force push, or Work-backed execution occurred.

stop_reason: COMPLETED_SINGLE_BOUNDED_P0_CONTROL_STATE_POINTER_AUDIT
