# RV02-RD002 — boundary-input gain result

## Outcome

The fixed post-training gain grid completed all 18 development cells and 468 probes.
Gain 4 recruited 83 hidden spikes across 35 of 78 natural route probes. It changed
full visible final UnitState in 33 probes, but changed no visible spike sequence and
improved no task score. Gains 1 and 2 recruited no hidden spikes. The preregistered
useful-development-effect criterion is not supported at either gain 2 or gain 4.
This is a mechanism diagnosis on exposed development fixtures, not a formal result.

| Natural condition | Hidden-spiking probes | Hidden spikes | Visible trace differences vs cut | Visible state differences vs cut | Strict exact routes | Off-route errors | Excess route events |
|---|---:|---:|---:|---:|---:|---:|---:|
| Gain 1 | 0 / 78 | 0 | 0 / 78 | 0 / 78 | 24 / 78 | 492 | 48 |
| Gain 2 | 0 / 78 | 0 | 0 / 78 | 0 / 78 | 24 / 78 | 492 | 48 |
| Gain 4 | 35 / 78 | 83 | 0 / 78 | 33 / 78 | 24 / 78 | 492 | 48 |

All three cut conditions have the same task scores as the natural conditions.
Ordered retention is 1.0 throughout and has no room to improve; strict recovery and
raw error counts expose the inherited ambiguity and extra outputs. These dependent
route diagnostics are not independent statistical replicates. Per-family/scale
results and the complete conservative decision-rule reconstruction are in
`RV02_RD002_INDEPENDENT_INTERPRETATION.md`.

## Execution and retained evidence

- Exact executed local source: `58f196b006020b144cf62c695ca1c1fff8e7087e`.
- Source, preregistration, tests and independent audit were committed after separate
  pre-execution engineering and scientific reviews, before this single grid run.
- Output: `artifacts/research/rv02/rd002/`.
- Raw uncompressed SHA-256: `3548b20d3e8e0003ffd6f5964888b948a9d3cf39c28b2167385ea9ff5a433ee4`.
- Raw gzip SHA-256: `8f5e2929d8f4ed9b4a91ecf9eef6434ef8812240220379c16db190fddb106257`.
- Exact local history: `executed_source.bundle`, SHA-256
  `f365ef4b82d1672b427dd4e6f02443b4d5c2c09826742359d0021ff9cb41fe3d`;
  prerequisite `2f2aae612ee6e0f08453c855a9910d965fa89bec`.

The GitHub API publication commit differs from the local executed-source commit.
The saved source manifest and verified Git bundle bind the actual execution; a
publication SHA must not be substituted for that execution identity.

The summed worker wall time was 48.45 seconds and peak reported RSS was 92,272 KiB.
All cells completed within the fixed native arrival/spike, 60-second worker,
600-second total and 1-GiB limits. No condition failed and no retry occurred.
A live queue at 140 ms is horizon truncation, not proof of runaway or stability.

## Reproduction and validation

```bash
python scripts/run_rv02_boundary_recruitment.py --output /fresh/local/rd002-output
python scripts/run_rv02_boundary_recruitment.py --verify artifacts/research/rv02/rd002
PYTHONPATH=src python scripts/audit_rv02_boundary_recruitment.py artifacts/research/rv02/rd002
PYTHONPATH=src python -m unittest discover -s tests -p 'test_rv02*.py' -q
python scripts/local_readiness_check.py
```

At source freeze, all 63 focused RV02 tests passed, including 14 new reserved
synthetic intervention/scoring/raw-audit tests. Local readiness passed on Python
3.12.14. Full pytest, ruff and the repository-wide validation sequence were not
available in this environment; they are not reported as passed. Separate final
raw-only acceptance is documented in `RV02_RD002_INDEPENDENT_ACCEPTANCE.md`.

## Boundary and next question

Input gain can cross the hidden threshold without changing the learner or threshold.
Hidden spikes then affect visible subthreshold/provenance state in some probes.
This does not establish useful distributed computation, learned hidden structure,
capacity advantage, or stability beyond the 40-ms window. The unchanged external-only
learner still has no hidden external trace or hidden-edge update.

The RD001 baseline and all older runtime/result bytes remain unchanged. No new
formal candidate, held-out evaluation, baseline tuning, reservoir comparison,
claim-grade increase or main-branch merge is included. A different learning or
return-path intervention requires a separate preregistered development study.
