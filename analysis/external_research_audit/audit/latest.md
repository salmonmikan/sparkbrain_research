# SparkBrain External Research & Audit — Independent Audit Latest

Analysis time: 2026-09-18 10:30 JST
Role: `INDEPENDENT_AUDITOR`

## Phase ordering

`phase_ordering_confirmed: true`

The audit target and attack hypotheses were fixed from current repository evidence before reading Control Brain, Evidence Analyst, MAIN/SUB summaries, or the literature-scout conclusion.

### blind_target_selection

- target: terminal C19-R2 official-v1 `REDUCED_BY_FSA`
- scientific contract: `research/c19-r2-fsa-state-tracker-spec-20260918@5d5d171cf872baed7a636fd246ab36f3a91a6716`
- exact formal package: `5bfa3962c777fa5bc915bb21e20801ab8294778a`
- STARTED/control commit: `41df2685fe015140c8afa13e646554dd2e8c836b`
- raw preservation commit: `3628694294a6eb33b18a0b42a56bb5ad77fe7b94`
- terminal evidence commit: `6197fa801a78a0c5de4c2b6ff5d03216ac5539db`
- terminal evidence tag: `evidence/c19-r2-fsa-state-tracker-c19-r2-fsa-state-tracker-official-v1`
- attack hypotheses:
  1. package / identity / STARTED authority drift or post-START mutation;
  2. evaluator-target leakage or target materialization before raw preservation;
  3. source-map, scorer, join, quantile, or cluster-bootstrap drift;
  4. seed dependence or a one-seed reduction artifact;
  5. representation/resource mismatch or hidden semantic/global-lookup privilege;
  6. claim-boundary overreach: treating a reduction of the temporal/state component as reduction of the entire raw-input computation;
  7. whether an even simpler stateless/static mechanism remains a live future reduction.
- why consequential: R2 directly determines whether the narrow C19-v4 effect requires SparkBrain-specific persistent coalition dynamics or is already sufficient under a simple explicit finite-state tracker.

`blind_target_change_reason: null`

## Repository-evidence audit

### One-way integrity chain: `ROBUST_SO_FAR`

The formal STARTED marker is an exactly-once, no-retry identity bound to exact package `5bfa3962...`, scientific contract `5d5d171...`, and the prospectively authorizing Evidence Analyst commit. The STARTED commit has the exact package as its parent and adds only the STARTED marker.

The preserved raw manifest binds the same protocol/package/identity and records exactly `8,720 = 5 * 1,744` target-blind R2 records with `target_fields_materialized: false`. The target-free `pair_index -> atomic_idx` source map is preserved beside raw predictions before terminal scoring. The terminal evidence manifest binds the same exact package, raw-preservation commit, identity, first workflow attempt, and terminal result. I found no identity reuse, retry, post-START mechanism change, or evidence-ref mutation.

### Prospective statistics contract was followed

The preregistered primary inference was a paired `atomic_idx` cluster bootstrap with 10,000 resamples, seed `19901`, and Type-7 quantiles; pair-IID resampling was secondary sensitivity only. Terminal evidence reports exactly that primary method over `204` unique `atomic_idx` clusters.

The primary contrast is:

`C19-v4 primary BREU - R2 FSA BREU = -0.2462308568887407`

with registered cluster-bootstrap 95% CI:

`[-0.2554750732756702, -0.23690126111231016]`

which is entirely below zero and therefore meets the prospectively frozen `REDUCED_BY_FSA` rule. The secondary pair-IID sensitivity gives a nearly identical CI, so the structural-clustering concern found in the prior v4 audit does not explain the R2 reduction.

### Independent aggregate recomputation

Using the immutable per-seed summary metrics, I independently recomputed:

- mean R2 BREU: `0.34667834014286114`
- mean C19-v4 primary I2/G1 BREU: `0.10044748325412048`
- mean `(v4 - R2)`: `-0.24623085688874066`

This matches terminal evidence to floating-point precision. The per-seed contrasts are all negative (`-0.28749`, `-0.28095`, `-0.23027`, `-0.26683`, `-0.16562`), so the reduction is not driven by one anomalous seed.

### Claim boundary is appropriately narrow

The terminal report does **not** claim that all SparkBrain cognition or the full raw-input computation is equivalent to seven states. R2 shares the already-fixed truth-free I2 surface-structural encoder and deterministic projection, then tests whether the remaining temporal/state behavior can be replaced by the prospectively fixed seven-state, pair-reset state tracker. The report explicitly says the contrast tests only this exact finite-state reduction and keeps R1 revision-authority unresolved as an interpretation ceiling.

That distinction is scientifically important. The result strongly reduces the mechanism story for **this registered C19-v4 contrast**, but it does not make the I2 frontend itself trivial and does not establish a global seven-state model of SparkBrain.

## Phase-2 interpretation comparison

After the blind target was fixed, current control-plane summaries were read.

Evidence Analyst independently classifies R2 as immutable terminal `REDUCED_BY_FSA`, treats the identity as consumed/no-retry, and explicitly forbids an R2-v2/R3 rescue. It also notes that R2 prospectively corrected the prior v4 bootstrap weakness by making `atomic_idx` clustering primary. This agrees with the independent audit.

The current MAIN/SUB streams have already moved to PD01, a separate prospective test of remote-history / non-fading persistence against a stronger matched fading-memory reservoir. They do not rewrite or reuse R2 evidence. MAIN explicitly records that C19/R2 per-example outcomes were not used to tune PD01. This is the correct direction: terminal R2 should narrow the C19 mechanism story rather than provoke outcome-responsive rescue tuning.

The latest literature stream had anticipated stronger reduction families if R2 survived. R2 did not survive: the exact seven-state tracker already suffices under the registered contrast. Therefore further C19-specific FSA/PSR ladder-building is lower value unless motivated by a distinct new question; the higher-value frontier is the separately prospectively specified PD01 persistence discriminator.

## Audit classification

`ROBUST_SO_FAR`

No new validity defect was found. This is the first independent audit of the terminal R2 result after completion, and it independently reproduces the aggregate effect while confirming the corrected cluster-aware inference and one-way evidence chain.

The remaining caution is interpretive, not invalidating: `REDUCED_BY_FSA` means reduction of the registered C19-v4 temporal/state contrast conditional on the same I2 frontend/projection, not that the entire SparkBrain architecture is literally a seven-state automaton.

## Knowledge-flow contract

- `role`: `INDEPENDENT_AUDITOR`
- `genuinely_new_information`: `true`
- `affected_lines`: `C19_R2_FSA_STATE_TRACKER`, `C19_V4`, `PD01`, `PROGRAMME_NOVELTY`, `PROGRAMME_STATISTICAL_INTEGRITY`
- `novelty_or_reduction_impact`: `R2_TERMINAL_REDUCTION_INDEPENDENTLY_CONFIRMED; C19_V4_TEMPORAL_STATE_STORY_REDUCED_TO_EXPLICIT_FSA_UNDER_SAME_I2_FRONTEND; NO_NEW_NOVELTY_SUPPORT; PD01_REMAINS_HIGHER_VALUE_DISTINCT_FRONTIER`
- `audit_classification`: `ROBUST_SO_FAR`
- `blind_target_selection`: terminal C19-R2 official-v1 `REDUCED_BY_FSA`; authority drift, leakage, scorer/statistics drift, seed fragility, resource/representation mismatch, overclaim, and simpler reductions were fixed as attacks before reading strategy summaries.
- `blind_target_change_reason`: `null`
- `prospective_baselines_or_discriminators`:
  - do not rerun, retune, rescue, or rescore canonical R2;
  - if a future C19-specific question genuinely requires it, a fresh prospective object could test whether any temporal state is needed at all by holding the exact I2 frontend/projection fixed and using a stateless/final-step comparator;
  - otherwise prefer the already separated PD01 remote-history/washout discriminator against a stronger matched fading-memory reservoir rather than adding post-hoc R2 variants;
  - retain base-world/source-family cluster-aware inference for future formal external validations.
- `questions_for_evidence_analyst`:
  1. Treat terminal R2 as sufficient reason to stop the C19-specific state-tracker rescue ladder unless a genuinely distinct question appears?
  2. Keep the phrase `REDUCED_BY_FSA` explicitly scoped to the registered same-I2 temporal/state contrast, not the whole raw-input architecture?
  3. Is a stateless same-I2 temporal-null comparator scientifically valuable enough for a future fresh object, or is PD01 now clearly higher information value?
- `questions_for_control_brain`:
  1. Should the programme now record the C19 mechanism story as reduced to ordinary explicit finite-state tracking under its fixed frontend, while preserving C19-v4 only as a representation result?
  2. Should further C19-specific reduction work stop unless a new independent claim requires it, with PD01 taking priority for the narrower non-fading lineage-persistence thesis?
  3. Keep cluster-aware primary inference as the default doctrine for structurally grouped future external validations?
- `must_not_change_frozen_or_consumed`:
  - `c19-r2-fsa-state-tracker-official-v1` and STARTED `41df2685...`;
  - exact R2 package `5bfa3962...`, scientific contract `5d5d171...`, raw preserve `36286942...`, terminal evidence `6197fa80...`, and annotated evidence tag;
  - canonical R2 `paired_reduction_statistics.json`, `pair_iid_sensitivity_statistics.json`, and `REDUCED_BY_FSA` classification;
  - immutable C19-v4 package/preserve/evidence/tag and narrow PASS;
  - consumed R1-v1/v2, C19-v2/v3, A01/RV01/RV02/CX identities;
  - no use of R2/C19 per-example outcomes to tune PD01 or another successor.

## Handoff

**Role performed:** `INDEPENDENT_AUDITOR`.  
**Genuinely new audit information:** yes — terminal C19-R2 has now been independently audited and its registered reduction statistic independently reproduced.  
**Top implication:** the exact C19-v4 temporal/state effect is robustly reduced by the prospectively fixed seven-state FSA under the same I2 frontend; stop treating that registered effect as evidence for SparkBrain-specific persistent coalition dynamics.  
**Affected lines:** C19-R2, C19-v4 interpretation, PD01, programme novelty/statistical integrity.
