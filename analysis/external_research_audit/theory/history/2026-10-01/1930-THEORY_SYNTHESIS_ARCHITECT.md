# Theory R32 — single-authority durable causal frontier

generation_id: `THEORY-20261001T192955+0900-R32-SINGLE-AUTHORITY-DURABLE-CAUSAL-FRONTIER`
produced_at: `2026-10-01T19:29:55+09:00`
producer_run_id: `EXTERNAL_SCIENCE_TRIROLE-20261001T192955+0900`
role: `THEORY_SYNTHESIS_ARCHITECT`
status: `INTEGRATION_DESIGN_PROPOSAL`
authority_scope: `NON_EVIDENTIARY_NONCANONICAL_THEORY_SYNTHESIS_ZERO_EXECUTION_AUTHORITY`
genuinely_new_information: `true`
new_sparkbrain_scientific_result: `false`
scientific_credit: `0`

## Design

design_id: `ID-SB-FLY-SINGLE-AUTHORITY-DURABLE-CAUSAL-FRONTIER-001`

R31's durable reconciliation inbox is now engineering-green on Forge exact tested head `1d2c5edc7db894827108ab3a3ae325dac2da41b4` / CI `36839614462`. It proves true subprocess cold restart, durable issue/execution reconstruction, R30 effect binding, atomic receipt-dedup + scalar-frontier update/rollback, exact replay, outcome-gap rejection, and fail-closed missing/tampered provenance.

The remaining composition seam is a split authority. R31 durably stores session/cut/epoch/position/outcome/accepted-receipt progress in SQLite/WAL, while R27 separately maintains a checkpointable frontier with `horizon_floor` and `observer_certainty`. R25 also keeps unresolved-gap/horizon state separately. R32 proposes one local durable causal-progress authority and makes R27 a rebuildable projection/validator rather than a second recoverable authority.

## Component map / provenance

- R30 local atomic WORLD/effect journal: local WORLD/effect authority.
- R31 durable provenance + inbox: durable issue/execution/effect/receipt authority.
- R25 bounded horizon: reuse explicit outside-horizon and unresolved-gap semantics.
- R27 frontier: reuse monotonic session/cut/epoch/outcome/horizon checks, not its checkpoint as authority.
- Established reductions: SQLite/WAL ACID, transactional/idempotent inbox, scalar watermark, materialized projection, checkpoint/event-history replay, generation fencing.

All reused components carry zero inherited scientific credit.

## Interfaces and state loop

`durable source/execution provenance → R30 WORLD/effect commit → receipt validation → one transaction updates inbox + single durable frontier row → rebuild R27-style projection → next issue/admission`.

The single frontier row should retain at least WORLD session, cut generation, recovery epoch, WORLD position, outcome watermark, accepted-receipt count/linkage, reconciliation horizon floor, and unresolved-gap count. Observer certainty should be derived from durable gap state rather than maintained as a second independent truth value.

Horizon expiry, receipt admission and cut/epoch transition must update this durable authority transactionally or fail closed. A legacy R27 checkpoint can be checked for consistency but must never overwrite or roll back the durable row.

## Why these components

R30 closes local WORLD/effect dual-write. R31 closes process-loss provenance and duplicate-receipt admission. R25 provides explicit uncertainty when exact history is compacted. R27 contributes useful monotonic fencing. Unifying their progress state removes the remaining crash-recovery split-brain surface without inventing a new scientific mechanism.

## Known limitations

Local ACID does not prove remote API or physical-world exactly-once execution. Scalar progress is appropriate only while WORLD progress is total-ordered. Retention compaction needs explicit migration/expiry semantics. True simultaneous duplicate races still need focused engineering coverage. This proposal does not activate SB003 or alter M1 authority.

## Acceptance tests

1. True subprocess restart rebuilds an R27-equivalent projection only from durable rows; no Phase-A objects or standalone R27 checkpoint.
2. Crash after receipt/frontier commit but before in-memory refresh recovers exactly the committed frontier with no duplicate advance.
3. Stale/tampered standalone R27 checkpoint cannot become co-authority or move durable state backward.
4. Horizon expiry durably advances horizon floor and unresolved-gap state; restart preserves degraded certainty; late outside-horizon receipt cannot become fresh exact success.
5. Rebase advances cut/epoch monotonically and old issue lineage stays retired across restart.
6. Duplicate receipt remains idempotent across independently opened processes; add a true concurrent race probe where practical.
7. Missing/corrupt durable horizon/gap state fails closed or requires explicit schema migration.
8. Structured, degree-preserving rewired and random-sparse variants share identical provenance/frontier semantics.

## Replacement / ablation

Compare existing R27 checkpoint + R31 inbox, unified SQLite authority + rebuildable R27 projection, and append-only event-history / consistent-checkpoint replay under the same crash/replay/tamper/horizon/rebase suite. Prefer the simplest passing architecture.

Engineering ablations: omit durable horizon/gap state; inject a divergent legacy R27 checkpoint; remove effect binding while keeping receipt/frontier durability. These are diagnostics only and do not establish composition contribution.

## Alternative established architecture

Deterministic event-history replay, or a Flink-style consistent checkpoint with replay position and state, can supply the same function and should win if simpler under the local/offline constraint.

## Scientific claims explicitly not made

This is not scientific evidence. It does not establish biological fidelity/equivalence, fly-topology necessity/superiority, cognitive or causal-mechanism novelty, composition contribution, whole-system superiority, emergence, external validity, or compute/energy efficiency.

## Build value and suggested scope

A single authority reduces state surfaces and crash-recovery ambiguity while making bounded-horizon uncertainty durable. First extend only the current bounded Forge comparator with durable horizon/gap fields, pure R27 projection rebuild, and the tests above. No direct SYSTEM_BUILD handoff until fresh Evidence Analyst reconciliation. Do not block M1. SB003 remains `ALLOCATED_CONDITIONAL_INACTIVE`.

## Independence / current authority

The design depends only on already durable non-evidentiary engineering artifacts and not on unknown MAIN outcomes. Control is R152; Evidence Analyst is R177 and the pending R178 request has no observed workflow run/check suite/receipt/target advance; Theory predecessor is R31; Literature latest is R55 with state R54; Audit is R15. Canonical science remains 35/35 terminal, active 0, queued 0, 8 consumed FORMAL identities, scientific credit 0. P0 `INC-GITHUB-MUTATION-RECURRENCE-20260928-001` remains OPEN / root cause UNKNOWN.

Refs inspected: main `18ff183983a2657d7199a708e4d3398550d7740c`; directive index `8ce979b9ec0bc7eede5225c0403698f8886d3e8d` / blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`; Control `8e888eb7300766b9b0d2fb9c848b5730c416dbce`; Analyst `6eabb82d512db004d2bc411bd494f2bbea584ea4`; external before `db88aa98a4e321ce46bc523cdbc485993dba818c`; Forge report `1ac3ccbf3d160112c03813a6eb81486b346dc7ae`; R30 `36c2a321767dd6c18606eaeea51d3e818c446a20`; R27 `8db5eb55e65cbd436e465cde8a879d90dad8cac2`.

No experiment/result-bearing workflow was executed. No scheduler, immutable evidence, or consumed FORMAL identity was changed.
