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
| CL-003 | A losing belief can retain state and later recover after new evidence. | E2 | controlled ablation with confidence intervals and held-out worlds |
| CL-004 | No-ignition can be represented as a low-level computational state. | E1 | learned system evaluation and calibration |
| CL-005 | Event routing can avoid touching every dormant Spark in the reference algorithm. | E1 | audited counters and scale study |
| CL-006 | Residual retention improves belief revision in the current hand-authored SwitchWorld distribution. | E2 | preregistered held-out distributions and matched statistical tests |
| CL-007 | SparkBrain improves the stability/adaptability frontier over strong neural baselines. | E0 | C04–C06 |
| CL-008 | Learned Spark groups form stable functional organs. | E0 | C08 causal specialization tests |
| CL-009 | A spiking substrate preserves core SparkBrain behavior. | E0 | C07 equivalence suite |
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
