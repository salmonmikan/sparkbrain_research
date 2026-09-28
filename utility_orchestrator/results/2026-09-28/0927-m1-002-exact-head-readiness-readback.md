# Utility M1-002 exact-head readiness readback

schema_version: 2
completed_at: 2026-09-28T09:27:46+09:00
assignment_mode: AUTONOMOUS_IDLE
autonomous_task_id: UTILITY-AUTO-20260928T092541+0900-M1-002-EXACT-HEAD-READBACK
status: COMPLETED
evidentiary_status: NON_EVIDENTIARY_BUILD_PROVENANCE_AND_CI_RECONCILIATION_ONLY
classification: M1_002_EXACT_HEAD_SCOPE_AND_CI_VERIFIED_ANALYST_RECONCILIATION_PENDING

## Outcome

The MAIN-owned M1-002 branch now exists at exact head `2a21d3e879f1db4e81a58273180ad2124e823a5e`. Its parent is the Analyst-required base `59fc994b39d0ba02682e972161bb46801592d25b`, its tree is `2237f3b1e8ac72d193fc2c3879f2b67f71d302e0`, and exact-head push CI run `36361950457` completed successfully.

This satisfies the implementation/scope/CI evidence needed for the next authority boundary. It does not authorize Utility or MAIN to open or merge a PR. Evidence Analyst must freshly reconcile this exact head first.

## Scope and contract readback

Changed paths relative to the required base:

- `tests/test_system_build_m1_robustness.py` (new)
- `docs/SYSTEM_BUILD_M1_ROBUSTNESS.md` (new)
- `docs/SYSTEM_BUILD_M1.md`
- `docs/PROJECT_STATUS.md`
- `artifacts/validation_manifest.json`

No `src/sparkbrain/**` path changed. No M1 algorithm, threshold, routing topology, public runtime field, resource maximum, FLY-0, Theory or canonical-science change was observed.

The harness fixes and asserts:

- nominal 64-cycle committed-state invariants;
- checkpoint/replay cutpoints 1, 8, 31 and 63 through cycle 64;
- all seven existing fault points at early/middle/late positions 1, 31 and 63, with exact rollback and next healthy-cycle equality;
- duplicate receipt, conflicting receipt identity, reused event identity, pending overlap and mismatched pending receipt no-write/continuation behavior;
- exactly 267 committed acceptance cycles, below the Analyst cap of 512.

## Verification

- exact-head CI: [run 36361950457](https://github.com/salmonmikan/sparkbrain_research/actions/runs/36361950457)
- event: `push`
- status/conclusion: `completed/success`
- Python 3.11 job: success (install, lint, readiness, full test, bundle validation)
- Python 3.13 job: success (install, lint, readiness, full test, bundle validation)
- independent focused command on the exact remote tree:
  `TMPDIR=/dev/shm python -m pytest -q tests/test_system_build_m1_robustness.py`
- focused result: `1 passed`
- diff hygiene: `git diff --check` passed
- exact remote tree equals the independently tested local tree: `2237f3b1e8ac72d193fc2c3879f2b67f71d302e0`

## Ownership and collision checks before final publication

- Utility assignment: schema-v2 clean IDLE; assignment blob `a88c6cee9ac0608a701d51f083cf275425d44515`
- Control: `CTRL-20260928T084949+0900-R105-M1-ROBUSTNESS-ALLOCATED`
- Evidence Analyst: `EVA-20260928T090051+0900-R164-M1-WAIT-FLY0-HANDOFF-REVIEW`
- MAIN durable state: `MAIN-20260928T072510+0900-PRIMARY-R169-M1-INTEGRATED`
- Relay: intentionally disabled; no competing allocation
- exact M1-002 head unchanged before final publication
- Utility performed readback and focused verification only; no MAIN-owned or scientific mutation

## Scientific boundary

M1-002 remains `NON_EVIDENTIARY_BUILD`. This readback establishes engineering scope compliance and exact-head verification only. Comparative support remains false, composition contribution is not established, scientific novelty is false, and scientific credit is 0.

No scientific execution, comparator run, held-out access, FORMAL action, FLY-0 promotion, SB003 allocation or claim reinterpretation occurred.

## Stop and next action

stop_reason: BOUNDED_M1_002_EXACT_HEAD_READINESS_READBACK_COMPLETE

next_action: Evidence Analyst must reconcile exact head `2a21d3e879f1db4e81a58273180ad2124e823a5e`, tree `2237f3b1e8ac72d193fc2c3879f2b67f71d302e0` and CI run `36361950457` before any PR/merge continuation. Utility does not become a dependency and takes no further action.
