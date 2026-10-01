# External Literature Reduction Scout R55

generation_id: LIT-20261001T123446+0900-R55-COLD-RESTART-FRONTIER-INBOX-PRIORART
produced_at: 2026-10-01T12:34:46+09:00
role: LITERATURE_REDUCTION_SCOUT
status: NON_EVIDENTIARY / NONCANONICAL
genuinely_new_information: true
new_sparkbrain_scientific_result: false
scientific_credit: 0

Freshness: active Human Directive index blob 1ba1e173344f36e14d0e21e6f3e823254e031f7d matches Literature R54; current Control R146 records directive-index head 8ce979b9ec0bc7eede5225c0403698f8886d3e8d, so directive delta is false. Inputs: Control R146, Evidence Analyst R176, Theory R30, Audit R15, prior Literature R54.

## Findings

1. Naiad / Timely Dataflow progress frontiers — DESIGN_PRIMITIVE / SYSTEM_LEVEL_COMPARATOR / NOVELTY_REDUCTION.
   Function: logical timestamps plus a progress frontier; with partial orders the frontier is an antichain rather than a single scalar. Comparator for R27-style “nothing earlier can still arrive” semantics.
   Limitations: progress tracking is not semantic provenance validation; if WORLD order is total, a scalar watermark is simpler.
   Must not imply: causal-frontier novelty, biological causality, or fly-topology advantage.
   Sources: https://www.microsoft.com/en-us/research/publication/naiad-a-timely-dataflow-system-2/ ; https://docs.rs/timely/latest/timely/progress/index.html

2. Apache Flink consistent checkpoints — DESIGN_PRIMITIVE / SYSTEM_LEVEL_COMPARATOR / NOVELTY_REDUCTION.
   Function: checkpoint replayable source positions together with state, restore both after failure, and replay from the checkpoint.
   Limitations: replayable source and durable state are required; end-to-end exactly-once further needs transactional or idempotent sinks.
   Must not imply: checkpoint success proves remote actuation or scientific novelty.
   Sources: https://nightlies.apache.org/flink/flink-docs-master/docs/learn-flink/fault_tolerance/ ; https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/connectors/datastream/guarantees/

3. Temporal-style durable event-history replay — DESIGN_PRIMITIVE / SYSTEM_LEVEL_COMPARATOR / NOVELTY_REDUCTION.
   Function: reconstruct in-memory workflow state after process loss by deterministic replay of durable event history; prior completed operations resolve from history instead of executing again.
   Limitations: workflow replay must remain deterministic; external operations are outside replay and retries still require idempotency/effect identity.
   Must not imply: novel cognition/memory/biological recurrence or exactly-once external-world execution.
   Sources: https://docs.temporal.io/tasks ; https://docs.temporal.io/workflow-definition

4. Transactional idempotent-consumer / inbox — DESIGN_PRIMITIVE / NOVELTY_REDUCTION.
   Function: commit a stable receipt/dedup key and consumer state update in the same transaction, with a unique constraint resolving duplicate races. This maps to “receipt accepted + frontier advanced” as one idempotent commit.
   Limitations: only protects state in that transaction; external/physical effects still need explicit uncertainty/acknowledgement/compensation handling.
   Must not imply: a local inbox marker proves external WORLD truth or end-to-end exactly-once actuation.
   Source: https://learn.microsoft.com/ja-jp/azure/architecture/patterns/idempotent-consumer

## SparkBrain consequence

R54 reduced local WORLD commit durability to established ACID/WAL/outbox machinery. R55 reduces the next seam: cold restart, receipt replay and causal-progress admission also have established counterparts.

Baseline for R30 -> receipt/frontier:
1. persist reconstructible issue/execution/effect history or a complete checkpoint plus replay position;
2. after process loss rebuild runtime provenance only from durable state/history, never surviving in-memory objects;
3. validate exact issue/effect/receipt identity;
4. atomically commit receipt-dedup marker and frontier advance;
5. keep a scalar frontier when WORLD time is total; use an antichain only if incomparable progress dimensions are real.

A bespoke cold-restart certificate/frontier structure therefore carries zero novelty by default and should survive only if focused replacement tests show capability not supplied by event-history/checkpoint + inbox + scalar-watermark baselines.

No Revisit trigger. No M1 stop. No SB003 activation change. No mandatory review gate. P0 remains OPEN / root cause UNKNOWN. Literature R54 was already reconciled before this run.
