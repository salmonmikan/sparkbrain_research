# Fast Forge — R28 issue-time provenance binding green

generation_id: `FORGE-20260930T175000+0900-FLY0-R28-ISSUE-TIME-PROVENANCE-GREEN`
forge_id: `FORGE-FLY0-R28-ISSUE-TIME-PROVENANCE`
theory_source: `Theory R28 — issue-time provenance binding`
status: `FORGE_INTERESTING`
recommended_handoff: `SYSTEM_BUILD_INPUT`
evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
scientific_credit: `0`
new_scientific_result: `false`

## Fresh authority

Human Directive freshness remained unchanged at `ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d` / active-index blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`.

Authority used and rechecked before publication:
- Control append-only R136 @ `76644d32199038ac9554324dd0ee28a8ad56adc6`; P0 remains OPEN / root cause UNKNOWN.
- Evidence Analyst R174 @ `8cce9c66fd31d5696b973b3bc9cf1dc12bacd5f8`.
- PRIMARY MAIN R209 @ `30057c5c7955a81185caddb1ec0dfb5ddf349f73`; M1-002 remains exact head `2a21d3e879f1db4e81a58273180ad2124e823a5e`, 1 ahead / 0 behind main, CI green, required PR absent after five pre-GitHub refusals.
- Relay unallocated; no collision.
- Methodology R153 / WELL_CALIBRATED @ `85267c9cae49bc61358c501ba36f5e9061421790`.
- External Science @ `85241792624ef375ff5c3179f0cca70c60e8e355`: append-only Theory R28, Literature R52, Independent Audit R14.
- SB003 remains `ALLOCATED_CONDITIONAL_INACTIVE`.

Theory R28 is an `INTEGRATION_DESIGN_PROPOSAL`, not scientific evidence. FORGE.md permits a bounded non-colliding Forge integration prototype from such a design; only Analyst may allocate a later SYSTEM_BUILD.

## Why now / target capability

The existing recovery fence calls `bind_source_frame()` at binding time and stamps the then-current recovery epoch. That leaves a concrete interface gap: historical raw source material retained across resynchronization can otherwise be presented later to a current-epoch binder.

Target capability: bind source causal identity at issuance time so resynchronization cannot turn historical source material into current lineage merely by delayed submission.

This work is parallel FLY-0 reliability hardening and does not touch MAIN's M1-002 branch.

## Prototype

Isolated branch:

`forge/20260930-fly0-issue-time-provenance-binding-a`

Validated base:

`fb42a34219e221ebb73140a56b743745a0febe37`

Source:

`forge_prototypes/fly0_issue_time_provenance_binding.py`

Source commit:

`00681d56ec4462378177283dca643d097b6c6865`

Source blob:

`2228919bb4b6a2a5619ec992598061050187a2e5`

Focused test:

`tests/test_forge_fly0_issue_time_provenance_binding.py`

Exact tested head:

`f65716dfbdd42dafc954dec9d9f3ea8dd621abe1`

Test blob:

`9e91e50e207800aa4768bcc96542d63ad491e3fc`

The prototype adds an immutable issuance stamp carrying WORLD session, WORLD cut generation, recovery epoch, source-frame token, source checkpoint token, issue ID and monotonic issue sequence. A bounded exact issue registry verifies the stamp before the existing recovery layer is permitted to construct its current-epoch envelope.

## Focused acceptance / CI

Push CI `36691794340` completed successfully on exact head `f65716dfbdd42dafc954dec9d9f3ea8dd621abe1`.

- Python 3.11 job: success.
- Python 3.13 job: success.
- lint: success.
- local readiness: success.
- tests: success.
- bundle validation: success.

Focused acceptance covers:
- structured, degree-preserving rewired and random-sparse variants;
- source issued before resynchronization is rejected after the WORLD cut advances;
- mutating the retained issuance stamp to current WORLD-cut/recovery values is rejected as an issue-identity conflict;
- a genuinely newly issued post-resync source continues through normal reconciliation;
- checkpoint/restore preserves an issue created before execution;
- exact issue identity retention is bounded and expired identity fails closed as outside the replay horizon;
- issue lineage cannot cross an explicit new WORLD-session boundary;
- the R14 same-session backward-anchor monotonicity guard remains intact.

The earlier source-only push CI `36691475946` also completed successfully at source commit `00681d56ec4462378177283dca643d097b6c6865`.

## Observation / reduction

The focused probe closes the specific delayed-binding restamp surface at this wrapper boundary: the current recovery envelope is created only after the immutable issue-time stamp has been proven current against WORLD session/cut, recovery epoch and retained issue identity.

Ordinary reduction: immutable provenance stamping, generation fencing, bounded idempotency/lineage retention and checkpoint/replay. A local SQLite/WAL single-writer issuance ledger remains the natural simplification comparator if process-level durability is needed.

This does not authenticate WORLD truth. WORLD truth remains the separate independently validated anchor/cut boundary from the R26 prototype. It also does not establish global exactly-once semantics outside bounded retention.

## Disposition

`FORGE_INTERESTING / NON_EVIDENTIARY / NONCANONICAL`

recommended_handoff: `SYSTEM_BUILD_INPUT`, subject to fresh Evidence Analyst reconciliation/allocation. Forge does not activate SB003 or allocate a build.

Engineering usefulness: this prevents historical source lineage from being laundered into the post-resync generation and supplies a bounded, checkpointable input primitive for later SB003 B/C integration.

Scientific claim boundary: no biological fidelity/equivalence, fly-topology necessity/superiority, compute/energy efficiency, composition contribution, whole-system superiority, external validity or scientific novelty is established. Scientific credit remains 0.

## P0 publication telemetry

P0 `INC-GITHUB-MUTATION-RECURRENCE-20260928-001` remains OPEN / root cause UNKNOWN.

For the prototype/test publication purpose:
- source create: succeeded on attempt 1;
- focused-test create attempt 1: pre-GitHub platform safety refusal;
- focused-test create attempt 2: pre-GitHub platform safety refusal;
- focused-test create attempt 3: pre-GitHub platform safety refusal;
- focused-test create attempt 4: succeeded after fresh branch/path readback;
- no alternate API/tool route was used to bypass the refused test-write boundary.

This is another nonuniform observation: the same scheduled runtime could successfully create the source, refuse three consecutive test-file writes before GitHub, then successfully create that test on the fourth bounded attempt. It does not establish a root cause.

No M1-002 mutation, SB003 activation, canonical science change, consumed FORMAL action, immutable evidence mutation, scheduler-state change, or Work-backed execution occurred.
