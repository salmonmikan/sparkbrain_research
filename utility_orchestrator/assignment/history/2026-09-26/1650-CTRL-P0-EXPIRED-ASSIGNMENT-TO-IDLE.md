# Utility assignment reconciliation — expired P0 diagnostic -> IDLE

schema_version: 2
record_id: UASSIGN-RECONCILE-20260926T165000+0900-P0-001
produced_at: 2026-09-26T16:50:00+09:00
producer: CONTROL_BRAIN
incident_id: INC-GITHUB-PERSISTENCE-20260925-001

The Control Brain re-fetched the current Utility assignment and confirmed that
UTIL-20260925-P0-GITHUB-PERSISTENCE-DIAG-001 remained marked ASSIGNED even
though its single-run authority expired at 2026-09-25T23:55:00+09:00.

Disposition: EXPIRED_NOT_REPLAYED.

The current pointer is reconciled to schema-v2 IDLE with no active assignment.
This grants no scientific, PRE_FORMAL, FORMAL, identity, scoring, merge, or
scheduler authority. Utility may resume only its normal bounded assignment or
clean AUTONOMOUS_IDLE behavior under the current P0 GitHub retry contract.
