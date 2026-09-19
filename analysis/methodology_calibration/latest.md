# SparkBrain Methodology Calibration Audit — 2026-09-20 01:20 JST

## Overall classification

**`MIXED_CALIBRATION`** — changed from `WELL_CALIBRATED` because a material evidence-interpretation fidelity defect was independently verified after the prior audit.

The scientific admission/stop/integrity methodology itself continues to behave well: the completed Temporal Architecture object remains NON_EVIDENTIARY, was stopped after one prospectively fixed cycle, was reduced to ordinary API/event-time semantics, and was held with no cycle-2 or PRE_FORMAL/FORMAL auto-promotion. However, the newest Evidence Analyst durable closure does **not faithfully reproduce the authoritative workflow artifact at the fine-grained result/provenance level**. That is a methodology problem in evidence interpretation and handoff fidelity even though it did not cause an incorrect promotion in this case.

## Material change since the previous audit

### 1. Temporal Architecture result completed under a sound prospective contract

`CAND-TEMPORAL-BATCH-PARTITION-01` ran once on exact head `7fa4391bbf34cf25e10b708ce64acddf07bf7f42` via workflow `35451528895`; exact-head CI and the Architecture job completed successfully. The pre-outcome contract is DEV/reference-only, forbids official TEST and FORMAL authority, fixes the three partition arms and both timeline families, requires raw-before-interpretation, maps one bounded cycle to four local Architecture outcome classes, and requires a fresh Analyst stop after every valid mapped outcome.

This part is methodologically healthy and remains `KEEP`.

### 2. Authoritative artifact versus Evidence Analyst handoff mismatch

The authoritative uploaded artifact (`artifact_id=10587410697`, ZIP digest `sha256:22a5c650a58501a1dc8303118c366845201f9eba8453a22996f5fb4ca4d6428f`) reports:

- `mapped_outcome = FUNCTIONAL_BATCH_PARTITION_EFFECT`;
- embedded `contract_sha256 = eb4aa28cd4b7299302ac31a65c73586c4e5a17e5487b1d1ddf43757cee901049`;
- `noisy_motif_stream_defaults`: omission schedule **differs across arms** and downstream replay **differs across arms**;
- `repetition_train_defaults`: omission schedule **does not differ across arms** and downstream replay **does not differ across arms**;
- raw row count `6`, raw digest `71d4d8fddbe6b683b4ad93951c0f95fc1dfa5df74645743bfd39fba5b33c54ef`.

The 01:15 Evidence Analyst durable handoff preserves the correct high-level mapped token `FUNCTIONAL_BATCH_PARTITION_EFFECT`, keeps the result NON_EVIDENTIARY, and correctly chooses HOLD/no cycle-2/no PRE_FORMAL. But it records `contract_sha256 = 681c21e31c686be7d8beb10e927ef65510ce82689c2cc81ae5fd9fedc179c06d` and reverses the family-level interpretation: it attributes the functional difference to `repetition_train_defaults` and the scheduler-only difference to `noisy_motif_stream_defaults`.

Control Brain 00:50 and Literature 00:30 independently describe the family-level artifact in the direction matching the machine artifact: noisy motif changes schedule and replay, repetition train is invariant.

This is therefore not a disagreement in scientific theory. It is an **artifact-to-handoff transcription/provenance mismatch**.

### 3. The defect did not cause a false-positive scientific escalation

The error is consequential but contained. Evidence Analyst's high-level classification is the same as the machine artifact, the line remains Architecture/engineering-only, current candidate state is `HOLD`, PRE_FORMAL and FORMAL remain empty, and no same-object cycle 2 was authorized. The ordinary reduction to non-anticipation/event-time versus processing-time/batch semantics is also appropriate regardless of which prospectively chosen family exhibited the functional divergence.

Therefore the correct programme-level diagnosis is `MIXED_CALIBRATION`, not `TOO_PERMISSIVE`: scientific integrity/admission gates are strong, but fine-grained evidence ingestion and interpretation fidelity need a prospective guard.

## Gate calibration

| Gate / rule | Classification | Current finding |
| --- | --- | --- |
| No rerun/retune/rescore; immutable evidence; raw-before-score / preserve-before-read | `KEEP` | Hard integrity floor remains necessary and unchanged. |
| Prospective protocol / exact binding / STARTED no-clobber for FORMAL | `KEEP` | No weakening warranted. |
| Positive candidate signal before strong mechanistic `REDUCED_BY_*` language | `KEEP` | Preserves absent-signal versus explanatory-reduction distinction. |
| Equal-privilege comparator matching for mechanistic claims | `KEEP` | Stronger-privilege methods remain ceilings unless matched. |
| Stronger-reference / semantic ceiling labeling | `KEEP` | `EVENT_TIME_CAUSAL` is correctly labeled as a stronger API/event-time reference, not a mechanistic peer comparator. |
| New-computational-principle novelty bar | `KEEP` | Appropriate for the strongest claim. |
| Same novelty bar applied to architecture/system/testbed value | `SPLIT_BY_CLAIM_TYPE` | Temporal batching is useful Architecture/API evidence without novelty support. |
| `NO_HIGH_VALUE_FORMAL_OBJECT => programme-wide HOLD` | `RELAX` | Corrected doctrine remains appropriate. |
| Observable/question-level exhaustion rather than family-level exhaustion | `CLARIFY` | Fresh independently motivated bounded questions remain permissible. |
| Default three-cycle exploration budget | `KEEP` | Upper bound only; exact ordinary reductions and low support may stop earlier. |
| Stop after each Architecture cycle for fresh Analyst review | `KEEP` | Temporal stopped after one valid mapped result; no same-object continuation. |
| Legacy Top-k sparse-stratum local gate | `TIGHTEN` | Do not reuse its full-vote sparse-stratum semantics prospectively. |
| Top-k exact replacement support/uncertainty rule | `INSUFFICIENT_EVIDENCE` | Do not fit a universal rule to completed outcomes. |
| Prospective support-aware Architecture triage | `KEEP` | Assembly already demonstrated clean rejection under such a design. |
| Local Architecture numeric-threshold portability | `CLARIFY` | Local cutoffs are not programme standards. |
| Architecture local thresholds as novelty/FORMAL thresholds | `CLARIFY` | Keep local triage local. |
| Automatic PRE_FORMAL promotion after Architecture signal | `KEEP` | Explicitly absent. |
| Ordinary-control-first Architecture reduction | `KEEP` | Temporal is being interpreted through ordinary event-time/batching semantics. |
| Architecture value surviving novelty rejection | `KEEP` | Temporal engineering/reproducibility value is retained without novelty inflation. |
| Fresh Architecture contract before outcome visibility | `KEEP` | Temporal contract was fixed before its outcome. |
| **Machine artifact -> durable handoff value fidelity** | **`TIGHTEN`** | A correct workflow artifact was summarized with reversed family-level effects. |
| **Embedded contract/artifact digest binding in interpretation handoff** | **`TIGHTEN`** | Analyst recorded a contract digest different from the artifact metadata. |
| **Fail-closed reconciliation on artifact/handoff mismatch** | **`TIGHTEN`** | Fine-grained interpretation should be marked conflicting until machine values are reconciled; no promotion should depend on disputed fields. |
| Local existential Architecture effect versus cross-family generality | `CLARIFY` | One fixed family can establish a bounded local API sensitivity; it does not establish broad/general mechanism support. |

## Mandatory calibration dimensions

- `gate_drift`: the four-layer funnel, support-aware lower-funnel objects and mandatory post-cycle review remain positive changes. The new issue is not a need to tighten scientific novelty gates; it is a missing machine-to-handoff fidelity guard.
- `justification_trace`: strong for the hard integrity floor, comparator privilege, ordinary reduction and stop/review boundaries. The new fidelity recommendation has a direct observed justification: one completed artifact and its newest durable Analyst interpretation disagree on both contract digest and family-level result attribution.
- `false_positive_control`: scientifically strong. Despite the transcription defect, Temporal did not enter PRE_FORMAL or FORMAL and no new principle was claimed. Remaining risk is that a future mismatch could drive a wrong successor/comparator if not detected.
- `false_negative_risk`: controlled. Do **not** respond by requiring every Architecture family to replicate an effect before any local Architecture label; that would conflate local existence with generality. Tighten provenance/fidelity, not the scientific existence threshold globally.
- `duplicate_guards`: no scientific-purpose integrity guard should be removed. Machine-artifact fidelity is distinct from one-way execution integrity and is not redundant with it.
- `moving_goalposts`: `LOW`. The authoritative Temporal result was produced under a precommitted map, completed labels have not been changed, and no outcome-responsive cycle 2 was authorized.
- `pass_reachability`: `REACHABLE_BUT_NARROW`. FORMAL admission remains possible through fresh support-adequate exact-bound objects; the new recommendation improves interpretation reliability rather than raising the scientific bar.
- `comparator_calibration`: healthy. Event-time-causal remains explicitly a stronger semantic reference/ceiling.
- `signal_before_reduction`: healthy. Temporal produced a bounded Architecture/API effect and was then ordinarily reduced in interpretation; no mechanistic novelty was inferred.
- `claim_type_separation`: healthy. New computational principle and mechanistic distinctness are unsupported, while Architecture/system-integration and engineering/reproducibility value are retained.
- `research_worthiness_vs_novelty`: no material conflation observed.
- `external_calibration`: current Literature appropriately narrows Temporal to ordinary non-anticipation, event-time/processing-time and stream-partition semantics. Independent Audit continues to support narrow claim boundaries for H5.
- `opportunity_cost`: a cheap machine-checked handoff-fidelity guard has high expected information value and much lower cost than adding more scientific gating or rerunning experiments.

## Representative checks

- `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; exactly five authoritative `evidence/*` tags remain and `formal/*` remains empty.
- C19-R2 remains anchored by annotated evidence tag object `82b88f3e2ad524fed8b72300dcba46053c1f2c7e` to terminal commit `6197fa801a78a0c5de4c2b6ff5d03216ac5539db`.
- H5 remains anchored by annotated evidence tag object `e7d99cc806206ac27ced225d4779c9fc5bb67ff5` to terminal commit `61aff6d74b82b68a326f3d90505d70bcd4071fd5`; its latest independent audit keeps the terminal FAIL robust but interpretation narrow.
- Latest SUB Discovery cleanly rejected source-lineage permutation sensitivity after exact bounded-provenance bookkeeping reduction; this remains healthy lower-funnel stop behavior.
- Temporal workflow `35451528895` itself is valid and successful. The issue is the fidelity of downstream durable interpretation, not the workflow's one-way integrity.

## Prospective recommendations

1. Keep the four-layer funnel, `FORMAL_HOLD_WITH_ACTIVE_LOWER_FUNNEL`, complete one-way integrity floor, claim-type separation, ordinary-reduction-first interpretation and stop-after-each-Architecture-cycle review.
2. Keep `CAND-TEMPORAL-BATCH-PARTITION-01` at HOLD. Do not rerun, relabel, repair, create cycle 2, or promote it because of this audit.
3. Treat the machine artifact's mapped token as the authoritative lower-funnel result for this audit, but mark the disputed **fine-grained family interpretation and digest fields** as `ARTIFACT_HANDOFF_MISMATCH` until the owning roles reconcile them prospectively. This audit does not edit their records.
4. Before a future Analyst/Control interpretation is allowed to drive promotion or successor design, require machine-checkable binding of workflow run/head, artifact ID/digest, embedded candidate ID, embedded contract digest, mapped outcome, raw digest and the exact machine summary fields being narrated.
5. If machine artifact and durable handoff disagree, fail closed for downstream scientific use of the disputed fields: do not promote or design a successor from those details until reconciled. Do not automatically invalidate an internally consistent artifact merely because the narrative is wrong.
6. Distinguish local Architecture existence claims from breadth/generalization. Do not globally demand cross-family replication merely to fix a provenance problem.
7. Keep Top-k HOLD and do not derive a universal support threshold from completed outcomes.
8. Preserve external-literature reduction ladders as prospective comparator/discriminator input only.

## Utility request

Created `METHCAL-20260920-0120-ARTIFACT-HANDOFF-FIDELITY` on `ops/utility-orchestrator-requests` as a bounded read-only methodology proposal. It asks whether recent Architecture artifacts are faithfully represented in durable handoffs and forbids reruns, result edits, threshold selection, TEST access, formal authority creation, branch/evidence mutation and scheduler changes.

Request commit: `1e28e558a985db1c05bf81ef1033028b39ee9018`.

## Hard-integrity-floor confirmation

Confirmed unchanged: no rerun/retune/rescore of consumed identities; frozen/prospective protocols; raw-before-score; preserve-before-read; exact identity/source/package/runtime/input binding; immutable evidence; no evaluator/target leakage; no silent post-outcome repair.

## Bottom line

**`MIXED_CALIBRATION` is the best current classification.** The programme's scientific admission, stop and one-way-integrity gates remain strong and prevented the Temporal Architecture effect from becoming novelty/Formal evidence. But a newly verified artifact-to-handoff mismatch shows that evidence-interpretation fidelity is not yet calibrated to the same standard. Tighten machine-bound result ingestion and fail-closed reconciliation; do not tighten the FORMAL novelty bar or rerun completed science.