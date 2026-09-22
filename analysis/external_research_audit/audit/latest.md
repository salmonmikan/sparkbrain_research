# INDEPENDENT_AUDITOR — H7 FORMAL confirmatory-integrity and raw-gate audit

- schema_version: `2`
- generation_id: `AUD-20260922T223000+0900-R7-H7-RAWGATE-6C8F21D4`
- produced_at: `2026-09-22T22:30:20+09:00`
- producer_run_id: `external-audit-20260922T223000+0900-R7-H7-6C8F21D4`
- authority_scope: `INDEPENDENT_AUDITOR_READ_ONLY_REPOSITORY_EVIDENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `AUD-20260922T103000+0900-R6-PD01-NULLREDUCTION-9C4A21E7`
- role: `INDEPENDENT_AUDITOR`
- schedule_slot: `22:30 JST`
- schedule_inference: `false`
- audit_classification: `CONFOUNDED`

## Phase 1 — blind target selection

Before reading current Control Brain, Evidence Analyst, MAIN/SUB, or Literature summaries, the audit fixed H7 FORMAL-R2 `H7-FORMAL-R2-INPUT-SPLIT-BINDING-V1` as the target, specifically whether the proposed one-way FORMAL path could support an untouched/protected confirmatory interpretation.

Repository-only attack hypotheses were: public reconstruction of evaluation rows/targets; `split=test` providing provenance but not secrecy; scorer/evaluator leakage; pre-preserve target-derived scoring hidden inside the result runner; post-disclosure claim-capable implementation changes; hidden seed/task-label privilege; package/runtime/identity drift; no-clobber/preserve-order failure; and ordinary-reduction/resource mismatch. The target was consequential because H7 is the active MECHANISM candidate and a future PASS would become one-way confirmatory mechanism evidence.

Prior audit history was read only for dedupe. H7 had not previously received a dedicated independent audit. The blind target was not changed.

## Repository evidence — R2 holdout is reconstructible

Stable `main` remained `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; authoritative `evidence/*` remained five objects and tag-form `formal/*`, `sealed/*`, and `freeze/*` remained empty. H7 R2 was preidentity only: no FORMAL identity, STARTED marker, result-bearing workflow, official score, or scientific evidence object existed.

R2 publicly fixes FORMAL evaluation seeds `8846030..8846285`, world assignment, `split=test`, and 24 steps. The repository generator deterministically derives the episode observations and truth labels from the public seed. Therefore exact future evaluation rows and targets can be reconstructed without touching the official protected evaluation workflow. This independently confirms that exact input identity/workflow access control is not the same property as information-level holdout non-exposure.

## New audit issue — the claimed `target-blind raw` is already target-derived score material

A separate source-level integrity problem was found in the R1/R2 one-way path. The `TargetBlindRawCollector` only rejects keys such as `score`, `decision`, `pass`, and `fail`; it permits `baseline_correct` and `cut_correct`. The R2 result runner computes those fields by comparing predicted labels against `example.belief_truth` before the raw file is closed and immutably preserved.

The frozen scorer then consumes `baseline_correct` and `cut_correct` directly: episode baseline accuracy and cut effect are means of those fields, and the bootstrap/decision path is computed from them. Thus the primary target comparison has already happened runner-side before preserve. The persisted object is **decision-blind**, but it is not literally target-blind or score-free: it contains target-derived, primary-endpoint-sufficient statistics.

This matters for independent auditability. If raw contains only correctness bits rather than pre-score predictions plus a separately protected target mapping, the post-preserve scorer cannot independently recompute whether each correctness bit was derived correctly. A frozen buggy runner could alter the primary endpoint before the supposedly raw preservation boundary while the later scorer would faithfully aggregate the altered bits.

No existing FORMAL evidence is invalidated because no H7 FORMAL result exists. The finding is prospective and should be resolved before any future one-way identity/result-bearing execution.

## Phase 2 — interpretation comparison

Only after the target and attack hypotheses were fixed, current control-plane summaries were read. Literature R31 independently identified the reconstructible R2 holdout. Control R36 separated exact identity, workflow access control, and information-level exposure and stopped before FORMAL identity. Evidence Analyst R76/R77 went further: R2 is stopped as the FORMAL evidence surface, preserved as development history, and H7 moved prospectively to R3 with concealed post-binding evaluation commitment and exact runtime binding. MAIN reconciled to that R3 authority; no result-bearing work or identity was authorized.

The blind target therefore remains unchanged (`blind_target_change_reason=null`). The control-plane response is directionally correct. The remaining issue is that the new R3 design still states `target_blind_raw_required` while preserving R1/R2 scientific semantics; because no R3 result runner exists yet, this is the right moment to make the raw boundary literal rather than inherit R2's correctness-bit behavior.

## Audit conclusion

`audit_classification = CONFOUNDED` for H7 FORMAL-R2 as an untouched confirmatory evidence surface.

Two independent confounds are present: the R2 evaluation target is publicly reconstructible before identity, and the current R1/R2 "target-blind raw" path performs target-derived correctness evaluation before immutable raw preservation. Neither creates a negative H7 scientific result, and neither invalidates consumed evidence because no H7 FORMAL evidence exists. R2 should remain quarantined/non-evidentiary, and R3 should close both integrity surfaces prospectively before identity.

No Utility request was created because the active R3 lane already owns this preidentity integrity surface.

## Knowledge-flow contract

```yaml
role: INDEPENDENT_AUDITOR
genuinely_new_information: true
affected_lines:
  - H7_FORMAL_R2_CONFIRMATORY_INTEGRITY
  - H7_FORMAL_R3_ONE_WAY_RAW_GATE
  - H7_TARGET_BLIND_RAW_SEMANTICS
  - H7_PRESERVE_BEFORE_SCORE_AUDITABILITY
  - PROGRAMME_EVIDENCE_INTEGRITY
novelty_or_reduction_impact: H7_R2_CONFIRMATORY_SURFACE_CONFOUNDED_AND_R3_RAW_GATE_MUST_SEPARATE_PREDICTION_RAW_FROM_TARGET_DERIVED_SCORING_NO_MECHANISM_NOVELTY_UPLIFT
audit_classification: CONFOUNDED
blind_target_selection:
  target: H7 FORMAL-R2 one-way confirmatory evidence surface and its untouched/protected interpretation
  attack_hypotheses:
    - public deterministic evaluation-target reconstruction
    - split binding without information-level secrecy
    - scorer/evaluator or target leakage
    - pre-preserve target-derived endpoint computation inside the runner
    - post-disclosure claim-capable implementation changes
    - hidden seed/task-label privilege
    - runtime/package/identity/no-clobber drift
    - baseline/resource mismatch
blind_target_change_reason: null
prospective_baselines_or_discriminators:
  - preserve R2 unchanged as non-evidentiary/quarantined history; do not rescue it
  - in R3, make protected runner raw contain model outputs/intervention metadata plus opaque row IDs only, not *_correct, target, truth, aggregate effect, or decision fields
  - immutably preserve those pre-score bytes before target material is available to any scoring process
  - only after preservation, let the scorer combine preserved predictions with the protected target mapping and recompute correctness, bootstrap intervals, and decision
  - use a positive raw-schema allowlist plus a data-flow test showing target-sidecar changes cannot alter prediction-raw bytes for fixed observations
  - keep concealed post-final-binding evaluation commitment and exact runtime binding already introduced by R3
questions_for_evidence_analyst:
  - Should R3 define target-blind literally as no target-derived fields, rather than merely no final decision token?
  - Before FORMAL identity, require the scorer to recompute correctness from preserved predictions plus protected targets instead of trusting runner-produced correctness bits?
  - Treat this as a preidentity integrity closure, not a scientific rerun or H7 mechanism change?
questions_for_control_brain:
  - Add a three-way distinction: prediction-raw/target-blind, target-derived-but-decision-blind, and scored/decision-bearing?
  - Block H7 one-way identity until the preserve-before-score boundary is verified at data-flow level, not only by forbidden field names?
  - Keep R2 quarantined and R3 prospective with no retrofit to consumed/frozen evidence?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1-v1/C19-R1-v2/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - H7 PF-R1 development result/raw and no-rerun/no-rescore boundary
  - H7 R1/R2 historical contracts/results as immutable development history
  - H7 R2 current branch and public evaluation surface must not be repaired in place for evidence
  - no FORMAL identity/STARTED/protected evaluation/result-bearing workflow/scientific scoring or preserve/evidence ref by this role
  - no research merge, immutable-ref mutation, Utility execution, or scheduler change
utility_request_created: null
```
