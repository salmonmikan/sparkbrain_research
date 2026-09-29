# Fast Forge — R25 bounded reconciliation horizon source persisted, focused acceptance blocked

generation_id: `FORGE-20260930T0230+0900-FLY0-R25-BOUNDED-HORIZON-TEST-PUBLICATION-BLOCKED`
status: `FORGE_PROTOTYPE / UNVERIFIED / NON_EVIDENTIARY / NONCANONICAL`

## Fresh authority

Human Directive index remained unchanged at head `8ce979b9ec0bc7eede5225c0403698f8886d3e8d` / blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`.

Current authority used:
- Control R129; P0 remains OPEN / root cause UNKNOWN.
- Evidence Analyst R173.
- PRIMARY MAIN R198; M1-002 remains the critical path at exact head `2a21d3e879f1db4e81a58273180ad2124e823a5e`, CI green, required PR absent after five pre-GitHub refusals.
- Relay unallocated.
- Methodology R153 / WELL_CALIBRATED.
- Theory R25.
- Literature R51.
- Independent Audit R13.

Analyst R173 admits the exact tested upstream receipt validator `9cbb8949c26bf6ff9fd030b5fe6e2328310d2c74` and its repaired consumer-gate composition only for bounded NON_EVIDENTIARY SB003 B/C engineering use. Long-running receipt reconciliation remains held for R25 horizon adaptation, cycle-consistent recovery tests and scoped composed long-running acceptance. SB003 remains `ALLOCATED_CONDITIONAL_INACTIVE`.

## Probe

Created isolated branch:

`forge/20260930-fly0-bounded-horizon-recovery-a`

from validated upstream-receipt composite head:

`9cbb8949c26bf6ff9fd030b5fe6e2328310d2c74`.

Persisted source:

`forge_prototypes/fly0_bounded_reconciliation_horizon.py`

source commit:

`2eba4dbc21f31cd16cc46a54f7e731259b4a1f43`

source blob:

`0a604b98931b08e42a87fa9528fd6f9739c4c6f4`.

The prototype implements an R25-style shared `reconciliation_horizon_floor`, bounded exact proof retention, bounded pending receipts, explicit unresolved causal-gap state, checkpoint/restore of horizon/pending/gate state and an explicit authoritative resynchronization operation. Outcomes below the exact retention floor are classified `OUTSIDE_RETENTION_HORIZON` and do not mutate WORLD state. Horizon advancement is blocked by still-eligible pending lineage unless that item is explicitly expired into unresolved state.

The implementation composes the existing validated upstream receipt validator and repaired reconciliation admission gate rather than replacing either one.

## Validation status

Focused acceptance test publication did not complete.

The same-purpose code publication used the five-total-attempt ceiling:
1. source create: pre-GitHub platform safety refusal;
2. source create after fresh branch/file readback: SUCCESS;
3. focused-test create: pre-GitHub platform safety refusal;
4. focused-test create after fresh readback: pre-GitHub platform safety refusal;
5. focused-test create after fresh readback: pre-GitHub platform safety refusal.

Final readback found:
- source present at blob `0a604b98931b08e42a87fa9528fd6f9739c4c6f4`;
- focused test `tests/test_forge_fly0_bounded_reconciliation_horizon.py` absent;
- branch source state one commit ahead of validated base;
- source commit combined-status contexts observed: 0;
- PR-triggered workflow runs observed for source commit: 0.

Therefore this run does not claim focused acceptance or CI-green status for the new horizon component. The source is `FORGE_PROTOTYPE / UNVERIFIED`; it is not a new SYSTEM_BUILD handoff.

## Intended acceptance boundary

The blocked focused acceptance was designed to cover:
- validator -> consumer gate -> horizon composition on structured / degree-preserving rewired / random sparse / reactive variants;
- in-window exact replay protection;
- pending lineage blocking horizon advancement;
- explicit pending expiry into `DEGRADED_CAUSAL_GAP`;
- late out-of-horizon outcome refusing WORLD mutation rather than becoming zero/no-event;
- checkpoint/restore of exact identity, pending state, horizon and causal-gap state;
- explicit resynchronization as the only operation that clears degraded causal certainty;
- long-running exact identity state bounded by configured window rather than total history.

These remain unverified until focused tests land and exact-head CI is observed.

## Ordinary reduction and limitations

The design reduces to ordinary bounded event logs, execution journals, idempotent consumers, monotonic watermarks and checkpoint/replay. It is not a new cognitive or biological mechanism.

The guarantee is intentionally bounded. Exact replay identity is retained only within the configured horizon. An old causal item outside that horizon is treated as unresolved, not as a known duplicate. The prototype is not Byzantine/security-grade and does not establish end-to-end global exactly-once semantics.

## Disposition

`FORGE_PROTOTYPE / UNVERIFIED / NON_EVIDENTIARY / NONCANONICAL`

recommended_handoff: `NONE_THIS_RUN`

scientific_credit: `0`

No biological fidelity/equivalence, topology necessity/superiority, compute/energy efficiency, composition contribution, whole-system superiority, external validity or scientific novelty is established.

No M1-002 mutation, SB003 activation, SYSTEM_BUILD allocation, canonical science change, consumed FORMAL action, immutable evidence mutation or scheduler-state change occurred.

P0 remains OPEN / root cause UNKNOWN. This run again shows nonuniform mutation behavior: branch creation and source creation eventually succeeded, while three consecutive focused-test create attempts were refused before GitHub after fresh readback.

`reports/fast_forge/latest.md` and `state.json` are intentionally not advanced to this unverified generation. This append-only history entry is the durable record for the run.
