# Theory R29 — issue-to-WORLD-commit lineage join

generation_id: `THEORY-20260930T193342+0900-R29-WORLD-COMMIT-LINEAGE-JOIN`  
status: `INTEGRATION_DESIGN_PROPOSAL`  
new_sparkbrain_scientific_result: `false`

R29 binds one identity across `issue-time lineage -> WORLD commit -> execution journal -> observed receipt -> causal frontier`. It proposes a bounded `WorldCommitLineageRecord` created only after successful WORLD commit, with exact issue/session/cut/recovery/action/sequence/digest binding, so separately valid issue and commit records cannot be cross-wired into a false causal history.

The design is ordinary WAL/idempotency/outbox/fencing engineering. Prefer a local SQLite/WAL single-writer replacement if it satisfies the same adversarial tests more simply. Efference copy / predicted reafference remains a separate fly-inspired predictive channel, not transaction authority.

This is NON_EVIDENTIARY / NONCANONICAL engineering with scientific credit 0. Optional SB003 B/C hardening only after fresh Evidence Analyst reconciliation; no M1 stop, no SB003 activation change, no mandatory review gate.

History: `analysis/external_research_audit/theory/history/2026-09-30/1930-THEORY_SYNTHESIS_ARCHITECT.md`
