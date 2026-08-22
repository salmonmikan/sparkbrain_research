# Hypotheses and Falsification Matrix — v0.2.1

## 1. Research posture

SparkBrain is a family of falsifiable computational hypotheses, not one indivisible claim. Failure of a high-level claim must not be hidden by changing the task, metric, or terminology after seeing results. Each hypothesis below can fail independently.

## 2. Primary hypotheses

### H1 — Persistent competing beliefs improve non-monotonic revision

**Claim:** Keeping several explicit, nonzero belief states across events can improve the trade-off between resisting noise and responding to decisive new evidence.

**Null:** A matched recurrent or probabilistic state model performs equally well or better without explicit competing Spark objects.

**Required test:** C02 controlled worlds plus C04/C05 matched learned systems.

**Decisive metrics:** revision precision/recall, no-update retention, switch latency, calibration, recovery.

**Falsification condition:** SparkBrain is Pareto-dominated across held-out worlds and matching regimes, or the effect disappears when representation/training capacity is controlled.

**Allowed response to failure:** narrow or remove H1; do not redefine “belief” after results.

### H2 — Residual loser retention is a useful causal mechanism

**Claim:** Preserving inactive losing hypotheses supports later recovery without causing unacceptable false revisions.

**Null:** Residual state is unnecessary, or its benefits are fully reproduced by generic recurrent memory.

**Required test:** residual coefficient sweep, zero-residual ablation, matched-memory controls, returning-state episodes.

**Falsification condition:** no robust recovery gain on held-out recurrent-state episodes, or gain is outweighed by false certainty/revision across preregistered utility ranges.

### H3 — Evidence Coalitions improve epistemic robustness

**Claim:** Treating distinct evidence identities/sources as a temporary graph and gating ignition by diversity, contradiction, stability, and margin improves duplicate/correlated/noisy evidence handling.

**Null:** A scalar accumulator or learned readout performs equivalently after calibration.

**Required test:** ReliabilityWorld, duplicate evidence, correlated sources, contradiction, learned scorer ablations.

**Falsification condition:** Coalition components add no held-out robustness beyond a matched scalar or Bayesian baseline, or trace provenance is not causally faithful.

### H4 — No-ignition is a valuable computational state

**Claim:** Permitting the system to remain unresolved at the Workspace gate improves selective prediction and reliability compared with always forcing a belief.

**Null:** calibrated forced prediction or ordinary abstention head is equivalent.

**Required test:** coverage-risk curves, abstention baselines, out-of-distribution and insufficient-evidence cases.

**Falsification condition:** no-ignition is uncalibrated, collapses, or provides no utility above matched abstention mechanisms.

### H5 — Event-routed execution can reduce algorithmic work

**Claim:** Lazy decay and active-set event routing can avoid state/edge updates for dormant Sparks while retaining target behavior.

**Null:** bookkeeping and recurrent event fan-out remove any useful work reduction, or dense implementations are superior at all meaningful scales.

**Required test:** scale sweeps, audited state updates/messages, dense-equivalent implementation, quality-matched comparisons.

**Falsification condition:** SparkBrain requires equal or more algorithmic operations at matched quality across intended sparse regimes.

**Important:** H5 is not an energy hypothesis. Hardware energy requires H9-style direct measurement.

### H6 — Workspace broadcast enables useful cross-organ coordination

**Claim:** A capacity-limited broadcast improves information sharing between specialized modules without requiring all-to-all dense communication.

**Null:** direct communication, a shared recurrent state, or attention is equally effective and efficient.

**Required test:** no-broadcast, dense communication, direct routed communication, capacity sweeps, multi-task transfer.

**Falsification condition:** broadcast adds no robust coordination benefit or acts only as an unnecessary bottleneck.

### H7 — Learned routing can preserve inspectability

**Claim:** A trainable router and representation can generalize while retaining stable Spark IDs/roles, evidence paths, and causal trace usefulness.

**Null:** learned representations become uninterpretable or explanations are post-hoc and unfaithful.

**Required test:** held-out routing, attribution intervention, route stability, trace-to-output causal deletion/addition.

**Falsification condition:** cited evidence/routing is not causally connected to belief, or semantic labels are unreliable enough to mislead observers.

## 3. Secondary and high-risk hypotheses

### H8 — Functional organs can emerge

Candidate specialization must pass held-out reuse and causal ablation controls. Graph clustering alone is insufficient. Failure is expected and scientifically valid.

### H9 — A spiking substrate can preserve theory-level behavior

Rate and spiking backends should satisfy predefined invariants within tolerance. Failure may reveal that the current theory depends on rate-specific operations.

### Extension H10 — Dedicated-hardware execution improves energy efficiency

This is outside the core theory completion criteria. It requires matched workload, direct hardware power measurement, accuracy/latency controls, and platform disclosure. Event sparsity, spike counts, or local CPU/GPU runtime alone cannot support this claim.

## 4. Experiment-to-hypothesis map

| Experiment family | H1 | H2 | H3 | H4 | H5 | H6 | H7 | H8 | H9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| SwitchWorld Phase-0 | weak | weak | weak | weak | weak | weak | no | no | no |
| C02 controlled worlds | medium | strong | strong | strong | medium | medium | no | no | no |
| C04 learned routing | strong | strong | strong | strong | strong | medium | strong | no | no |
| C05 matched baselines | strong | strong | strong | strong | strong | strong | medium | no | no |
| C06 external validation | strong | strong | strong | strong | medium | medium | strong | no | no |
| C07 spiking equivalence | medium | medium | medium | medium | medium | medium | medium | no | strong |
| C08 structural plasticity | medium | medium | medium | medium | medium | strong | strong | strong | no |

“Weak/medium/strong” denotes how directly an experiment can bear on a hypothesis, not the expected result.

## 5. Anti-p-hacking commitments

Before a primary test run:

- freeze task generation and test seeds;
- freeze primary metrics and utility trade-offs;
- specify exclusion/failure rules;
- allocate equal tuning budgets;
- preserve all seeds and failed runs;
- record any post-hoc analysis as exploratory;
- do not promote an exploratory metric to primary because it is favorable.

## 6. Theory revision protocol

When a hypothesis fails:

1. append the result to `RESULTS_LEDGER.md`;
2. downgrade the corresponding claim grade;
3. identify whether failure concerns mechanism, implementation, task, or measurement;
4. propose the smallest revised hypothesis;
5. run a new preregistered experiment rather than rewriting the old prediction;
6. preserve the original theory version and migration note.
