# Utility P0 State Pointer Reconciliation

schema_version: 2
autonomous_task_id: AUTOUTIL-20260929T172819+0900-P0-STATE-POINTER-RECONCILE
produced_at: 2026-09-29T17:28:19+09:00
assignment_mode: AUTONOMOUS_IDLE
status: STARTED
max_runs: 1
evidentiary_status: NON_EVIDENTIARY_OPERATIONAL_DIAGNOSTIC_ONLY
scientific_authority: NONE

Objective: reconcile the stale Utility moving state pointer against the durable 15:28 terminal result and verify the Utility-owned Contents update surface.

Trigger: P0 remains OPEN; Utility state.json is stale at the 03:27 generation despite a durable 15:28 terminal result.

Ownership: Control R122; Analyst R169; MAIN R192; Relay unallocated; M1-002 remains PRIMARY MAIN at 2a21d3e879f1db4e81a58273180ad2124e823a5e; SB003 remains ALLOCATED_CONDITIONAL_INACTIVE; active-index blob 1ba1e173344f36e14d0e21e6f3e823254e031f7d; no directive delta.

Allowed: Utility-owned append-only publication and state-pointer reconciliation/readback only.
Forbidden: PR, merge, workflow, scheduler, science, SYSTEM_BUILD, non-Utility mutation, force push, or overwrite of newer generation.
Stop: on verified reconciliation or exhausted five-attempt publication ceiling.
