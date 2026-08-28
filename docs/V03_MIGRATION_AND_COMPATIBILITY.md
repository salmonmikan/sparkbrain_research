# SparkBrain v0.3 — Migration and compatibility

## Version boundary

The package version is `0.3.1`. The accepted v0.2.1 persisted config/state/trace schema remains
`0.2` and is read-only compatibility evidence. New v0.3 trace and checkpoint payloads use
schema `0.3`. A package-version change does not rewrite a persisted schema.

`v0.3.1` is the corrective and integrated-runtime version boundary. Its evidence is generated under
its own release directory and source pin; it does not rewrite `artifacts/release/v0.3/` or
reclassify C11--C19.

## Reference compatibility

The `v02_reference` condition continues to use the accepted v0.2.1 engine, configuration, and
artifacts. Its canonical trace and state hash must remain unchanged. New v0.3 conditions use
explicit names; existing `full`, `no_residual`, and related conditions do not acquire new
meanings through this release.

## Checkpoint and trace handling

- A v0.2 checkpoint is never automatically interpreted as schema 0.3.
- The additive `sparkbrain.v03_integration` boundary accepts only explicit schema-0.3 payloads.
- The v0.2 trace reader and replay path remain available and do not infer v0.3 evidence/entity
  events.
- A future legacy-schema migration command must record source/target schema, configuration differences,
  missing fields, and default assumptions without changing the source checkpoint. Unsupported
  fields must fail closed.

## Artifact and API boundaries

v0.3 artifacts are additive under `artifacts/v03/`; C01--C10 artifacts are retained as v0.2.1
historical evidence. The C18 static Brain Lab export is local-only and does not change the
existing `/api` surface. Any future v0.3 endpoint must use an explicit `/api/v03/` path or an
equivalent version field.

The chosen path is `/api/v03/*`. It sits beside legacy `/api/runs*` and does not reinterpret legacy
`SparkBrain` exports. The `sparkbrain.v03` facade is an implemented engineering integration
contract; its concept and organ monitors are observer-only until a separate protocol permits
decision use.

## Release compatibility criteria

- the v0.2.1 reference schema and historical hashes remain available;
- v0.3 schema validation never accepts a v0.2 payload by implicit conversion;
- the deterministic CPU/offline reference path remains available; and
- package/release changes do not promote negative C06, C08, C17, or unintegrated C19 evidence.

## Private review boundary

`scripts/build_v03_private_review_bundle.py` creates a deterministic private review source ZIP
from a clean, tracked source revision. The ZIP carries its own source manifest, checksum, fixed
timestamps, and owner-decision-pending notice, so its contents can be verified after extraction
without Git metadata. It is not a public archive, a public tag, or a substitute for the final
no-Git release manifest. The owner license blocker remains in force.
