# Results and Negative-Result Ledger

Append entries; do not rewrite prior outcomes to match later interpretations.

## 2026-08-22 — R0001 — Phase-0 SwitchWorld software validation

**Code/version:** SparkBrain prototype v0.2 bundle  
**Command:** `python scripts/run_benchmark.py --episodes 40 --steps 30`  
**Data:** seeded synthetic SwitchWorld; hand-authored evidence mapping  
**Raw outputs:** `artifacts/benchmarks/benchmark_results.json`  
**Aggregate:** `artifacts/benchmarks/benchmark_aggregate.csv`

### Observations

- full SparkBrain all-step accuracy was 0.6400 and coverage 0.9367;
- accumulator all-step accuracy was 0.6283, so the full system did not clearly dominate this simple baseline;
- removing residual state reduced accuracy to 0.4567 and coverage to 0.8183 in this distribution;
- single-Spark ignition improved revision precision relative to full SparkBrain but worsened latency and recovery in some measures;
- instant classification revised rapidly but produced many unnecessary revisions;
- algorithmic active-Spark counts are not hardware energy measurements.

### Interpretation

This run validates that the software exposes a stability/revision trade-off and that the selected ablations alter it. It does not establish generalization, learning ability, biological fidelity, or modern-model superiority.

### Negative or inconvenient findings retained

- the accumulator baseline is competitive;
- the reference engine's event fan-out can yield more Spark updates than a scalar baseline;
- hand-authored evidence weights may encode much of the task solution;
- some Phase-0 metrics are sensitive to coverage and forced-prediction differences.

### Follow-up

C01 must audit counters and replay; C02 must add controlled distributions and confidence intervals; C04/C05 must replace hand-authored-only comparisons with learned matched systems.

---

## Entry template

```text
## YYYY-MM-DD — R#### — title
Code/version:
Command:
Data/splits:
Seeds:
Raw outputs:
Aggregate:
Hypothesis:
Result:
Negative findings:
Confounds:
Claim grade impact:
Next action:
```

## 2026-08-22 — R0002 — v0.2.1 local-scope and documentation expansion

**Code/version:** SparkBrain package v0.2.1; persisted schema v0.2  
**Nature:** documentation, local-execution contract, validation guard; no intended dynamics change  
**Primary commands:** `python scripts/local_readiness_check.py`, `python -m pytest -q`, `python scripts/validate_bundle.py`

### Changes under test

- core completion constrained to one general-purpose local computer;
- CPU reference path made mandatory;
- remote runtime services excluded from core dependencies;
- dedicated hardware moved to Extension H;
- beginner foundation guide and expanded glossary added;
- local-readiness checks added;
- package version advanced to 0.2.1 while schema remains 0.2.

### Scientific result

None claimed. This patch does not increase the evidence grade of H1–H10 or establish a performance improvement.

### Validation outcome

- local readiness: PASS on Python 3.13.5 / Linux x86_64;
- tests: 30 passing;
- canonical demo: CAT → TOY → CAT reproduced;
- checkpoint state hash: `cedc8543d87677d2cbf1707f0df2ec7d95e8a1d31b735a40a917d9de9d7ff13c`;
- bundle validation: 23 required artifacts validated;
- benchmark aggregate CSV: byte-identical to archived v0.2;
- canonical trace JSON: byte-identical to archived v0.2;
- ruff: not executed in the packaging environment because it was not installed.

### Compatibility target

The Phase-0 dynamics and persisted config/state/trace schema are intended to remain compatible with v0.2. The byte-identical benchmark aggregate and canonical trace support that narrow compatibility statement for the bundled scenarios; they do not prove compatibility for every possible checkpoint or graph.

---

## 2026-08-23 — R0003 — C01 deterministic reference and replay contract

**Code/version:** SparkBrain package v0.2.1; persisted schema v0.2
**Nature:** reference-engine hardening and compatibility validation; no intended dynamics change
**Primary commands:** `python -m pytest -q`, `python -m ruff check .`, `python scripts/local_readiness_check.py`, `python scripts/validate_bundle.py`

### Changes under test

- deterministic continuation includes the pending event queue, sequence counter, RNG, stability, Workspace, eligibility, counters, trace, and frame-local audit buffers;
- pure `inspect_snapshot()` is separated from backward-compatible recording `snapshot()`;
- generated config, checkpoint, trace, summary, and benchmark JSON are validated against schema `0.2`;
- `broadcast_listeners` is required by both runtime and JSON Schema validation;
- equal-time ordering, event-limit diagnostics, invalid payloads, evidence identity, contradiction provenance, no-ignition, recovery, cooldown, refractory, homeostasis, Workspace, and plasticity boundaries are covered by focused tests.

### Validation outcome

- local readiness: PASS;
- tests: 55 passing;
- Ruff: PASS;
- fresh canonical state hash: `ba166f0e801665e98c200f8a291fdf475f2dbbc6d86232867e21b1f08226caa5` on two independent runs;
- normalized fresh-run traces: identical;
- generated-artifact schema regression: PASS;
- Phase-0 benchmark aggregate values: unchanged; persisted JSON documents gained explicit schema metadata only.

### Compatibility and limitations

Schema remains `0.2`; no migration is introduced. The stricter validators reject incomplete payloads that omitted required deterministic state, including `broadcast_listeners`. This is validation hardening rather than reinterpretation of valid v0.2 artifacts. Local validation does not replace a successful clean CI run on every supported Python version.
