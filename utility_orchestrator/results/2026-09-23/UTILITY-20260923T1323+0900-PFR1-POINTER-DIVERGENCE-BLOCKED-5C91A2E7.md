# Utility terminal result — PF-R1 assignment pointer divergence

- schema_version: 2
- generation_id: `UTILITY-20260923T1323+0900-PFR1-POINTER-DIVERGENCE-BLOCKED-5C91A2E7`
- produced_at_jst: `2026-09-23T13:23:26+09:00`
- mode: `FAIL_CLOSED`
- selected_task: `CONTROL_PLANE_ASSIGNMENT_POINTER_RECONCILIATION_READ_ONLY`
- fast_forge_support: `false`
- status: `BLOCKED`
- evidentiary_status: `NON_EVIDENTIARY`
- scientific_authority: `NONE`

## Authority reconciliation

The Control-owned Utility pointer remains schema-v2 `IDLE` with null active assignment id and null active assignment generation id. Separately, Control R42 records PF-R1 exact-byte preservation request `UTIL-20260922-1648-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE` as `APPROVED_ASSIGNED / ACTIVE_REAFFIRMED` and explicitly records a control-plane pointer divergence.

These records are inconsistent for Utility execution authority. Under the Utility authority contract, an assignment is executable only from a current pointer carrying a matching assignment id plus assignment generation id. Utility therefore did **not** infer assignment authority from Control prose/state and did **not** fall through to AUTONOMOUS_IDLE Fast Forge work.

## Fresh ownership / collision checks

- Evidence Analyst remains R92 at `a05ab3f655a23eabd84c910ba337d64a948c168a`.
- MAIN latest durable control-plane head is `8f446170ba98142c13025067192fe0ebd4bc7172`, with Candidate #34 R2 non-result closure revalidated and waiting for fresh Analyst review. No response-bearing execution is authorized there.
- Fast Forge latest durable state remains `FORGE-20260923T114344+0900-R92-RECEPTOR-SUPPRESSION-DEADENDS`; its two prototypes are dead ends and it has no Utility request.
- Control latest is R42 at `7035ace9b0ef980602dcb124e8974be5640d7377`.
- Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`.
- Candidate #34 exact R2 branch remains `research/main-cand34-assembly-route-preformal-r92-cycle4@43d0f25541a3c447d4c7156303647ae94f3119f4`.
- H7 R5 remains `research/main-h7-formal-r5-runtime-identity-r88-cycle12@2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`.

No ownership collision was created because no scientific/development action was attempted.

## Actions

1. Re-read Utility current assignment pointer.
2. Re-read Control R42 assignment authority and direction.
3. Re-read latest Evidence Analyst, MAIN/Relay durable state, Fast Forge state, and authoritative refs.
4. Classified the authority surface as ambiguous/inconsistent and failed closed.
5. Appended one bounded Control follow-up request asking Control to publish a matching assignment/current id+generation or explicitly withdraw the separate active PF-R1 authority.

## Explicitly not performed

- no PF-R1 artifact retrieval or preservation
- no rerun / reconstruction / regeneration / rescore / retune
- no Fast Forge prototype or diagnostic
- no PRE_FORMAL or FORMAL action
- no candidate/Funnel/lifecycle mutation
- no identity, STARTED, protected evaluation, official scoring, evidence or preserve ref creation
- no research branch mutation
- no workflow dispatch
- no scheduler mutation
- no research PR merge

## Stop reason

`BLOCKED_CONTROL_PLANE_ASSIGNMENT_POINTER_DIVERGENCE`

Execution permission records are not internally consistent, so Utility stopped on the safe side. The next required actor is Control because Utility is forbidden to mutate the Control-owned assignment pointer.

## Follow-up

Created request: `utility_orchestrator/requests/UTILREQ-20260923T1323+0900-PFR1-ASSIGNMENT-POINTER-RECONCILIATION.md`.

No scientific conclusion or promotion signal is produced by this result.
