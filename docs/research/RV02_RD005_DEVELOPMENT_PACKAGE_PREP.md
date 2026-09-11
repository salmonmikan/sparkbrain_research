# RV02 RD005 development package preparation

Date: 2026-09-12  
Status: **EXECUTION DISABLED / PRE-D1 PACKAGE CONTRACT**

## Purpose

This record advances RD005 only through source/package identity and fail-closed governance. It does not construct an RD005 development artifact, does not invoke learner/probe capability, does not score output, and does not create a held-out/formal candidate.

The package contract lives in:

```text
src/sparkbrain/research/rv02_rd005_development_package.py
```

The preregistered stage order is explicit: first freeze and run a **construction-only D1 wrapper**, retain/review the canonical D1 artifact, and only afterward prepare any separate learner/probe capability runner. Construction and capability must not be collapsed into one run.

## Source manifest boundary

A future construction package must bind a 40-character exact source Git SHA plus SHA-256 digests for, at minimum, the boundary-critical RD005 construction/gate/verifier modules, their direct inherited RV02/world contracts, and the preregistration/review documents named by `RD005_REQUIRED_SOURCE_PATHS`.

The contract refuses duplicate paths, unsafe relative paths, malformed SHA-256 values, and omission of any required boundary-critical path. Additional transitive files may be included; the minimum list is not permission to omit other files later shown to affect construction.

## Authoritative collision registry boundary

The previous construction type accepted an explicit collision-search record but did not itself prove that the supplied registry was the complete repository-wide consumed/reserved identity set. The package layer therefore requires a separate `RD005CollisionRegistry` with:

- a stable registry ID;
- retained source path(s) documenting how the registry was constructed;
- exact non-boolean integer seed identities;
- retained world identities;
- an explicit `authoritative_complete = true` assertion;
- deterministic registry SHA-256;
- fail-closed rejection if fresh seed `92505` or its world namespace collides.

This module does **not** invent an authoritative registry. The retained registry still has to be constructed and audited from repository evidence before the package can become freeze-ready.

## No-clobber package identity and stage order

`RD005DevelopmentPackagePlan` derives a deterministic prospective run identity from the source SHA and collision-registry digest and places it under:

```text
artifacts/rv02/rd005/development/<run-id>
```

The package state fixes:

```text
overwrite_allowed = false
retry_same_identity_allowed = false
d1_construction_only_stage_required = true
d1_retained_and_reviewed_before_capability_required = true
construction_and_capability_same_run_allowed = false
construction_verifier_required_before_capability = true
construction_integrity_failure_is_terminal = true
zero_ready_cells_is_terminal = true
capability_output_opened = false
learner_or_probe_executed = false
held_out_capability_allowed = false
formal_execution_allowed = false
construction_wrapper_bound = false
capability_wrapper_bound = false
python_runtime_bound = false
```

The final three `false` values are deliberate. This package-prep layer does not yet bind even the construction-only one-shot wrapper or exact Python runtime, and it explicitly refuses to bind a capability wrapper at the same stage. It therefore cannot be source-frozen or executed merely because a manifest/registry object validates.

## Topology provenance dependency

Independent review of the first verifier revision found that retained `topology_sha256` and connection rows were still self-authenticating rather than independently regenerated. A separate fix line now requires the verifier to regenerate canonical topology and pre-training gained connection state from the fixed seed/world/scale construction before any retained cell can enter a future capability inventory.

This package contract must eventually pin the repaired verifier revision. The unrepaired verifier is not sufficient authority for D1 review or any later capability transition.

## Next safe steps

Before any RD005 development capability execution can be considered, the line still needs, in order:

1. merge/review the topology-provenance verifier repair;
2. construct and audit the authoritative consumed/reserved seed + world registry;
3. build a real SHA-256 source manifest at an exact candidate commit;
4. bind an exact Python runtime and **construction-only** command contract;
5. create a fresh-output/no-clobber construction-only wrapper that always preserves raw D1 output even on failure and contains no learner/probe code path;
6. CI/review that exact construction source and freeze it under a non-moving development construction source ref;
7. run D1 construction only, retain the canonical artifact, and independently verify/review that exact artifact identity;
8. only after D1 review, prepare a separate capability package/runner with outcome-blind scoring fixed before capability output opens.

No D1 construction run, RD005 learner/probe capability, held-out capability, formal execution seal, or `STARTED` state is authorized here.
