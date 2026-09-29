# Theory R25 — bounded reconciliation horizon and unresolved-gap state

generation_id: `THEORY-20260930T013204+0900-R25-BOUNDED-RECONCILIATION-HORIZON`
produced_at: `2026-09-30T01:32:04+09:00`
producer_run_id: `EXTERNAL_SCIENCE_TRIROLE-20260930T013204+0900`
status: `INTEGRATION_DESIGN_PROPOSAL`
new_sparkbrain_scientific_result: `false`
scientific_credit: `0`

## Design identity

- design_id: `ID-SB-FLY-HIERARCHICAL-SENSORIMOTOR-LOOP-001`
- revision: `10`
- proposal: `BOUNDED_RECONCILIATION_HORIZON_AND_UNRESOLVED_GAPS`
- target capability: bound long-running receipt/proof/journal memory without silently converting late or no-longer-provable WORLD outcomes into zero, duplicates, or fresh state transitions.

## Authority and freshness

Human Directive index is unchanged at branch head `8ce979b9ec0bc7eede5225c0403698f8886d3e8d`, active-index blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`. No newly active/materially changed directive was found.

Fresh authority used:
- Control append-only authority R129; P0 remains OPEN / root cause UNKNOWN.
- Evidence Analyst R172; M1-002 remains critical path, SB003 remains `ALLOCATED_CONDITIONAL_INACTIVE`.
- Analyst R172 keeps the full receipt path at `HOLD_FOR_UPSTREAM_VALIDATOR_AND_SCOPED_ENGINEERING_ACCEPTANCE` and prospectively permits Forge work in order: `UPSTREAM_VALIDATOR_FOCUSED_ACCEPTANCE`, then `BOUNDED_RETENTION_RECOVERY`.
- Theory predecessor R24.
- Literature append-only R51 (latest/state cache still R50): retention horizon is part of the guarantee, cyclic recovery needs in-flight state, and exactly-once language must be scoped.
- Audit R13 plus Analyst R171 repair: downstream consumer proof-identity replay defects were repaired/admitted only as optional NON_EVIDENTIARY SB003 B/C input.
- Upstream validator source blob `6aa21e9a9b1c336c87defc224690bc1a21f33fc9`; Analyst R172 records source head `af238d1bd6fcb4d5433a5caaa96a246e880b1121` / CI 36592416544 green but no focused acceptance test, therefore NO_HANDOFF.

## Component map and provenance

1. **Upstream execution journal + receipt validator** — R24 design; Forge source exists but focused acceptance is missing. It binds source frame, authority provenance, commit/rollback journal, typed WORLD outcome and outcome sequence. NON_EVIDENTIARY/NONCANONICAL.
2. **Downstream canonical proof-identity gate** — repaired Forge head `dde6270db4238ca78d1678a8826b8a463cd2d8dc`, Analyst R171 optional SB003 B/C input. It rejects cross-transaction signal replay/conflicting sequence and preserves checkpointed dedupe state. NON_EVIDENTIARY.
3. **Generic bounded receipt retention reference substitute** — `forge/20260927-bounded-receipt-retention-a@8937342eea5f05777bdccd13aaa7e6f0c13fd609`. It uses exact in-window receipts plus compacted-prefix digest and a conservative fixed-size identity filter. Useful prior internal engineering, but not FLY-0-specific and no exact-head workflow verification was observed in this run.
4. **R25 shared reconciliation horizon** — proposed coordination layer between validator and consumer. This is ordinary bounded-log/event-sourcing engineering, not a new cognitive mechanism.

## Known reductions

This design reduces to established bounded logs, event correlation, execution journals, idempotent consumers, monotonic sequence watermarks, checkpoint/replay, and explicit expiry. Literature R51 further reduces the idea through durable subscription retention, causal logging/deduplication and cyclic dataflow snapshot principles. No novelty credit is requested.

## Interfaces and state loop

Use one monotonic `reconciliation_horizon_floor` shared by validator and consumer rather than independently expiring their state.

For each candidate receipt/proof:

`source frame -> execution journal -> typed ascending outcome -> upstream validator -> canonical proof -> reconciliation gate -> observer/WORLD state`

The horizon adds:

- `reconciliation_horizon_floor`: smallest outcome sequence still eligible for exact causal validation/reconciliation.
- `exact_identity_registry`: canonical proof/signal identities for sequences at or above the floor.
- `pending_receipts`: delayed/in-flight items still inside the eligible window.
- `expired_unresolved`: explicit records/counters for items whose causal lineage aged out before resolution.
- `outcome_watermark`: highest safely applied monotonic outcome sequence.
- optional `sealed_prefix_digest`: audit/checkpoint integrity only, never a membership proof.
- `observer_certainty`: at minimum `EXACT_WITHIN_HORIZON` or `DEGRADED_CAUSAL_GAP`.

Invariant: validator lineage needed to certify an in-window proof must not be compacted before that proof is reconciled or explicitly expired. Consumer dedupe/proof identity state must not be forgotten while the validator could still issue an admissible proof for that identity.

If a receipt/proof arrives with `outcome_sequence < reconciliation_horizon_floor`, classify it `OUTSIDE_RETENTION_HORIZON` / unresolved and do not mutate WORLD state. Do not call it a duplicate unless exact retained identity proves that fact.

When an unresolved item expires, the system may continue ordinary local control, but the high-level observer must retain a causal-gap marker until an explicit resynchronization policy clears it. Expiry is a loss of historical certainty, not evidence that nothing happened.

## Why each component is used

- Validator journal: prevents self-attested signal payloads from becoming WORLD truth.
- Canonical proof identity: prevents cross-transaction replay and conflicting sequence reuse.
- Shared horizon: allows both layers to reclaim memory without creating a window in which one layer forgets evidence that the other still treats as admissible.
- Explicit unresolved/expired state: prevents bounded memory from silently becoming fabricated certainty.
- Checkpointed horizon/pending state: makes crash/replay semantics deterministic for the cyclic sensorimotor loop.
- Optional prefix digest: detects checkpoint/history divergence without pretending to answer old membership queries.

## Known limitations

- This is not Byzantine/security-grade proof. Python dataclasses/tokens are provenance contracts, not cryptographic trust boundaries.
- A configured horizon trades late-arrival liveness for bounded memory; arrivals beyond it are intentionally unresolved.
- If the system cannot obtain a later authoritative WORLD resynchronization, `DEGRADED_CAUSAL_GAP` may persist.
- Sequence/horizon policy must be prospective engineering configuration, not tuned against scientific outcomes.
- The generic 2,048-bit compacted identity filter is not preferred as the primary FLY-0 guarantee because false positives grow over long histories. It remains a replacement comparator, not an authority mechanism.
- No claim is made that this mirrors fly neurobiology.

## Acceptance tests

1. In-window exact proof replay is a duplicate no-op; same canonical identity with conflicting content fails closed.
2. Same signal rewrapped under a second transaction/sequence is rejected while within the exact window.
3. Proof with sequence below `reconciliation_horizon_floor` returns `OUTSIDE_RETENTION_HORIZON`, never WORLD mutation and never silent duplicate classification.
4. A committed outcome delayed past expiry creates/retains an explicit unresolved causal gap; it is not converted to zero/no-event.
5. Horizon advancement is blocked while a still-eligible pending item requires validator lineage, unless the item is explicitly transitioned to expired-unresolved.
6. Validator and consumer horizon/checkpoint state advance atomically enough that restore yields either the pre-advance or post-advance state, never a mixed half-compacted state.
7. Checkpoint/restore preserves horizon floor, outcome watermark, exact identity registry, pending items, expired-unresolved markers and observer-certainty state; replay is deterministic.
8. Out-of-order in-window outcomes cannot roll back observer state; expired old outcomes cannot advance the watermark.
9. Long-running bounded test demonstrates memory proportional to configured exact window + bounded pending state rather than total history.
10. After an unresolved expiry, only an explicitly defined resynchronization event may clear `DEGRADED_CAUSAL_GAP`; ordinary new receipts do not erase the gap silently.

## Component-replacement tests

- **Unbounded ledger** vs **shared bounded horizon** under identical delay/replay load: bounded variant must preserve safety classifications while bounding state.
- **Generic compacted Bloom-style identity filter** vs **shared-horizon exact-window design**: compare false-positive liveness loss and state size; do not assume the custom horizon is superior.
- **Independent validator/consumer expiry** vs **shared horizon**: deliberately stagger compaction and test for accepted unverifiable proofs or replay gaps.
- **SQLite/WAL local event log with unique canonical identity + partition/horizon compaction** as an established alternative architecture. If it is simpler/more robust under the same local-only constraints, prefer it.

## Interaction ablations

- Remove explicit expired-unresolved state: test whether late causal loss is silently misclassified as no-event.
- Remove checkpointed pending state: crash with delayed receipt in flight and verify whether replay diverges.
- Remove shared horizon coupling: compact validator before consumer and vice versa to expose cross-layer ambiguity.
- Remove observer-certainty degradation: verify whether downstream logic incorrectly presents exact state after a causal gap.

## Scientific claims explicitly not made

No biological fidelity/equivalence, fly topology necessity/superiority, energy/compute efficiency, composition contribution, whole-system superiority, external validity, emergence or scientific novelty is established. This proposal is not scientific evidence. Scientific credit = 0.

## Build value if no novelty exists

The value is operational: bounded long-running memory, deterministic recovery, explicit uncertainty rather than invented certainty, and a composable handoff between the validator and repaired consumer gate. These remain useful even if every mechanism is fully reduced to standard systems engineering.

## Suggested SYSTEM_BUILD scope

Do not change M1-002 critical path, SB003 activation conditions, or review policy. Keep R25 as optional SB003 Milestone B/C hardening.

Recommended order:
1. complete the already-approved upstream-validator focused acceptance;
2. Forge-probe the shared-horizon/expired-unresolved contract against the existing generic bounded-retention substitute;
3. if bounded acceptance is green, hand to Evidence Analyst for fresh scoped admission;
4. only then compose validator + repaired consumer + retention/recovery for long-running SB003 tests.

No scientific execution, no result-bearing workflow dispatch, no consumed identity action, no immutable ref movement.

## Independence from current MAIN unknown outcomes

The design depends only on current declared interfaces and NON_EVIDENTIARY engineering artifacts. It does not depend on whether M1-002 PR creation succeeds, whether SB003 later shows a performance benefit, or any unknown MAIN scientific outcome.

## Revisit scan

No Revisit trigger. This is integration hardening and prior-art reduction, not reopening a terminal scientific object.
