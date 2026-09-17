---
name: human-directives
description: Add, revise, withdraw, or inspect human-originated SparkBrain directives by writing only to the dedicated ops/human-directives branch. Use when the user says things like "Human Directiveに追加", "人間側の意図に入れて", "この方針をControl Brainに検討させたい", or asks to update/review the human directive channel.
---

# SparkBrain Human Directive workflow

Use this skill to maintain the human-originated proposal channel for SparkBrain.

The target branch is always:

`ops/human-directives`

The designated files are:

- `ops/human_directives/README.md`
- `ops/human_directives/active.md`
- append-only files under `ops/human_directives/history/YYYY-MM-DD/`

## Core authority rule

A Human Directive is a **human proposal / intent**, not scientific evidence and not automatic execution authority.

Never present a directive as approved merely because the human requested it.

Control Brain independently classifies active directives as:

- `ACCEPT`
- `MODIFY`
- `DEFER`
- `REJECT`

Human directives never override scientific evidence, immutable/frozen/formal/evidence results, consumed-identity/no-rerun rules, or prospective-integrity constraints.

## Strict write boundary

When using this skill:

- write only to `ops/human-directives`;
- never write Control Brain disposition into this branch;
- never modify `ops/control-brain-handoff`, Evidence Analyst, Orchestrator, Steward, or external-audit branches;
- never modify scheduler/automation definitions;
- never execute the directive itself as part of merely recording it;
- never modify immutable scientific refs;
- never force-push.

The scheduled/control workers treat this branch as read-only.

## Start of every operation

1. Fetch current remote `ops/human-directives`.
2. Read `ops/human_directives/README.md`.
3. Read the latest `ops/human_directives/active.md`.
4. Read relevant history entries when revising, withdrawing, or resolving ambiguity.
5. Re-fetch the exact file immediately before every write and reconcile concurrent changes.
6. Preserve the user's intended meaning. Do not silently strengthen, weaken, or scientifically reinterpret it.

If the branch is missing, stop and report that the human-directive channel has not been initialized. Do not substitute another branch.

## Supported operations

### 1. Inspect / list

When the user asks what human directives exist:

- read `active.md`;
- return the active IDs, short titles, human status, and concise intent;
- do not treat Control Brain disposition as part of the human branch unless separately requested from Control Brain state.

No write is required.

### 2. Add a directive

When the user asks to add a new human directive:

1. Determine today's Asia/Tokyo date.
2. Allocate a new ID:
   `HUMAN-YYYYMMDD-NNN`
3. Determine `NNN` from existing IDs for that date; never reuse an ID.
4. Append a new section to `active.md`.
5. Create an append-only history file:
   `ops/human_directives/history/YYYY-MM-DD/<ID>-<short-slug>.md`
6. Commit directly to `ops/human-directives`.

The active entry should contain, as applicable:

- directive ID and concise title;
- `Human status: OPEN`;
- created date;
- human intent;
- important context/constraints explicitly supplied by the human;
- desired end state;
- explicit non-goals or things not to touch;
- preferred implementation/routing if the human stated one;
- `Required independent review` stating that Control Brain may ACCEPT/MODIFY/DEFER/REJECT it.

Do not invent scientific rationale that the user did not supply.

### 3. Revise a directive

When the user modifies an existing directive:

1. Keep the same directive ID.
2. Read the current active entry and relevant history.
3. Update only the current representation in `active.md`.
4. Never rewrite or delete old history.
5. Append a new history file with a revision suffix or timestamp, recording:
   - what the human changed;
   - what remained unchanged;
   - the new intended wording/state.
6. Commit directly to `ops/human-directives`.

If the user's revision materially supersedes the original goal, preserve the old history and clearly label the active entry as revised rather than pretending the original never existed.

### 4. Withdraw a directive

When the human explicitly withdraws a directive:

1. Append a history record marking explicit human withdrawal.
2. Remove it from the active-directive section of `active.md` or move it to a clearly non-active withdrawn section if that file already uses one.
3. Do not delete prior history.
4. Do not alter Control Brain's historical disposition records.
5. Commit directly to `ops/human-directives`.

Withdrawal means "the human no longer proposes this"; it does not rewrite past scientific or strategic history.

### 5. Replace / supersede

When the human says a new directive replaces an older one:

- create a fresh directive ID for the new proposal if the underlying goal materially changes;
- append history to the old directive stating it was superseded by the new ID;
- remove the old directive from active consideration;
- never reuse the old ID for a materially different proposal.

For small scope/wording changes, revise in place instead.

## Writing style

Human Directive files should be concise, operational, and faithful to the user's wording.

Prefer sections such as:

- `Intent`
- `Context / constraints`
- `Desired end state`
- `Explicit non-goals`
- `Human preference`
- `Required independent review`

Avoid turning a human proposal into a long research essay.

## Control Brain interaction

This skill does **not** ask Control Brain to accept the directive and does not write its decision.

The normal control path is:

`Human Directive -> Control Brain independent review -> Evidence Analyst / Repository Steward / Orchestrator as appropriate`

Control Brain may reject the human proposal.

If the user explicitly asks for immediate Control Brain review in the same task, record the Human Directive first, then inspect the normal Control Brain mechanism separately. Do not write an artificial ACCEPT decision on the human branch.

## Direct-write semantics

Direct writes to `ops/human-directives` are intentional: this branch is the human-input mailbox, not a code-integration branch.

Do not open a PR merely to record a directive unless the user explicitly requests a review workflow for the human-input branch.

The repository skill itself may live on `main`, but directive content belongs only on `ops/human-directives`.

## Completion report

After a write, report only what matters:

- operation: added / revised / withdrawn;
- directive ID;
- branch: `ops/human-directives`;
- exact commit SHA(s);
- one-line summary of what is now proposed;
- remind that Control Brain still independently reviews it.

## Invocation examples

```text
Use $human-directives. Add this as a new Human Directive:
CXで作った比較モデル群のうち、結果非依存で再利用可能なものをmain共通基盤へ統合したい。
```

```text
Use $human-directives. Revise HUMAN-20260918-001:
G8は一旦除外して、G3/G6/G7と共通contractだけを優先候補にしたい。
```

```text
Use $human-directives. Show me the currently active Human Directives.
```

```text
Use $human-directives. Withdraw HUMAN-20260918-001.
```
