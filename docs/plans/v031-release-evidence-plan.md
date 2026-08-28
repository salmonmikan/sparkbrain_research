# v0.3.1 release evidence plan

## Objective

Generate and validate a separate `artifacts/release/v0.3.1/` evidence layer while preserving the
tracked `artifacts/release/v0.3/` bytes and every saved scientific result.

## Current behavior

The v0.3 release helpers accept package 0.3.1 but still hard-code the v0.3 directory, package
version, schemas, and exact-ten paths. Running them would therefore target the historical v0.3
evidence boundary.

## Theory contract

No dynamics, metric, threshold, seed, schema-0.2 persistence rule, or C18 schema-0.3 payload
changes. C19 remains blocked and not evaluated. C17 v1 remains an engineering implementation
failure: its five candidate-present cells have 25 incomplete controls because the disjoint pool is
too small, so science is `not_evaluated_implementation_failure`; only the 100 not-applicable
controls in candidate-absent cells are valid negative observations. Corrective evidence is
engineering-only and does not change a claim grade.

## Implementation slices

1. Add fixed release contracts for package 0.3.0 and 0.3.1.
2. Route generation and validation through the selected package contract.
3. Keep the original v0.3 constants and tests as backward-compatible aliases.
4. Add v0.3.1 exact-directory, evidence-boundary, tamper, and root-integration tests.

## Data and evaluation

Only existing C11--C19 evidence, the C17 v1 control-gap audit boundary, and corrective source/test
evidence are indexed. No model, controller, official seed, external cache, or scientific artifact
is executed or rewritten.

## Risk register

- Accidentally targeting `artifacts/release/v0.3/`: prevent with an exact version-to-directory map.
- Claim escalation: require the corrective entry to have no claim IDs and an engineering-only
  boundary.
- Circular manifests: retain the existing staged source/root manifest workflow.
- Future runtime overclaim: future entries must be explicitly registered per package version.

## Acceptance criteria

- Package 0.3.1 targets only `artifacts/release/v0.3.1/`.
- Package 0.3.0 retains its exact existing generator and validator contract.
- Persisted schema remains 0.2; C18 schema remains 0.3.
- C19 remains blocked and official data is not read.
- C17 v1 is not reclassified as a scientific negative; its saved artifacts remain unchanged.
- Root manifests and saved scientific artifacts are not generated or changed in this commit.

## Validation commands

```text
python -m pytest tests/test_v03_release_artifacts.py tests/test_v03_release_compatibility.py
python -m pytest tests/test_v03_private_review_bundle.py
python -m ruff check src/sparkbrain/release_v03_artifacts.py src/sparkbrain/release.py scripts/generate_v03_release_artifacts.py scripts/generate_v03_root_manifest.py tests/test_v03_release_artifacts.py
python scripts/local_readiness_check.py
```

## Documentation updates

Only this execution plan is added. Existing scientific ledgers and decisions already define the
v0.3.1 separation boundary and are not rewritten.

## Local execution contract

Generation and validation use local files and Git metadata only. They perform no network access
and require no accelerator.

## Rollback boundary

Revert the source/test/plan commit. The historical v0.3 directory and root release bindings remain
byte-identical throughout.
