# Test tiers

## Purpose

The default suite checks software correctness for the local reference engine, APIs, race/order
guards, checkpoints, traces, and small runner fixtures. It deliberately does not stand in for
scientific-result reproduction or release-artifact regeneration.

## Commands

| Tier | Command | Intended use |
| --- | --- | --- |
| Fast | `python scripts/run_tests.py fast` | Tight development loop; excludes local API/service integration, every `slow` test, and all science, reproduction, and external boundaries. |
| Engineering | `python scripts/run_tests.py engineering` | Normal local software regression, including local API/service integration and small runner correctness fixtures. |
| Scientific | `python scripts/run_tests.py scientific` | Controlled-science implementation/result-contract checks for C15--C17; this does not regenerate official artifacts. |
| Release | `python scripts/run_tests.py release` | Complete marker-inclusive validation, including release/reproduction and external-boundary guards. |

`python -m pytest -q` is the engineering default: it excludes `scientific`, `reproduction`, and
`external`. Pytest chooses its normal collision-safe, per-session temporary directory. The suite
does not force a shared or repository-local `--basetemp`, because stale Windows ownership and
concurrent worktrees can otherwise turn cleanup into a permission failure before a test runs.

## Classification

| Category | Tests | Rationale |
| --- | --- | --- |
| Fast / engineering | Core dynamics, invariants, serialization, API/service integration, C11--C14, C18 guards, and C15--C17 runner fixture checks | Software correctness; no official-science execution or artifact regeneration. |
| Scientific + slow | `test_c15_revision.py`, `test_c16_concepts.py`, `test_c17_organs.py` | Controlled-science implementation and result-contract coverage is preserved but separated from ordinary regression. |
| Reproduction + slow | Clean-room/release/artifact/review bundle modules | These exercise generated artifacts, git/archive contracts, and release reproduction rather than normal behavior. |
| External + slow | C19 and external-validation modules | External-validation adapters and blocked-readiness boundaries remain explicit and excluded from routine regression. |

## Baseline and verification record

- Before classification, collection found 804 tests (2026-08-28).
- The original shared `--basetemp=../.sparkbrain-pytest-runtime` caused concurrently launched
  pytest processes to contend; that run is recorded as invalid for pass/fail timing rather than
  treated as a product regression. The configuration no longer has this cross-worktree collision.
- After v0.3.1 integration and tier classification, collection found 853 tests. Fast executes 457,
  Engineering/default 473, Scientific 156, and Release all 853. The Fast tier is 16 local
  integration tests smaller than Engineering.
- Focused selector/classification tests: 8 passed.
- Fast: 457 passed, 396 deselected in 43.71s. Engineering/default: 473 passed, 380 deselected in
  43.88s.
- Scientific: 156 passed, 697 deselected in 158.59s. The C17 candidate-absence fixture remains a
  scientific negative; its test also asserts the separate historical protected-hash and external
  reproduction gates rather than treating either as scientific support.
- Release runs every marker category. It is the required path for clean-room/reproduction tests;
  it must be run from a source/hash-compatible integration head before treating protected-artifact
  assertions as release failures.
