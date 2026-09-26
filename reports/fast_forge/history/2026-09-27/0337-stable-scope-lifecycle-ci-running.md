# Fast Forge history — stable-scope lifecycle prototype

- generation_id: `FORGE-20260927T0337+0900-STABLE-SCOPE-LIFECYCLE-CI-RUNNING`
- produced_at: `2026-09-27T03:37:00+09:00`
- forge_id: `FORGE-STABLE-SCOPE-LIFECYCLE-A`
- status: `FORGE_PROTOTYPE`
- branch: `forge/20260927-stable-scope-lifecycle-a`
- prototype_head: `d52bb83041abc719f94d4f11e7cbad585ad37fc8`
- evidentiary_status: `NON_EVIDENTIARY`
- scientific_credit: `0`

## Why now

The previous stable-scope prototype was useful but left one explicit limitation: scope-token lifetime was entirely external, so accidental reuse of a retired token could intentionally recover old late-evidence support. This run tested the smallest ordinary engineering guard against that failure mode without touching SB001 or canonical science.

## Prototype

Added a wrapper that:
- closes exactly one Assembly + scope-token namespace;
- discards accumulated support for that namespace;
- persists a closed-token tombstone;
- rejects reuse of the retired token for that Assembly;
- permits a fresh token to start clean;
- preserves same-token independence across different Assemblies;
- serializes/replays the lifecycle boundary through JSON.

Files:
- `forge_prototypes/managed_scope_hypothesis_revision.py`
- `tests/test_forge_managed_scope_hypothesis_revision.py`

## Reduction / claim boundary

This is ordinary session/cache lifecycle and tombstoning. It does not establish a new memory mechanism, emergent context identity, or scientific novelty. A future SYSTEM_BUILD would still need to define scope issuance/closure prospectively and without privileged evaluator information.

## Collision / authority

Evidence Analyst R140 still allocates SB001 integration only; MAIN R153 owns that integration attempt and reported a current-run pre-GitHub merge refusal. SB001 branch/PR and all scientific refs were untouched.

HUMAN-20260927-001 (RV02) was observed but not executed: it explicitly routes through Control/Evidence Analyst review, and R140 contains no RV02 allocation.

## P0 observation

Prototype publication used a new isolated Forge branch. Non-force `update_ref` attempt 1 was blocked by OpenAI safety checks before GitHub; after fresh branch readback, attempt 2 succeeded and readback verified `d52bb83041abc719f94d4f11e7cbad585ad37fc8`. This repeats the intermittent/context-selective mutation pattern but does not prove its internal cause.

## CI

Push CI run `36263166258` is currently in progress on exact prototype head `d52bb83041abc719f94d4f11e7cbad585ad37fc8`. No handoff is proposed until CI completes successfully.

New scientific result: none.
