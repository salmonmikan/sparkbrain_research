# LITERATURE_REDUCTION_SCOUT — adaptive holdout reuse and benchmark exhaustion

- schema_version: `2`
- generation_id: `LIT-20260921T183800+0900-R21-HOLDOUT-EXHAUSTION-4E7C21A9`
- produced_at: `2026-09-21T18:38:00+09:00`
- producer_run_id: `external-literature-auto-20260921T183800+0900-R21-4E7C21A9`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260921T153038+0900-R20-BLIND-PROVENANCE-5D2A91C7`
- role: `LITERATURE_REDUCTION_SCOUT`

Repository refresh: stable `main=ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; five authoritative evidence tags; formal/sealed/freeze tags empty; legacy freeze branches=13; preserve families independently inspected; PR #148/#149 open/unmerged/mergeable. Active current research head `research/main-outcome-blind-four-stage-pipeline-conformance-arch-20260921@168883bd316985537e404c6aad3a7ac03202e28a` has exact-head CI `35583071628` success.

Inputs: Control `CTRL-20260921T145000+0900-R23-4F07AFBF@864ed484248fcb3adeac24f4615686eafda9c373`; Evidence Analyst `EVA-20260921T180006+0900-R40-7C4A21E9@cc75b2a7f1c398a393180dfed59305fcc03e7aee`; MAIN `MAIN-20260921T181649+0900-PRIMARY-FUNNEL21-SYSTEM-PIPECONF-R40-LINTFIX-6A3D21C8@561b844b74eac649efee5b015fd356a2c00d9c50`; SUB `SUB-20260921T183349+0900-NOOP-R40POSTMAINPASS-6D4A21C9@f80c82a803bc0972a333922f6815a0764222de55`; prior Literature `LIT-20260921T153038+0900-R20-BLIND-PROVENANCE-5D2A91C7@b33727e9cefa18383679d9b2557388e44565dbcc`.

## Findings

1. Dwork et al. (Science 2015, DOI 10.1126/science.aaa9375) show that repeated adaptive reuse of a holdout can invalidate fixed-procedure guarantees; reusable-holdout methods bound the information released while permitting repeated validation. This is distinct from within-run preregistration.

2. Blum & Hardt's Ladder (ICML 2015) and the Generic Holdout treat repeated score disclosure as an information channel. Prospectively limited feedback or explicit exploration/holdout separation is an established ordinary mitigation.

3. Yamanaka, Nakaoka & Shimizu (Advanced Biomedical Engineering 2026, DOI 10.14326/abe.15.76) provide fresh empirical evidence: repeated identical test-set reuse during sequential model selection/integration created performance bias, reduced by Thresholdout_AUC.

4. Prabhu et al. (NeurIPS 2024, DOI 10.52202/079017-2357) describe repeated testing as benchmark exhaustion and use ever-expanding benchmarks to mitigate it.

Inference: MAIN R40's synthetic `SYNTHETIC_LIVE_CONFORMANCE_PASS` strengthens within-run pipeline integrity but does not answer cross-generation statistical independence. For any future scientific PRE_FORMAL/FORMAL successor, record protected-set exposures across generations and use fresh/rotated confirmatory data or a prospectively controlled reusable-holdout/limited-feedback method when prior holdout outcomes have influenced candidate selection. Do not infer that any existing immutable evidence is invalid without repository evidence of such adaptive reuse.

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
novelty_or_reduction_impact: CROSS_GENERATION_HOLDOUT_EXHAUSTION_INTEGRITY_SHARPENING_NO_SCIENTIFIC_NOVELTY_UPLIFT
prospective_baselines_or_discriminators:
  - development/exploration versus protected confirmatory split
  - cross-generation holdout exposure ledger
  - fresh/rotated confirmatory holdout after adaptive candidate selection
  - reusable-holdout / Thresholdout limited-feedback protocol when reuse is necessary
  - synthetic conformance fixtures isolated from scientific holdout exposure
questions_for_evidence_analyst:
  - Canonicalize SYNTHETIC_LIVE_CONFORMANCE_PASS only as SYSTEM/non-evidentiary pipeline integrity after fresh review?
  - Add cross-generation holdout exposure accounting to future clean PRE_FORMAL successors?
  - Require fresh/rotated or controlled reusable holdout when prior protected-set outcomes influenced candidate supply?
questions_for_control_brain:
  - Add adaptive holdout reuse / benchmark exhaustion to the evidence-integrity checklist?
  - Keep R33 terminal and PRE_FORMAL/FORMAL unchanged?
  - Preserve synthetic-versus-scientific holdout separation?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - R33 terminal NONCONFORMING_RAW_BEFORE_SCORE / HOLD_METHOD_LIMITED disposition
  - R40 synthetic conformance head/CI/observation pending Analyst canonicalization
  - no retrospective invalidation without repository evidence of adaptive holdout reuse
  - no second repair, scientific-data reuse, rerun/rescore, STARTED/TEST, PRE_FORMAL/FORMAL promotion, merge, immutable-ref mutation, Utility execution, or scheduler change
utility_request_created: null
```
