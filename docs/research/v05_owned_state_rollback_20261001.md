# v0.5 producer-owned transaction: source map and minimal proposal

2026-10-01 UTC. **SOURCE AUDIT / DESIGN / NONCANONICAL / NON_EVIDENTIARY**.
Scientific credit: **0**. No real brain, clone, checkpoint, fixture or dynamics was executed.
Source pin: `00ef5bac171b3ec05f581a157cccd9528bb71e8f` (merged PR #175).
AGENTS SHA-256: `ceb4a6b2f14b0efa25148cf0f652f75133e00d11360a020ef6aa6adcdb34a002`.
Fresh directive head: `8ce979b9ec0bc7eede5225c0403698f8886d3e8d`.

## Decision

**Native checkpoint as complete transaction snapshot: no. Whole-graph in-memory
copy-on-write: a source-feasible candidate, not yet verified.** This is the next concrete
prerequisite for the [real producer inlet](assembly_m1_interface_design_20261001.md).
The [fake sentinel](assembly_m1_contract_sentinel_20261001.md) does not certify real v0.5
state ownership. A successful bounded clone test would establish a producer-local
transaction boundary only, not learned predictive value, M1 integration or an accepted build.

Use one `copy.deepcopy` call on the complete owned brain object, process inputs on that
candidate only, build and validate detached output, and publish its private owner pointer
as the final commit step. No fallible export/validation step may follow publication.
On failure discard the candidate. Do not restore selected fields into a partially mutated
live brain or independently copy components: shared references must survive within the clone.
No M1 run, production runtime change, checkpoint-format repair, PR #164 work, PR #172 M1
loader work, weight/delay experiment, shared ledger or scientific identity is part of this scope.

## Exact state gaps and references

All links are source facts at the pin, not measured property-test results.

| Owned state | Native v0.5 persistence | Why a complete transaction needs more |
|---|---|---|
| `base.cascade_tracker._pending` | Omitted although the tracker has its own `state_dict` | Unfinished cascade influences later recurrence/assembly processing |
| `base.burst_detector._window`, `_emitted_keys` | Omitted | Recent spikes and duplicate-emission guards influence later bursts |
| Field `last_run_arrivals`, `last_run_spikes`, `last_input_routes` | Omitted | Observable counters/input routing are reset or lost despite matching persisted state |
| Field `outgoing` / `incoming` lists and their live order | Reconstructed | Outgoing lists are sorted by current delay on load, while delay updates do not re-sort live lists; future scheduling tie counters can differ |
| `brain.results`, `base.results` | Not restored; base result payload is explicitly cleared by v0.5 | Complete retained result/inspection state and cross-result references are lost |
| Base detector/gate configs; base plasticity, expectations and transducers | Not serialized by the nested base payload | Constructor defaults return; these are dormant/default on the restricted v0.5 pulse path but still owned fields |
| `base.config`, `base._topology` | Base config is written as `brain_config` but ignored by v0.5 load; initial topology is reconstructed | Standard-constructor values initially agree; this is a reconstruction/dormant-state gap, not an observed divergence |
| Receptor channels, assembly candidates/suppression, top-level plasticity/homeostasis, predictor/action, pending activation/action, trace/index | Explicitly persisted | Must remain in the copy inventory too; “persisted” does not establish all alias/order invariants |
| Field units/connections, event queue/counter/clock and total arrivals/spikes | Explicitly persisted | Queue is serialized sorted and rebuilt as a heap; raw container layout/alias identity is not a complete graph snapshot |
| `UnitState.source_pulse_ids` tuple type | JSON writes arrays; loader passes them directly into `UnitState` | Restored fields hold lists until touched by a later update; equal JSON hashes can hide this in-memory type change |

Source: [v0.5 checkpoint/write/load](https://github.com/salmonmikan/sparkbrain_research/blob/00ef5bac171b3ec05f581a157cccd9528bb71e8f/src/sparkbrain/v05/brain.py#L270-L361),
[base checkpoint](https://github.com/salmonmikan/sparkbrain_research/blob/00ef5bac171b3ec05f581a157cccd9528bb71e8f/src/sparkbrain/v04/brain.py#L258-L316),
[detector/tracker](https://github.com/salmonmikan/sparkbrain_research/blob/00ef5bac171b3ec05f581a157cccd9528bb71e8f/src/sparkbrain/v04/dynamics.py#L39-L214),
[field construction](https://github.com/salmonmikan/sparkbrain_research/blob/00ef5bac171b3ec05f581a157cccd9528bb71e8f/src/sparkbrain/v04/field.py#L77-L107)
and [field persistence](https://github.com/salmonmikan/sparkbrain_research/blob/00ef5bac171b3ec05f581a157cccd9528bb71e8f/src/sparkbrain/v04/field.py#L300-L356).

The constructor establishes these essential aliases:
- Each `field.connections[(source,target)]` object is the identical object in the matching
  outgoing and incoming lists; copies must preserve that relationship internally while
  sharing no mutable edge with the original
- `base.cascade_tracker.memory is base.assembly_memory`
- A returned v0.5 result retains the same v0.4 result object appended to `base.results`;
  pending activation/action also reference objects represented in retained results
- Emitted pulse elements are shared with the base result's `input_pulses`; spike elements
  can be shared between retained results and detector/tracker buffers
- A newly acquired assembly candidate's `prototype` is the same `ActivityPattern` object
  held in the corresponding result's `patterns` tuple

The initial `_topology` is separate from mutable field units/connections. Do not falsely
bind it to live objects while reconstructing a snapshot. Whole-graph cloning should preserve
both the actual aliases and actual separations.

## Copy feasibility and ownership restrictions

Inspected constructors and dataclass fields contain ordinary objects, numbers, strings,
lists, tuples, dicts, sets and a deque. There is no stored lock, socket, file handle,
generator, worker thread, or custom copying hook in this restricted graph. Topology RNGs
are local to construction; no live generator is stored. This is source inspection under
the stated constructors/entrypoints, not a guarantee about arbitrary monkey-patched objects.
The [machine source map](../../artifacts/research/v05_owned_state_20261001/source_map.json)
records source hashes and initialized field names, including all configuration and result/
event contract dataclasses, without importing a runtime. It is a proposed exact-type/field
allowlist; whether the actual live graph is closed over it must be checked before cloning.

Python's [official copy documentation](https://docs.python.org/3/library/copy.html)
explains recursive copying and the memo used to track already-copied objects, while warning
that some external-resource types are not copied and custom classes can override behavior.
Inference: one whole-object `deepcopy` is a sensible candidate here; it is not an existing
supported SparkBrain checkpoint/rollback API. Never use shallow copy or a fresh memo per
component. No pickle/unpickle of external content is needed.

For the proposed test only:
1. The isolated owner constructs its own brain. Do not accept an externally held live brain
   or expose brain/component handles. There is no concurrent stepping
2. Accept only exact known types with finite primitive fields, exact list/tuple pulse
   containers, and exact empty dictionaries for both pulse metadata and the separate
   `process_episode` metadata argument. Reject additional fields, nonempty metadata,
   unsupported types, iterators/generators and custom container subclasses before cloning
3. Copy or freshly construct the validated pulses before calling `process_episode`.
   That API retains caller `SignalPulse` objects in `raw_pulses`; frozen dataclasses can
   still contain mutable metadata dictionaries. State cloning alone does not isolate inputs
4. Return detached primitive output, not the live result object. Receptor-emitted metadata
   generated internally is included in the graph inventory
5. “In flight” means queued arrivals or pending detector state at a synchronous public-call
   boundary. It never means copying a running Python frame or another thread
6. Disable v0.5 prediction/action/reward modulation. Base action-association diagnostics still
   run during ingestion and must be copied. No scalar outcome or reward is supplied

## Minimal proposed property matrix

The [machine proposal](../../artifacts/research/v05_owned_state_20261001/property_proposal.json)
fixes the six cases, config, inputs, mutations and exact call budgets. It is **not execution
authorization**. Freeze implementation,
exact input/config bytes and inventory checks after peer review before running it.
Use one fresh topology seed `920041`, CPU only, no historical runner/checkpoint/suffix.
One standard v0.5 constructor is used with prediction/action/reward modulation disabled;
other defaults are preserved unless a case explicitly names a prospective mutation.

Before execution, source review and the task owner expanded the prefix to the minimum
three distinct episodes needed for possible default maturity. The fixed prefix is Q at
8, 208 and 408 ms, one pulse per `process_episode` call, with distinct opaque episode IDs
`owned-0001`, `owned-0002`, `owned-0003`. Each pulse has magnitude 1.2, positive polarity,
constant source `owned-state-probe`, zero external novelty/prediction-error and empty
metadata. The fixed suffix is R at 600 ms with the same scalar fields and ID `owned-0004`.
`settle_ms=32`. Three episodes are necessary, not sufficient: require actual mature-candidate
counts and a mature non-null pending activation, never assume them from the call count.
No pulse, seed, threshold or extra episode may be added after seeing a coverage failure.

| Case | Fixed boundary and intervention | Required observation |
|---|---|---|
| P1 Graph copy/isolation | Fresh brain; whole deepcopy; mutate one cloned unit and edge only | Equal pre-mutation full inventory; both essential aliases preserved; no cross-copy mutable sharing; original inventory unchanged after clone mutation |
| P2 Acquired prefix / end-episode vs quiet | Inspect after the first episode as an immature negative control; finish the two remaining fixed episodes, then compare original/direct, whole-copy and native-save/load before the fixed suffix | First-episode maturity is absent; actual three-episode mature candidate and non-null pending activation are required before readiness; whole-copy inventory/continuation equals direct; quiet eligibility and native losses are reported separately |
| P3 Pending transients | Advance the fresh empty field publicly to 3 ms; create four valid spike records at times 0,1,2,3 across three valid units; feed detector/tracker via their update APIs with flush cutoff 3; schedule one future arrival at 4 | Nonempty burst window/emitted keys, tracker pending and queue asserted before copy; whole-copy inventory/continuation match; native omitted caches are reported, never repaired |
| P4 Live edge order | At clock 0, choose the lowest source with two outgoing edges, set the first delay to second delay + 0.25 (without re-sorting), then copy/save/load | Whole-copy preserves edge objects/list order; native reconstruction reorders; report full-state/continuation projections separately, without assuming native prediction failure |
| P5 Abort acquired-state ownership | Two independently constructed fixed three-episode owner prefixes: throw during detached-output validation after a candidate suffix, before publication; separately replace field event cap with 1 after the prefix to force a real partial-update suffix exception | Original whole-graph inventory unchanged in both cases; candidate mutation/exception recorded, no native restore used |
| P6 Acquired-state commit/output ownership | Two independent fixed three-episode prefixes, one owner and one direct reference; process the suffix on the owner clone/reference, validate detached output, then publish the pointer once | Live pointer advances once; direct result/owned state agree; mutating the originally empty caller pulse metadata and nested exported raw/emitted metadata cannot change committed state |

For P3, use public detector/tracker calls on hand-built valid `SpikeEvent` values; this is a
time-consistent adversarial component-state fixture, not evidence those spikes were
acquired through the field or reached by the complete producer entrypoint. The
queue arrival targets the lowest valid receptor, has current 0.25, no source unit and fixed
opaque pulse ID. Continue the field through the existing pulse-processing entrypoint;
compare whole-copy/direct outputs. No required native output divergence is invented from
a mere structural mismatch. P4 likewise engineers a valid ordering boundary rather than
claiming delay learning benefits. P5's event cap is replaced prospectively with a valid
positive value before cloning; capture its abort baseline after that replacement.
Receptor fanout 2 ensures the cap can be reached. Materialize P3 source-pulse IDs as an
exact tuple; a dataclass annotation alone does not convert the JSON array into one.

### Comparisons, limits and stop criteria

- Compare a complete, allowlisted field inventory (including ordered queues/adjacency,
  counters, caches, configs, transducers, results and traces), including dict insertion
  order and tuple/list type tags rather than JSON/asdict value equality alone; record
  repeated-object reference relationships, not only separately flattened field values
- P2 must record emitted pulses, spikes, patterns and acquired candidate/prototype references
  to exercise those alias types. Preserve the one-episode immature control. After exactly
  three episodes, require a non-null mature pending activation bound to a candidate with
  at least three distinct prefix episode IDs and its retained prototype. If any required
  target is absent, record a coverage block and skip dependent P5/P6; do not search for a
  better pulse, seed or longer prefix. Repeat these checks on every independently
  constructed P5/P6 prefix too. Maturity is not learned predictive usefulness
- Keep whole-inventory equality, native `state_dict` equality and future output equality
  separate. A matching persisted hash is not completeness evidence
- For P2, quiet eligibility requires empty field queue/tracker pending, expired burst window
  relative to the fixed suffix, old emitted keys and canonical outgoing order. If ineligible,
  report it as an end-episode case; do not clear caches or delay/retime the suffix to rescue it
- Maximum six cases, 11 fresh constructors/native loads total (including three native
  loads), seven whole-brain copies, 28 pulse-processing calls/attempts total, one input pulse
  per call, and four hand-built P3 spike records. P2 uses six calls, P3/P4 three each,
  P5 four per fault branch, and P6 eight across owner/reference. No hidden prefix rebuilds
  or retests after a failed gate. Limits: 60 CPU / 120 wall seconds,
  512 MiB process address space and 32 MiB saved artifacts. Stop on cap or unsupported graph
- Preserve full raw comparisons before the summary. No threshold, pulse, topology or
  inventory relaxation after results. An unexpected direct-versus-whole-copy mismatch or
  owner-invariant failure blocks the transaction proposal pending diagnosis; the native
  negative control is not required to pass full-inventory equality
- The native expected-loss set is the source-mapped omitted/reconstructed fields above:
  result lists, detector caches, field diagnostic counters/routes, tuple/list type, and
  adjacency order when noncanonical. Dormant/default config/topology fields may still agree.
  Record any additional native difference separately; never classify an expected loss as
  a whole-copy failure or silently ignore an unexpected one

A pass would establish the bounded in-process transaction prerequisite on the actually
exercised acquired producer state under this restricted contract. It would permit
considering a later representation inlet, but would not establish that inlet or support
native cold checkpoint completeness, M1 composition, online schema migration, learned assembly benefit, global identity neutrality,
biological claims, or a scientific promotion. A fail would identify the exact owned field,
alias, ordering or continuation boundary needing a separately scoped change.


## Source review checkpoint

Independent source review cleared the revised six-case proposal for implementation freeze.
All 16 source hashes, 50 class field inventories and the 11/7/28 resource counts were
rechecked without importing SparkBrain or running any fixture. The state inventory, P3
clock, nested metadata isolation, output-before-commit ordering and native negative-control
interpretation incorporate that review. Actual implementation hashes and eligibility
checks must still be frozen before any model execution.
