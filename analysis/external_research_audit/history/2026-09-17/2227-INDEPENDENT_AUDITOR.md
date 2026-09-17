# SparkBrain External Research & Audit — 2026-09-17 22:27 JST

Role: `INDEPENDENT_AUDITOR`

## Phase ordering

The blind target was fixed before reading Control Brain, Evidence Analyst, MAIN/SUB reports, or the literature-scout stream.

`blind_target_selection`:
- target: terminal C19 official-v4 `PASS` and its inferential/statistical validity
- authoritative package: `74bfe6b4a39758656f291baaa3f16236e3e71964`
- STARTED: `3ebffb0c55ea9e5dac6c2a52d3d5c0ee6443d58e`
- target-blind preserve: `d8fcc5216ff24940836972816cb0ec8f11e4ba06`
- terminal evidence: `evidence/c19-official-v4-c19-external-v2-official-v4` -> `a0f83318356ced1c84863737803080d0dc69d208`
- blind attacks: target leakage; authority drift; scorer/join/quantile drift; unmatched-baseline overclaim; pair-bootstrap dependence; simpler reductions.

`blind_target_change_reason: null`

## Result

The target-blind/raw-before-score chain is strong. STARTED binds the exact package and no-retry identity. The workflow checks the exact package/STARTED diff, checks out the exact package, preserves target-blind raw through a no-clobber branch, independently re-fetches and digest-verifies it, and only after that materializes evaluator targets and scores. The preserved manifest records 55 x 1,744 = 95,920 records and `target_fields_materialized=false`. The terminal annotated evidence tag points to `a0f83318...`.

The formal result is contract-valid: primary BREU effect `+0.10044748325412106`, registered 95% pair-bootstrap CI `[0.09457740578201118, 0.10647303483001931]`, result `PASS`. The terminal claim is deliberately restricted to `truth_free_surface_structural_representation_gain_only`, and the evidence explicitly prohibits winner claims for unmatched descriptive baselines.

### New audit issue: registered bootstrap unit is not obviously independent

The scorer independently resamples the 1,744 `pair_index` values. But Belief-R pair construction indexes candidate initial rows by `(atomic_idx, modus)`, so multiple later pairs can belong to the same structural family and can reuse closely related source structure. The official dataset exposes atomic indices only 0–596 across 3,656 rows, while C19 scores 1,744 pairs. Pair-level independence is therefore not established.

This does not invalidate the frozen v4 PASS or change its canonical result. It does mean that the very tight pair-bootstrap CI should not automatically be interpreted as population-generalization uncertainty across independent reasoning situations. Positive within-family dependence can make an IID pair bootstrap anti-conservative.

No post-hoc rescore was substituted for the formal result. A cluster-aware CI was not calculated in this run because terminal `scored_predictions.json` intentionally omits `atomic_idx`, while the exact cluster mapping is external to the terminal score artifact. A future read-only sensitivity can be done without changing v4, but the higher-value action is prospective: R1 is still pre-START, so its formal statistical contract can explicitly freeze the inferential unit and cluster handling before execution.

## Control-plane comparison

After fixing the blind target, Evidence Analyst was read. It independently treats C19-v4 as a real but narrow PASS and explicitly requested a fresh audit of the tag/preserve/binding/scoring chain. The integrity conclusion agrees. The new point not present in that handoff is the pair-dependence / clustering issue.

MAIN has already brought C19-R1 to green pre-START readiness and is correctly stopped pending fresh Analyst authorization. This audit does not justify touching v4 or abandoning R1. It does suggest that a future R1 formal contract should not silently copy the pair-IID bootstrap: prospectively define the sampling unit and include a cluster-aware paired analysis if the intended inference generalizes across benchmark source families.

The literature scout's revision-authority/FSA reduction ladder is compatible with this result but did not determine the target.

## Classification

`WEAKENED`

The registered benchmark PASS and provenance chain remain robust so far; uncertainty/generalization beyond the exact pair inventory is weaker than the reported narrow CI suggests until benchmark clustering is handled explicitly.

## Knowledge-flow contract

- `role`: `INDEPENDENT_AUDITOR`
- `genuinely_new_information`: `true`
- `affected_lines`: `C19_V4`, `C19_R1`, `PROGRAMME_STATISTICAL_INTEGRITY`, `FUTURE_EXTERNAL_VALIDATION`
- `novelty_or_reduction_impact`: `NO_NEW_NOVELTY_SUPPORT; C19_V4_REMAINS_NARROW_PASS; CI_GENERALIZATION_WEAKENED_BY_UNRESOLVED_CLUSTERING; R1_REMAINS_HIGH_VALUE`
- `audit_classification`: `WEAKENED`
- `blind_target_selection`: terminal C19-v4 PASS; target leakage, authority drift, scorer drift, baseline overclaim, clustered-bootstrap dependence and simpler reductions were fixed as attacks before strategy summaries.
- `blind_target_change_reason`: `null`
- `prospective_baselines_or_discriminators`: do not alter v4; optional post-hoc read-only cluster sensitivity only; before R1 STARTED freeze the scientific sampling unit and cluster-aware paired statistics; retain same-I2 stateless revision-authority reduction; if survived, continue to matched FSA/state-tracker reduction.
- `questions_for_evidence_analyst`:
  1. What is the scientific sampling unit for R1: pair, `(atomic_idx, modus)` family, dataset family, or another predeclared grouping?
  2. Should R1 freeze both pair-level and cluster-aware intervals, with cluster-level inference governing claims across reasoning families?
  3. Should v4's pair-bootstrap CI be described as contract-valid resampling stability unless a cluster sensitivity supports broader inference?
  4. Does this finding change R1 START authorization or only the prospective statistics contract?
- `questions_for_control_brain`:
  1. Require explicit independence/cluster-unit declarations in future external-validation protocols?
  2. Require matched reductions to reuse a fixed benchmark clustering to avoid pseudo-replication?
  3. Keep v4's narrow claim and testbed reframe unchanged unless a cluster-aware sensitivity materially overturns the signal?
- `must_not_change_frozen_or_consumed`: C19-v4 package/STARTED/raw/evidence/tag and formal PASS; consumed C19-v2/v3; all consumed A01/RV01/RV02/CX identities; do not use v4 per-example outcomes to tune R1.

## Handoff

**Role performed:** `INDEPENDENT_AUDITOR`.  
**Genuinely new audit issue:** yes.  
**Top implication:** preserve C19-v4 as a narrow contract-valid PASS, but prospectively fix cluster-aware inferential semantics before R1 STARTED rather than treating the v4 pair-bootstrap CI as independent-situation certainty.  
**Affected lines:** C19-v4, C19-R1, programme statistical integrity, future external validation.
