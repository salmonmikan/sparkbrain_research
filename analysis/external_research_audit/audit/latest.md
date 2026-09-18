# SparkBrain External Research & Audit — Independent Audit Latest

Analysis time: 2026-09-18 22:32 JST
Role: `INDEPENDENT_AUDITOR`

## Phase ordering

`phase_ordering_confirmed: true`

The target and attack hypotheses were fixed from repository evidence and prior audit history before reading Control Brain, Evidence Analyst, MAIN/SUB, or Literature summaries.

### blind_target_selection

- target: terminal PD01 `pd01-long-history-fading-memory-official-v1`, canonical result `FAIL_REDUCED_BY_FADING_MEMORY`
- exact package: `b9d38daa5faca348ad2db3898ba71e2abc99f631`
- scientific-contract blob: `0ce03b01baf41a0c77c513835b1c6063e47b2614`
- implementation blob: `16bbfb6ed57d6c9701e8437360692b62e7c36915`
- STARTED: `control/pd01-long-history-fading-memory-started-v1-20260918`
- raw preserve commit: `65ae7a50ee2279ab5edc3ca43ea3bf69daecb881`
- terminal evidence commit: `fc5c8cda283360addddb7da482b14e69beaba1f7`
- evidence tag: `evidence/pd01-long-history-fading-memory-pd01-long-history-fading-memory-official-v1`
- attacks fixed blind: one-way authority/leakage drift; null-signal versus comparator-reduction conflation; readout-access asymmetry; clustered long-lag statistic binding; whole-system overclaim.
- why consequential: PD01 is used to close the generic remote-history / non-fading-persistence frontier, so “no registered signal” and “fading-memory comparator explains a real signal” must not be conflated.

`blind_target_change_reason: null`

## Repository-evidence audit

### Evidence integrity: `ROBUST_SO_FAR`

STARTED binds the fresh no-retry identity to exact package `b9d38daa...`. The workflow verifies the STARTED-only delta before TEST access. The target-blind preserve stores 2,048 prediction rows over 1,024 histories with `targets_materialized: false`, independently re-fetches preserved bytes, and only then materializes TEST targets. No identity reuse, target-before-preserve access, post-START scientific mutation, or outcome-responsive retuning was found.

The preregistered primary endpoint is lags 64/128, clustered by `base_world_id`, 10,000 bootstrap resamples, fixed seed and Type-7 quantiles. Terminal statistics are:

- SparkBrain accuracy `0.47265625`, 95% CI `[0.431640625, 0.515625]`
- fixed contractive reservoir accuracy `0.5`
- effect `(SparkBrain - reservoir)` `-0.02734375`, 95% CI `[-0.068359375, 0.015625]`

The frozen rule `effect_ci95_upper <= 0.05` therefore validly maps the exact consumed object to `FAIL_REDUCED_BY_FADING_MEMORY` under its preregistered taxonomy.

### New issue: `NO_SIGNAL` and `REDUCED_BY_COMPARATOR` are collapsed

SparkBrain itself does not demonstrate recoverable long-lag history under the registered probe: its accuracy is below chance and its 95% CI contains `0.5`. The reservoir is also at `0.5`. Thus PD01 does not show a positive SparkBrain persistence effect that a fading-memory reservoir reproduces. It shows a **failed registered persistence probe**, with the reservoir not materially worse under the frozen contrast.

The FAIL rule has no prospectively required candidate-signal floor. It therefore assigns the same `FAIL_REDUCED_BY_FADING_MEMORY` token to two different scientific situations: a real candidate signal matched by the comparator, or no demonstrated signal in either model. The observed result is compatible with the latter. This is a **null-vs-reduction confound**, not an evidence-integrity failure.

### Secondary ceiling: readout access is acknowledged but asymmetric

Execution authority explicitly records `resource_asymmetry_ruling: ACCEPT_FOR_THIS_BOUNDARY_TEST_WITH_INTERPRETATION_CAP`. SparkBrain exposes a 64-vector formed only from spikes emitted during the final symmetric probe, while the reservoir exposes its full continuous 64-dimensional post-probe state. Equal dimensionality and identical ridge fitting do not make latent-state observation privilege equivalent.

That is acceptable for the exact operational claim about **SparkBrain probe response**, but it blocks a stronger inference that SparkBrain's full latent state is fading-memory-reducible.

## Phase-2 comparison

After target selection was fixed, current summaries were read. Control Brain says PD01 “terminally reduces the registered remote-history discriminator to a fading-memory comparator”; Evidence Analyst records `TERMINAL_FAIL_REDUCED_BY_FADING_MEMORY / AUDIT_PENDING`. Neither currently distinguishes no registered candidate signal from positive-signal comparator reduction.

A safer programme statement is:

> PD01 failed to demonstrate registered long-lag remote-history recoverability in the SparkBrain final-probe readout; the exact fixed contractive reservoir was not materially worse under the preregistered contrast. This does not show that a fading-memory reservoir mechanistically reproduces a demonstrated positive SparkBrain persistence effect, nor that all SparkBrain latent state is fading-memory-reducible.

This does **not** restore generic persistence novelty. There is no positive PD01 long-lag signal to protect. MAIN has already moved to LP01 prospective specification; SUB remains no-op. Nothing here authorizes reopening PD01 or changing consumed evidence.

## Audit classification

`CONFOUNDED`

Evidence integrity and the frozen terminal token remain `ROBUST_SO_FAR`; the **mechanistic reduction interpretation** is confounded by absent demonstrated candidate signal and the prospectively acknowledged observation/readout asymmetry.

## Knowledge-flow contract

- `role`: `INDEPENDENT_AUDITOR`
- `genuinely_new_information`: `true`
- `affected_lines`: `PD01`, `PERSISTENT_DYNAMICS_RESIDUAL`, `PROGRAMME_NOVELTY`, `FUTURE_REDUCTION_TAXONOMY`
- `novelty_or_reduction_impact`: `PD01_NO_POSITIVE_LONG_LAG_SIGNAL; CANONICAL_FAIL_VALID_BUT_MECHANISTIC_RESERVOIR_REDUCTION_NOT_ESTABLISHED; NO_NOVELTY_SUPPORT_RESTORED`
- `audit_classification`: `CONFOUNDED`
- `blind_target_selection`: PD01 official-v1 terminal FAIL, selected before control-plane summaries; attacks were integrity/leakage, null-vs-reduction conflation, readout asymmetry, statistics binding and overclaim.
- `blind_target_change_reason`: `null`
- `prospective_baselines_or_discriminators`:
  - never rerun, retune, rescore or relabel canonical PD01;
  - future reduction contracts should distinguish `NO_REGISTERED_SIGNAL` from `REDUCED_BY_COMPARATOR`;
  - require a prospectively fixed positive candidate-signal gate before mechanistic `REDUCED_BY_*` language is armed;
  - for latent-memory claims, match observation/readout privilege rather than only feature dimension.
- `questions_for_evidence_analyst`:
  1. Preserve the canonical FAIL token but summarize PD01 as no registered long-lag probe signal plus comparator-not-worse?
  2. Require a positive candidate-signal gate in future mechanistic reduction contracts?
  3. State final-probe-only candidate observation explicitly whenever PD01 is synthesized?
- `questions_for_control_brain`:
  1. Count PD01 as negative evidence for the registered persistence probe rather than a mechanistically specific reservoir reduction?
  2. Adopt programme-wide `ABSENT_SIGNAL` versus `EXPLAINED_BY_REDUCTION` semantics?
  3. Keep testbed/reduction-first framing unchanged because no positive persistence evidence is restored?
- `must_not_change_frozen_or_consumed`:
  - `pd01-long-history-fading-memory-official-v1`;
  - exact package `b9d38daa5faca348ad2db3898ba71e2abc99f631`;
  - scientific-contract blob `0ce03b01baf41a0c77c513835b1c6063e47b2614`;
  - implementation blob `16bbfb6ed57d6c9701e8437360692b62e7c36915`;
  - STARTED `control/pd01-long-history-fading-memory-started-v1-20260918`;
  - raw preserve `65ae7a50ee2279ab5edc3ca43ea3bf69daecb881`;
  - terminal evidence `fc5c8cda283360addddb7da482b14e69beaba1f7`, evidence tag, canonical statistics and `FAIL_REDUCED_BY_FADING_MEMORY`;
  - all other consumed C19/R1/R2/NI01/H5/A01/RV01/RV02/CX identities and immutable evidence.

## Handoff

**Role performed:** `INDEPENDENT_AUDITOR`.  
**Genuinely new audit information:** yes — PD01's frozen result is integrity-valid, but its mechanistic reduction interpretation conflates comparator reduction with absence of a registered SparkBrain long-lag signal.  
**Top implication:** preserve canonical FAIL unchanged, but describe PD01 as a failed persistence probe with comparator-not-worse; do not claim a reservoir explained a demonstrated positive SparkBrain persistence effect.  
**Affected lines:** PD01, persistent-dynamics residual, programme novelty, future reduction taxonomy.
