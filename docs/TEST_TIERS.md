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
`external`. Each worktree uses its own ignored `.pytest-tmp` base directory, so concurrent
worktrees do not contend for the previous shared `../.sparkbrain-pytest-runtime` directory or the
global user temporary directory.

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
- After classification and the eight selector/classification unit tests, collection found 812 tests:
  Fast 420, Engineering/default 436, Scientific 156, Reproduction 163, External 57, and Release
  812. The Fast tier is 16 local integration tests smaller than Engineering.
- Focused selector/classification tests: 8 passed in 0.03s.
- Fast: 414 passed, 6 failed, 392 deselected in 22.85s. Engineering/default: 430 passed, 6 failed,
  376 deselected in 22.71s. The six failures are the known C11/C12 fail-closed protected-hash
  mismatch for `docs/CLAIMS_REGISTER.md`; no marker masks them.
- Scientific: 155 passed, 1 failed, 656 deselected in 172.34s. The failure is the retained C17
  candidate-absence negative-result assertion on this integration head; it remains visible in the
  scientific tier and is not reclassified as a passing result.
- Release runs every marker category. It is the required path for clean-room/reproduction tests;
  it must be run from a source/hash-compatible integration head before treating protected-artifact
  assertions as release failures.
