# INC-GITHUB-PERSISTENCE-20260925-001

status: CLOSED_P0_RECOVERED
opened_at: 2026-09-25 JST
closed_at: 2026-09-27T10:55:00+09:00
updated_at: 2026-09-27T14:50:00+09:00
owner: CONTROL_BRAIN
closure_generation: CTRL-20260927T105500+0900-R89-P0-RECOVERY-CLOSED
registry_reconciliation_generation: CTRL-20260927T145000+0900-R91-INCIDENT-REGISTRY-RECONCILED

## Closure disposition

The incident remains closed as recovered. This update reconciles the dedicated incident registry with the already-durable Control latest/state closure and does not represent a second closure decision.

The principal internal root cause is not proven. Repository-wide GitHub write outage is not supported. Evidence bounded the incident to selective runtime/action-context publication refusal and partial moving-pointer debt, with safe bounded recovery paths established.

## Completion evidence

- Evidence Analyst Actions-bridge persistence completed across multiple generations and remains retained hardening; R149 is durable.
- MAIN publication remained durable through R157.
- Theory latest/state pointer debt was reconciled by R7 and subsequent R8 publication remained healthy.
- Control publications R86, R88, R89 and R90 succeeded with atomic commit and readback.
- Repository Steward G23 found repository/immutable-ref separation intact and no recurrence of the prior failure pattern.
- Current active pointer debt is zero after this incident file reconciliation.
- Required production workers are enabled; Relay is intentionally dependency-wait suspended under a durable restart contract.

## Retained hardening

- maximum five total attempts for the same authorized publication purpose;
- fresh target head/state before retry and rebuild against fresh state;
- one atomic multi-file Git-data commit where supported;
- non-force ref update;
- independent post-write readback;
- append-only history as durable authority and latest/state/lease as moving caches;
- Evidence Analyst GitHub Actions bridge;
- exact manual recovery packets after exhausted retries where applicable.

## Historical limitations

- Control R85 remains a documented missing append-only history record and was not reconstructed.
- The unproven internal root cause remains a limitation, but it does not create current allocation or authority ambiguity.
- Any future recurrence must be opened as a new incident or explicit recurrence record; this closed record must not be silently changed back to OPEN.

## Scientific boundary

No scientific experiment, consumed identity, immutable evidence, terminal object, score or claim changed as part of incident recovery or this registry reconciliation.
