# RV02 RD005 construction-input binding technical review

Date: 2026-09-14  
Scope: prospective D1 construction-input preparation only  
Execution status: **D1 NOT STARTED; capability unopened; seed 92505 unconsumed**  
Human-review status: substantive automation review under `USER_AUTHORIZED_REVIEW_GATE_OVERRIDE / HUMAN_REVIEW_WAIVED_BY_USER_2026-09-11`; no independent human identity is claimed.

## Purpose

The D1 runtime and launch command are already bound prospectively. The remaining input-side gap was the absence of one deterministic, source-bound way to turn the final exact source manifest plus the authoritative pre-RD005 collision registry into the exact bytes consumed by the bound D1 wrapper.

`rv02_rd005_construction_input.py` closes that gap without executing D1.

## Input construction contract

The builder:

1. loads an exact `RD005SourceManifest` and rejects extra or missing top-level/entry keys;
2. verifies the manifest against the actual Git top-level, exact HEAD, clean tracked checkout, and every declared SHA-256 source digest;
3. independently reconstructs the authoritative pre-RD005 collision registry from retained evidence using `build_authoritative_rd005_collision_registry`;
4. constructs `RD005DevelopmentPackagePlan` from those two verified identities;
5. emits exactly the six fields accepted by the D1 construction runner:
   - `source_git_sha`
   - `source_manifest_sha256`
   - `source_manifest`
   - `collision_registry_sha256`
   - `package_plan_sha256`
   - `collision_registry`
6. serializes them deterministically as sorted, indented UTF-8 JSON with one trailing newline;
7. reports the SHA-256 digest of those exact bytes.

The prospective seed `92505` is never inserted into prior identity evidence. Registry validation remains fail-closed if that seed or its world namespace collides with retained history.

## No-clobber and execution boundary

The builder is execution-disabled. It does not import or call the D1 construction runner, allocate the D1 output identity, construct a field/artifact, run a learner or probe, score an outcome, or open capability output.

Source and retained-registry validation complete before any construction-input file is written. The output file is created with exclusive-create semantics and is never overwritten. Tests verify deterministic bytes, exact digesting, no-clobber behavior, and that a source-verification failure leaves neither a construction-input artifact nor a D1 output tree.

`src/sparkbrain/research/rv02_rd005_construction_input.py` and this review record are themselves required RD005 source-manifest paths. The final source manifest must therefore be regenerated only after this change is merged and the source head has settled.

## Scientific boundary

This review does **not** authorize D1 execution and does not create a `STARTED` marker or execution seal. The package remains before the one-way construction boundary. Seed `92505` remains unconsumed.

No capability learner/probe exists in this path. Capability must remain closed until the exactly-once D1 construction output is preserved and independently reviewed under the preregistered stage order.

## Remaining gates before D1

After this change is reviewed, CI-green, and merged, D1 remains blocked until all of the following are completed against the final settled source head:

1. generate the exact SHA-256 source manifest with the final source SHA;
2. re-run exact source checkout verification and authoritative collision-registry reconstruction;
3. use this builder to create one concrete no-clobber construction-input artifact and record its exact SHA-256 digest;
4. perform final technical/semantic review of the exact source/package/input identities;
5. create and verify a non-moving exact-source freeze ref;
6. create the execution seal/control record binding the concrete input digest/path, frozen source SHA/ref, runtime binding digest, exact command contract, and fresh D1 output identity;
7. only if the actual D1 launch can occur in the same integrity-preserving progression, cross the construction boundary exactly once.

## Decision

**CONSTRUCTION-INPUT BINDING IS SUITABLE FOR PROSPECTIVE REVIEW. D1 REMAINS UNSTARTED AND BLOCKED PENDING FINAL SOURCE MANIFEST, CONCRETE INPUT ARTIFACT, FINAL REVIEW, SOURCE FREEZE, AND EXECUTION SEAL.**
