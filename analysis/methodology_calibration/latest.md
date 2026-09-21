# SparkBrain Methodology Calibration Audit — 2026-09-21 11:22 JST

schema_version: `2`  
generation_id: `METHCAL-20260921T112242+0900-R34-9C4E2A71`  
produced_at: `2026-09-21T11:22:42+09:00`  
producer_run_id: `methodology-calibration-auto-20260921T112242+0900-R34-9C4E2A71`  
authority_scope: `METHODOLOGY_ADVISORY_ONLY`  
supersedes_generation_id: `METHCAL-20260921T102100+0900-R33-7B2E4C91`

## Run disposition

**`MATERIAL_CALIBRATION_UPDATE`**

## Overall classification

**`MIXED_CALIBRATION`**.

Funnel-v2.1 admission semantics improved materially: the programme has now observed its first Analyst-authoritative `READY -> PRE_FORMAL` transition, and it is correctly based on development/test readiness before the intervention outcome. However, the first live PRE_FORMAL execution also exposes a non-negotiable hard-floor implementation defect: the execution harness calculates `D_uniform`, `D_balanced`, perturbation-footprint support, and terminal classification in the same process before writing the combined result artifact. There is no separately preserved raw-only package before those scores/classification are computed. The Actions artifact is uploaded only after the harness completes. This does not justify rerunning, retuning, repairing, rescoring, or retrospectively changing the consumed object; it requires a prospective execution-pipeline correction for future PRE_FORMAL objects.

## Fresh independent reconstruction

Prior Methodology R33 was read first. Stable `main` was independently re-fetched at `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; authoritative annotated refs remain `evidence/*=5`, `formal/*=0`, `sealed/*=0`, tag-based `freeze/*=0`.

Designated Control remains `CTRL-20260921T085000+0900-R21-4F7C2A91@49ac783b5640b8250c19133f8842f0bf49867e8f`. Fresh designated Evidence Analyst is `EVA-20260921T105950+0900-R33-5A8C31E7@f22b345bceab464ac0fd593c11a7b6b99742af4f`. Analyst canonical funnel is `27/27` complete, `MECHANISM=13 / SYSTEM=14`, PRE_FORMAL eligible=`1`, READY=`1`, with the current object prospectively limited to `claim_ceiling=MECHANISM`.

Evidence Analyst R33 explicitly states that READY means the next PRE_FORMAL test is completely specified and informative, not that the candidate already defeated comparator/reduction/falsifier. The current object moved from `eligible=true / NOT_READY` to `eligible=true / READY` only after source/package/runtime inputs, four surfaces, comparator distributions, balance variables, equal privilege, endpoint, perturbation-footprint support, resource bound, and falsifier were fixed without intervention outcome.

MAIN then acquired the R33 PRE_FORMAL lease. The scientific binding at `14999b...`/execution head `b907403...` fixes `main@ebed6ab...`, Python `3.11.13`, package `0.3.2.dev0`, contract `52e142...`, surfaces `1701..1704`, deterministic control construction, equal privilege, endpoint/support logic, and terminal mapping. A pre-outcome packaging commit `a6f445...` only renamed the unchanged harness from `.py` to `.py.txt` and adjusted the workflow path; it changed zero harness lines. Workflow run `35554203269` succeeded, including exact source/contract ancestry verification, and uploaded artifact `10618883581` with digest `sha256:4cb9e43f7e4af1e85a8468462e34d896e51d7500aebec8e2db4d69886f290472`.

The hard-floor defect is localized but material. The harness computes the raw episode outcomes and then, before writing `preformal-result.json`, computes the two discriminators, perturbation-footprint envelope/support, and `_classify_surface`; only after terminal selection does it write/print the combined result. The workflow uploads that combined file after the execution step. Therefore `raw-before-score` is not implemented as a two-stage preserved raw -> fixed scorer pipeline. The uploaded artifact is digested but retention-limited, and no fresh immutable raw-preserve anchor is yet present in the designated Analyst authoritative refs.

## Funnel v2.1 mandatory audit

1. `claim_ceiling` current-object semantics: **KEEP**. Current object is prospectively MECHANISM; no permanent topic/prestige relabeling observed.
2. completed SYSTEM -> same-object MECHANISM upgrade: **KEEP**. No such upgrade observed.
3. `preformal_eligible` vs READY: **KEEP**. The same object was eligible while NOT_READY, then became READY after test-development choices closed.
4. READY semantics: **KEEP**; `HIDDEN_SECOND_FORMAL_GATE=false`. This first live READY transition occurred before intervention outcome and did not require prior comparator/reduction/falsifier victory.
5. HOLD multidimensional model: **KEEP**. Producer enum conformance remains a separate `CLARIFY` watchpoint.
6. MAIN MECHANISM priority / SYSTEM-priority exception: **KEEP**. Current MAIN object is MECHANISM; genuine SYSTEM-over-comparable-MECHANISM exception remains unobserved.
7. `NO_COHERENT_MECHANISM_TARGET`: **KEEP**. No current exception; prior episodes closed when fresh coherent mechanism work emerged.
8. theory-backward quality: **KEEP**. Current mechanism route is falsifiable and not a relabeled SYSTEM question.
9. SYSTEM value: **KEEP**. SYSTEM architecture/contract objects remain independently useful and terminal where appropriate.
10. PRE_FORMAL/PASS reachability: **PRE_FORMAL_REACHED_BUT_PIPELINE_INTEGRITY_DEFECT_BLOCKS_CLEAN_PASS_INFERENCE**.
11. classification-completeness gating: **KEEP**. Policy conclusions remain based on Analyst-reviewed `27/27`; the post-R33 PRE_FORMAL result is not yet a fresh canonical Analyst disposition.
12. first READY -> PRE_FORMAL empirical semantics: **KEEP**. It is directly consistent with development readiness rather than prior success.

## Material gate classifications

- hard-integrity policy itself: **`KEEP`** — it must not be relaxed.
- first Analyst-authoritative READY -> PRE_FORMAL transition: **`KEEP`** (was `INSUFFICIENT_EVIDENCE`).
- `preformal_eligible` / READY separation: **`KEEP`**, now empirically stronger.
- READY development-readiness semantics: **`KEEP`**, now empirically observed.
- `preformal_raw_before_score_execution_order`: **`TIGHTEN`**. Future PRE_FORMAL must emit a raw-only package before any score/terminal computation.
- `preformal_preserve_then_score_pipeline`: **`TIGHTEN`**. Fixed scorer must consume the exact preserved raw blob/digest, not in-memory observations that have not yet been preserved.
- `preformal_immutable_evidence_durability`: **`TIGHTEN`**. A retention-limited Actions artifact is useful transport but is not a substitute for the programme's durable raw-preserve anchor if the result will be interpreted scientifically.
- exact source/package/runtime/input binding: **`KEEP`**. The live workflow verified source/contract ancestry and no `src/`/`pyproject.toml` drift; runtime matched the frozen binding.
- pre-outcome mechanical packaging repair: **`KEEP`**. The `.py` -> `.py.txt` move was zero-content and before outcome.
- no silent post-outcome repair: **`KEEP`**; no repair after the PRE_FORMAL outcome has been observed in the current authoritative history.
- causal comparator equivalence standard: **`SPLIT_BY_CLAIM_TYPE`**, unchanged.
- equal-privilege comparator / ordinary-reduction-first / claim-type separation: **`KEEP`**.
- producer Funnel-v2.1 HOLD enum conformance: **`CLARIFY`**, unchanged pending a fresh producer demonstration.
- first genuine SYSTEM-priority exception: **`INSUFFICIENT_EVIDENCE`**.
- external-validation competent reference, relevant simple state-machine reduction, shared-source clustered inference, and legacy Top-k sparse-support: **`TIGHTEN`**, unchanged.

## Calibration dimensions

`gate_drift`: low in scientific semantics; material execution-order nonconformance in PRE_FORMAL plumbing.  
`justification_trace`: strong.  
`false_positive_control`: scientifically strong comparator/terminal design, but raw-before-score ordering weakens auditability of first PRE_FORMAL execution.  
`false_negative_risk`: do not respond by requiring prior scientific success for READY or by rerunning the current object; fix only future execution plumbing.  
`duplicate_guards`: none material.  
`moving_goalposts`: `LOW`; the fixed terminal map was used and no outcome-responsive redesign is observed.  
`pass_reachability`: `PRE_FORMAL_REACHED_BUT_FUTURE_PASS_REQUIRES_HARD_FLOOR_PIPELINE_CONFORMANCE`.  
`comparator_calibration`: `HEALTHY_CLAIM_TYPE_SPLIT_WITH_PROSPECTIVE_EQUAL_PRIVILEGE`.  
`signal_before_reduction`: healthy.  
`claim_type_separation`: healthy set/coalition MECHANISM ceiling.  
`research_worthiness_vs_novelty`: healthy.  
`external_calibration`: unchanged from R33.  
`opportunity_cost`: acceptable.  
`mechanism_supply_health`: `QUALITY_FLOOR_HEALTHY_M13_S14_READY1_PRE_FORMAL_REACHED_SMALL_N`.  
`funnel_observability`: `GOOD_27_OF_27_CANONICAL_PLUS_POST_ANALYST_PREFORMAL_RESULT_PENDING_REVIEW`.  
`preformal_gate_calibration`: `READY_SEMANTICS_VALIDATED_EXECUTION_EVIDENCE_ORDERING_NEEDS_TIGHTENING`.

## Remaining defects / watchpoints

The primary defect is not the readiness bar; it is PRE_FORMAL evidence ordering. Future PRE_FORMAL workflows should be mechanically split: (1) generator writes raw observations only; (2) raw package is durably preserved with exact source/package/runtime/input metadata and digest; (3) only then does a fixed scorer read that preserved blob and derive discriminators/terminal state; (4) scorer output is separately preserved. The scorer must have no ability to change target/comparator selection after raw preservation.

The current R33 result must not be rerun or repaired under the same object merely to fix this methodology defect. Control/Analyst should explicitly adjudicate its integrity status under the already-existing hard floor, using the preserved run/artifact as historical calibration evidence. This audit does not rescore, invalidate, upgrade, or dispatch any science.

Producer HOLD enum conformance remains `CLARIFY`. First genuine SYSTEM-over-comparable-MECHANISM exception remains unobserved.

## Prospective recommendations

Keep READY semantics exactly as R33 used them. For every future PRE_FORMAL object, require a raw-only immutable-preserve stage before any scoring or terminal classification. Bind scorer version/hash and make it consume only the exact preserved raw digest. Preserve the generator/scorer separation even for deterministic fixed formulas; determinism is not a substitute for raw-first evidence ordering.

Do not rerun the current PRE_FORMAL object to obtain a cleaner pipeline. Do not change its comparator, support envelope, surfaces, endpoint, or terminal mapping after outcome. Await fresh Analyst/Control integrity adjudication and use this run only as a calibration example until that occurs.

## Utility request

None created. The live first PRE_FORMAL rollout already provides higher-information methodology evidence than a synthetic probe.

## Hard-integrity-floor confirmation

**POLICY CONFIRMED / IMPLEMENTATION NONCONFORMANCE FOUND. DO NOT RELAX.** Exact source/package/runtime/input binding and prospective terminal mapping were strong, but `raw-before-score` is not implemented in the live R33 PRE_FORMAL harness, and durable immutable raw-preserve-before-scoring is not demonstrated. Prospective correction is required; retrospective rerun/repair is forbidden.

## Current inputs / authoritative refs

- stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- previous Methodology `METHCAL-20260921T102100+0900-R33-7B2E4C91@27c6d7e7464b322267cb955ebc4914b2e8f60563`
- Control `CTRL-20260921T085000+0900-R21-4F7C2A91@49ac783b5640b8250c19133f8842f0bf49867e8f`
- Evidence Analyst `EVA-20260921T105950+0900-R33-5A8C31E7@f22b345bceab464ac0fd593c11a7b6b99742af4f`
- MAIN lease `MAIN-20260921T111650+0900-PRIMARY-FUNNEL21-PREFORMAL-ASMSET-R33-4A7C91E2@96b437574d9a5e06472511773337ef2e0377285f`
- scientific source `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- prospective contract `52e14294d8e413a95c1dad387104bdeaa4468d39`
- PRE_FORMAL execution head `b907403e972af7df8a6502dfe4c54bdbb0d23475`
- PRE_FORMAL workflow run `35554203269=success`; artifact `10618883581`; digest `sha256:4cb9e43f7e4af1e85a8468462e34d896e51d7500aebec8e2db4d69886f290472`
- authoritative tags independently re-fetched: `evidence/*=5`; `formal/*=0`; `sealed/*=0`; tag-based `freeze/*=0`

## Confidence

**HIGH** on the first READY-transition finding and the raw-before-score implementation defect. **MODERATE** on the eventual admissibility of the already-produced development result until fresh Control/Analyst integrity adjudication; no retrospective action is recommended here.

## Questions for Control / Analyst

- Explicitly adjudicate the R33 PRE_FORMAL result against the pre-existing `raw-before-score` and durable preserve requirements without rerunning or repairing the object.
- For future PRE_FORMAL, require `raw generator -> immutable preserve/digest -> fixed scorer -> scored preserve` as a machine-checkable sequence.
- Keep READY as development/test readiness; do not turn this plumbing defect into a hidden requirement for prior scientific success.
- Keep the current claim ceiling and terminal/comparator contract frozen; no same-object rescue after outcome.
- Continue classification-completeness gating and keep the post-R33 result outside canonical conversion conclusions until fresh Analyst review.
- Preserve opportunity-local no-target accounting and prospective SYSTEM-priority exceptions unchanged.
