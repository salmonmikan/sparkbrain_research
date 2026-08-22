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
