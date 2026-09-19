# SparkBrain Methodology Calibration Audit — 2026-09-20 05:18 JST

## Run disposition

**`MATERIAL_CALIBRATION_UPDATE`**

## Overall classification

**`MIXED_CALIBRATION`** — unchanged, but the remaining weakness is now better localized: artifact-to-handoff binding is being prospectively addressed, while a distinct upstream machine-fact extraction defect has now been observed inside a completed NON_EVIDENTIARY Architecture diagnostic.

The scientific admission, novelty, reduction, comparator, stop/reframe, and FORMAL evidence gates remain broadly well calibrated. The material new evidence does **not** justify making the scientific bar stricter. It justifies tightening the validity requirements for decision-relevant machine facts that are extracted from source/runtime surfaces before those facts are allowed to drive successor allocation.

## What changed since the 04:21 audit

### 1. Control accepted the generic handoff-binding guard prototype

Control Brain 04:50 accepted `EVA-20260920-0401-HANDOFF-BINDING-GUARD` and issued one bounded NON_EVIDENTIARY Utility assignment, `CTRL-20260920-0450-HANDOFF-BINDING-GUARD`.

The assignment is correctly scoped to already-completed safe fixtures, must detect the known Temporal and Top-k handoff mismatches fail-closed, must pass at least one faithful binding, and may not rerun/rescore/repair scientific results, change thresholds, touch TEST/FORMAL evidence, mutate research/main, or wire itself into live schedulers/workflows.

This is a real prospective methodology improvement, but the prototype has not yet completed and is not yet demonstrated in a live closure. Therefore programme-wide handoff-binding enforcement is still not fully established.

### 2. A distinct upstream detector-fidelity defect appeared in the suppression Architecture object

`CAND-V05-UNIT-SUPPRESSION-TRANSIENT-SEMANTICS-01` was prospectively bound and executed once on exact head `2ef4b24f8e7ef8577ebbcb0328e7b3476bc24336`. Workflow `35465512928` succeeded and emitted machine outcome `AMBIGUOUS_CONTRACT`.

Independent source/harness inspection confirms that the harness derives `restore_restores_original_base_threshold` by the literal test:

`"unit.base_threshold = threshold" in restore_source`

but the exact bound source implements restoration as:

`self.base.field.units[unit_id].base_threshold = threshold`

Therefore the emitted boolean can be false even though the bound source plainly restores the threshold. This is a machine-fact extraction false negative, not merely a prose handoff mismatch.

The current control path responded correctly: MAIN detected the post-outcome diagnostic anomaly, marked the Architecture attempt invalid/discarded for successor use, blocked itself, and explicitly refused in-run patch/rerun/rescore/relabel. Evidence Analyst also placed the candidate on HOLD and created a bounded read-only detector-consistency request rather than repairing the result.

### 3. The integrity/STOP rules successfully contained the defect

The machine artifact remains preserved; no replacement scientific outcome has been manufactured. No dynamic cycle 2, PRE_FORMAL, or FORMAL successor was authorized from the suspect static fact. This is strong evidence that the hard one-way integrity floor and fresh-review stop rule are working.

The defect nevertheless matters for methodology calibration because a machine-bound artifact is not automatically semantically valid merely because its provenance/digest binding is correct. A generic handoff checker alone cannot catch a wrong fact that is internally consistent inside the artifact.

### 4. Claim-type separation remains healthy

SUB's fresh cross-cascade fallback Discovery is explicitly reduced to ordinary fallback/control-flow semantics and remains NON_EVIDENTIARY. Evidence Analyst promotes only a fresh Architecture/testbed segmentation question, not a computational-principle claim. This continues to support the distinction between novelty and research-worthiness.

## Gate calibration

| Gate / rule | Classification | Current finding |
| --- | --- | --- |
| No rerun/retune/rescore; immutable evidence; raw-before-score / preserve-before-read | `KEEP` | Suppression invalid-diagnostic handling demonstrates the safeguard working. |
| Prospective protocol / exact source-runtime-input binding | `KEEP` | Necessary but not sufficient for semantic detector correctness. |
| Positive signal before strong mechanistic reduction language | `KEEP` | No evidence for change. |
| Equal-privilege comparator/resource matching | `KEEP` | No evidence for relaxation or overmatching. |
| New-computational-principle novelty bar | `KEEP` | Appropriate for the strongest claim type. |
| Applying that novelty bar to architecture/system/testbed value | `SPLIT_BY_CLAIM_TYPE` | Current Assembly/suppression handling preserves the split. |
| `NO_HIGH_VALUE_FORMAL_OBJECT => programme-wide HOLD` | `RELAX` | Lower-funnel information gain remains useful. |
| Stop after each Architecture cycle for fresh Analyst review | `KEEP` | Correctly prevented same-run repair/rescue. |
| Legacy Top-k sparse-stratum support gate | `TIGHTEN` | Historical local weakness remains. |
| Programme-wide replacement support/uncertainty threshold | `INSUFFICIENT_EVIDENCE` | Do not fit completed outcomes. |
| Machine artifact -> durable handoff value fidelity | `TIGHTEN` | Generic guard is Control-approved but not yet demonstrated. |
| Embedded contract/interpretation digest binding | `TIGHTEN` | Still justified by repeated historical handoff defects. |
| Machine application of declared thresholds/support rules | `TIGHTEN` | Still justified by Top-k. |
| **Decision-relevant machine-fact extraction from source/runtime** | **`TIGHTEN`** | New suppression false negative shows provenance-correct artifacts can contain semantically wrong extracted facts. |
| **Brittle literal-string semantic detectors used for outcome mapping** | **`TIGHTEN`** | Prefer deterministic structural/AST/typed checks or explicit tests that bind the actual semantic condition. |
| Fail-closed handling of a post-outcome diagnostic anomaly | `KEEP` | Block continuation; preserve the artifact; do not silently repair. |
| Generic handoff-binding guard before successor allocation | `TIGHTEN` | Accepted for prototype; live/end-to-end validation still pending. |
| Automatic PRE_FORMAL promotion after Architecture signal | `KEEP` | Must remain absent. |
| Local Architecture thresholds as FORMAL/novelty thresholds | `CLARIFY` | Local triage remains local. |

## Mandatory calibration dimensions

- `gate_drift`: two evidence-driven procedural changes are now visible: Control accepted the handoff-binding prototype, and suppression exposed a new upstream extractor-validity requirement. Neither changes the scientific novelty bar.
- `justification_trace`: strong. Temporal/Top-k justify handoff binding; suppression independently justifies machine-fact extractor validation.
- `false_positive_control`: improved by fail-closed invalid-diagnostic handling, but still vulnerable if semantically wrong machine facts are treated as authoritative solely because their provenance is correct.
- `false_negative_risk`: a brittle detector can also create false negatives by mapping a real implementation property to `false`. The correction should target detector validity, not require universal replication or stronger scientific support.
- `duplicate_guards`: provenance binding, artifact->handoff consistency, and machine-fact semantic validation protect three distinct stages; they should not be merged conceptually.
- `moving_goalposts`: `LOW`. The completed suppression artifact/outcome is not repaired or relabeled; successor use is blocked prospectively because the diagnostic itself is suspect.
- `pass_reachability`: `REACHABLE_BUT_NARROW`. A valid mechanism can still PASS through the existing funnel; detector validity is an integrity condition, not a new novelty hurdle.
- `comparator_calibration`: unchanged.
- `signal_before_reduction`: healthy; no weak/suspect suppression artifact is being promoted mechanistically.
- `claim_type_separation`: healthy; Assembly fallback and suppression remain Architecture/testbed questions, not novelty evidence.
- `research_worthiness_vs_novelty`: no material conflation observed.
- `external_calibration`: Literature/Audit add no reason to change substantive scientific thresholds; H5 remains a narrow robust negative for its registered metric.
- `opportunity_cost`: highest information gain comes from validating the handoff guard and the suppression static-fact extractor. Increasing scientific replication/novelty strictness would address the wrong failure mode.

## PASS reachability

**`REACHABLE_BUT_NARROW`**. The route remains: prospectively positive native signal -> fresh exact-bound object -> locally adequate support -> matched equal-privilege comparator for mechanistic claims -> survive ordinary implementation/dynamical reductions -> semantically valid machine-fact extraction -> faithful machine-bound handoff -> fixed intervention/falsifier -> one-way preserved FORMAL evidence.

Authoritative `evidence/*` remains exactly five annotated tags; tag-based `formal/*` remains empty. No new FORMAL evidence appeared.

## Prospective recommendations

1. Keep the four-layer funnel, strict FORMAL novelty bar, comparator discipline, ordinary-reduction-first interpretation, and hard integrity floor unchanged.
2. Complete and evaluate `CTRL-20260920-0450-HANDOFF-BINDING-GUARD`; do not confuse artifact/handoff consistency with artifact semantic validity.
3. Treat every decision-relevant machine fact derived from source/runtime inspection as requiring a prospectively specified validity method appropriate to the fact. For source semantics, prefer structural/AST/typed checks or explicit invariant tests over brittle literal substrings when practical.
4. If a post-outcome detector defect is found, preserve the artifact, fail closed for interpretation-dependent continuation, and require fresh prospective authority for any new diagnostic object. Never silently patch and reinterpret the completed attempt.
5. Do not respond to this defect with universal replication, stronger novelty thresholds, or automatic candidate rejection.
6. Keep local Architecture terminal classes and detector checks separate from FORMAL/novelty thresholds.
7. Do not retroactively rescore, relabel, rerun, invalidate, or upgrade consumed/frozen experiments because of this methodology update.

## Utility request

No new Methodology Calibration Utility request created. Evidence Analyst already created `EVA-20260920-0502-SUPPRESSION-STATIC-DETECTOR-CONSISTENCY`, a bounded read-only request that directly tests the new detector-fidelity issue. Creating a duplicate request would add no information value.

## Hard-integrity-floor confirmation

Confirmed unchanged: no rerun/retune/rescore of consumed identities; frozen/prospective protocols; raw-before-score; preserve-before-read; exact identity/source/package/runtime/input binding; immutable evidence; no evaluator/target leakage; no silent post-outcome repair.

## Bottom line

There **is** a material calibration update. Control has now accepted the generic artifact->handoff guard prototype, but a fresh suppression Architecture attempt exposed a separate upstream class of failure: a provenance-correct machine artifact can contain an incorrect decision-relevant static fact because the detector itself is brittle. Overall remains **`MIXED_CALIBRATION`**. Tighten machine-fact extraction validity and keep the scientific admission/novelty/comparator bars otherwise unchanged.