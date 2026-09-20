# SparkBrain External Research & Audit — Independent Audit Latest

- schema_version: `2`
- generation_id: `AUD-20260920T223110+0900-R3-C19V4-REDUCTION-6B4E21D9`
- produced_at: `2026-09-20T22:31:10+09:00`
- producer_run_id: `external-audit-auto-20260920T223110+0900-R3-C19V4-6B4E21D9`
- authority_scope: `INDEPENDENT_AUDITOR_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LEGACY_GENERATION_UNKNOWN`
- role: `INDEPENDENT_AUDITOR`
- genuinely_new_information: `true`

## Phase ordering

`phase_ordering_confirmed: true`

Phase 1 selected and fixed the audit target from repository evidence alone, after reading only prior role-specific audit history needed to avoid duplicate auditing. Control Brain, Evidence Analyst, MAIN/SUB summaries, and Literature were not read until the target and attack hypotheses were fixed.

### blind_target_selection

- target: C19 official-v4 `c19-external-v2-official-v4`, terminal `PASS`, exact claim boundary `truth_free_surface_structural_representation_gain_only`
- authoritative evidence tag: `evidence/c19-official-v4-c19-external-v2-official-v4`
- evidence commit: `a0f83318356ced1c84863737803080d0dc69d208`
- exact package: `74bfe6b4a39758656f291baaa3f16236e3e71964`
- STARTED: `control/c19-official-v4-started-20260917@3ebffb0c55ea9e5dac6c2a52d3d5c0ee6443d58e`
- raw preserve: `d8fcc5216ff24940836972816cb0ec8f11e4ba06`
- workflow: `35217655980`, attempt 1, completed/success
- attacks fixed blind:
  - package/STARTED/raw/evidence authority mismatch or post-START drift
  - scorer/evaluator target leakage despite truth-free raw boundary
  - reference/comparator mismatch or a degenerate reference condition
  - pseudo-replication / wrong independent resampling unit
  - seed fragility
  - unmatched baseline/resource privilege
  - simpler state-machine/FSA reduction
  - stale/duplicate evidence or broader-than-registered causal/novelty interpretation
- why consequential: C19-v4 is one of only five authoritative `evidence/*` tags and is the central positive external-validation result; a later authoritative C19-R2 tag provides a direct simpler-mechanism reduction that had not yet been independently synthesized against the original PASS.

`blind_target_change_reason: null`

## Phase 1 — repository-evidence audit

### 1. One-way integrity and target separation survive audit

The official-v4 authority chain is internally coherent. The annotated evidence tag resolves to evidence commit `a0f833...`; its manifest binds exact package `74bfe6...`, analyst admission `56f066...`, STARTED `3ebffb...`, raw preservation `d8fcc...`, workflow `35217655980`, and identity `c19-external-v2-official-v4`. The workflow completed once successfully. Raw preservation occurred before scoring and records `95920` target-blind predictions over `55 × 1744` row/pair observations with target fields not materialized. The scorer later joins only the fixed evaluator fields and fails closed on key/inventory mismatch.

No evidence of target leakage, retry, identity reuse, post-START scientific retuning, or package/evidence mismatch was found.

### 2. The frozen PASS is real but much narrower than a SparkBrain-specific superiority claim

The fixed primary comparison is `I2_truth_free_symbolic_surface/G1_coalition/E0_global` minus `I1_local_compositional/G1_coalition/E0_global`, using BREU=`(BU_Acc+BM_Acc)/2`. Official evidence reports effect `0.10044748325412106`, pair-bootstrap 95% CI `[0.09457740578201118, 0.10647303483001931]`, hence `PASS` under the frozen `lower_bound > 0` rule.

Read-only recomputation from the immutable per-seed metrics gives mean primary BREU `0.10044748325412045`. Every primary seed is positive (`0.1319631`, `0.1515912`, `0.0632202`, `0.0602282`, `0.0952347`), while the entire registered I1/G1 reference condition is exactly `BREU=0.0`, `BU_Acc=0.0`, `BM_Acc=0.0` for all five seeds. The PASS therefore establishes a surface-representation gain over this specific zero-performing reference path; it does not by itself establish a general model or mechanism advantage.

The scorer also explicitly marks learned/recurrent/transformer baseline matching as unasserted and `winner_claim_allowed=false`. Those rows are descriptive only, so C19-v4 cannot validly support a matched-resource superiority claim over them.

### 3. Later authoritative C19-R2 evidence directly reduces the positive result to a fixed seven-state FSA

The separate immutable tag `evidence/c19-r2-fsa-state-tracker-c19-r2-fsa-state-tracker-official-v1` closes with `REDUCED_BY_FSA`. Its exact primary contrast is `c19_v4_primary_breu_minus_r2_breu`; the fixed seven-state FSA has mean BREU `0.34667834014286114` versus C19-v4 primary mean `0.10044748325412045`, yielding observed effect `-0.2462308568887407`.

Crucially, R2 treats `atomic_idx` as the clustered independent unit: `204` unique clusters, paired cluster-bootstrap 95% CI `[-0.2554750732756702, -0.23690126111231016]`. A pair-IID sensitivity analysis gives nearly the same conclusion. Thus the later authoritative evidence does not merely match C19-v4; the simple fixed FSA substantially exceeds it on the registered comparison.

This independently supports `REDUCIBLE`: the original positive representational effect remains an immutable empirical PASS for its exact contrast, but it is not evidence for a SparkBrain-specific computational mechanism once the ordinary FSA reduction is admitted.

### 4. C19-v4 uncertainty used a weaker independence assumption than the later C19-R2 primary analysis

C19-v4's frozen bootstrap samples all `1744` official pairs as if they are the resampling units. C19-R2 later promotes an `atomic_idx` cluster bootstrap with only `204` unique clusters to primary inference and demotes pair-IID resampling to sensitivity-only. That later choice reveals a real inferential dependency structure not represented in the original v4 confidence interval.

This does **not** make the frozen C19-v4 evidence invalid: the exact registered statistic was followed, the five seed-level primary scores are all positive, and this audit did not re-score or replace the official result. It does mean the v4 CI should not be treated as the strongest available uncertainty statement. Any fresh successor should fix cluster-aware resampling prospectively from the start.

The R2 evidence itself states an interpretation ceiling: it tests only the fixed seven-state FSA reduction; C19-R1 revision-authority remains scientifically unresolved. This audit does not collapse that distinct unresolved question into the FSA result.

## Phase 2 — interpretation comparison

Only after the blind target was fixed, current Control Brain, Evidence Analyst, both MAIN/SUB streams, their newest role-suffixed reports, and the newest Literature stream were read.

Current strategy does not rely on C19-v4 as fresh mechanism novelty. Evidence Analyst holds FORMAL empty, records both C19-v4 and C19-R2 among consumed no-retry identities, and has no PRE_FORMAL-ready object. MAIN is intentionally idle; SUB is operating only bounded NON_EVIDENTIARY Discovery. The latest Literature concerns delayed temporal credit and does not alter this C19 audit. No current control-plane summary was found to overclaim C19-v4 beyond the immutable evidence boundary.

The Phase-1 target therefore remains unchanged.

## Audit classification

`REDUCIBLE`

The C19-v4 evidence chain and exact PASS remain valid for the registered narrow comparison. The scientifically important independent-audit result is that its positive effect is **not** a surviving SparkBrain-specific mechanism/novelty result: the registered reference is a complete zero sink, matched-resource superiority over the descriptive learned baselines was never authorized, and later immutable C19-R2 evidence shows a fixed seven-state FSA outperforms C19-v4 by about `0.24623` BREU under a cluster-aware primary analysis.

## Knowledge-flow contract

```yaml
role: INDEPENDENT_AUDITOR
genuinely_new_information: true
affected_lines:
  - C19_OFFICIAL_V4_EXTERNAL_VALIDATION
  - C19_R2_FSA_REDUCTION
  - PROGRAMME_EXTERNAL_VALIDATION
  - PROGRAMME_NOVELTY
  - FUTURE_EXTERNAL_VALIDATION_STATISTICS
novelty_or_reduction_impact: >
  C19-v4's immutable PASS remains valid only for its exact truth-free-surface
  versus local-compositional reference contrast. It does not survive as
  SparkBrain-specific mechanistic novelty: the registered reference is
  zero-performing, general learned-baseline superiority was never authorized,
  and authoritative C19-R2 shows a fixed seven-state FSA substantially exceeds
  the C19-v4 primary result under cluster-aware inference.
audit_classification: REDUCIBLE
blind_target_selection:
  target: c19-external-v2-official-v4 PASS / truth_free_surface_structural_representation_gain_only
  selected_before_control_plane_summaries: true
  authoritative_refs_inspected:
    - main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d
    - evidence tag object@4d6c0bd9a6c06c17352941d3fa730502e72b8540
    - evidence commit@a0f83318356ced1c84863737803080d0dc69d208
    - exact package@74bfe6b4a39758656f291baaa3f16236e3e71964
    - STARTED@3ebffb0c55ea9e5dac6c2a52d3d5c0ee6443d58e
    - raw preserve@d8fcc5216ff24940836972816cb0ec8f11e4ba06
    - C19-R2 evidence commit@6197fa801a78a0c5de4c2b6ff5d03216ac5539db
  attack_hypotheses:
    - authority/package/STARTED/raw/evidence mismatch or post-START drift
    - target/evaluator leakage
    - degenerate reference or comparator privilege mismatch
    - pseudo-replication / incorrect independent resampling unit
    - seed dependence
    - unmatched baseline/resource comparison
    - simpler fixed-state/FSA reduction
    - broader-than-registered novelty or causal interpretation
  why_consequential: C19-v4 is an authoritative positive evidence tag and its interpretation affects programme-level novelty.
blind_target_change_reason: null
prospective_baselines_or_discriminators:
  - keep C19-v4 and C19-R2 immutable; never rescore/relabel either canonical result
  - any fresh external-validation successor should prospectively use atomic/source-level cluster-aware inference when multiple pairs share a source unit
  - require a nondegenerate competent reference path rather than a zero-performing reference if the claim is representational/mechanistic advantage
  - include the fixed seven-state FSA as an ordinary baseline under matched information and resource privilege
  - require actual parameter/optimization/compute matching before any superiority claim over learned/recurrent/transformer baselines
  - keep C19-R1 revision-authority as a separate unresolved question rather than treating FSA reduction as its answer
questions_for_evidence_analyst:
  - Annotate C19-v4 synthesis as an exact-contrast PASS but programme-level REDUCIBLE result once C19-R2 is considered?
  - Preserve the frozen pair-bootstrap statistic as historical evidence while treating cluster-aware inference as the prospective standard for fresh successors?
  - Keep C19-R1 revision-authority explicitly unresolved and separate from the seven-state FSA reduction?
questions_for_control_brain:
  - Avoid counting C19-v4 as positive SparkBrain-specific mechanism/novelty support; retain it as a narrow historical representation-surface effect?
  - Require competent nonzero reference behavior plus matched FSA/resource baselines before any future external-validation promotion?
  - Keep FORMAL/PRE_FORMAL unaffected by this audit; no consumed identity is reopened?
must_not_change_frozen_or_consumed:
  - c19-external-v2-official-v4 and evidence tag
  - exact package 74bfe6b4a39758656f291baaa3f16236e3e71964
  - STARTED 3ebffb0c55ea9e5dac6c2a52d3d5c0ee6443d58e
  - raw preserve d8fcc5216ff24940836972816cb0ec8f11e4ba06
  - evidence commit a0f83318356ced1c84863737803080d0dc69d208 and canonical PASS statistics
  - c19-r2-fsa-state-tracker-official-v1 and evidence commit 6197fa801a78a0c5de4c2b6ff5d03216ac5539db
  - all C19-R1 consumed identities and their unresolved revision-authority ceiling
  - all other consumed PD01/NI01/H5 identities and immutable evidence
utility_request_created: null
```
