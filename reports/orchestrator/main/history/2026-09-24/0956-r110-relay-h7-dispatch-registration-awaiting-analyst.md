# MAIN RELAY — H7 dispatch registration observed; waiting for fresh Analyst exact binding

- schema_version: `2`
- generation: `MAIN-20260924T095600+0900-RELAY-H7-R110-DISPATCH-REGISTRATION-AWAITING-ANALYST`
- execution_mode: `RELAY`
- status: `WAITING_EXTERNAL`
- canonical object: `CAND-H7-RESPONSIBILITY`
- research layer: `PRE_FORMAL`
- development phase/revision: `RESULT_EXPOSED_DEVELOPMENT / R5_UNCHANGED`
- authorized scientific cycle: `12`; Relay did not extend or reassess the scientific cycle

## Fresh authority and collision reconciliation

Relay re-fetched Evidence Analyst R110 (`7bc866c6d4dd1d723156345d056fadb027a85c1c`) and the MAIN lease immediately before this persistence. The MAIN lease remains `WAITING_EXTERNAL`, not `RUNNING`, so there is no fresh PRIMARY same-object collision.

R110 remains the current scientific authority. It preserves H7 as `MECHANISM`, PRE_FORMAL eligible, scientifically `READY` / `QUEUED`, `RESULT_EXPOSED_DEVELOPMENT / R5_UNCHANGED`, and requires a fresh Evidence Analyst exact-binding revalidation after one-shot trigger capability exists before any FORMAL START.

## Operational change observed

Since R110, the repository gained a default-branch registration workflow at `.github/workflows/h7-formal-r5-one-way-launch.yml` (`d16403414fc7abebd23075fc401240971b8eb91d`) and an R111 operational controller candidate `research/main-h7-r5-launch-plumbing-r111-workflow-dispatch@bac7402fb01b69353eb926228574cc68c2c2a2d2` with `workflow_dispatch`, exact controller/science/Analyst input binding, and serialized one-shot concurrency.

This is treated only as a science-invariant operational/control-plane change. Relay does **not** reinterpret it as fresh scientific authority, does not replace the R110-bound controller `research/main-h7-r5-launch-plumbing-r105@042d00375278d551dbf643ad866a4c883852804d`, and does not declare R111 FORMAL-authorized. The current Analyst generation predates this operational change and explicitly requires a fresh exact-binding revalidation after capability recovery.

## Funnel v2.1 preserved exactly

- claim_ceiling: `MECHANISM`
- preformal_eligible: `true`
- preformal_readiness: `READY`
- hold_class: `null`
- hold_reason: `null`
- terminal_state: `ACTIVE`
- queue_state: `QUEUED`
- system_priority_exception: `false`
- development_phase: `RESULT_EXPOSED_DEVELOPMENT`
- development_revision: `R5_UNCHANGED`

## FORMAL / evidentiary status

- repair/change classification: `SCIENCE_INVARIANT_OPERATIONAL_PLUMBING_OBSERVED_ONLY`
- scientific source: unchanged at `research/main-h7-formal-r5-runtime-identity-r88-cycle12@2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`
- R110 exact-bound controller: unchanged at `research/main-h7-r5-launch-plumbing-r105@042d00375278d551dbf643ad866a4c883852804d`
- active H7 FORMAL identity: `null`
- new identity created/consumed: `false`
- official consumed FORMAL identity count: `7`, unchanged
- STARTED created: `false`
- result-bearing workflow dispatched: `false`
- workflow run id: `null`
- protected/held-out evaluation accessed: `false`
- raw produced/preserved: `false / false`
- official scoring or PASS/FAIL: `false`
- immutable/formal/sealed/evidence/freeze/preserve refs mutated: `false`
- prior results preserved unchanged: `true`
- new scientific result: `false`

## Integrity / stop

The workflow registration and R111 controller candidate were re-fetched directly. Relay performed no scientific tuning, threshold/tolerance/comparator/metric/protocol/intervention/seed/exclusion/resource/privilege change and no outcome-responsive redesign. No consumed FORMAL identity was rerun, retuned, or rescored.

Stop reason: `R110_FRESH_ANALYST_EXACT_BINDING_REVALIDATION_REQUIRED_AFTER_DISPATCH_PLUMBING_CHANGE`.

Expected next MAIN action: wait for a fresh Evidence Analyst generation to inspect the registered workflow-dispatch path and explicitly bind the exact controller/science pair. Only if that fresh generation supplies a valid one-shot GO may MAIN dispatch exactly one result-bearing workflow using the exact Analyst-bound controller and inputs. Until then, do not create identity/START and do not dispatch.
