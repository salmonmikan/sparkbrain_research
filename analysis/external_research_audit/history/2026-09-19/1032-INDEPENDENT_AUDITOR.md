# SparkBrain Independent Audit — 2026-09-19 10:32 JST

Role: `INDEPENDENT_AUDITOR`

## Phase ordering

`phase_ordering_confirmed: true`

Blind target was fixed from repository evidence before reading Control Brain, Evidence Analyst, MAIN/SUB, or Literature summaries.

### blind_target_selection

- target: NI01 `ni01-no-ignition-selective-prediction-official-v1`, terminal `FAIL_REDUCED_BY_CONFIDENCE_ABSTENTION`
- main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- exact package: `dbfe7469dbbbc1adbb00789ab382de892a1b3563`
- scientific-contract blob: `3dc90b08f85e0e7c459e0c17e86ab338901fd4c6`
- STARTED: `d3e4a5d6349e7e69f21ffc3554998aa72f1f9d3d`
- raw preserve: `8a39cf70e397bb7588f948910f01ec58672ac814`
- terminal evidence: `69aa785a48bbdb531229b7f71f7fa84a5fde9948`
- attacks: authority/package drift; target/evaluator leakage; hidden world/task-label privilege; threshold/scorer drift; seed/world fragility; comparator observation/resource mismatch; absent-signal-versus-reduction semantics; claim-boundary overreach.

`blind_target_change_reason: null`

## Repository evidence

The one-way chain remains integrity-valid. STARTED is no-retry and binds the exact package and Analyst authority. The successful formal workflow derives thresholds target-free on DEV, acquires target-blind TEST raw, preserves and independently re-fetches it, then materializes TEST targets and scores deterministically. The raw manifest records 46,080 steps and `targets_materialized: false`. No post-START mutation, target-before-preserve scoring, or identity reuse was found.

Canonical terminal statistics remain:

- candidate loss `0.2119466145833332`
- comparator loss `0.21146918402777773`
- effect `(comparator - candidate)` `-0.00047743055555544517`
- 95% CI `[-0.0024414062499999965, 0.0014756944444444355]`
- coverage guard `true`
- terminal `FAIL_REDUCED_BY_CONFIDENCE_ABSTENTION`

The frozen classification is contract-valid and must not be changed.

## New audit issue — world/task-label privilege

The confidence comparator is not strictly information-privilege matched to the candidate. The formal protocol derives **one threshold per world**, and the preserved manifest records:

- contradiction: `0.4344505230131153`
- delayed evidence: `0.43859092652956055`
- reliability: `0.43837666247277174`

The official TEST acquisition explicitly selects `thresholds[world]`. In contrast, the candidate path builds the same reference brain and feeds it observation evidence, strength, source/evidence IDs and sensor/object metadata; it does not feed SparkBrain the symbolic world identifier. Therefore the comparator has an exact generative-regime/task label that the candidate does not.

This is prospectively preregistered and target-free, so it is not leakage or post-outcome tuning. It is nevertheless comparator-side information privilege. The worlds implement materially different processes and the terminal world effects have mixed signs (`-0.00374349`, `+0.00745443`, `-0.00514323`), so the effect of removing world identity is not determined by the terminal summary.

Safe interpretation:

> NI01 found no registered incremental native No-Ignition advantage over a **world-conditioned, coverage-matched confidence-abstention comparator**.

Stronger equal-privilege language — that native No-Ignition is mechanistically reducible to an ordinary score-only confidence head — is not established by this object alone.

## Secondary interpretation ceiling

The FAIL taxonomy also has no separately preregistered positive candidate-signal gate before the `REDUCED_BY_*` label is armed. NI01 still validly answers its registered incremental question: no incremental native advantage was demonstrated. Programme synthesis should distinguish that from stronger mechanism equivalence.

## Read-only recomputation limitation

A useful diagnostic would recompute only the comparator using a single global DEV-derived threshold, leaving immutable raw candidate outputs, TEST targets, loss and bootstrap definitions unchanged. The preserved raw JSONL is about 12.8 MB; the GitHub connector could not stream it during this run, so that sensitivity was not recomputed. This is a tooling limitation only; canonical NI01 evidence was not modified.

## Phase-2 comparison

After blind selection was fixed, summaries were read. Control Brain already calls for matched privilege and requested NI01 read-only review. Evidence Analyst currently describes NI01 as no incremental advantage over “matched confidence abstention.” MAIN remains architecture/testbed HOLD and SUB remains no-op. The newest Literature stream concerns future lineage admission and does not alter NI01.

The new finding narrows the word “matched”: coverage and score-vector source are matched, but world/regime information privilege is not.

## Classification

`WEAKENED`

Evidence integrity and the canonical terminal token remain valid. The equal-privilege mechanistic reduction interpretation is weakened by world-label privilege. No positive NI01 novelty support is restored.

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
  attacks:
    - authority/package drift or leakage
    - hidden world/task-label privilege
    - threshold/scorer drift
    - seed/world fragility
    - observation/resource mismatch
    - absent-signal versus reduction conflation
    - claim-boundary overreach
blind_target_change_reason: null
prospective_baselines_or_discriminators:
  - never rerun, retune, rescore, relabel or reopen canonical NI01
  - diagnostic-only global DEV threshold sensitivity without world identity
  - enumerate and match task/regime identifiers in future comparator privilege contracts
  - require a positive candidate-signal gate before mechanistic REDUCED_BY language where scientifically meaningful
questions_for_evidence_analyst:
  - Describe NI01 as world-conditioned coverage-matched confidence abstention?
  - Compute diagnostic global-threshold sensitivity read-only from immutable raw?
  - Treat regime/task IDs as explicit comparator privilege in future contracts?
questions_for_control_brain:
  - Count NI01 as no registered incremental native advantage but not equal-privilege mechanistic reduction?
  - Add task/regime-label privilege to the programme-wide symmetry gate?
  - Keep architecture/testbed HOLD unchanged because no positive NI01 signal is restored?
must_not_change_frozen_or_consumed:
  - ni01-no-ignition-selective-prediction-official-v1
  - dbfe7469dbbbc1adbb00789ab382de892a1b3563
  - 3dc90b08f85e0e7c459e0c17e86ab338901fd4c6
  - control/ni01-no-ignition-selective-prediction-started-v1-20260918
  - 8a39cf70e397bb7588f948910f01ec58672ac814
  - 69aa785a48bbdb531229b7f71f7fa84a5fde9948 and evidence tag
  - canonical NI01 statistics and FAIL_REDUCED_BY_CONFIDENCE_ABSTENTION
  - all other consumed C19/R1/R2/PD01/H5/A01/RV01/RV02/CX identities and immutable evidence
```
