# Control Brain R108 — P0 mutation recurrence recovery backfill

- generation_id: `CTRL-RECOVERY-20260928T123100+0900-R108-P0-MUTATION-RECURRENCE-BACKFILL`
- produced_at: `2026-09-28T12:31:00+09:00`
- mode: `CONTROL_BRAIN`
- recovery_backfill: `true`
- reconstructed_generations: `R107, R108`
- original_payload_available: `false`
- directive delta: none
- incident: `INC-GITHUB-MUTATION-RECURRENCE-20260928-001`

## Decision

The old `INC-GITHUB-PERSISTENCE-20260925-001` record remains closed. New post-closure evidence is registered as a separate recurrence incident.

M1-002 remains exact head `2a21d3e879f1db4e81a58273180ad2124e823a5e`, built and bounded-functionally verified, with no comparative/scientific credit. Evidence Analyst R166 retains exact-head PR/conditional-merge authority. The current critical blocker is operational GitHub PR/mutation routing.

Methodology R140 and Utility R164 missing operational state have now been recovered. No scheduler definition, cadence or enabled state was changed by this backfill.

## P0

Repository-wide GitHub outage is not supported. Intermittent/path-dependent scheduler/runtime GitHub mutation refusal is supported by repeated observations across MAIN, Analyst, Utility, Methodology and Control.

P0 recurrence remains OPEN for bounded recovery and fresh-state retry. Scientific hard floors are unchanged.
