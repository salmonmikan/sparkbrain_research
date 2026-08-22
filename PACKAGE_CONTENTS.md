# SparkBrain v0.2 Package Contents

- Files: 76
- Uncompressed size: 632,241 bytes
- Main entry point: `README.md`
- Current status: `docs/PROJECT_STATUS.md`

## Core research documents

- `docs/PROJECT_CHARTER.md`
- `docs/THEORY_SPEC_v0.2.md`
- `docs/HYPOTHESES_AND_FALSIFICATION.md`
- `docs/PRIOR_ART_GAP_ANALYSIS.md`
- `docs/TECHNICAL_REPORT_DRAFT_v0.2.md`

## Runnable implementation

- `src/sparkbrain/engine.py`
- `src/sparkbrain/model.py`
- `src/sparkbrain/worlds.py`
- `src/sparkbrain/serialization.py`
- `src/sparkbrain/replay.py`

## Visualizer and evidence

- `artifacts/demo/visualizer.html`
- `artifacts/demo/trace.json`
- `artifacts/demo/checkpoint.json`
- `artifacts/benchmarks/benchmark_report.md`

## Codex handoff

- `AGENTS.md`
- `.agents/skills/sparkbrain-research/SKILL.md`
- `docs/CODEX_EXECUTION_BRIEF.md`
- `docs/codex/PROMPTS.md`

## Quality and reproducibility

- `tests/`
- `schemas/`
- `.github/workflows/ci.yml`
- `scripts/validate_bundle.py`
- `artifacts/validation_manifest.json`

## Verification

```bash
python -m pytest -q
python scripts/run_demo.py
python scripts/checkpoint_demo.py
python scripts/run_benchmark.py --episodes 40 --steps 30
python scripts/validate_bundle.py
```

The package manifest lists SHA-256 hashes for every included source file. The outer ZIP hash is provided separately.
