# Three-observation M1 eligibility: separate prospective proposal

2026-10-02 UTC. **SOURCE-ONLY / UNAPPROVED / UNEXECUTED / NON_EVIDENTIARY**.
Scientific credit **0**. This is a review proposal, not an execution freeze, runnable
probe, approval, successful eligibility record, or amendment of the 68-call pilot.
Parent review and independent review must precede any final binding. No execution
authorization, approved digest, resource limits, STARTED marker or permit is supplied.

## 1. Purpose, source and precise coverage

Propose the smallest literal-preserving transactional path that reaches one actual
three-observation, two-receipt, pending-third-observation owner for each S/R arm,
and explicitly tests an alias-preserving joint clone and native predictive checkpoint
roundtrip of each of those owners. The extra two verification clones are deliberate:
merely snapshotting the third aftergraph would not exercise its joint cloneability.

Source derivation used PR191 preparation `e43f95326610d09c04e99be30d6e98be0935795a`
with repaired runtime source `46bbd9b8b28c2404c73f028f8736ed83c3b5c3fe`. All line
references below refer to that inspected source unless a later independently reviewed
instrumentation change is explicitly identified. Sources were read/AST-parsed only.
No SparkBrain model import, construction, native enum import, checkpoint operation,
producer call, M1 transition or research run was used to derive this proposal.

This probe covers **the fixed third-A endpoint only**. It does not establish observed
eligibility of third-B, A/B, B/A or A/A-sham endpoint graphs, nor all failure restores.
Exact source support, prospective bounds and before-operation fullgraph checks remain
necessary for those pilot paths. If admission requires observed coverage of each,
that requirement remains unmet; it cannot be silently waived by this smaller probe.

Three observations do not imply nonempty concepts. The proposed mandatory condition
is preservation and exact-type support for the **actual** concept subtree reached,
including an honestly recorded empty subtree. A claim of observed nonempty
`_MutableConcept` support needs a real nonempty witness; none is promised here.
A controlled codec software fixture may test the repaired type contract separately,
but cannot substitute for empirical integrated-path coverage or authorize a pilot.

## 2. Fixed exposure, with independent authority

Proposed one-shot identity: `assembly-m1-three-observation-eligibility-v1-20261002`.
Proposed evidence destination: `artifacts/research/assembly_m1_three_observation_eligibility_v1_20261002/`.
These are prospective names only; no directory is created or reserved, and no approval
is implied. Bind and approve this **probe** identity separately from G0 and the pilot.
Retain the existing exposed observation/receipt literals unchanged: run identity and
output namespace are separate from observation IDs visible to M1. Changing those
visible IDs would change trace and receipt-binding values and would require another
review; do not call the resulting graph identical.

Inputs are rows 0 through 66, inclusive (the first 67 rows), from the reviewed
`artifacts/research/assembly_m1_path_v1_20261002/inputs.jsonl`, bound by file hash
and exact selected-row hashes in a future freeze. Preserve all four existing teaching
receipts: A is +0.8 and B is -0.8; event IDs, arm-specific receipt IDs and delivery
at start +100 ms remain unchanged. Decision time remains (start +72 ms)/1000.
The unused row 67 (third B alternative) is not executed. No export search, donor
selection, checkpoint import, alternate seed, added stimulus, padding of observations,
receipt replay, query outcome or inlet control is included.

The exposed 64-window prefix must be reacquired once from one fresh V05 producer.
A preexisting producer donor would introduce an independently unsupported native
load/clone and source-equivalence assumption; it is not this proposal. R retains a
separately detached copy of the same 64 literal raw-history records, with no producer.
Do not copy the acquired producer during arm initialization.

The configured producer remains the existing first PR182 recipe; M1 remains the
identical default I1/E0 configuration and the existing eight-scalar channel contract.
NativeBackend source at `scripts/m1_path_native.py:88-116,203-248,256-281` establishes
these definitions but does not authorize this probe. The current backend and schedule
require the disabled pilot permit; they are **not** a probe launcher or a way to
bootstrap the missing eligibility gate (`m1_path_native.py:160-168`;
`m1_path_pilot.py:106-111,123-141`). A separate reviewed admission/launcher is required.

## 3. Candidate and endpoint schedule

First acquire 64 native windows with learning, preserve the complete acquired graph,
then freeze the native dictionary. Construct the two fresh independent M1 owners.
S owns the acquired producer; R owns raw history and has producer/dictionary null.
For each arm, in fixed S-then-R order, use six joint candidates:

| Candidate | Clone source | Sole transition | Result |
|---|---|---|---|
| C1 | Initial arm owner | Features for row 64; M1 observe A | Pending A |
| C2 | C1 | Deliver A receipt | First committed receipt |
| C3 | C2 | Features for row 65; M1 observe B | Pending B |
| C4 | C3 | Deliver B receipt | Two-receipt trained owner |
| C5 | C4 | Features for row 66; M1 observe A | Pending third A |
| C6 | C5 | None | Unadvanced fullgraph verification clone |

Publish C1-C4 according to the existing candidate-before-publication discipline.
C5 is an unpublished endpoint branch, not a teaching continuation. C6 is never
published and never advanced. S calls the producer for rows 64,65,66 exactly once,
with field/assembly learning false; R encodes those same rows once each. The native
producer's outcome API is never called. Every observation receives its own arm's
seven features in both inlets; the original signal and route coordinate remain zero.
Source analogues: `m1_path_pilot.py:221-265,287-320,343-379` and
`m1_path_inputs.py:201-218`.

At C5, preserve the full joint graph, then make C6 and verify exact source/candidate
value, type, insertion-order and alias topology equality with mutable disjointness.
Preserve every other live root's identities, values and resource bindings across this
operation. Explicitly save C5's predictive package once, load it once, compare it,
and dispose the readback before any further operation. No extra save-back, replay,
observation, receipt or predictive/scope query is allowed for comparison.

### Required endpoint witnesses, per arm

A global call total is insufficient. Evidence must bind each arm's exact predecessor
DAG, literal row, wire payload, event/receipt IDs and transition ordering. Require:

- Exactly three original event bindings, two committed receipt bindings, coordinator
  sequence 2, a pending third observation and matching pending action
- Predictive revision step 2, its pending third context/sample, and the raw reference
  brain's three-step history/results, all with exact field/type and alias census
- The complete scope state and receipt evidence, plus the actual router components
  and their bindings. For the proposed two-route eligibility claim, require two
  distinct route tokens committed by the A and B receipts; if not observed, fail
  that eligibility requirement rather than forcing a second route
- Presence/preservation of two route objects is not a claim that both were selected
  by M1's pre-feedback query. First A is queried before any scope exists; B is
  queried before its new scope is created. The third-A query adds only one actual
  query observation. Log actual query and receipt-routing choices separately
- Complete producer state, dictionary, raw history, coordinator, pending bindings,
  receipt ledger and resource mappings in C5/C6, not just predictive hashes
- The actual concept map and its exact typed values, explicitly reporting whether
  `_MutableConcept` is absent or present. Never replace an absent witness with a
  source registry entry or an injected object

Sources: `integrated_m1.py:267-274,391-450,452-526`; scope router birth/query distinction
in `causal_scope_revision.py:237-246,284-315`; pending predictive state in
`predictive_revision.py:250-260,413-416`.

## 4. Exact proposed successful call contract

Counts below are **probe counts**, never the full pilot's 68/14/4/18/28/10/58 counts.
For positive eligibility, require exact equality of raw call attempts and normal
returns to this vector, plus zero exceptions/pending records and a closed successful
session. A cap-only upper bound cannot establish positive coverage. A required
`call_targets` map must equal the reviewed map in both keys and exact routes; empty,
partial, substituted and type-only maps are invalid. Freeze emergency ceilings
separately from this exact successful vector.

Paths in this table are repository-relative exact profiler routes; the parenthetical
line is a source citation, not part of the route. Constructors generated by dataclasses
belong to the separate complete type census rather than guessed AST call targets.

| Counter key | Exact path | Exact qualname | Successful calls |
|---|---|---|---:|
| producer_init | src/sparkbrain/v05/brain.py | IntegratedV05Brain.__init__ | 1 |
| producer_process | src/sparkbrain/v05/brain.py | IntegratedV05Brain.process_episode | 67 |
| producer_learn_outcome | src/sparkbrain/v05/brain.py | IntegratedV05Brain.learn_outcome | 0 |
| v04_init | src/sparkbrain/v04/brain.py | IntegratedV04Brain.__init__ | 1 |
| v04_ingest | src/sparkbrain/v04/brain.py | IntegratedV04Brain.ingest_pulses | 67 |
| field_init | src/sparkbrain/v04/field.py | TemporalExcitableField.__init__ | 1 |
| field_run | src/sparkbrain/v04/field.py | TemporalExcitableField.run_until | 67 |
| m1_init | src/sparkbrain/system_build/integrated_m1.py | IntegratedM1Pilot.__init__ | 2 |
| m1_observe | src/sparkbrain/system_build/integrated_m1.py | IntegratedM1Pilot.observe | 6 |
| m1_outcome | src/sparkbrain/system_build/integrated_m1.py | IntegratedM1Pilot.apply_outcome | 4 |
| m1_restore | src/sparkbrain/system_build/integrated_m1.py | IntegratedM1Pilot._restore_components | 0 |
| predictive_init | src/sparkbrain/system_build/predictive_revision.py | PredictiveRevisionPilot.__init__ | 4 |
| predictive_observe | src/sparkbrain/system_build/predictive_revision.py | PredictiveRevisionPilot.observe | 6 |
| predictive_feedback | src/sparkbrain/system_build/predictive_revision.py | PredictiveRevisionPilot.feedback | 4 |
| predictive_from_payload | src/sparkbrain/system_build/predictive_revision.py | PredictiveRevisionPilot._from_checkpoint_payload | 2 |
| scope_init | src/sparkbrain/system_build/causal_scope_revision.py | CausalScopeRevisionPilot.__init__ | 2 |
| scope_query | src/sparkbrain/system_build/causal_scope_revision.py | CausalScopeRevisionPilot.query | 6 |
| scope_step | src/sparkbrain/system_build/causal_scope_revision.py | CausalScopeRevisionPilot.step | 4 |
| scope_restore | src/sparkbrain/system_build/causal_scope_revision.py | CausalScopeRevisionPilot._restore_payload | 0 |
| scope_from_payload | src/sparkbrain/system_build/causal_scope_revision.py | CausalScopeRevisionPilot._from_checkpoint_payload | 0 |
| router_init | src/sparkbrain/system_build/causal_scope_revision.py | CausalScopeRouter.__init__ | 2 |
| router_route | src/sparkbrain/system_build/causal_scope_revision.py | CausalScopeRouter.route | 6 |
| router_observe | src/sparkbrain/system_build/causal_scope_revision.py | CausalScopeRouter.observe | 4 |
| router_from_state | src/sparkbrain/system_build/causal_scope_revision.py | CausalScopeRouter.from_state_dict | 0 |
| raw_init | src/sparkbrain/v03/runtime.py | IntegratedV03Brain.__init__ | 2 |
| raw_step | src/sparkbrain/v03/runtime.py | IntegratedV03Brain.step | 6 |
| facade_init | src/sparkbrain/v032/runtime.py | IntegratedV032Brain.__init__ | 28 |
| facade_step | src/sparkbrain/v032/runtime.py | IntegratedV032Brain.step | 6 |
| joint_clone | scripts/g0_joint_ownership.py | clone_joint | 12 |
| joint_construct | scripts/g0_joint_ownership.py | _construct | 12 |
| pilot_save | src/sparkbrain/system_build/predictive_revision.py | PilotCheckpointManager.save | 12 |
| direct_save | src/sparkbrain/v032/checkpoint.py | DirectCheckpointManager.save | 12 |
| pilot_load | src/sparkbrain/system_build/predictive_revision.py | PilotCheckpointManager.load | 2 |
| direct_load | src/sparkbrain/v032/checkpoint.py | DirectCheckpointManager.load | 2 |
| direct_load_bytes | src/sparkbrain/v032/checkpoint.py | DirectCheckpointManager._load_bytes | 14 |

Source call sites: producer nesting `v05/brain.py:63-112,132-169`;
`v04/brain.py:72-109,125-151`; M1 nesting `integrated_m1.py:261-268,401-408,469-487`;
checkpoint nesting `predictive_revision.py:600-634`; raw reconstruction
`v032/checkpoint.py:343-415`; clone reconstruction `g0_joint_ownership.py:557-629`.

The four special resource counters are **not ordinary call_targets** in the current
profiler; require them as exact additional call-cap/coverage keys with these routes:

| Resource key | Allowed exact parent routes | Successful calls |
|---|---|---:|
| model_rng | v03/runtime.py:IntegratedV03Brain._initialize_runtime; v032/checkpoint.py:_decode; scripts/g0_joint_ownership.py:_construct | 28 |
| topology_rng | v05/topology.py:layered_reservoir_topology | 1 |
| model_lock | v032/runtime.py:_shared_step_lock | 28 |
| registry_guard | v032/runtime.py:<module> | 1 |

For the resource table, runtime paths have the `src/sparkbrain/` prefix. Model RNG
subcounts are 2 fresh +12 joint-copy +14 decoder; topology RNG is not retained in the
native producer graph. The same clean import also constructs **one
`weakref.WeakKeyDictionary` registry** at `v032/runtime.py:17-18`. This is an actual
bootstrap allocation in addition to the guard; the future launcher must bind and
record its exact stdlib constructor/source parent. The current SparkBrain/resource
per-type census does not, merely by listing the guard, establish coverage of this
stdlib registry object. Exact resource route definitions already appear in
`m1_path_census.py:60-74,223-277` and `m1_path_census_evidence.py:24-38`.

The separately admitted launcher must also bind its adapter operation journal:
producer construction 1; M1 construction 2; process 67; observe 6; outcome 4;
explicit predictive save 2; load 2; compare 2; readback disposal 2; raw encoding 3;
accepted native export 3. If it reuses the current adapter without changing its
method bodies, require the matching exact NativeBackend method routes at
`m1_path_native.py:221,232,256,292,323,335,350,369,379,424` in the expanded launcher
map. The construction/permit boundary itself must be reviewed separately. No wrapper
journal can replace the required nested native profiler map above.

## 5. Constructor and reconstruction derivation

There are ten state transitions that save predictive beforestate: 6 observes +4
receipts. Add two explicit third-endpoint saves: **12 saves/validation reconstructions**.
Two explicit loads add two further `_load_bytes` calls, for **14 native decodes**.
Each decode creates one raw shell, facade, RNG and lock. Each joint clone creates one
raw shell, facade, RNG and lock. Only S's six clones contain the native producer.

| Exact core type | Fresh/normal init | Joint shells | Codec shells | Total births |
|---|---:|---:|---:|---:|
| IntegratedM1Pilot | 2 | 12 | 0 | 14 |
| PredictiveRevisionPilot | 4 (2 roots +2 readbacks) | 12 | 0 | 16 |
| CausalScopeRevisionPilot | 2 | 12 | 0 | 14 |
| CausalScopeRouter | 2 | 12 | 0 | 14 |
| IntegratedV032Brain | 28 | 0 | 0 | 28 |
| IntegratedV03Brain | 2 | 12 | 14 | 28 |
| IntegratedV05Brain | 1 | 6 | 0 | 7 |
| random.Random, model-owned | 28 | 0 | 0 | 28 |
| random.Random, topology-local | 1 | 0 | 0 | 1 |
| _thread.RLock, model-owned | 28 | 0 | 0 | 28 |
| _thread.lock, registry guard | 0 | 0 | 1 module shell | 1 |

The facade always uses its real constructor; ordinary joint objects use exact-class
shells. A checkpoint does not construct a full M1 or scope pilot. Pilot readback does
construct a predictive pilot using the already-restored facade, hence four predictive
constructors rather than two (`predictive_revision.py:499-523,618-634`).

Every one-per-producer nested owner also has one fresh birth +6 joint shells:
V04 brain, field, topology, V04 assembly memory/burst detector/cascade tracker/ignition
and plasticity/action/expectation/transducer objects, and V05 receptor/assembly/
plasticity/homeostasis/predictor/action objects. Shared aliases, such as
`base.assembly_memory is base.cascade_tracker.memory`, must remain one object per
producer graph (`v04/brain.py:91-106`). Original topology units/connections and mutable
field copies are distinct. With unchanged 64-unit topology, 128 initial UnitState
objects plus 6x128 joint shells gives 896 unit allocations; connection counts and
duplicate temporary allocations need their own source-bound census.

The six prepared producer configuration objects are constructed once during adapter
preparation and once again via `dataclasses.replace` for the producer, not hidden
copyreg copies (`m1_path_native.py:203-209,224-227`). Other config constructors,
transient outputs and retained graph-node types remain in the full type census.
Required clean imports include 7 SparkKind,5 EventKind,4 TransitionKind initializations;
these are import-phase allocations, not arm observations or scientific exposure.

### Exact feature-state allocation obligation and current blocker

For the fixed eight-channel, no-world-feedback observations:

- `_FeatureState.__init__`: **48**. The default object in `setdefault` is eagerly
  constructed on every channel at every observe, including existing keys
- Internal default-deepcopy `_FeatureState` shells: **32**. First observe copies an
  empty state map; each later observe copies eight states, twice per arm
- Joint-clone `_FeatureState` shells: **80** = 2x(0+8+8+8+8+8)
- Codec `_FeatureState` shells: **96** = 2x(0+8+8+8+8+8+8), for five internal
  saves, one explicit save and one readback per arm
- Therefore total `_FeatureState` shells: **208**, across three distinct routes

Sources: `sensory_field.py:261,265-276,449-451`; no feedback reentry because
`predictive_revision.py:256` supplies no world feedback and
`v03/runtime.py:970-978` returns before a second sensory observation.

**Inspected census implementation blocks this path before the second observation:**
`m1_path_census.py:199-204` rejects every SparkBrain `copyreg.__newobj__` allocation,
while `sensory_field.py:261` necessarily uses default deepcopy of slot dataclasses.
No source-only count or mock success resolves that blocker.

Before admission, independently review a narrow instrumentation change for exact
`sparkbrain.v03_seed.sensory_field:_FeatureState` shell allocation at
`["stdlib/copyreg.py","__newobj__"]`, linked to the exact `copy._reconstruct` path,
source-bound `AdaptiveSensoryField.observe_with_trace` deepcopy site, dedicated owner
and memo membership. Count its attempt before the allocator body and birth only on
successful return. Bind the stdlib bytes and extend raw-evidence validation accordingly.
Unknown class/callsite/stack paths, direct calls, `__newobj_ex__` and other native
copyreg uses remain rejected. This document does not implement or approve that repair.

### Counts that remain unresolved prospectively

Pulse emission, queue/arrival/spike/burst/cascade/pattern/assembly/receptor-state
allocations, evidence and trace rows, concept instances and codec tree multiplicity
must have reviewed finite per-type init/shell caps before the probe. There is no
blanket wildcard or online allowlist extension. Value-tree decodes may duplicate
aliases; their counts cannot be replaced by the number of distinct source nodes.
The fixed exposure vector above is not a guessed bound for these allocations.
No model construction may be hidden in source validation or cap derivation.

## 6. Fullgraph and checkpoint boundaries

The C5-to-C6 oracle must preserve complete joint graph semantics, alias topology,
insertion order and original-owner noninterference; it also proves independent raw
brain/lock/weak-registry bindings. The producer and raw-history state do not advance
in C6. Keep every predecessor explicitly live until reverse-order disposal.

Predictive checkpoint compatibility is narrower: preserve both original native files
as bytes, preserve all 14 direct decoder inputs before decoding and both pilot decoder
inputs before load, compare the complete predictive payload and complete raw-brain
codec tree, and verify exact types plus cross-owner mutable isolation. Tree comparison
relaxes alias topology/map order only for the native codec; it is not a joint cold
restart and cannot cover coordinator, scope, producer or receipt state by itself.
Source comparator: `m1_path_native.py:335-429`; cloner: `g0_joint_ownership.py:672-735`.

For positive eligibility require nonvacuous arm-bound graph evidence and call evidence
together. Hash-bound arbitrary files plus two booleans are not a graph proof, and
an internally consistent type-only event trace is not a three-observation proof.
The inspected validator only verifies supplied call routes and cap upper bounds
(`m1_path_census_evidence.py:280-310,483-488,523-540`); it does not yet require this
exact call map/vector or derive the arm transition graph. Those repairs remain
mandatory before a real positive eligibility record could be admitted.

## 7. Nonempty concepts, scope interpretation and admissible conclusions

For R's exact A,B,A one-hot sequence, source arithmetic predicts **no nonempty
concept at the third endpoint**. First observation admits all eight channels by onset.
The second observation flips the two one-hot channels. At third A, temporal_000's
salience is 0.175 and temporal_001's is approximately 1.276596, both below their 1.3
threshold; constant zero channels are also suppressed. No pair attains the default
minimum three occurrences. This is a source-derived consequence, not observed data
(`sensory_field.py:281-324,366-401`; `concepts.py:13,70-102`).

Therefore requiring a nonempty `_MutableConcept` in **both** arms would make this
literal-preserving probe incapable of positive eligibility. Do not modify stimuli,
thresholds, selected endpoint or concepts to obtain that witness. Report R's actual
empty map and S's actual result. If pilot safety requires a nonempty class-bearing
path that this endpoint never reaches, source-reviewed codec support may be one
prerequisite but observed integrated support remains unestablished. A source-only
fixture cannot retrospectively certify that unexecuted path.

Similarly, two committed receipt routes, two stored components, two successful
pre-feedback query selections and both signs producing valid actions are different
properties. Only the explicitly required graph/type/ownership/checkpoint conditions
are eligibility criteria; correct action or native superiority is not required.
If two distinct receipt routes are mandatory and S does not form them, record
ineligibility. Do not count a single-route graph as observed two-route coverage.

## 8. First-failure, rollback and cleanup contract

Stop the **whole probe** on its first terminal or arm-ineligibility failure. A positive
result requires both arms, so there is no useful independently continuing arm in this
eligibility attempt. No retry, replacement root, additional clone, replay or new
receipt ID is permitted. Preserve failed attempts and partial evidence as failure;
they cannot establish positive eligibility. Successful call counts need not be filled.

No fault injection or deliberate rollback is in the successful schedule. Reserve,
without claiming it was exercised, at most **one** terminal M1 rollback chain:

- +1 PilotCheckpointManager.load, DirectCheckpointManager.load and `_load_bytes`
- +1 predictive constructor/from-payload, facade/raw-shell/model-RNG/model-lock birth
- +1 outer scope restore; if an internal scope restore precedes it, at most two scope
  restores total, each adding one scope constructor and two router constructors
- Thus at most +2 scope constructors and +4 router constructors as an emergency
  envelope; not the full pilot's two-terminal-arm allowance

The outer chain is `integrated_m1.py:380-389,444-449,520-525`; a scope restore constructs
one temporary pilot/router and another restored router
(`causal_scope_revision.py:731-760,329-331`). Internal scope restore sites are
`619,640`. This envelope does not authorize an excluded constructor branch:
`_RevisionRejected` remains outside the currently supported inherited-C allocator
scope. Profiler poison raises BaseException and must not be converted into a native
ordinary-Exception rollback success. Failure before a save/inside decoder may create
fewer objects or partially constructed objects; census must preserve actual attempts,
births, errors and pending records rather than assume the maximum completed chain.

On success and failure alike, release the predictive readback first if allocated,
scrub model-retaining exception/traceback references, drop caller/candidate aliases,
dispose C6 through C1 for R then S in global reverse allocation order, finally release
initial owners and verify the registry returns to the empty baseline. No direct
registry deletion or private state clearing is allowed. Preserve each cleanup verdict,
including failed cleanup; finalization failure forbids a successful terminal manifest.
Sources: `g0_joint_ownership.py:655-680`; readback cleanup
`m1_path_native.py:350-367,379-388,424-429`; schedule cleanup analogue
`m1_path_pilot.py:395-425`.

## 9. Outstanding decisions and stopping boundary

Before any execution, parent approval and independent source review must settle:

1. This precise first-67-row / unchanged-receipt / two-post-third-clone proposal and
   its deliberately limited endpoint coverage
2. The exact positive call map/vector, arm-bound evidence validator, narrowly counted
   internal deepcopy repair and complete finite per-type allocation caps
3. Whether required concept/route coverage is satisfied by actual reached state or
   whether unobserved additional endpoints remain mandatory blockers
4. Successful historical G0, exact repaired-source delta reconciliation and separate
   probe launcher/one-shot admission without depending circularly on pilot clearance
5. Exact interpreter/stdlib/packages/import routes, owner-thread installation before
   native imports, resource limits, evidence capacity and finalization reserves
6. A separate exact probe execution clearance; publication or merge supplies none

The stopping boundary is completion of both fixed C5/C6 graph checks, their two
predictive roundtrips, complete census reconciliation and clean terminal disposal,
or the first declared failure. No continuation is selected after seeing the result.
The original 68-call pilot and all of its separate gates remain unchanged and disabled.
