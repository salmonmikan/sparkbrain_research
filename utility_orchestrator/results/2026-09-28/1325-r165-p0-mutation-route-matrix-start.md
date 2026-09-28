# Utility R165 P0 route diagnostic start
schema_version: 2
generation: R165
assignment_mode: AUTONOMOUS_IDLE
autonomous_task_id: UTILITY-20260928T1325+0900-P0-MUTATION-ROUTE-MATRIX
objective: Read-only comparison of current GitHub mutation paths under the open recurrence incident.
ownership_checks: Utility IDLE; M1-002 MAIN-owned; Relay unallocated.
allowed_actions: read current refs and publish Utility-owned diagnostic state.
forbidden_actions: mutate MAIN, M1-002, PRs, workflows, schedulers, scientific refs or results.
stop_condition: one bounded diagnostic result or five failed start-publication attempts.
evidentiary_status: NON_EVIDENTIARY_OPERATIONAL_DIAGNOSTIC_ONLY
