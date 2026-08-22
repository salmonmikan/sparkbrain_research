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

## 2026-08-23 — R0003 — C02 controlled synthetic suite

**Code/base:** C02 branch from accepted C01 `c5178db`; schema remains `0.2`
**Command:** `python -m sparkbrain.evaluation.run_suite --config configs/experiments/phase1/main.json --output artifacts/phase1/c02-main-1000`
**Data/splits:** frozen local test seeds 200000–200999; 37 declared conditions; 1,000 episodes per condition
**Raw outputs:** `artifacts/phase1/c02-main-1000/raw/` (local, reproducible, approximately 492 MiB)
**Aggregate:** `artifacts/phase1/c02-main-1000/aggregate/metrics.json`

### Result

- SwitchWorld full accuracy was 0.5965, coverage 0.9234, revision recall 0.6839,
  revision precision 0.6761, and mean switch latency 1.6196.
- Removing residual state reduced SwitchWorld accuracy to 0.4180 and delayed-evidence
  accuracy from 0.7035 to 0.4573 in these frozen synthetic distributions.
- Hard-WTA reduced SwitchWorld recovery from 0.7240 to 0.5636 and delayed-evidence recovery
  from 0.9284 to 0.8136.
- GoalConflictWorld changed actions while the measured goal-only belief-flip rate remained
  zero. This is a narrow implementation observation, not a cognitive claim.

### Negative findings and confounds

- MultiObjectWorld full-system coverage and all-step accuracy were both zero: the frozen
  configuration did not ignite object-scoped beliefs. The failure is retained.
- Duplicate evidence produced a non-zero paired score change on average; evidence-record
  identity deduplication does not guarantee activation-level invariance.
- The supplementary frozen reliability run reported source-reliability sensitivity of
  0.0175 for the full condition; this small descriptive difference is not a calibrated
  reliability claim.
- Coalition softmax values were used only for descriptive Brier/ECE; they are not calibrated
  probabilities.
- The generators and evidence weights remain hand-authored, and no learned or modern matched
  baseline is present. No general superiority claim is supported.
- Main bootstrap intervals are descriptive. No p-value family or significance-ranking claim
  was made.

**Claim impact:** CL-003 and CL-006 remain E2; CL-007 remains E0.
**Next action:** C04/C05 consume the immutable Episode/split contracts without tuning on C02
test seeds. Multi-object ignition requires dev-only diagnosis before a new frozen evaluation.

---

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
- GitHub Actions CI: PASS on Python 3.11 and 3.13, run `32594805438`.

### Compatibility and limitations

Schema remains `0.2`; no migration is introduced. The stricter validators reject incomplete payloads that omitted required deterministic state, including `broadcast_listeners`. This is validation hardening rather than reinterpretation of valid v0.2 artifacts. The clean CI matrix passed on the two repository-supported Python versions; this does not establish compatibility with untested environments.

---

## 2026-08-23 — R0004 — C03 localhost Brain Lab acceptance

**Code/version:** SparkBrain package v0.2.1; persisted engine schema v0.2; Brain Lab schema v1
**Nature:** optional local UI/control plane; no intended core dynamics change
**Primary commands:** `python -m pytest -q`, `python -m ruff check .`, `python scripts/measure_brain_lab.py`, `python scripts/run_brain_lab.py`

### Changes under test

- loopback-only FastAPI control plane and bundled no-CDN frontend;
- nine UI regions for graph, timeline, belief, Workspace, inspection, control, intervention, comparison, and export/import;
- deterministic pause, single-step, run, reset, and validated event injection;
- parent-preserving checkpoint fork with edge, Spark, organ, and threshold interventions;
- frame-index synchronized comparison, blind-safe API/export, and local bundle import;
- static visualizer fallback and pure-inspection non-interference.

### Validation outcome

- tests: 68 passing, including 13 focused Brain Lab API/service/E2E contract tests;
- Ruff: PASS;
- canonical UI/API flow: CAT → TOY → CAT with evidence provenance;
- 2,000-Spark / 10,000-edge relevant-subset preparation: 0.9654 ms for 250 Sparks / 600 edges;
- 60 FPS preparation budget (16.6667 ms): PASS;
- loopback startup and non-loopback rejection: PASS;
- offline bundled assets, keyboard/focus/accessibility contract, blind truth removal, and import/export regression: PASS.

### Limitations retained

- the measured time covers deterministic subset preparation, not browser paint or end-to-end frame time;
- the run registry is in-memory and single-process; exported bundles are required across restarts;
- SSE reports a finite current-frame snapshot and does not create a background simulation queue;
- the native SVG graph is a functional view, not a biological anatomy claim;
- no energy-efficiency claim follows from UI timing.

---

## 2026-08-23 — R0005 — C07 reduced snnTorch hybrid equivalence

**Code/version:** `codex/c07-spiking-backend`; schema `0.2` unchanged
**Command:** `python scripts/run_spiking_comparison.py`
**Data/seed:** fixed seven-event SwitchWorld CAT→TOY→CAT; seed 7
**Raw outputs:** `artifacts/spiking/c07_comparison.json`, `rate_trace.json`, `spike_trace.json`
**Aggregate:** `artifacts/spiking/c07_report.md`

### Result

- all 9 frozen comparison checks passed;
- hybrid predictions exactly matched `[None, cat, cat, cat, toy, toy, cat]`;
- distinct ignition order matched `[cat, toy, cat]`;
- focused tests preserved no-ignition, duplicate evidence, residual recovery, Workspace
  capacity, directional edge ablation, protocol conformance, and state replay.

### Negative findings and confounds

- LIF threshold 1.1 produced no sensory spikes and no predictions;
- equivalence is parameter-sensitive and covers one hand-authored scenario;
- only sensory encoding is spiking; Coalition and Workspace remain algorithmic/rate;
- local wall-clock is not an energy measurement;
- no fully spiking, learned, surrogate-gradient, or local-plasticity comparison was done.

### Claim impact

CL-009 advances only to E1 for this reduced hybrid canonical fixture. It does not establish
general spiking equivalence, biological fidelity, efficiency, or multi-world robustness.
