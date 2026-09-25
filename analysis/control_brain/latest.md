# SparkBrain Control Brain — Latest

- schema_version: `2`
- generation_id: `CTRL-20260925T205800+0900-R75-MANUAL-P0`
- produced_at: `2026-09-25T20:58:00+09:00`
- authority_scope: `CONTROL_BRAIN_STRATEGY_GOVERNANCE_AND_INCIDENT_CONTROL`
- invocation_kind: `MANUAL_IMMEDIATE_RESPONSE`
- history_path: `analysis/control_brain/history/2026-09-25/2058-R75-MANUAL-P0.md`

## P0 directive

HUMAN-20260925-002 is ACCEPTED and active immediately as the highest operational priority until its completion criteria are met. Control Brain owns incident `INC-GITHUB-PERSISTENCE-20260925-001`.

Scientific hard floors are unchanged. No cadence change, scheduler creation/deletion, or scientific-standard change is authorized by this application.

## Immediate fleet posture

- MAIN: enabled; owns accepted SB001 critical path.
- Utility: enabled as `RESTARTING_DIAGNOSTIC`; next run is a persistence/runtime canary. On material failure, return to FAULT_SUSPENDED rather than rapid restart.
- Relay: disabled under `DEPENDENCY_WAIT_SUSPEND`; restart only when MAIN provides a safe handoff, the mutation/publication path is sufficiently bounded, and first post-restart durable publication can be validated.
- Evidence Analyst / Methodology / Fast Forge / External Science / Current State Brief / Control: enabled for discovery, integrity audit, and independent incident evidence.
- No cadence changes were made.

## Persistence authority

A complete append-only generation history is the primary durable record. latest/state are moving pointers/caches and must not override a newer complete history generation.

Before mutation: refresh branch head/blob SHA. Prefer atomic multi-file persistence where available. Otherwise use bounded compare-and-swap retry, never force-push, never overwrite a newer concurrent generation, and record write telemetry where possible.

A single successful later write does not resolve the P0 incident.

## Science / build

Canonical science remains 35/35 terminal (14 MECHANISM / 21 SYSTEM), active 0, queued 0. Consumed FORMAL identities remain immutable.

BUILD-SB-001 remains an accepted bounded NON_EVIDENTIARY_BUILD at its accepted exact head. Built/functionally verified within bounded acceptance: yes. Comparative support: no. Composition contribution: not established. Scientific novelty/credit: none. Reviewed integration PR remains pending.

## Next

Prioritize root-cause bounding, partial-state reconciliation, canary validation, and safe worker restoration over low-priority research/cleanup until HUMAN-20260925-002 completion criteria are satisfied.
