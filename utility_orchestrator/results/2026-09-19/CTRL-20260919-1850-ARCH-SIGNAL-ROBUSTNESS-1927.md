# Utility Result — CTRL-20260919-1850-ARCH-SIGNAL-ROBUSTNESS

timestamp: `2026-09-19T19:27:21+09:00`  
assignment_id: `CTRL-20260919-1850-ARCH-SIGNAL-ROBUSTNESS`  
source_request: `METHCAL-20260919-1818-ARCH-SIGNAL-SUPPORT`  
mode: `READ_ONLY_ARCHITECTURE_SIGNAL_ROBUSTNESS`  
evidentiary_status: `NON_EVIDENTIARY_METHODOLOGY_DIAGNOSTIC`  
run_count: `1/1`  
status: `COMPLETED`

## Scope and integrity checks

- Target only: `CAND-TOPK-PA-01` cycle-1 DEV artifact from workflow `35432088902`, artifact `10581155271`.
- Workflow target head verified as `97f542d86dcd3a609cd039379fcda41ba61e0909` and completed successfully.
- Downloaded artifact SHA-256 verified against GitHub metadata: `62ee402e9e7c5a1cd41e65eebcbbe183d2be0625e4e66c2157ae207317f93f83`.
- Artifact contains `2304` raw condition rows = `1152` paired cases.
- Exact cycle-1 harness/contract read from `scripts/architecture_studies/topk_persistent_amplification_cycle1.py` at the target head.
- Current authoritative `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`.
- Current research branch has advanced beyond the cycle-1 head, but the current MAIN lease is not RUNNING on a conflicting Utility object; this diagnostic used cycle-1 material only and no later scientific result was used for the analysis.
- No TEST, formal identity, STARTED, preserve/evidence artifact, consumed formal raw, scheduler mutation, research branch mutation, rerun, retraining, reprobe, or scientific workflow execution occurred.

## Canonical cycle-1 contract and result (unchanged)

The fixed cycle-1 gate is:

- total turnover cases `>=20`;
- a magnitude is a signal vote when median state-AUC ratio `>=2.0` and median probability-AUC ratio `>=1.5`;
- final signal requires at least `2/3` signal magnitudes;
- ratio denominator floor is `1e-12`.

Existing canonical NON_EVIDENTIARY classification remains unchanged: `PERSISTENCE_COUPLED_DELAYED_AMPLIFICATION_SIGNAL`.

Observed turnover support and medians:

| magnitude | turnover n | median state ratio | median probability ratio | canonical signal vote |
|---:|---:|---:|---:|:---:|
| 0.01 | 1 | 2.0297 | 35.5036 | yes |
| 0.05 | 11 | 1.4654 | 10.1260 | no |
| 0.10 | 25 | 2.0326 | 7.8192 | yes |

The support imbalance is material: the `0.01` vote is one turnover case only. It occurs in one calibration episode at probe position 24. At `0.05`, 8/11 turnover cases occur at probe position 24 and 3/11 at position 18. The `0.10` stratum is much broader across probe positions. Across all turnover cases, the three most represented calibration episodes contribute 29/37 cases (`78.4%`), so case-level rows are not plausibly independent replicates.

## 1. Leave-one-magnitude-out stability

Applying the existing harness logic to the remaining magnitudes only, without changing any raw value:

| omitted magnitude | remaining turnover n | diagnostic classification |
|---:|---:|---|
| 0.01 | 36 | `MIXED_ARCHITECTURE_RESULT` |
| 0.05 | 26 | `PERSISTENCE_COUPLED_DELAYED_AMPLIFICATION_SIGNAL` |
| 0.10 | 12 | `ARCHITECTURE_INCONCLUSIVE_LOW_TURNOVER` |

Only one of the three leave-one-magnitude-out views retains `SIGNAL`, and that retained view still depends on the single-case `0.01` signal vote. This indicates the current triage classification is not leave-one-stratum robust.

## 2. Per-stratum minimum-support sensitivity

As non-canonical diagnostics, require a stratum to have at least `n>=3`, `n>=5`, or `n>=10` before it can cast a signal vote. Under all three examples:

- `0.01` becomes ineligible (`n=1`);
- `0.05` remains eligible but fails the state-ratio signal cutoff;
- `0.10` remains eligible and passes both cutoffs;
- only one supported stratum supplies a signal vote.

Therefore all three example rules produce a **MIXED** triage interpretation rather than SIGNAL. They do not make the whole result under-supported because two strata still meet each example support floor.

## 3. Uncertainty diagnostics

These are diagnostic summaries only, not formal confidence statements. Rows share episodes/probes/directions, so independence assumptions are weak.

Naive turnover-case bootstrap median 95% intervals (`20,000` resamples, seed `20260919`):

| magnitude | n | state-ratio median 95% interval | probability-ratio median 95% interval |
|---:|---:|---:|---:|
| 0.01 | 1 | not estimable from one case | not estimable from one case |
| 0.05 | 11 | 1.246–2.031 | 7.407–24.480 |
| 0.10 | 25 | 1.810–3.722 | 5.033–12.484 |
| pooled turnover | 37 | 1.675–2.402 | 6.381–12.646 |

Episode-cluster bootstrap (`10,000` resamples of the 12 calibration episodes, seed `20260919`) is wider, as expected:

- `0.01`: 36.1% of resamples contain no turnover support at all; when present it is still the same single observed case duplicated by cluster resampling, so it cannot supply meaningful uncertainty estimation.
- `0.05`: conditional state median interval about `1.244–3.623`; probability median `8.943–83.845`.
- `0.10`: state median interval about `1.491–3.851`; probability median `5.068–14.117`.
- pooled state median interval about `1.271–3.658`; pooled probability median `6.382–18.725`.

Under the current total-support + two-vote rule applied to these episode-cluster resamples, the diagnostic outcome is SIGNAL in about `56.9%`, low-turnover/inconclusive in `9.7%`, and mixed/other in `33.4%`. This is not a p-value or formal sampling statement; it is a robustness check showing that the current gate is materially sensitive to episode composition.

The main uncertainty is the **state-ratio threshold near 2.0**, not the probability-ratio threshold. The probability amplification remains well above `1.5` in the supported `0.05` and `0.10` strata, while state-ratio intervals span the `2.0` boundary.

## 4. Denominator-floor / near-zero-control sensitivity

The fixed `1e-12` denominator floor does **not** create the large ratios:

- minimum turnover-case control state AUC is about `0.3485`;
- minimum turnover-case control probability AUC is about `4.60e-4`;
- therefore no turnover-case denominator is clipped by the canonical `1e-12` floor.

The probability ratios are partly large because the actual no-persistent control probability AUCs are small, especially at low magnitude, but they are not a numerical-floor artifact. As deliberately non-canonical stress tests, replacing the probability denominator floor with much larger values still leaves median probability ratios above the `1.5` cutoff:

| diagnostic floor | 0.01 prob median | 0.05 prob median | 0.10 prob median |
|---:|---:|---:|---:|
| 1e-3 | 33.616 | 10.126 | 7.819 |
| 5e-3 | 6.723 | 10.126 | 7.819 |
| 1e-2 | 3.362 | 7.445 | 5.033 |

So the output-amplification observation is substantially more robust than the state-ratio vote structure. These alternative floors are diagnostics only and are not proposed as replacements.

## 5. Robust aggregate interpretation

A support-aware aggregate is more consistent with **MIXED** than with SIGNAL or globally UNDER-SUPPORTED:

- Excluding only the unsupported `0.01` stratum leaves 36 turnover cases.
- The two supported stratum medians are state ratios `1.465` and `2.033`; their equal-stratum-weight midpoint is about `1.749`, below the `2.0` signal cutoff.
- Their probability-ratio medians are `10.126` and `7.819`; both are comfortably above `1.5`.
- The pooled supported-case state median is about `2.004`, almost exactly on the cutoff and not robust under bootstrap, while the pooled probability median is about `8.506`.

Therefore the cycle-1 material supports a robust qualitative statement of **strong output amplification with mixed / threshold-sensitive state amplification**, not a support-robust two-stratum state+output SIGNAL vote.

Diagnostic robust aggregate classification: `MIXED`.

## 6. Methodology-only recommendation

Recommendation: **`ADD_PER_STRATUM_SUPPORT`**.

Reason: the clearest permissiveness defect is that the present rule allows a single turnover case to cast one of the two required magnitude votes. A modest prospective per-stratum support eligibility rule would prevent that failure mode while leaving the exact support threshold open to calibration. A robust aggregate can be useful as a secondary diagnostic, but the first-order fix is to prevent under-supported strata from voting as though they were comparably characterized.

This recommendation is prospective methodology input only. It does not alter the cycle-1 canonical NON_EVIDENTIARY result, does not promote or demote the candidate, and creates no PRE_FORMAL/FORMAL authority.

## Stop / follow-up

Stop condition reached after one result. No follow-up Utility run requested under this assignment.
