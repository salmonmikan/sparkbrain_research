# SparkBrain External Research & Audit — Independent Audit Latest

Analysis time: 2026-09-19 10:32 JST
Role: `INDEPENDENT_AUDITOR`

## Phase ordering

`phase_ordering_confirmed: true`

The audit target and attack hypotheses were fixed from current repository evidence and prior audit history before reading Control Brain, Evidence Analyst, MAIN/SUB, or Literature summaries.

### blind_target_selection

- target: NI01 `ni01-no-ignition-selective-prediction-official-v1`, canonical terminal `FAIL_REDUCED_BY_CONFIDENCE_ABSTENTION`
- main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- exact package: `dbfe7469dbbbc1adbb00789ab382de892a1b3563`
- scientific-contract blob: `3dc90b08f85e0e7c459e0c17e86ab338901fd4c6`
- STARTED: `control/ni01-no-ignition-selective-prediction-started-v1-20260918@d3e4a5d6349e7e69f21ffc3554998aa72f1f9d3d`
- raw preserve: `8a39cf70e397bb7588f948910f01ec58672ac814`
- terminal evidence: `69aa785a48bbdb531229b7f71f7fa84a5fde9948`
- evidence tag: `evidence/ni01-no-ignition-selective-prediction-ni01-no-ignition-selective-prediction-official-v1`
- attacks fixed blind: authority/package drift; target/evaluator leakage; hidden world/task-label privilege; threshold/scorer drift; seed/world fragility; comparator observation/resource mismatch; absent-signal-versus-reduction semantics; claim-boundary overreach.
- why consequential: NI01 is used to reduce the native No-Ignition/selective-decision line to ordinary confidence abstention. A comparator with extra regime identity can make that mechanistic reduction claim stronger than the actual evidence.

`blind_target_change_reason: null`

## Repository-evidence audit

### Evidence integrity: `ROBUST_SO_FAR`

The no-retry STARTED marker binds the exact package and Evidence Analyst authority. The successful one-way workflow uses target-free DEV threshold derivation, target-blind TEST raw acquisition, immutable preserve, independent byte re-fetch/digest verification, then target materialization and deterministic scoring. The preserved manifest records 46,080 TEST steps, `targets_materialized: false`, and the exact source/package bindings. No post-START retuning, identity reuse, target-before-preserve scoring, or package drift was found.

Terminal statistics are contract-valid:

- candidate selective loss: `0.2119466145833332`
- comparator selective loss: `0.21146918402777773`
- effect `(comparator - candidate)`: `-0.00047743055555544517`
- 95% CI: `[-0.0024414062499999965, 0.0014756944444444355]`
- coverage guard: pass
- terminal class: `FAIL_REDUCED_BY_CONFIDENCE_ABSTENTION`

The frozen FAIL rule is satisfied because the 95% CI upper bound is below `0.005`.

### New issue: comparator receives explicit world identity that the candidate does not

The formal contract describes the comparator as receiving the same per-step LABELS probability vector, but also prospectively fits **one separate DEV threshold per world**. The exact raw manifest shows:

- `contradiction_world`: `0.4344505230131153`
- `delayed_evidence_world`: `0.43859092652956055`
- `reliability_world`: `0.43837666247277174`

The threshold spread is about `0.00414` confidence units. At TEST time the official runner indexes `thresholds[world]` and applies that threshold to each row.

By contrast, the candidate path creates the same reference brain for each episode and injects only the generated observation (`evidence_label`, strength, source/evidence IDs, sensor/object metadata). It does not pass the symbolic `world` identifier into SparkBrain. Thus the confidence comparator is not strictly information-privilege matched: it receives an oracle regime/task label used to choose its abstention policy, while the candidate must infer regime consequences only from observations/dynamics.

This is target-free and prospectively preregistered, so it is **not leakage or post-outcome tuning**. But it is hidden task-label privilege in the comparator. The three worlds are genuinely different generative regimes, and the terminal world effects are heterogeneous (`-0.00374349`, `+0.00745443`, `-0.00514323`), so the asymmetry cannot be dismissed from the summary alone.

The safe conclusion is therefore narrower:

> NI01 found no registered incremental native No-Ignition advantage over a **world-conditioned, coverage-matched confidence-abstention comparator**.

It does not yet establish equal-privilege reduction to a single ordinary confidence-abstention rule that sees only the same score vector.

### Secondary semantics: no positive-signal gate for mechanistic `REDUCED_BY_*`

NI01's FAIL taxonomy, like the previously audited PD01 taxonomy, does not separately require an absolute/prospective candidate-positive-signal gate before mechanistic `REDUCED_BY_*` language is armed. For NI01, the registered scientific question is itself incremental value over the comparator, so the terminal result validly supports **no registered incremental advantage**. It is still safer not to upgrade that to a stronger mechanism-equivalence statement, especially while comparator privilege is asymmetric.

### Read-only sensitivity limitation

A decisive post-hoc sensitivity would recompute the frozen TEST contrast using one global DEV-derived confidence threshold (or another threshold policy that does not receive world identity), while preserving all targets, raw predictions, loss, and bootstrap machinery. The immutable raw is preserved, but the GitHub connector could not stream the 12.8 MB JSONL in this run, so this sensitivity was not recomputed here. Canonical evidence must not be rescored or relabeled; any such calculation is diagnostic only.

## Phase-2 comparison

After blind selection was fixed, current control-plane summaries were read. Control Brain already requires symmetric privilege for future reduction claims and explicitly requested a read-only NI01 absent-signal-versus-reduction audit. Evidence Analyst currently summarizes NI01 as “no registered incremental native advantage over matched confidence abstention.” MAIN/SUB remain architecture/testbed HOLD/no-op; newest Literature concerns future lineage admission and does not alter NI01 evidence.

The new audit finding sharpens the Evidence Analyst wording: “matched” is accurate for coverage and score-vector source, but **not for regime-information privilege** because the comparator is keyed by exact world identity.

## Audit classification

`WEAKENED`

The canonical terminal token and one-way evidence integrity remain valid. The mechanistic/equal-privilege reduction interpretation is weakened by a prospectively registered but asymmetric world-label privilege. No positive NI01 novelty evidence is restored.

## Knowledge-flow contract

```yaml
role: INDEPENDENT_AUDITOR
genuinely_new_information: true
affected_lines:
  - NI01_H4
  - PROGRAMME_NOVELTY
  - FUTURE_REDUCTION_TAXONOMY
  - COMPARATOR_PRIVILEGE_DOCTRINE
novelty_or_reduction_impact: >
  NI01_CANONICAL_FAIL_VALID; NO_REGISTERED_INCREMENTAL_NATIVE_ADVANTAGE_OVER_WORLD_CONDITIONED_CONFIDENCE_ABSTENTION;
  EQUAL_PRIVILEGE_MECHANISTIC_REDUCTION_NOT_ESTABLISHED; NO_NOVELTY_SUPPORT_RESTORED.
audit_classification: WEAKENED
blind_target_selection:
  target: NI01 official-v1 terminal FAIL_REDUCED_BY_CONFIDENCE_ABSTENTION
  selected_before_control_plane_summaries: true
  authoritative_refs:
    - main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d
    - exact package@dbfe7469dbbbc1adbb00789ab382de892a1b3563
    - STARTED@d3e4a5d6349e7e69f21ffc3554998aa72f1f9d3d
    - raw preserve@8a39cf70e397bb7588f948910f01ec58672ac814
    - terminal evidence@69aa785a48bbdb531229b7f71f7fa84a5fde9948
  attack_hypotheses:
    - authority/package drift or leakage
    - hidden world/task-label privilege
    - threshold/scorer drift
    - seed/world fragility
    - observation/resource mismatch
    - absent-signal versus reduction conflation
    - claim-boundary overreach
  why_consequential: NI01 closes the native No-Ignition/selective-decision mechanism line via an ordinary-confidence interpretation.
blind_target_change_reason: null
prospective_baselines_or_discriminators:
  - never rerun, retune, rescore, relabel or reopen canonical NI01
  - diagnostic-only read-only sensitivity with one global DEV-derived threshold that does not use world identity
  - future comparators must declare every task/regime identifier and match candidate information privilege
  - future mechanistic REDUCED_BY_* contracts should require a prospectively fixed positive candidate-signal gate where scientifically meaningful
questions_for_evidence_analyst:
  - Should NI01 synthesis say “world-conditioned coverage-matched confidence abstention” rather than simply “matched confidence abstention”?
  - Can a read-only global-threshold sensitivity be computed from immutable NI01 raw without changing canonical evidence?
  - Should future comparator contracts treat regime/task IDs as explicit privilege that must be matched or justified?
questions_for_control_brain:
  - Count NI01 as no registered incremental native advantage, but not yet equal-privilege mechanistic reduction?
  - Add explicit task/regime-label privilege to the programme-wide symmetry gate?
  - Keep architecture/testbed HOLD unchanged because this audit restores no positive NI01 signal?
must_not_change_frozen_or_consumed:
  - ni01-no-ignition-selective-prediction-official-v1
  - exact package dbfe7469dbbbc1adbb00789ab382de892a1b3563
  - scientific-contract blob 3dc90b08f85e0e7c459e0c17e86ab338901fd4c6
  - STARTED control/ni01-no-ignition-selective-prediction-started-v1-20260918
  - raw preserve 8a39cf70e397bb7588f948910f01ec58672ac814
  - terminal evidence 69aa785a48bbdb531229b7f71f7fa84a5fde9948 and evidence tag
  - canonical NI01 statistics and FAIL_REDUCED_BY_CONFIDENCE_ABSTENTION token
  - all other consumed C19/R1/R2/PD01/H5/A01/RV01/RV02/CX identities and immutable evidence
```
