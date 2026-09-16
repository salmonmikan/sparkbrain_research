# v0.6.1 A01 — Family-A / Family-B / Family-C Terminal-Provenance and Negative-Completion Bookkeeping Audit

## Scope and ownership

This is a SUB-owned, documentation-only audit under Evidence Analyst handoff:

```text
ops/evidence-analyst-handoff@5eb075481b8a5846a5234f1d397a88fd288af861
```

It extends the completed A/B audit at:

```text
research/v061-a01-negative-completion-ab-audit-sub-20260917
@9468bbe882bd7bd8bb0b60c2ad91d11e4616ac56
```

with Family C and a complete three-family provenance matrix. It does not create a scientific identity, change any evaluator/protocol/schema, authorize execution, synthesize a candidate disposition, declare machine negative completion, modify immutable evidence, or alter MAIN's registered-family closeout.

The branch is based on the completed MAIN closeout head only to inherit the already-completed semantics-preserving descendant test-scope fix and current canonical status:

```text
research/v061-a01-registered-family-closeout-20260917
@3329d15d9a3f73555396fb93a4dab117616e7bc2
```

This audit is not on MAIN's critical path and MAIN does not need its result to remain scientifically closed at the registered-family tested/bound-object level.

## Audited authorities

### Family A — transient-return-address

Terminal scientific object:

```text
identity: a01-md002-p4-merged-lineage-selective-resolution-candidate-001-v1
classification: UNSUPPORTED_EN_BLOC_MERGED_CREDIT
STARTED: true
identity consumed: true
P5 after P4 failure: NOT_ADMISSIBLE
```

Authority chain:

```text
freeze/a01-md002-p4-candidate-001-source-20260916
  -> 1bd0099f4358e02efac7ee4acccfe5257a86c4be
control/a01-md002-p4-candidate-001-started-20260916
  -> 1bd0099f4358e02efac7ee4acccfe5257a86c4be
preserve/a01-md002-p4-candidate-001-raw-20260916
  -> 2511454f1633d3bc6f10e3d2a99e3ddd823bb798
preserve/a01-md002-p4-candidate-001-scored-20260916
  -> 56ee762540e0519034d2e8db0ad3c6acda667ffd
```

Bound proposal specification SHA-256 recorded by the prior A/B audit:

```text
2794d1596227eab17c68c46d6874662c3669656edb49e28425f1ef613b66c5dc
```

### Family B — distributed-field-trace

Canonical closeout:

```text
research/v061-a01-family-b-gen1-execution-package-20260916
@db66596ed4479e8dac8b713b4f92a73f76a25047
```

Terminal scientific object:

```text
identity: a01-family-b-distributed-field-trace-gen1-v1
classification: REJECT_BEFORE_STARTED_STATIC_REDUCTION
STARTED: false
identity consumed: false
phase execution: none
reduction comparator: prospectively registered equal-resource recurrent causal-trace null
```

No acquisition, raw/scored evidence, preserve/freeze/formal/evidence authority, or one-way identity consumption was created for this object.

### Family C — joint-return-and-local-field-update

Canonical closeout:

```text
research/v061-a01-family-c-gen1-20260917
@cfe1c3e5506d9fd8b41028dbfe0f8a8dd31a82c5
```

Proposal binding:

```text
proposal-binding commit: 9cfddc6dc4d2beab090a9b38661a68dcec755ff7
proposal SHA-256: 4b574b7053efb50b59a8d7536c94d02a7a25bdfc5b1d7f88575c7b6fc3e614ac
Family-C null/resource binding SHA-256: 690a62df641d0577e3f7d760354763a6f0ec69e33eedfdacb37e92e7c654dbbc
```

Terminal scientific object:

```text
identity: a01-family-c-joint-return-local-field-gen1-v1
classification: REJECT_BEFORE_STARTED_STATIC_REDUCTION
STARTED: false
identity consumed: false
phase execution: none
reduction comparator: v061-a01-cgen1-separable-address-plus-field-null-v1
```

The prospectively registered comparator receives the same actual pending provenance capability, applies the same local Field update, expires the selector at the same point, and exposes the same post-update Field state to the same later readout without extra persistent state or greater lookup privilege. Therefore the exact candidate is statically subsumed before STARTED.

No Family-C STARTED/control, workflow dispatch, acquisition, raw/scored evidence, preserve/freeze/formal/evidence authority, or identity consumption exists for this object.

## Three-family terminal-provenance matrix

| Family | Mechanism family | Proposal authority | Terminal class | STARTED | Identity consumed | P1-P4 phase state | P5 state | Reduction comparator / falsifier | Canonical terminal authority | Faithful under current `CandidateDisposition`? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | `transient-return-address` | SHA-256 `2794d159...` | executed P4 terminal negative `UNSUPPORTED_EN_BLOC_MERGED_CREDIT` | yes | yes | executed through P4; exact P1-P3 booleans must come only from canonical phase authorities | not admissible after P4 failure | P4 selective historical-lineage resolution failed; merged ancestry changed en bloc | freeze/control/raw/scored chain above plus canonical A01 status | **Structurally yes**, if every mandatory P1-P4 boolean is populated from exact evidence authority; this audit does not synthesize them |
| B | `distributed-field-trace` | prospectively bound Family-B Gen1 object at `db66596...` | `REJECT_BEFORE_STARTED_STATIC_REDUCTION` | no | no | `NOT_ASSESSED` for P1-P4 | `NOT_ASSESSED` | equal-resource recurrent causal-trace null statically subsumes exact object | Family-B pre-START reduction decision / closeout branch | **No** — mandatory P1-P4 booleans cannot express not-assessed, and P5 explicit-memory reduction is the wrong semantic class |
| C | `joint-return-and-local-field-update` | proposal SHA-256 `4b574b70...`; extension binding `690a62df...` | `REJECT_BEFORE_STARTED_STATIC_REDUCTION` | no | no | `NOT_ASSESSED` for P1-P4 | `NOT_ASSESSED` | equal-resource separable address-plus-Field null statically subsumes exact object | `docs/V061_A01_FAMILY_C_GEN1_PRESTART_REDUCTION_DECISION.md` at `cfe1c3e...` | **No** — same representability failure as Family B; no truthful P1-P4 boolean encoding exists |

## Exact Family-C representability conclusion

Family C **repeats Family B's representability gap** under the current `CandidateDisposition` schema.

The schema requires unconditional booleans:

```text
p1_passed
p2_passed
p3_passed
p4_passed
```

and has only:

```text
p5_assessed
p5_reduced_to_explicit_memory
```

for P5 provenance. Family C was rejected at admission/static-screen time before any P1-P5 phase execution. Therefore:

- `false` in a P1-P4 field would falsely encode an observed phase failure;
- `true` would fabricate an observed phase pass;
- `p5_assessed=true` would fabricate a P5 execution;
- `p5_reduced_to_explicit_memory=true` would misclassify the actual comparator, which is a prospectively registered separable address-plus-Field null rather than an executed strengthened-P5 explicit-memory reduction.

Accordingly:

```text
Family-C CandidateDisposition under current schema: DO NOT CREATE
```

The Family-C identity remains unconsumed; bookkeeping must not convert that fact into a synthetic failed execution.

## Programme coverage gap remains after adding Family C

`NegativeCompletionProgramme.completed_families` is still a free tuple of mechanism-family enums. `assess_negative_completion()` tests family coverage by set equality against all registered mechanism families, while `validate()` does not require each completed family to have a matching evidence-backed disposition or terminal-provenance record.

Family C therefore does not close the bookkeeping gap merely by making all three families scientifically terminal at their current tested/bound-object level. Today it is possible in principle for a caller to claim A/B/C family coverage independently of whether B/C can be represented truthfully in `dispositions`.

That mismatch is exactly why the canonical programme-level machine verdict remains:

```text
WITHHELD
```

The strategic registered-family closeout is a separate evidence interpretation and does not imply that the existing machine accounting has emitted one of its two formal negative-completion classifications.

## Minimum future accounting requirements

A future, prospectively designed terminal-provenance layer should distinguish at least:

```text
EXECUTED_PHASE_FAILURE
EXECUTED_P5_REDUCTION
PRE_START_STATIC_REDUCTION
PRE_START_OTHER_REJECTION
```

and preserve, where applicable:

```text
mechanism family
proposal specification authority/hash
scientific identity
STARTED / not-STARTED
identity consumed / unconsumed
phase assessed / not-assessed per phase
terminal classification
reduction comparator class and exact authority
canonical evidence/status authority
```

Family coverage should be derived from, or strictly cross-validated against, these evidence-backed terminal records rather than accepted independently from them.

This audit intentionally does **not** implement that layer. A schema/evaluator change is a separate prospective methods/readiness object and must not be used retroactively to force a machine verdict for the already observed A/B/C programme.

## Safe current bookkeeping state

Until a prospective accounting redesign exists:

1. Family A may be represented only from exact evidence-backed phase facts; do not fill missing booleans from later prose.
2. Family B remains a canonical pre-START terminal record outside `CandidateDisposition`.
3. Family C remains a canonical pre-START terminal record outside `CandidateDisposition`.
4. Do not synthesize P1-P4 failures or passes for B/C.
5. Do not use `completed_families=(A, B, C)` alone as evidence for a machine negative-completion verdict.
6. Keep the current machine verdict `WITHHELD` while preserving the separate strategic closeout/reframe.

## Integrity / role boundary

This audit changes no scientific evidence or scientific interpretation. It performs no experiment, STARTED/control operation, workflow dispatch, acquisition, scoring, identity consumption, freeze/seal/formal/evidence mutation, or merge.

It does not touch MAIN's completed programme-closeout logic or branch, does not fix a MAIN blocker, and does not design A01 Gen2, Family-D, replacement science, new nulls, resource contracts, scorers, or success criteria.
