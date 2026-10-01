# Theory R32 — single-authority durable causal frontier

generation_id: `THEORY-20261001T192955+0900-R32-SINGLE-AUTHORITY-DURABLE-CAUSAL-FRONTIER`
status: `INTEGRATION_DESIGN_PROPOSAL`
new_sparkbrain_scientific_result: `false`

R31's durable cold-restart inbox is now engineering-green. R32 removes the remaining dual-authority seam: make the SQLite/WAL reconciliation frontier the sole local causal-progress authority, persist bounded-horizon/gap state there, and rebuild the R27-style frontier only as a projection/validator. A stale standalone R27 checkpoint must never override the durable row.

Baseline: SQLite/WAL ACID + idempotent inbox + scalar watermark + materialized projection, compared against event-history/consistent-checkpoint replay. This is NON_EVIDENTIARY / NONCANONICAL, scientific credit 0. No M1 stop, no SB003 activation change, and no mandatory review gate.

History: `analysis/external_research_audit/theory/history/2026-10-01/1930-THEORY_SYNTHESIS_ARCHITECT.md`
