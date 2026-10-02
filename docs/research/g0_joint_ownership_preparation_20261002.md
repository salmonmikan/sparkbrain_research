# G0 joint ownership adapter preparation

2026-10-02 UTC. **SOURCE-ONLY / NONCANONICAL / NON_EVIDENTIARY**.
Scientific credit **0**. Real G0 **NOT EXECUTED**.

This prospective implementation follows [PR184](https://github.com/salmonmikan/sparkbrain_research/pull/184),
whose source-only eligibility finding remains unchanged. It addresses a concrete route
through the lock/RNG/alias blockers, rather than treating a fake sentinel or native
checkpoint equality as real integration evidence. No production runtime source changes.
No producer or M1 is imported, constructed, advanced, restored, or replayed by preparation.

## Source scope and limits

The [source contract](../../artifacts/research/g0_joint_ownership_preparation_20261002/source_contract.json)
pins 28 class-bearing files and 101 selected class declarations at main
`a6aa0addfcd8f73b72a796ebd8c5625a0a2347dd` (tree
`ae2823ae487d9e22c1a21c46e5a2457ab5c6921a`). A separate complete inventory also pins all 157 runtime Python files and 15 schema JSON
files, including the constructor/checkpoint/save/load dependency chain. Added, missing or
changed dependency files fail closed. Its AST auditor parses source bytes without importing them. It distinguishes dictionary-backed and slot-backed fields
and excludes handwritten copy/reducer/finalizer hooks. AST field witnesses are a proposed
allowlist, not proof that a future live graph is fully covered. Any unsupported live field
or type must stop before candidate dynamics, with no whitelist relaxation within that run.
The separately pinned prior acquired-ownership auditor supplies attributed graph-audit
design provenance; it is not imported or invoked by the new adapter. Its original runtime
results and limitations are unchanged.

Only default I1/E0, no supplied revision model, is proposed. Torch/I3, arbitrary mappings,
arbitrary subclasses and concurrent access are outside scope. Source-only test fixtures
are explicitly stand-ins. Their passing results do not establish real M1 support.
The future executable freeze must bind the adapter, registry, full runtime package,
literal inputs, interpreter/library environment, resource counters, faults and runner.
Source publication, a successful AST audit, review and repository CI do not authorize it.

The ordinary registry entry point is explicitly synthetic. A separate dormant
`from_verified_source` entry point accepts already-loaded classes only after verifying
the pinned source contract and exact module/name/path bindings. It imports no runtime
modules. In verified-source mode, the facade constructor and weak-registry/guard must be
the exact source module bindings, not a lookalike registry. These origin checks are not
in-memory bytecode attestation: the future dedicated runner must freshly load the pinned
package after source/environment admission, excluding stale bytecode, custom import hooks,
process monkeypatching and externally supplied class implementations. Class files being
correct on disk alone cannot prove arbitrary preexisting process memory is correct.

## Construction strategy

Use one fresh memo for the complete joint producer, M1, clock, immutable-coordinate
dictionary, pending binding and receipt-log root. Independently audit the source root
before allocating candidates. Source-whitelisted object shells and their actual
`__dict__`/slots must be populated through that memo; generic object reconstruction can
otherwise duplicate a dictionary referenced both as object state and elsewhere in the root.

An exact `random.Random` adapter creates `Random(0)` and restores the complete saved RNG
state, including Gaussian cache, without drawing random values or requesting system entropy.
The Python instance dictionary and aliases are separately preserved and audited.

For each source-approved facade, first clone its underlying v0.3 graph, then invoke the
existing `IntegratedV032Brain(base=cloned_base)` constructor. It creates no new underlying
model and obtains the legitimate lock through the runtime's own weak-registry mechanism.
Memo entries for original facade, lock and instance dictionary must all point to their
corresponding new objects. Multiple facades over one underlying brain share one lock;
different cloned brains must not. Rawbrain-to-facade cycles that prevent this construction
order are rejected, not repaired by calling methods on an incomplete brain.

The graph oracle preserves types, ordered mappings/sequences, deque bounds, exact float
representations, typed set membership and reference topology. In particular,
`set[tuple[str | None, str]]` is supported without coercion. Class fields are not converted
with dataclass `asdict`, JSON or native checkpoint roundtrips. Unknown proxies/custom mappings
are rejected rather than flattened. Complete graph equality uses traversal-relative node
labels; separate live identity checks require disjoint mutable owner/candidate objects.
Original-source noninterference additionally compares identity-to-traversal-node
correspondence, so exchanging two equal original objects cannot pass merely because the
value graph remains isomorphic and its mutable identity set is unchanged. The same checks
cover every separately retained root.

## Synchronization is an explicit resource contract

Locks and the module-global registry are not silently omitted from a completeness claim.
Their contract is resource noninterference in a dedicated, strictly serial worker, not
bitwise equality of the entire process or equality of original/candidate lock identities.

- Pin CPython and the exact native lock types/APIs. Unsupported inspection fails closed
- At audit boundaries, no facade step is active and no temporary sensory callback remains
- Reject an owned/reentrant lock; a balanced nonblocking acquire/release probe verifies
  availability. This is a synchronization probe, not a nonmutating heap observation
- Snapshot registry bindings under its guard; the exact controlled live underlying brains
  must map to their declared unique locks, without missing/replaced/unexpected bindings
- Candidate allocation adds only declared bindings through the existing facade mechanism;
  original owner lock identities and registry pairs remain exact
- Failure exports contain primitive data, never object-bearing exceptions or tracebacks
- Discard candidate, memo, audit object tables, closures and traceback references before
  checking bounded garbage-collection cleanup. No manual registry deletion is permitted
- A leak or extra registry entry is a resource failure and terminates the attempt
- Retained successful predecessors remain explicitly declared live owners

Each clone request must also name separately retained live roots. They are independently
audited but never implicitly cloned with the active source. Registry completeness includes
these roots, and the new candidate must be mutable-disjoint from every one of them. The
minimal lifecycle is nested: discard temporary candidates in reverse allocation order so
each cleanup restores its captured baseline. An unsupported disposal order fails closed;
it is not permission to ignore another candidate's registry entry. The prospective runner
must retain and declare successful predecessors explicitly at every subsequent clone.

An M1 internal rollback may construct an additional replacement facade/base before the
whole candidate is discarded. The lifecycle inventory must cover these transient births,
not assume exactly one added registry entry throughout a candidate's lifetime. Candidate
cleanup must restore the original registry baseline after all such temporary roots die.

## Candidate real G0 protocol, not an executable freeze

The smallest next real test is one inherited, explicitly exposed acquisition recipe from
PR182, followed by actual producer-to-M1 observations and positive teaching feedback.
Use a fresh G0 engineering identity. Never rerun the consumed PR182 identity or relabel
its stored results. No outcome-dependent seed choice, additional acquisition or rescue.

Before admission, freeze exact literal acquisition/query rows, event/receipt IDs, copied
configurations, graph registry, source/environment hashes and the per-case call schedule.
Proposed exposure: the first declared nuisance seed 910071, its complete 64-window A32/B32
acquisition prefix, and the unchanged native all-mature-coordinate export rule. This is
known development exposure, not a fresh scientific replicate. Reject absent/colliding
dictionaries, native ties, unsupported graphs or insufficient actual M1 dimensional capacity.
Never truncate native coordinates or weaken the comparator to make a test fit.

Bootstrap one successful joint observation and one fixed positive `+0.8` teaching receipt
to obtain nonempty M1 hypotheses/routes and a nonempty committed receipt ledger. Subsequent
cases start from the declared bootstrap or pending boundary. Preserve exact pre-outcome
native features in the pending binding; detach caller sensory/pulse data and outward results.

1. Malformed/schema/capacity rejection before either component advances
2. Two private candidates at the nonempty boundary: exact graphs/aliases, resource mapping,
   and all pairwise mutable-disjointness checks; dispose both without dynamics
3. Abort after real producer advancement, before M1 observes
4. Abort after real M1 observation; separately fail export validation after both advance
5. Successful observe against a separately cloned direct reference, then one owner-pointer
   publication. Keep predecessor and successor graphs and independent resource inventories
6. At that pending boundary, inject the real `after_predictive_revision` fault and discard
   the entire candidate, including native rollback-created replacement resources
7. Successful outcome against a separately cloned reference, followed by one joint publish
8. Exact receipt replay and changed-value identity conflict: no repeated producer extraction
   or duplicated credit; distinguish the two outcomes and retain unchanged-state evidence
9. Mutate actual caller metadata and detached outputs; verify both retained owners are intact

An illustrative bounded schedule uses 14 private candidates, 70 producer calls (64 prefix
plus six queries), five real M1 observations and six M1 outcome API invocations. Replay and
conflict API invocations count even when they do not call predictive feedback. The exact
runner must independently derive and check these totals before execution; these are not
observed counts and do not authorize additional work if construction needs more calls.
The earlier planning maxima of 80 producer calls, 32 observations, 32 outcomes, 16 candidates,
600 CPU seconds, 900 wall seconds, 1 GiB address space and 256 MiB evidence remain ceilings.
Acquisition, adapter construction, reference branches, internal rollback loads and finalization
all consume the envelope. Any prospective revision must happen before live results.

All required evidence writes precede publication of the owner pointer. A later terminal
evidence-write failure cannot be reported as a verified successful run. Process crash
consistency, native cold restart, arbitrary-state cloning and concurrency are excluded.
Unsupported coverage, cap exhaustion, cleanup failure or partial evidence are retained
terminal outcomes, not permission for an unrecorded retry or a weaker oracle.

## Acceptance and next boundary

Preparation acceptance requires adversarial model-free adapter/resource tests, exact static
source binding, independent implementation review and exact-head Codex/CI. Passing them
only validates preparation within the tested stand-in fixtures. The real G0 runner,
prospective execution freeze, execution clearance, actual graph coverage and actual lifecycle
results remain separate gates. No new project acceptance, claim grade or scientific credit
is assigned here; shared status/results ledgers and scheduler/control state are unchanged.

Repository CI runs its normal software regression suite separately. The source-only local
preparation checks intentionally exclude full runtime tests/demo/benchmark and all actual
G0 producer/M1 activity. Passing ordinary CI cannot be counted as a real G0 execution.

### Local preparation checks

The adapter suite has 56 model-free cases and the static source auditor has 14. The
broader relevant set also includes 18 existing acquired-ownership helper cases and 78
existing history-export helper/evidence cases. They use stand-ins or already retained
primitive evidence, not fresh producer/M1 activity. Exact final pass/fail evidence and
independent review are recorded with the PR; current-head CI/Codex are separate checks.

```bash
python -B scripts/verify_g0_joint_source_contract.py
python -B -m pytest -q tests/test_g0_joint_ownership.py tests/test_g0_joint_source_contract.py \
  tests/test_v05_acquired_ownership_runner.py tests/test_v05_history_export_evidence.py \
  tests/test_v05_history_export_runner.py
python -B -m ruff check --no-cache scripts/g0_joint_ownership.py \
  scripts/verify_g0_joint_source_contract.py tests/test_g0_joint_ownership.py \
  tests/test_g0_joint_source_contract.py
```

An additional source constraint remains for a later, longer M1 continuation: the native
direct-checkpoint registry does not list `_MutableConcept`, which its concept observer can
retain after repeated co-occurrence. This is a source-level compatibility concern, not an
observed runtime failure here. The proposed G0 branch schedule reaches at most two M1
observations along a continuation and makes no mature-concept/native-restore generalization.
Its graph registry includes that class, but this does not repair or certify native checkpoints.

A later efficacy comparison still requires separately trained native/raw-history/zero-context
consumers with equal feedback and capacity, prospective evaluable-coverage rules, and full
coverage/rejection/resource reporting. G0 itself cannot establish benefit, biological
equivalence, physical assembly necessity, generalization or scientific novelty.
