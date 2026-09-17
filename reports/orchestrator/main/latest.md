# MAIN Orchestrator — RELAY C19-R2 authority packaging

Timestamp: `2026-09-18 06:54 JST`
Execution mode: `RELAY`
Evidence Analyst authority: `719b9e74063e5e10f6226fd49f1835036ed75e5b`

## MAIN frontier

The latest Evidence Analyst handoff prospectively authorizes exactly one formal R2 identity, `c19-r2-fsa-state-tracker-official-v1`, after science-invariant authority packaging and full exact-head GO revalidation. The frozen scientific package remains anchored at `5d5d171cf872baed7a636fd246ab36f3a91a6716` and its scientific contract/protocol/scoring/source-map/state-tracker blobs were not modified.

RELAY advanced only the authorized operational envelope on `research/c19-r2-fsa-state-tracker-spec-20260918`, producing final authority-package head `31398d6eb4e56fe1b51ddb8206fa395075638a2b`.

## Authority packaging completed

Added science-invariant execution authority and one-way infrastructure:

- `configs/external_validation/c19_r2_execution_authority.json` binds the fresh R2 identity, Analyst commit, STARTED namespace, preserve namespace, evidence tag, immutable C19-v4 comparator refs, and exact frozen scientific blobs.
- `scripts/run_c19_r2_official.py` provides authority validation, target-blind acquisition, target-free `atomic_idx` source-map creation, post-preservation target materialization, and the already-preregistered cluster-primary scorer.
- `scripts/preserve_c19_r2_boundary.py` atomically preserves raw predictions, raw manifest, and the target-free source map without clobbering.
- `.github/workflows/c19-r2-one-way.yml` enforces STARTED/no-retry, exact-package checkout, raw+source-map preservation/refetch before targets, immutable C19-v4 raw binding, cluster-primary scoring, and terminal evidence tagging.
- the dedicated pre-START workflow/checker now validates the authority package and production execution binding while requiring the original scientific blobs to remain exact.

No R2 scientific semantics, state machine, transition/reset/readout, seeds, resource contract, scoring method, cluster definition, thresholds, or success criteria were changed.

## Collision / role reconciliation

The inherited MAIN lease was `BLOCKED` and stale; no fresh PRIMARY `RUNNING` collision existed. SUB remains on independent NON_EVIDENTIARY RV01 exploratory work and did not touch R2. Control Brain was read only as strategic prior and did not override the current Analyst authority.

## Exact-head revalidation now running

Final authority-package head: `31398d6eb4e56fe1b51ddb8206fa395075638a2b`.

- dedicated R2 pre-START run `35279107972`: `queued` when handed off.
- ordinary CI run `35279107964`: `in_progress` when handed off.

The lease is `WAITING_EXTERNAL`. RELAY did not remain occupied solely waiting for these workflows.

## STARTED / evidence boundary

No STARTED ref was created. No official R2 data was accessed. No raw/preserve/evidence ref was created. The formal identity is prospectively reserved by authority but remains unSTARTED and unconsumed.

The next MAIN/RELAY may cross STARTED exactly once only if both exact-head checks finish `success`, the Analyst authority remains compatible, the branch head remains unchanged, and the R2 control/preserve/evidence namespaces remain collision-free immediately before STARTED.

## New scientific information

None. This run is operational authority/readiness progress only; no official R2 measurement exists yet.
