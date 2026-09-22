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

## Blind target selection

Before any current Control Brain, Evidence Analyst, MAIN/SUB, or Literature summary was read, the audit fixed H7 FORMAL-R2 `H7-FORMAL-R2-INPUT-SPLIT-BINDING-V1` as the target. The question was whether its proposed protected/untouched one-way FORMAL path could support confirmatory mechanism evidence.

Authoritative repository evidence inspected in Phase 1 included stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`, active H7 R2 at `a7a3c82416af5bd3c8bf3340cc9276f161ddb0d0`, R2/R1 contracts, the public world generator, R2 runner, R1 collector/scorer, current evidence/formal/sealed/freeze refs, relevant workflow state, and prior audit history only for dedupe.

Attack hypotheses were fixed as: reconstructible evaluation rows/targets; split identity without secrecy; scorer/evaluator leakage; target-derived endpoint computation before raw preservation; post-disclosure claim-capable implementation changes; hidden seed/task-label privilege; runtime/package/identity/no-clobber drift; and comparator/resource mismatch. H7 had not previously received a dedicated independent audit.

## Phase-1 findings

### 1. R2 is not an untouched holdout

R2 publishes exact evaluation seeds `8846030..8846285`, deterministic world assignment, 24 steps, and `split=test`. The repository world generator uses the seed to derive both episode observations and truth labels. Exact future evaluation rows and labels are therefore reconstructible without dispatching the official protected workflow.

This does not prove actual tuning. It does establish that `identity-bound`, `workflow-access-controlled`, and `information-level unexposed` are distinct properties. R2 cannot support the last property.

### 2. `target-blind raw` is target-derived correctness data

The R1/R2 `TargetBlindRawCollector` rejects keys named `score`, `decision`, `pass`, `fail`, and related final-decision vocabulary, but allows `baseline_correct` and `cut_correct`. The R2 runner creates those fields by comparing predictions with `example.belief_truth` before the raw file is closed and preserved.

The frozen scorer then computes episode accuracy/effect directly from those correctness bits, bootstraps the contrasts, and derives the decision. In other words, the raw object is **decision-blind**, but it is not target-blind or score-free. The runner has already evaluated the primary endpoint against targets before immutable preservation.

A static read-only data-flow reconstruction is enough to establish this; no experiment, workflow, rescore, or target materialization was performed by the auditor.

The auditability consequence is concrete: a later scorer receiving only correctness bits cannot independently verify whether those bits were correctly derived from predictions and truth. If the frozen result runner were buggy, the supposedly pre-score preserved raw would already contain the bug's target-derived endpoint values.

## Phase 2 — control-plane comparison

Only after Phase 1 was fixed, current strategy summaries were read. Literature R31 independently identified the reconstructible R2 holdout. Control R36 stopped before FORMAL identity and separated input identity/workflow access from information-level exposure. Evidence Analyst R76/R77 classified R2 as a stopped/quarantined FORMAL evidence surface and moved the same H7 object prospectively to R3. MAIN reconciled to the R3 preidentity lane; no one-way identity, STARTED marker, protected evaluation, result-bearing execution, official scoring, or scientific evidence exists.

The independently chosen target therefore remained valid and `blind_target_change_reason=null`.

At final repository refresh, R3 existed at `research/main-h7-formal-r3-unexposed-eval-runtime-r76-cycle9@325e93c62c1f79baa107b677a3dc881dc6f47ace`. Its contract correctly introduces a concealed post-final-binding evaluation commitment and exact runtime binding, and cycle 9 remains strictly preidentity/non-result-bearing. However, the R3 design still requires `target_blind_raw`. Because the result runner has not yet been materialized, this is the appropriate point to define that boundary literally rather than inherit R2 correctness-bit semantics.

## Classification

`CONFOUNDED`.

R2 cannot be an untouched confirmatory FORMAL surface because its target set is reconstructible, and its current raw-before-score implementation computes target-derived score-sufficient correctness values before immutable preservation. No existing H7 FORMAL evidence is invalidated because no such evidence exists. R2 should remain quarantined. R3 can close both defects prospectively before identity.

## Prospective discriminator

For R3, the strongest one-way boundary is: protected runner emits prediction/output/intervention metadata plus opaque row IDs only; no truth, target, `baseline_correct`, `cut_correct`, aggregate effect, or decision fields. Those exact prediction-raw bytes are immutably preserved first. Only then does a scorer receive the protected target mapping, recompute correctness from preserved predictions, bootstrap intervals, and derive the decision. A positive schema allowlist and a data-flow test should verify that changing the target sidecar cannot change prediction-raw bytes when the observations are fixed.

No Utility request was created because the active R3 lane already owns this integrity surface.

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
  authoritative_refs_inspected:
    - main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d
    - research/main-h7-formal-r2-input-split-r75-cycle8@a7a3c82416af5bd3c8bf3340cc9276f161ddb0d0
    - H7 R1/R2 contracts and runner/scorer source
    - evidence/* 5; formal/* 0; sealed/* 0; freeze/* 0
  attack_hypotheses:
    - reconstructible protected evaluation
    - split binding without secrecy
    - scorer/evaluator/target leakage
    - target-derived endpoint computation before preserve
    - post-disclosure claim-capable changes
    - hidden seed/task-label privilege
    - runtime/package/identity/no-clobber drift
    - baseline/resource mismatch
blind_target_change_reason: null
prospective_baselines_or_discriminators:
  - quarantine R2 unchanged
  - R3 pre-score raw contains predictions/outputs plus opaque IDs only
  - preserve prediction-raw before any scoring process sees target material
  - post-preserve scorer recomputes correctness from preserved predictions and protected targets
  - positive raw-schema allowlist plus target-sidecar independence data-flow test
  - retain concealed post-binding evaluation commitment and exact runtime binding
questions_for_evidence_analyst:
  - Define target-blind literally as no target-derived fields before preserve?
  - Require scorer-side recomputation of correctness from preserved predictions plus protected targets before FORMAL identity?
  - Treat this as preidentity integrity closure rather than a scientific H7 redesign?
questions_for_control_brain:
  - Distinguish prediction-raw/target-blind, target-derived-but-decision-blind, and scored/decision-bearing artifacts?
  - Block identity until preserve-before-score is data-flow verified rather than only key-name checked?
  - Keep R2 quarantined and make any raw-gate change only prospectively?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1-v1/C19-R1-v2/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - H7 PF-R1 no-rerun/no-rescore boundary
  - H7 R1/R2 historical contracts and development results
  - no R2 in-place evidence repair
  - no FORMAL identity/STARTED/protected evaluation/result-bearing execution/scoring/evidence by this role
  - no research merge, immutable-ref mutation, Utility execution, or scheduler change
utility_request_created: null
```
