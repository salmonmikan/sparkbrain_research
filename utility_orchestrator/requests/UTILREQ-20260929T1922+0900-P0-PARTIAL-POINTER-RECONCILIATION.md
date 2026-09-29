# Utility request: reconcile fresh Control R124 / MAIN R194 pointer debt

schema_version: 2
request_id: UTILREQ-20260929T1922+0900-P0-PARTIAL-POINTER-RECONCILIATION
created_at: 2026-09-29T19:28:00+09:00
created_by: UTILITY
status: PROPOSED_FOR_CONTROL_ACTION
control_decision_required: true
utility_self_approval: false
scientific_authority: NONE
evidentiary_status: NON_EVIDENTIARY_CONTROL_PLANE_ONLY
incident_id: INC-GITHUB-MUTATION-RECURRENCE-20260928-001

Fresh readback found Control append-only R124 with latest R123/state R122 and MAIN R194 history/state/latest with lease R193.

Requested Control action: reconcile those moving caches without rewriting append-only history; preserve bounded retry/readback, no force push, and no newer-generation overwrite. No scientific, PR/merge, scheduler, or Utility mutation of Control/MAIN state is requested.

Supporting result: utility_orchestrator/results/2026-09-29/1922-p0-partial-pointer-reconciliation.md
