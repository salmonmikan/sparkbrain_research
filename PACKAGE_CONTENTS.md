# SparkBrain v0.2.1 Package Contents

- Package version: `0.2.1`
- Persisted config/state/trace schema: `0.2`
- Main entry point: `README.md`
- First reader guide: `docs/START_HERE.md`
- Current status: `docs/PROJECT_STATUS.md`
- Local execution contract: `docs/LOCAL_EXECUTION_POLICY.md`
- File-level hashes: `PACKAGE_MANIFEST.json`
- Archive-mode hash binding: `RELEASE_METADATA.json`

## v0.2.1 expansion

- formalized single-machine local completion condition
- CPU reference path required; local GPU optional
- mandatory remote runtime services prohibited
- dedicated hardware moved to independent Extension H
- beginner foundation guide added
- glossary expanded with plain-language definitions and non-implications
- local-readiness checker and local-only tests added
- package version updated without changing persisted schema or Phase-0 dynamics

## Core research documents

- `docs/START_HERE.md`
- `docs/FOUNDATIONS_FOR_BEGINNERS.md`
- `docs/GLOSSARY.md`
- `docs/LOCAL_EXECUTION_POLICY.md`
- `docs/PROJECT_CHARTER.md`
- `docs/THEORY_SPEC_v0.2.1.md`
- `docs/HYPOTHESES_AND_FALSIFICATION.md`
- `docs/PRIOR_ART_GAP_ANALYSIS.md`
- `docs/TECHNICAL_REPORT_DRAFT_v0.2.1.md`
- `docs/EXPERIMENT_PROTOCOL.md`
- `docs/MASTER_ROADMAP.md`

## Runnable implementation

- `src/sparkbrain/engine.py`
- `src/sparkbrain/model.py`
- `src/sparkbrain/worlds.py`
- `src/sparkbrain/serialization.py`
- `src/sparkbrain/replay.py`
- `src/sparkbrain/validation.py`

## Local validation

- `scripts/local_readiness_check.py`
- `tests/test_local_only.py`
- `scripts/validate_bundle.py`
- `scripts/validate_release.py`
- `scripts/build_review_bundle.py`
- `tests/test_release.py` includes validator classification and scientific integrity fixtures
- `.github/workflows/ci.yml` as an optional mirror of local checks

## Visualizer and evidence

- `artifacts/demo/visualizer.html`
- `artifacts/demo/trace.json`
- `artifacts/demo/checkpoint.json`
- `artifacts/demo/summary.json`
- `artifacts/benchmarks/benchmark_report.md`
- `artifacts/benchmarks/benchmark_aggregate.csv`
- `artifacts/benchmarks/benchmark_results.json`

## Codex handoff

- `AGENTS.md`
- `.agents/skills/sparkbrain-research/SKILL.md`
- `docs/CODEX_EXECUTION_BRIEF.md`
- `docs/codex/C01_ENGINE_HARDENING.md` through `C10_REPRODUCIBILITY_RELEASE.md`
- `docs/codex/PROMPTS.md`

## Version history

- `archive/v0.1/` preserves the first minimal prototype
- `archive/v0.2/` preserves the original v0.2 release materials and source ZIP
- `CHANGELOG.md` summarizes the v0.2.1 patch

## Verified commands

```bash
python scripts/local_readiness_check.py
python -m pytest -q
python scripts/run_demo.py
python scripts/checkpoint_demo.py
python scripts/replay_trace.py
python scripts/run_benchmark.py --episodes 40 --steps 30
python scripts/validate_bundle.py
python scripts/validate_release.py --preparation-only
```

Current packaging validation:

- local readiness: PASS
- the repository and no-`.git` archive test suites are authoritative; dated counts remain in
  `docs/RESULTS_LEDGER.md` rather than this living package index
- canonical final belief: CAT
- Ruff: PASS
- bundle validation: PASS
- offline primary-subset reproduction: PASS with exact table/SVG hashes
- integrity/preparation/evidence validation: PASS
- public release validation: blocked only by owner license selection

## C10 release-candidate evidence

- `requirements-release.lock` and its provenance record pin the tested Windows/Python 3.13
  candidate snapshot; they do not claim a universal wheel lock.
- `scripts/reproduce_release.py` is the single offline CPU smoke command and writes a local
  machine-readable run manifest.
- `artifacts/release/primary_subset.json` freezes the bounded input/output hashes and states
  that the subset is not a full evaluation.
- `artifacts/release/evidence_map.json` and `provenance.json` connect claims, runs, inputs, and
  generated products.
- `scripts/build_release_archive.py` refuses to create a public archive while the project
  license gate remains blocked.
- repository mode checks tracked-file completeness and Git ancestry; archive mode checks the
  fixed release metadata and packaged file hashes without invoking Git.
- archive validation is fail-closed before runtime tests; the later plain pytest phase writes
  temporary test data outside the archive root and disables the pytest cache provider.
- `scripts/build_review_bundle.py` builds the separately scoped private review ZIP. Its embedded
  `REVIEW_BUNDLE_MANIFEST.json` lists every ZIP member except itself, and the adjacent
  `.sha256` file authenticates the ZIP byte stream.
