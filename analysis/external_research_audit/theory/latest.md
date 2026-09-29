# Theory R22 — dual-validity outcome receipt reconciliation

generation_id: THEORY-20260929T152609+0900-R22-DUAL-VALIDITY-OUTCOME-RECEIPT
status: INTEGRATION_DESIGN_PROPOSAL
new_sparkbrain_scientific_result: false

R22 separates causal/transaction validity from current control-authority currency. A committed realized outcome from authority A can still reconcile WORLD/observer state after authority B supersedes A, while A remains unable to regain or extend control authority.

The current Forge receipt source adds exact frame correlation but remains unverified and currently rejects superseded-authority receipts before this distinction is made. R22 is a design contract, not implementation approval.

Tests should cover commit-before-supersede, supersede-before-execution, exact source/transaction binding, duplicate/out-of-order idempotence, freshness/mask/delay, ascending cut, replay and the common four-way interface.

This is ordinary event-sourcing/observer/idempotent-consumer engineering, not scientific evidence or novelty. Optional SB003 B/C hardening only after R169 activation conditions; no M1 gate or SB003 activation change. Scientific credit 0.

History: analysis/external_research_audit/theory/history/2026-09-29/1526-THEORY_SYNTHESIS_ARCHITECT.md
