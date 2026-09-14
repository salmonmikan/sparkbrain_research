# RV02 RD005 final source/runtime/package binding audit

Date: 2026-09-14  
Scope: prospective pre-D1 integrity audit only  
Execution status: **D1 NOT STARTED; capability unopened; no identity consumed**  
Human-review status: automation technical/semantic review under `USER_AUTHORIZED_REVIEW_GATE_OVERRIDE / HUMAN_REVIEW_WAIVED_BY_USER_2026-09-11`

## Current authoritative source reviewed

The audit began from authoritative branch `research/rv02-rd005-source-binding-20260913` at exact commit:

`c8fee652ad68d6038666e00add37a81db0c8bff1`

The retained-identity registry is merged and authoritative for the currently enumerated RV02 retained evidence. The prospective RD005 seed remains `92505`; no D1 construction run has been opened by this audit.

## Source-manifest gap and preparation tool

The package requires an exact Git SHA plus SHA-256 digests for every path in `RD005_REQUIRED_SOURCE_PATHS`, and the source verifier independently checks the actual Git top-level, exact `HEAD`, clean tracked checkout, and every declared byte digest before any construction output identity is allocated.

No real checked-in RD005 source manifest existed at the reviewed authoritative head. This change therefore adds `scripts/build_rv02_rd005_source_manifest.py`, which is deliberately execution-disabled and:

- refuses a nested/non-top-level repository root;
- refuses a dirty tracked checkout;
- binds the exact 40-character current `HEAD`;
- hashes every package-required source path;
- additionally hashes the builder itself as provenance;
- emits the existing `RD005SourceManifest` schema and its canonical digest;
- grants no D1, capability, held-out, or formal authority.

The manifest must be generated only after the final candidate source head is settled. If this preparation change is merged, the merged head—not `c8fee652...`—becomes the next candidate source head and must receive a freshly generated manifest.

## Remaining integrity gap: package-plan digest is not yet enforced

The current construction input schema contains `package_plan_sha256`, but `rv02_rd005_construction_runner._load_input(...)` currently validates only that this field is a 64-character lowercase hex digest. It does **not** reconstruct `RD005DevelopmentPackagePlan(source_manifest, collision_registry)` and compare the supplied digest with the canonical `package_plan_sha256` property.

Existing unit-test fixtures intentionally demonstrate this state by supplying an arbitrary `"d" * 64` package-plan digest.

This is a genuine pre-D1 integrity blocker. A construction input could otherwise carry a syntactically valid but semantically unrelated package-plan digest while still reaching construction. D1 MUST NOT execute until the runner or the exact bound invocation path fail-closes on the canonical plan digest.

## Runtime/command binding

The existing construction runner records the observed Python implementation, version, executable and runner module in raw output, but that is post-start evidence rather than a prospective runtime/command precommit. Exact runtime and construction-only command therefore remain unbound.

A later prospective package step must bind, before D1:

1. the exact source manifest and its digest;
2. the canonical collision-registry digest;
3. the canonical `RD005DevelopmentPackagePlan.package_plan_sha256`;
4. the exact Python runtime contract;
5. the exact construction-only command/invocation contract;
6. the fresh output/no-clobber identity contract already enforced by the runner.

## Decision

**SOURCE-MANIFEST PREPARATION TOOLING MAY PROCEED. D1 REMAINS BLOCKED.**

The next safe implementation frontier is to make package-plan-digest verification fail closed, then define and test the prospective runtime/command binding. Only after those changes are merged, reviewed, and represented by an exact generated source manifest should a non-moving source freeze be created and D1 construction be considered for exactly-once execution.
