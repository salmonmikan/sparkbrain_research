# SparkBrain v0.3 — Migration and compatibility

## Version boundary

The package version is `0.3.0`. The accepted v0.2.1 persisted config/state/trace schema remains
`0.2` and is read-only compatibility evidence. New v0.3 trace and checkpoint payloads use
schema `0.3`. A package-version change does not rewrite a persisted schema.

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
- A future migration command must record source/target schema, configuration differences,
  missing fields, and default assumptions without changing the source checkpoint. Unsupported
  fields must fail closed.

## Artifact and API boundaries

v0.3 artifacts are additive under `artifacts/v03/`; C01--C10 artifacts are retained as v0.2.1
historical evidence. The C18 static Brain Lab export is local-only and does not change the
existing `/api` surface. Any future v0.3 endpoint must use an explicit `/api/v03/` path or an
equivalent version field.

## Release compatibility criteria

- the v0.2.1 reference schema and historical hashes remain available;
- v0.3 schema validation never accepts a v0.2 payload by implicit conversion;
- the deterministic CPU/offline reference path remains available; and
- package/release changes do not promote negative C06, C08, C17, or unintegrated C19 evidence.
