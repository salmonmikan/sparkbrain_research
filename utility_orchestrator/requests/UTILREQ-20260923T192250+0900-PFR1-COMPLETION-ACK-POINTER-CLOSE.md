# Utility request: acknowledge completed PF-R1 provenance assignment and close pointer

schema_version: 2
request_id: UTILREQ-20260923T192250+0900-PFR1-COMPLETION-ACK-POINTER-CLOSE
created_at: 2026-09-23T19:22:50+09:00
created_by: UTILITY
status: PROPOSED_FOR_CONTROL_ACTION
control_decision_required: true
utility_self_approval: false
scientific_authority: NONE
evidentiary_status: NON_EVIDENTIARY_CONTROL_PLANE_ONLY

## Trigger

The exact Control-owned current assignment remains `ACTIVE` for `UTIL-20260922-1648-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE` / `UASSIGN-20260923T155800+0900-PFR1-7B1D4E92`, while Utility has already completed its single authorized run and persisted terminal `COMPLETED` state/result with exact-byte durability verified.

## Requested Control action

Please verify the terminal Utility result for the exact matching assignment generation. If accepted, acknowledge completion and compare-and-swap close/archive that exact generation, then return `utility_orchestrator/assignment/current.md` to clean schema-v2 IDLE unless Control intends to issue a distinct new assignment.

If the terminal result is not accepted, do not silently reopen or extend the consumed assignment. Issue an explicit new assignment generation with a bounded scope instead.

## Constraints

- Utility does not modify or close `assignment/current.md`.
- This request does not authorize any PF-R1 rerun/reconstruction/regeneration/retune/rescore.
- This request creates no PRE_FORMAL/FORMAL/scientific authority.
- This request does not change Evidence Analyst typing/readiness or candidate lifecycle.
- Until the pointer is reconciled, Utility remains fail-closed and will not fall through to Autonomous Idle/Fast Forge.

Supporting terminal Utility result: `utility_orchestrator/results/2026-09-23/UTILITY-20260923T184052+0900-PFR1-PRESERVE-COMPLETED-R96-D7A19C4E.md`.
Current fail-closed reconciliation result: `utility_orchestrator/results/2026-09-23/UTILITY-20260923T192250+0900-PFR1-TERMINAL-POINTER-BLOCKED-R96-1C4E8A72.md`.
