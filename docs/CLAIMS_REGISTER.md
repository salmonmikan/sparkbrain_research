# Claims Register — v0.2.1

This file separates implementation facts, observed results, supported research claims, and prohibited statements.

## Evidence grades

| Grade | Meaning |
|---|---|
| E0 | design intention or hypothesis only |
| E1 | implemented and unit-tested behavior |
| E2 | observed in controlled seeded synthetic experiments |
| E3 | replicated across held-out tasks and matched baselines |
| E4 | independently reproduced or supported by multiple external evaluations |
| E5 | biological/hardware claim directly measured with suitable instruments and controls |

## Active claims

| ID | Claim | Current grade | Required upgrade evidence |
|---|---|---:|---|
| CL-001 | Persistent competing belief objects can be represented and inspected in a deterministic event-driven engine. | E1 | independent replay and schema conformance |
| CL-002 | Coalition-level ignition can require score, margin, stability, and source diversity. | E1 | expanded adversarial tests |
| CL-003 | A losing belief can retain state and later recover after new evidence. | E2 | matched learned baselines and external tasks |
| CL-004 | No-ignition can be represented and development-calibrated in reference and learned controlled-synthetic backends. | E2 | external tasks and matched calibration baselines |
| CL-005 | Event routing can avoid touching every dormant Spark in the reference algorithm. | E1 | audited counters and scale study |
| CL-006 | Residual retention improves belief revision in the current hand-authored SwitchWorld and delayed-evidence distributions. | E2 | matched learned baselines and external tasks |
| CL-007 | SparkBrain improves the stability/adaptability frontier over strong neural baselines. | E0 | C04–C06 |
| CL-008 | Learned Spark groups form stable functional organs. | E0 | C08 causal specialization tests |
| CL-009 | A reduced snnTorch LIF hybrid preserves the frozen canonical SparkBrain behavior. | E1 | fully spiking mapping, multiple held-out worlds, and independent reproduction |
| CL-010 | Dedicated-hardware execution is more energy efficient. Extension H only. | E0 | direct hardware measurement, matched workloads, accuracy/latency controls, power methodology |
| CL-011 | The deterministic reference engine and static visualizer can run on one local CPU machine without a remote runtime service. | E1 | clean-room run on additional supported platforms |

## Prohibited public claims at v0.2.1

- “The human brain has been reproduced.”
- “The system is conscious.”
- “This is AGI.”
- “The theory is completely novel.”
- “SparkBrain is better than Transformers.”
- “Sparse activity proves lower energy use.”
- “Organs emerged autonomously.”

## C09 prior-art audit status (2026-08-23)

This status is separate from evidence grades. It does not raise or lower any grade above.

The adversarial second pass additionally reviewed HEARSAY-II, active inference, attractor and HMM baselines, asynchronous sparse convolution, bipolar argumentation, and neuromorphic dynamic-field memory. It strengthens the constraints below but does not change an evidence grade. See `docs/research/claim_challenge_report.md` for the matrix-derived strongest counterexample per target.

| Claim IDs | Current prior-art verdict | Strongest reviewed counterexample(s) | Public framing constraint |
|---|---|---|---|
| CL-001, CL-002, CL-004 | partial overlap / strong near-duplicate at mechanism level | LIDA; Global Neuronal Workspace; Shared Global Workspace | Do not describe persistent state, coalition, ignition, workspace competition, or broadcast as original mechanisms. |
| CL-003, CL-006 | partial overlap; performance difference unverified | Dynamic Field Theory; Adaptive Resonance Theory | Residual-loser recovery is a testable evaluation emphasis only until controlled ablations reproduce an advantage. |
| CL-005 | partial overlap; strong execution precedent | RIMs; AEGNN | Claim only audited reference-algorithm behavior. Activity ratios alone do not establish true no-touch execution or efficiency. |
| CL-007 | unsupported | Shared Global Workspace; RIMs; established neural baselines | No performance-frontier claim before C04–C06 matched, held-out experiments. |
| CL-008 | unsupported | Assembly Calculus; existing modular and plastic systems | No emergent-organ claim before causal specialization and held-out reuse tests. |
| CL-009 | known research program; unsupported for SparkBrain | Shanahan spiking workspace; Spaun | C07 may report behavioral equivalence or failure only; spiking implementation is not novelty by itself. |
| CL-010 | unsupported; Extension H only | no C09 efficiency conclusion | Preserve the direct-hardware-measurement requirement. |
| CL-011 | engineering implementation claim | local cognitive and neural simulators | Local-only execution is a reproducibility constraint, not a scientific contribution. |

See `docs/research/literature_matrix.csv` for source-level verdicts and `docs/research/closest_systems.md` for the rationale.

## C02 controlled-result boundary (run `c02-main-1000`)

- CL-003/CL-006 remain E2. Frozen synthetic ablations reproduced a residual-state advantage
  in SwitchWorld and DelayedEvidenceWorld, but this does not establish generalization.
- MultiObjectWorld full-system coverage was zero in the frozen run. No multi-object success
  claim is permitted from C02.
- Source-reliability, contradiction, calibration, and work metrics are descriptive for a
  hand-authored system. They do not raise CL-007 or any biological/energy grade.

## C04 claim change record (run `learned-routing-v1/main`)

- **Claim:** CL-004 advances from E1 to E2 only for representing and development-calibrating
  no-ignition in the controlled-synthetic learned backend.
- **Config/seeds:** `configs/experiments/phase2/main.json`; C02 dev manifest prefix from seed
  100000 for training and its disjoint suffix for calibration; test prefix from seed 200000.
- **Raw/aggregate:** `artifacts/phase2/learned-routing-v1/main/held-out-rows.json` and
  `summary.json`; immutable split hashes are in `manifest-evidence.json`.
- **Baselines/ablations:** chance, training-majority non-learning baseline, and all conditions
  in `ablations.json`; coefficient and active-set sensitivity are in `sensitivity.json`.
- **Method:** confidence and margin thresholds are selected only on development calibration
  episodes. The main held-out run had coverage 0.7796 with 476 no-ignition steps, so the gate
  was neither always-on nor always-off.
- **Confounds:** generated C02 worlds only; 60/1,000 test seeds; no matched learned calibration
  baseline; primary unseen-bigram count was zero; derived stresses are separately labeled;
  router load collapse remains. No CL-007, external-generalization, or superiority upgrade.
- **Reproduction status:** one local CPU run plus deterministic training and checkpoint tests;
  no independent reproduction.
- **Permitted wording:** “The controlled-synthetic learned backend preserves a
  development-calibrated no-ignition state.” Do not generalize this to external tasks or
  calibrated uncertainty broadly. See `docs/C04_LEARNED_ROUTING_RESULTS.md`.

## C05 reduced matched-baseline boundary

- The harness and ten baseline-family CPU paths are E1 implementation evidence only.
- The reduced five-seed profile matched architecture-body parameter counts within the declared
  tolerance. Only an optimizer-work proxy matched the compute tolerance; family-specific
  analytical work and CPU timing did not, so scientific compute matching is false.
- Dev quality matching failed for at least one learned family/seed.
- The profile is not the full frozen 1,000-episode-per-world evaluation and does not raise
  CL-007 above E0. No neural, general-superiority, biological, or energy claim is permitted.

## Claim change procedure

Any grade change must include:

- experiment/run identifier;
- immutable configuration and seeds;
- raw result location;
- baseline and ablation definitions;
- statistical method;
- known confounds;
- reviewer or reproduction status;
- exact wording permitted after the upgrade.
