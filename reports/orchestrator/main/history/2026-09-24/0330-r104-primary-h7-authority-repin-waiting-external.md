# MAIN PRIMARY history — H7 R104 authority repin and external wait

- schema_version: `2`
- generation: `MAIN-20260924T033000+0900-PRIMARY-H7-R104-AUTHORITY-REPIN-WAITING`
- execution_mode: `PRIMARY`
- canonical object: `CAND-H7-RESPONSIBILITY`
- layer: `PRE_FORMAL`
- phase/revision: `RESULT_EXPOSED_DEVELOPMENT / R5_UNCHANGED`
- cycle: `12`
- result classification: `NON_RESULT_SCIENCE_INVARIANT_AUTHORITY_REPIN_WAITING_EXTERNAL`

## Fresh authority and exact refs

Evidence Analyst R104 at `ops/evidence-analyst-handoff@0dfa28e2a8d0ddd6731ccbe9eccc7882e7f3be6f` supersedes R103 and grants `GO_ONCE_CONDITIONAL_EXACT_BINDING` for H7. The exact H7 scientific source remains `research/main-h7-formal-r5-runtime-identity-r88-cycle12@2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`.

Before mutation, H7 `control/h7*`, `preserve/h7*`, and H7 `formal/*`, `sealed/*`, `freeze/*` namespaces were absent. Stable main remained `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. Relay was enabled and no same-object mutation collision was observed. Fast Forge's observed active branch did not collide with H7, and Utility remained outside the canonical critical path.

## Work performed

The readiness controller at `research/main-h7-r5-oneway-controller-r98` still pinned superseded Analyst R103. R104 explicitly permits a science-invariant authority/control-metadata repin if required. PRIMARY therefore changed only `ANALYST_SHA` in `.github/workflows/h7-formal-r5-one-way-readiness.yml` from R103 to R104.

No scientific source, hypothesis, comparator, metric/scorer meaning, threshold/tolerance, intervention, seed/exclusion policy, resource/privilege contract, protocol, package/runtime, input, component hash, preserver semantics, or one-way result-handling rule changed. The controller head after the repin is `9c9f7e312aaf919418806d55dad0f1fcaafa5ee1`.

The push triggered fresh workflows on that exact controller head:

- R104-bound strictly NON_RESULT H7 readiness: run `35902642575`, `in_progress` at the wait boundary.
- generic CI: run `35902642400`, `queued` at the wait boundary.

The previously missing protected-sidecar capability had already been repaired externally and verified by the successful unchanged R5 NON_RESULT readiness attempt under R103. No secret value was exposed.

## Scientific/evidentiary status

No new scientific result was generated. No FORMAL identity was created or consumed. No STARTED marker was created. No protected or held-out evaluation was accessed. No official scorer was run and no PASS/FAIL was assigned. No evidence, immutable, formal, sealed, freeze, preserve, or scientific source ref was mutated. Official consumed FORMAL identities remain `7`.

Forge-derived code, observations, prototypes, or tuning history were not reused. Prior scientific results remain unchanged.

## Hard-floor status

The FORMAL one-way floor is intact. No consumed identity was rerun, retuned, or rescored. The R104 authority is conditional and has not been exercised. The control-metadata repin is classified `SCIENCE_INVARIANT_REPAIR_CONTROL_METADATA_ONLY`.

## Stop reason

`WAITING_R104_BOUND_NON_RESULT_READINESS_AND_CI`.

Per MAIN wait policy, no FORMAL identity or START action is allowed while the fresh R104-bound readiness or generic CI is pending.

## Next canonical action

On continuation, first inspect the exact workflow outcomes. If both are green, re-fetch the current Analyst generation immediately before any FORMAL mutation and revalidate exact H7 source/controller refs, frozen scientific contract, package/runtime, input, components, scorer, preserver, workflow, resource/privilege binding, and unused STARTED/preserve namespaces. Only if R104 remains current and every binding is exact may MAIN create exactly one fresh FORMAL identity and execute the one-way START path once. Any mismatch, superseding Analyst generation, or namespace collision fails closed.
