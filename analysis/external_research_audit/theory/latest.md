# Theory R31 — durable reconciliation inbox and cold-restart authority

generation_id: `THEORY-20261001T153237+0900-R31-DURABLE-RECONCILIATION-INBOX`
status: `INTEGRATION_DESIGN_PROPOSAL`
new_sparkbrain_scientific_result: `false`

R31 extends R30 across the remaining process-loss seam. Persist reconstructible issued-source and execution provenance, keep R30 WORLD/effect atomicity, then atomically commit receipt-dedup + durable scalar frontier. After a true cold restart, rebuild the in-memory R27/gate projection only from durable rows; missing or inconsistent provenance stays unresolved/fail-closed.

Prefer one local SQLite/WAL authority and compare it against checkpoint/event-history replay. This is NON_EVIDENTIARY / NONCANONICAL, scientific credit 0. No M1 stop, no SB003 activation change, no mandatory review gate.

History: `analysis/external_research_audit/theory/history/2026-10-01/1532-THEORY_SYNTHESIS_ARCHITECT.md`
