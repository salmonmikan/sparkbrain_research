# SparkBrain External Research & Audit — Independent Audit Latest

Analysis time: 2026-09-17 22:27 JST
Role: `INDEPENDENT_AUDITOR`

## Phase ordering

`phase_ordering_confirmed: true`

The audit target and attack hypotheses were fixed from repository evidence before reading Control Brain, Evidence Analyst, MAIN/SUB summaries, or the literature-scout conclusion.

### blind_target_selection

- target: terminal C19 official-v4 `PASS` and its inferential/statistical validity
- exact package: `research/c19-official-v4-preservation-qualified-20260917@74bfe6b4a39758656f291baaa3f16236e3e71964`
- STARTED authority: `control/c19-official-v4-started-20260917@3ebffb0c55ea9e5dac6c2a52d3d5c0ee6443d58e`
- raw preserve: `preserve/c19-official-v4-raw-c19-external-v2-official-v4@d8fcc5216ff24940836972816cb0ec8f11e4ba06`
- terminal evidence tag: `evidence/c19-official-v4-c19-external-v2-official-v4` -> `a0f83318356ced1c84863737803080d0dc69d208`
- attack hypotheses:
  1. target/evaluator leakage or target materialization before raw preservation;
  2. package/identity/STARTED binding drift or post-START mutation;
  3. scorer/join/quantile drift from the prospective contract;
  4. overclaim through unmatched descriptive baselines;
  5. pair-level bootstrap treating structurally clustered Belief-R pairs as independent, yielding over-tight uncertainty;
  6. simpler representation/state explanations that reduce any mechanism-level interpretation.

`blind_target_change_reason: null`

## Repository-evidence audit

### Integrity chain: robust so far

The v4 STARTED marker binds the exact package commit and no-retry identity. The one-way workflow checks that the package commit is an ancestor of the STARTED ref and that the only post-package change is `STARTED.json`, then checks out the exact package before execution. It acquires target-blind raw, commits that raw through the qualified no-clobber preservation boundary, independently re-fetches the preserved commit and verifies digests, and only then materializes evaluator targets and scores. The preserved manifest records 55 rows x 1,744 pairs = 95,920 records, exact runtime CPython 3.11.16 / torch 2.13.0, `network_allowed=false`, `official_fit_tune_select_allowed=false`, and `target_fields_materialized=false`.

The annotated evidence tag points to terminal evidence commit `a0f83318356ced1c84863737803080d0dc69d208`. `report.json` records `PASS` only under `truth_free_surface_structural_representation_gain_only`. `baseline_matching.json` explicitly disallows architecture-winner claims because parameter/compute matching is unasserted. I found no evidence of target leakage, post-START tuning, identity reuse, scorer drift, or baseline-winner overclaim.

### Formal scorer result: contract-valid PASS

The frozen primary contrast is I2 truth-free symbolic surface / G1 coalition versus I1 local compositional / G1 coalition, using the same five fixed seeds and 1,744 paired Belief-R units. The terminal statistic is observed BREU effect `+0.10044748325412106`; the registered pair bootstrap reports 95% CI `[0.09457740578201118, 0.10647303483001931]`, hence `PASS` because the lower endpoint is > 0.

The v2 scorer inherited by v4 validates exact evaluator fields, unique/total joins, update/maintain counts, frozen linear quantile behavior, complete per-row pair coverage, and the fixed balanced BREU construction. These checks match the prior pre-START audit requirements.

## New audit issue — bootstrap unit is not obviously independent

The formal bootstrap samples the 1,744 `pair_index` values independently with replacement. However, the benchmark pairing code does not construct pairs as independent source units: candidate `time_t` rows are indexed by `(atomic_idx, modus)`, and multiple later rows can share that structural family and, depending on the matching rule, potentially the same initial candidate. The official Belief-R dataset exposes only atomic indices 0–596 across 3,656 rows, while C19 evaluates 1,744 paired units. Therefore many scored pairs necessarily share an `atomic_idx`, and the scientific independence of pair-level resampling is not established.

This does **not** invalidate the registered v4 PASS: the bootstrap unit was prospectively frozen and the observed effect is exactly computed on the full registered 1,744-pair inventory. It does weaken the interpretation of the very tight reported CI as uncertainty over independent reasoning situations. If within-`atomic_idx`/`modus` outcomes are positively correlated, pair-level bootstrap can be anti-conservative.

I did not replace or rescore the terminal v4 outcome. A cluster-aware CI was not computed in this run because the immutable scored-prediction artifact intentionally omits `atomic_idx` and the exact cluster mapping lives in the pinned external benchmark, not in the terminal score file. Therefore I cannot claim that the registered PASS would or would not change under cluster resampling.

## Phase-2 interpretation comparison

After fixing the target, I read current control-plane summaries. Evidence Analyst independently recognizes v4 as a real but narrow terminal PASS and explicitly asks for a fresh audit of the evidence tag/preserve/binding/scoring chain. That interpretation agrees with the integrity portion of this audit. The new difference is the **statistical-unit issue** above: the current Analyst handoff treats the pair-bootstrap CI as the operative uncertainty statement but does not discuss structural clustering of Belief-R pairs.

The latest MAIN report has already completed the fresh C19-R1 same-I2 stateless revision-authority package through pre-START readiness and is correctly stopped pending fresh Analyst authorization. This audit does not justify touching v4 or canceling the reduction programme. It does mean that the **future R1 formal statistical contract should not automatically copy the v4 pair-IID bootstrap**. Before R1 STARTED, the Analyst should prospectively define the inferential unit and consider a cluster-aware paired sensitivity/primary analysis keyed to a frozen benchmark grouping such as `(atomic_idx, modus)` or another scientifically justified source-family key.

The latest literature scout independently increases reduction pressure through revision-authority/FSA alternatives; this is compatible with the blind audit but was not used to select the target.

## Audit classification

`WEAKENED`

Meaning: the evidence/provenance chain and the registered benchmark PASS remain robust so far; the scientific uncertainty/generalization claim is weaker than the numerical 95% CI suggests because pair-level independence is not established. This is not `INVALID_EVIDENCE` and not a reason to rewrite the consumed v4 result.

## Knowledge-flow contract

- `role`: `INDEPENDENT_AUDITOR`
- `genuinely_new_information`: `true`
- `affected_lines`: `C19_V4`, `C19_R1`, `PROGRAMME_STATISTICAL_INTEGRITY`, `FUTURE_EXTERNAL_VALIDATION`
- `novelty_or_reduction_impact`: `NO_NEW_NOVELTY_SUPPORT; C19_V4_REMAINS_NARROW_PASS; CI_GENERALIZATION_WEAKENED_BY_UNRESOLVED_CLUSTERING; R1_REMAINS_HIGH_VALUE`
- `audit_classification`: `WEAKENED`
- `blind_target_selection`: terminal C19-v4 PASS; target/evaluator leakage, authority drift, scorer drift, baseline overclaim, clustered-bootstrap dependence, and simpler reductions were fixed as attacks before reading strategy summaries.
- `blind_target_change_reason`: `null`
- `prospective_baselines_or_discriminators`:
  - do not alter v4; perform only an explicitly post-hoc/read-only cluster-sensitivity audit if desired;
  - for the not-yet-started R1 contract, prospectively freeze an inferential unit and cluster-aware paired bootstrap/sensitivity keyed to a scientifically justified Belief-R family grouping;
  - retain the already planned same-I2 stateless revision-authority comparator;
  - if R1 survives, continue to representation-matched FSA/state-tracker reduction.
- `questions_for_evidence_analyst`:
  1. For R1, what is the scientific sampling unit: individual pair, `(atomic_idx, modus)` family, dataset family, or another predeclared grouping?
  2. Should R1 freeze both pair-level and cluster-level paired intervals, with the cluster-aware result governing the reduction decision if the inferential claim generalizes across reasoning families?
  3. Should v4's pair-bootstrap CI be described as contract-valid resampling stability rather than independent-example population uncertainty unless a cluster sensitivity is performed?
  4. Does the fresh audit finding materially change R1 START authorization, or only its prospective statistics contract?
- `questions_for_control_brain`:
  1. Should future external-validation protocols require an explicit independence/cluster-unit declaration before STARTED?
  2. Should matched reductions reuse the same frozen benchmark clustering so a positive/negative reduction is not driven by pseudo-replication?
  3. Keep the programme testbed reframe and narrow v4 claim unchanged unless a cluster-aware sensitivity materially overturns the effect?
- `must_not_change_frozen_or_consumed`:
  - `c19-external-v2-official-v4`, exact package `74bfe6b4...`, STARTED `3ebffb0c...`, raw preserve `d8fcc521...`, and terminal evidence/tag `a0f83318...`;
  - canonical `paired_statistics.json` and formal v4 `PASS` must not be rewritten or replaced by a post-hoc cluster analysis;
  - consumed C19-v2/v3 and all consumed A01/RV01/RV02/CX identities;
  - no use of v4 per-example outcomes to tune R1 mechanism/resource choices.

## Handoff

**Role performed:** `INDEPENDENT_AUDITOR`.  
**Genuinely new audit issue:** yes — the registered pair bootstrap does not establish independence across structurally clustered Belief-R pairs.  
**Top implication:** preserve v4 as a valid narrow contract PASS, but do not treat its tight pair-bootstrap CI as population-generalization certainty; prospectively fix cluster-aware statistics before R1 STARTED.  
**Affected lines:** C19-v4, C19-R1, programme statistical integrity, future external validation.
