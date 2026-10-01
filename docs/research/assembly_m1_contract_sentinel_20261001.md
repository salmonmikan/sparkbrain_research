# Executable temporal-inlet contract sentinel: frozen cases

Date: 2026-10-01 UTC. **SYNTHETIC CONTRACT TEST / NONCANONICAL / NON_EVIDENTIARY**.
Scientific credit: **0**. This is not a real M1/v0.5 integration or model experiment.

## Scope fixed before execution

Reference: [merged inlet design](assembly_m1_interface_design_20261001.md), PR #174,
merge `9073a563dea936c6f76610387503f9583c0d3966`. Runtime source remains fixed to that
main snapshot. AGENTS SHA-256 is
`ceb4a6b2f14b0efa25148cf0f652f75133e00d11360a020ef6aa6adcdb34a002`;
the fresh Human Directive branch head remains
`8ce979b9ec0bc7eede5225c0403698f8886d3e8d`.

This separately requested cloud prototype uses only its dedicated script, tests and
research artifacts. It is not a scheduled role, build allocation, or scientific object.
PR #164, checkpoint work, weight/delay experiments, shared ledgers and runtime files are
not write targets. No SparkBrain, learned backend, world, dataset or model is imported.

The implementation will contain one small coordinator and explicitly named fake temporal
and fake M1 consumer components. A test-supplied two-number sentinel is returned by the
fake temporal component. The fake consumer compares those numbers in the sensory and
route copies and applies the specified agreement/abstention rule. It does not learn an
assembly or reproduce M1's prototype/router dynamics. Its receipt method records which
previously supplied context received credit, without learning a predictive model.

That intentional construction tests the wire, preconditions and state boundaries, not
whether a real representation is useful. A pass must be described as **synthetic contract
conformance**. The real reference path's semantic ID effects and v0.5's omitted checkpoint
state remain unresolved, as documented in PR #174.

## Fixed input and finite cases

[Machine case freeze](../../artifacts/research/assembly_m1_contract_sentinel_20261001/case_freeze.json)
is the exact case inventory. Default original inputs are sensory `signal=0` and route
`(0,)`; pulses contain a single Q pulse at 40 ms, cutoff 40 ms, decision 72 ms, receipt
80 ms, and subsequent windows start at 200 ms multiples. Sentinel A is `(1,0)`, B is
`(0,1)`, and removal is `(0,0)`. No random generator, seed sweep or target search is used.

Twenty-two named cases cover accepted A/B inputs; sham, both-consumer and one-consumer
swaps; zero context; actual configured limits; ID-renamed fake decision paths; pending
credit and receipt idempotence; clock/identity rejections; injected rollback; actual pure
rendering; malformed representation rejection; channel-schema preservation; and one-pending
backpressure. All case inputs and expected outcomes are fixed before executing the suite.

Fakes store all mutable operational data in explicit owned fields. The coordinator's
transaction snapshot includes every owned fake and coordinator field. Tests compare full
before/after inventories under faults. No external resource, shared alias, live runtime,
thread, generator, network connection or native checkpoint participates. Complete rollback
therefore means completeness for these declared fake states only. It certifies nothing
about an arbitrary backend's state serialization.

## Bounds, validation and stop rule

- Standard-library prototype; pytest for tests only; no SparkBrain imports
- At most 64 fresh coordinator fixtures across this fixed suite; at most four input pulses
  and four observations per fixture; no stochastic or result-responsive search
- No runtime/source/config repair; no retrospective change to expected outcomes to make
  the suite pass; an implementation defect may be repaired while retaining the frozen cases
- Run only the dedicated tests and scoped lint/audit; do not run real M1/v0.5 or formal tests
- Record every case's accepted/rejected boundary and exact test command after execution
- Stop after this finite contract report and reviewed PR, or on a required change in scope

At initial freeze publication, implementation and tests are not yet executed. The case
freeze's commit must precede the first test run. Publication/CI does not authorize a real
producer, real M1 integration, scientific acceptance, or weakening any causal control.
