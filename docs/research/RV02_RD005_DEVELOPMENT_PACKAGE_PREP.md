# RV02 RD005 development package preparation

Date: 2026-09-12  
Status: **EXECUTION DISABLED / PRE-FREEZE PACKAGE CONTRACT**

## Purpose

This record advances RD005 only through source/package identity and fail-closed governance. It does not construct an RD005 development artifact, does not invoke learner/probe capability, does not score output, and does not create a held-out/formal candidate.

The package contract lives in:

```text
src/sparkbrain/research/rv02_rd005_development_package.py
```

## Source manifest boundary

A future package must bind a 40-character exact source Git SHA plus SHA-256 digests for, at minimum, the boundary-critical RD005 construction/gate/verifier modules, their direct inherited RV02/world contracts, and the preregistration/review documents named by `RD005_REQUIRED_SOURCE_PATHS`.

The contract refuses duplicate paths, unsafe relative paths, malformed SHA-256 values, and omission of any required boundary-critical path. Additional transitive files may be included; the minimum list is not permission to omit other files later shown to affect execution.

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

## No-clobber package identity

`RD005DevelopmentPackagePlan` derives a deterministic prospective run identity from the source SHA and collision-registry digest and places it under:

```text
artifacts/rv02/rd005/development/<run-id>
```

The package state fixes:

```text
overwrite_allowed = false
retry_same_identity_allowed = false
construction_verifier_required_before_capability = true
construction_integrity_failure_is_terminal = true
zero_ready_cells_is_terminal = true
capability_output_opened = false
learner_or_probe_executed = false
held_out_capability_allowed = false
formal_execution_allowed = false
execution_wrapper_bound = false
python_runtime_bound = false
```

The final two `false` values are deliberate. This package-prep layer does not yet bind the one-shot execution wrapper or exact Python runtime, so it cannot be source-frozen or executed merely because a manifest/registry object validates.

## Next safe steps

Before any one-shot RD005 development capability execution can be considered, the line still needs:

1. an audited authoritative consumed/reserved seed + world registry committed as retained evidence;
2. a real SHA-256 source manifest at an exact candidate commit;
3. an exact Python runtime and command contract;
4. a fresh-output/no-clobber wrapper that always preserves raw construction/capability failure evidence;
5. a verifier-before-capability gate wired into that wrapper;
6. outcome-blind result/scoring schema fixed before capability output is opened;
7. CI plus exact-head technical/semantic review of the final prospective source;
8. only then, a non-moving development source freeze candidate.

No RD005 development capability, held-out capability, formal execution seal, or `STARTED` state is authorized here.
