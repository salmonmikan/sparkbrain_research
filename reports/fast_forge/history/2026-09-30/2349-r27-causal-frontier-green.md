# Fast Forge — R27 causal frontier semantic acceptance green

- forge_id: `FORGE-FLY0-CAUSAL-FRONTIER-R27-FOCUSED-ACCEPTANCE`
- status: `FORGE_INTERESTING`
- evidentiary_status: `NON_EVIDENTIARY / NONCANONICAL`
- branch: `forge/20260930-fly0-causal-frontier-a`
- exact_tested_head: `8db5eb55e65cbd436e465cde8a879d90dad8cac2`
- source_blob: `ee91e7535f6d61b219d0a4a8c684a75d0cb6e514`
- focused_test_blob: `92232504539a16978c2c7a41c1a978cf2f8f2821`
- exact_head_ci: `36731193715`
- recommended_handoff: `SYSTEM_BUILD_INPUT`
- handoff_condition: `FRESH_EVIDENCE_ANALYST_RECONCILIATION`
- scientific_credit: 0

## Authority

Human Directive identity is unchanged at
`ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d` /
blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`.
Inputs: Control R140, Evidence Analyst R176, PRIMARY MAIN R212,
Methodology R153, Theory R29, Literature R53, Independent Audit R15.
Relay remains unallocated. M1-002 remains PRIMARY MAIN-owned at
`2a21d3e879f1db4e81a58273180ad2124e823a5e`; SB003 remains
`ALLOCATED_CONDITIONAL_INACTIVE`.

R176 requires green exact-head semantic acceptance plus fresh Analyst
reconciliation before any SYSTEM_BUILD handoff. This generation satisfies the
first condition only.

## Result

The import-order blocker was repaired at
`97d1024bd28a5c3d01fe9cc943dfd717f7aab05d`. CI `36730714337`
then reached semantic tests and exposed one implementation mismatch: a fresh
bounded reconciliation horizon legitimately starts with
`outcome_watermark=-1`, while the outer frontier rejected all negative
watermarks.

The bounded repair at `8db5eb55e65cbd436e465cde8a879d90dad8cac2` preserves non-negative
WORLD-cut/recovery/horizon counters while accepting exactly the existing
`-1` initial watermark sentinel and rejecting values below `-1`.

CI `36731193715` is green on Python 3.11 and 3.13 through Ruff, local
readiness, the full pytest suite, and bundle validation.

The focused acceptance now verifies that:
- structured / rewired / random-sparse inner recreation cannot reset a durable
  outcome watermark;
- wrong WORLD-session and older WORLD-cut inners are rejected;
- atomic rebase advances cut/recovery lineage and retires old issue lineage;
- stale anchor coverage cannot move the frontier backward;
- checkpoint tampering and restore behind the durable frontier fail closed;
- repeated rebases keep frontier metadata bounded and fixed-shape.

The previously repaired candidate-ledger seam is therefore exercised by tests,
not just source inspection.

## Disposition

R27 is engineering-green as a bounded monotonic causal-frontier primitive.
It is ordinary systems engineering reducible to state-machine/WAL/fencing
patterns. A local SQLite/WAL single-writer implementation remains a valid
simplification comparator.

Forge recommends it as optional SYSTEM_BUILD input, but only after fresh
Evidence Analyst reconciliation. Forge does not allocate or activate SB003.
R29 remains separate next-stage work for the Audit R15 issue-to-WORLD-commit
gap; R27 green status does not close that gap.

No biological fidelity/equivalence, fly-topology superiority, efficiency,
composition contribution, whole-system superiority, external validity or
scientific novelty is established. Scientific credit remains 0.

## P0

This run again showed non-uniform mutation behavior:
- import-order repair: first persistence attempt refused before repository
  mutation, second attempt succeeded;
- initial-watermark repair: first persistence attempt succeeded.

P0 `INC-GITHUB-MUTATION-RECURRENCE-20260928-001` remains OPEN / root cause
UNKNOWN. No scheduler state, canonical science, consumed FORMAL identity,
immutable evidence, M1-002, SB003 activation, or MAIN/Relay ownership was
changed. No Work-backed execution path was used.
