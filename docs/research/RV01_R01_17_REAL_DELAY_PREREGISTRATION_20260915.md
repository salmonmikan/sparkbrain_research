# RV01 R01-17 real-delay development preregistration — 2026-09-15

## Status and scientific boundary

This document prospectively defines a **new exposed-development identity** after the consumed R01-16 result and its post-hoc measurement-validity audit. It is not a repair, rerun, rescore, or continuation of the consumed R01-16 identity, and it has no held-out or formal authority.

R01-17 asks one narrow mechanistic question:

> When the ordinary physical Field learner is given a deliberately nonzero delay-learning error while learned weights are held identical at expression time, does the learned physical delay causally shift downstream propagation timing by a preregistered, non-roundoff amount while preserving the same route?

A positive result supports only this controlled development capability. It does not establish interference retention, generality, a held-out result, biological fidelity, or a formal SparkBrain claim.

## Why this successor is distinct

R01-16 initialized every physical connection delay from the same `world.lag_ms` used as the external training-pulse spacing. The learner moves causal connection delay toward that observed lag, so R01-16 supplied essentially zero intentional delay error. Its exact-float delay-change eligibility admitted roundoff-scale movement. R01-17 changes the prospective input contract rather than retuning R01-16 after its outcome.

The R01-16 frozen labels remain immutable historical outputs:

- Weight: `WEIGHT_SUPPORTED` (100/100 support cells)
- Delay: `DELAY_MIXED` (0 support / 54 negative / 46 discordant)
- Combined: `COMBINED_SUPPORTED` (100/100 support cells)

R01-17 does not rescore those cells.

## Fixed identity

- Protocol: `rv01-r01-17-real-delay-causal-timing-v1`
- Phase: exposed development only
- Families: one fixed four-unit directed chain per prospective parameter cell
- Unit IDs: `0 -> 1 -> 2 -> 3`
- Development seeds: `141800, 141801, 141802, 141803, 141804`
- Seed freshness audit before preregistration: all five literals were absent from the repository search surface before this branch introduced them.
- World salt: `rv01-r01-17-real-delay-world-grid-v1`
- Held-out authority: false
- Formal authority: false

The five seeds are not five stochastic repetitions of one identical world. Each seed deterministically fixes a distinct prospective training lag, initial-delay offset, threshold, and cue magnitude before any R01-17 output is opened.

## Fixed construction

For each seed, deterministic parameters are generated from the seed only:

- training lag is in `[3.8, 4.2] ms`;
- initial physical delay exceeds the training lag by `[1.5, 2.25] ms`;
- all three chain edges begin at weight `0.05`;
- threshold is in `[0.45, 0.53]`;
- cue magnitude is `threshold + 0.65`;
- six training exposures are used;
- the existing RV01 external-only physical learner and its default frozen configuration are used unchanged.

The learner receives four external pulses per exposure at exactly the fixed training lag. Endogenous activity never writes the connection state.

## Fixed factor arms

After training, all arms start from the same post-training checkpoint and preserve the same topology and learned weights.

- `F0`: post-training weights + post-training delays.
- `FD`: post-training weights + **pre-training delays**.
- `SHAM`: exact copy of `F0` used to verify deterministic replay/no intervention effect.

No weight-reset arm is part of the R01-17 primary question. This is deliberate: R01-17 first establishes whether a scientifically nontrivial learned-delay state exists and has a causal timing expression while weight is held matched. A later distinct successor may return to interference interactions if this capability is supported.

## Raw acquisition contract

The exactly-once acquisition stores, without applying the decision rule:

- exact source Git SHA and source manifest;
- Python runtime identity;
- fixed world/spec identity for each seed;
- learner API hash;
- every training exposure's deterministic input pulses, learner observation results, before/after connection hashes, and post-exposure connection inventory;
- complete pre-training and post-training connection inventories;
- `F0`, `FD`, and `SHAM` downstream generated unit sequences;
- exact generated spike times in milliseconds for every arm;
- checkpoint/connection hashes needed to prove that probing did not mutate connection state.

CI, unit tests, and preflight must not call the real fixed-seed acquisition function. Synthetic tests may exercise pure validation helpers only.

Raw evidence must be pushed to its immutable preservation ref **before** the scorer is invoked. If acquisition fails after STARTED, that terminal failure consumes the identity and must be preserved rather than retried.

## Frozen eligibility and scoring

Constants fixed before output:

- minimum meaningful learned-delay displacement per chain edge: `0.5 ms`;
- minimum causal first-arrival shift per downstream unit: `0.5 ms`;
- numerical/tie tolerance: `0.05 ms`;
- required downstream route: exactly `(1, 2, 3)` in both `F0` and `FD`;
- all five prospective cells are required for a supported aggregate classification.

For one seed, `REAL_DELAY_SUPPORT_CELL` requires all of the following:

1. every chain edge has `abs(post_delay - pre_delay) >= 0.5 ms`;
2. `F0` and `FD` retain exactly the downstream unit sequence `(1, 2, 3)`;
3. `SHAM` is byte-equivalent at the measured sequence/time endpoint to `F0`;
4. every downstream unit is observed in both `F0` and `FD`;
5. resetting delay from learned/post to pre-training makes every downstream first-arrival at least `0.5 ms` later (`FD_time - F0_time >= 0.5 ms`);
6. matched `F0` and `FD` connection weights are exactly equal for every edge.

A cell is `REAL_DELAY_NEGATIVE_CELL` if the construction is scientifically eligible (condition 1) but one or more causal timing/route conditions fail. A cell is `REAL_DELAY_INELIGIBLE` if the required nontrivial delay displacement is not created; ineligible cells are not silently converted to negatives.

Aggregate classification:

- all five cells support -> `SUPPORTED_REAL_DELAY_CAUSAL_TIMING`;
- five eligible cells and zero support -> `UNSUPPORTED_REAL_DELAY_CAUSAL_TIMING`;
- any other completed mixture -> `MIXED_REAL_DELAY_CAUSAL_TIMING`;
- any ineligible cell -> `INSUFFICIENT_REAL_DELAY_CONSTRUCTION`.

No threshold, seed, parameter range, denominator, or endpoint may be changed after raw acquisition begins.

## Exactly-once and preservation boundary

Execution is permitted only after all of the following are true:

1. the source containing this preregistration, runner, scorer, tests, and exactly-once workflow has a reviewed exact SHA;
2. CI for that exact SHA is green;
3. the source is anchored by a new non-moving `freeze/*` ref;
4. both raw and scored preserve refs are absent;
5. the exact STARTED/control ref does not already exist;
6. the control ref is atomically created at the exact frozen source SHA and is the only legitimate workflow trigger;
7. the workflow refuses `GITHUB_RUN_ATTEMPT != 1` and refuses pre-existing preserve refs;
8. raw acquisition is completed and immutably preserved before score execution.

Independent-human-only review is waived by the user's standing authorization; if that is the only remaining review gate, record `USER_AUTHORIZED_REVIEW_GATE_OVERRIDE / HUMAN_REVIEW_WAIVED_BY_USER`. This waiver does not bypass any scientific or integrity blocker.

## STOP conditions

Do not execute if any of these is true:

- a development seed or world identity collides with retained consumed/reserved history;
- initial physical delay equals or is only roundoff-different from training lag;
- delay eligibility uses exact floating-point inequality instead of the fixed `0.5 ms` displacement threshold;
- a sub-`0.5 ms` or tie-only shift can satisfy the primary endpoint;
- tests or CI execute the real five fixed candidate cells before STARTED;
- source, scorer, workflow, or thresholds move after review/freeze;
- another worker already created the same STARTED identity or either preserve ref;
- raw evidence cannot be preserved before scoring.

## Next scientific step after R01-17

If supported, the next **distinct** development experiment may reintroduce shared-cue/shared-prefix/reversal/dense-route competition to test whether a real learned-delay signal changes route competition independently of or jointly with weight. If unsupported or construction-ineligible, preserve that result and diagnose the physical delay mechanism without rerunning or retuning this R01-17 identity.
