# A01 MD-002 P4 retained-trace binding technical review

Date: 2026-09-12  
Reviewed source head: `2f21c59f8351ff69df870e59a38e9c11107f095e`  
Review type: **automation technical/scientific-integrity review; not an independent human identity**  
Verdict: **P4 INPUT-BINDING GAP CLOSED / FULL P4 NOT YET EXECUTION-READY**

## Scope

This review covers only the source-level binding between retained runtime trace material and the `MergedAncestryObservation` input required by MD-002 P4. It does not claim that a complete P4 experiment has been constructed, executed, scored, or accepted.

No MD-001 evidence, N3-DEV-001 evidence, frozen/preserved source, or consumed capability result is changed or rerun.

## Findings

### Genuine merged ancestry — PASS at the input contract

The active binding requires at least one retained `BoundaryEvent` whose own `source_proposal_ids` contain at least two distinct proposal identities. Multiple separate singleton boundary events cannot be combined by the caller to manufacture a merged ancestry observation.

### Complete retained boundary-event coverage — PASS

The first implementation was not sufficient because a caller could provide a favorable subset of retained P4 boundary events while leaving additional boundary-event rows in the runtime trace. That would have permitted cherry-picking after the trace existed.

The merged revision closes this gap. The supplied `BoundaryEvent` set must exactly cover the complete retained `md002-p4-boundary-event` trace. Duplicate retained boundary rows are rejected and the canonical retained row set must equal the canonical supplied event set.

### Before/after live-lineage binding — PASS

The binding requires exactly one retained active-lineage record for each `before` and `after` phase. Lineage IDs must be unique non-empty strings. The derived boundary ancestry and active-lineage values must themselves appear as exactly one retained `md002-merged-ancestry-measurement` record.

The caller therefore cannot provide an independent expected winner/lineage constant outside the retained trace and have it silently accepted as P4 evidence.

### Existing observation contract — PASS as downstream validation

After the retained-trace derivation succeeds, the result is passed through the existing fail-closed `MergedAncestryObservation.validate()` path. The new layer narrows admissible inputs rather than replacing the already preregistered observation semantics.

## Negative/audit result retained

The pre-merge audit found a real scientific-integrity defect in the initial source-only implementation: membership of each supplied boundary event in the trace did not prove that the supplied set was complete. The implementation was corrected before merge and a regression test now rejects cherry-picked boundary subsets.

This negative finding is retained because it is relevant to future P4 runner review: **trace membership is not equivalent to complete trace coverage**.

## Remaining P4 blockers

Closing the input-binding gap is not equivalent to completing P4. Before a one-shot P4 mechanism-discrimination execution can be considered, the line still needs at least:

1. a prospective schedule/fixture that creates a genuine merged boundary ancestry and the later separating/inseparable lineage condition required by the frozen MD-002 contract;
2. an execution-disabled source-bound runner that records the complete raw boundary-event and before/after active-lineage trace without caller-selected filtering;
3. exact source manifest and runtime binding for that runner;
4. fixed outcome-blind scoring/acceptance rules for P4 and its negative controls before output is opened;
5. preservation/no-clobber semantics and an independent read-only artifact verifier;
6. integration with the rest of the MD-002 P1-P5 matrix without allowing P4 success to compensate for invalid/missing P1-P3 or P5 coverage;
7. separate resource-matching/P5 completion for the N3 comparator; the existing N3-DEV-001 audit explicitly leaves resource matching `NOT_EVALUATED`.

## Human-review policy note

This document does not claim an independent human reviewer. The standing user-authorized human-review waiver may later permit progression through a literal reviewer-identity-only gate, but it does not waive any of the technical and scientific-integrity prerequisites above.

## Execution authority

No execution seal, `STARTED` marker, source freeze, held-out capability, formal capability, or fresh candidate consumption is authorized by this review.
