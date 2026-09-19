# Utility Result — CTRL-20260920-0250-ARTIFACT-HANDOFF-FIDELITY

- status: `COMPLETED`
- assignment_id: `CTRL-20260920-0250-ARTIFACT-HANDOFF-FIDELITY`
- source_request: `METHCAL-20260920-0120-ARTIFACT-HANDOFF-FIDELITY`
- temporary_role: `READ_ONLY_ARTIFACT_HANDOFF_CONSISTENCY_AUDIT`
- evidentiary_status: `NON_EVIDENTIARY_METHODOLOGY_FIDELITY_DIAGNOSTIC`
- run_count: `1 / 1`
- diagnostic_classification: `REPEATED_HANDOFF_FIDELITY_DEFECT`
- recommendation: `ADD_FAIL_CLOSED_MACHINE_CHECKABLE_HANDOFF_GUARD`

## Executive conclusion

The fidelity defect is **not isolated to the Temporal result**. In two independent completed NON_EVIDENTIARY Architecture chains that were safely accessible, workflow/artifact identity and top-level classification were mostly preserved, but lower-level machine facts were mistranscribed in durable MAIN/Evidence Analyst prose:

1. **Temporal cycle 1:** Evidence Analyst used the wrong embedded contract digest and reversed which timeline family had schedule/replay divergence. MAIN later reconciled this correctly from the artifact. The top-level mapped outcome and HOLD decision were unchanged.
2. **Top-k cycle 1:** MAIN and the subsequent Evidence Analyst correctly preserved workflow/head/artifact provenance, aggregate ratios, and top-level classification, but both stated that the predeclared signal criterion cleared at magnitudes `0.01` and `0.10`. The machine summary itself fixes `turnover_minimum=20`; `0.01` has only `1` turnover case, while `0.10` has `25`. Therefore only `0.10` clears all stated signal criteria. The top-level classification remained valid because `0.10` independently clears the contract.

This is enough to reject the hypothesis that the Temporal mismatch was a single isolated transcription accident. It does **not** establish a numerical fleet-wide error rate from two samples. The supported conclusion is narrower: there is a repeated artifact-to-handoff fidelity weakness, and downstream methodological decisions should not depend on manually narrated machine fields without a fail-closed consistency check.

No historical record is rewritten by this audit.

## Mandatory sample — CAND-TEMPORAL-BATCH-PARTITION-01 cycle 1

### Machine provenance

- workflow run: `35451528895`
- workflow conclusion: `success`
- producing head: `7fa4391bbf34cf25e10b708ce64acddf07bf7f42`
- artifact ID: `10587410697`
- artifact name: `temporal-batch-partition-cycle1-7fa4391bbf34cf25e10b708ce64acddf07bf7f42`
- archive SHA-256: `22a5c650a58501a1dc8303118c366845201f9eba8453a22996f5fb4ca4d6428f`
- candidate: `CAND-TEMPORAL-BATCH-PARTITION-01`
- embedded analyst authority: `862dd62cdce58f06e5c782b4b54212d93e40212e`
- embedded contract SHA-256: `eb4aa28cd4b7299302ac31a65c73586c4e5a17e5487b1d1ddf43757cee901049`
- metadata SHA-256: `7dca97b2ccd9d937469288d7c3e75ac53bfd01346d39d660f8c467777b16f5ec`
- raw SHA-256: `71d4d8fddbe6b683b4ad93951c0f95fc1dfa5df74645743bfd39fba5b33c54ef`
- summary SHA-256: `037e3bfdd7f14404308753512a0331c4b8a9d31ec7b59191778d7f84af195290`
- raw rows: `6`
- mapped outcome: `FUNCTIONAL_BATCH_PARTITION_EFFECT`
- `official_test_opened=false`
- `started=false`
- `raw_before_interpretation=true`

### Exact machine family summary

`repetition_train_defaults`:
- `schedule_differs_across_arms=false`
- `replay_differs_across_arms=false`
- all three omission-schedule hashes are identical
- all three replay-observable hashes are identical

`noisy_motif_stream_defaults`:
- `schedule_differs_across_arms=true`
- `replay_differs_across_arms=true`
- omission-schedule hashes differ by arm
- replay-observable hashes differ by arm

### Handoff comparison

The 01:15 Evidence Analyst handoff correctly preserved:
- workflow run/head;
- artifact ID;
- top-level mapped outcome `FUNCTIONAL_BATCH_PARTITION_EFFECT`;
- NON_EVIDENTIARY Architecture status;
- downstream decision to close/HOLD rather than auto-promote.

It did **not** faithfully preserve:
- embedded contract digest: handoff recorded `681c21e31c686be7d8beb10e927ef65510ce82689c2cc81ae5fd9fedc179c06d`, artifact reports `eb4aa28cd4b7299302ac31a65c73586c4e5a17e5487b1d1ddf43757cee901049`;
- family-level behavior: handoff attributed functional partition dependence to repetition and no downstream difference to noisy-motif, while the artifact says the reverse.

The 01:24 MAIN full reconciliation re-opened the artifact read-only and correctly restored the artifact truth: repetition invariant, noisy-motif partition-sensitive, correct artifact contract digest/raw digest, while retaining the same top-level mapped outcome and HOLD allocation. It classified the issue `YELLOW_NON_DECISION_CHANGING_ANALYST_DESCRIPTIVE_MISMATCH`.

Temporal fidelity result: `MISMATCH_CONFIRMED / DECISION_UNCHANGED`.

## Opportunistic sample — CAND-TOPK-PA-01 cycle 1

This already-produced artifact was safely accessible, so one additional independent chain was sampled. A second sample is sufficient for the bounded question of whether the Temporal defect is isolated; Assembly was not sampled after the repeated defect was established, avoiding unnecessary scope expansion.

### Machine provenance

- workflow run: `35432088902`
- workflow conclusion: `success`
- producing head: `97f542d86dcd3a609cd039379fcda41ba61e0909`
- artifact ID: `10581155271`
- artifact: `topk-persistent-amplification-cycle1`
- archive SHA-256: `62ee402e9e7c5a1cd41e65eebcbbe183d2be0625e4e66c2157ae207317f93f83`
- study: `CAND-TOPK-PA-01`
- embedded analyst commit: `3e83f1eb683ce80e326b756fa304e96688fdd3fe`
- metadata SHA-256: `3603010917e2e693b93e1023e778c64b89b07c69b69867754cfa09079177ee78`
- raw SHA-256: `316498f99ff60c59e1a1eb146c1e498972539402820cea48202ab4bf420c3b00`
- summary SHA-256: `783578fbe6f2187d02c0b078a078b83e101bf1b7a345dedbedcf3d545b3ee861`
- classification: `PERSISTENCE_COUPLED_DELAYED_AMPLIFICATION_SIGNAL`
- `test_manifest_opened=false`

### Fixed machine interpretation contract

- `probability_ratio_signal >= 1.5`
- `state_ratio_signal >= 2.0`
- `turnover_minimum >= 20`
- denominator floor `1e-12`

Machine magnitude summary:

| magnitude | turnover cases | median probability ratio | median state ratio | clears all fixed signal requirements? |
|---:|---:|---:|---:|---|
| `0.01` | `1` | `35.5036` | `2.0297` | **No — support <20** |
| `0.05` | `11` | `10.1260` | `1.4654` | No |
| `0.10` | `25` | `7.8192` | `2.0326` | **Yes** |

### Handoff comparison

The 17:33 MAIN result faithfully preserved workflow/head/artifact/archive digest, internal file hashes, aggregate paired/turnover counts, all three ratio summaries, classification, and NON_EVIDENTIARY status. However it states: `The prospectively fixed signal condition is satisfied at magnitudes 0.01 and 0.10.` This is incompatible with its own artifact's `turnover_minimum=20`, because `0.01` has only one turnover case.

The 18:20 Evidence Analyst handoff repeats the same statement: `the predeclared signal criterion cleared at 0.01 and 0.10.` Thus this is not only a one-hop wording slip; the incorrect stratum-level interpretation propagated into the next control-plane handoff.

The top-level classification remains valid because magnitude `0.10` independently satisfies all fixed conditions. Later read-only Utility support analysis explicitly treated `0.01` as under-supported rather than a supported signal.

Top-k fidelity result: `MISMATCH_CONFIRMED / PROPAGATED_ONE_HOP / TOP_LEVEL_DECISION_STILL_SUPPORTED`.

## Cross-sample assessment

Observed across the two sampled completed Architecture chains:

| Field class | Temporal | Top-k cycle 1 |
|---|---|---|
| workflow run / head | faithful | faithful |
| artifact identity / archive digest | faithful once reconciled | faithful |
| embedded contract/interpretation identity | **wrong in Analyst** | threshold values themselves faithfully stated |
| raw digest | faithful in reconciled MAIN | faithful |
| top-level mapped outcome/classification | faithful | faithful |
| lower-level family/stratum machine summary | **reversed in Analyst** | values faithful but criterion application **wrong** |
| downstream allocation impact in sampled chain | unchanged | cycle-2 replication still scientifically supportable from the `0.10` stratum, but rationale overclaimed breadth |

Diagnostic classification: **`REPEATED_HANDOFF_FIDELITY_DEFECT`**.

The common failure mode is not loss of the entire artifact identity; it is **manual semantic transcription after the artifact is available**. Exact identifiers and top-level labels survive, while lower-level fields or criterion application can drift. Those lower-level facts are precisely the facts later used for methodology calibration, reduction choices, breadth/generalization claims, and successor design.

## Prospective methodology recommendation

Recommendation: **`ADD_FAIL_CLOSED_MACHINE_CHECKABLE_HANDOFF_GUARD`**.

For future outcome-bearing lower-funnel workflow artifacts, before a MAIN/Relay or Evidence Analyst handoff can authorize successor design, the durable handoff should machine-bind at minimum:

1. workflow run ID and exact producing head;
2. artifact ID/name and archive digest;
3. embedded candidate/study identity;
4. embedded Analyst/contract/interpretation identity or digest when present;
5. raw digest and row/cardinality count when present;
6. exact mapped outcome/classification;
7. a canonical digest of the complete machine summary object used for interpretation;
8. every family/stratum boolean, count, ratio, threshold application, or other machine-summary field that is narrated in prose.

A practical guard can validate a small structured `handoff_binding.json` or equivalent against the downloaded machine artifact before allowing the durable narrative to be marked current. If any bound field differs, set a fail-closed state such as `HANDOFF_FIDELITY_BLOCKED`, preserve the machine artifact as authority, and block successor allocation that depends on the disputed field until reconciliation. The guard should be prospective only; do not rewrite or retroactively relabel historical scientific results.

This recommendation does not change any scientific threshold, comparator, metric, seed, outcome, candidate status, or evidence identity. It is a control-plane fidelity safeguard.

## Collision / ownership check

At audit time, current MAIN is on a distinct fresh v0.5 topology-config Architecture object and the current Evidence Analyst explicitly lists this Utility fidelity assignment as active, read-only, and nonblocking. The audit touched no MAIN/SUB/Relay active object and created no dependency on their critical path.

## Integrity record

- scientific/model workflow rerun: `false`
- workflow dispatch: `false`
- training/probe rerun: `false`
- result regeneration/rescoring: `false`
- official TEST accessed: `false`
- formal/consumed raw evidence accessed: `false`
- main/research branch mutated: `false`
- immutable/freeze/sealed/formal/evidence/control/preserve refs mutated: `false`
- prior MAIN/Analyst/Control/request/result record edited: `false`
- threshold/comparator/metric/seed/successor changed: `false`
- PRE_FORMAL/FORMAL authority created: `false`
- scheduler mutated: `false`
- follow-up Utility request self-issued: `false`

Stop reason: `COMPLETED_ONE_BOUNDED_CONSISTENCY_AUDIT_MAX_RUNS_REACHED`.
