# Fast Forge — R27 causal frontier focused acceptance persisted; lint repair blocked

- forge_id: `FORGE-FLY0-CAUSAL-FRONTIER-R27-FOCUSED-ACCEPTANCE`
- status: `FORGE_PROTOTYPE`
- evidentiary_status: `NON_EVIDENTIARY / NONCANONICAL`
- branch: `forge/20260930-fly0-causal-frontier-a`
- source_head_before_test: `2ccb4df11241b8547b69c06c6d8731f245625c27`
- focused_test_commit: `b427a2417c3657cedcf9886a8b3041785f34e533`
- focused_test_blob: `10ced27c7eabea4e9ec3ef01b31808ca7a9e4612`
- candidate-ledger repair commit: `6c246ce34f2b4e51e6521b19240e7d39b908c6d0`
- repaired source blob: `a5fe6115e32672c06abf32bd428845f9cf9a2657`
- recommended_handoff: `NONE_UNTIL_FOCUSED_ACCEPTANCE_GREEN`
- scientific_credit: 0

## Fresh authority

Human Directive identity is unchanged at
`ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d` /
active-index blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`.
No directive delta was observed.

Current durable inputs used in this run:
- Control R138;
- Evidence Analyst R174;
- PRIMARY MAIN R211;
- Methodology R153 / WELL_CALIBRATED;
- Independent Audit R14;
- append-only Literature R53;
- append-only Theory R29;
- Relay unallocated;
- M1-002 remains PRIMARY MAIN-owned at exact head
  `2a21d3e879f1db4e81a58273180ad2124e823a5e`;
- SB003 remains `ALLOCATED_CONDITIONAL_INACTIVE`.

Theory R29 is newer than the moving Theory R27 pointer and explicitly records
the current R27 causal-frontier source as source-only/unverified. R29 proposes a
later issue-to-WORLD-commit lineage join, but this run did not stack that new
primitive on top of an unverified frontier. The narrower prerequisite was
focused first.

## Focused acceptance publication

The previously missing focused test now exists at:

`tests/test_forge_fly0_causal_frontier.py`

The create purpose succeeded on attempt 2 after attempt 1 was refused before
GitHub mutation execution. Independent readback verified blob
`10ced27c7eabea4e9ec3ef01b31808ca7a9e4612`.

The test covers:
1. structured / rewired / random-sparse inner recreation cannot reset a durable
   outcome watermark;
2. an inner reconciler attached to a different WORLD session must be rejected;
3. atomic rebase advances cut/recovery lineage and retires older R28 issue
   lineage;
4. a same-session stale anchor below the durable watermark cannot move the
   frontier backward;
5. checkpoint tampering and restore into an inner reconciler behind the durable
   frontier fail closed;
6. repeated rebases keep the outer frontier checkpoint fixed-shape.

## Candidate-ledger seam found and repaired

While preparing the focused acceptance, source inspection found that
`SessionCausalFrontierGuard._observe(candidate)` was reading
`self._ledger.world_session_id` and `self._ledger.world_cut_generation`
rather than the candidate reconciler's attached ledger. That meant the
`WRONG_WORLD_SESSION` / candidate `WORLD_CUT_ROLLBACK` checks could not
actually distinguish a candidate attached to another/older WORLD ledger.

A bounded Forge repair was persisted at
`6c246ce34f2b4e51e6521b19240e7d39b908c6d0`. The guard now inspects the
candidate reconciler's attached `WorldSessionLedger`, verifies constructor
ledger/session-cut agreement, and uses the candidate ledger for observed
session/cut identity. No canonical or previously validated scientific object
was changed.

## CI result

CI run `36710041575` on the test-publication head failed in lint on both
Python 3.11 and 3.13 before Local readiness / Test / Validate bundle ran.

CI run `36710169579` on the candidate-ledger repair head also failed in lint
on both Python 3.11 and 3.13 before semantic tests ran.

The directly observed lint error in both jobs was:

`F401 [*] dataclasses.replace imported but unused`

in the new focused test file. Therefore there is currently no semantic
acceptance evidence for the repaired causal-frontier head.

A dedicated focused-test lint-repair publication purpose was attempted five
times. Every attempt was refused before GitHub mutation execution with the
runtime/platform safety refusal. The test blob remained unchanged after the
ceiling was exhausted, so no alternate write route was used.

## Disposition

`FORGE_PROTOTYPE / FOCUSED_TEST_PERSISTED / SOURCE_REPAIRED /
CI_LINT_BLOCKED / SEMANTIC_ACCEPTANCE_NOT_RUN / UNVERIFIED /
NON_EVIDENTIARY / NONCANONICAL`.

No SYSTEM_BUILD handoff is recommended yet. The R28 issue-time provenance
exact-tested head remains independently engineering-green and is not downgraded
by this result.

The R27/R29 engineering remains reducible to established monotonic state
machine, fencing, WAL/idempotency and transaction-lineage patterns. Nothing in
this run establishes biological fidelity/equivalence, fly-topology necessity or
superiority, compute/energy efficiency, composition contribution, whole-system
superiority, external validity, emergence or scientific novelty.

## P0 observation

This run again produced non-uniform mutation behavior on the same branch:
- focused test create: attempt 1 pre-GitHub refusal, attempt 2 success;
- causal-frontier source repair: attempt 1 success;
- focused-test lint repair: 5/5 pre-GitHub refusal.

This is evidence about the tested mutation surfaces only. It does not establish
a repository-wide GitHub outage or identify the root cause.

P0 `INC-GITHUB-MUTATION-RECURRENCE-20260928-001` remains OPEN / root cause
UNKNOWN.

No M1-002 mutation, SB003 activation, canonical science change, consumed FORMAL
rerun/retune/rescore, immutable evidence mutation, MAIN/Relay ownership change,
scheduler-state mutation, or Work-backed execution occurred.
