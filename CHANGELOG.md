# Changelog

## v0.3.1 — corrective patch in progress

This entry reserves the corrective boundary; the package metadata remains `0.3.0` until the
versioned release implementation is completed. No scientific artifact, claim grade, or external
evaluation result is changed by documentation synchronization.

### Planned corrective scope

- make the private-review ZIP and checksum publication no-clobber across competing writers;
- make `examples/v03_seed_demo.py` emit JSON-safe state;
- add the v0.3 theory specification and synchronize reader and Codex entrypoints;
- define, without claiming completion, the versioned `sparkbrain.v03` integrated-runtime boundary.

### Not changed

- persisted legacy config/state/trace schema `0.2`;
- additive C18 trace/checkpoint schema `0.3`;
- C06 external negative result; C15/C17 negative scientific findings; C16 candidate-only result;
- C19 `blocked` / `not_evaluated` status; project-license public-release gate.

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
