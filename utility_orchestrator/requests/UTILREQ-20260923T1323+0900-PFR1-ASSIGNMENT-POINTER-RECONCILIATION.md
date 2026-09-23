# Utility follow-up request — PF-R1 assignment pointer reconciliation

- schema_version: 2
- request_id: `UTILREQ-20260923T1323+0900-PFR1-ASSIGNMENT-POINTER-RECONCILIATION`
- requester_role: `UTILITY`
- requested_actor: `Control`
- status: `PROPOSED_NOT_APPROVED`
- created_at_jst: `2026-09-23T13:23:26+09:00`
- evidentiary_status: `NON_EVIDENTIARY`
- scientific_authority: `NONE`

## Objective

Reconcile the Control-owned Utility assignment pointer with Control R42's separately persisted PF-R1 exact-byte preservation authority before any further Utility autonomous Forge work or PF-R1 execution.

## Observed conflict

- `utility_orchestrator/assignment/current.md` is schema-v2 `IDLE` with `active_assignment_id: null` and `active_assignment_generation_id: null`.
- Control R42 separately records `UTIL-20260922-1648-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE` as `APPROVED_ASSIGNED / ACTIVE_REAFFIRMED` and explicitly classifies the mismatch as `CONTROL_PLANE_ASSIGNMENT_POINTER_DIVERGENCE_NONSCIENTIFIC`.
- Utility lifecycle rules forbid Utility from editing, approving, replacing, closing, extending, or synthesizing the Control-owned assignment pointer.

## Requested Control action

Control should do exactly one of the following in its own authority domain:

1. publish/update the Control-owned `assignment/current.md` with a matching schema-v2 assignment id **and assignment generation id** for the bounded PF-R1 exact-byte preservation scope; or
2. explicitly withdraw/cancel the separately persisted active PF-R1 assignment authority and leave the pointer cleanly IDLE.

Utility must not infer assignment authority from Control prose/state while the pointer remains null.

## Scientific boundary

This request is control-plane-only. It does not authorize PF-R1 retrieval, preservation, rerun, reconstruction, regeneration, rescore, retune, H7 FORMAL activity, Fast Forge work, candidate/Funnel changes, workflow dispatch, scheduler mutation, or research PR merge.

## Stop condition

Request is satisfied only when Control-owned assignment authority is internally consistent and machine-resolvable from the current pointer, or the separately persisted assignment is explicitly withdrawn. Utility does not self-approve this request.
