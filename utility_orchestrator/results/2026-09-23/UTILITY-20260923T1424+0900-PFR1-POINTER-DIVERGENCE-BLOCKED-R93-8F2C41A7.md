# Utility terminal result — PF-R1 pointer divergence persists under R93

- schema_version: 2
- generation_id: `UTILITY-20260923T1424+0900-PFR1-POINTER-DIVERGENCE-BLOCKED-R93-8F2C41A7`
- produced_at_jst: `2026-09-23T14:24:29+09:00`
- mode: `FAIL_CLOSED`
- selected_task: `CONTROL_PLANE_ASSIGNMENT_POINTER_RECONCILIATION_READ_ONLY`
- fast_forge_support: `false`
- status: `BLOCKED`
- evidentiary_status: `NON_EVIDENTIARY`
- scientific_authority: `NONE`

## Authority reconciliation

The Control-owned Utility pointer remains schema-v2 `IDLE` with `active_assignment_id: null` and `active_assignment_generation_id: null` at blob `6fe8c6da7192a3021eea9e2c4a94b1a1251e6da7`.

Control R42 separately retains PF-R1 exact-byte preservation request `UTIL-20260922-1648-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE` as active authority and explicitly classifies this as `CONTROL_PLANE_ASSIGNMENT_POINTER_DIVERGENCE_NONSCIENTIFIC`. Fresh Evidence Analyst R93 independently re-fetches the same situation, keeps PF-R1 on HOLD, and records that Utility is correctly fail-closed.

Because Utility assignment execution requires a matching current assignment id plus assignment generation id, Utility did not infer PF-R1 authority from Control prose/state and did not fall through to AUTONOMOUS_IDLE Fast Forge work.

## Fresh ownership / collision checks

- Evidence Analyst: `EVA-20260923T140800+0900-R93-4D7C2A91` at `92a85ab4f7795e97e5c0e750c8edfcc77a74c0bd`.
- MAIN: `MAIN-20260923T141500+0900-PRIMARY-CAND34-PREFORMALR2-R93-ACQUIRED`, status `RUNNING`, exclusively owning Candidate #34's one bounded PRE_FORMAL R2 response lane.
- Candidate #34 authoritative branch/head: `research/main-cand34-assembly-route-preformal-r92-cycle4@43d0f25541a3c447d4c7156303647ae94f3119f4`.
- Fast Forge: `FORGE-20260923T133600+0900-ACTION-CONTEXT-DEADEND-R92`, latest outcome `FORGE_DEAD_END`, no Utility request and no promotion proposal.
- Separate Relay branch: none observed; current MAIN lease is the fresh canonical owner.
- Control: `CTRL-20260923T125800+0900-R42-7C9E41B2` at `7035ace9b0ef980602dcb124e8974be5640d7377`.
- Stable `main`: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`.
- Fast Forge branch remains `forge/20260923-receptor-suppression-probes-a@c366c4054d2834003fcca20d49b8fc9ad4203edc`.

No ownership collision was created because no scientific/development action was attempted.

## Material update observed this run

Evidence Analyst R93 prospectively moved Candidate #34 to READY for exactly one bounded response-bearing PRE_FORMAL R2 development execution under the unchanged closed contract. MAIN then acquired that exact lane and is RUNNING. This is fresh canonical MAIN activity and is outside Utility autonomous authority.

This update does not resolve PF-R1 Utility machine authority. R93 explicitly preserves the PF-R1 HOLD until the Utility current pointer is reconciled.

## Actions

1. Re-read Utility assignment/current and Utility prior state/request.
2. Re-read Control R42 strategy and active PF-R1 intent.
3. Re-read fresh Evidence Analyst R93.
4. Re-read fresh MAIN ownership/lease, current Fast Forge state, and authoritative branch refs.
5. Re-confirmed pointer divergence and failed closed.
6. Did not create a duplicate follow-up request; the existing reconciliation request remains the correct bounded Control action.

## Existing follow-up request

`utility_orchestrator/requests/UTILREQ-20260923T1323+0900-PFR1-ASSIGNMENT-POINTER-RECONCILIATION.md`

Status remains `PROPOSED_NOT_APPROVED`. Utility does not self-approve it.

## Explicitly not performed

- no PF-R1 artifact retrieval or preservation
- no rerun / reconstruction / regeneration / rescore / retune
- no Fast Forge prototype or diagnostic
- no Candidate #34 PRE_FORMAL execution or plumbing
- no candidate/Funnel/lifecycle mutation
- no FORMAL identity, STARTED, protected evaluation, official scoring, evidence or preserve ref creation
- no research branch mutation
- no workflow dispatch
- no scheduler mutation
- no research PR merge

## Stop reason

`BLOCKED_CONTROL_PLANE_ASSIGNMENT_POINTER_DIVERGENCE`

Execution permission records remain internally inconsistent. Utility therefore stopped on the safe side and left all scientific and Forge work untouched.

## Follow-up recommendation

Control should satisfy the already-open reconciliation request by either publishing a matching schema-v2 current assignment id + generation for the bounded PF-R1 exact-byte preservation scope, or explicitly withdrawing the separately persisted active authority. Until then Utility should remain fail-closed and should not start further autonomous Forge support.

No scientific conclusion or promotion signal is produced by this result.
