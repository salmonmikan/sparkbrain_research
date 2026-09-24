# MAIN PRIMARY — H7 dispatch path registered; waiting for fresh Analyst exact binding

- schema_version: `2`
- generation: `MAIN-20260924T101500+0900-PRIMARY-H7-R110-DISPATCH-REGISTRATION-AWAITING-ANALYST`
- execution_mode: `PRIMARY`
- status: `WAITING_EXTERNAL`
- canonical object: `CAND-H7-RESPONSIBILITY`
- research layer: `PRE_FORMAL`
- development phase/revision: `RESULT_EXPOSED_DEVELOPMENT / R5_UNCHANGED`
- authorized scientific cycle: `12`; no extension
- claim ceiling: `MECHANISM`

## Authority / collision

Evidence Analyst R110 remains the latest durable authority. It retains conditional one-shot scientific authority for H7, but binds the frozen science to the older R110 controller and explicitly requires trigger capability followed by a fresh Analyst exact-binding revalidation before START.

The prior MAIN lease was RELAY/WAITING_EXTERNAL, so no same-object PRIMARY collision existed. Utility is IDLE with no scientific authority. Fast Forge latest is noncanonical NO_OP and explicitly avoids H7; no Forge-derived code, observations or tuning history were reused.

H7 Funnel state remains unchanged: READY, ACTIVE, QUEUED, PRE_FORMAL, `RESULT_EXPOSED_DEVELOPMENT / R5_UNCHANGED`, claim ceiling MECHANISM.

## Operational advance observed

Current default `main` now registers `.github/workflows/h7-formal-r5-one-way-launch.yml` for `workflow_dispatch` and fails closed on the default branch. An R111 operational controller candidate also exists with serialized one-shot dispatch plus exact controller/science/Analyst input checks.

This is operational plumbing only. R110 predates R111 and does not bind it, so PRIMARY did not substitute R111 for the R110-authorized controller and did not dispatch FORMAL.

Authorized frozen science remains `research/main-h7-formal-r5-runtime-identity-r88-cycle12@2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`. R110 exact-bound controller remains `research/main-h7-r5-launch-plumbing-r105@042d00375278d551dbf643ad866a4c883852804d`. Observed, not-authorized R111 candidate is `research/main-h7-r5-launch-plumbing-r111-workflow-dispatch@bac7402fb01b69353eb926228574cc68c2c2a2d2`.

## Evidentiary / integrity status

- new scientific result: `false`
- prior results preserved unchanged: `true`
- consumed FORMAL identities: `7`, unchanged
- active H7 identity / STARTED: `null / false`
- H7 control/preserve/formal/sealed/freeze/evidence namespaces: unused
- result-bearing workflow: not dispatched
- protected evaluation / held-out access: `false`
- raw production / preservation: `false / false`
- official scoring / PASS-FAIL: `false / false`
- immutable/formal/sealed/evidence/freeze/preserve mutation: `false`
- science-affecting change: `false`
- Forge-derived code reused: `false`
- FORMAL hard floor: respected

## Stop / next MAIN action

Stop reason: `R110_FRESH_ANALYST_EXACT_BINDING_REVALIDATION_REQUIRED_AFTER_DISPATCH_PLUMBING_CHANGE`.

Wait for a fresh Evidence Analyst generation to inspect the registered workflow-dispatch path and explicitly bind the exact executable controller/science pair. Only if that generation supplies a valid one-shot GO may MAIN dispatch exactly one result-bearing workflow. Until then remain prestart: create no identity/START, access no protected evaluation, produce no raw, perform no scoring, and mutate no one-way evidence refs.
