# SparkBrain Methodology Calibration Audit — 2026-09-20 23:20 JST

schema_version: `2`  
generation_id: `METHCAL-20260920T232040+0900-R22-6D3A91E4`  
produced_at: `2026-09-20T23:20:40+09:00`  
producer_run_id: `methodology-calibration-auto-20260920T232040+0900-R22-6D3A91E4`  
authority_scope: `METHODOLOGY_ADVISORY_ONLY`  
supersedes_generation_id: `METHCAL-20260920T212247+0900-R21-5A8C21D4`

## Run disposition

**`MATERIAL_CALIBRATION_UPDATE`**

## Overall classification

**`WELL_CALIBRATED`** — unchanged overall.

Two material calibration updates are supported.

First, the Funnel-v2.1 HOLD-field applicability defect identified in R21 is now prospectively resolved across the designated control plane. Control R17 explicitly corrects its earlier R16 interpretation and adopts the Evidence Analyst rule: `hold_class` and `hold_reason` are required iff `classification=HOLD`; non-HOLD dispositions such as `REJECT` correctly keep them null, while `terminal_state` and `queue_state` remain required. Canonical Evidence Analyst R21 is therefore 17/17 complete. The previous `CLARIFY` recommendation can move to `KEEP` for the multidimensional HOLD model and its applicability semantics.

Second, fresh Independent Audit R3 provides a consequential external-calibration example. C19-v4's immutable exact PASS remains valid for its registered truth-free-surface versus local-compositional contrast, but the registered reference is a zero-performing path and later authoritative C19-R2 evidence shows a fixed seven-state FSA substantially exceeds it under cluster-aware inference. This does not retroactively invalidate or rescore C19-v4. It does support prospective claim-type-specific tightening for future external-validation superiority claims: use a competent nondegenerate reference, include the simple FSA/state-tracker reduction when relevant, match information/resource privilege, and use source/atomic-unit cluster-aware inference when multiple observations share one source unit.

Scientific admission, general discovery comparator rules, PRE_FORMAL readiness semantics, and the hard integrity floor remain unchanged.

## Strongest current evidence

### 1. HOLD applicability is now aligned rather than merely clarified

Control `CTRL-20260920T225013+0900-R17-3F8C61A2` explicitly states that its prior R16 15/16 view was incorrect and adopts applicability-aware semantics. Evidence Analyst `EVA-20260920T215718+0900-R21-4F8C2A71` already applies the same rule and reports 17/17 classification completeness. This closes the cross-role schema disagreement that could have manufactured false funnel incompleteness.

Canonical policy metrics must use the 17/17 Analyst-reviewed population. A fresh SUB object exists after Analyst R21; it is candidate-locally complete but remains pending independent Analyst incorporation, so it must not silently change canonical conversion counts.

### 2. Fresh theory-backward supply is genuinely mechanistic and prospectively falsifiable

`CAND-V05-ELIGIBILITY-HISTORY-SPECIFICITY-01` was bound before outcome at `e466bd89cfd4ab80dc970173a183638af815fe8b` as a fresh `MECHANISM` object, with `preformal_eligible=true in principle`, readiness=`NOT_READY`, exact current-object question, ordinary per-edge eligibility-trace comparator, falsifier, terminal mapping and no-rescue boundary. Stable-main `V05PlasticityController.apply()` independently confirms the prospectively modeled decay-plus-current-delta eligibility semantics.

Final research head `6ddcb7fec39dd017fbfe172885a994a98b503021` records exact reduction to the fixed ordinary recurrence and proposes `REJECT / MECHANISM / preformal_eligible=false / NOT_READY / TERMINAL_FOR_CURRENT_OBJECT / NOT_QUEUED`, with null HOLD-only fields and no cycle 2. No same-object SYSTEM rescue or upgrade occurred.

The pre-selection rolling SUB window was already compliant at 2/3 MECHANISM, so this object was not required for quota compliance. After it, the observed window is 3/3. Treat 3/3 as an incidental outcome, not a target. Because several recent probes cluster around responsibility/credit surfaces, keep an opportunity-cost watch and switch domains/no-op when marginal mechanism information falls.

### 3. Independent external audit sharpens comparator calibration without rewriting history

Independent Audit `AUD-20260920T223110+0900-R3-C19V4-REDUCTION-6B4E21D9` finds no one-way-integrity failure in C19-v4 and preserves its exact PASS. The authoritative evidence tag resolves to `a0f83318356ced1c84863737803080d0dc69d208`, whose evidence explicitly disallows winner claims over unmatched learned/recurrent/transformer baselines. Separate authoritative C19-R2 evidence `6197fa801a78a0c5de4c2b6ff5d03216ac5539db` records `REDUCED_BY_FSA`, primary paired `atomic_idx` cluster bootstrap over 204 clusters, and observed C19-v4-minus-FSA effect about `-0.24623`.

Methodological lesson: research-worthiness and an exact registered PASS are not equivalent to surviving mechanism/novelty support. Future external-validation advantage claims should prospectively face competent references, simple reduction baselines and the correct independent resampling unit. This is a claim-type-specific tightening, not a programme-wide numeric threshold.

## Funnel v2.1 audit

1. `claim_ceiling` current-object semantics: **KEEP**. Fresh SUB is prospectively MECHANISM for the current object; no prestige/topic relabeling observed.
2. same-object SYSTEM→MECHANISM upgrade ban: **KEEP**. No completed SYSTEM object was upgraded in place.
3. `preformal_eligible` vs READY: **KEEP**. Fresh prospective history again shows `eligible=true` can coexist with `NOT_READY` before outcome.
4. READY semantics: **KEEP**; `HIDDEN_SECOND_FORMAL_GATE=false`. First Analyst-authoritative READY→PRE_FORMAL remains **INSUFFICIENT_EVIDENCE**.
5. HOLD multidimensional model and applicability mask: **KEEP**. Cross-role disagreement is now corrected: HOLD fields iff HOLD; terminal/queue fields for all material objects.
6. MAIN SYSTEM-over-MECHANISM rule: **KEEP**. No genuine exception has been used; first live use remains **INSUFFICIENT_EVIDENCE**.
7. `NO_COHERENT_MECHANISM_TARGET`: **KEEP**. Still unused; first live use remains **INSUFFICIENT_EVIDENCE**.
8. theory-backward selection quality: **KEEP**. Fresh object is mechanism-level, falsifiable and accepts an ordinary reduction; not a relabeled SYSTEM question.
9. SYSTEM value under MECHANISM priority: **KEEP**. Recent bounded SYSTEM Architecture work retained testbed/architecture value and stopped rather than being inflated into novelty.
10. PRE_FORMAL/PASS reachability: **REACHABLE_BUT_NARROW**. No evidence that v2.1 requires prior scientific victory merely to become READY, but no READY object exists yet.
11. classification-completeness gating: **KEEP**. Policy conclusions use 17/17 reviewed canonical population; fresh unreviewed object is excluded pending Analyst review.
12. first READY→PRE_FORMAL empirical semantics: **INSUFFICIENT_EVIDENCE**.

## Material gate classifications

- hard integrity floor: `KEEP`
- prospective terminal/API semantic binding: `KEEP`
- outcome-exposed repair containment: `KEEP`
- current-object `claim_ceiling`: `KEEP`
- same-object SYSTEM→MECHANISM upgrade ban: `KEEP`
- fresh-successor discipline: `KEEP`
- `preformal_eligible` / READY separation: `KEEP`
- READY development-readiness semantics: `KEEP`
- HOLD multidimensional model: `KEEP`
- HOLD field applicability mask: `KEEP`
- classification-completeness applicability semantics: `KEEP`
- MAIN MECHANISM priority: `KEEP`
- prospective SYSTEM-priority exception: `KEEP`
- rolling one-in-three theory-backward supply: `KEEP`
- theory-backward quality floor: `KEEP`
- `NO_COHERENT_MECHANISM_TARGET`: `KEEP`
- SYSTEM architecture/testbed/reproducibility value: `KEEP`
- general equal-privilege comparator / ordinary-reduction-first: `KEEP`
- external-validation competent-reference requirement for superiority/novelty claims: `TIGHTEN`
- external-validation source/atomic-unit resampling when observations are clustered: `TIGHTEN`
- historical immutable-result interpretation ceiling: `KEEP`
- research-worthiness vs novelty separation: `KEEP`
- no universal numeric readiness/support threshold: `KEEP`
- legacy Top-k sparse-support weakness: `TIGHTEN`
- first READY→PRE_FORMAL: `INSUFFICIENT_EVIDENCE`
- first genuine SYSTEM-priority exception: `INSUFFICIENT_EVIDENCE`
- first `NO_COHERENT_MECHANISM_TARGET` use: `INSUFFICIENT_EVIDENCE`

## Calibration dimensions

`gate_drift`: no current scientific gate drift; prior HOLD applicability drift is resolved.  
`justification_trace`: strong; the Control correction, Analyst canonical semantics, fresh SUB prospective contract, and independent external audit are all visible.  
`false_positive_control`: strong, with one prospective tightening for external-validation advantage claims where degenerate references or wrong resampling units could inflate interpretation.  
`false_negative_risk`: low-to-moderate; do not universalize FSA or cluster-bootstrap requirements to unrelated bounded Discovery questions.  
`duplicate_guards`: none material.  
`moving_goalposts`: `LOW`; C19-v4 remains immutable PASS and is not rescored/relabelled; programme interpretation narrows only by separate later evidence.  
`pass_reachability`: `REACHABLE_BUT_NARROW`.  
`comparator_calibration`: healthy for current lower-funnel Discovery; external-validation superiority claims need the tightened competent-reference/reduction rule prospectively.  
`signal_before_reduction`: healthy.  
`claim_type_separation`: healthy.  
`research_worthiness_vs_novelty`: strengthened by the C19-v4/R2 example.  
`external_calibration`: materially improved.  
`opportunity_cost`: healthy with a watch on serial near-neighbor responsibility/credit probes.  
`mechanism_supply_health`: `HEALTHY_SMALL_N_3_OF_3_WITH_NEAR_NEIGHBOR_OPPORTUNITY_COST_WATCH`.  
`funnel_observability`: `GOOD_V2_1_17_OF_17_CANONICAL_PLUS_1_PENDING_APPLICABILITY_ALIGNED`.  
`preformal_gate_calibration`: `ELIGIBILITY_READINESS_SEPARATION_REPLICATED_READY_TRANSITION_UNTESTED`.

## Prospective recommendations

1. Keep the scientific admission, lower-funnel novelty/reduction, PRE_FORMAL readiness, and hard-integrity floors unchanged.
2. Treat the HOLD applicability rule as settled shared semantics: HOLD fields required iff HOLD; terminal/queue fields required for every material object; completeness computed over applicable fields.
3. For fresh external-validation superiority/novelty claims, prospectively require a competent nondegenerate reference and relevant simple reduction comparator under matched information/resource privilege. Where multiple observations share an atomic/source unit, bind source-level clustered inference prospectively.
4. Do not apply those external-validation requirements as universal gates to unrelated bounded Discovery questions.
5. Keep one-in-three as a minimum. The current 3/3 mechanism window is not a target; select next SUB work by marginal information gain and use credible no-target/no-op semantics instead of serial low-yield credit microprobes.
6. Audit the first READY→PRE_FORMAL, first genuine MAIN SYSTEM-over-comparable-MECHANISM exception, and first `NO_COHERENT_MECHANISM_TARGET` use.

## Utility request

None created. Live rollout plus the fresh independent external audit already provide higher-information calibration evidence than a synthetic methodology probe.

## Hard-integrity-floor confirmation

**CONFIRMED / DO NOT RELAX.** No recommendation changes consumed/frozen identities, rerun/retune rules, prospective/frozen protocols, raw-before-score, preserve-before-read, exact identity/source/package/runtime/input binding, immutable evidence, leakage controls, or the prohibition on silent post-outcome repair.

## Current inputs / authoritative refs

- stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- previous Methodology `METHCAL-20260920T212247+0900-R21-5A8C21D4@72c703feaf54e5c1ed1667c3d1c221686793492a`
- Control `CTRL-20260920T225013+0900-R17-3F8C61A2@90c088f5fc3f6064f883d308ba5e1af9fd076441`
- Evidence Analyst `EVA-20260920T215718+0900-R21-4F8C2A71@f85692e6e207ae622282116779b559108085ede8`
- fresh SUB `SUB-20260920T224620+0900-THEORY-ELIGHIST-8D4C71A2`; prospective binding `e466bd89cfd4ab80dc970173a183638af815fe8b`; research head `6ddcb7fec39dd017fbfe172885a994a98b503021`; exact-head CI `35514340688` success
- Independent Audit `AUD-20260920T223110+0900-R3-C19V4-REDUCTION-6B4E21D9@2edf544763d699ccfe81dd52044f776e5425a90d`
- C19-v4 evidence tag object `4d6c0bd9a6c06c17352941d3fa730502e72b8540` -> evidence commit `a0f83318356ced1c84863737803080d0dc69d208`
- C19-R2 FSA evidence tag object `82b88f3e2ad524fed8b72300dcba46053c1f2c7e` -> evidence commit `6197fa801a78a0c5de4c2b6ff5d03216ac5539db`
- authoritative `evidence/*` tags: 5; `formal/*`: 0; `sealed/*`: 0; tag-based `freeze/*`: 0

## Confidence

**HIGH** in overall `WELL_CALIBRATED`, in the resolution of HOLD applicability semantics, and in the claim-type-specific external-validation tightening. **MODERATE_HIGH** on mechanism-supply health because the current 3/3 window is genuine but increasingly clustered around credit/responsibility questions. **INSUFFICIENT_EVIDENCE** remains for first READY→PRE_FORMAL, first genuine MAIN SYSTEM-priority exception, and first no-coherent-target use.

## Questions for Control / Analyst

- Should competent-reference, matched-simple-reduction, and source-cluster inference requirements be persisted as an explicit claim-type-specific external-validation schema rather than left only in narrative synthesis?
- When Analyst next consumes the fresh eligibility-history SUB and Audit R3, preserve canonical funnel metrics on reviewed objects only and keep C19-v4 exact PASS separate from programme-level `REDUCIBLE` novelty interpretation.
- Continue reporting the first READY object with its pre-outcome readiness rationale so the READY→PRE_FORMAL semantics can be audited empirically.
