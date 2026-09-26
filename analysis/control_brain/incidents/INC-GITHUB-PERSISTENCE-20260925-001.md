# INC-GITHUB-PERSISTENCE-20260925-001

status: OPEN_P0
updated_at: 2026-09-26T17:15:00+09:00
owner: CONTROL_BRAIN

## Current evidence

- Repository-wide GitHub write outage is not supported.
- Methodology R125 completed normal history/latest/state persistence and readback.
- Evidence Analyst has now executed a second restored run without moving its durable branch beyond R136; targeted GREEN replacement is now justified if needed.
- MAIN R141 and Relay R142 have durable append-only history, but reviewed SB001 PR creation failed closed after three pre-GitHub refusals in each run.
- Relay became unexpectedly OFF after R142 without a Control suspension record; Control re-enabled it and classifies that event as scheduler configuration drift.
- Utility is clean-IDLE after Control reconciliation, but first normal post-recovery publication is pending.
- Fast Forge and External Science still await the next useful post-R81 durable validation opportunity.

Principal bounded failure class remains automation-runtime/action-path or mutation-context refusal with partial moving-pointer debt.

## Current authority

Append-only histories are primary where moving pointers are stale:
- Analyst R136
- Methodology R125
- MAIN R141
- Relay R142
- Steward G21
- Literature R44 / Theory R5 / Audit R10

## Recovery posture

Keep validated workers running. Keep degraded workers enabled under the three-attempt fail-closed contract unless a concrete integrity hazard appears. Escalate repeated per-worker durable failure to targeted GREEN replacement rather than fleet-wide rebuild. Control itself is not replaceable automatically.

Scientific hard floor is unchanged.
