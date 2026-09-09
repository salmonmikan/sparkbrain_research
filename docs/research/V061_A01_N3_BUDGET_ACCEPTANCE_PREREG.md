# A01 N3 budget and independent technical acceptance preregistration

Date: 2026-09-09. Source baseline: c05abe90c9ef904aead27df5176d7385aa06fb64.
Status: ENGINEERING_CONTRACT_FROZEN; MD-002 mechanism execution remains disabled.
This prospective contract permits adapter implementation and engineering invariant tests.
It does not provide formal execution-seal authority or replace the MD-002 binding.
No mechanism outcomes informed this contract. MD-001 evidence is immutable.

## Accounting boundary

Compare complete arm runtimes at identical input/event-clock cuts: after initialization,
before and after every external attribution, after every elapsed step, and before/after
probe. Reset boundaries must be identical and declared. State retained between calls is
persistent for this accounting, even if called a transient eligibility or hidden vector.
Report episode-resettable and cross-episode state separately; neither is free.

| Category | Included items |
|---|---|
| Fixed weights | All recurrent/input/readout constants or arrays used by the mechanism |
| Learned weights/state | A01 support counters; N3 learned readout; any adaptive statistic |
| Persistent dynamic state | Hidden vector, pending eligibility, clock, deduplication state |
| Config/topology/router | Seeds, hyperparameters, edges, identifier mapping, indices, caches |
| Common runtime | Actual L base state, C state, provenance ledger, F state, scheduling/output state used by each arm |
| Transient working state | Live intermediate vectors, score maps, ancestry traversal and update scratch |
| Instrumentation | Counters and retained audit records; reported separately and in resident total |

A category belongs to exactly one row. Each arm must identify its actual objects and
serialization paths; empty/missing objects cannot be filled using candidate measurements.
A shared object is counted once per standalone arm, not once for the paired process.
Common cost subtraction is allowed only with verified identical code and object-content
hashes at the relevant cut; otherwise report each arm separately. Read-only derived
indices remain resident cost. Regenerable weights are not zero-cost.

Report (a) fixed/learned numeric scalar counts, (b) retained dynamic numeric counts,
(c) identifiers/topology/config counts and bytes, (d) canonical checkpoint bytes, and
(e) transient high-water occupancy separately. Numeric payload uses eight bytes per
finite float and bounded integer, one per bool; strings use UTF-8 length plus an
explicit length field. Integers outside signed 64-bit fail this normalized format.
Canonical JSON uses sorted keys, compact separators, UTF-8, allow_nan=false, no LF.
Canonical bytes are a representation-size measurement, not RAM or physical energy.
The complete checkpoint includes all state required for deterministic continuation.
Actual resident duplicates and temporary allocations must be reported separately when
not represented in the checkpoint; absent instrumentation is unavailable, never zero.

## Resource interpretation fixed before outcomes

The original 444-byte reservoir payload and 155-byte A01 support payload have different
scopes. They establish no size ordering. Normalization must not rewrite either record.
The proposed K=2 N3 has two fixed weights, two learned weights and two retained hidden
scalars, whereas A01 has four support counters at full two-path occupancy. This already
prevents asserting equal incremental persistent scalar capacity for that design.

The primary matched-null test requires N3 to use no more whole-system normalized
persistent payload, canonical checkpoint bytes, transient peak, update operations,
lookup operations, observations, elapsed steps, active outputs and generated events
than A01 on every paired episode, with equal evidence and I/O privilege. Incremental
mechanism cost must also be reported, without using large common costs to hide a
mechanism overhead. Exact equality and no-greater-than matching are distinct fields.
Missing instrumentation makes matching NOT_EVALUATED, not true.

Equal ceilings are budget feasibility, not measured resource matching. An oversized
adapter may be implemented and tested for engineering behavior, but is marked
UNMATCHED_ENGINEERING_ONLY; it cannot bind N3 for complete P5. No padding A01 state,
post-outcome ceiling increase, omitted hidden state or free deterministic weights may
repair a mismatch. A later alternate matched architecture needs a new prospective
contract before its outcomes. Preserve adverse feasibility results.

## Evidence, timing and mechanism discrimination

The adapter receives only the same opaque eligible-path activation, pre-observation
anonymous match/contradiction classification and elapsed event clock available to A01.
The exact-parent provenance router must be shared or independently shown equivalent.
No expected winner, evaluator truth, future world map, candidate output, semantic ID,
or extra supervision is admissible. No next-token training through future input.

Activation/idle recurrence may alter hidden dynamics on absence or replay, but only
admissible external evidence may alter learned readout. Tests must distinguish learned
state from dynamic state; demanding all hidden state remain fixed would suppress the
very recurrent null being tested. Resetting hidden state at each update is prohibited
unless explicitly preregistered as a different comparator.

Freeze equations, topology, initial weights, sign update, confidence mapping, tick
order, seeds, reset semantics and admissibility behavior in a source-adjacent adapter
contract before implementation. Inherited defaults are not a completed equation.
No parameter search on MD-001/002 results is allowed.

Full discrimination remains conditional on the separately bound MD-002 matrix:
P1 exact evidence and negative controls; P2 actual world-map interventions with fixed
initial history and evidence-withheld controls; P3 independently executed third R-only
transplant; P4 genuine merged ancestry and later separating/inseparable evidence;
P5 identifier bijections, actual physical trajectories, unseen combinations and
interference. All applicable traces, latency, ambiguity, contamination and state loci
must be compared. Endpoint agreement alone cannot establish recurrent equivalence.
Invalid/missing stage coverage is NOT_EVALUATED. Valid adverse response is retained.
N3 success cannot compensate for A01 P1-P4 invalidity. No emergence claim follows.

## Independent technical acceptance checklist

Review source before mechanism outputs. Record reviewer, exact source SHA, protocol
SHA and reviewed file manifest; this review is not a formal seal.

1. Recurrence has history dependence and zero-input elapsed-step behavior, plus a
   recurrence-ablated engineering control demonstrating the term is actually used.
2. Absence/replay/fallback/unknown ancestry cannot train; exact eligible evidence can;
   updates never consult evaluator-owned fields. Input rejection is tested.
3. Complete save/restore reproduces continuation, hidden state, weights, clock and
   counters; snapshots and audit inspection do not alter future behavior.
4. Identifier permutation remaps the complete declared topology and mapping, not just
   display strings. Output values are derived from the comparator itself.
5. Measured categories reconcile to complete payload and runtime inventory. Injected
   oversized weights, extra hidden state, missing counters and dishonest common-state
   declarations fail validation; unavailable values cannot become matched=true.
6. Operations count actual reads/writes and recurrence steps. Peak occupancy and
   observation-to-effect latency derive from executed transitions, not stage labels.
7. Frozen budgets reject before mechanism outcome generation; raw engineering results
   remain distinguishable from capability runs. Missing source pins fail closed.
8. MD-002 execution requires its complete matrix, controls, source-bound runner,
   artifact schema and independent technical review in addition to this checklist.

Acceptance is componentwise: family-valid, input-valid, checkpoint-valid,
instrumentation-valid, budget-feasible, resource-matched and matrix-ready. A single
SUPPORTED label must not collapse these distinctions. The current document does not
assert any adapter acceptance or authorize a MD-002 run.
