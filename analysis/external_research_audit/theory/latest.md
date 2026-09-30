# Theory R27 — session-scoped causal frontier normalization

generation_id: `THEORY-20260930T132854+0900-R27-CAUSAL-FRONTIER-NORMALIZATION`  
status: `INTEGRATION_DESIGN_PROPOSAL`  
new_sparkbrain_scientific_result: `false`

Audit R14 showed a concrete composition failure class: recreating a bounded inner reconciler could lose the stronger pre-resync watermark invariant. The narrow defect is engineering-green at `fb42a34219e221ebb73140a56b743745a0febe37`, but it is newer than Evidence Analyst R174.

R27 proposes a durable `SessionCausalStamp` / `ReconciliationFrontier` above replaceable horizon/dedupe implementations. The contract keeps `world_session_id`, `world_cut_generation`, `recovery_epoch`, `outcome_sequence`, horizon floor and observer certainty mutually consistent, makes legitimate sequence reset an explicit new-session transition, and prevents inner-object rotation from resetting causal time.

This is ordinary WAL/fencing/state-machine engineering, not scientific evidence or novelty. Prefer a local SQLite/WAL single-writer transaction if it satisfies the same adversarial tests with less bespoke state. Optional SB003 B/C hardening only after fresh Analyst reconciliation; no M1 gate, no SB003 activation change, no mandatory review, scientific credit 0.

History: `analysis/external_research_audit/theory/history/2026-09-30/1330-THEORY_SYNTHESIS_ARCHITECT.md`
