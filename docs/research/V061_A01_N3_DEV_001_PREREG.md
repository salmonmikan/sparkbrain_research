# N3-DEV-001: prospective recurrent adapter development diagnostic

Date: 2026-09-09. Status: EQUATIONS_AND_MATRIX_FROZEN_EXECUTION_DISABLED.
This new development diagnostic does not execute MD-001, MD-002 or candidate-003.
The supplemental MD-002 P2/P3/P4 interventions and full P5 remain pending.
No outcome has been inspected. Source-only implementation and independent review
must precede a separate source-pin execution authorization record.

## Model and admissible interface

Two opaque local-path slots, assigned by the supplied ordered path tuple (never
lexical sorting or semantic ID parsing). A bijection renames that tuple in place.
Reciprocal fixed edges (0,1),(1,0). Python random.Random(12001) draws uniform(-1,1)
in edge order; scale both by .75 / maximum incoming absolute row sum. This is
extracted from ResourceMatchedSparseReservoir at source
2f2aae612ee6e0f08453c855a9910d965fa89bec, blob
b703a326bbeae1dabc5b8a50055aaeb1a3ae310d. No RV01 training/outcomes are imported.
For every clock tick, simultaneously update both hidden units:

    h'_i = .2*h_i + .8*tanh(x_i + sum_j W_ji*h_j)

x_i=1 for active supplied opaque paths, otherwise zero. Empty input is permitted.
Episode construction zeros h and the two learned diagonal readout weights w.
There is no hidden reset between activation, delay, evidence and probe.
Only actual exact-parent external evidence classified by the unchanged
A01TransientCreditBridge supplies eligible paths and matched bool. For each
eligible i, y is +1 for anonymous match and -1 for anonymous contradiction:

    w'_i = clip(w_i + .25*(y-tanh(w_i*h_i))*h_i/(1e-8+h_i*h_i), -2, 2)

All other weights remain unchanged. This signed diagonal readout is a prospective
adapter change from the source family's next-token readout, not a drop-in claim.
The live readout is r_i=(1+tanh(w_i*h_i))/2; gain=2*r_i. Existing A01 base local
confidence is multiplied by gain and capped at 1. Querying does not advance h.
A previously proposed zero-state query was rejected BEFORE source/outcomes;
recurrence here can influence both learning and current inference.

N3 owns no world-response mapping, semantic lineage role, expected winner,
future target, reward or candidate output. Exact ancestry routing and prior C
classification are shared with A01; the comparison cannot discriminate routing.
All numeric state, ID mapping, config, hidden vector and clock are charged.

## Fixed matrix and chronology

36 cases: evidence in confirmation, contradiction, absence, replay; delay in
0,1,4 ticks; actual boundary proposal ancestry in first, second, both supplied
paths, nested in that order. Each case executes independent A01 and N3 arms
from fresh identical temporal and anonymous-C histories, 72 arm rows total.
One seed 12001, no replicates, selection, hyperparameter search or statistics.
Each case registers two real local-path proposals and a boundary carrying the
selected proposal IDs. This is shared exact-parent input, not world causality
or physical-trajectory discrimination.

At boundary time 20ms, eligible path activity advances h once; then d empty-input
ticks advance h. Returned evidence time is 22+d ms. Confirmation returns the
established anonymous target; contradiction returns a different opaque target.
Absence delivers nothing. Replay attempts an endogenous-unconfirmed event and
must be rejected by the actual bridge. Probe occurs immediately after the
attribution cut, with identical external shared-root cue at 300ms. The cue
queries frozen local confidence and does not advance adapter time. Adapter tick
is an explicitly discrete diagnostic clock, not claimed as physical ms fidelity.
No learned-state mutation occurs during probes.

## Resource and artifact contract

Per arm retain every initialization, activity, idle, pre-evidence, post-evidence,
and post-probe checkpoint; actual state dictionaries include base temporal,
C, ledger, bridge, and N3 config/mapping/weights/hidden/clock/counters. No actual
Field simulation or scheduler is executed; those absent components are not
silently invented. This is a local-competition adapter diagnostic only.
Canonical JSON: sorted keys, compact separators, ensure_ascii=false,
allow_nan=false, no LF for measurement; output JSON files add one LF.
Normalized payload recursively charges number8/bool1/null0, string UTF8+8,
list8+children, dictionary8+all key/value charges. This explicit logical payload
is not resident RAM. Python resident duplicates and exact shared-router
operations are unavailable and must be null, never zero or matched=true.
N3 actual hidden writes, learned writes, recurrent edge evaluations and update slot-index
search comparisons are instrumented (validation/query lookups excluded). A01 counters remain in actual snapshots;
no N3 operation count is copied to A01. Shared-router operations and transient
scratch occupancy are unavailable; full resource matching is NOT_EVALUATED.
Whole-arm tracemalloc peak is descriptive interpreter allocation, not an exact
matched transient-state measure. Wall-clock latency is measured per attribution
and probe using perf_counter_ns; no hardware-energy claim.

Execution ceilings (feasibility only): two path slots, 64 adapter ticks,
65536 canonical checkpoint bytes per cut, 36 cases and 72 complete arm rows.
Any overrun/identity/input failure aborts before publishing outcomes. No budget
is raised after inspection. Model numeric capacity N3 fixed2+learned2+hidden2
versus A01 up to4 learned support counters is already unequal.

Exact output inventory in a new no-clobber directory: protocol.json (copy),
source_manifest.json, raw_rows.jsonl, summary.json. Each row includes case spec,
arm, admissible input hash, complete checkpoint cuts, bridge resolution/replay
rejection, actual confidence before/after, resource category measurements,
wall-clock attribution/probe timings. Summary reports per-case A01/N3 confidence
differences descriptively, control learned-state equality, complete row count,
and resource matching NOT_EVALUATED. No universal supported/winner/P5 pass field.

## Engineering checks and interpretation

Before execution, test recurrence history and recurrence-off perturbation,
zero-input dynamics, live hidden effect on readout, exact save/restore,
nonmutating inspection/probe, identifier bijection, unknown/duplicate path and
malformed state rejection, and true bridge external/replay/fallback/no-prior
admissibility. Synthetic engineering inputs use separate names from runner.
The independent review records exact code/protocol hashes before outcomes.
A successful run shows only how this fixed recurrent learner responds to this
small admissible-input matrix. Differences can falsify this adapter's equality,
not generic recurrence, Field emergence, or upstream causal routing. Adverse
responses are retained. Incomplete full MD-002 remains not evaluated.

## Pre-execution failure retention clarification

Frozen before outcome execution: 120-second wall-clock deadline and 256MiB
whole-arm tracemalloc peak ceiling. Each completed arm is retained. A failed
arm stops the matrix, retains prior complete raw rows and an explicit failure
record in summary; no retries or ceiling changes. Incomplete matrices are
NOT_ACCEPTED. Identity/preflight failures run no model and create no outcomes.
Counters named update_slot_index_comparisons count only update-side index
search, not validation/query lookups; overall lookups remain unavailable.

Limits are checked between/after finite bounded arm calls, not OS-enforced hard
process limits. Completed rows are appended to a fresh staging JSONL after each arm and atomically
published on success or caught failure; a process crash may leave staging, not an
accepted result. This is not a per-step durable journal.
Control equality is null unless all 36 control arm rows completed.
