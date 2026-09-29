# Fast Forge — R25 bounded reconciliation horizon recovery green

generation_id: `FORGE-20260930T035503+0900-FLY0-R25-BOUNDED-HORIZON-RECOVERY-GREEN`
status: `FORGE_INTERESTING / SYSTEM_BUILD_INPUT / NON_EVIDENTIARY / NONCANONICAL`

## Fresh authority

Human Directive freshness remained unchanged at `ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d` / active-index blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`.

Current authority used:
- Control R129; P0 remains OPEN / root cause UNKNOWN.
- Evidence Analyst R173.
- PRIMARY MAIN R199; M1-002 remains the critical path at exact head `2a21d3e879f1db4e81a58273180ad2124e823a5e`, CI green, required PR absent after five pre-GitHub refusals in R199.
- Relay remains unallocated.
- Methodology R153 / WELL_CALIBRATED.
- Theory R25.
- Literature R51 is the durable append-only generation already incorporated by R25/R173; moving latest/state remain older.
- Independent Audit R13.

Evidence Analyst R173 keeps SB003 `ALLOCATED_CONDITIONAL_INACTIVE`, admits the validated upstream receipt validator and repaired consumer composition only as bounded NON_EVIDENTIARY B/C inputs, and explicitly authorizes Forge work on R25 horizon adaptation, cycle-consistent recovery tests and scoped composed long-running acceptance. This generation performs that noncanonical Forge work only; it does not activate SB003 or change MAIN/Relay ownership.

## Probe and exact validated state

Branch:
`forge/20260930-fly0-bounded-horizon-recovery-a`

R25 source:
`forge_prototypes/fly0_bounded_reconciliation_horizon.py`

Source blob:
`0a604b98931b08e42a87fa9528fd6f9739c4c6f4`

Focused acceptance:
`tests/test_forge_fly0_bounded_reconciliation_horizon.py`

Final test blob:
`1e429aad804b2dde55fa5dd18374c6a475029c6c`

Exact validated code/test head:
`b21a9495e207ab7af66b021968985993c4428c31`

Final CI:
`36615136680` — push CI success on Python 3.11 and 3.13 through install, lint, local readiness, tests and bundle validation.

The source composes the already validated upstream receipt validator with the repaired reconciliation gate behind one shared monotonic `reconciliation_horizon_floor`. It bounds exact proof identity state and pending receipts while preserving causal uncertainty explicitly.

## Acceptance covered

The focused suite now covers:
- validator -> repaired consumer gate -> R25 horizon composition on structured, degree-preserving rewired, random sparse and reactive variants;
- exact in-window reconciliation and bounded retained identity count;
- pending masked/delayed lineage blocking horizon advancement unless explicitly expired;
- explicit expiry producing `DEGRADED_CAUSAL_GAP` rather than zero/no-event;
- out-of-horizon late outcomes returning `OUTSIDE_RETENTION_HORIZON` without WORLD mutation or watermark rollback;
- checkpoint/restore preserving pending state and allowing the same lineage to resolve later;
- checkpoint/restore preserving an advanced horizon, watermark, exact in-window replay identity and degraded causal-gap state;
- duplicate replay after restore remaining a no-op without clearing causal uncertainty;
- ordinary later receipts not clearing a causal gap;
- explicit authoritative resynchronization as the operation that clears degraded causal certainty;
- a 20-outcome long-running acceptance with retained exact identity state bounded by the configured four-outcome window instead of total history.

This is a bounded guarantee. It does not claim global/end-to-end exactly-once outside the retention horizon.

## CI / repair trace

The first newly landed acceptance head `858607dd6b5ef7f2cf71a4147b990b82c4048df8` triggered CI `36614087678`. Python 3.11 exposed a test-fixture error before the prototype assertions: the test instantiated `WorldState` outside its declared [-4, 4] world bounds. This was a fixture defect, not evidence for or against the horizon mechanism.

Fixture repair used the same-purpose bounded retry contract:
1. Contents update: pre-GitHub platform safety refusal.
2. Fresh readback + Contents update: pre-GitHub platform safety refusal.
3. Fresh readback + Git-data atomic test-file replacement: success at `d48d6e2dfcde36be8c30462a42de8ea077306e25`.

CI `36614612442` then passed on Python 3.11/3.13.

A final prospective recovery test was added to cover checkpoint/restore after horizon advancement and causal-gap creation. Its publication used:
1. Contents update: pre-GitHub platform safety refusal.
2. Fresh readback + Contents update: pre-GitHub platform safety refusal.
3. Fresh readback + Git-data atomic test-file replacement: success at `b21a9495e207ab7af66b021968985993c4428c31`.

Final CI `36615136680` passed on Python 3.11/3.13.

These observations remain P0 operational diagnostics only. They show nonuniform mutation behavior across attempts/routes but do not establish a root cause.

## Ordinary reduction

The component reduces to ordinary bounded event-log / execution-journal / idempotent-consumer / watermark / checkpoint-replay engineering.

The useful property is explicit uncertainty under bounded memory:
- forgetting old exact identity does not manufacture “no event”;
- an old item below the floor cannot mutate WORLD state;
- unresolved expiry remains visible;
- ordinary later traffic does not silently restore certainty;
- explicit resynchronization may restore exact observer state.

No new biological mechanism is required to explain the behavior.

## Disposition

`FORGE_INTERESTING / SYSTEM_BUILD_INPUT / NON_EVIDENTIARY / NONCANONICAL`

Recommended handoff: fresh Evidence Analyst reconciliation as optional SB003 Milestone B/C long-running receipt hardening. Forge does not self-admit it into SYSTEM_BUILD and does not alter SB003 activation conditions.

Scientific credit: `0`.

No biological fidelity/equivalence, fly-topology necessity/superiority, compute/energy efficiency, composition contribution, whole-system superiority, external validity or scientific novelty is established.

No M1-002 mutation, SYSTEM_BUILD allocation, canonical-science change, consumed FORMAL action, immutable evidence mutation, scheduler-state change or Work-backed execution occurred.
