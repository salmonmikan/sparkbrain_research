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
| Fast / engineering | Core dynamics, invariants, serialization, C11--C14, C18 guards, and C15--C17 runner fixture checks | Software correctness; no official-science execution or artifact regeneration. |
| Engineering integration | Brain Lab API/service and end-to-end modules, including the v0.3.1 API and v0.3.2 runtime/direct-checkpoint facade | Multi-component local regressions are retained in Engineering and excluded from Fast. |
| Scientific + slow | `test_c15_revision.py`, `test_c16_concepts.py`, `test_c17_organs.py` | Controlled-science implementation and result-contract coverage is preserved but separated from ordinary regression. |
| Reproduction + slow | Clean-room/release/artifact/review bundle modules | These exercise generated artifacts, git/archive contracts, and release reproduction rather than normal behavior. |
| External + slow | C19 and external-validation modules | External-validation adapters and blocked-readiness boundaries remain explicit and excluded from routine regression. |

I3 integration tests use the optional learned Torch runtime when it is installed and are reported
as skips in a clean `.[dev]` environment without Torch. Dependency-light v0.3.1 tests continue to
run in both environments; installing `.[learned]` activates the real I3 integration checks.

## Baseline and verification record

- Before classification, collection found 804 tests (2026-08-28).
- The original shared `--basetemp=../.sparkbrain-pytest-runtime` caused concurrently launched
  pytest processes to contend; that run is recorded as invalid for pass/fail timing rather than
  treated as a product regression. The configuration no longer has this cross-worktree collision.
- After the final v0.3.1 audit corrections, collection found 855 tests. Fast executes 454,
  Engineering/default 475, Scientific 156, and Release all 855. The Fast tier is 21 local
  integration tests smaller than Engineering.
- Focused selector/classification tests: 8 passed.
- Fast: 454 passed, 401 deselected in 42.68s. Engineering/default: 475 passed, 380 deselected in
  46.53s. Both runs used the same local checkout and optional Torch was available.
- Scientific collection remains 156 tests; the last full run passed 156 with 697 deselected in
  158.59s. The C17 candidate-absence fixture remains a
  scientific negative; its test also asserts the separate historical protected-hash and external
  reproduction gates rather than treating either as scientific support.
- Release collected and passed all 855 tests in 501.98s. This includes
  all scientific, reproduction, external-boundary,
  private-bundle, and no-Git clean-room checks. The Windows clean-room fixture uses a short,
  session-unique system temporary root so path-length limits do not weaken the archive contract.
- Release runs every marker category. It is the required path for clean-room/reproduction tests;
  it must be run from a source/hash-compatible integration head before treating protected-artifact
  assertions as release failures.
- The v0.3.2 development collection contains 892 tests: Fast 469, Engineering/default 502,
  Scientific 156, and Release 892. The new metric and input-semantics contracts remain Fast;
  runtime/direct-checkpoint tests are Integration; native release publication tests are Slow +
  Reproduction. Fast passed 469 with 423 deselected in 47.06s and Engineering passed 502 with 390
  deselected in 48.44s on 2026-08-28. Scientific and Release were collected but not fully executed
  for this engineering development commit.
