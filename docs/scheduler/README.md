# SparkBrain Scheduler Policy Layout

This directory contains the durable repository-side policy used by SparkBrain scheduled workers.

## Bootstrap order

Every SparkBrain scheduler run must:

1. fetch `AGENTS.md` explicitly from `main`;
2. fetch `docs/scheduler/COMMON.md` from `main`;
3. fetch `docs/scheduler/SCIENTIFIC_INTEGRITY.md` from `main`;
4. fetch its own role file under `docs/scheduler/roles/` from `main`;
5. read `docs/scheduler/ACTIVE_POLICY.md` and then fetch only the active Human Directives applicable to that role;
6. re-fetch the current role-owned and dependency state from their authoritative refs.

Repository policy comes from `main`. Code, scientific objects, evidence, and operational mailboxes remain on their authorized exact refs. A `main` update does not by itself authorize merging or rebasing a working branch.

## Policy vs procedure

- `AGENTS.md`: repository-wide always-on policy.
- `docs/scheduler/*.md`: scheduler governance and role authority.
- `.agents/skills/*`: procedural workflows loaded only when relevant.
- `ops/*`: control-plane mailboxes and moving state; never repository snapshots.
- scientific evidence / immutable refs: authoritative scientific records.

The scheduler prompt should stay small and point here instead of duplicating these documents.
