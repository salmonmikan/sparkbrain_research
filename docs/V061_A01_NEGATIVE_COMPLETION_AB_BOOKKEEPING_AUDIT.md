# v0.6.1 A01 — Family-A / Family-B Negative-Completion Bookkeeping Audit

## Scope

This is a SUB-owned, outcome-independent bookkeeping audit. It does not create a scientific identity, authorize execution, reinterpret immutable evidence, or declare programme negative completion.

Audited authorities:

- Family-A transient-return-address proposal and terminal P4 status;
- Family-B Generation-1 pre-START static-reduction closeout;
- `CandidateDisposition`, `NegativeCompletionProgramme`, and `assess_negative_completion` in `src/sparkbrain/evaluation/v061_premechanism_admission.py`;
- `docs/V061_PREMECHANISM_ADMISSION_AND_NEGATIVE_COMPLETION.md`.

The audit intentionally does not inspect or modify the active Family-C scientific object.

## Finding

The current bookkeeping schema can represent an ordinary executed Family-A P4 terminal disposition in principle, but it cannot faithfully represent the Family-B Generation-1 pre-START static-reduction closeout. In addition, `NegativeCompletionProgramme.completed_families` is not cross-validated against dispositions, so current family-coverage accounting is not sufficient by itself for a future programme-level negative-completion declaration.

No synthetic `CandidateDisposition` should therefore be created for Family-B under the current schema.

## Family-A mapping

Family A is `transient-return-address`. Its proposal was prospectively bound with specification SHA-256:

```text
2794d1596227eab17c68c46d6874662c3669656edb49e28425f1ef613b66c5dc
```

The consumed terminal candidate is:

```text
a01-md002-p4-merged-lineage-selective-resolution-candidate-001-v1
```

Canonical status records P2 and P3 positive development evidence and P4 terminal negative evidence:

```text
UNSUPPORTED_EN_BLOC_MERGED_CREDIT
```

For an executed candidate that has authoritative phase results, the current `CandidateDisposition` shape can express a P4 terminal path as:

```text
mechanism_family = transient-return-address
proposal_specification_hash = 2794d159...
non_privileged = true
p4_passed = false
p5_assessed = false
p5_reduced_to_explicit_memory = false
```

The remaining P1/P2/P3 booleans must be populated only from their canonical authorities. This audit does not infer or manufacture a missing phase boolean from later status prose. In particular, the bookkeeping object should not be instantiated until all required P1-P4 boolean values have exact evidence provenance.

Structurally, however, Family-A's terminal mode is compatible with the current schema: it is an executed P1-P4 candidate with a terminal P4 result, and P5 is not admissible after P4 failure.

## Family-B mapping fails closed

Family B is `distributed-field-trace`. Generation-1 closed as:

```text
classification: REJECT_BEFORE_STARTED_STATIC_REDUCTION
identity: a01-family-b-distributed-field-trace-gen1-v1
STARTED: false
identity_consumed: false
one_way_execution_allowed: false
```

This is explicitly an admission-level static reduction, not a P1/P2/P3/P4/P5 measurement.

The current `CandidateDisposition` has unconditional booleans for:

```text
p1_passed
p2_passed
p3_passed
p4_passed
```

but no `*_assessed` state for P1-P4 and no terminal/admission classification. Therefore every attempted Family-B encoding is semantically wrong:

- setting any P1-P4 field `false` would falsely turn `NOT_ASSESSED` into a measured phase failure;
- setting them `true` would fabricate phase passes that never occurred;
- `p5_assessed=true` would fabricate a P5 assessment;
- `p5_reduced_to_explicit_memory=true` is both too narrow and invalid here: the closeout was a pre-START recurrent-null static reduction, not an executed P5 explicit-memory reduction.

Accordingly:

```text
Family-B CandidateDisposition under current schema: DO NOT CREATE
```

The unconsumed Family-B identity must remain unconsumed and must not be converted into a synthetic failed candidate merely for bookkeeping convenience.

## Family-coverage validation gap

`assess_negative_completion` computes family coverage only as:

```text
set(programme.completed_families) == REQUIRED_NEGATIVE_COMPLETION_FAMILIES
```

`NegativeCompletionProgramme.validate()` checks uniqueness and validates each disposition, but it does not require:

1. every `completed_family` to have a corresponding evidence-backed disposition or terminal record;
2. every disposition's family to appear in `completed_families`;
3. exactly one or an otherwise explicitly governed set of terminal records per completed family;
4. a distinction between executed phase failure and pre-START admission rejection.

The existing unit tests also demonstrate that full family coverage can be declared independently of the mechanism-family values of the supplied dispositions. Consequently, `completed_families` is presently a caller assertion rather than an evidence-derived coverage proof.

This is harmless while `candidate_programme_complete=false`, but it is not strong enough to support a future `stop_stronger_field_claim=true` decision without additional bookkeeping semantics.

## Required bookkeeping prerequisite before programme-level negative completion

Before a future programme-level negative-completion declaration relies on Family-A / Family-B / Family-C terminal states, the accounting layer should gain an outcome-independent way to represent terminal family disposition without falsifying phase history. A minimal design should distinguish at least:

```text
EXECUTED_PHASE_FAILURE
EXECUTED_P5_REDUCTION
PRE_START_STATIC_REDUCTION
PRE_START_OTHER_REJECTION
```

and should preserve, where applicable:

```text
started / not-started
identity consumed / unconsumed
phase assessed / not-assessed
reduction comparator class
canonical authority/ref
proposal specification hash
mechanism family
```

Family coverage should then be derived from, or validated against, these evidence-backed terminal records rather than accepted as a free tuple of family enum values.

This audit does not prescribe the exact implementation API. Changing evaluator semantics is a separate prospective governance/readiness decision and must not be used to retroactively alter any Family-A or Family-B scientific result.

## Safe current bookkeeping state

Until such accounting is prospectively defined:

- Family-A may be documented as structurally representable, but an actual `CandidateDisposition` should only be emitted from exact authoritative phase facts;
- Family-B must remain a canonical pre-START terminal record outside `CandidateDisposition` rather than be coerced into P1-P5 booleans;
- `completed_families` must not be used alone as evidence that A/B/C coverage is scientifically complete;
- no programme negative-completion stop should be declared from the current schema merely by setting all family enum values in `completed_families`.

## Independence and integrity boundary

This audit changes no scientific evidence and is not required for MAIN to proceed. It does not touch Family-C implementation, MAIN CI/binding, consumed identities, STARTED/control refs, freeze/preserve/formal/evidence authorities, scorers, nulls, or experimental workflows.
