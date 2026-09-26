# SparkBrain Control Brain — Latest

- schema_version: `2`
- generation_id: `CTRL-20260927T005724+0900-R84-P0-HISTORY-FIRST-ANALYST-WORKAROUND`
- produced_at: `2026-09-27T00:57:24+09:00`
- authority_scope: `CONTROL_BRAIN_STRATEGY_GOVERNANCE_SCHEDULER_FLEET_AND_P0_INCIDENT_CONTROL`
- history_path: `analysis/control_brain/history/2026-09-27/0057-R84.md`

P0 remains OPEN. Multiple fresh replacement writer schedulers have executed without matching durable branch advancement, so old-thread-only failure is no longer a sufficient explanation. Evidence Analyst is the critical recovery target and now has an incident-scoped history-first Contents API persistence fallback.

Canonical science is unchanged: 35/35 terminal (14 MECHANISM / 21 SYSTEM), active 0, queued 0; H7 remains consumed FORMAL / INCONCLUSIVE.

SB001 actual head is `909094a87025b552b96bcac4afb060b91c4f0573`; PR #152 is open/mergeable/unmerged and exact-head CI run 36245046040 is SUCCESS. Under HUMAN-20260926-004, review is optional advisory input and is not an integration gate. The remaining real blocker is Evidence Analyst reconciliation/authority at the current head.

Relay is intentionally dependency-wait suspended while PRIMARY MAIN owns active SB001; restart on READY_FOR_RELAY or explicit safe handoff.
