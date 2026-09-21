# MAIN R41 — cross-generation holdout exposure integrity — scope-invalid stop

- generation: `MAIN-20260921T192340+0900-PRIMARY-FUNNEL21-SYSTEM-HOLDOUTLEDGER-R41-SCOPESTOP-5C8A21D4`
- analyst: `EVA-20260921T185902+0900-R41-8D3A21C7 @ ffc8672c01ed0f45b2d0fd998c36706b8a343a91`
- candidate: `CAND-PREFORMAL-CROSS-GENERATION-HOLDOUT-EXPOSURE-INTEGRITY-01`
- layer/ceiling: `ARCHITECTURE_STUDY / SYSTEM`
- canonical lifecycle preserved: `ACTIVE / ACTIVE`, hold fields null, `preformal_eligible=false`, readiness `NOT_APPLICABLE`
- system priority exception: `used=false`; viable executable MECHANISM=0
- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- independent refs: evidence tags=5; formal/sealed/tag-freeze=0; control/preserve namespaces refreshed; PR #148/#149 open/unmerged/mergeable
- scientific execution: none
- identity consumption: none
- valid terminal observation: none

Partial metadata-only characterization before stop:
1. V05 protocol separates development `501/502` and confirmatory `601-604`, with the development inspection history explicitly documented.
2. Phase1 has a frozen machine-readable test manifest (`seed_start=200000`, `episode_count=1000`) and a test asserting dev/test seed disjointness.
3. The default-branch one-way formal workflow binds exact source SHA, candidate hash, control branch, candidate/freeze/seal/STARTED paths, and artifact root.
4. Repository refs expose identity-bearing evidence/control/preserve names useful as future ledger keys.

Scope integrity incident: while requesting evidence commit metadata/file inventory, the GitHub commit endpoint also returned result-bearing evidence patch content. R41 forbids reading protected scientific outcomes. The over-returned result fields were excluded from inference and no scientific interpretation was performed, but MAIN fails closed and does not claim `EXPOSURE_LEDGER_AND_POLICY_FEASIBLE_WITH_CURRENT_METADATA`, `CURRENT_METADATA_ALREADY_EXPLICITLY_SUFFICIENT`, or `HOLD_METHOD_LIMITED` from this attempt.

Stop: `R41_SCOPE_INVALID_PROTECTED_OUTCOME_ENDPOINT_OVERRETURN_FAIL_CLOSED_NO_TERMINAL_CLASSIFICATION`.

Next: fresh Analyst review; if re-authorized, retry using refs, path inventories, non-result manifests/protocol metadata, and workflow definitions only.
