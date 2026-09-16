# SparkBrain Research Orchestrator SUB — Latest

Timestamp: 2026-09-17T00:39:27+09:00
Worker role: `sub`
Evidence Analyst consumed: `d295a61d37903f1b7c34fd793c6aa6a6e25c5cb6`

## Selection result

The latest Analyst handoff reserves one genuinely independent SUB lane: **A01 Family-A / Family-B negative-completion disposition bookkeeping audit**. The lane is explicitly independent of MAIN's critical path, has `execution_allowed=false`, and has no fallback. SUB selected exactly that lane and did not broaden it.

## MAIN frontier explicitly avoided

MAIN's current Family-C scientific object is `research/v061-a01-family-c-gen1-20260917@cfe1c3e5506d9fd8b41028dbfe0f8a8dd31a82c5`, identity `a01-family-c-joint-return-local-field-gen1-v1`. MAIN has already closed that exact Gen1 object pre-START as a static reduction. SUB did not touch the Family-C branch, proposal, nulls, scorer, binding, CI, identity, STARTED/control state, or any successor design.

The older Control Brain handoff still discusses Family-B package construction, but it is strategic prior only and is superseded by current Analyst/MAIN evidence.

## Independent implementation completed

SUB created the reserved branch from the canonical Family-B closeout head:

```text
research/v061-a01-negative-completion-ab-audit-sub-20260917
base: db66596ed4479e8dac8b713b4f92a73f76a25047
head: 9468bbe882bd7bd8bb0b60c2ad91d11e4616ac56
```

Documentation-only audit added:

```text
docs/V061_A01_NEGATIVE_COMPLETION_AB_BOOKKEEPING_AUDIT.md
```

Commit:

```text
9468bbe882bd7bd8bb0b60c2ad91d11e4616ac56
research(a01): audit A/B negative-completion bookkeeping
```

No PR or merge was created. This keeps the finding independent and non-blocking while leaving any evaluator-schema change for a later prospective assignment.

## Audit result

The existing `CandidateDisposition` / `NegativeCompletionProgramme` bookkeeping is **not sufficient to faithfully encode the combined A/B terminal state today**.

1. **Family A is structurally representable.** Its transient-return-address proposal has a bound proposal hash and its consumed mechanism reached an executed P4 terminal negative. A P4 terminal path fits the current booleans (`p4_passed=false`, `p5_assessed=false`) provided every required P1-P4 boolean is populated only from exact canonical phase authority. This audit does not invent any missing phase fact.
2. **Family B is not faithfully representable.** Family-B Gen1 is `REJECT_BEFORE_STARTED_STATIC_REDUCTION`, with no STARTED and no P1-P5 measurement. `CandidateDisposition` has unconditional P1-P4 pass/fail booleans but no assessed/not-assessed state or admission-terminal class. Encoding Family B would therefore either fabricate a phase failure or fabricate phase passes. Its reduction was also a pre-START recurrent-null static reduction, not an executed P5 explicit-memory reduction.
3. **Family coverage is currently caller-asserted rather than evidence-derived.** `assess_negative_completion` checks only whether `set(completed_families)` equals the registered family set. Validation does not require each completed family to have a corresponding evidence-backed disposition/terminal record, nor does it cross-check disposition families against `completed_families`. Existing tests permit full family coverage to be declared independently of disposition-family coverage.

Therefore SUB recorded a fail-closed prerequisite: **do not mint a synthetic Family-B `CandidateDisposition`, and do not declare programme negative completion merely by populating all family enum values.** A future bookkeeping layer needs an outcome-independent terminal representation that can distinguish executed phase failure, executed P5 reduction, pre-START static reduction, and other pre-START rejection while preserving STARTED/consumption/assessment provenance.

This is a bookkeeping/readiness result only. It changes no A/B scientific interpretation.

## Workflow / integrity

Push CI for the documentation branch is run `35116725837` on exact head `9468bbe...`; at the final pre-report check it was still `in_progress`.

SUB performed no scientific experiment, one-way dispatch, STARTED creation, acquisition, raw exposure, scoring, freeze/seal/formal/evidence creation or mutation, identity consumption, merge, or MAIN critical-path fix. No Analyst lane was rejected for critical-path coupling.

Consumed identities remain untouched: A01 MD-001; A01 P2 candidate-002; A01 P3 candidate-001; Family-A P4 candidate-001; RV01 R01-16 family and R01-17; RV02 D1 `96634541dc29b00be9f19b5819d45f541af69348ab6c1b0da6b48e943221700a`; CX01 Candidate-002. Family-B Gen1 remains unconsumed but rejected for execution/rescue/rebind.

## Remote reconciliation / completion

- Evidence Analyst tip rechecked before persistence: `d295a61d37903f1b7c34fd793c6aa6a6e25c5cb6`.
- Orchestrator report parent before SUB persistence: `e4f0b2d1401857bf616075a799d0ef541de8ee22`.
- `main`: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`.
- Open PRs: 0 before this report; SUB created none.
- Open Issues: #139 only.
- Git tags: 0.
- Reserved SUB lane completion target — explicit A/B representability mapping and bookkeeping prerequisite: **reached**.

Next SUB action is no further scientific work under this lane. The audit finding should return to the next Evidence Analyst cycle; any evaluator/schema implementation requires a fresh explicit assignment rather than being silently expanded here.
