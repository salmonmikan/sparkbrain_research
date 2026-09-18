# Independent Audit — 2026-09-18 10:30 JST

Role: `INDEPENDENT_AUDITOR`

## Phase 1 — blind target selection

Before reading Control Brain, Evidence Analyst, MAIN/SUB reports, or literature conclusions, repository evidence selected terminal C19-R2 official-v1 `REDUCED_BY_FSA` as the audit target.

Authoritative refs inspected:

- scientific contract `research/c19-r2-fsa-state-tracker-spec-20260918@5d5d171cf872baed7a636fd246ab36f3a91a6716`;
- exact formal package `5bfa3962c777fa5bc915bb21e20801ab8294778a`;
- STARTED/control commit `41df2685fe015140c8afa13e646554dd2e8c836b`;
- raw preservation `3628694294a6eb33b18a0b42a56bb5ad77fe7b94`;
- terminal evidence `6197fa801a78a0c5de4c2b6ff5d03216ac5539db`;
- annotated evidence tag `evidence/c19-r2-fsa-state-tracker-c19-r2-fsa-state-tracker-official-v1`;
- immutable C19-v4 parent package `74bfe6b4a39758656f291baaa3f16236e3e71964`.

Attack hypotheses were fixed as authority drift, target leakage, source-map/scorer/statistics drift, seed fragility, representation/resource mismatch, overclaim beyond the registered same-I2 temporal/state contrast, and the possibility of a simpler stateless reduction.

`blind_target_change_reason: null`

## Phase 1 result

No integrity violation was found. STARTED is exact-package-bound and no-retry. The preserved raw manifest contains exactly 8,720 target-blind records and states that target fields were not materialized. A target-free pair-to-`atomic_idx` map is preserved before scoring. Terminal evidence binds the same identity/package/preserve and first workflow attempt.

The prospectively fixed primary statistic is the paired `atomic_idx` cluster bootstrap, 204 unique clusters, 10,000 resamples, seed 19901. Terminal result:

- observed effect `C19-v4 primary BREU - R2 BREU = -0.2462308568887407`;
- 95% CI `[-0.2554750732756702, -0.23690126111231016]`;
- classification `REDUCED_BY_FSA`.

The pair-IID sensitivity interval is nearly identical, so the structural-clustering issue previously identified for C19-v4 does not explain the R2 result.

Independent recomputation from immutable per-seed summaries produced mean R2 BREU `0.34667834014286114`, mean C19-v4 primary BREU `0.10044748325412048`, and mean contrast `-0.24623085688874066`, matching terminal evidence to floating-point precision. All five seed-level contrasts are negative.

The result's claim boundary is also correctly limited: R2 tests whether the C19-v4 temporal/state behavior, conditional on the same fixed I2 surface-structural frontend and deterministic projection, can be replaced by one exact seven-state pair-reset tracker. It does not claim that the full SparkBrain raw-input computation is itself seven-state.

## Phase 2 — interpretation comparison

Control Brain, Evidence Analyst, MAIN/SUB report streams, and the newest literature handoff were read only after the target and attacks above were fixed.

Evidence Analyst already treats R2 as immutable terminal `REDUCED_BY_FSA`, consumed/no-retry, forbids R2-v2/R3 rescue, and recognizes that `atomic_idx` clustering corrects the prior v4 statistical weakness. This matches the blind audit.

MAIN/SUB have moved to PD01 rather than rewriting R2. PD01 is a distinct prospective remote-history/non-fading test against a stronger matched fading-memory reservoir, and current reports explicitly say R2/C19 per-example outcomes were not used for PD01 tuning. That downstream interpretation is conservative and scientifically appropriate.

The latest literature handoff had identified stronger reduction classes if R2 survived. Since R2 instead reduced the registered effect already, additional C19-specific post-hoc FSA/PSR ladder work is lower value unless a genuinely distinct new question motivates it.

## Classification

`ROBUST_SO_FAR`

This is genuinely new audit information because it is the first independent read-only verification of the terminal R2 result after completion, including an independent aggregate recomputation. No invalidity or new confound was found.

Interpretive ceiling: `REDUCED_BY_FSA` should remain scoped to the registered same-I2 temporal/state contrast. The I2 frontend/projection remains part of the fixed observable transformation and is not itself proven reducible to seven states by this result.

## Machine-usable handoff

```yaml
role: INDEPENDENT_AUDITOR
genuinely_new_information: true
affected_lines:
  - C19_R2_FSA_STATE_TRACKER
  - C19_V4
  - PD01
  - PROGRAMME_NOVELTY
  - PROGRAMME_STATISTICAL_INTEGRITY
novelty_or_reduction_impact: >
  R2_TERMINAL_REDUCTION_INDEPENDENTLY_CONFIRMED;
  C19_V4_TEMPORAL_STATE_STORY_REDUCED_TO_EXPLICIT_FSA_UNDER_SAME_I2_FRONTEND;
  NO_NEW_NOVELTY_SUPPORT;
  PD01_REMAINS_HIGHER_VALUE_DISTINCT_FRONTIER
audit_classification: ROBUST_SO_FAR
blind_target_selection:
  target: C19-R2 official-v1 terminal REDUCED_BY_FSA
  selected_before_control_plane_summaries: true
  attack_hypotheses:
    - authority/post-START drift
    - target leakage
    - source-map/scorer/statistics drift
    - seed fragility
    - resource/representation mismatch
    - claim-boundary overreach
    - simpler stateless reduction
blind_target_change_reason: null
prospective_baselines_or_discriminators:
  - do not rerun, retune, rescue or rescore canonical R2
  - only if independently justified, a fresh same-I2 stateless/final-step temporal-null could test whether any temporal state is needed
  - otherwise prioritize PD01 remote-history/washout versus matched fading-memory reservoir
  - retain source-family/base-world cluster-aware primary inference in future external validations
questions_for_evidence_analyst:
  - Should terminal R2 close the C19-specific state-tracker rescue ladder absent a distinct new question?
  - Keep REDUCED_BY_FSA explicitly scoped to the same-I2 temporal/state contrast?
  - Is a stateless same-I2 null worth a fresh object, or is PD01 clearly higher information value?
questions_for_control_brain:
  - Record C19's registered temporal-state story as reduced to ordinary explicit finite-state tracking under the fixed frontend?
  - Stop further C19-specific reduction work unless a distinct claim requires it and prioritize PD01?
  - Keep cluster-aware inference as default doctrine for structurally grouped formal validations?
must_not_change_frozen_or_consumed:
  - c19-r2-fsa-state-tracker-official-v1 and STARTED 41df2685...
  - exact package 5bfa3962... and scientific contract 5d5d171...
  - raw preserve 36286942... and terminal evidence 6197fa80... plus annotated evidence tag
  - canonical R2 statistics and REDUCED_BY_FSA classification
  - immutable C19-v4 package/preserve/evidence/tag and narrow PASS
  - consumed R1-v1/v2, C19-v2/v3, A01/RV01/RV02/CX identities
  - no R2/C19 per-example outcomes used to tune PD01 or another successor
```
