# SparkBrain External Research & Audit — Independent Audit

Analysis time: 2026-09-18 22:32 JST
Role: `INDEPENDENT_AUDITOR`

## Phase ordering

`phase_ordering_confirmed: true`

The target and attack hypotheses below were fixed from repository evidence and prior audit history before reading Control Brain, Evidence Analyst, MAIN/SUB, or Literature summaries.

### blind_target_selection

- target: terminal PD01 `pd01-long-history-fading-memory-official-v1`, canonical result `FAIL_REDUCED_BY_FADING_MEMORY`
- exact package: `b9d38daa5faca348ad2db3898ba71e2abc99f631`
- scientific-contract blob: `0ce03b01baf41a0c77c513835b1c6063e47b2614`
- implementation blob: `16bbfb6ed57d6c9701e8437360692b62e7c36915`
- STARTED: `control/pd01-long-history-fading-memory-started-v1-20260918`
- raw preserve commit: `65ae7a50ee2279ab5edc3ca43ea3bf69daecb881`
- terminal evidence commit: `fc5c8cda283360addddb7da482b14e69beaba1f7`
- evidence tag: `evidence/pd01-long-history-fading-memory-pd01-long-history-fading-memory-official-v1`
- attacks fixed blind:
  1. package / identity / STARTED drift, target leakage, or post-START repair;
  2. whether the FAIL rule distinguishes genuine comparator reduction from absence of any registered candidate signal;
  3. resource/readout asymmetry between SparkBrain probe features and the reservoir full hidden-state readout;
  4. paired/base-world bootstrap correctness and long-lag endpoint binding;
  5. overclaim from an exact probe-level failure to a whole-system fading-memory reduction.
- why consequential: PD01 is being used to close the generic remote-history / non-fading-persistence frontier, so the difference between “no registered signal existed” and “a fading-memory comparator explained a real SparkBrain signal” materially changes the mechanistic interpretation.

`blind_target_change_reason: null`

## Repository-evidence audit

### Evidence-integrity chain: `ROBUST_SO_FAR`

The one-way chain is internally coherent. STARTED binds `pd01-long-history-fading-memory-official-v1` to exact package `b9d38daa...`, no-retry is true, and the workflow checks that only the STARTED marker differs from the exact package before execution. The target-blind preserve branch stores 2,048 model rows covering 1,024 histories with `targets_materialized: false`, and terminal scoring independently re-fetches those bytes before TEST target materialization. I found no evidence of identity reuse, outcome-responsive retuning, target-before-preserve access, or post-START scientific mutation.

The primary endpoint is prospectively fixed to lags 64 and 128, clustered by `base_world_id`, with 10,000 bootstrap resamples and fixed Type-7 quantiles. The registered terminal statistics are:

- SparkBrain candidate accuracy: `0.47265625`
- candidate 95% CI: `[0.431640625, 0.515625]`
- matched contractive reservoir accuracy: `0.5`
- effect `(SparkBrain - reservoir)`: `-0.02734375`
- effect 95% CI: `[-0.068359375, 0.015625]`

The frozen rule `effect_ci95_upper <= 0.05` therefore validly maps the exact object to `FAIL_REDUCED_BY_FADING_MEMORY` under its preregistered taxonomy.

### New audit issue: the terminal taxonomy conflates “reduction” with “no candidate signal”

The mechanistic interpretation is weaker than the terminal label suggests. SparkBrain itself is not shown to recover the remote event at the primary long lags: its accuracy is below chance at `0.4727`, and its 95% CI contains `0.5`. The comparator is exactly at `0.5`.

Therefore this run does **not** show a positive SparkBrain long-history effect that a fading-memory reservoir successfully reproduces. It shows that the registered SparkBrain probe readout does not demonstrate above-chance long-lag recoverability, while the reservoir is not more than 5 percentage points worse under the frozen contrast.

The frozen FAIL rule contains no candidate-signal floor. Consequently two scientifically different cases collapse to the same terminal class:

1. SparkBrain has a real long-lag signal and the reservoir matches it; and
2. neither system has a demonstrated long-lag signal.

The observed PD01 result is compatible with case (2). This is a **null-vs-reduction confound**, not an integrity failure and not grounds to alter the consumed canonical result.

### Secondary interpretation ceiling: readout access is not symmetric

The authority explicitly recorded `resource_asymmetry_ruling: ACCEPT_FOR_THIS_BOUNDARY_TEST_WITH_INTERPRETATION_CAP`. The candidate exposes a 64-vector made only from spikes emitted during the final symmetric probe, summing `potential_before_reset` for spiking units. The reservoir exposes its full 64-dimensional continuous state after the same probe. Equal dimensionality and the same ridge readout do not make these hidden-state observation channels equivalent.

That asymmetry is acceptable for the exact operational claim about **SparkBrain probe response**, but it prevents using PD01 as evidence that SparkBrain's complete latent/internal state is itself fading-memory-reducible.

## Phase-2 interpretation comparison

After the blind target was fixed, current control-plane summaries were read.

Control Brain currently says PD01 “terminally reduces the registered remote-history discriminator to a fading-memory comparator” and lists PD01 among the reductions narrowing the programme. Evidence Analyst likewise records `TERMINAL_FAIL_REDUCED_BY_FADING_MEMORY / AUDIT_PENDING`. Neither summary distinguishes the observed no-signal case from a positive-signal comparator reduction.

The blind audit therefore changes the **interpretation**, not the immutable outcome. A safer programme statement is:

> PD01 failed to demonstrate registered long-lag remote-history recoverability in the SparkBrain final-probe readout; the exact fixed contractive reservoir was not materially worse under the preregistered contrast. This does not demonstrate that a fading-memory reservoir mechanistically reproduces a positive SparkBrain persistence effect, nor that all SparkBrain latent state is fading-memory-reducible.

This correction does not revive a generic persistence novelty claim. On the contrary, the registered PD01 probe supplied no positive long-lag evidence to protect. It does mean PD01 should not be counted as a mechanistically specific reservoir-reduction result when building the reduction ladder.

Current MAIN has already moved to LP01 specification and reports `NO_HIGH_VALUE_OBJECT` pressure because admitted lineage metadata can be reconstructed by an ordinary explicit parent-state table under matched privilege. SUB remains no-op. Nothing in this audit authorizes reopening PD01 or changing LP01.

## Audit classification

`CONFOUNDED`

Evidence integrity and frozen terminal classification are `ROBUST_SO_FAR`; the **mechanistic reduction interpretation** is confounded by the absence of a demonstrated candidate signal and by the acknowledged probe-state/readout asymmetry.

## Knowledge-flow contract

```yaml
role: INDEPENDENT_AUDITOR
genuinely_new_information: true
affected_lines:
  - PD01
  - PERSISTENT_DYNAMICS_RESIDUAL
  - PROGRAMME_NOVELTY
  - FUTURE_REDUCTION_TAXONOMY
novelty_or_reduction_impact: >
  PD01 supplies no positive long-lag SparkBrain persistence signal to explain.
  The immutable FAIL remains valid under its frozen contract, but it should be
  interpreted as NO_REGISTERED_LONG_LAG_SIGNAL_PLUS_COMPARATOR_NOT_WORSE, not
  as evidence that a fading-memory reservoir mechanistically reproduces a
  demonstrated SparkBrain persistence effect. No novelty support is restored.
audit_classification: CONFOUNDED
blind_target_selection:
  target: pd01-long-history-fading-memory-official-v1 terminal FAIL_REDUCED_BY_FADING_MEMORY
  selected_before_control_plane_summaries: true
  attacks:
    - one-way authority / leakage / post-START drift
    - null-signal versus comparator-reduction conflation
    - candidate/comparator readout-access asymmetry
    - clustered long-lag statistic binding
    - whole-system overclaim
blind_target_change_reason: null
prospective_baselines_or_discriminators:
  - do not rerun, retune, rescore, or relabel canonical PD01
  - future reduction contracts should separate NO_REGISTERED_SIGNAL from REDUCED_BY_COMPARATOR
  - require a prospectively fixed candidate-signal floor before mechanistic reduction language is armed
  - where latent-memory claims are intended, match observation/readout privilege rather than only feature dimension
questions_for_evidence_analyst:
  - Should PD01 be summarized as no registered long-lag probe signal plus comparator-not-worse, while preserving the canonical FAIL token unchanged?
  - Should future reduction contracts require a positive candidate-signal gate before REDUCED_BY_* can be interpreted mechanistically?
  - Should the final-probe-only candidate readout be stated explicitly whenever PD01 is used in programme synthesis?
questions_for_control_brain:
  - Remove PD01 from the mechanistically specific “reservoir reduction” count and instead count it as negative evidence for the registered persistence probe?
  - Adopt a programme-wide distinction between ABSENT_SIGNAL and EXPLAINED_BY_REDUCTION?
  - Keep the testbed/reduction-first framing unchanged, since this audit restores no positive persistence evidence?
must_not_change_frozen_or_consumed:
  - pd01-long-history-fading-memory-official-v1
  - exact package b9d38daa5faca348ad2db3898ba71e2abc99f631
  - scientific-contract blob 0ce03b01baf41a0c77c513835b1c6063e47b2614
  - implementation blob 16bbfb6ed57d6c9701e8437360692b62e7c36915
  - STARTED control/pd01-long-history-fading-memory-started-v1-20260918
  - raw preserve 65ae7a50ee2279ab5edc3ca43ea3bf69daecb881
  - terminal evidence fc5c8cda283360addddb7da482b14e69beaba1f7 and annotated evidence tag
  - canonical FAIL_REDUCED_BY_FADING_MEMORY token and frozen statistics
  - all other consumed C19/R1/R2/NI01/H5/A01/RV01/RV02/CX identities and immutable evidence
```

## Handoff

**Role performed:** `INDEPENDENT_AUDITOR`.  
**Genuinely new audit information:** yes — PD01's frozen result is integrity-valid, but its mechanistic “reduced by fading memory” interpretation conflates comparator reduction with absence of a registered SparkBrain long-lag signal.  
**Top implication:** preserve the canonical FAIL unchanged, but describe PD01 as a failed persistence probe with comparator-not-worse; do not claim that a reservoir explained a demonstrated positive SparkBrain persistence effect.  
**Affected lines:** PD01, persistent-dynamics residual, programme novelty, future reduction taxonomy.
