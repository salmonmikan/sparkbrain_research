# RV02-RD003 online hidden-eligibility preregistration

Date: 2026-09-11  
Status: **PREREGISTERED_DEVELOPMENT_ONLY / IMPLEMENTATION_NOT_STARTED**

This is a prospective development protocol written before RD003 implementation or execution. It does not modify or rerun RD001/RD002 evidence, does not create held-out/formal evidence, and does not authorize a parameter sweep.

## Motivation fixed from RD002

RD002 established a narrow bottleneck result under exposed development worlds:

- gain 4 recruited hidden spikes in 35/78 natural probes and produced 83 hidden spikes;
- cutting the hidden boundary reversed visible final-state differences in 33 probes;
- no visible spike sequence or task score changed at gain 2 or gain 4;
- hidden external learning eligibility remained absent under the unchanged learner.

Therefore RD003 does **not** ask whether still more boundary gain produces still more activity. It asks whether hidden activity can participate in a locally organized learning process without giving endogenous activity permission to confirm itself.

## Hypothesis

A hidden pathway may become behaviorally useful only if the Field is dynamically engaged during training and hidden activity can leave a transient local eligibility trace that is committed only by a later independent external observation.

The causal claim under test is deliberately narrow:

> externally gated hidden-return eligibility can organize already-recruitable hidden activity into useful continuation more effectively than equal training without hidden eligibility or with lineage-shuffled hidden eligibility.

This is not a claim of general intelligence, representation learning, reward learning, or Field superiority.

## Fixed inherited world and learner boundary

RD003 reuses the already exposed RV02 development worlds, route/exposure schedules, scale multipliers, resource guards and scoring conventions. These worlds remain development-only.

The ordinary local plasticity constants are inherited byte-for-byte from `DirectFieldPlasticityConfig` and are not tuned in RD003:

- eligible lag: 0.5..6.5 ms;
- potentiation tau: 10 ms;
- depression tau: 10 ms;
- potentiation rate: 0.50;
- depression rate: 0.15;
- delay learning rate: 0.50;
- weight bounds: 0..1.25;
- delay bounds: 0.5..20 ms;
- maximum modulation: 2.0;
- maximum 256 updates per external observation.

No reward, correct-action flag, route label, outcome class, task score, semantic type or success signal may enter the learner.

## Fixed recruitment condition

All RD003 arms use the same predeclared visible-to-hidden boundary multiplier **4.0 during online training and probing**.

This value is selected once from the already completed RD002 diagnosis because gain 2 produced zero hidden spikes whereas gain 4 produced measurable hidden recruitment and visible-state causality. RD003 must not increase the gain if training recruitment is weak. If gain 4 yields no qualifying hidden training activity, RD003 records that negative result and stops.

## Online-training requirement

Unlike RD002's external-only training loop, RD003 must actually advance the `TemporalExcitableField` through each training episode so endogenous Field events can occur between successive externally originated route observations.

Every external route event must remain the authoritative observation clock. Runtime-generated hidden spikes may create only short-lived local eligibility state; they are not independent teaching events.

A hidden trace must contain only anonymous/local information sufficient for audit, such as hidden unit id, event time, magnitude/current provenance and causal runtime lineage. It must expire under a fixed lag bound and must not persist as a learned source-target table.

## Three training arms

The exact same world, route order, exposures, boundary gain and ordinary external observations are used in all arms.

### E0 — online dynamics, hidden eligibility disabled

The Field is advanced online during training, but hidden runtime events cannot create eligibility used by the learner. This controls for the effect of merely running the Field during training.

### E1 — causal hidden-return eligibility

A hidden endogenous spike may create a transient unit-local eligibility trace. That trace may influence an ordinary physical connection update **only when a later externally originated visible observation arrives inside the inherited eligible-lag window**.

The allowed new update locus is hidden-to-visible return edges whose hidden source has a live runtime trace and whose visible target is the later external observation. The external observation remains the gate that commits the update.

RD003 must not potentiate a visible-to-hidden edge merely because the hidden target fired; such self-confirming incoming reinforcement is outside this protocol.

### ES — lineage-shuffled eligibility control

This arm must preserve the count, timestamps, magnitudes, expiry policy and update budget of E1 eligibility events while deterministically permuting which hidden unit identity receives each eligibility trace using a fixed source-bound permutation declared before execution.

The shuffled arm is intended to preserve activity/eligibility amount while destroying the actual local causal assignment. It must not use task outcomes to choose the permutation.

## Probe controls

After training, each arm is probed using the existing RV02 continuation scoring and the same 40-ms bounded horizon.

For every natural probe, a paired hidden-boundary-zero probe is required. Probe learning is forbidden. Observer/reference equivalence and native event/spike guards remain mandatory.

## Required retained evidence

Each training episode must retain enough raw information to reconstruct independently:

- external observations and their route-independent anonymous identities;
- all hidden runtime spikes considered for eligibility;
- eligibility creation, expiry and shuffled assignment records;
- every physical connection update with before/after weight and delay;
- whether the committing event was externally originated;
- connection hashes before and after training;
- update counts partitioned by visible-visible, visible-hidden, hidden-visible and hidden-hidden loci;
- no task score or outcome field in learner input;
- probe spike traces, visible final states, hidden activity and boundary-cut pairs.

An independent verifier must reconstruct all reported task metrics from raw spikes and verify that ES preserves the declared eligibility-event budget relative to E1.

## Fail-closed feasibility gates

A cell is incomplete and cannot contribute scientific metrics if any of the following occurs:

- native event/spike/resource limit is reached;
- an endogenous event directly commits plasticity without a later external gate;
- a hidden eligibility trace survives beyond its fixed lifetime;
- E1 and ES do not have matched eligibility-event counts/timing/magnitude budgets;
- probe changes connection state;
- retained raw data cannot reconstruct the update locus and score.

If E1 produces zero hidden eligibility events across the complete matrix, RD003 ends as a negative recruitment/online-training result. No gain or threshold change is permitted under the RD003 identity.

## Scientific readout

The primary diagnostic is **selective organization, not activity amount**.

A useful RD003 signal requires all of the following in at least one preregistered family/scale cell while preserving complete-cell integrity:

1. E1 improves strict exact-route recovery or reduces off-route contamination relative to both E0 and ES without reducing ordered retention;
2. the improving probe contains retained hidden eligibility activity;
3. the paired hidden-boundary cut removes or reverses the relevant visible behavioral improvement;
4. ES fails to reproduce the same improvement despite matched eligibility-event budget.

If E1 and ES behave equivalently, the causal-assignment hypothesis is not supported even if both outperform E0. If E1 merely increases hidden spikes or changes subthreshold visible state without behavioral improvement, RD003 is negative for useful selective organization.

No aggregate average may compensate for a required per-probe regression. Shared-cue/shared-prefix ambiguity remains interpreted under the existing RV02 scoring convention.

## Prohibited RD003 adaptations

After the first RD003 execution begins, do not under the same identity:

- change boundary gain, threshold, time constants or plasticity rates;
- add reward/correct-action/task-score feedback;
- change the shuffled-control construction after seeing outcomes;
- add route-specific or family-specific exceptions;
- extend the probe horizon to rescue a result;
- redefine exact-route, retention or contamination scoring.

Any such change requires a new diagnostic identity.

## Next implementation step

Implement the smallest online-training adapter and trace/audit schema needed to realize E0/E1/ES while keeping the existing Field, ordinary connection state and inherited plasticity constants intact. Add unit tests that prove endogenous events cannot commit updates by themselves and that E1/ES eligibility budgets match before any development matrix is run.
