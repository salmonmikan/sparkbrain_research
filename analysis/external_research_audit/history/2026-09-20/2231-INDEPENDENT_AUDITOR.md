# Independent Auditor — C19-v4 external validation / FSA reduction

- schema_version: `2`
- generation_id: `AUD-20260920T223110+0900-R3-C19V4-REDUCTION-6B4E21D9`
- produced_at: `2026-09-20T22:31:10+09:00`
- producer_run_id: `external-audit-auto-20260920T223110+0900-R3-C19V4-6B4E21D9`
- authority_scope: `INDEPENDENT_AUDITOR_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LEGACY_GENERATION_UNKNOWN`
- role: `INDEPENDENT_AUDITOR`
- phase_ordering_confirmed: `true`
- genuinely_new_information: `true`
- audit_classification: `REDUCIBLE`

## Blind Phase 1

Before reading Control Brain, Evidence Analyst, MAIN/SUB, or Literature summaries, repository evidence fixed the target as C19 official-v4 `c19-external-v2-official-v4`, canonical `PASS`, exact claim boundary `truth_free_surface_structural_representation_gain_only`. Prior Auditor history showed NI01 and H5 had already been audited; C19-v4 had not.

Authoritative chain inspected read-only:

- `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- C19-v4 evidence tag object `4d6c0bd9a6c06c17352941d3fa730502e72b8540`
- evidence commit `a0f83318356ced1c84863737803080d0dc69d208`
- exact package `74bfe6b4a39758656f291baaa3f16236e3e71964`
- STARTED `control/c19-official-v4-started-20260917@3ebffb0c55ea9e5dac6c2a52d3d5c0ee6443d58e`
- raw preservation `d8fcc5216ff24940836972816cb0ec8f11e4ba06`
- workflow `35217655980`, attempt 1, success
- C19-R2 evidence tag object `82b88f3e2ad524fed8b72300dcba46053c1f2c7e`
- C19-R2 evidence commit `6197fa801a78a0c5de4c2b6ff5d03216ac5539db`
- C19-R2 workflow `35288390550`, attempt 1, success

Blind attack hypotheses: authority drift; target leakage; reference/comparator mismatch; pseudo-replication; seed dependence; resource mismatch; simpler state-machine/FSA reduction; stale/duplicate evidence; and overclaim beyond the registered boundary.

`blind_target_change_reason: null`

## Repository evidence findings

### One-way chain: robust

C19-v4 exact package, STARTED, single successful workflow, target-blind raw-before-score preservation, evaluator join, and terminal evidence all bind coherently. The raw manifest records 55 rows × 1744 pairs = 95920 predictions with target fields not materialized; network access and official fit/tune/select were disabled. The scorer validates exact evaluator fields and join keys only after raw preservation. No retry, identity mismatch, target leakage, or post-START scientific retuning was found.

### Frozen PASS: valid but narrow

The registered primary is `I2_truth_free_symbolic_surface/G1_coalition/E0_global` minus `I1_local_compositional/G1_coalition/E0_global` on BREU. Frozen evidence reports effect `0.10044748325412106`, pair-bootstrap 95% CI `[0.09457740578201118, 0.10647303483001931]`, hence PASS.

Read-only recomputation from immutable per-seed metrics gives C19-v4 primary mean BREU `0.10044748325412045`. All five primary seeds are positive, but the entire registered I1/G1 reference has BREU=BU_Acc=BM_Acc=`0.0` in every seed. The positive result therefore establishes improvement over this exact zero-performing reference path, not a general architecture or mechanism advantage.

The official scorer separately records learned/recurrent/transformer baseline matching as unasserted and `winner_claim_allowed=false`; those rows are descriptive only.

### Simpler fixed seven-state FSA reduction: decisive for mechanism/novelty interpretation

Authoritative C19-R2 closes `REDUCED_BY_FSA`. Its fixed seven-state FSA mean BREU is `0.34667834014286114`. The registered reduction contrast `c19_v4_primary_breu_minus_r2_breu` is `-0.2462308568887407` with primary `atomic_idx` cluster-bootstrap 95% CI `[-0.2554750732756702, -0.23690126111231016]` across `204` unique clusters. Pair-IID sensitivity gives essentially the same conclusion.

Thus C19-v4 remains a valid historical exact-contrast PASS, but no longer survives as SparkBrain-specific computational/mechanistic novelty once the immutable R2 ordinary reduction is admitted.

### Statistical interpretation ceiling

C19-v4 froze pair-IID bootstrap over all `1744` pairs. C19-R2 later treats only `204` `atomic_idx` source clusters as the primary resampling units and explicitly demotes pair-IID to sensitivity. This reveals dependency structure absent from the original v4 uncertainty model. The audit does not rescore or invalidate the frozen PASS; it records that future successors should bind cluster-aware inference prospectively and that the original v4 CI is not the strongest available uncertainty statement.

R2 itself limits the conclusion to the fixed seven-state FSA and explicitly leaves C19-R1 revision-authority unresolved. This separate ceiling remains intact.

## Phase 2 comparison

After Phase 1 was fixed, consumed generations were:

- Control: `CTRL-20260920T205000+0900-R16-5E9A71C3@016a248143dc71380fca28128d564d74aeb4c3f3`
- Evidence Analyst: `EVA-20260920T215718+0900-R21-4F8C2A71@f85692e6e207ae622282116779b559108085ede8`
- MAIN: `MAIN-20260920T221704+0900-PRIMARY-FUNNEL21-HOLD-R21-9C2A7E41@e2cf88dc98d00f20df73789e4824a81325eb0c0f`
- SUB: `SUB-20260920T214600+0900-THEORY-PREDERR-5C8A2F17@3cc5daa65b0decbbd689a9181e94602de5e395f9`
- Literature: `LIT-20260920T213000+0900-R14-DELAYED-CREDIT-9C4E71B2@d2047294508816007249f23e06f3b8c3687628df`
- prior Audit: `LEGACY_GENERATION_UNKNOWN@d3a9c8d4c4cf8a3e5a0152d7b0749633776ecb56`

Current control-plane interpretation does not overclaim C19-v4: FORMAL and PRE_FORMAL are empty, C19-v4 and C19-R2 remain consumed no-retry identities, MAIN is intentionally idle, and SUB is NON_EVIDENTIARY Discovery only. No Phase-1 target change was warranted.

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
  why_consequential: authoritative positive external-validation evidence with a later direct FSA reduction
blind_target_change_reason: null
prospective_baselines_or_discriminators:
  - never rerun/rescore/relabel/reopen canonical C19-v4 or C19-R2
  - prospectively use source/atomic-cluster-aware inference for fresh successors
  - require a competent nondegenerate reference path for representational/mechanistic advantage claims
  - include the fixed seven-state FSA under matched information/resource privilege
  - require actual parameter/optimization/compute matching for learned-baseline superiority claims
  - keep C19-R1 revision-authority separate and unresolved
questions_for_evidence_analyst:
  - Treat C19-v4 as exact-contrast PASS but programme-level REDUCIBLE once R2 is integrated?
  - Preserve pair-bootstrap as frozen history while making cluster-aware inference prospective standard?
  - Keep C19-R1 revision-authority separate from FSA reduction?
questions_for_control_brain:
  - Do not count C19-v4 as surviving SparkBrain-specific mechanism/novelty support?
  - Require competent reference plus matched FSA/resource baselines before future external-validation promotion?
  - Keep FORMAL/PRE_FORMAL unchanged and reopen no consumed identity?
must_not_change_frozen_or_consumed:
  - c19-external-v2-official-v4, package, STARTED, raw preserve, evidence commit/tag and canonical PASS statistics
  - c19-r2-fsa-state-tracker-official-v1 and its immutable evidence
  - all consumed C19-R1 identities and unresolved revision-authority ceiling
  - all other consumed PD01/NI01/H5 identities and immutable evidence
utility_request_created: null
```

No Utility request was created because C19-R2 already provides the decisive cluster-aware simpler-mechanism reduction; a duplicate recomputation request would add little information and risks encouraging unnecessary work on consumed identities.
