# Theory R25 — bounded reconciliation horizon and unresolved-gap state

generation_id: `THEORY-20260930T013204+0900-R25-BOUNDED-RECONCILIATION-HORIZON`
status: INTEGRATION_DESIGN_PROPOSAL
new_sparkbrain_scientific_result: false

R25 extends R24 with a coordinated bounded-retention contract for long-running receipt reconciliation. Validator lineage and consumer proof/dedupe state share a monotonic `reconciliation_horizon_floor`; anything older than the floor is explicitly `OUTSIDE_RETENTION_HORIZON` / unresolved and can never mutate WORLD state. Expiry must not be silently interpreted as zero, no-event, or a known duplicate.

Pending/delayed items, exact in-window proof identities, outcome watermark, horizon floor and expired-unresolved causal gaps are checkpoint/replay state. If a causal item expires unresolved, observer certainty degrades until an explicit resynchronization policy clears it.

This is ordinary bounded-log/event-sourcing/checkpoint engineering, not scientific evidence or novelty. It is optional SB003 B/C hardening only after the already-approved upstream-validator focused acceptance; no M1 gate, no SB003 activation change, no mandatory review, scientific credit 0.

History: analysis/external_research_audit/theory/history/2026-09-30/0132-THEORY_SYNTHESIS_ARCHITECT.md
