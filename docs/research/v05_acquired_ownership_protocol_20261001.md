# Prospective ownership of an acquired v0.5 producer

2026-10-01 UTC. **EXPLORATORY / NONCANONICAL / NON_EVIDENTIARY**; scientific credit **0**.
Fresh diagnostic: `v05-acquired-ownership-20261001`.

## Question and scope

Can a private, single-threaded owner preserve the complete supported v0.5 producer graph
when postprocessing or actual processing fails, and publish one validated successor without
leaking mutable caller/output objects into that acquired state?

[PR177](https://github.com/salmonmikan/sparkbrain_research/pull/177) established a bounded
[acquisition sequence](v05_paired_coverage_results_20261001.md), not a resumable snapshot or
an ownership guarantee. This is a separate prospective test using that input shape, fresh
receipt/episode IDs and an independently verified maturity gate. [PR176's earlier block](v05_owned_state_results_20261001.md)
and unexecuted P5/P6 remain unchanged. Neither prior probe runner will be imported or run.

This tests an isolated prototype transaction around the real acquired producer, with no
production runtime edit, M1 call, native restoration or scientific promotion. The exact
PR177 configuration disables v0.5 prediction/action/reward modulation. Their learned state
therefore remains dormant. Acquired assemblies, pending activation, field learning and
base v0.4 action diagnostics belong to the owned graph and are included. No predictor/action
learning usefulness, supported snapshot API or cross-component atomicity claim follows.

## Exact finite fixture

The [complete protocol](../../artifacts/research/v05_acquired_ownership_20261001/protocol.json)
SHA-256 is `723859ed058957a4bf832ef09a8b42407e5fde3b0a5d8186de1edcd5f39c0a3f`.
It freezes all 157 runtime source hashes at
`9549a2bf6bc76cb7b5714742f3ed54decd618263`, all twelve constructor configuration projections,
input fields, IDs, branch order, clocks, copy limits, fault placement and decision rules.

One private root receives three pairs of positive Q pulses, magnitude 1.2, null location,
zero supplied novelty/prediction error and initially empty metadata:

| Episode | Raw pulse times, ms | Episode ID |
|---|---|---|
| Prefix 1 | 8, 12 | acquired-ownership-20261001-01 |
| Prefix 2 | 208, 212 | acquired-ownership-20261001-02 |
| Prefix 3 | 408, 412 | acquired-ownership-20261001-03 |
| Every branch's suffix | 608, 612 | acquired-ownership-20261001-04 |

The new source ID is `acquired-ownership-probe`. Each pair is one call, with the unchanged
seed 920041, settle 32 ms and call flags `learn_assembly=True`, `learn_field=True`,
`explore_action=False`, empty metadata. No outcome is delivered. The four suffix branches
use exactly the same input bytes/episode ID from separate copies of the same acquired
beforestate; they are not independent statistical replicates or extra independent episode
evidence within one graph.

After prefix 1, no candidate/activation is mature and pending activation is null. After
prefix 3, require an actual mature, unsuppressed pending activation resolving to a candidate
whose episode-ID set is exactly the three prefix IDs. Its prototype and pending activation
must be live objects in retained results. Missing coverage stops before copying or suffixes.
No extra acquisition is permitted.

Successful field end clocks must be 44, 244, 444 and 644 ms. Receptor Q's corresponding last
observation clocks are 12, 212, 412 and 612 ms. Unit clocks, candidate timestamps and queued
event times remain separately recorded; none is substituted for another clock.

## Complete owned-state oracle

Use exact equality of canonical **typed graph bytes**, retaining the complete inventories:
known classes and all instance fields; primitive types; dictionary/list/deque order;
deque capacity; set membership; repeated references; alias and separation structure.
Include queues/heap layout, live adjacency order, eligibility, receptor traces, field/unit
state, detector caches, results, pending objects, traces, configuration and dormant components.
Do not flush, sort, normalize or reconstruct state to make a comparison pass.

The source-bound [PR176 graph schema](../../artifacts/research/v05_owned_state_20261001/source_map.json)
has SHA-256 `af3e00d35f8272fc2819b6b059a1ac18c872343496ec7a99f8651c6edb14dd69`.
Independent source review found no omitted declared instance field in its listed classes.
Its GraphAudit/alias-inspection algorithm may be copied with explicit provenance into the
new dedicated runner; the old runner must not be imported or executed. Unknown types,
fields, custom copy hooks or external handles cause a stop, not an omitted-state fallback.

Do not use native checkpoints or runtime output hashes as the ownership oracle:

- Native v0.5 value snapshots omit owned regions documented by PR176
- `V05StepResult.state_hash` precedes result/trace append and episode-index increment
- `v04_result.field_state_hash` precedes v0.5 plasticity/homeostasis

These hashes remain ordinary output fields, not complete post-return state digests.
Source: [v05/brain.py](../../src/sparkbrain/v05/brain.py), lines 154–170, 220–244 and 271–298.

Readable identity witnesses supplement full graph equality. Include candidate prototype,
pending activation/action, each v0.5 result's actual v0.4 result, emitted/base input pulses,
actual buffered/retained spike links, connection/outgoing/incoming aliases, cascade memory,
and the separation of initial topology objects from mutable live units/connections.
Numeric object IDs or witness booleans alone are insufficient.

Preserve the acquired beforestate, then create **all four whole-brain copies before any
branch processing**, each with a new deepcopy memo from that unchanged original root.
Every copy must match the full beforestate bytes. Mutable identities must be pairwise
disjoint among root and all four copies, while references remain alive. Within-graph alias
structure must remain equal. Immutable primitive/tuple sharing is not mutable leakage.

## Four branches, in fixed order

| Branch | Single suffix operation | Required boundary |
|---|---|---|
| export_abort | Process copied caller inputs, preserve real result/full graph, validate mature suffix and detached output, then inject a unique export-validation boundary error | Actual candidate advancement; no commit; original owner/root exact |
| event_cap_abort | Preserve exact clone, replace only this private candidate's `max_events_per_run` with 1, preserve that state, then process identical copied inputs | Genuine processing exception and mutation beyond the config replacement; no commit; original exact |
| direct_reference | Process identical copied inputs directly on its separate copy | Retain detached output/full graph and actual mature suffix; original exact |
| commit | Process identical copied inputs, validate mature suffix/output/full graph, compare with direct reference, then assign owner pointer once and return only the validated detached tree | Exact direct equality before commit; external mutation isolation afterward |

For each successfully processed suffix in export_abort, direct_reference and commit, require
an actual mature, unsuppressed pending activation in the newly retained fourth result, and
a candidate containing exactly all four episode IDs. Retain the actual prototype alias.
Two equal null activations cannot pass mature-output coverage. Missing required suffix
coverage is a coverage block and stops remaining branches without retuning.

The only injected state override is branch 2's private candidate event cap. Preserve three
separate graph states: exact clone, after-cap replacement, and after the processing error.
The expected error is `RuntimeError("max_events_per_run exceeded")`. The failed graph must
change beyond the cap replacement: receptor Q has observed the two new pulses and reached
612 ms, while arrival counters/queue contents demonstrate actual processing mutation.
The source can raise while popping the second simultaneous arrival, before group delivery;
do not require a spike or a field-clock advance. Source:
[field.py](../../src/sparkbrain/v04/field.py), lines 270–293, and
[receptors.py](../../src/sparkbrain/v05/receptors.py), lines 61–78 and 126–137.

The export-boundary error is deliberately injected, not a claimed naturally occurring
runtime defect. The event-cap error must come from the real process call. Neither case
permits restoring a partial native snapshot or quietly swapping in a rebuilt original.
The transaction strategy is candidate abandonment, with the original graph never mutated.

## Caller ownership and commit placement

The accepted public input is an exact tuple of two exact SignalPulse instances whose actual
metadata dictionaries are exact, initially empty dicts. Check all frozen fields and IDs.
Deepcopy the caller pulse tuple before every prefix and suffix call; this is input detachment,
not an additional whole-brain copy. Keep originals for isolation checks. No arbitrary
object, custom handle, subclass or nonempty metadata is accepted in this bounded contract.

The private owner holds the producer pointer; it exposes no live brain/result/candidate
handle. All fallible model processing, output detachment, validation, graph inspection and
direct-reference comparisons occur before the single pointer assignment. After assignment,
return only the already validated detached primitive tree; do not place later validation or
caller mutation inside an abort handler that could pretend an already committed state was
rolled back. Postcommit failures are reported as such.

After the real return, mutate caller-owned objects only, with no additional model call:

- Both actual suffix caller SignalPulse.metadata dictionaries
- Exported top-level result.metadata
- Exported raw_pulses[*].metadata and emitted_pulses[*].metadata
- Exported v04_result.input_pulses[*].metadata

Add the protocol's nested `after_return` value and retain changed external bytes. Do not
mutate a dictionary used only to construct a pulse: SignalPulse copies that outer dictionary.
Do not reach into source-private fields to manufacture the control. Require the detached
output's mutable identities to be disjoint from the committed graph, then require exact
unchanged committed graph bytes and exact unchanged old-root bytes after all mutations.
Source: [contracts.py](../../src/sparkbrain/v04/contracts.py), lines 73–80, and
[v05/contracts.py](../../src/sparkbrain/v05/contracts.py), lines 114–129.

## Budget, failure and preservation

On full completion: **1 fresh root, 4 whole-brain copy attempts, 7 process attempts,
14 submitted raw pulses, 6 process returns, 1 expected processing exception, 2 aborted
transactions and 1 owner commit**. These are ceilings on early stop, not instructions to
finish after failure. There are no native loads, outcome calls or M1 calls.

CPU 60 s, wall 120 s with external hard timeout, address space 512 MiB and output 32 MiB.
Finalization reserves stay inside these limits. Record the actual network-enforcement layer;
Python socket/process audit is not OS isolation. Hard termination can prevent finalization.

Stop without retry on absent required coverage, unsupported state/copy behavior, graph or
alias/isolation mismatch, unexpected error, a missing genuine fault witness, output/state
mismatch, mutation leakage or a resource cap. Preserve raw return/error, all available
partial typed graph inventories, source/config/clock/count records and external-control
bytes before summaries. No source repair-and-rerun, extra episode, seed search or claim upgrade
is authorized by this protocol.

Before execution, the dedicated implementation, graph-audit logic and exact command need a
separate source freeze and independent pre-execution review. This source-only protocol is
not execution-readiness evidence. A positive result would be restricted acquired-assembly
ownership under these faults, not native checkpoint completeness, full crash recovery,
predictor/action ownership, M1 joint transactions or learned task benefit.

## Source review and coordination

The independent source review supported the four-copy design with the corrections now
explicit above: full graph oracle; dormant predictor/action scope; mutation beyond the
fault config; explicit v0.4-result aliases; outward metadata paths; post-return controls;
and a separately required mature suffix. No model was imported or run for that review.

Main and AGENTS were checked at `9549a2bf6bc76cb7b5714742f3ed54decd618263`; the active
Human Directive index remained at ref `ops/human-directives`, head
`8ce979b9ec0bc7eede5225c0403698f8886d3e8d`. This dedicated cloud-only prototype does not
modify shared scheduler state, scientific acceptance, PR173 causal triage or canonical M1.
