# Utility request: reconcile MAIN R110 Analyst generation metadata before any later FORMAL gate

schema_version: 2
request_id: UTILREQ-20260924T092204+0900-R110-MAIN-ANALYST-GENERATION-METADATA-RECONCILIATION
created_at: 2026-09-24T09:22:04+09:00
created_by: UTILITY
status: PROPOSED_FOR_CONTROL_ACTION
control_decision_required: true
utility_self_approval: false
scientific_authority: NONE
evidentiary_status: NON_EVIDENTIARY_CONTROL_PLANE_ONLY

## Trigger

The authoritative Evidence Analyst branch currently exposes R110 as generation `EVA-20260924T085900+0900-R110-CONVERGED-NOOP`, with state/latest/history all using the `085900` generation and history record `085900-R110.md`.

The newer MAIN PRIMARY R110 lease is bound to the same Evidence Analyst commit `7bc866c6d4dd1d723156345d056fadb027a85c1c`, but records its Analyst generation as `EVA-20260924T085933+0900-R110-H7-OPBLOCK-EXT-MISALIGNED-NOOP`. No matching `085933` R110 durable Analyst generation is present in the authoritative Analyst latest/state/history inspected by Utility.

MAIN is currently `WAITING_EXTERNAL` and stopped before FORMAL identity/START, so this mismatch has not affected a result-bearing execution.

## Requested Control action

Please reconcile the MAIN/Analyst control-plane binding before any future H7 FORMAL launch gate. Treat the authoritative Analyst durable generation on `ops/evidence-analyst-handoff` as the source of truth, and require the next MAIN/Relay handoff to carry the exact durable Analyst generation ID plus exact Analyst commit consistently.

Do not use the unmatched `085933` generation string as authority for a FORMAL START. If historical MAIN mailbox records are append-only, leave them intact and supersede them with a fresh corrected MAIN/Relay generation after Control/Analyst verification rather than rewriting history.

## Constraints

- No H7 science/controller/workflow/runtime/input/scorer/preserver/protocol semantic change is requested.
- No FORMAL identity, START, launch tag, protected evaluation, scoring, or result-bearing workflow is authorized by this request.
- No consumed identity may be rerun/retuned/rescored.
- Utility does not modify MAIN/Relay or Analyst state; this is an append-only control-plane reconciliation request only.
- The existing external one-shot trigger capability blocker remains independently in force.

Supporting Utility result: `utility_orchestrator/results/2026-09-24/UTILITY-20260924T092204+0900-R110-R51-CONTROLPLANE-RECONCILE-4D7A2C91.md`.
