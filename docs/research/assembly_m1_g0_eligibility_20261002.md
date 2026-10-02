# G0: real producer–M1 ownership eligibility

2026-10-02 UTC. **SOURCE-ONLY / NONCANONICAL / NON_EVIDENTIARY**.
Scientific credit: **0**. Status: **BLOCKED_SOURCE_CONTRACT_GAP**.
No SparkBrain import, construction, checkpoint load, producer call or M1 transition
is authorized by this document or its auditor. This is preparation, not a live harness
or a completed ownership test. The existing fake sentinel is unchanged.

## Decision and useful finding

The next integration gate cannot safely reuse the producer-only whole-object copy
procedure on the joined M1 graph. The real M1 facade owns a reentrant lock tied to a
module-global weak registry; its underlying runtime owns an RNG and additional state
classes. The existing exact-type producer auditor correctly rejects those objects.
Its allowed set elements also exclude the reference runtime's populated
`tuple[str | None, str]` candidate keys.

Nor does existing native M1 checkpointing supply a complete replacement oracle:
its nested direct checkpoint is a tree encoding, not an alias-preserving reference
graph. It serializes repeated references independently, canonicalizes mapping order,
reconstructs generic mappings, and creates a new facade/lock registry binding. Save-back
bytes and native hashes can agree while properties of the original object graph differ.
This is a scope limit of the existing checkpoint contract, not a demonstrated runtime
bug or a reversal of its previously accepted continuation results.

The smallest useful deliverable now is the source-bound eligibility auditor and the
explicit prospective transaction contract below. Extending a fake's success to the real
system, skipping unsupported fields, or bypassing the wrapped reference brain would
hide the exact problem G0 is intended to test.

## Sources and authority

Source snapshot: `main@2682b895435f79c9723934e2c116e440719304d8`.
The [machine source contract](../../artifacts/research/assembly_m1_g0_20261002/source_contract.json)
binds five files, nine inspected symbols, their exact SHA-256 values, four blockers
and eight future case IDs. The auditor reads files as data and parses ASTs; it does
not import the inspected modules. Hashes bind the selected bytes; token checks and
AST ranges are only narrow source witnesses, not a whole-program proof. Duplicate JSON keys, nonfinite constants and overflowed numbers reject before source access. The complete
logical contract is itself digest-pinned to reject reduced/relabelled fact inventories.
The source commit is declared provenance checked during preparation; the auditor does
not query Git or independently prove commit membership.

Repository AGENTS/common/scientific-integrity/active-policy files were fetched from
main. The authoritative active Human Directive index was fetched explicitly from
`ops/human-directives`, index blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`.
The full [HUMAN-20260928-001 integration directive](https://github.com/salmonmikan/sparkbrain_research/blob/ops/human-directives/ops/human_directives/history/2026-09-28/HUMAN-20260928-001-accelerated-integrated-sparkbrain-completion.md)
prioritizes the integrated observation–state–action–outcome–revision loop, while
preserving fresh prospective contracts and the build-to-science boundary.

This is separately requested cloud research, not a scheduler invocation or allocation
of a SYSTEM_BUILD milestone. Scheduler/control state, role-owned work, runtime source,
shared acceptance/claim/status/result ledgers, immutable evidence, and consumed scientific
identities are outside this change. Actual execution requires a later exact implementation
freeze and explicit execution clearance. Publication or CI does not confer that clearance.

## Source audit

- `system_build/integrated_m1.py`: `observe` uses both predictive and scope components;
  `apply_outcome` can fail after predictive revision; `_restore_components` reloads the
  predictive object and reconstructs scope/compositor state. No v0.5 object or adapter
  pending binding participates in these transactions.
- `v032/runtime.py`: `_shared_step_lock` accesses a global weak registry;
  `IntegratedV032Brain.__init__` retains that lock. `step` temporarily installs an
  instance callback and restores it in `finally`; only quiescent boundaries are candidates
  for snapshots. Synchronization state cannot be silently dropped from a completeness claim.
- `v03/runtime.py`: `_initialize_runtime` creates the RNG, histories, results, trace and
  other nested state. Restrict the first target to default I1/E0, no supplied revision
  model; I3/Torch would expand this scope.
- `v032/checkpoint.py`: `_encode` tracks a recursion stack rather than a reference table;
  `_decode` reconstructs mappings and children independently. This handles RNG values
  but does not prove alias topology or original concrete mapping types/order.
- `scripts/v05_acquired_ownership_probe.py`: the existing typed/reference auditor is
  attributed prior engineering. Its exact-class, exact-field and mutable-identity checks
  remain useful for the producer; its whitelist is not a joint M1 ownership contract.

M1 additionally retains its supplied `M1Observation`; the frozen dataclass contains a
mutable sensory dictionary. The new coordinator must detach caller data before handing
it to M1 and retain the exact pre-outcome feature vector for credit assignment.

## Proposed ownership strategy, still unimplemented

A private outer owner holds one complete logical joint state: producer, M1, dictionary,
clock, pending observation/export/receipt binding and committed receipt ledger. It must
never publish components independently.

1. Preflight all inputs, actual configured feature limits, source bindings and graph
   eligibility before either component advances.
2. Construct a private candidate by an explicitly supported method. Producer copying can
   reuse the existing fresh-memo approach. M1 fresh serial replay from a frozen ordered
   observation/outcome log is a candidate method, not an established clone.
3. Verify complete declared state, internal reference relationships and owner/candidate
   mutable disjointness. Cover exact RNG state and every new supported class/container.
4. Advance producer, export native features, detach the adapted observation, call real
   M1, validate/export outputs and preserve pending binding inside that candidate.
5. On any failure, discard the entire candidate; the owner pointer and complete owner
   state must remain exact. Do not restore over the original owner.
6. On success, publish one joint owner pointer only after all validation and evidence
   writes required for that transaction succeed. Delayed feedback uses the same private
   candidate/publish discipline, preserving one pending occurrence.

The required new oracle must separately inventory computational graph state and
synchronization resources. Specify exclusive serial access, quiescence, lock identity
and registry bindings for each owner/candidate; reject unsupported activity. Recreated
locks cannot be described as bitwise rollback of process-global synchronization state.
If that boundary cannot be justified without runtime changes, stop and request a
separately scoped change. Neither native serialization nor opaque state hashes can stand
in for the explicit graph/alias checks. Fresh replay must be checked, not assumed equal.

## Prospective G0 case inventory

This is a case proposal, **not an executable freeze**. Exact literal inputs, source/type
registry, reconstruction steps, faults, beforestates and counters must be frozen and
independently reviewed before any model is imported or constructed.

- G0-01: malformed input/configured headroom/schema rejection before component advancement
- G0-02: complete real producer/M1/coordinator copy or reconstruction equality and isolation,
  at a nonempty acquired/one-receipt boundary
- G0-03: abort after actual producer advancement, before M1 observation
- G0-04: abort after actual M1 observation, before joint publication; include a distinct
  export-validation failure after both components have advanced
- G0-05: fault after real M1 predictive feedback, retaining the exact pending joint owner;
  do not assume M1's internal native rollback itself preserves graph identity
- G0-06: successful joined publication; preserve both old owner and new owner inventories,
  plus an independently reconstructed reference continuation for the declared comparison
- G0-07: identical receipt replay and conflicting receipt rejection; no producer re-extraction
  or duplicated credit; report their distinct outcomes
- G0-08: mutate actual caller sensory/pulse metadata and detached outputs after preservation;
  prove those mutations cannot alter acquired owner or committed joint state

Use one inherited, explicitly exposed PR182 acquisition recipe for G0 engineering only;
no new performance comparison, favorable seed selection or candidate-count rescue.
Use a fixed positive teaching outcome for a nonempty M1 state; do not force opposite
signs into one identical routing context merely to manufacture a control failure.

Planning envelope: one acquired producer root, at most 80 producer calls, 32 real M1
observations and 32 outcomes, 16 private joint candidates, 600 CPU seconds, 900 wall
seconds, 1 GiB address space and 256 MiB retained evidence. Include replay/reconstruction
and finalization in those caps. These are planning ceilings, not executed counts or a
performance prediction. The implementation freeze must enumerate exact calls per case;
if the supported strategy cannot fit, revise the proposal **before results**, not after.
The separate 192-call representation experiment is not authorized or scheduled here.

G0 passes only for the exact exercised graphs and faults after all accepted cases,
rejected cases, owner-pointer transitions, graphs/aliases and real resource counts are
retained. Failure, unsupported types, incomplete evidence and budget exhaustion remain
explicit outcomes; none authorize a retry or a looser oracle. G0 cannot establish cold
restart, arbitrary-state cloning, concurrency, generalized efficacy or scientific novelty.

## Downstream comparison safeguards

A later feature experiment must train S/native, serious raw-history replacement R, and
zero-context Z consumers separately with identical M1 configurations, hypothesis/router
capacity, teaching/feedback access and causal input cutoff. Retain all native coordinates;
do not select a favorable subset. Equal vector width alone does not imply equal resources:
record acquisition work, raw histories, prototype stores, full producer/consumer state and
all candidate copies. No arm may use target-derived representation values.

M1 has exactly two scope components, independently of its eight-dimensional vector cap.
A third native or raw cluster can therefore reject on capacity. Z may reject opposite
sign outcomes as `identical_observation_conflict`. Keep action abstention, input rejection,
receipt conflict, capacity exhaustion and unsupported ownership distinct. A terminated
comparator cannot be silently scored as bad accuracy or used to claim superiority. Compare
utility only on prospectively defined evaluable coverage; otherwise report comparative
utility as not evaluable. Always retain whole-stream coverage, termination and rejection
rates alongside any prospectively shared evaluable subset. Do not weaken R or alter its encoder after seeing S's performance.

A real swap/sham result without an efficacy advantage establishes only a representation
path contribution. Prediction changes, scope changes and final action changes are separate
observations. Plasticity necessity and physical assembly causality still require fresh
matched ablations; PR169's negative comparison and PR182's producer-only boundary remain.

## Literature constraints

- [Maass, Natschlaeger and Markram (2002), original author-hosted paper](https://igi-web.tugraz.at/people/maass/psfiles/130.pdf)
  distinguishes separation of internal trajectories from useful readout approximation.
  A separated native export does not itself establish useful downstream computation.
- [Littman, Sutton and Singh (2001), original proceedings paper](https://proceedings.neurips.cc/paper/2001/file/1e4d36177d71bbb3558e43af9577d70e-Paper.pdf)
  defines predictive state through sufficiency for future tests. This bridge neither
  implements PSRs nor inherits their theoretical guarantees.
- [McCallum (1994), original proceedings paper](https://papers.nips.cc/paper/1994/file/d2ed45a52bc0edfa11c2064e9edee8bf-Paper.pdf)
  provides established history-based state-disambiguation prior art. A current-input-only
  control is therefore insufficient evidence of a special assembly advantage.

## Verification performed

The source auditor bound five source files and nine symbol-level facts. Its successful
exit means the selected source bindings matched; reported G0 status remains blocked.
Thirty-seven focused model-free tests passed, including source drift, boundary corruption,
path escape, missing/ambiguous symbols, reduced/relabelled contracts, contract non-mutation
and a subprocess import
finder that rejects every SparkBrain import. Scoped Ruff passed. No fake sentinel was
modified or reused as evidence of real integration.

Commands:

```bash
python -B scripts/verify_assembly_m1_g0_eligibility.py
python -B -m pytest -q tests/test_assembly_m1_g0_eligibility.py
ruff check scripts/verify_assembly_m1_g0_eligibility.py tests/test_assembly_m1_g0_eligibility.py
```

Full repository runtime tests/demo/benchmark were intentionally not run in this
source-only scope. The real G0 implementation and execution, external independent review,
current-head Codex review and CI remain separate gates. Independent source-only review
found no publication blocker and identified contract-hardening improvements; the final
auditor now pins the complete logical contract and adds five corruption tests. No G0 pass or runtime readiness
is claimed by this preparation.

### Codex source-auditor correction

Review of initial head `2f29900a09733122c085c6f948a39f1d92719fbe` identified that
ordinary JSON loading silently accepts duplicate keys before logical contract hashing.
The corrected loader rejects duplicates at every object depth and nonfinite constants.
Five added tests reject conflicting/identical root keys, nested duplicates and NaN before
source-file access. This is a source-auditor parsing repair; no runtime or experiment
semantics changed and no G0 execution occurred. Initial-head CI passed; latest-head CI
and Codex re-review are required before merge.

Review of head `d42f7490fd89a7f96352e7a762a380bf5a3e6488` additionally identified
that standard JSON numeric literals such as `1e400` bypass `parse_constant` and become
infinity through default float parsing. A finite-checking `parse_float` hook now rejects
those values during parsing. The nonfinite test covers NaN, signed Infinity and three
positive/negative overflow literals, bringing the suite to 37 tests.
