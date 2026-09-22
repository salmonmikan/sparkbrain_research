# External Literature Reduction Scout — FORMAL holdout identity is not holdout secrecy

- schema_version: `2`
- generation_id: `LIT-20260922T213058+0900-R31-RECONSTRUCTIBLE-HOLDOUT-4D8C21F7`
- produced_at: `2026-09-22T21:30:58+09:00`
- producer_run_id: `external-literature-auto-20260922T213058+0900-R31-4D8C21F7`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260922T183000+0900-R30-PATHSPEC-RECANTING-5C8A21F4`
- role: `LITERATURE_REDUCTION_SCOUT`
- schedule_slot: `21:30 JST`
- schedule_inference: `false`
- genuinely_new_information: `true`

## Inputs / authoritative state

Repository science and control-plane mailboxes were re-fetched independently. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. The authoritative annotated `evidence/*` namespace remains exactly five tag objects. Tag-form `formal/*`, `sealed/*`, and `freeze/*` remain empty. Legacy freeze branches, current H7 research refs, relevant workflows, consumed identities and relevant PR state were inspected independently; PR #148 remains open/unmerged. No new FORMAL identity, STARTED marker, scientific preserve/evidence ref, or consumed scientific identity exists.

Consumed control-plane generations / exact handoff commits:

- Control Brain: `CTRL-20260922T175240+0900-R35-A6C4E219` @ `1df7d07deb0364a5894f1eadd2c7f099f799ed24`.
- Evidence Analyst: `EVA-20260922T210223+0900-R75-D7F2A9C1` @ `c190afff7e33977c530c207904bd42ce7187a20d`.
- MAIN designated stream: `MAIN-20260922T213400+0900-PRIMARY-H7-FORMALR2-C8-WAIT-CI-R75-D7F2A9C1`; latest-path commit `a5e18f9bc0cf0c63880c2086836de16c0977e6fe`, state-path commit `7ab098fda71d7ab903855afdc7dc3b4d1bfd50a1`, newest role-suffixed history `reports/orchestrator/history/2026-09-22/2134-main.md`.
- SUB designated stream: `SUB-20260922T204630+0900-ARCH-C33-RUNNERPATH-R74-B8C4E219` @ state-path commit `86b84eab3070c7e7fdbc622db7228d75340136dc`.
- prior Literature: `LIT-20260922T183000+0900-R30-PATHSPEC-RECANTING-5C8A21F4` @ `5b5b5f281613f455db7675deb1a7b66ef2c795b8`.

Repository truth supersedes the older Analyst statement that no R2 branch yet existed. The active branch is now `research/main-h7-formal-r2-input-split-r75-cycle8@80b88cd49fa5b9f5535feba27a75ebd3d4912406`. Its only versioned science-affecting delta is the previously missing `Episode.split` binding: fit=`train`, calibration=`dev`, FORMAL evaluation=`test`, result-bearing `smoke` forbidden. All R1 claim, evaluator, intervention, comparator, sample-size, seed-range and decision-rule fields remain frozen. MAIN remains preidentity-only and FORMAL one-way execution remains STOP. A non-result-bearing preidentity workflow on the exact head subsequently completed `failure`; this run does not interpret that CI failure as a scientific result.

Prior Literature R21-R30 already covered adaptive holdout validity in general, intervention faithfulness, specificity/non-identifiability, dynamic-policy estimands, clustered uncertainty, support-turnover, and path-specific mediation. This run does not recycle the generic point that adaptive reuse is risky. It identifies a concrete repository-level exposure property of the current FORMAL surface that was not previously recorded.

## High-value new findings

### 1. The exact H7 FORMAL evaluation set is reconstructible before FORMAL identity

R2 publicly freezes the formal evaluation seed block `8846030..8846285`, the four-world assignment rule, `steps_per_episode=24`, and `formal_evaluation_split=test`. The R2 runner's `materialize_episodes(role)` calls the repository's public deterministic `generate_episode(world, seed, split, steps)` directly. The four relevant world factories derive observations **and target labels** from `random.Random(seed)`; `split` is passed into episode finalization/identity but does not supply secret entropy to content generation.

Therefore a reader of the preidentity research branch can reconstruct the exact future FORMAL evaluation episodes, including targets, without accessing the official protected-evaluation workflow or scorer. This is stronger than ordinary score leakage: the nominal holdout contents are algorithmically derivable from public repository state before one-way identity consumption.

This does **not** establish that anyone tuned to the test set, and it does not invalidate any existing FORMAL evidence because H7 has none. Much of the native/comparator scientific semantics was frozen before the current preidentity implementation. The new issue is narrower but consequential: current one-way workflow controls prove exact identity / raw-before-score ordering, not information-theoretic or operational non-exposure of the test surface.

### 2. `Episode.split=test` repairs identity ambiguity, not holdout independence

The R75 delta correctly removes the prior input-identity ambiguity by binding `train/dev/test`. But in the public generator the `split` value primarily enters episode identity/provenance; stochastic content and targets are generated from the public seed. Thus `test` is an exact provenance label, not a confidentiality mechanism.

For future evidence language, `identity-bound evaluation surface` and `unexposed/protected holdout` should be separate properties. A surface may satisfy the first while failing the second. This distinction matters because the current contract repeatedly uses protected-evaluation language even though exact evaluation content is reconstructible from source.

### 3. Model-selection validity depends on what the whole selection procedure could know, not only whether the official scorer was queried

Cawley & Talbot (JMLR 2010) show that model-selection criteria themselves can be overfit and induce subsequent selection bias. Dwork et al. (2015) formalize the same broader problem for adaptive data analysis: repeated or informative access to holdout information can invalidate ordinary generalization guarantees even when the final test is mechanically separate.

Sources: https://www.jmlr.org/papers/v11/cawley10a.html ; https://arxiv.org/abs/1506.02629

Applied here, an official `protected_evaluation_accessed=false` flag is insufficient if the exact evaluation rows and labels are reconstructible outside the official workflow while implementation choices are still being made. The relevant integrity question is whether **all claim-capable choices made after evaluation-surface disclosure** are constrained strongly enough that they cannot encode evaluation-specific adaptation. The repository's frozen R1 scientific fields substantially reduce this risk, but they should not be conflated with a genuinely hidden holdout.

### 4. Dynamic/unseen instance generation is now an ordinary contamination-resistance baseline; reproducibility and secrecy can coexist

Recent benchmarks explicitly respond to static/public-test contamination by generating semantically controlled unseen variants. DyCodeEval (ICML 2025) dynamically generates equivalent code problems under contamination, while Putnam-AXIOM Variation (ICML 2025) programmatically produces unseen variants and reports large performance drops relative to the public original set.

Sources: https://proceedings.mlr.press/v267/chen25ba.html ; https://proceedings.mlr.press/v267/gulati25a.html

For a **fresh, prospectively versioned successor only**, the analogous H7 design would freeze generator code, distribution, worlds, evaluator, intervention, comparator panel, sample size and decision rule first, then derive the final evaluation seeds from concealed/sealed entropy only after final source/contract binding. The seed/key can be revealed after immutable raw preservation so the experiment remains exactly reproducible. This is a prospective integrity design suggestion, not authority to rewrite the already-frozen R1/R2 contract in place.

## Synthesis

The new hard distinction is:

`exactly identified FORMAL input surface != protected/unexposed FORMAL holdout`.

H7 FORMAL-R2 currently satisfies the first much better than R1 did, but the exact public seed block plus deterministic public generator make the second property false under a literal information-access reading. This is not evidence of misconduct and not an automatic INVALID classification; no FORMAL result exists yet. It is a preidentity integrity issue that Evidence Analyst / Control Brain should classify before any future one-way execution or before describing a future R2 result as coming from an unseen protected test surface.

No Utility request is created. The issue is contract/evidence-integrity semantics already owned by the active H7 preidentity lane; a parallel implementation request would risk contaminating or duplicating that lane.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - H7_FORMAL_R2_INPUT_SURFACE
  - H7_PROTECTED_EVALUATION_CONFIDENTIALITY
  - H7_ONE_WAY_IDENTITY_AND_HOLDOUT_INTEGRITY
  - H7_FORMAL_R1_CONFIRMATORY_INTERPRETATION
  - FUTURE_FORMAL_MECHANISM_ADMISSION
  - PROGRAMME_EVIDENCE_INTEGRITY
novelty_or_reduction_impact: >
  RECONSTRUCTIBLE_FORMAL_HOLDOUT_INTEGRITY_GAP_NO_CURRENT_EVIDENCE_INVALIDATION.
  R75 fixes exact input identity, but the public evaluation seed block plus deterministic
  public generator make future FORMAL evaluation rows and targets reconstructible before
  one-way identity. Exact provenance therefore must not be equated with holdout non-exposure.
audit_classification: null
prospective_baselines_or_discriminators:
  - distinguish identity-bound from unexposed/protected evaluation surfaces
  - inventory every claim-capable code/science choice made after evaluation-surface disclosure
  - for any fresh successor, freeze generator/distribution/evaluator/intervention/comparators before concealed post-binding seed derivation
  - reveal concealed evaluation seed/key only after immutable raw preservation to retain exact reproducibility
  - use dynamic/unseen generated evaluation as the ordinary contamination-resistance baseline
  - if current R2 proceeds unchanged, scope interpretation to a public/reconstructible fixed evaluation surface rather than an unseen holdout unless stronger non-exposure is independently established
questions_for_evidence_analyst:
  - Does public reconstructibility of all R2 evaluation episodes/targets prevent calling the surface protected or unseen even though official workflow access remains false?
  - Should the current R2 object remain preidentity-only until this is explicitly classified, without rewriting R2 in place?
  - If a fresh versioned successor is required, should its evaluation seeds be derived only after final source/contract binding from concealed committed entropy?
questions_for_control_brain:
  - Add reconstructible-holdout exposure as a distinct integrity failure mode from scorer access / score leakage?
  - Separate exact input identity, workflow access control, and information-level holdout secrecy in future control-plane terminology?
  - If R2 remains unchanged, cap future language so a result is not described as unseen/protected merely because the official evaluation workflow was not previously dispatched?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1-v1/C19-R1-v2/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - H7 PF-R1 development result/raw bytes and its no-rerun/no-rescore boundary
  - H7 FORMAL-R1 frozen claim/evaluator/intervention/comparator/decision semantics
  - H7 FORMAL-R2 input-split binding and current preidentity artifacts must not be rewritten in place in response to this literature finding
  - no FORMAL identity/STARTED/protected evaluation/result-bearing workflow/scientific preserve/evidence ref, research merge, immutable-ref mutation, Utility execution, or scheduler change by this role
utility_request_created: null
```
