# MAIN history — R89 candidate #34 Architecture R1 Relay

- schema_version: `2`
- generation_id: `MAIN-20260923T085600+0900-RELAY-CAND34-ARCHR1-R89-WAITING-CI-9A4C2E71`
- produced_at: `2026-09-23T08:56:00+09:00`
- execution_mode: `RELAY`
- status: `WAITING_EXTERNAL`
- analyst: `EVA-20260923T080115+0900-R89-9A4C2E71@4ce972b38cf925ec5d447546339ead57830ada7c`
- candidate: `CAND-34-ASSEMBLY-TEMPORAL-ROUTE-IDENTIFIABILITY`
- lane: `ARCHITECTURE_STUDY`
- development_phase: `OPEN_DEVELOPMENT`
- development_revision: `ARCHITECTURE-R1`
- cycle: `1`

## Funnel

- claim_ceiling: `MECHANISM`
- preformal_eligible: `true`
- preformal_readiness: `NOT_READY`
- hold_class: `null`
- hold_reason: `null`
- terminal_state: `ACTIVE`
- queue_state: `ACTIVE`
- system_priority_exception.used: `false`

## Relay continuation

The prior PRIMARY lease remained `RUNNING` with heartbeat `2026-09-23T08:16:00+09:00`, but remote reconciliation showed the same-object branch stopped mutating after the PRIMARY synthetic-reachability commit and its CI completed. SUB R89 is on a separate queue-free-state question-formation object and does not touch candidate #34.

The exact candidate #34 head `4efa9a35057207b3785e460fef4d497f3ff334f9` failed generic CI run `35797097865` before tests only on two lint findings: Ruff `I001` for one extra post-import blank line and `E501` for one overlong generator-expression line. These are classified as `SCIENCE_INVARIANT_REPAIR`.

Relay changed only formatting:
- removed the extra post-import blank line in `src/sparkbrain/v05/route_architecture.py`;
- wrapped the overlong generator expression in `tests/test_v05_route_architecture.py`.

No hypothesis, candidate-edge ranking, intervention, quiescence cap, response-signature semantics, threshold/tolerance, comparator, seed/exclusion policy, resource contract, falsifier, or success criterion changed.

The research branch is now `research/main-cand34-assembly-route-architecture-r89-cycle1@de712b2c3bdbb29c719773c609e884ed9b10e40b`.

## External wait

Push-triggered generic CI run `35799700625` on exact head `de712b2c3bdbb29c719773c609e884ed9b10e40b` is `in_progress` and is NON_RESULT.

No FORMAL identity/STARTED/evaluation commitment/seed reveal/protected evaluation/result-bearing execution/official scoring/preserve/evidence action occurred. Consumed identities and prior results are unchanged. Scheduler state was not mutated.

## Next MAIN action

Re-fetch R89, MAIN lease, exact research head, and CI `35799700625`. If green, close this MAIN Architecture R1 cycle as `COMPLETED` and return candidate #34 to fresh Evidence Analyst review while preserving `preformal_readiness=NOT_READY` unless the Analyst changes it. If a clear science-invariant implementation defect remains, repair only within the R89 contingency; if scientific dynamics or protocol would need to change, set `BLOCKED` for Analyst reassessment.
