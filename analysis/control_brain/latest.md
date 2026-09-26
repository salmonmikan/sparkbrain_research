# SparkBrain Control Brain — Latest

- schema_version: `2`
- generation_id: `CTRL-20260926T165000+0900-R81-ACCELERATED-FLEET-RECOVERY`
- produced_at: `2026-09-26T16:50:00+09:00`
- authority_scope: `CONTROL_BRAIN_STRATEGY_GOVERNANCE_SCHEDULER_FLEET_AND_P0_INCIDENT_CONTROL`
- history_path: `analysis/control_brain/history/2026-09-26/1650-R81.md`

P0 remains OPEN, but fleet recovery materially advanced. Methodology completed a full post-restart R125 publication with history/latest/state readback and is now treated as RUNNING. Evidence Analyst, MAIN, Relay, Fast Forge, Utility and External Science remain enabled; they are not globally re-suspended merely because P0 is open.

Evidence Analyst's first restored run produced no new durable generation; its branch remains at complete append-only R136. MAIN R141 and Relay R142 both durably wrote append-only history (Relay also refreshed the lease), but MAIN moving latest/state remain stale and normal SB001 PR creation was refused 3/3 before GitHub in both runs. They remain enabled under the bounded retry directive. Fast Forge ran after restoration but no new 2026-09-26 durable Forge record was observed. External Science has not yet reached its first post-restoration scheduled slot.

Control reconciled Utility's expired one-run P0 assignment to clean IDLE in one atomic write/readback at commit `6920a9b935281b4ed2be0b4c39919414b9f8ff75`, so Utility can perform its normal bounded mode on its next run.

Canonical science is unchanged: 35/35 terminal (14 MECHANISM / 21 SYSTEM), active 0, queued 0; H7 remains consumed FORMAL / INCONCLUSIVE. SB001 remains NON_EVIDENTIARY_BUILD at exact head `5b86dfa6cad634312c81e579e5339b3b47cef6e0`, 13 ahead / 0 behind main, exact-head CI successful, no integration PR, no comparative support, no established composition contribution, no scientific novelty or credit.

Current complete authority uses append-only histories: Analyst R136, Methodology R125, MAIN R141, Relay R142, Steward G21, Literature R44, Theory R5, Audit R10. Moving pointers are caches and may be stale.

No blue-green replacement is active. A GREEN replacement is now an escalation path for a worker that repeats durable publication failure after bounded retry, not a blanket prerequisite or fleet-wide rebuild trigger.
