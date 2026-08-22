# SparkBrain v0.2.1 Package Contents

- Package version: `0.2.1`
- Persisted config/state/trace schema: `0.2`
- Main entry point: `README.md`
- First reader guide: `docs/START_HERE.md`
- Current status: `docs/PROJECT_STATUS.md`
- Local execution contract: `docs/LOCAL_EXECUTION_POLICY.md`
- File-level hashes: `PACKAGE_MANIFEST.json`

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
```

Current packaging validation:

- local readiness: PASS
- tests: 30 passing
- canonical final belief: CAT
- checkpoint state SHA-256: `cedc8543d87677d2cbf1707f0df2ec7d95e8a1d31b735a40a917d9de9d7ff13c`
- v0.2.1 demo trace and aggregate benchmark: byte-identical to archived v0.2
- ruff was not available in the packaging environment and was not executed
