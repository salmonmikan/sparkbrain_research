# Theory R31 — durable reconciliation inbox and cold-restart authority

schema_version: 2
generation_id: `THEORY-20261001T153237+0900-R31-DURABLE-RECONCILIATION-INBOX`
produced_at: `2026-10-01T15:32:37+09:00`
producer_run_id: `EXTERNAL_SCIENCE_TRIROLE-20261001T153237+0900`
authority_scope: `NON_EVIDENTIARY_NONCANONICAL_THEORY_SYNTHESIS_ZERO_EXECUTION_AUTHORITY`
supersedes_generation_id: `THEORY-20261001T073425+0900-R30-LOCAL-ATOMIC-WORLD-EFFECT-JOURNAL`
status: `INTEGRATION_DESIGN_PROPOSAL`
design_id: `ID-SB-FLY-DURABLE-RECONCILIATION-INBOX-001`
genuinely_new_information: true
new_sparkbrain_scientific_result: false
scientific_credit: 0

## Target capability

Close the remaining local cold-restart seam after R30 and the current effect/receipt/frontier Forge gate: after all process memory is lost, rebuild exact issue/execution/effect provenance from durable state, accept a matching receipt at most once, and recover the same monotonic causal frontier without inventing fresh lineage.

This is an engineering integration proposal only. It is not scientific evidence.

## Current observations

- Current Control R148 records the effect/receipt/frontier Forge path as engineering-green at test-bearing head `74536fb9e3063c48d68080e392121175037e3215` / focused CI `36812964770`, while the requested direct tamper test publication remains blocked 5/5. No SYSTEM_BUILD handoff exists.
- Current exact branch head `edf5f7629c2049f412777d597713ff3f9b9ac616` contains `EffectReceiptFrontierGate` and its focused tests. The gate requires an exact retained R30 WORLD effect before frontier advance and rejects missing/cross-wired effects.
- `IssueTimeProvenanceBinding.checkpoint()` durably serializes issue stamps and full `SourceFrameRecord`, but not `IssueBoundExecution` / `ExecutionJournalEntry`.
- `LocalAtomicWorldEffectJournal` durably stores the WORLD state and an effect identity derived from the execution, but the effect row does not contain every field required to reconstruct the exact `ExecutionJournalEntry` used by `UpstreamReceiptValidator`.
- `EffectReceiptFrontierGate.checkpoint()` stores accepted binding identities and a digest of the current frontier checkpoint; it still assumes the corresponding provenance/frontier objects are separately restored.
- Literature R55 reduces this seam to established checkpoint/event-history replay + transactional inbox/idempotent consumer + scalar watermark primitives.

Therefore the next useful integration object is not another certificate layer. It is one durable reconciliation authority for reconstructible provenance and receipt admission.

## Component map and provenance

1. **Issued-source row** — direct SparkBrain R28 data, but stored in ordinary SQLite/WAL. Persist full `IssueTimeStamp` plus full `SourceFrameRecord`, keyed by world session/cut/epoch/issue identity.
2. **Execution row** — existing `ExecutionJournalEntry` serialized completely, keyed to the exact issued-source token and transaction id.
3. **WORLD effect row** — reuse R30's atomic `world_state + world_effects` transaction and exact effect token.
4. **Receipt inbox row** — established idempotent-consumer pattern. Persist stable receipt/signal/effect identity with a unique key.
5. **Frontier state row** — materialized scalar watermark/session/cut/epoch/horizon state. Update it in the same transaction that inserts the accepted receipt-inbox row.
6. **In-memory R27 frontier and gate bindings** — treat as rebuildable projections/caches, not the sole durable authority.

Known reductions: SQLite/WAL ACID, transactional inbox/outbox, idempotency key, consistent checkpoint/event-history replay, generation fencing and scalar watermark. No novelty credit attaches to any of these.

## Interfaces and state loop

`issue source`
→ persist reconstructible issued-source record
→ local execution
→ persist exact execution journal
→ R30 transaction commits WORLD mutation + exact effect row
→ process may die and lose all Python objects
→ restart opens durable reconciliation store
→ reconstruct `IssuedSourceFrame`, `IssueBoundExecution`, `WorldEffectIntent`/effect identity from durable rows only
→ validate later `TypedAscendingSignal`
→ transactionally insert receipt-dedup row + advance durable frontier row
→ rebuild/update in-memory R27 frontier projection
→ next observation/action.

If a required durable row is absent, expired or inconsistent, return unresolved/fail-closed. Never synthesize a current issue or execution from effect hashes alone.

## Why each component is used

- Full issued-source and execution rows make cold restart reconstructible rather than merely token-verifiable.
- R30 keeps WORLD mutation and effect identity crash-atomic.
- Receipt inbox prevents duplicate receipt replay from double-advancing causal time.
- Frontier row makes progress durable independently of Python object lifetime.
- R27 remains useful as a validation/projection layer but no longer needs to be trusted as the only persistence surface.

## Known limitations

- Local ACID state proves only the local authoritative synthetic WORLD bookkeeping, not a remote API or physical actuator.
- The proposal does not solve external side-effect exactly-once. Remote/physical actions still require `INTENT → DISPATCHED → ACKNOWLEDGED | UNCERTAIN | COMPENSATED` handling and idempotency where available.
- Bounded retention means an evicted provenance/effect/receipt identity becomes outside-horizon/unresolved, never silently current.
- If independent databases/files are used instead of one transaction authority, cross-store checkpoint skew returns; the baseline should therefore start with one SQLite database unless a concrete requirement forces separation.
- WORLD time is currently total/monotonic; use a scalar watermark. Do not introduce antichain/vector progress without real incomparable time dimensions.

## Acceptance tests

1. **True two-process cold restart:** Phase A persists issue + execution + WORLD effect and exits. Phase B receives no Python objects from A, reconstructs only from durable rows, validates a matching receipt and advances exactly once.
2. **Missing provenance:** preserve a valid effect row but remove/omit the issued-source or execution row; receipt must remain unresolved/fail-closed and frontier must not advance.
3. **Cross-wire:** issue A + execution/effect B, or receipt A + effect B, must be rejected.
4. **Tamper:** mutate any reconstructible source/execution payload while retaining old tokens; restore/admission must reject.
5. **Crash before receipt transaction commit:** neither inbox marker nor frontier advance survives.
6. **Crash after receipt transaction commit but before in-memory frontier refresh:** both inbox marker and durable frontier survive; restart reconstructs the same frontier and exact replay is a no-op.
7. **Duplicate/concurrent receipt:** unique receipt/effect identity admits at most one frontier transition.
8. **Retention boundary:** evicted exact provenance/effect becomes outside-horizon/unresolved, never reissued as current.
9. **Epoch/cut/session fencing:** stale/future lineage cannot cross restart.
10. **Topology invariance:** structured, degree-preserving rewired and random-sparse variants use the same persistence/admission contract.

## Suggested component-replacement tests

Run the same adversarial suite against:
- minimal SQLite provenance + inbox + scalar frontier;
- explicit append-only event history + deterministic replay;
- complete checkpoint/replay snapshot.

Prefer the simplest implementation that satisfies the same acceptance contract. A bespoke SparkBrain certificate/recovery subsystem should survive only if it demonstrates a concrete capability missing from these established baselines.

## Suggested interaction-ablation tests

- Remove the durable execution row while keeping R30 effect persistence: cold restart should fail closed, showing the execution record is functionally necessary for reconstruction.
- Keep execution/effect durability but remove atomic receipt-inbox + frontier update: injected crash should expose duplicate or skew risk.
- Replace R27 in-memory frontier with direct durable scalar frontier admission while retaining identical provenance checks: if behavior is equivalent, keep R27 as a thin projection rather than a separate durable mechanism.

These are engineering interaction tests only, not scientific composition evidence.

## Alternative established architecture

A workflow/event-history engine model is the alternative: append deterministic issue/execution/effect/receipt events, replay them after restart, and use an idempotent transactional sink for receipt/frontier state. For the current bounded local prototype, SQLite/WAL is likely simpler and preserves offline/local execution.

## Scientific claims explicitly not made

No biological fidelity/equivalence; no fly-topology necessity or superiority; no cognitive novelty; no scientific novelty; no composition contribution; no whole-system superiority; no emergence; no external validity; no compute/energy-efficiency claim; no end-to-end exactly-once physical actuation claim.

## Build value if no novelty exists

This design can make the sensorimotor integration path restart-safe, replayable and inspectable while reducing bespoke persistence logic. That has SYSTEM_BUILD value even if every mechanism is fully established prior art.

## Suggested SYSTEM_BUILD scope

Keep this bounded to Forge first: one SQLite reconciliation store, a two-process cold-restart acceptance test, missing/cross-wire/tamper cases, and atomic inbox/frontier crash tests. Evidence Analyst decides whether any result is admitted to SYSTEM_BUILD. Do not block M1 or activate SB003 solely for this proposal.

## Independence from current MAIN unknown outcomes

The proposal depends only on current known interface invariants and current Forge code shape. It does not depend on M1 PR #164's eventual merge outcome and does not reinterpret any scientific result.

## Current authority reconciliation

- Canonical science remains 35/35 terminal, active 0, queued 0, 8 consumed FORMAL identities, scientific credit 0.
- M1 remains on its own critical path: Control R148 reports conflict resolution and exact-head CI green, awaiting fresh Analyst exact-head reconciliation. This proposal creates no additional review gate.
- SB003 remains `ALLOCATED_CONDITIONAL_INACTIVE`.
- Audit durable authority remains R15. R15's immediate issue→WORLD-commit seam is substantially addressed by R30 plus the current effect gate, but no new Audit classification is claimed here.
- Literature append-only/latest is R55 while literature state remains R54; this pointer debt is outside Theory ownership and is not modified.
- P0 `INC-GITHUB-MUTATION-RECURRENCE-20260928-001` remains OPEN / root cause UNKNOWN.

## Freshness and refs inspected

- main: `18ff183983a2657d7199a708e4d3398550d7740c`
- Human Directive index head/blob: `8ce979b9ec0bc7eede5225c0403698f8886d3e8d` / `1ba1e173344f36e14d0e21e6f3e823254e031f7d`; delta from Theory R30: false
- Control: R148 / `c4eadd7c199d2430a635edc71a1ae430d5465ece`
- Evidence Analyst: R177 / `6eabb82d512db004d2bc411bd494f2bbea584ea4`
- external-science branch before publication: `649c8ee99446343d564882b29f573db2925f8b1a`
- effect/receipt/frontier branch current head: `edf5f7629c2049f412777d597713ff3f9b9ac616`
- effect/receipt/frontier test-bearing head: `74536fb9e3063c48d68080e392121175037e3215`
- R30 exact head: `36c2a321767dd6c18606eaeea51d3e818c446a20`

Applicable Human Directives read/retained: HUMAN-20260925-002, HUMAN-20260926-003, HUMAN-20260926-004, HUMAN-20260927-002, HUMAN-20260928-001, HUMAN-20260928-002. No directive-index delta was observed.

No experiments, result-bearing workflow dispatch, scientific identity consumption, immutable-ref movement, scheduler mutation, or Work-mode execution occurred.
