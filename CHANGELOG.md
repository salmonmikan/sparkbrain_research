# Changelog

## v0.3.1 — 2026-08-28

Corrective private-review and engineering-integration patch. No scientific artifact, claim grade,
or external-evaluation result is upgraded.

### Added

- stateful `sparkbrain.v03.IntegratedV03Brain` with explicit I0--I3 and E0--E2 boundaries;
- actual C15 `RevisionController` integration for I3, registered ablations, action/feedback,
  full-state checkpoint/restore/replay, and engineering-only eight-world evaluation;
- live `/api/v03/*` Brain Lab observer while preserving legacy `/api/runs*`;
- fast, engineering, scientific, reproduction, external, and release test tiers;
- separate version-aware `artifacts/release/v0.3.1/` generation contract.

### Fixed

- private-review ZIP/checksum no-clobber publication across competing writers;
- JSON-safe `examples/v03_seed_demo.py` output;
- reader, theory, architecture, status, migration, Brain Lab, and Codex entrypoints;
- C17 v1 control-gap classification as engineering failure/science not evaluated.

### Not changed

- persisted legacy config/state/trace schema `0.2`;
- additive C18 trace/checkpoint schema `0.3`;
- C06/C08 negative findings, C15 residual non-support, C16 candidate-level result, C17 claim
  boundary, C19 blocked status, CL-007/CL-008 grades, or the owner-license blocker.

## v0.3.0 — 2026-08-28

Private research-release candidate. C11--C18 evidence is retained with its individual engineering
and scientific boundary, C19 is a blocked readiness record, and C20 binds a private-review
manifest/evidence layer. This did not create a public tag, public archive, public release, or
claim-grade upgrade.

## v0.2.1 — 2026-08-22

Documentation and local-execution patch release. The persisted JSON schema remains `0.2`.

### Added

- `docs/START_HERE.md`
- `docs/FOUNDATIONS_FOR_BEGINNERS.md`
- `docs/LOCAL_EXECUTION_POLICY.md`
- expanded plain-language `docs/GLOSSARY.md`
- `scripts/local_readiness_check.py`
- local-only policy tests
- explicit package `__version__`

### Changed

- core completion condition is now a single general-purpose local computer
- CPU reference execution is mandatory; local GPU is optional
- runtime cloud services and remote APIs are not required or permitted as core dependencies
- dedicated neuromorphic hardware moved to independent Extension H
- theory, technical report, charter, status, roadmap, software architecture, Codex instructions, and README updated to v0.2.1

### Compatibility

- Python package version: `0.2.1`
- persisted config/state/trace schema: unchanged at `0.2`
- v0.2 checkpoints and traces remain the intended compatibility target

### Not changed

- Phase-0 engine dynamics
- hand-authored evidence routing
- benchmark results
- scientific claim strength
