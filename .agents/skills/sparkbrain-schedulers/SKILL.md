---
name: sparkbrain-schedulers
description: Inspect, create, update, enable, disable, consolidate, or otherwise change SparkBrain ChatGPT schedulers while transactionally versioning every scheduler definition change in the ops/scheduler-registry branch. Use for any SparkBrain scheduler/task/automation maintenance request.
---

# SparkBrain scheduler maintenance with Git-backed history

Use this skill for **every mutation of a SparkBrain ChatGPT scheduler**.

The live ChatGPT automation service is the execution authority. The Git branch below is the durable definition/change-history mirror:

`ops/scheduler-registry`

Registry paths:

- `scheduler_registry/README.md`
- `scheduler_registry/current/manifest.json`
- `scheduler_registry/current/<task-id>.md`
- append-only `scheduler_registry/history/YYYY-MM-DD/`

## Core rule

Never mutate a SparkBrain scheduler first and "document it later".

Scheduler changes are a transaction:

`LIVE BEFORE -> GIT PRE_CHANGE -> CHATGPT MUTATION -> LIVE AFTER -> GIT APPLIED`

If the PRE_CHANGE Git record cannot be persisted, **do not mutate the scheduler**.

## What counts as a scheduler mutation

Use this workflow for:

- prompt/instruction changes;
- schedule/cadence changes;
- timing mode changes;
- timezone changes;
- title changes;
- enable/disable changes;
- creation of a new SparkBrain scheduler;
- replacement or consolidation of existing SparkBrain schedulers;
- retirement of an existing scheduler.

Ordinary scheduler runs and run-output persistence are not definition changes.

## Managed fleet discovery

Do not assume the fleet size or task IDs from memory.

At the start:

1. inspect current ChatGPT automations;
2. identify SparkBrain-related tasks;
3. read `ops/scheduler-registry/scheduler_registry/current/manifest.json`;
4. match tasks primarily by immutable task ID, not title;
5. report any live-vs-registry drift before the requested mutation.

Disabled legacy/maintenance SparkBrain tasks may exist. Do not silently treat them as active fleet members.

## Live definition fields

For history purposes capture at minimum:

- task ID;
- title;
- enabled state;
- prompt;
- schedule;
- timing mode;
- timezone;
- live `updated_at` when available.

Preserve the exact prompt text. Do not summarize prompt bodies in the current definition file.

## Drift reconciliation before a requested change

If the live scheduler differs from `scheduler_registry/current/<task-id>.md` before the requested mutation:

1. stop treating the registry current file as authoritative;
2. preserve the registry version as the last known Git snapshot;
3. append a `RECONCILIATION` history record describing the detected drift;
4. update the current file to the exact live definition;
5. update the manifest;
6. only then begin the requested scheduler-change transaction.

Do not guess how or when unregistered drift occurred.

## Existing scheduler update transaction

For each scheduler being changed:

### Phase 1 — PRE_CHANGE

1. Re-read the exact live scheduler definition.
2. Re-read the registry current file and manifest.
3. Confirm there is no unresolved drift.
4. Create an append-only history record with status `PRE_CHANGE`.
5. The record must contain:
   - timestamp in Asia/Tokyo;
   - task ID/title;
   - reason/user request;
   - exact before definition or a content-complete reference to the immutable Git commit containing it;
   - intended fields to change;
   - intended after values;
   - actor/context when useful.
6. Commit PRE_CHANGE to `ops/scheduler-registry`.
7. Verify the PRE_CHANGE write succeeded.

If this write fails, STOP. Do not call the scheduler mutation.

### Phase 2 — mutate live ChatGPT scheduler

1. Re-check that the target task ID is still the same live object.
2. Apply only the requested change.
3. Do not make unrelated cadence/prompt edits.
4. If the live update fails, append a `FAILED` history record when possible and leave registry current unchanged.

### Phase 3 — APPLIED

After a successful live mutation:

1. Re-read the live scheduler definition.
2. Verify the requested change actually took effect.
3. Replace `scheduler_registry/current/<task-id>.md` with the exact new definition.
4. Update the matching entry in `current/manifest.json`.
5. Append an `APPLIED` history record containing:
   - PRE_CHANGE record reference;
   - exact before definition reference;
   - exact after definition;
   - live updated_at;
   - fields changed;
   - reason;
   - any validation notes.
6. Commit the registry update.

If ChatGPT mutation succeeds but Phase 3 Git persistence fails:

- report `REGISTRY_OUT_OF_SYNC`;
- do not perform any additional SparkBrain scheduler mutation;
- reconcile the registry from the live scheduler before future changes.

## Creating a new SparkBrain scheduler

Before creation:

1. write a PRE_CHANGE/CREATE_INTENT history record with proposed title, prompt, schedule, timing mode, timezone, and purpose;
2. verify the Git write;
3. create the ChatGPT scheduler;
4. re-read the created task and obtain its real task ID;
5. add `current/<new-task-id>.md`;
6. add it to manifest;
7. append APPLIED/CREATED history.

Never invent the task ID in Git before ChatGPT creates it.

## Enable / disable

Enabled-state changes are scheduler-definition changes and require the same transaction.

Do not delete historical current/history files when a task is disabled. Mark the new current state with `enabled: false`.

## Consolidation / replacement

When multiple tasks are consolidated:

- preserve every old task's history;
- record which task IDs were disabled/replaced;
- record the surviving/new task ID;
- do not reuse an old task ID as though it were a new scheduler;
- capture schedule and prompt changes separately enough to audit.

## History filenames

Prefer:

`scheduler_registry/history/YYYY-MM-DD/HHMMSS-<task-id>-<status>.md`

where status is one of:

- `PRE_CHANGE`
- `APPLIED`
- `FAILED`
- `RECONCILIATION`
- `CREATED`
- `DISABLED`
- `CONSOLIDATED`

History is append-only. Never rewrite an old history record to make later events look cleaner.

## Current definition format

Each `current/<task-id>.md` must contain:

- task ID;
- title;
- enabled;
- timing mode;
- timezone;
- updated_at;
- full iCal schedule;
- exact full prompt.

This is deliberately verbose: Git diff should show precisely what instruction changed.

## Registry branch semantics

`ops/scheduler-registry` is a control-plane definition ledger, not a scientific source-of-truth branch and not a repository snapshot.

Scheduled SparkBrain workers do not need to write this branch during ordinary runs.

Do not merge/rebase this ops branch into main merely to synchronize repository contents.

## Interaction with repository skills

The repository skill lives on `main`, but scheduler registry content lives only on `ops/scheduler-registry`.

Do not store live scheduler definitions on main.

## Safety / scientific boundaries

Scheduler-history maintenance must not:

- reinterpret scientific evidence;
- modify immutable/frozen/formal/evidence refs;
- rerun consumed identities;
- broaden a scheduler's research authority unless the requested scheduler change explicitly does so;
- use repository history as justification for changing scientific results.

When a scheduler prompt change would alter scientific authority or one-way integrity, call that out explicitly in the change record.

## Completion report

After scheduler maintenance, report:

- task IDs/titles changed;
- exact live fields changed;
- PRE_CHANGE Git commit;
- scheduler update success/failure;
- APPLIED/FAILED Git commit;
- registry sync status;
- unchanged related schedulers when relevant.

If no mutation was needed, say so and do not create meaningless history noise.

## Invocation examples

```text
Use $sparkbrain-schedulers. Change Evidence Analyst from hourly to every 2 hours without changing its prompt.
```

```text
Use $sparkbrain-schedulers. Add this paragraph to the MAIN Orchestrator prompt and preserve full before/after history.
```

```text
Use $sparkbrain-schedulers. Disable the old duplicate SUB scheduler and record the retirement.
```

```text
Use $sparkbrain-schedulers. Show the seven active SparkBrain scheduler definitions and whether Git registry matches live ChatGPT state.
```
