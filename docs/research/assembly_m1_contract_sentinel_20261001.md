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

## First execution: bounded result

The 22-case freeze was published and independently fetched at
`7420f176334e5b54ed5f608387d959794db90faf` before execution. The first suite run passed
all 22 cases, instantiated 28 fresh coordinator fixtures, and imported no module named
`sparkbrain` or beginning with `sparkbrain.`. The measured pytest invocation took
0.165950 seconds; this excludes importing pytest and preparing the wrapper. It is a
small test-run duration, not a performance or resource-efficiency result.

The [JUnit output](../../artifacts/research/assembly_m1_contract_sentinel_20261001/junit.xml),
[case-by-case assertion results](../../artifacts/research/assembly_m1_contract_sentinel_20261001/case_results.json),
[pre-run source hashes](../../artifacts/research/assembly_m1_contract_sentinel_20261001/execution_manifest.json)
and [post-run hashes/module inventory](../../artifacts/research/assembly_m1_contract_sentinel_20261001/execution_result.json)
are preserved. Input cases and both source files had equal pre/post hashes.

| Boundary | Accepted or rejected in the fake-only tests |
|---|---|
| Representation wire | A selected alpha; B selected beta; unchanged sham matched exactly; swapping both feature copies changed action |
| Agreement gate | Swapping only one copy produced disagreement abstention; all-zero context abstained |
| Configured headroom | 3/3 ceilings accepted one original plus two coordinates; route ceiling 4 rejected three originals; ceiling 2 rejected before backend work |
| Identity | Renamed event/receipt IDs preserved the specified fake numeric projection and outputs; ID ledgers differed as intended |
| Pending credit | The delayed receipt recorded exactly the earlier adapted observation, with one extraction and one credit operation |
| Receipt integrity | Identical replay returned the prior revision unchanged; changed receipt content and wrong pending event were rejected unchanged |
| Clock | A pulse after cutoff and feedback at decision time were rejected unchanged |
| Transaction | Faults after backend advance, consumer observe, consumer feedback and ledger commit restored the complete declared fake inventory |
| Observation | The actual pure render/export function left state, outputs and counters unchanged |
| Remaining boundaries | Malformed context, reserved channel, changed original channel schema and a second pending observation were rejected as specified |

The execution used a small Python wrapper around `pytest.main` to record source hashes,
fixture count and imported modules. The command stored in the manifest is the equivalent
pytest CLI invocation. Reproduce only these fake cases with:

```bash
python -m pytest -q tests/test_assembly_m1_contract_sentinel.py
python -m ruff check scripts/assembly_m1_contract_sentinel.py tests/test_assembly_m1_contract_sentinel.py
```

The toy readout deliberately encodes the sign/agreement rule. A passing swap demonstrates
that the adapter passes the representation into those fake consumers; it is not evidence
that real M1 uses a learned representation, generalizes, or improves. The fake receipt
records credit but does not learn predictions, emulate SB002's content-conflict policy,
or repair any real runtime. Full fake inventory comparison is not a native v0.5 checkpoint
or arbitrary-backend rollback guarantee. Real producer and real M1 tests remain outside
this prototype. Exact-head peer/Codex review and CI are separate publication checks.

## Prospective correction after source review

Independent review found that checking only the outer tuples allowed a mutable pulse-list
record to be retained by the fake backend and pending window. The original 22-case pass
therefore does not establish isolation against malformed nested input records. Its source
hashes, JUnit and results remain preserved; no prior expectation is changed.

The [v2 case amendment](../../artifacts/research/assembly_m1_contract_sentinel_20261001/case_amendment_v2.json)
adds only C23, with four explicitly listed malformed/mutable pair/triple inputs. Before
backend advance, the correction must require each sensory row to be an immutable length-two
tuple and each pulse row to be an immutable length-three tuple. All 23 cases retain the
same 64-fixture ceiling. This amendment will be published before executing the corrected
suite; it is ordinary prototype input-validation repair, not scientific rescue or a new
model experiment.

## Corrected execution: 23 cases

The C23 amendment was published and independently read back at
`cda8776fb4c2191412e2cad4c0fb757a2b1e58bb` before the corrected suite ran. That commit
also preserves the exact first-run prototype/test source, including the input-isolation
gap. All first-run artifacts and the original 22-case freeze remain unchanged.

With strict nested record validation, all **23 cases passed**, using **32 fake fixtures**.
C23 rejected all four mutable/malformed record variants before backend advance, with
identical full before/after state. The measured pytest invocation was 0.137174 seconds,
with zero SparkBrain module imports and unchanged pre/post source hashes. Original
expectations were not relaxed.

Corrected evidence is separate:
[JUnit](../../artifacts/research/assembly_m1_contract_sentinel_20261001/junit-v2.xml),
[case results](../../artifacts/research/assembly_m1_contract_sentinel_20261001/case_results-v2.json),
[execution manifest](../../artifacts/research/assembly_m1_contract_sentinel_20261001/execution_manifest-v2.json),
and [execution result](../../artifacts/research/assembly_m1_contract_sentinel_20261001/execution_result-v2.json).
The record preserves the exact `pytest.main` arguments; temporary workspace paths are
execution provenance, not required reproduction locations.

The useful outcome is a small, exercised contract skeleton and explicit rejection cases
that can guide a later real adapter. It supplies neither real temporal representation
extraction nor M1 runtime replacement, real checkpoint completeness, global identity
neutrality, learned adaptation, assembly-specific causality, or predictive benefit.

Independent source review accepted the corrected boundary and separately reran the same
23 cases: 32 fixtures, zero SparkBrain imports, and unchanged source hashes. No blocking
finding remained. Scoped Ruff, whitespace and report-link checks passed. Exact-head
Codex review and CI remain pending at this report revision.
