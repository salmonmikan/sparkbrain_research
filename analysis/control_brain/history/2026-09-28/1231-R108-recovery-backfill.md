# Control Brain R108 — P0 GitHub mutation recurrence RECOVERY_BACKFILL

- recovery_generated_at: `2026-09-28T12:31:00+09:00`
- original_generation: `R108`
- original_payload_available: `false`
- mode: `CONTROL_BRAIN`
- new_scientific_result: `false`
- recurrence_incident: `INC-GITHUB-MUTATION-RECURRENCE-20260928-001`

## Recovery provenance

R108 completed an operational Control assessment but its publication failed before a branch ref update. This record is reconstructed from the unpersisted user-facing R108 report under explicit user authorization. It is not a byte-for-byte recovery of the unpublished payload.

## Decision

The prior incident `INC-GITHUB-PERSISTENCE-20260925-001` remains historically closed and is not rewritten. Newer evidence constitutes a recurrence and is tracked under a new incident.

M1-002 remains built and bounded-functionally verified at exact head `2a21d3e879f1db4e81a58273180ad2124e823a5e`, with no comparative support, no established composition contribution, no scientific novelty, and scientific credit 0. The critical blocker is operational PR mutation routing, not implementation, CI, review, or science.

Evidence accumulated across MAIN, Evidence Analyst, Utility, Methodology and Control shows that GitHub reads are stable and some Git-data writes succeed, while authorized mutations can be refused before GitHub. This does not support a repository-wide GitHub outage. It supports an intermittent or path-dependent scheduler/runtime GitHub mutation reliability recurrence.

## Original R108 persistence failure

The original R108 Control publication exhausted its five-attempt purpose budget. The user-facing report recorded:
- an initial tool/orchestration-limit failure before ref update;
- multiple pre-GitHub safety/runtime refusals;
- a later attempt in which a history blob was created but subsequent mutation was refused;
- no atomic commit/ref update;
- durable Control state therefore remained R106.

No partial Control state became authoritative.

## Fleet / scheduler boundary

No scheduler was created, replaced, enabled, disabled or otherwise changed by R108. The recovery operation likewise does not change scheduler definitions or cadence.

## Current reconciliation

After separate user-authorized recovery, Methodology R140 is durable at `0102ca2c537a4fb9704f4b3d2def933d7d56f152` and Utility R164 failed-closed state is durable at `df5de71f2f5788272d04001a9e6cf3f9957a9920`.

Evidence Analyst R166 is durable at `46c93259af8ec986fd8465ed5f5cf8fe893cb2e5`; MAIN R172 is durable at `1dedab2a37411efa4e3ae222255910fa8c82856e`.

## Hard floor

Canonical science remains 35/35 terminal with eight consumed FORMAL identities. No scientific execution, rerun, retune, rescore, terminal reopen, evidence mutation or scientific credit is created by this recovery.
