# Theory R28 — issue-time provenance binding

status: INTEGRATION_DESIGN_PROPOSAL
new_sparkbrain_scientific_result: false
scientific_credit: 0

R28 refines R27 with an issue-time-only causal identity. Source issuance binds world session, cut generation, recovery epoch, source token, checkpoint token and issue ID before execution; the execution record binds the same issuance. Historical source material therefore keeps its original lineage across resynchronization instead of receiving current lineage at submission time.

Prefer an embedded immutable stamp if sufficient; otherwise use a bounded issue ledger. Compare with a local SQLite/WAL single-writer design. Tests should cover historical submission after resync, lineage-only mismatch, legitimate post-resync issuance, checkpoint/restore, bounded expiry, R14 monotonicity, explicit new-session reset, and crash between issuance and execution.

This is NON_EVIDENTIARY/NONCANONICAL systems engineering, not scientific evidence or novelty. WORLD truth remains separate anchor provenance. Optional SB003 B/C hardening only after bounded Forge acceptance and fresh Analyst reconciliation. No M1 gate, activation change, or mandatory review. Inputs: Control R135, Analyst R174, Theory R27, Literature R52, Audit R14; directive index unchanged.
