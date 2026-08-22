# Changelog

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
