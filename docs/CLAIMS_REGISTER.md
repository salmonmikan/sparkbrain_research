# Claims Register

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
| CL-010 | Neuromorphic execution is more energy efficient. | E0 | hardware measurement, matched workloads, power methodology |

## Prohibited public claims at v0.2

- “The human brain has been reproduced.”
- “The system is conscious.”
- “This is AGI.”
- “The theory is completely novel.”
- “SparkBrain is better than Transformers.”
- “Sparse activity proves lower energy use.”
- “Organs emerged autonomously.”

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
