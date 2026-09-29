# Theory R23 — typed ascending semantic reconciliation

generation_id: `THEORY-20260929T193236+0900-R23-TYPED-ASCENDING-SEMANTIC-RECONCILIATION`
status: INTEGRATION_DESIGN_PROPOSAL
new_sparkbrain_scientific_result: false

R23 extends R22 by separating ascending-message direction from semantic meaning. Predictive motor-copy, realized local behavioral state and reafferent WORLD outcome are distinct lanes; availability state (observed/gated/masked/delayed/missing) is orthogonal metadata.

Only transaction-valid committed REAFFERENT_WORLD_OUTCOME events may use R22 exact-once WORLD reconciliation. Predictive signals may update provisional expectation but must not be committed as realized facts. Gated/masked feedback must not be interpreted as a zero/no-change outcome.

This is ordinary typed telemetry + observer/event-sourcing engineering, not scientific evidence or novelty. Optional SB003 B/C hardening only; no M1 gate, no SB003 activation change, no mandatory review, scientific credit 0.

History: analysis/external_research_audit/theory/history/2026-09-29/1932-THEORY_SYNTHESIS_ARCHITECT.md
