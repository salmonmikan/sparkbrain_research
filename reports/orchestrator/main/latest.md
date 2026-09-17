# MAIN Orchestrator — PRIMARY checkpoint

Timestamp: `2026-09-18 01:28 JST`
Execution mode: `PRIMARY`
Evidence Analyst authority: `42836802e78abd26d19c5b8a789411f2b03d0ea1`

## MAIN frontier

C19-R1 representation-matched stateless revision-authority reduction remains the PRIMARY frontier. The exact fresh identity is `c19-r1-revision-authority-official-v1`.

## Fast-path reconciliation

FAST PATH was used. The prior MAIN lease was stale and the R1 branch had not moved, so PRIMARY safely recovered ownership. No target/authority anomaly required full reconciliation. SUB's independent NON_EVIDENTIARY work was not touched.

## Critical-path progress

MAIN mechanically added the science-invariant R1 execution-admission wrapper on `research/c19-r1-revision-authority-reduction-20260917`.

New exact head: `7197ab0f9683616858859446ae9eed7b75707f25`.

The admission commit adds only:
- `configs/external_validation/c19_r1_execution_authority.json`;
- `.github/workflows/c19-r1-one-way.yml`;
- the admission checks/path triggers in `.github/workflows/c19-r1-prestart.yml`.

The wrapper binds Analyst authority `42836802...`, scientific basis `7cf84905...`, the unchanged scientific-contract and preregistration blobs, target-free `atomic_idx` source-map digest `cb3ca637...`, immutable v4 package/preserve/evidence/raw bindings, exact R1 identity, exactly-one execution, and no retry after STARTED. The scientific contract/preregistration remain unchanged and still encode their historical pre-START boundary; the new authority file is an operational admission layer, not a science mutation.

The one-way wrapper prospectively enforces STARTED/no-retry, exact package + Analyst authority, admission-only package diff, fresh preserve/evidence namespaces, CPython 3.11.16, post-START pinned Belief-R acquisition, target-blind/network-blocked R1 acquisition, exact source-map digest/inventory, atomic preservation of raw + source map + manifest, independent remote re-fetch/digest equality before targets, read-only immutable v4 raw binding, scoring only after preservation, and annotated terminal evidence.

## Workflow/check state

Exact-head ordinary CI: `35246655185` — `in_progress` at checkpoint.

Exact-head dedicated R1 pre-START: `35246655189` — `in_progress` at checkpoint.

Both runs are bound to `7197ab0f9683616858859446ae9eed7b75707f25`. STARTED has not been created; official R1 data access, one-way execution, preservation, scoring and identity consumption have not occurred.

## Stop / relay boundary

PRIMARY stopped because the only remaining critical-path work is waiting for the two external exact-head gates. Lease is `WAITING_EXTERNAL` so Relay may collect the runs.

If both runs are green, Relay/next MAIN must fresh re-fetch the Analyst handoff, R1 exact head, R1 control/preserve/evidence namespaces, identity freshness, and all source/protocol/package/input/runtime/controller/source-map/scorer/preserver bindings. Only if every GO condition remains clean may it create one STARTED control ref bound to exact package `7197ab0f...` and Analyst `42836802...`, then allow the single one-way workflow to continue.

If either gate fails for a science-invariant mechanical reason, MAIN owns the fix and must re-establish both gates on the new same final SHA. Any scientific/statistical/controller/resource/runtime-version redesign requires STOP and fresh Analyst authority.

## Science / integrity

New scientific information: **none**. This run performed admission/readiness packaging only. R1 remains unSTARTED/unconsumed. Consumed C19-v2/v3/v4 and immutable v4 evidence were not changed or rescored.

Work left for SUB: none on MAIN's critical path; SUB remains independent and must not take R1 blockers.
