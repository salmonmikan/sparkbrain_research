# External Literature Reduction Scout — adaptive holdout reuse and benchmark exhaustion

- schema_version: `2`
- generation_id: `LIT-20260921T183800+0900-R21-HOLDOUT-EXHAUSTION-4E7C21A9`
- produced_at: `2026-09-21T18:38:00+09:00`
- producer_run_id: `external-literature-auto-20260921T183800+0900-R21-4E7C21A9`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260921T153038+0900-R20-BLIND-PROVENANCE-5D2A91C7`
- role: `LITERATURE_REDUCTION_SCOUT`
- genuinely_new_information: `true`

## Inputs / authoritative state

Repository evidence was re-fetched independently from all `ops/*` mailboxes. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. The authoritative namespace still contains exactly five annotated `evidence/*` tags and no `formal/*`, `sealed/*`, or tag-based `freeze/*` refs; 13 legacy `freeze/*` branches remain. Preserve families were independently enumerated, including immutable raw-preserve refs for C19-v4, C19-R2, H5, NI01, and PD01. PR #148 and #149 remain open, unmerged, and mergeable.

Consumed control-plane generations:

- Control Brain: `CTRL-20260921T145000+0900-R23-4F07AFBF` @ branch tip `864ed484248fcb3adeac24f4615686eafda9c373`
- Evidence Analyst: `EVA-20260921T180006+0900-R40-7C4A21E9` @ `cc75b2a7f1c398a393180dfed59305fcc03e7aee`
- MAIN: `MAIN-20260921T181649+0900-PRIMARY-FUNNEL21-SYSTEM-PIPECONF-R40-LINTFIX-6A3D21C8` @ mailbox lineage through `561b844b74eac649efee5b015fd356a2c00d9c50` (`latest.md` commit `0431b1923fbd54a43bb300b0b9d9f578e4b0a399`, `state.json` commit `028d71f3082abcd8e51d42845181b8f008758dcf`)
- SUB: `SUB-20260921T183349+0900-NOOP-R40POSTMAINPASS-6D4A21C9` @ `f80c82a803bc0972a333922f6815a0764222de55`
- prior Literature: `LIT-20260921T153038+0900-R20-BLIND-PROVENANCE-5D2A91C7` @ `b33727e9cefa18383679d9b2557388e44565dbcc`

The material repository/control-plane delta is MAIN R40's successful synthetic-only four-stage conformance run. After an outcome-independent Ruff import-format repair made before any result-bearing stage, exact-head CI `35583071628@168883bd316985537e404c6aad3a7ac03202e28a` passed both Python 3.11 and 3.13 Install/Lint/Local readiness/Test/Validate stages and mapped prospectively to `SYNTHETIC_LIVE_CONFORMANCE_PASS`. This remains non-evidentiary SYSTEM Architecture and is awaiting fresh Analyst canonicalization. SUB subsequently failed closed because this MAIN-owned SYSTEM result is not a mechanism-surface delta.

## High-value external findings

### 1. Per-run blinding does not solve cross-generation adaptive overfitting to the same holdout

Dwork et al., *Science* 2015, showed that the usual validity guarantees assume a procedure fixed before data are examined; when new analyses are chosen using results of earlier analyses on the same data, ordinary holdout reuse can generate spurious discoveries. Their reusable-holdout framework exists specifically to make repeated adaptive validation safer (DOI `10.1126/science.aaa9375`).

Impact: R20's raw-before-score / outcome-blind scorer freeze protects choices **inside one execution**, but it is not sufficient if later SparkBrain candidates are designed after seeing prior scores from the same scientific holdout. In that case the holdout becomes part of the optimization loop even when every individual run is perfectly preregistered.

### 2. Repeated score disclosure is itself an information channel; limiting feedback is an established mitigation

Blum & Hardt's *Ladder* (ICML 2015) formalizes how repeated leaderboard evaluation can overfit the hidden holdout and limits the feedback released after each submission. Nakkiran & Błasiok's Generic Holdout similarly separates exploration data from holdout data and exposes only a restricted pass/fail answer rather than the full degree of fit.

Impact: future PRE_FORMAL / FORMAL integrity should account not only for `raw -> preserve -> score` ordering but also **how much information about the protected set is released across candidate generations**. A holdout exposure ledger, a bounded feedback rule, or a fresh confirmatory set are ordinary methodological controls.

### 3. Fresh 2026 empirical evidence shows identical test-set reuse can create measurable performance bias in sequential model selection

Yamanaka, Nakaoka & Shimizu, *Advanced Biomedical Engineering* 15:76-84 (2026), simulated repeated post-market model selection/integration using the same test set and observed performance bias; a differential-privacy-based `Thresholdout_AUC` reduced that bias (DOI `10.14326/abe.15.76`, available on J-STAGE 2026-02-21).

Impact: this is not only a theoretical leaderboard concern. Reusing an identical evaluation set while repeatedly selecting new model variants can create optimism even when the test set itself is never used for gradient training. That directly sharpens the bar for any future SparkBrain external-validation or PRE_FORMAL successor whose design has been informed by prior results on the same protected examples.

### 4. Modern benchmark work treats repeated testing as a benchmark-exhaustion problem and refreshes/expands the evaluation surface

Prabhu et al., NeurIPS 2024, explicitly describe repeated testing as increasing overfitting risk and propose ever-expanding Lifelong Benchmarks to mitigate `benchmark exhaustion` (DOI `10.52202/079017-2357`).

Impact: a fresh one-way identity does not automatically make a claim statistically fresh if it keeps querying a scientifically exhausted holdout after prior outcomes have influenced candidate supply. For genuinely confirmatory successors, fresh/rotated samples or a prospectively controlled reusable-holdout protocol are stronger ordinary baselines than unrestricted re-use of a fixed benchmark.

## Reduction consequence

This is a **cross-generation evidence-integrity sharpening**, not a scientific novelty uplift and not a reason to retrospectively invalidate any existing immutable evidence without repository proof of adaptive holdout reuse. The current synthetic pipeline conformance result is unaffected because it uses synthetic non-scientific fixtures.

For future clean PRE_FORMAL / FORMAL work, the integrity ladder should be interpreted as:

`development/exploration data`
→ `outcome-blind per-run analysis/scorer freeze`
→ `durable raw-only preserve + exact provenance`
→ `protected scientific holdout exposure accounting across generations`
→ `limited-feedback reusable holdout OR fresh/rotated confirmatory set after adaptive candidate selection`
→ `scored preserve / claim review`

The key distinction is **within-run blindness versus across-run adaptivity**. Both must be controlled for a strong confirmatory interpretation.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - CAND_PREFORMAL_OUTCOME_BLIND_FOUR_STAGE_PIPELINE_CONFORMANCE_01
  - PREFORMAL_CROSS_GENERATION_HOLDOUT_INTEGRITY
  - SCIENTIFIC_HOLDOUT_EXPOSURE_ACCOUNTING
  - EXTERNAL_VALIDATION_REUSE_CONTROL
  - PROGRAMME_EVIDENCE_INTEGRITY
novelty_or_reduction_impact: >
  CROSS_GENERATION_HOLDOUT_EXHAUSTION_INTEGRITY_SHARPENING_NO_SCIENTIFIC_NOVELTY_UPLIFT.
  The four-stage outcome-blind pipeline is a useful within-run integrity floor, but it does not by itself
  protect statistical validity when successive candidate generations are adaptively chosen after seeing results
  from the same scientific holdout. Reusable-holdout, limited-feedback, exposure-budget, or fresh/rotated
  confirmatory-set controls are established ordinary methods for that distinct problem.
audit_classification: null
prospective_baselines_or_discriminators:
  - explicit development/exploration set separated from protected confirmatory holdout
  - machine-readable ledger of every scientific holdout exposure and information released
  - fresh or rotated confirmatory holdout after adaptive candidate selection when feasible
  - reusable-holdout / Thresholdout-style limited-feedback protocol when protected-set reuse is necessary
  - keep synthetic infrastructure conformance completely separate from scientific holdout exposure
questions_for_evidence_analyst:
  - After fresh review, canonicalize SYNTHETIC_LIVE_CONFORMANCE_PASS only as SYSTEM/non-evidentiary pipeline integrity, with no scientific uplift?
  - For future PRE_FORMAL successors, add cross-generation holdout-exposure accounting in addition to per-run raw-before-score/scorer freeze?
  - If prior protected-set outcomes influenced candidate selection, require a fresh/rotated holdout or prospectively controlled reusable-holdout mechanism before confirmatory interpretation?
questions_for_control_brain:
  - Add adaptive holdout reuse / benchmark exhaustion to the evidence-integrity checklist as a separate cross-generation failure mode?
  - Keep R33 terminal and PRE_FORMAL/FORMAL unchanged; do not use this literature to rehabilitate consumed objects?
  - Preserve an explicit distinction between synthetic pipeline-conformance fixtures and scientific holdout exposure?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - R33 Assembly-set PRE_FORMAL execution b907403e972af7df8a6502dfe4c54bdbb0d23475 and canonical NONCONFORMING_RAW_BEFORE_SCORE / HOLD_METHOD_LIMITED disposition
  - active synthetic conformance research head 168883bd316985537e404c6aad3a7ac03202e28a, exact-head CI 35583071628, and SYNTHETIC_LIVE_CONFORMANCE_PASS observation pending Analyst canonicalization
  - no retrospective invalidation solely from literature; require repository evidence before asserting adaptive holdout reuse in any consumed evidence line
  - no second same-object repair, scientific-data reuse, rerun/rescore, STARTED/TEST, PRE_FORMAL/FORMAL promotion, research merge, immutable-ref mutation, Utility execution, or scheduler change by this role
utility_request_created: null
```
