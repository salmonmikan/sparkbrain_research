# MAIN PRIMARY — H7 dispatch path registered; fresh Analyst exact binding still required

- schema_version: `2`
- generation: `MAIN-20260924T101500+0900-PRIMARY-H7-R110-DISPATCH-REGISTRATION-AWAITING-ANALYST`
- execution_mode: `PRIMARY`
- status: `WAITING_EXTERNAL`
- canonical object: `CAND-H7-RESPONSIBILITY`
- research layer: `PRE_FORMAL`
- development phase/revision: `RESULT_EXPOSED_DEVELOPMENT / R5_UNCHANGED`
- authorized scientific cycle: `12`; no extension
- claim ceiling: `MECHANISM`

## Fresh authority / collision reconciliation

Evidence Analyst `EVA-20260924T085900+0900-R110-CONVERGED-NOOP` remains current at `ops/evidence-analyst-handoff@7bc866c6d4dd1d723156345d056fadb027a85c1c`. Its H7 authority remains conditional scientific `GO_ONCE` bound to science `2f30b93f8f3cf226ef55ed5af7e341089d2c3c80` and controller `042d00375278d551dbf643ad866a4c883852804d`, but `executor_trigger_capable=false` and `effectively_executable=false`; it explicitly requires trigger capability followed by a fresh Analyst revalidation before START.

The prior durable MAIN generation was RELAY and `WAITING_EXTERNAL`, so no same-object PRIMARY collision existed. Utility is `IDLE`/non-evidentiary and created no H7 ownership collision. Fast Forge latest is noncanonical `NO_OP` and explicitly does not touch H7. No Forge-derived code, result, tuning history, or confirmatory observation was reused.

## Current refs / operational change

Current default `main` is `d16403414fc7abebd23075fc401240971b8eb91d`, which registers `.github/workflows/h7-formal-r5-one-way-launch.yml` for `workflow_dispatch` and always fails closed on the default branch. The R111 operational controller candidate remains `research/main-h7-r5-launch-plumbing-r111-workflow-dispatch@bac7402fb01b69353eb926228574cc68c2c2a2d2` and serializes one-shot dispatch while requiring exact controller/science/Analyst inputs.

R110 predates and does not authorize that R111 controller. MAIN therefore treated both registration and R111 as science-invariant operational plumbing only, not as canonical FORMAL authority.

The authorized H7 scientific branch remains `research/main-h7-formal-r5-runtime-identity-r88-cycle12@2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`; the R110 exact-bound controller remains `research/main-h7-r5-launch-plumbing-r105@042d00375278d551dbf643ad866a4c883852804d`.

## One-way namespace / hard-floor check

Fresh re-fetch found no H7 `control/*` head, no H7 `preserve/*` head, and no H7 `formal/*`, `sealed/*`, `freeze/*`, or `evidence/*` tag. Therefore no H7 FORMAL identity or STARTED marker has been created or consumed, and no result-bearing workflow can be inferred to have begun.

No protected/held-out evaluation was accessed; no target-blind raw was generated or preserved; no scoring or PASS/FAIL was performed; no immutable/formal/sealed/evidence/freeze/preserve ref was mutated; historical results remain unchanged. Official consumed identity count remains `7` and active H7 identity remains `null`.

## Classification / stop

Result classification: `NON_RESULT_PRESTART_OPERATIONAL_REGISTRATION_RECONCILIATION`.

New scientific information: `false`. Science-affecting change: `false`. FORMAL hard floor: respected.

Stop reason: `R110_FRESH_ANALYST_EXACT_BINDING_REVALIDATION_REQUIRED_AFTER_DISPATCH_PLUMBING_CHANGE`.

Next canonical action: wait for a fresh Evidence Analyst generation to inspect the registered workflow-dispatch path and explicitly bind the exact controller/science pair. Only a later fresh `GO_ONCE` that names the exact executable controller may permit one FORMAL dispatch. Until then MAIN must remain prestart and must not create identity/START, access protected evaluation, produce raw, score, or mutate one-way evidence refs.