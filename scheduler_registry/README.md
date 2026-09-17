# SparkBrain Scheduler Registry

This branch is the Git-backed registry for **ChatGPT scheduler definitions** used by the SparkBrain programme.

It is separate from:

- scientific evidence;
- scheduler run reports / handoffs;
- scheduler execution state;
- Human Directives.

## Why this branch exists

ChatGPT currently exposes the current automation definitions and timestamps, but the available scheduler interface does not expose a reliable version-by-version history of prior prompt/schedule definitions.

The existing `ops/*` branches preserve **run outputs and control-plane handoffs**, not the scheduler definition that produced each run.

Therefore this branch bootstraps the current scheduler fleet and becomes the durable definition/change history from this point forward.

## Historical boundary

Registry history begins on **2026-09-18 JST**.

Earlier scheduler versions are **not reconstructed by guesswork**. Old one-time scheduler-sync tasks or conversation records may provide partial historical clues, but they are not treated as a complete scheduler-version ledger.

## Managed fleet

The registry currently manages the seven enabled SparkBrain schedulers:

1. SparkBrain Control & Repository Steward
2. SparkBrain Evidence Analyst
3. SparkBrain Research Orchestrator
4. SparkBrain Research Orchestrator Relay
5. SparkBrain Research Orchestrator Sub
6. SparkBrain External Research & Audit
7. SparkBrain 現在状態ブリーフ

Disabled legacy/maintenance tasks may be recorded separately, but they are not part of the current seven-task fleet.

## Directory contract

- `scheduler_registry/current/manifest.json`
  - current fleet metadata and task IDs.
- `scheduler_registry/current/<task-id>.md`
  - exact current scheduler definition: title, enabled state, timing mode, timezone, schedule, prompt.
- `scheduler_registry/history/YYYY-MM-DD/`
  - append-only scheduler-change records.
- `scheduler_registry/history/YYYY-MM-DD/<timestamp>-bootstrap.md`
  - initial fleet bootstrap snapshot.
- `scheduler_registry/README.md`
  - this governance contract.

Git commit history is useful, but append-only history records are mandatory so scheduler changes remain explicit even if the `current/` files are replaced.

## Update transaction

Every future SparkBrain scheduler mutation should follow this sequence:

1. Read the live ChatGPT scheduler definition.
2. Read the registry current snapshot.
3. Reconcile drift before changing anything.
4. Write an append-only **PRE_CHANGE** record containing the exact live "before" definition and intended change.
5. Only after PRE_CHANGE persistence succeeds, mutate the ChatGPT scheduler.
6. Re-read the live scheduler.
7. Replace `current/<task-id>.md` and update `manifest.json`.
8. Append **APPLIED** history with exact before/after definitions and reason.
9. If the scheduler update fails, append **FAILED** and leave the current snapshot unchanged.
10. If ChatGPT updates successfully but Git post-persistence fails, report `REGISTRY_OUT_OF_SYNC` and reconcile before any later scheduler mutation.

This order intentionally makes the Git history a prerequisite for scheduler mutation rather than a best-effort afterthought.

## Scope

A scheduler change includes:

- prompt/instruction changes;
- schedule/cadence changes;
- title changes;
- enabled/disabled changes;
- timing-mode changes;
- timezone changes;
- replacement/consolidation of a scheduler;
- creation of a new SparkBrain scheduler;
- retirement of an existing SparkBrain scheduler.

Ordinary run-time output does not count as a scheduler-definition change.

## Authority

This registry records what the scheduler definition is and how it changed. It does not itself authorize scientific execution or reinterpret scientific results.

Scheduler definitions on the ChatGPT automation service remain the live execution authority; this branch is the durable mirrored history and reconciliation source.
